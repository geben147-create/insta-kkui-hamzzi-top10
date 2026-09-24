"""EDL(JSON) -> FFmpeg render: exact cut points, xfade transitions, KR/EN/JP ASS subtitles, audio mix, loudness.

Usage:  python edl_render.py edl_rank2.json            (clips/, fonts/, sfx/, music/ live next to the EDL)
        python edl_render.py edl_rank2.json --dry-run  (writes subs.ass + graph.txt only)
"""
import json, os, subprocess, sys

NOWIN = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def run(cmd, cwd=None, timeout=3600):
    return subprocess.run(cmd, cwd=cwd, stdin=subprocess.DEVNULL, capture_output=True,
                          creationflags=NOWIN, timeout=timeout)


def has_audio(path):
    out = run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index",
               "-of", "csv=p=0", path]).stdout.strip()
    return bool(out)


def ass_time(t):
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def ass_style(name, font, size, outline, shadow, bold=-1):
    return (f"Style: {name},{font},{size},&H00FFFFFF,&H00FFFFFF,&H30000000,&H90000000,{bold},0,0,0,"
            f"100,100,0,0,1,{outline},{shadow},5,20,20,0,1")


def write_ass(edl, path):
    st, W, H = edl["subs"]["style"], edl["w"], edl["h"]
    lines = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 2",
             "ScaledBorderAndShadow: yes", "", "[V4+ Styles]",
             "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, "
             "Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
             "Alignment, MarginL, MarginR, MarginV, Encoding",
             ass_style("KR", st["kr_font"], st["kr_size"], st["outline"], st["shadow"]),
             ass_style("EN", st["en_font"], st["en_size"], st["outline"] * 0.8, st["shadow"]),
             ass_style("JP", st["jp_font"], st["jp_size"], st["outline"] * 0.8, st["shadow"]),
             "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    x = W // 2
    for ev in edl["subs"]["events"]:
        for key, dy in (("kr", 0), ("en", st["en_dy"]), ("jp", st["jp_dy"])):
            if ev.get(key):
                y = round((st["kr_y"] + dy) * H)
                lines.append(f"Dialogue: 0,{ass_time(ev['t0'])},{ass_time(ev['t1'])},{key.upper()},,0,0,0,,"
                             f"{{\\pos({x},{y})}}{ev[key]}")
    with open(path, "w", encoding="utf-8-sig") as f:
        f.write("\n".join(lines) + "\n")


def plan(edl):
    shots = edl["shots"]
    for i, s in enumerate(shots):
        tr_out = s.get("out", {"type": "cut"}) if i < len(shots) - 1 else {"type": "cut"}
        s["_dout"] = 0.0 if tr_out["type"] == "cut" else float(tr_out.get("dur", 0.1))
        s["_tout"] = tr_out
        s["_din"] = shots[i - 1]["_dout"] if i else 0.0
        s["_dur"] = s["t1"] - s["t0"]
        pre, post = s["_din"] / 2, s["_dout"] / 2
        s["_in"] = max(float(s.get("in", 0.0)), pre)
        s["_L"] = s["_dur"] + pre + post
        s["_src0"] = s["_in"] - pre
    return shots


def video_graph(edl, shots):
    W, H, FPS, g, segs = edl["w"], edl["h"], edl["fps"], [], []
    for i, s in enumerate(shots):
        z = float(s.get("push", 0))
        zoom = (f",scale=w='trunc({W}*(1+{z}*t/{s['_L']:.3f})/2)*2':h='trunc({H}*(1+{z}*t/{s['_L']:.3f})/2)*2'"
                f":eval=frame,crop={W}:{H}") if z else ""
        parts = [p for p, need in (("h", s["_din"] > 0), ("b", True), ("t", s["_dout"] > 0)) if need]
        g.append(f"[{i}:v]trim=start={s['_src0']:.3f}:end={s['_src0'] + s['_L']:.3f},setpts=PTS-STARTPTS,"
                 f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setsar=1,"
                 f"format=yuv420p{zoom},split={len(parts)}" + "".join(f"[s{i}{p}]" for p in parts))
        pre, post, L = s["_din"] / 2, s["_dout"] / 2, s["_L"]
        if "h" in parts:
            g.append(f"[s{i}h]trim=end={s['_din']:.3f},setpts=PTS-STARTPTS[h{i}]")
        g.append(f"[s{i}b]trim=start={2 * pre:.3f}:end={L - 2 * post:.3f},setpts=PTS-STARTPTS[b{i}]")
        if "t" in parts:
            g.append(f"[s{i}t]trim=start={L - s['_dout']:.3f},setpts=PTS-STARTPTS[t{i}]")
    for i, s in enumerate(shots):
        segs.append(f"[b{i}]")
        if s["_dout"] > 0:
            g.append(f"[t{i}][h{i + 1}]xfade=transition={s['_tout']['type']}:duration={s['_dout']:.3f}:offset=0[x{i}]")
            segs.append(f"[x{i}]")
    g.append("".join(segs) + f"concat=n={len(segs)}:v=1:a=0[vcat]")
    if edl.get("subs", {}).get("events"):
        g.append("[vcat]ass=subs.ass:fontsdir=fonts[vout]")
    else:
        g.append("[vcat]null[vout]")
    return g


def audio_graph(edl, shots, base, total):
    au, g, mix, n = edl.get("audio", {}), [], [], len(shots)
    for i, s in enumerate(shots):
        path = os.path.join(base, edl["clips_dir"], s["file"])
        if au.get("clip_gain", 1.0) > 0 and has_audio(path):
            g.append(f"[{i}:a]atrim=start={s['_in']:.3f}:end={s['_in'] + s['_dur']:.3f},asetpts=PTS-STARTPTS,"
                     f"aresample=48000,aformat=channel_layouts=stereo,apad,atrim=end={s['_dur']:.3f}[a{i}]")
        else:
            g.append(f"anullsrc=r=48000:cl=stereo,atrim=end={s['_dur']:.3f}[a{i}]")
    g.append("".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1,volume={au.get('clip_gain', 1.0)}[clip]")
    k = n
    if au.get("music"):
        g.append(f"[{k}:a]atrim=end={total:.3f},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,"
                 f"volume={au.get('music_gain_db', -10)}dB,afade=t=in:d=0.3,afade=t=out:st={max(0, total - 0.8):.3f}:d=0.8[mus]")
        if au.get("duck"):
            g.append("[clip]asplit=2[clip][sc]")
            g.append("[mus][sc]sidechaincompress=threshold=0.04:ratio=6:attack=15:release=350[musd]")
            mix.append("[musd]")
        else:
            mix.append("[mus]")
        k += 1
    mix.insert(0, "[clip]")
    for j, fx in enumerate(au.get("sfx", [])):
        ms = int(round(fx["t"] * 1000))
        g.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,adelay=delays={ms}:all=1,"
                 f"volume={fx.get('gain_db', 0)}dB[fx{j}]")
        mix.append(f"[fx{j}]")
        k += 1
    g.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:dropout_transition=0,"
             f"apad,atrim=end={total:.3f},loudnorm=I={au.get('lufs', -14)}:TP={au.get('tp', -1.0)}:LRA=11,"
             f"aresample=48000[aout]")
    return g


def main(edl_path, dry=False):
    base = os.path.dirname(os.path.abspath(edl_path))
    edl = json.load(open(edl_path, encoding="utf-8"))
    shots = plan(edl)
    total = shots[-1]["t1"] - shots[0]["t0"]
    if edl.get("subs", {}).get("events"):
        write_ass(edl, os.path.join(base, "subs.ass"))
    graph = video_graph(edl, shots) + audio_graph(edl, shots, base, total)
    open(os.path.join(base, "graph.txt"), "w", encoding="utf-8").write(";\n".join(graph))
    cmd = ["ffmpeg", "-y", "-hide_banner"]
    for s in shots:
        cmd += ["-i", os.path.join(edl["clips_dir"], s["file"])]
    au = edl.get("audio", {})
    if au.get("music"):
        cmd += ["-i", au["music"]]
    for fx in au.get("sfx", []):
        cmd += ["-i", fx["file"]]
    cmd += ["-filter_complex", ";".join(graph), "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(edl["fps"]),
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart",
            "-t", f"{total:.3f}", edl.get("output", "out.mp4")]
    print(f"shots={len(shots)} total={total:.3f}s transitions={sum(1 for s in shots if s['_dout'] > 0)}")
    for s in shots:
        if float(s.get("in", 0.0)) < s["_din"] / 2:
            print(f"  note: {s['id']} in-point moved to {s['_in']:.3f}s to make room for the incoming transition")
    if dry:
        return 0
    r = run(cmd, cwd=base)
    if r.returncode:
        print(r.stderr.decode("utf-8", "ignore")[-3000:])
        return r.returncode
    print("wrote", os.path.join(base, edl.get("output", "out.mp4")))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], "--dry-run" in sys.argv))
