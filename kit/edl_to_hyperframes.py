"""EDL(JSON) -> HyperFrames standalone composition (index.html) with the same cuts, transitions, captions, audio.

Usage: python edl_to_hyperframes.py edl_rank2_chuseok.json out_dir
Then:  cd out_dir && npx hyperframes check   (copy clips/ fonts/ sfx/ music/ next to index.html first)
"""
import html, json, os, sys

TRANSITION_JS = {
    "fade": "tl.fromTo('#in-{b}', {{opacity: 0}}, {{opacity: 1, duration: {d}, ease: 'none'}}, {w0});",
    "fadewhite": ("tl.set('#in-{b}', {{opacity: 0}}, 0);"
                  "tl.fromTo('#flash-{a}', {{opacity: 0}}, {{opacity: 1, duration: {h}, ease: 'power1.in'}}, {w0});"
                  "tl.set('#in-{b}', {{opacity: 1}}, {c});"
                  "tl.to('#flash-{a}', {{opacity: 0, duration: {h}, ease: 'power1.out'}}, {c});"),
    "hblur": ("tl.set('#in-{b}', {{opacity: 0}}, 0);"
              "tl.fromTo('#in-{a}', {{xPercent: 0, filter: 'blur(0px)'}}, {{xPercent: -22, filter: 'blur(26px)', duration: {h}, ease: 'power2.in'}}, {w0});"
              "tl.set('#in-{b}', {{opacity: 1}}, {c});"
              "tl.fromTo('#in-{b}', {{xPercent: 22, filter: 'blur(26px)'}}, {{xPercent: 0, filter: 'blur(0px)', duration: {h}, ease: 'power2.out'}}, {c});"),
    "zoomin": ("tl.set('#in-{b}', {{opacity: 0}}, 0);"
               "tl.fromTo('#in-{a}', {{scale: 1, filter: 'blur(0px)'}}, {{scale: 1.35, filter: 'blur(14px)', duration: {h}, ease: 'power2.in'}}, {w0});"
               "tl.set('#in-{b}', {{opacity: 1}}, {c});"
               "tl.fromTo('#in-{b}', {{scale: 1.25, filter: 'blur(14px)'}}, {{scale: 1, filter: 'blur(0px)', duration: {h}, ease: 'power2.out'}}, {c});"),
    "squeezeh": ("tl.set('#in-{b}', {{opacity: 0}}, 0);"
                 "tl.fromTo('#in-{a}', {{scaleX: 1}}, {{scaleX: 1.9, duration: {h}, ease: 'power2.in'}}, {w0});"
                 "tl.set('#in-{b}', {{opacity: 1}}, {c});"
                 "tl.fromTo('#in-{b}', {{scaleX: 1.9}}, {{scaleX: 1, duration: {h}, ease: 'power2.out'}}, {c});"),
}


def r3(x):
    return f"{x:.3f}".rstrip("0").rstrip(".") if x else "0"


def build(edl):
    W, H = edl["w"], edl["h"]
    shots, total = edl["shots"], edl["shots"][-1]["t1"]
    body, js, n = [], ["const tl = gsap.timeline({ paused: true });"], len(shots)
    for i, s in enumerate(shots):
        d_in = 0.0 if i == 0 or shots[i - 1].get("out", {"type": "cut"})["type"] == "cut" else shots[i - 1]["out"]["dur"]
        d_out = 0.0 if i == n - 1 or s.get("out", {"type": "cut"})["type"] == "cut" else s["out"]["dur"]
        start, dur = s["t0"] - d_in / 2, (s["t1"] - s["t0"]) + d_in / 2 + d_out / 2
        media = max(float(s.get("in", 0.0)), d_in / 2) - d_in / 2
        body.append(f'<div class="shot" id="shot-{s["id"]}"><div class="inner" id="in-{s["id"]}">'
                    f'<video id="v-{s["id"]}" class="clip" src="clips/{s["file"]}" data-start="{r3(start)}" '
                    f'data-duration="{r3(dur)}" data-media-start="{r3(media)}" data-track-index="{i % 2}" '
                    f'muted playsinline></video></div></div>')
        if s.get("push"):
            js.append(f"tl.fromTo('#in-{s['id']}', {{scale: 1}}, {{scale: {1 + s['push']}, duration: {r3(dur)}, "
                      f"ease: 'none'}}, {r3(start)});")
        if d_out:
            kind, c = s["out"]["type"], s["t1"]
            if kind == "fadewhite":
                body.append(f'<div class="flash clip" id="flash-{s["id"]}" data-start="{r3(c - d_out / 2)}" '
                            f'data-duration="{r3(d_out)}" data-track-index="30"></div>')
            tpl = TRANSITION_JS.get(kind, TRANSITION_JS["fade"])
            js.append(tpl.format(a=s["id"], b=shots[i + 1]["id"], d=r3(d_out), h=r3(d_out / 2),
                                 w0=r3(c - d_out / 2), c=r3(c)))
    au = edl.get("audio", {})
    if au.get("clip_gain", 1.0) > 0:
        for i, s in enumerate(shots):
            media = max(float(s.get("in", 0.0)), 0.0)
            body.append(f'<audio id="a-{s["id"]}" src="clips/{s["file"]}" data-start="{r3(s["t0"])}" '
                        f'data-duration="{r3(s["t1"] - s["t0"])}" data-media-start="{r3(media)}" '
                        f'data-track-index="{10 + i}" data-volume="{au.get("clip_gain", 1.0)}"></audio>')
    if au.get("music"):
        vol = round(10 ** (au.get("music_gain_db", -10) / 20), 3)
        pts = [{"t": 0, "v": 0}, {"t": 0.3, "v": vol}]
        for a, b in au.get("duck_ranges", []):
            pts += [{"t": a - 0.2, "v": vol}, {"t": a, "v": round(vol * 0.35, 3)},
                    {"t": b, "v": round(vol * 0.35, 3)}, {"t": b + 0.25, "v": vol}]
        pts += [{"t": total - 0.8, "v": vol}, {"t": total, "v": 0}]
        lane = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": pts}]})
        body.append(f"<audio id=\"music-bed\" src=\"{au['music']}\" data-start=\"0\" data-duration=\"{r3(total)}\" "
                    f"data-track-index=\"40\" data-automation='{lane}'></audio>")
    for j, fx in enumerate(au.get("sfx", [])):
        body.append(f'<audio id="sfx-{j:02d}" src="{fx["file"]}" data-start="{r3(fx["t"])}" data-track-index="{50 + j}" '
                    f'data-volume="{round(10 ** (fx.get("gain_db", 0) / 20), 3)}"></audio>')
    st = edl.get("subs", {}).get("style", {})
    for k, ev in enumerate(edl.get("subs", {}).get("events", [])):
        lines = []
        for key, dy, size in (("kr", 0, st.get("kr_size")), ("en", st.get("en_dy"), st.get("en_size")),
                              ("jp", st.get("jp_dy"), st.get("jp_size"))):
            if ev.get(key):
                top = round((st["kr_y"] + dy) * H - size * 0.62)
                lines.append(f'<p class="{key}" style="top: {top}px; font-size: {size}px">{html.escape(ev[key])}</p>')
        body.append(f'<div class="cap clip" id="cap-{k:02d}" data-start="{r3(ev["t0"])}" '
                    f'data-duration="{r3(ev["t1"] - ev["t0"])}" data-track-index="20">{"".join(lines)}</div>')
    js.append('window.__timelines["main"] = tl;')
    return f"""<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>{html.escape(edl['name'])}</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Pretendard"; src: url("fonts/Pretendard-SemiBold.otf") format("opentype"); font-weight: 600; }}
      @font-face {{ font-family: "Noto Sans JP"; src: url("fonts/NotoSansJP-SemiBold.ttf") format("truetype"); font-weight: 600; }}
      body {{ margin: 0; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #000; }}
      .shot, .inner {{ position: absolute; inset: 0; }}
      .shot video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      .flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; }}
      .cap {{ position: absolute; inset: 0; color: #fff; text-align: center; }}
      .cap p {{ position: absolute; left: 0; right: 0; margin: 0; line-height: 1.2; font-weight: 600;
               text-shadow: 0 0 3px rgba(0, 0, 0, 0.85), 0 2px 4px rgba(0, 0, 0, 0.55); }}
      .cap .kr, .cap .en {{ font-family: "Pretendard", sans-serif; }}
      .cap .jp {{ font-family: "Noto Sans JP", sans-serif; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-width="{W}" data-height="{H}" data-duration="{r3(total)}">
      {chr(10).join('      ' + b for b in body).lstrip()}
    </div>
    <script>
      {chr(10).join('      ' + j for j in js).lstrip()}
    </script>
  </body>
</html>
"""


def self_check(page):
    import re
    ids = re.findall(r'id="([^"]+)"', page)
    problems = [f"duplicate id {i}" for i in set(ids) if ids.count(i) > 1]
    problems += ["audio without id"] if re.search(r"<audio(?![^>]*\bid=)", page) else []
    problems += ["crossorigin present"] if "crossorigin" in page else []
    problems += ["<br> present"] if "<br" in page else []
    return problems


if __name__ == "__main__":
    edl = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    page = build(edl)
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(page)
    print(out, "clips:", page.count("<video"), "audio:", page.count("<audio"), "captions:", page.count('class="cap clip"'),
          "self-check:", self_check(page) or "OK")
