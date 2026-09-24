import json, subprocess, sys
import numpy as np
NOWIN = getattr(subprocess, "CREATE_NO_WINDOW", 0)
RGB = {"red": (255,0,0), "green": (0,128,0), "blue": (0,0,255), "yellow": (255,255,0), "magenta": (255,0,255),
       "cyan": (0,255,255), "orange": (255,165,0), "purple": (128,0,128), "white": (255,255,255), "gray": (128,128,128)}
cols = list(RGB)
def frame_rgb(path, t):
    raw = subprocess.run(["ffmpeg","-v","error","-ss",f"{t:.3f}","-i",path,"-frames:v","1","-vf","crop=1080:300:0:100,scale=8:8","-pix_fmt","rgb24","-f","rawvideo","-"],
                         capture_output=True, stdin=subprocess.DEVNULL, creationflags=NOWIN).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1,3).mean(0)
for name in sys.argv[1:]:
    edl = json.load(open(f"_test/{name}/edl.json", encoding="utf-8")); out = f"_test/{name}/{edl['output']}"
    ok = 0; bad = []
    for i, s in enumerate(edl["shots"]):
        for t in ((s["t0"]+s["t1"])/2, s["t0"]+0.12 if i else 0.05, s["t1"]-0.12):
            got = frame_rgb(out, t); exp = np.array(RGB[cols[i % len(cols)]])
            best = min(cols, key=lambda c: np.abs(np.array(RGB[c]) - got).sum())
            if best == cols[i % len(cols)]: ok += 1
            else: bad.append((s["id"], round(t,2), best))
    print(name, f"samples correct {ok}/{3*len(edl['shots'])}", bad[:6])
