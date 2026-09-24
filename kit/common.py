"""Shared blocks for the three analysis pages: model catalog, character DNA, style, workflow."""

MODELS = {
    "seedance25": {"name": "Seedance 2.5", "id": "bytedance/seedance-2-5",
                   "spec": "이미지→영상·레퍼런스→영상 / 4~30초 / 최대 1080p / 첫·끝 프레임 / 네이티브 오디오 / 참조 이미지 최대 30장",
                   "why": "원작자 캡션에 #capcutseedance25 표기 → 같은 계열. 긴 원테이크·캐릭터 일관성·음성까지 한 번에"},
    "klingomni": {"name": "Kling v3 Omni", "id": "kling-ai/kling-v3-omni",
                  "spec": "3~15초 / std·pro·4K / 첫·끝 프레임 / 네이티브 오디오 / 레퍼런스→영상",
                  "why": "표정 연기·손으로 소품 다루기·두 캐릭터 동시 연기에 강한 편(일반 평판)"},
    "minimaxh3": {"name": "MiniMax H3", "id": "minimax/minimax-h3 (고품질: minimax-h3-max)",
                  "spec": "4~15초 / 최대 2K / 첫·끝 프레임 / 레퍼런스→영상 / 오디오 옵션 없음(후반에 효과음)",
                  "why": "튀김·반죽·팝콘 폭발 같은 물리 움직임이 강한 편(하이루오 계열 평판)"},
    "omni11": {"name": "Google Gemini Omni 1.1 Flash", "id": "google/gemini-omni-1-1-flash",
               "spec": "3~10초 / 9:16 / 최대 4K / 첫·끝 프레임 / 레퍼런스→영상",
               "why": "9:16 네이티브·4K 지원 → 음식 클로즈업·인서트 컷 화질용 (품질은 테스트 필요)"},
    "veo31": {"name": "Google Veo 3.1", "id": "google/veo-3-1",
              "spec": "4·6·8초 / 9:16 / 1080p·4K / 첫·끝 프레임 / 네이티브 오디오(대사)",
              "why": "사람 배우 + 한국어 대사 립싱크가 필요한 컷(3위 보디빌더, 2위 부모님 대사)"},
    "hailuo23": {"name": "Hailuo 2.3", "id": "minimax/hailuo-2-3",
                 "spec": "6·10초 / 768p·1080p(6초만) / 끝 프레임 없음",
                 "why": "0.4~1초짜리 짧은 인서트를 싸게 뽑을 때"},
}

IMAGE_MODELS = [
    ("Nano Banana Pro", "google/nano-banana-pro", "캐릭터 시트를 참조로 넣고 샷별 첫 프레임 만들기(일관성 1순위)"),
    ("Seedream 5.0 Pro", "bytedance/seedream-5-0-pro", "Seedance와 같은 회사 — 실사 털·음식 질감"),
    ("GPT Image 2", "openai/gpt-image-2", "소품·간판·포장지 디테일 수정"),
    ("Flux Kontext Max", "flux/flux-kontext-max", "기존 키프레임 부분 수정(표정만 바꾸기 등)"),
]

AUDIO_MODELS = [
    ("Suno v5.5", "suno/suno-v5-5", "배경음악(징글) — 1회 2곡 생성, 18크레딧"),
    ("ElevenLabs v3", "elevenlabs/eleven-v3", "사람 대사(한국어) TTS"),
    ("MiniMax Speech 2.8 HD", "minimax/speech-2-8-hd", "한국어 대사 TTS 대안"),
    ("Seed Audio 1.0", "bytedance/seed-audio-1-0", "TTS 대안"),
]

COSTS = [
    ("Seedance 2.5 · 1080p · 12초 · 오디오", "720 (할인 288)"),
    ("Seedance 2.5 · 720p · 5초 · 오디오", "150 (할인 60)"),
    ("Kling v3 Omni · pro · 5초 · 오디오", "50 (할인 20)"),
    ("MiniMax H3 · 768p · 5초", "50"),
    ("Google Omni 1.1 Flash · 1080p · 5초", "50"),
    ("Veo 3.1 · 1080p · 4초 · 오디오", "120 (할인 48)"),
    ("Nano Banana Pro 이미지 1장", "18 (할인 9)"),
    ("Suno v5.5 음악 (2곡)", "18"),
]

STYLE = ("hyperrealistic photograph, vertical 9:16, shot on a full-frame cinema camera, soft natural light, "
         "shallow depth of field, crisp individual fur strands, subtle film grain, no text, no watermark, no logo")

NEGATIVE = ("text, subtitles, captions, watermark, logo, brand names, extra fingers, extra limbs, deformed paws, "
            "cartoon, anime, 3D toy render, plastic skin, blurry face, duplicate character, gore")

CHAR_ORIGINAL = ("a chubby anthropomorphic guinea pig with caramel-brown and white fur and a white blaze down the "
                 "nose, realistic human-like almond eyes with double eyelids and lashes, small pink human lips, "
                 "deadpan half-lidded expression, tiny pink paws, toddler-like upright posture")

CHAR_SWAPS = [
    ("골든 햄스터", "a chubby anthropomorphic golden hamster with honey-gold and cream fur and a white belly"),
    ("스코티시폴드 아기고양이", "a chubby anthropomorphic Scottish Fold kitten with orange tabby fur and folded ears"),
    ("시바견 아기", "a chubby anthropomorphic Shiba Inu puppy with red-sesame fur and a cream mask"),
    ("아기 카피바라", "a chubby anthropomorphic baby capybara with coarse chestnut fur and a blunt snout"),
    ("친칠라", "a chubby anthropomorphic grey chinchilla with ultra-soft silver fur and big round ears"),
]

CHAR_KEEP = [
    "사람 같은 눈(쌍꺼풀·속눈썹) + 작은 사람 입술 — 이 '언캐니 귀여움'이 밈의 핵심. 동물만 바꾸고 이건 유지",
    "통통한 공 모양 몸 + 짧은 팔다리 + 서서 행동하는 유아 자세",
    "기본 표정은 무표정(데드팬)·반쯤 감긴 눈 → 반응 컷에서만 크게 변화(반짝 눈·눈물)",
    "소품보다 작은 몸 크기(스케일 개그): 양동이·송편·감튀 상자와의 크기 대비",
    "캐릭터 전용 한마디(원본은 '꾸이') → 새 캐릭터 이름 1~2음절로 통일, 말은 전부 이 소리로",
]

CHAR_SHEET_PROMPT = ("character reference sheet of [CHARACTER], same character shown 5 times on a plain light-grey "
                     "background: front view, three-quarter view, side profile, back view, and a close-up of the face "
                     "with neutral deadpan expression; consistent fur markings and proportions in every view; "
                     "photoreal studio lighting, 9:16, " + "no text, no watermark")

WORKFLOW = [
    ("① 캐릭터 시트", "Nano Banana Pro로 [CHARACTER] 시트 1장 (정면·측면·후면·얼굴). 이후 모든 컷의 참조 이미지로 사용", "9~18 크레딧"),
    ("② 샷별 첫 프레임", "각 샷의 '이미지 프롬프트' + 캐릭터 시트 참조 → 키프레임 생성. 원본 캡처와 구도 비교", "샷 수 × 9~18"),
    ("③ 샷별 영상", "키프레임을 첫 프레임으로 넣고 '영상 프롬프트' 실행. 필요한 길이보다 0.5초 이상 길게", "모델별 표 참고"),
    ("④ 사운드", "네이티브 오디오 확인 → 부족하면 효과음/음악/보이스 추가 (사운드 섹션)", "0~20"),
    ("⑤ 파일 정리", "clips/S01.mp4 … 편집표(EDL)의 파일명 그대로 저장, fonts/에 Pretendard·Noto Sans JP", "무료"),
    ("⑥ 자동 편집", "python edl_render.py edl_xxx.json → 원본과 같은 컷 타이밍·전환·3줄 자막·-14 LUFS", "무료"),
    ("⑦ (선택) HyperFrames", "hyperframes/폴더의 index.html로 Studio에서 미세 조정 → npx hyperframes check → render", "무료"),
]
