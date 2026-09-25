import json
import sys
from content_rank4_10 import PAGES_4_10
from content_rank11_17 import PAGES_11_17
for v in (PAGES_11_17 if "11" in sys.argv else PAGES_4_10):
    shots = []
    for sh in v["shots"]:
        d = {"id": sh["id"], "file": f"{sh['id']}.mp4", "in": 0.0, "t0": sh["t0"], "t1": sh["t1"]}
        if sh.get("tr"): d["out"] = {"type": sh["tr"][0], "dur": sh["tr"][1]}
        if "푸시인" in sh.get("move", ""): d["push"] = 0.12
        shots.append(d)
    st = dict(v["subs_style"]); 
    if st: st.update({"kr_font": "Pretendard SemiBold", "en_font": "Pretendard", "jp_font": "Noto Sans JP"})
    edl = {"name": f"rank{v['rank']}_{v['id']}", "fps": 30, "w": 1080, "h": 1920, "clips_dir": "clips",
           "output": f"rank{v['rank']}.mp4", "shots": shots,
           "subs": {"style": st, "events": v["subs"]} if v["subs"] else {"events": []},
           "audio": {"clip_gain": 1.0, "music": None, "sfx": [], "lufs": -14, "tp": -1.0}}
    if v["rank"] in (4, 7, 16): edl["fps"] = 24
    json.dump(edl, open(f"edl_rank{v['rank']}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("edl", v["rank"], len(shots))
