"""Smoke test: dummy clips/music/sfx for every EDL, render, then verify duration and cut timing."""
import json, os, shutil, subprocess, sys
import numpy as np

NOWIN = getattr(subprocess, "CREATE_NO_WINDOW", 0)
HERE = os.path.dirname(os.path.abspath(__file__))


def ff(args, cwd):
    r = subprocess.run(["ffmpeg", "-v", "error", "-y"] + args, cwd=cwd, stdin=subprocess.DEVNULL,
                       capture_output=True, creationflags=NOWIN, timeout=600)
    if r.returncode:
        raise RuntimeError(r.stderr.decode("utf-8", "ignore")[-800:])


def probe_dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, stdin=subprocess.DEVNULL, creationflags=NOWIN).stdout
    return float(out.strip())


def cut_times(path, fps):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", "scale=36:64,format=gray", "-f", "rawvideo", "-"],
                         capture_output=True, stdin=subprocess.DEVNULL, creationflags=NOWIN).stdout
    f = np.frombuffer(raw, np.uint8).reshape(-1, 64, 36).astype(np.float32)
    d = np.abs(np.diff(f, axis=0)).mean((1, 2))
    return [round((i + 1) / fps, 3) for i in range(len(d)) if d[i] > 25]


def main(edl_name):
    edl = json.load(open(os.path.join(HERE, edl_name), encoding="utf-8"))
    work = os.path.join(HERE, "_test", edl["name"])
    shutil.rmtree(work, ignore_errors=True)
    for sub in ("clips", "fonts", "sfx", "music"):
        os.makedirs(os.path.join(work, sub), exist_ok=True)
    for src, dst in (("malgunbd.ttf", "malgunbd.ttf"), ("YuGothB.ttc", "YuGothB.ttc")):
        shutil.copy(os.path.join("C:/Windows/Fonts", src), os.path.join(work, "fonts", dst))
    edl["subs"].setdefault("style", {})
    st = edl["subs"]["style"]
    if st:
        st.update({"kr_font": "Malgun Gothic", "en_font": "Malgun Gothic", "jp_font": "Yu Gothic"})
    colors = ["red", "green", "blue", "yellow", "magenta", "cyan", "orange", "purple", "white", "gray"]
    for i, s in enumerate(edl["shots"]):
        L = s["t1"] - s["t0"] + 1.0
        c = colors[i % len(colors)]
        ff(["-f", "lavfi", "-i", f"color=c={c}:s=720x1280:r={edl['fps']}:d={L:.3f}",
            "-f", "lavfi", "-i", f"sine=frequency={300 + 40 * i}:duration={L:.3f}",
            "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", f"clips/{s['file']}"], work)
    au = edl.get("audio", {})
    if au.get("music"):
        ff(["-f", "lavfi", "-i", "sine=frequency=220:duration=60", "-c:a", "libmp3lame", au["music"]], work)
    for fx in au.get("sfx", []):
        ff(["-f", "lavfi", "-i", "sine=frequency=1000:duration=0.4", fx["file"]], work)
    json.dump(edl, open(os.path.join(work, "edl.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    r = subprocess.run([sys.executable, os.path.join(HERE, "edl_render.py"), os.path.join(work, "edl.json")],
                       capture_output=True, stdin=subprocess.DEVNULL, creationflags=NOWIN, timeout=900)
    print(r.stdout.decode("utf-8", "ignore").strip())
    if r.returncode:
        print(r.stderr.decode("utf-8", "ignore")[-1500:])
        return 1
    out = os.path.join(work, edl["output"])
    total = edl["shots"][-1]["t1"]
    got = probe_dur(out)
    expected_cuts = [s["t1"] for s in edl["shots"][:-1]]
    found = cut_times(out, edl["fps"])
    matched = sum(1 for c in expected_cuts if any(abs(c - f) <= 0.3 for f in found))
    print(f"  duration expected {total:.3f}s got {got:.3f}s | cuts matched {matched}/{len(expected_cuts)}")
    return 0


if __name__ == "__main__":
    rc = 0
    for name in sys.argv[1:]:
        rc |= main(name)
    sys.exit(rc)
