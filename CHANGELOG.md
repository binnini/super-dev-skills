# 바뀐 것

## art 0.1.1 · 2026-11-23
- `art:imagegen`: CrazyArena(10-29 ~)에서 쓴 것을 옮김.
  - `scripts/imagegen_log.py collect`: Chrome이 받은 `<epoch ms>.jpg` 최신 N장을 `<work_dir>/imagegen/<key>/<id>_a, _b …`로 옮김(CrazyArena `references/web/imagegen/_tools/collect.py`).
  - `scripts/key_fit.py`: 초록 배경(#00FF00) JPG를 투명 PNG로 키잉하고 캔버스에 맞춤. 아래 여백 기본값을 캔버스 높이 / 16으로, 세로로도 넘치지 않게 고침.
  - `references/site.md`: 내려받기 위치 · 결과 크기(JPG, 알파 없음) · 사용량 · 설정 창은 토글로 닫기 · 받기와 옮기기를 한 메시지에 섞지 않기 등 10-29 함정.
  - SKILL.md 5 · 8단계에 초록 배경 · collect · key_fit 순서를 적음.
- `tests/run_tests.py`: collect가 최신 N장만 옮기는지, 장수가 모자라면 멈추는지.
- `docs/KIT.md`: art 줄, CLI beta.8 새 이름, CrazyArena 후보(글 · 시나리오 편집 페이지, 밸런스 봇), 메모리는 전역 CLAUDE.md로 옮긴다는 줄.

## art 0.1.0 · 2026-10-28
- 새 플러그인 `art`, 스킬 `art:imagegen`(CrazyArena 10-28 UI 목업 2장을 뽑은 방법).
  - 절차: 프로필 · 스타일 팩 읽기 → 브리프 → 참조 고르기(원작 그림은 `imagegen.original_refs` 규칙) → 프롬프트 조립 → 확인받기 → Claude in Chrome 조작 → 기록 → 고르기 → 넣기.
  - `references/site.md`: 사이트 화면 · 순서 · 함정(앱 안 브라우저는 참조 업로드 불가, `file_upload`는 세션이 읽는 폴더만, 설정 창 닫은 뒤 비율이 "자동"으로 돌아감).
  - `references/style_pack.md`: 프로젝트 스타일 팩(JSON) 형식과 갱신 절차. approved는 승인자만.
  - `scripts/imagegen_log.py`: `record`(프롬프트 · 모델 · 참조 · 스타일 팩 버전 기록, 원작 참조 규칙 검사) · `list` · `pick`(고른 것을 용도별 폴더로 복사).
- `templates/skill-profile.yaml`: `imagegen:` 절(`site` · `model` · `style_pack` · `out_dir` · `draft_dir` · `original_refs` · `approvers`).
- `tests/run_tests.py`: imagegen_log를 가짜 프로젝트로 record → list → pick, 원작 참조 규칙 · 빈 프로필에서 멈추는지.

## 저장소 · 2026-10-27
- `docs/KIT.md` 새로: 키트 묶음(A 템플릿 · B 패키지 · C 스킬 · D 환경)마다 TotM · BigHunter의 출처 파일, 다루는 법(그대로 · 양식 · 떼어 냄 · 참고), 순위, 넘기지 않는 것, 새 과제 시작 묶음. README · TOOLKIT · HANDOFF에서 연결.
- `docs/TOOLKIT.md` 8장 "만드는 순서"를 1 · 2 · 3순위 표로 다시 씀(TotM 근거 열 추가). 7장 1일차의 패키지 · 잠금 훅 줄을 순위에 맞춤.
- `docs/HANDOFF.md` "다음 할 일"을 같은 순위로 다시 나눔, "정한 것"에 10-27 만드는 순서 줄 추가, 디자이너 협업 줄에 10-27 바꾼 내용(첫 주는 최소판)을 적음.

## assets 0.1.1 · 2026-10-27
- `assets:web-sound-search`: TombOfTheMask 로컬 복사본에서 10-24~10-26에 더한 것을 옮김.
  - 0단계 소리 현황 페이지(`scripts/build_status.py`, `assets/status_template.html`). 경로는 프로필에서 읽고, 순간 이름표 · 묶음 · 임시 삐 목록은 프로젝트의 `sound.labels` JSON으로 뺌. 원작 키가 비면 원작 줄 · 버튼을 숨김.
  - `references/extract.md`: Pixabay 항목 페이지를 한꺼번에 받으면 429가 나는 주의.
  - `scripts/freesound_search.py`: `"loop": true`면 이름 거르기를 끔(계속 나는 소리용).
- 정적 평가(10-27)에서 나온 것:
  - 안내 없던 파일을 SKILL.md에 연결: `freesound_search.py`(셸에서 Freesound 넓게 훑기, 소리 3단계), `readme_template.txt`(VFX 6단계 묶음 README).
  - 옛 경로 · 맨 `python` 정리: `build_index.py` · `freesound_ids.py` · `page_template.html` · `atlas_tools.py` · VFX `build_page.py` · `forge.md` · `forge_gen.js`를 `<python>` · `<skill_dir>`로. 소리 `build_page.py` 기본 출력은 `references/web` 고정 대신 후보 파일 옆.
  - `forge_gen.js`: playwright를 실행한 폴더(cwd)에서 찾음. 플러그인 캐시에서 돌면 `<work_dir>`에 설치한 playwright를 못 찾던 문제.
- `tests/run_tests.py`: 현황 페이지 동작 검사(가짜 프로젝트), 스킬 안 모든 파일이 다른 파일에서 가리켜지는지 · 옛 경로(`.claude/skills/`, `Assets/_Project`) · 맨 `python -I/-m`이 없는지 검사(옛 버전에서 FAIL 9 확인), Windows 콘솔(cp949)에서 멈추지 않게 stdout을 utf-8로.
- `templates/skill-profile.yaml`: `sound.enum` · `audio_dir` · `labels` · `original_game_dir` · `original_listen_dir`, `docs.original_sounds` 키를 더함. `vfx.art_dir` 예시를 실제 폴더(`Art/Vfx`)로.

## 저장소 · 2026-10-24
- 마켓플레이스 이름을 저장소 이름에 맞춰 `pudin-skills` → `super-dev-skills`로 바꿈(설치한 곳이 없을 때 바꿈).
- `CLAUDE.md`(이 저장소 작업 규칙), `docs/TOOLKIT.md`(작업 도구함), `docs/HANDOFF.md`(결정 · 다음 할 일), README "시작하기"를 더함.

## assets 0.1.0 · 2026-10-24
- 저장소 뼈대: 마켓플레이스(당시 이름 `pudin-skills`), 플러그인 `assets`.
- `assets:web-sound-search`: TombOfTheMask `.claude/skills/web-sound-search`(10-23)를 옮김. 경로를 `skill-profile.yaml`에서 읽게 바꿈.
- `assets:web-vfx-search`: 새로 만듦(10-24 자석 오라 시험). 받는 값 확인 · 유료는 레퍼런스로만 · Forge 생성 · 묶음 전달.
