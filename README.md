# 인스타 햄찌 김꾸이(@ggooiikim) TOP17 릴스 분석 — 똑같이 만들기 키트

- `report/index.html` : 분석 페이지 목록 (1~17위, 한 페이지 = 한 영상)
- `subtitles_top10/` : 인스타 TOP17 자막 (1~3위는 한·영·일 전 줄 검증)
- `kit/edl_render.py` : 편집표(EDL) → FFmpeg 자동 편집 (원본 컷 타이밍·전환·3줄 자막·-14 LUFS)
- `kit/edl_*.json` : 1~17위 편집표 / `kit/hyperframes/` : HyperFrames 컴포지션
- `작업기록.md` : 작업 로그

## 보는 법
저장소를 받은 뒤 `report/index.html` 을 브라우저로 열기 (또는 `python -m http.server -d report 8765` 후 http://localhost:8765)

## 편집 실행
`python kit/edl_render.py <폴더>/edl_rank2_chuseok.json`  (같은 폴더에 clips/S01.mp4…, fonts/ 필요)

