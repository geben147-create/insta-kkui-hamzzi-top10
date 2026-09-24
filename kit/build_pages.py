"""Builds report/rank1.html, rank2.html, rank3.html (+ index.html) from analysis data and content modules."""
import html, json, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import common as C
from content_rank1 import RANK1
from content_rank2 import RANK2
from content_rank3 import RANK3

NOWIN = getattr(subprocess, "CREATE_NO_WINDOW", 0)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # insta/
OUT = os.path.join(ROOT, "report")
E = html.escape
TR_COLORS = {"cut": "#8a8f98", "hblur": "#e8590c", "zoomin": "#7048e8", "fade": "#1c7ed6", "fadewhite": "#f59f00",
             "squeezeh": "#d6336c"}


def ff(args):
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + args, stdin=subprocess.DEVNULL, capture_output=True,
                   creationflags=NOWIN, timeout=120)


def palette(path, k=5):
    px = np.asarray(Image.open(path).convert("RGB").resize((60, 107))).reshape(-1, 3).astype(np.float32)
    cen = px[np.random.default_rng(0).choice(len(px), k, replace=False)]
    for _ in range(12):
        lab = np.argmin(((px[:, None] - cen[None]) ** 2).sum(-1), 1)
        cen = np.array([px[lab == i].mean(0) if (lab == i).any() else cen[i] for i in range(k)])
    share = np.bincount(lab, minlength=k) / len(lab)
    return [("#%02x%02x%02x" % tuple(int(v) for v in cen[i]), float(share[i])) for i in np.argsort(-share)]


def frames_for(v, vid, fps):
    os.makedirs(os.path.join(OUT, "img", vid), exist_ok=True)
    src = os.path.join(ROOT, "video", f"{vid}.mp4")
    for sh in v["shots"]:
        pad = min(0.12, (sh["t1"] - sh["t0"]) / 4)
        for tag, t in (("a", sh["t0"] + pad), ("m", (sh["t0"] + sh["t1"]) / 2), ("z", sh["t1"] - pad)):
            dst = os.path.join(OUT, "img", vid, f"{sh['id']}_{tag}.jpg")
            if not os.path.exists(dst):
                ff(["-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", "-vf", "scale=405:720", "-q:v", "4", dst])
        sh["palette"] = palette(os.path.join(OUT, "img", vid, f"{sh['id']}_m.jpg"))
    for k, sh in enumerate(v["shots"][:-1]):
        n = int(round(sh["t1"] * fps))
        dst = os.path.join(OUT, "img", vid, f"tr_{sh['id']}.jpg")
        if not os.path.exists(dst):
            ff(["-i", src, "-vf", f"select='between(n\\,{n - 3}\\,{n + 2})',scale=120:213,tile=6x1",
                "-frames:v", "1", "-fps_mode", "passthrough", "-q:v", "4", dst])


def audio_image(v, vid, dur):
    a = os.path.join(ROOT, "analysis", vid)
    sp, wv = Image.open(f"{a}/spectrum.png").convert("RGB"), Image.open(f"{a}/wave.png").convert("RGB")
    img = Image.new("RGB", (sp.width, sp.height + wv.height + 26), (12, 12, 14))
    img.paste(sp, (0, 0)); img.paste(wv, (0, sp.height))
    d, F = ImageDraw.Draw(img), ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 15)
    for sh in v["shots"][:-1]:
        x = int(sh["t1"] / dur * sp.width); d.line([(x, 0), (x, sp.height + wv.height)], fill=(0, 230, 255), width=2)
    for s in range(int(dur) + 1):
        x = int(s / dur * sp.width); d.text((x + 2, sp.height + wv.height + 4), f"{s}s", font=F, fill=(210, 210, 210))
    img.save(os.path.join(OUT, "img", vid, "audio.jpg"), quality=85)


def tr_kind(sh):
    out = sh.get("out", "")
    if any(w in out for w in ("연속", "없음", "영상 끝")):
        return "none"
    for key, word in (("fadewhite", "플래시"), ("zoomin", "줌"), ("squeezeh", "늘이기"), ("hblur", "휩"),
                      ("hblur", "블러"), ("fade", "디졸브")):
        if word in out:
            return key
    return "cut"


def timeline_svg(v, dur, subs, speech):
    W, pad = 1000, 4
    x = lambda t: pad + t / dur * (W - 2 * pad)
    g = ['<svg class="tl" viewBox="0 0 1000 150" role="img" aria-label="타임라인">']
    for i, sh in enumerate(v["shots"]):
        x0, x1 = x(sh["t0"]), x(sh["t1"])
        g.append(f'<rect x="{x0:.1f}" y="18" width="{max(1, x1 - x0 - 1):.1f}" height="34" rx="3" '
                 f'class="shot{i % 2}"><title>{E(sh["id"])} {sh["t0"]:.2f}–{sh["t1"]:.2f}s {E(sh["name"])}</title></rect>')
        if x1 - x0 > 22:
            g.append(f'<text x="{(x0 + x1) / 2:.1f}" y="40" class="lbl">{E(sh["id"])}</text>')
        if i < len(v["shots"]) - 1:
            k = tr_kind(sh)
            if k == "none":
                continue
            g.append(f'<rect x="{x1 - 3:.1f}" y="12" width="6" height="46" fill="{TR_COLORS[k]}" rx="2">'
                     f'<title>{sh["t1"]:.2f}s {E(sh.get("out", ""))}</title></rect>')
    for ev in subs:
        g.append(f'<rect x="{x(ev["t0"]):.1f}" y="66" width="{x(ev["t1"]) - x(ev["t0"]):.1f}" height="14" rx="3" '
                 f'class="sub"><title>{ev["t0"]:.2f}–{ev["t1"]:.2f}s 자막: {E(ev["kr"])}</title></rect>')
    for seg in speech:
        g.append(f'<rect x="{x(seg["t0"]):.1f}" y="88" width="{max(2, x(seg["t1"]) - x(seg["t0"])):.1f}" height="14" '
                 f'rx="3" class="spk"><title>{seg["t0"]:.1f}–{seg["t1"]:.1f}s 음성: {E(seg["text"])}</title></rect>')
    for s in range(0, int(dur) + 1, 2 if dur > 20 else 1):
        g.append(f'<text x="{x(s):.1f}" y="124" class="tick">{s}s</text>')
    g.append('<text x="4" y="10" class="rowlbl">샷 · 전환</text><text x="4" y="64" class="rowlbl"></text>')
    g.append("</svg>")
    return "".join(g)


def prompt_box(label, template, extra=""):
    t = E(template + extra)
    return (f'<div class="pbox"><div class="phead"><span>{E(label)}</span>'
            f'<button class="copy" type="button">복사</button></div><pre class="prompt" data-tpl="{t}">{t}</pre></div>')


def shot_card(v, sh):
    vid = v["id"]
    imgs = "".join(f'<figure><div class="thirds"><img loading="lazy" src="img/{vid}/{sh["id"]}_{t}.jpg" '
                   f'alt="{E(sh["id"])} {lab}"></div><figcaption>{lab} {tt:.2f}s</figcaption></figure>'
                   for t, lab, tt in (("a", "시작", sh["t0"]), ("m", "중간", (sh["t0"] + sh["t1"]) / 2),
                                      ("z", "끝", sh["t1"])))
    sw = "".join(f'<span class="sw" style="background:{c};flex:{max(0.08, sh_):.2f}" title="{c}"></span>'
                 for c, sh_ in sh["palette"])
    rows = [("샷 크기", sh.get("size")), ("앵글", sh.get("angle")), ("렌즈 느낌", sh.get("lens")),
            ("카메라 무빙", sh.get("move")), ("구도·위치", sh.get("comp")), ("동작·표정", sh.get("action")),
            ("배경·소품", sh.get("bg")), ("조명", sh.get("light")), ("화면 자막", sh.get("text")),
            ("소리", sh.get("sound")), ("다음 전환", sh.get("out"))]
    table = "".join(f"<tr><th>{E(k)}</th><td>{E(val)}</td></tr>" for k, val in rows if val)
    models = "".join(f'<span class="chip" title="{E(C.MODELS[m]["spec"])}"><b>{E(C.MODELS[m]["name"])}</b>'
                     f'<small>{E(C.MODELS[m]["id"])}</small></span>' for m in sh["models"])
    dur = sh["t1"] - sh["t0"]
    prompts = ""
    if sh.get("img"):
        prompts += prompt_box("이미지 프롬프트 (첫 프레임 · 9:16)", sh["img"], ", " + C.STYLE)
    if sh.get("vid"):
        prompts += prompt_box(f"영상 프롬프트 (필요 {dur:.2f}초 → {max(4, int(dur + 1.5))}초 생성)", sh["vid"],
                              " Vertical 9:16, photoreal, keep the character identical to the reference.")
    note = f'<p class="note">💡 {E(sh["note"])}</p>' if sh.get("note") else ""
    return (f'<article class="shot" id="{E(sh["id"])}"><header><span class="sid">{E(sh["id"])}</span>'
            f'<h3>{E(sh["name"])}</h3><span class="time">{sh["t0"]:.2f}–{sh["t1"]:.2f}초 · {dur:.2f}초</span></header>'
            f'<div class="frames">{imgs}</div><div class="palette">{sw}</div>'
            f'<table class="spec">{table}</table><div class="models"><span class="mlabel">추천 모델</span>{models}</div>'
            f'{prompts}{note}</article>')


def section(id_, title, body, lead=""):
    lead_html = f'<p class="lead">{E(lead)}</p>' if lead else ""
    return f'<section id="{id_}"><h2>{E(title)}</h2>{lead_html}{body}</section>'


def cast_block(v):
    presets = [("원본 (기니피그 · 꾸이)", "a chubby anthropomorphic guinea pig with caramel-brown and white fur and a white blaze down the nose", "guinea pig")]
    presets += [(ko, en, en.split("anthropomorphic ")[1].split(" with")[0]) for ko, en in C.CHAR_SWAPS]
    opts = "".join(f'<option value="{i}">{E(p[0])}</option>' for i, p in enumerate(presets))
    cast = "".join(f"<li><code>{E(a)}</code> {E(b)}</li>" for a, b in v.get("cast", [])) or \
        "<li><code>[CHARACTER]</code> 주인공 1명</li>"
    keep = "".join(f"<li>{E(k)}</li>" for k in C.CHAR_KEEP)
    return (f'<div class="swap"><label for="animal">바꿀 동물</label><select id="animal">{opts}</select>'
            f'<label for="custom">직접 입력(선택) — [CHARACTER] 설명을 통째로 교체</label>'
            f'<textarea id="custom" rows="2" placeholder="예: a chubby anthropomorphic white Samoyed puppy with fluffy cream fur"></textarea>'
            f'<p class="small">선택하면 이 페이지의 모든 프롬프트에서 [CHARACTER]·[CHARACTER_2]·[MOM]·[DAD]가 자동으로 바뀝니다.</p></div>'
            f'<div class="two"><div><h4>등장인물 슬롯</h4><ul>{cast}</ul></div><div><h4>동물을 바꿔도 반드시 유지할 것</h4><ul>{keep}</ul></div></div>'
            + prompt_box("캐릭터 시트 프롬프트 (Nano Banana Pro · 가장 먼저)", C.CHAR_SHEET_PROMPT)
            + f'<script id="presets" type="application/json">{json.dumps(presets, ensure_ascii=False)}</script>')


def page(v, others):
    vid = v["id"]
    s = json.load(open(os.path.join(ROOT, "analysis", vid, "shots.json"), encoding="utf-8"))
    au = json.load(open(os.path.join(ROOT, "analysis", vid, "audio.json"), encoding="utf-8"))
    speech = json.load(open(os.path.join(ROOT, "analysis", vid, "speech.json"), encoding="utf-8"))
    edl = json.load(open(os.path.join(ROOT, "kit", v["edl"][0]), encoding="utf-8"))
    dur, fps = s["dur"], s["fps"]
    frames_for(v, vid, fps)
    audio_image(v, vid, dur)
    subs = edl.get("subs", {}).get("events", [])
    kpis = "".join(f'<div class="kpi"><span>{E(k)}</span><b>{E(val)}</b></div>' for k, val in v["stats"])
    viral = "".join(f'<li><span class="when">{E(a)}</span><b>{E(b)}</b><p>{E(c)}</p></li>' for a, b, c in v["viral"])
    legend = "".join(f'<span><i style="background:{c}"></i>{E(n)}</span>' for n, c in
                     (("하드컷", TR_COLORS["cut"]), ("휩/블러", TR_COLORS["hblur"]), ("줌", TR_COLORS["zoomin"]),
                      ("디졸브", TR_COLORS["fade"]), ("흰 플래시", TR_COLORS["fadewhite"]), ("늘이기", TR_COLORS["squeezeh"])))
    tl = (timeline_svg(v, dur, subs, speech) + f'<div class="legend">{legend}<span><i class="isub"></i>화면 자막</span>'
          f'<span><i class="ispk"></i>음성(Whisper)</span></div>')
    shots = "".join(shot_card(v, sh) for sh in v["shots"])
    trs = "".join(f'<tr><td>{E(t["t"])}</td><td>{E(t["type"])}</td><td>{E(t["frames"])}</td><td>{E(t["how"])}</td>'
                  f'<td><code>{E(t["ffmpeg"])}</code></td><td>{E(t["capcut"])}</td><td>{E(t["pro"])}</td></tr>'
                  for t in v["transitions"])
    strips = "".join(f'<figure class="strip"><img loading="lazy" src="img/{vid}/tr_{sh["id"]}.jpg" alt="전환 {sh["t1"]:.2f}초">'
                     f'<figcaption>{sh["t1"]:.2f}초 · {E(sh.get("out", ""))}</figcaption></figure>'
                     for sh in v["shots"][:-1])
    a = v["audio"]
    cues = "".join(f"<tr><td>{E(t)}</td><td>{E(w)}</td><td>{E(h)}</td></tr>" for t, w, h in a["cues"])
    audio_body = (f'<p>{E(a["summary"])}</p><img class="wide" src="img/{vid}/audio.jpg" alt="스펙트로그램·파형과 컷 위치">'
                  f'<p class="small">위: 스펙트로그램(세로 밝은 줄 = 타격음/효과음, 가로 줄무늬 = 목소리·멜로디), 아래: 파형. 하늘색 선 = 컷 위치. '
                  f'측정: {E(au["loudness"]["integrated_lufs"])} LUFS · LRA {E(au["loudness"]["lra_lu"])} · '
                  f'트루피크 {E(au["loudness"]["true_peak_dbfs"])} dBFS</p>'
                  f'<table class="grid"><tr><th>시간(초)</th><th>소리</th><th>메모</th></tr>{cues}</table>'
                  f'<h4>목소리</h4><p>{E(a["voice"])}</p>')
    if a.get("music_prompt"):
        audio_body += prompt_box("배경음악 프롬프트 (Suno v5.5)", a["music_prompt"])
    for p in a.get("sfx_prompts", []):
        audio_body += prompt_box("효과음 프롬프트 (ElevenLabs SFX 등 · 영상 모델 오디오로 부족할 때)", p)
    plans = "".join(f'<div class="plan"><h4>{E(n)}</h4><p>{E(d)}</p>{prompt_box("프롬프트 / 설정", pr)}'
                    f'<p class="small">예상 크레딧: {E(cost)}</p></div>' for n, d, pr, cost in v["gen_plans"])
    graph_path = os.path.join(ROOT, "kit", "_test", edl["name"], "graph.txt")
    graph = open(graph_path, encoding="utf-8").read() if os.path.exists(graph_path) else ""
    edl_name = v["edl"][0]
    folder = edl_name.replace(".json", "")
    edit_body = (
        f'<ol class="steps"><li>작업 폴더 만들기: <code>{E(folder)}/</code> 안에 <code>{E(edl_name)}</code>, '
        f'<code>clips/</code>(S01.mp4…), <code>fonts/</code>(Pretendard-SemiBold.otf, NotoSansJP-SemiBold.ttf)'
        + (", <code>music/</code>" if edl["audio"].get("music") else "") + (", <code>sfx/</code>" if edl["audio"].get("sfx") else "")
        + '</li><li>명령 1줄 실행 (kit 폴더에서):</li></ol>'
        + prompt_box("FFmpeg 자동 편집 명령", f"python edl_render.py {folder}/{edl_name}")
        + f'<p class="small">✅ 검증함: 더미 클립으로 실제 렌더 → 길이 정확({dur:.2f}초), 모든 샷이 제 시간 구간에 나오는지 색상 검사 통과, '
          f'한·영·일 3줄 자막·♬ 기호 렌더 확인. 결과: 1080×1920 · {edl["fps"]}fps · H.264 CRF18 · AAC 192k · -14 LUFS / -1 dBTP.</p>'
        + (f'<details><summary>실제 FFmpeg 필터 그래프 보기 (edl_render.py가 자동 생성)</summary><pre class="code">{E(graph)}</pre></details>' if graph else "")
        + "<h4>HyperFrames로 편집할 때</h4>"
        + prompt_box("Claude Code에 붙여넣을 프롬프트",
                     f"/hyperframes 스킬로 kit/{v['hf'][0]} 컴포지션을 작업해줘. 이 파일은 {edl_name} 편집표에서 자동 생성된 것이고 "
                     f"컷 타이밍·전환·자막 위치가 원본 측정값과 같다. 수정 가능 범위: clips/ 파일 교체, 자막 문장, 전환 강도만. "
                     f"규칙: 1) clips/ fonts/ {'music/ ' if edl['audio'].get('music') else ''}폴더를 index.html 옆에 둔다 "
                     f"2) npx hyperframes check 0건 통과 3) 문제 컷은 npx hyperframes snapshot --at 으로 확인 "
                     f"4) npx hyperframes preview --background 로 내가 확인한 뒤, 내가 승인하면 render. 승인 전 render 금지.")
        + f'<p class="small">생성된 파일: <code>kit/{E(v["hf"][0])}</code> · 자체 규칙 검사 통과(중복 id·audio id·crossorigin·&lt;br&gt;). '
          f'⚠️ HyperFrames CLI가 이 PC에 없어 <code>npx hyperframes check</code>는 아직 못 돌렸습니다.</p>')
    legal = "".join(f"<li>{E(x)}</li>" for x in v["legal"])
    enhance = "".join(f"<li>{E(x)}</li>" for x in v["enhance"])
    workflow = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td></tr>" for a, b, c in C.WORKFLOW)
    costs = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in C.COSTS)
    img_models = "".join(f"<tr><td>{E(a)}</td><td><code>{E(b)}</code></td><td>{E(c)}</td></tr>" for a, b, c in C.IMAGE_MODELS)
    aud_models = "".join(f"<tr><td>{E(a)}</td><td><code>{E(b)}</code></td><td>{E(c)}</td></tr>" for a, b, c in C.AUDIO_MODELS)
    vid_models = "".join(f"<tr><td>{E(m['name'])}</td><td><code>{E(m['id'])}</code></td><td>{E(m['spec'])}</td><td>{E(m['why'])}</td></tr>"
                         for m in C.MODELS.values())
    nav = "".join(f'<a href="{o["file"]}" class="{"on" if o is v else ""}">{o["rank"]}위</a>' for o in others)
    body = (
        section("summary", "한눈에 보기", f'<div class="hero"><img src="img/{vid}/{v["shots"][0]["id"]}_m.jpg" alt="대표 프레임">'
                f'<div><p class="big">{E(v["one_liner"])}</p><div class="kpis">{kpis}</div>'
                f'<p class="small">원본: <a href="{E(v["url"])}">{E(v["url"])}</a> · 캡션 “{E(v["caption"])}”</p>'
                f'<p class="warn">{E(v["structure_note"])}</p></div></div>')
        + section("why", "왜 떡상했나 — 편집 장치를 시간대별로", f'<ol class="viral">{viral}</ol>')
        + section("timeline", "타임라인", tl, "막대 위에 마우스를 올리면 샷·자막·음성 내용이 보입니다.")
        + section("cast", "다른 동물로 바꾸기", cast_block(v))
        + section("shots", "샷별 분석 + 프롬프트", shots, "프레임 위 격자 = 3분할선. 색 띠 = 그 샷의 실제 색 팔레트.")
        + section("plan", "생성 계획", plans)
        + section("transitions", "전환 효과", f'<div class="scroll"><table class="grid"><tr><th>시간</th><th>종류</th><th>길이</th>'
                  f'<th>설명</th><th>FFmpeg</th><th>CapCut</th><th>프리미어/애펙</th></tr>{trs}</table></div>'
                  f'<h4>전환 전후 프레임 (가운데가 전환 지점)</h4><div class="strips">{strips}</div>')
        + section("audio", "사운드 디자인", audio_body)
        + section("edit", "편집 레시피 — FFmpeg · HyperFrames", edit_body)
        + section("models", "모델 선택표", f'<div class="scroll"><table class="grid"><tr><th>영상 모델</th><th>Pollo ID</th><th>스펙(실측 조회)</th><th>이런 컷에</th></tr>{vid_models}</table></div>'
                  f'<div class="two"><div><h4>이미지</h4><table class="grid">{img_models}</table></div>'
                  f'<div><h4>음악·목소리</h4><table class="grid">{aud_models}</table></div></div>'
                  f'<h4>예상 크레딧 (Pollo 견적 도구 실측, 차감 없음)</h4><table class="grid">{costs}</table>')
        + section("workflow", "제작 순서", f'<table class="grid"><tr><th>단계</th><th>할 일</th><th>크레딧</th></tr>{workflow}</table>')
        + section("legal", "주의·강화 아이디어", f'<h4>주의</h4><ul>{legal}</ul><h4>원본을 넘어서는 강화 옵션</h4><ul>{enhance}</ul>'))
    toc = "".join(f'<a href="#{i}">{t}</a>' for i, t in (("summary", "요약"), ("why", "떡상 이유"), ("timeline", "타임라인"),
                                                         ("cast", "동물 교체"), ("shots", "샷별"), ("plan", "생성 계획"),
                                                         ("transitions", "전환"), ("audio", "사운드"), ("edit", "편집"),
                                                         ("models", "모델"), ("workflow", "순서"), ("legal", "주의")))
    return TEMPLATE.format(title=E(f"{v['rank']}위 분석"), h1=E(f"{v['rank']}위 · {v['title']}"), nav=nav, toc=toc, body=body)


CSS = """
:root{--bg:#f6f5f2;--card:#fff;--ink:#1c1c1f;--sub:#5f6068;--line:#e4e2dd;--acc:#e8590c;--chip:#f1efe9;--code:#f4f3ef;--warn:#fff4e6}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#121214;--card:#1c1c20;--ink:#f1f1f3;--sub:#a3a3ad;--line:#2d2d33;--acc:#ff8a3d;--chip:#26262c;--code:#18181c;--warn:#2a2118}}
:root[data-theme="dark"]{--bg:#121214;--card:#1c1c20;--ink:#f1f1f3;--sub:#a3a3ad;--line:#2d2d33;--acc:#ff8a3d;--chip:#26262c;--code:#18181c;--warn:#2a2118}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 "Pretendard","Malgun Gothic",system-ui,sans-serif}
.top{position:sticky;top:0;z-index:5;background:var(--card);border-bottom:1px solid var(--line);padding:10px 16px;display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center}
.top h1{font-size:17px;margin:0;flex:1 1 280px}.top nav a{margin-right:6px;padding:4px 10px;border-radius:99px;background:var(--chip);color:var(--ink);text-decoration:none;font-weight:700}
.top nav a.on{background:var(--acc);color:#fff}.toc{width:100%;overflow-x:auto;white-space:nowrap;font-size:13px}.toc a{color:var(--sub);margin-right:12px;text-decoration:none}
main{max-width:1180px;margin:0 auto;padding:16px}section{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px;margin:16px 0}
h2{margin:0 0 10px;font-size:20px}h3{margin:0;font-size:16px}h4{margin:14px 0 6px}.lead,.small{color:var(--sub);font-size:13px}.big{font-size:17px;font-weight:600}
.warn{background:var(--warn);border-radius:10px;padding:10px 12px;font-size:13px}
.hero{display:grid;grid-template-columns:220px 1fr;gap:18px}.hero img{width:100%;border-radius:12px}
.kpis{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:8px;margin:10px 0}.kpi{background:var(--chip);border-radius:10px;padding:8px 10px}.kpi span{display:block;font-size:12px;color:var(--sub)}.kpi b{font-size:16px}
.viral{list-style:none;padding:0;margin:0;display:grid;gap:8px}.viral li{border-left:4px solid var(--acc);padding:6px 12px;background:var(--chip);border-radius:0 10px 10px 0}.viral p{margin:2px 0 0}.when{font-size:12px;color:var(--acc);font-weight:700;margin-right:8px}
svg.tl{width:100%;height:auto;display:block}.shot0{fill:#4dabf7}.shot1{fill:#339af0}.sub{fill:#63e6be}.spk{fill:#ffa94d}.lbl{font-size:10px;fill:#fff;text-anchor:middle;font-weight:700}.tick{font-size:10px;fill:var(--sub);text-anchor:middle}.rowlbl{font-size:10px;fill:var(--sub)}
.legend{display:flex;flex-wrap:wrap;gap:12px;font-size:12px;color:var(--sub);margin-top:6px}.legend i{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:4px;vertical-align:-2px}.isub{background:#63e6be}.ispk{background:#ffa94d}
.shot{border:1px solid var(--line);border-radius:12px;padding:14px;margin:14px 0}.shot header{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px;margin-bottom:10px}.sid{background:var(--acc);color:#fff;border-radius:6px;padding:1px 8px;font-weight:800}.time{color:var(--sub);font-size:13px}
.frames{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;max-width:560px}.frames figure{margin:0}.frames figcaption{font-size:11px;color:var(--sub);text-align:center}
.thirds{position:relative;border-radius:8px;overflow:hidden}.thirds img{width:100%;display:block}.thirds::after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(to right,transparent 33.1%,rgba(255,255,255,.45) 33.3%,transparent 33.5%,transparent 66.4%,rgba(255,255,255,.45) 66.6%,transparent 66.8%),linear-gradient(to bottom,transparent 33.1%,rgba(255,255,255,.45) 33.3%,transparent 33.5%,transparent 66.4%,rgba(255,255,255,.45) 66.6%,transparent 66.8%)}
.palette{display:flex;height:12px;border-radius:6px;overflow:hidden;max-width:560px;margin:8px 0}.sw{display:block}
table{border-collapse:collapse;width:100%}.spec th{text-align:left;width:92px;color:var(--sub);font-weight:600;vertical-align:top;padding:3px 8px 3px 0;font-size:13px}.spec td{padding:3px 0;font-size:14px}
.grid th,.grid td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top;font-size:13px}.grid th{color:var(--sub)}
.scroll{overflow-x:auto}.models{margin:10px 0;display:flex;flex-wrap:wrap;gap:6px;align-items:center}.mlabel{font-size:12px;color:var(--sub);margin-right:4px}
.chip{background:var(--chip);border-radius:8px;padding:4px 8px;font-size:13px}.chip small{display:block;color:var(--sub);font-size:11px}
.pbox{border:1px solid var(--line);border-radius:10px;margin:8px 0;overflow:hidden}.phead{display:flex;justify-content:space-between;align-items:center;background:var(--chip);padding:6px 10px;font-size:13px;font-weight:700}
.copy{border:0;background:var(--acc);color:#fff;border-radius:6px;padding:4px 12px;font-weight:700;cursor:pointer}.copy.done{background:#2b8a3e}
pre{margin:0;white-space:pre-wrap;word-break:break-word}.prompt,.code{background:var(--code);padding:10px;font:12.5px/1.55 Consolas,"Malgun Gothic",monospace}.code{max-height:360px;overflow:auto}
.note{font-size:13px;color:var(--sub)}.swap{display:grid;gap:6px;max-width:640px}.swap select,.swap textarea{font:inherit;padding:8px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--ink)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:16px}.plan{border:1px dashed var(--line);border-radius:12px;padding:12px;margin:10px 0}
.strips{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:10px}.strip{margin:0}.strip img{width:100%;border-radius:6px}.strip figcaption{font-size:11px;color:var(--sub)}
img.wide{width:100%;border-radius:8px}.steps{padding-left:20px}code{background:var(--code);padding:1px 5px;border-radius:4px;font-size:12.5px}
@media (max-width:760px){.hero,.two{grid-template-columns:1fr}.hero img{max-width:240px}}
"""

JS = """
const presets = JSON.parse((document.getElementById('presets')||{textContent:'[]'}).textContent || '[]');
function blocks(){const sel=document.getElementById('animal'); const custom=(document.getElementById('custom')||{}).value||'';
 const p=presets[sel?+sel.value:0]||['','a chubby anthropomorphic guinea pig','guinea pig'];
 const human=', realistic human-like almond eyes with double eyelids and lashes, small pink human lips, deadpan half-lidded expression, tiny paws, toddler-like upright posture';
 const sp=p[2]; return {'[CHARACTER_2]':'a second chubby anthropomorphic '+sp+' sibling with black-and-white fur'+human,
 '[CHARACTER]':(custom.trim()||p[1])+human,'[MOM]':'an adult anthropomorphic '+sp+' mother with brown and cream fur'+human,
 '[DAD]':'an adult anthropomorphic '+sp+' father with black-and-white fur'+human};}
function render(){const b=blocks(); document.querySelectorAll('pre.prompt').forEach(el=>{let t=el.dataset.tpl;
 for(const k of ['[CHARACTER_2]','[CHARACTER]','[MOM]','[DAD]']) t=t.split(k).join(b[k]); el.textContent=t;});}
document.addEventListener('change',e=>{if(e.target.id==='animal')render();});
document.addEventListener('input',e=>{if(e.target.id==='custom')render();});
document.addEventListener('click',e=>{if(!e.target.classList.contains('copy'))return; const pre=e.target.closest('.pbox').querySelector('pre');
 const ok=()=>{e.target.textContent='복사됨';e.target.classList.add('done');setTimeout(()=>{e.target.textContent='복사';e.target.classList.remove('done')},1500)};
 if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(pre.textContent).then(ok,()=>fb(pre,ok));}else fb(pre,ok);});
function fb(pre,ok){const r=document.createRange();r.selectNodeContents(pre);const s=getSelection();s.removeAllRanges();s.addRange(r);try{document.execCommand('copy');ok();}catch(_){}}
try{const saved=localStorage.getItem('animal'); if(saved!==null&&document.getElementById('animal')) document.getElementById('animal').value=saved;}catch(_){}
document.addEventListener('change',e=>{if(e.target.id==='animal'){try{localStorage.setItem('animal',e.target.value)}catch(_){}}});
render();
"""

TEMPLATE = ("<!doctype html><html lang=\"ko\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            "<title>{title}</title><style>" + CSS.replace("{", "{{").replace("}", "}}") + "</style></head><body>"
            "<div class=\"top\"><h1>{h1}</h1><nav><a href=\"index.html\">목록</a>{nav}</nav><div class=\"toc\">{toc}</div></div>"
            "<main>{body}</main><script>" + JS.replace("{", "{{").replace("}", "}}") + "</script></body></html>")


def index(pages):
    cards = "".join(f'<a class="card" href="{v["file"]}"><img src="img/{v["id"]}/{v["shots"][0]["id"]}_m.jpg" alt="">'
                    f'<div><b>{v["rank"]}위 · {E(v["title"])}</b><p>{E(v["one_liner"])}</p></div></a>' for v in pages)
    css = CSS + ".cards{display:grid;gap:14px}.card{display:grid;grid-template-columns:120px 1fr;gap:14px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px;color:var(--ink);text-decoration:none}.card img{width:100%;border-radius:10px}"
    return (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>김꾸이 TOP3 분석</title><style>{css}</style></head><body><div class="top"><h1>@ggooiikim TOP3 — 똑같이 만들기 분석서</h1></div>'
            f'<main><p class="lead">한 페이지 = 한 영상. 각 페이지에 샷별 캡처·구도·전환·사운드·AI 프롬프트·모델·FFmpeg/HyperFrames 편집법이 있습니다.</p>'
            f'<div class="cards">{cards}</div></main></body></html>')


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    pages = [RANK1, RANK2, RANK3]
    for v in pages:
        open(os.path.join(OUT, v["file"]), "w", encoding="utf-8").write(page(v, pages))
        print("wrote", v["file"], len(v["shots"]), "shots")
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(index(pages))
    print("wrote index.html")
