"""1위 — 마그마 팝콘 (DdQnQ6AiXg9): 12초 원테이크."""

RANK1 = {
    "rank": 1, "id": "DdQnQ6AiXg9", "file": "rank1.html",
    "title": "마그마 팝콘 — 12초 원테이크",
    "caption": "마그마로 팝콘 만들었다꾸이🍿",
    "url": "https://www.instagram.com/reel/DdQnQ6AiXg9/",
    "stats": [("조회수", "930만"), ("좋아요", "82,283"), ("댓글", "541"), ("업로드", "2026-09-14"),
              ("길이", "12.04초"), ("컷", "0 (원테이크)"), ("fps", "24"), ("배경음악", "없음")],
    "one_liner": ("헬기 문에서 옥수수 한 양동이를 용암에 부으면 → 팝콘 기둥이 솟아 → 헬기 안까지 덮친다. "
                  "12초 동안 컷이 한 번도 없는 '말도 안 되는 원테이크'. 자막 0줄, 음악 0, 효과음과 '꾸이 꾸이'만."),
    "structure_note": ("편집 컷이 없습니다. 카메라가 캐릭터 → 쏟아지는 옥수수 → 용암(수직 부감) → 솟는 팝콘 → 다시 캐릭터로 "
                       "한 번에 움직이는 AI 생성 원테이크입니다. 아래 '장면'은 편집 컷이 아니라 카메라 동선의 비트(구간)입니다. "
                       "8.83초·9.42초에 감지된 변화도 컷이 아니라 빠른 틸트·팬(카메라 이동)이었습니다."),
    "viral": [
        ("0.0–1.2초", "1초 안에 설정 완성", "캐릭터 + 옥수수 양동이 + 열린 헬기 문 + 아래서 올라오는 주황빛. 말 한마디 없이 '이제 뭘 할지' 궁금해짐 → 스와이프 방지."),
        ("전체", "컷 없는 원테이크", "편집점이 없으니 이탈 타이밍도 없음. 실제 촬영 같은 연속 카메라가 '진짜 같다'는 착각을 줌."),
        ("3.3–4.7초", "1.5초의 정적 = 긴장", "용암 위에서 아무 일도 안 일어나는 1.5초. 효과음도 바람 소리뿐 → 첫 '팝!'의 쾌감을 키움."),
        ("4.75–9.4초", "점점 커지는 폭발", "팝 1개 → 수십 개 → 기둥 → 헬기 높이까지. '규칙 3단계' 에스컬레이션."),
        ("9.4–10.3초", "반전: 나한테 온다", "구경하던 캐릭터가 팝콘에 파묻힘. 관찰자 → 피해자로 뒤집히는 순간."),
        ("10.3–12.0초", "무표정 엔딩 + 루프", "팝콘에 묻힌 채 카메라를 멍하게 응시. 같은 헬기 안이라 첫 장면으로 자연스럽게 이어져 반복 재생을 유도(12초·완주율 극대화)."),
        ("캡션", "짧은 말투 캡션", "'~했다꾸이' 캐릭터 말투 + 이모지 1개. 화면 자막이 없으니 언어 상관없이 전 세계에 통함."),
    ],
    "shots": [
        {"id": "B1", "t0": 0.0, "t1": 1.25, "name": "훅: 헬기 문 앞의 캐릭터",
         "size": "MCU (가슴 위)", "angle": "아이레벨", "lens": "35mm 느낌, 얕은 심도", "move": "핸드헬드 미세 흔들림",
         "comp": "캐릭터 좌측 1/3, 눈이 상단 1/3선. 양동이 하단 중앙. 오른쪽 가장자리에 헬기 문틀(세로선)",
         "action": "양동이를 끌어안고 카메라를 보며 '꾸이 꾸이'(입 모양 0.2~0.9초). 무표정",
         "bg": "열린 헬기 측면 문, 로즈핑크 내장 패널, 검정 가죽 시트, 문 밖은 흐린 하늘",
         "light": "차가운 하늘빛 + 아래에서 올라오는 주황 용암 반사광(양동이 표면·턱에 림라이트)",
         "text": "없음", "sound": "'꾸이 꾸이' 고음 목소리 (0.2~0.9초), 헬기 바람 베드",
         "out": "없음(연속 카메라)",
         "img": ("[CHARACTER] sitting upright on a black leather seat at the open side door of a helicopter with "
                 "rose-pink interior panels, hugging a large galvanized steel bucket overflowing with dried popcorn "
                 "kernels; outside the door a hazy sky and, far below, an enormous glowing lava lake casting warm "
                 "orange light up onto the bucket and the chin; medium close-up, eye level, 35mm, character on the "
                 "left third, door frame on the right edge"),
         "vid": ("0.0-1.2s: [CHARACTER] looks into the lens and squeaks 'kkui kkui' in a tiny high-pitched voice, "
                 "slight handheld camera shake, rotor wind outside"),
         "models": ["seedance25", "klingomni"], "note": "원테이크로 한 번에 생성하는 것이 원본과 가장 가깝습니다(아래 A안)."},
        {"id": "B2", "t0": 1.25, "t1": 2.0, "name": "양동이 기울이기 → 문 밖 공개",
         "size": "MCU → MS", "angle": "아이레벨 → 약간 부감", "lens": "35mm", "move": "팬 라이트 + 틸트 다운(양동이를 따라감)",
         "comp": "양동이가 화면 중앙→우하단으로 이동, 문 밖 하늘·붉은 빛이 우측에서 열림",
         "action": "양동이를 문 밖으로 기울임", "bg": "헬기 문턱·스키드 일부, 멀리 용암의 붉은 빛",
         "light": "주황 반사광이 점점 강해짐", "text": "없음", "sound": "금속 양동이 달그락 (1.3초)", "out": "연속",
         "img": "", "vid": ("1.2-2.0s: it tips the bucket out of the open door; the camera pans right and tilts down "
                            "following the bucket, revealing the glowing orange below"),
         "models": ["seedance25"], "note": ""},
        {"id": "B3", "t0": 2.0, "t1": 3.25, "name": "쏟아지는 옥수수 팔로우",
         "size": "인서트", "angle": "부감으로 전환 중", "lens": "28~35mm", "move": "연속 틸트 다운(약 90°), 낙하 알갱이 추적",
         "comp": "좌상단 양동이 → 대각선으로 흐르는 옥수수 줄기 → 우하단 용암. 좌하단에 검정 헬기 스키드(리벳) 사선",
         "action": "옥수수 알갱이가 줄기처럼 쏟아짐", "bg": "헬기 하부·스키드, 아래 용암",
         "light": "용암 주황빛이 화면 대부분", "text": "없음", "sound": "알갱이 쏟아지는 '촤르르' (2.0~3.0초)", "out": "연속",
         "img": "", "vid": ("2.0-3.2s: a stream of kernels pours out and falls; the camera keeps tilting down following "
                            "the kernels, the black helicopter landing skid enters from the lower left"),
         "models": ["seedance25", "minimaxh3"], "note": ""},
        {"id": "B4", "t0": 3.25, "t1": 4.75, "name": "탑다운 정적 (긴장 빌드업)",
         "size": "익스트림 와이드", "angle": "수직 부감(탑다운 POV)", "lens": "24~28mm", "move": "거의 정지(아주 느린 드리프트)",
         "comp": "화면 전체가 용암 호수. 좌하→중앙으로 헬기 스키드 대각선(리딩 라인). 알갱이는 중앙에서 사라짐",
         "action": "아무 일도 안 일어남 — 1.5초 대기", "bg": "균열선이 빛나는 용암 호수(주황~적색, 밝은 노랑 균열)",
         "light": "용암 자체 발광", "text": "없음", "sound": "바람 + 저음 용암 럼블만 (조용)", "out": "연속",
         "img": ("straight top-down view from a hovering helicopter onto a vast lava lake with glowing yellow cracks "
                 "in a dark orange crust, the black landing skid crossing diagonally from the lower-left corner, "
                 "tiny falling popcorn kernels disappearing into the lava"),
         "vid": "3.2-4.7s: straight top-down view of the lava lake; the kernels vanish; calm, suspenseful pause",
         "models": ["seedance25", "minimaxh3"], "note": "3클립(B안)으로 만들 때 C1의 끝 프레임 = 이 이미지."},
        {"id": "B5", "t0": 4.75, "t1": 8.25, "name": "팝! → 팝콘 기둥",
         "size": "익스트림 와이드(탑다운 유지)", "angle": "수직 부감", "lens": "24~28mm", "move": "정지 → 살짝 풀백",
         "comp": "중앙에서 흰 팝콘 기둥이 카메라 쪽으로 솟으며 타원이 점점 커짐(원근). 주변에 불꽃 같은 팝 여러 개",
         "action": "4.75초 첫 팝(흰 섬광) → 5초 2~3개 → 6초 수십 개 → 7초 기둥 형성",
         "bg": "용암 호수", "light": "팝마다 순간 섬광", "text": "없음",
         "sound": "4.85초 큰 온셋: 팝 + 보글보글 용암 + 저음 쿵 → 밀도가 계속 올라감", "out": "연속",
         "img": "", "vid": ("4.7-8.2s: a single popcorn kernel pops with a bright flash, then dozens pop, then a massive "
                            "column of white popcorn erupts upward toward the camera, crackling"),
         "models": ["minimaxh3", "seedance25"], "note": "물리(폭발·입자)가 핵심 → 분할 생성 시 MiniMax H3."},
        {"id": "B6", "t0": 8.25, "t1": 9.4, "name": "틸트 업 리빌",
         "size": "WS", "angle": "부감 → 수평", "lens": "28mm", "move": "빠른 틸트 업 + 풀백",
         "comp": "헬기 문 바로 옆으로 솟는 팝콘 타워(9.0초). 좌측에 문틀·양동이",
         "action": "기둥이 헬기 높이까지 올라옴", "bg": "하늘, 헬기 동체", "light": "자연광으로 복귀",
         "text": "없음", "sound": "위로 올라가는 휘익(whoosh, 8.8초)", "out": "연속",
         "img": "", "vid": "8.2-9.4s: the camera tilts up as the popcorn column rises past the open door",
         "models": ["seedance25", "klingomni"], "note": ""},
        {"id": "B7", "t0": 9.4, "t1": 10.3, "name": "리액션 → 팝콘 홍수",
         "size": "MS", "angle": "아이레벨", "lens": "35mm", "move": "팬 레프트로 캐릭터 복귀 + 흔들림",
         "comp": "캐릭터 옆모습(좌), 창밖 팝콘 벽(우) → 팝콘이 화면을 덮음",
         "action": "멍하니 팝콘 타워를 봄 → 팝콘이 기내로 쏟아져 파묻힘(모션블러)", "bg": "헬기 실내",
         "light": "자연광", "text": "없음", "sound": "쿵 + 와르르(9.35초), '꾸이 꾸이!'(9.7초)", "out": "연속",
         "img": "", "vid": ("9.4-10.3s: the camera pans left to [CHARACTER] staring blankly at the popcorn tower; "
                            "a wave of popcorn floods into the cabin and engulfs it"),
         "models": ["seedance25", "klingomni"], "note": ""},
        {"id": "B8", "t0": 10.3, "t1": 12.04, "name": "페이오프: 팝콘에 묻힌 무표정",
         "size": "MCU 정면", "angle": "아이레벨", "lens": "35~50mm", "move": "정지(팝콘만 살짝 흘러내림)",
         "comp": "중앙, 머리와 앞발만 팝콘 위로. 화면 하단 2/3가 팝콘",
         "action": "무표정으로 카메라 응시", "bg": "헬기 시트가 팝콘에 덮임", "light": "부드러운 자연광",
         "text": "없음", "sound": "팝콘 부스럭 잔향 (10.3초~)", "out": "영상 끝 → 루프",
         "img": ("[CHARACTER] buried chest-deep in a mountain of fresh popcorn inside a helicopter cabin, only its head "
                 "and front paws above the popcorn, deadpan stare into the lens, a few kernels tumbling, medium "
                 "close-up, centered"),
         "vid": "10.3-12s: buried chest-deep in popcorn, deadpan stare into the lens, a few kernels settle",
         "models": ["seedance25", "klingomni"], "note": "A안에서는 끝 프레임(imageTail)으로 넣으면 엔딩 구도가 고정됩니다."},
    ],
    "gen_plans": [
        ("A안 (추천) — 원테이크 1회 생성",
         "Seedance 2.5 · 이미지→영상 · duration 12 · 1080p · generateAudio 켬 · 첫 프레임 = B1 이미지 · 끝 프레임 = B8 이미지",
         ("One continuous take, no cuts, handheld documentary camera, realistic physics. "
          "0-1.2s: [CHARACTER] at the open helicopter door hugging a bucket of popcorn kernels looks into the lens and "
          "squeaks 'kkui kkui'. 1.2-2s: it tips the bucket out of the door; the camera pans right and tilts down "
          "following the bucket. 2-3.2s: a stream of kernels pours out; the camera keeps tilting down following them, "
          "the black landing skid enters lower-left. 3.2-4.7s: straight top-down view of a vast lava lake; the kernels "
          "vanish; calm suspenseful pause. 4.7-8.2s: one kernel pops with a bright flash, then dozens, then a massive "
          "column of white popcorn erupts upward toward the camera. 8.2-9.4s: the camera tilts up as the column rises "
          "past the door. 9.4-10.3s: the camera pans left to [CHARACTER] staring blankly; popcorn floods into the cabin "
          "and engulfs it. 10.3-12s: buried chest-deep in popcorn, deadpan stare into the lens. Sound: rotor wind, "
          "lava rumble, popcorn crackling, tiny squeaky 'kkui kkui'."),
         "720 (할인 288) × 시도 2~3회"),
        ("B안 — 3클립 이어붙이기(물리 컷만 MiniMax)",
         "C1 0~4.75초 (B1~B4) / C2 4.75~9.42초 (B5~B6) / C3 9.42~12.04초 (B7~B8). 이음새는 첫 팝의 흰 섬광(fadewhite 0.125초)과 팝콘 홍수 모션블러(fade 0.25초)로 숨김",
         ("C1 = Seedance 2.5 또는 Kling v3 Omni, 5초, 첫 프레임 B1 / 끝 프레임 B4.  "
          "C2 = MiniMax H3(-max), 5초, 첫 프레임 = C1 마지막 프레임, 프롬프트 = B5+B6.  "
          "C3 = Kling v3 Omni, 4초, 첫 프레임 = C2 마지막 프레임, 끝 프레임 B8, 프롬프트 = B7+B8.  "
          "MiniMax는 오디오가 없으므로 edl_rank1_3clips.json의 효과음 11개로 사운드를 채움"),
         "약 150~250 (할인가) × 시도"),
    ],
    "transitions": [
        {"t": "8.83초", "type": "카메라 틸트 업 (편집 전환 아님)", "frames": "약 7프레임(209~216)",
         "how": "AI 영상 안의 카메라 이동. 편집으로 흉내 낼 땐 필요 없음", "ffmpeg": "—", "capcut": "—", "pro": "—"},
        {"t": "9.42초", "type": "팬 레프트 + 팝콘 와이프 (편집 전환 아님)", "frames": "약 19프레임(217~236)",
         "how": "팝콘이 화면을 덮는 '오브젝트 와이프'. 분할 생성(B안)이면 여기서 이어붙이면 이음새가 안 보임",
         "ffmpeg": "xfade=transition=fade:duration=0.25", "capcut": "기본 > 디졸브 0.25초", "pro": "Cross Dissolve 6f(24fps)"},
    ],
    "audio": {
        "summary": ("배경음악 없음. 캐릭터 목소리('꾸이 꾸이') + 현장 효과음만. 전체 -14.9 LUFS(인스타 권장 범위), "
                    "LRA 6.4 LU, 트루피크 0.0 dBFS(클리핑 직전 → 재현 시 -1 dBTP 권장). 4.85초에 소리가 폭발적으로 커짐(조용→팝)."),
        "cues": [
            ("0.0–12.0", "헬기 바람·로터 베드", "아주 작게(-18 dB), 3초 이후 용암 저음 럼블 추가"),
            ("0.2–0.9", "'꾸이 꾸이' (귀여운 고음)", "입 모양과 싱크"),
            ("1.3", "금속 양동이 달그락", "-8 dB"),
            ("2.0–3.0", "옥수수 쏟아지는 촤르르", "-6 dB"),
            ("4.75", "첫 '팝' + 지글", "0 dB — 가장 중요한 한 방"),
            ("4.85–8.8", "팝콘 튀는 소리 밀도 상승 + 보글보글", "점점 크게"),
            ("8.8", "휘익(위로)", "-6 dB"),
            ("9.35", "쿵 + 팝콘 와르르", "0 dB"),
            ("9.7–10.5", "'꾸이 꾸이!' (놀람)", "-3 dB"),
            ("10.3–12.0", "팝콘 부스럭 잔향", "-9 dB, 페이드아웃"),
        ],
        "music_prompt": "",
        "sfx_prompts": [
            "helicopter cabin interior, open side door, steady rotor wind rumble, 12 seconds",
            "hundreds of popcorn kernels popping rapidly over bubbling lava, crackling and sizzling, rising intensity, 4 seconds",
            "huge avalanche of popcorn crashing into a small cabin, whoosh and soft rustling impact, 1.5 seconds",
        ],
        "voice": ("'꾸이'는 캐릭터 이름 = 말버릇. 영상 모델 오디오로 'tiny squeaky high-pitched voice saying kkui kkui'를 넣거나, "
                  "직접 녹음 후 FFmpeg로 음정만 올리기: ffmpeg -i my_voice.wav -af \"asetrate=48000*1.5,aresample=48000,atempo=0.8\" kkui.wav "
                  "(약 +7반음, 속도는 비슷하게 유지)"),
    },
    "edl": ["edl_rank1_onetake.json", "edl_rank1_3clips.json"],
    "hf": ["hyperframes/rank1_onetake/index.html", "hyperframes/rank1_3clips/index.html"],
    "legal": [
        "브랜드·로고 없음 → 상표 위험 낮음",
        "인스타 게시 시 'AI 정보(AI 생성)' 라벨 켜기 — 원작 계정도 AI content 라벨 사용 중",
        "원작 콘셉트를 그대로 복제하기보다 동물·장소·음식(예: 빙하에 솜사탕)을 바꿔 '형식'만 가져가기",
    ],
    "enhance": [
        "원본에 없는 강화 옵션: 첫 0.5초에 짧은 훅 자막 1줄('용암에 옥수수 부으면?') — 원본은 자막 0줄로 성공했으므로 A/B 테스트용으로만",
        "4.75초 첫 팝 순간 1프레임 흰 플래시 + 5% 줌 펀치 → 쾌감 강조 (HyperFrames: 펀치 줌 레시피)",
    ],
}
