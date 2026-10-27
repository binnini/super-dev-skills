# 바뀐 것

## assets 0.1.1 · 2026-10-27
- `assets:web-sound-search`: TombOfTheMask 로컬 복사본에서 10-24~10-26에 더한 것을 옮김.
  - 0단계 소리 현황 페이지(`scripts/build_status.py`, `assets/status_template.html`). 경로는 프로필에서 읽고, 순간 이름표 · 묶음 · 임시 삐 목록은 프로젝트의 `sound.labels` JSON으로 뺌. 원작 키가 비면 원작 줄 · 버튼을 숨김.
  - `references/extract.md`: Pixabay 항목 페이지를 한꺼번에 받으면 429가 나는 주의.
  - `scripts/freesound_search.py`: `"loop": true`면 이름 거르기를 끔(계속 나는 소리용).
- `tests/run_tests.py`: 현황 페이지 동작 검사(가짜 프로젝트) 추가, Windows 콘솔(cp949)에서 멈추지 않게 stdout을 utf-8로.
- `templates/skill-profile.yaml`: `sound.enum` · `audio_dir` · `labels` · `original_game_dir` · `original_listen_dir`, `docs.original_sounds` 키를 더함. `vfx.art_dir` 예시를 실제 폴더(`Art/Vfx`)로.

## 저장소 · 2026-10-24
- 마켓플레이스 이름을 저장소 이름에 맞춰 `pudin-skills` → `super-dev-skills`로 바꿈(설치한 곳이 없을 때 바꿈).
- `CLAUDE.md`(이 저장소 작업 규칙), `docs/TOOLKIT.md`(작업 도구함), `docs/HANDOFF.md`(결정 · 다음 할 일), README "시작하기"를 더함.

## assets 0.1.0 · 2026-10-24
- 저장소 뼈대: 마켓플레이스(당시 이름 `pudin-skills`), 플러그인 `assets`.
- `assets:web-sound-search`: TombOfTheMask `.claude/skills/web-sound-search`(10-23)를 옮김. 경로를 `skill-profile.yaml`에서 읽게 바꿈.
- `assets:web-vfx-search`: 새로 만듦(10-24 자석 오라 시험). 받는 값 확인 · 유료는 레퍼런스로만 · Forge 생성 · 묶음 전달.
