"""Builds the edit decision lists (EDL) measured from the three reference reels."""
import json

KR, JP = "Pretendard SemiBold", "Noto Sans JP"
AUDIO_DEFAULT = {"clip_gain": 1.0, "music": None, "sfx": [], "lufs": -14, "tp": -1.0}


def shots(rows, fps):
    out = []
    for i, r in enumerate(rows):
        sid, t0, t1, tr = r[0], r[1], r[2], r[3]
        s = {"id": sid, "file": f"{sid}.mp4", "in": 0.0, "t0": t0, "t1": t1}
        if tr:
            kind, dur = tr
            s["out"] = {"type": kind, "dur": dur}
        if len(r) > 4:
            s["push"] = r[4]
        out.append(s)
    return out


def events(rows):
    return [{"t0": a, "t1": b, "kr": k, "en": e, "jp": j} for a, b, k, e, j in rows]


rank1_single = {
    "name": "rank1_magma_popcorn_onetake", "fps": 24, "w": 1080, "h": 1920, "clips_dir": "clips",
    "output": "rank1_onetake.mp4",
    "shots": shots([("S01", 0.0, 12.04, None)], 24),
    "subs": {"events": []},
    "audio": dict(AUDIO_DEFAULT),
}

rank1_3clips = {
    "name": "rank1_magma_popcorn_3clips", "fps": 24, "w": 1080, "h": 1920, "clips_dir": "clips",
    "output": "rank1_3clips.mp4",
    "shots": shots([("C1", 0.0, 4.75, ("fadewhite", 0.125)),
                    ("C2", 4.75, 9.42, ("fade", 0.25)),
                    ("C3", 9.42, 12.04, None)], 24),
    "subs": {"events": []},
    "audio": {"clip_gain": 0.0, "music": None, "lufs": -14, "tp": -1.0, "sfx": [
        {"file": "sfx/heli_wind_bed.wav", "t": 0.0, "gain_db": -18},
        {"file": "sfx/kuii_kuii.wav", "t": 0.2, "gain_db": -2},
        {"file": "sfx/bucket_clank.wav", "t": 1.3, "gain_db": -8},
        {"file": "sfx/kernels_pour.wav", "t": 2.0, "gain_db": -6},
        {"file": "sfx/lava_rumble.wav", "t": 3.0, "gain_db": -12},
        {"file": "sfx/first_pop.wav", "t": 4.75, "gain_db": 0},
        {"file": "sfx/popcorn_crackle_rise.wav", "t": 4.85, "gain_db": -3},
        {"file": "sfx/whoosh_up.wav", "t": 8.8, "gain_db": -6},
        {"file": "sfx/popcorn_avalanche.wav", "t": 9.35, "gain_db": 0},
        {"file": "sfx/kuii_surprised.wav", "t": 9.7, "gain_db": -3},
        {"file": "sfx/popcorn_settle.wav", "t": 10.3, "gain_db": -9}]},
}

rank2 = {
    "name": "rank2_chuseok", "fps": 30, "w": 1080, "h": 1920, "clips_dir": "clips", "output": "rank2_chuseok.mp4",
    "shots": shots([
        ("S01", 0.000, 2.133, None), ("S02", 2.133, 3.700, None), ("S03", 3.700, 5.733, None),
        ("S04", 5.733, 8.300, ("hblur", 0.2)), ("S05", 8.300, 10.733, ("hblur", 0.2)),
        ("S06", 10.733, 13.700, ("zoomin", 0.2)), ("S07", 13.700, 16.267, ("hblur", 0.2)),
        ("S08", 16.267, 20.400, None), ("S09", 20.400, 21.733, None), ("S10", 21.733, 24.967, None),
        ("S11", 24.967, 27.300, None), ("S12", 27.300, 29.250, ("fadewhite", 0.45)),
        ("S13", 29.250, 30.800, None), ("S14", 30.800, 32.100, ("fade", 0.1)), ("S15", 32.100, 34.000, None),
        ("S16", 34.000, 36.333, None), ("S17", 36.333, 40.033, ("hblur", 0.15)),
        ("S18", 40.033, 42.200, ("squeezeh", 0.15)), ("S19", 42.200, 44.500, None)], 30),
    "subs": {"style": {"kr_font": KR, "kr_size": 46, "en_font": "Pretendard", "en_size": 27, "jp_font": JP,
                       "jp_size": 26, "kr_y": 0.752, "en_dy": 0.021, "jp_dy": 0.041, "outline": 2, "shadow": 1.5},
             "events": events([
                 (0.40, 2.10, "엄마, 아빠. 풍성한 한가위 보내세요!", "Have a happy and abundant Chuseok!",
                  "実り多い素敵なチュソク（秋夕）をお過ごしください！"),
                 (4.10, 5.70, "절은 한 번만 하는거야.", "You only do a big bow once.",
                  "韓国の大きな礼（クンジョル）は1回だけするものだよ。"),
                 (6.40, 8.28, "그래. 10만원씩 나눠 가져라.", "Split this 100,000 won between you two.",
                  "10万円ずつ分けて持ってね。"),
                 (9.50, 10.70, "용돈이다~~!", "Pocket money~~!", "お小遣いだ~~！"),
                 (11.20, 12.45, "우리 송편 누가 더 잘 빚나 내기할래?", "Wanna bet on who makes better songpyeon?",
                  "どっちが上手にソンピョンを作れるか勝負しようよ！"),
                 (12.50, 13.65, "좋아!", "Deal!", "乗った！"),
                 (20.45, 21.70, "차라리 대형 송편을 만들자.", "Fine, I'll just make a giant songpyeon.",
                  "もう、いっそ巨大なソンピョンを作ろう。"),
                 (25.70, 27.28, "대형 송편 완성이다 꾸이~~!", "Giant songpyeon is done~~!", "巨大ソンピョン、完成~！"),
                 (28.25, 29.05, "저게 뭐지....?", "What is that....?", "あれはなんだ....？"),
                 (30.80, 32.05, "맛있겠다~~!", "Looks delicious~~!", "おいしそう~！"),
                 (32.60, 33.98, "갈비찜 나간다, 얘들아~", "Galbi-jjim is coming, kids!", "カルビチムできたよ、みんな〜！"),
                 (36.40, 40.00, "(입에서 살살 녹는다 꾸이...)", "It just melts in your mouth...", "口の中でとろける......"),
                 (40.10, 42.15, "(맛있다 꾸이...)", "So good...", "おいし......"),
                 (43.20, 44.50, "매일 추석이었으면 좋겠다 꾸이!!!", "I wish every day was Chuseok!!!",
                  "毎日がチュソクならいいのに！！！")])},
    "audio": dict(AUDIO_DEFAULT),
}

rank3 = {
    "name": "rank3_burger_parttime", "fps": 30, "w": 1080, "h": 1920, "clips_dir": "clips",
    "output": "rank3_burger.mp4",
    "shots": shots([
        ("S01", 0.000, 6.000, None), ("S02", 6.000, 7.067, None), ("S03", 7.067, 8.100, ("fade", 0.1)),
        ("S04", 8.100, 8.767, ("fade", 0.067)), ("S05", 8.767, 9.167, None), ("S06", 9.167, 10.000, None),
        ("S07", 10.000, 11.567, ("fade", 0.1)), ("S08", 11.567, 13.367, None), ("S09", 13.367, 14.067, None),
        ("S10", 14.067, 16.267, ("fade", 0.067)), ("S11", 16.267, 18.367, None),
        ("S12", 18.367, 20.967, ("zoomin", 0.133)), ("S13", 20.967, 22.400, None, 0.10)], 30),
    "subs": {"style": {"kr_font": KR, "kr_size": 60, "en_font": "Pretendard", "en_size": 34, "jp_font": JP,
                       "jp_size": 33, "kr_y": 0.741, "en_dy": 0.038, "jp_dy": 0.057, "outline": 2.4, "shadow": 1.8},
             "events": events([
                 (0.60, 1.50, "정성을 담아서~♬", "With love and care~♬", "心を込めて~♬"),
                 (1.50, 3.05, "햄버거를 만들자~♬", "Let's make a hamburger~♬", "ハンバーガーを作ろう~♬"),
                 (3.20, 5.40, "버거야 맛있어져라~", "Be delicious~", "おいしくな〜れ〜"),
                 (5.45, 6.20, "완성!", "Done!", "完成!"),
                 (6.25, 7.25, "감튀 투하!", "Fries going in!", "ポテト投入!"),
                 (7.25, 8.75, "향기~", "Smells so good~", "いい香り〜"),
                 (9.20, 10.00, "감튀 준비완료!", "Fries are ready!", "ポテト準備完了!"),
                 (10.95, 11.70, "준비 끝!", "All set!", "準備完了!"),
                 (11.75, 13.40, "주문 나왔습니다~!", "Order's ready~!", "ご注文できました〜!"),
                 (13.45, 14.50, "뭐야 이게...?", "What is this...?", "なんだこれ…?"),
                 (14.60, 16.25, "간에 기별도 안가겠네...", "That's barely a bite...", "一口で終わりじゃん…"),
                 (19.70, 20.65, "열심히 만들었는데...", "I worked so hard on it...", "一生懸命作ったのに…"),
                 (20.70, 22.40, "그 와중에 맛있어...", "But... it's delicious...", "でも、おいしい…")])},
    "audio": {"clip_gain": 1.0, "music": "music/kuii_jingle.mp3", "music_gain_db": -8, "duck": True, "duck_ranges": [[13.3, 16.4]],
              "sfx": [], "lufs": -14, "tp": -1.0},
}

if __name__ == "__main__":
    for name, edl in [("edl_rank1_onetake", rank1_single), ("edl_rank1_3clips", rank1_3clips),
                      ("edl_rank2_chuseok", rank2), ("edl_rank3_burger", rank3)]:
        json.dump(edl, open(f"{name}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("wrote", name)
