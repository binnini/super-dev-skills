# 다음 과제 키트: 넘길 파일 목록

TOOLKIT.md의 산출물(템플릿 · 패키지 · 스킬 · 환경)을 **실제 파일 단위**로 적은 목록이다(2026-10-27, 회사 PC에서 두 저장소를 보고 씀). 키트를 만들 때 여기서 파일을 꺼내고, 새 과제를 시작할 때 마지막 장의 묶음을 넘긴다.

- 출처 저장소: **TotM** = `C:\Users\111percent\workspace\TombOfTheMask`(GitLab, 브랜치 Dev), **BH** = `C:\Users\111percent\workspace\bighunter`(마지막 커밋 10-13). `BigHunterLike` 폴더는 BH의 옛 사본이라 쓰지 않는다.
- 아래 경로는 각 저장소 루트 기준이다. `Scripts/` = `Assets/_Project/Scripts/`.
- 다루는 법 표기
  - **그대로**: 복사하고 이름 · 네임스페이스만 바꾼다
  - **양식**: 구조(절 · 표 머리)만 남기고 내용을 비운다
  - **떼어 냄**: 게임 전용 부분을 빼고 일반화한다(SO · 프로필에서 값을 읽게)
  - **참고**: 복사하지 않고 만들 때 읽는다
- 만드는 순서는 TOOLKIT 8장(1 · 2 · 3순위)을 따른다. 각 표의 "순위" 열이 그 순위다.

## 키트 한눈에

| 묶음 | 형태 | 받는 곳 |
|---|---|---|
| A. project-template | GitLab 템플릿 저장소 하나 | 새 과제 1일차에 복제 |
| B. Unity 패키지 | UPM 패키지(공용 원본 폴더 `_shared` → 각 프로젝트 `Packages/` 또는 git URL) | 새 과제 `Packages/manifest.json` |
| C. super-dev-skills | 이 저장소(플러그인 마켓플레이스) | 새 과제 `.claude/settings.json` 두 줄 |
| D. PC 환경 | 설치 목록(저장소 밖) | 새 PC · 디자이너 PC |

## A. project-template 저장소

### 문서 (`docs/`, 루트)

| 키트 파일 | 출처 | 다루는 법 | 순위 |
|---|---|---|---|
| `CLAUDE.md` | TotM `docs/playbook/CLAUDE_TEMPLATE.md`(채운 예: TotM `CLAUDE.md`) | 그대로(양식). 환경 · 측정 도구 경로 절은 TotM `CLAUDE.md`의 "Unity CLI" · "측정 도구" · "파일 편집" 규칙을 옮김 | 1 |
| `docs/PROJECT_PLAYBOOK.md` | TotM `docs/playbook/PROJECT_PLAYBOOK.md` | 그대로 + **v2 보강**: TOOLKIT 6장 테스트 계층 · 작성 규칙, 3일차 결정 게이트, 배치 소유 규칙(5장), 리포트 A/B는 클론 선택 모듈로 | 1 |
| `docs/PITFALLS.md` | TotM `docs/PITFALLS.md`(BH에서 겪은 것을 정리한 TotM `docs/playbook/PITFALLS.md`의 절을 모두 포함하는 합본) | 떼어 냄: "맵 · 회귀 eval" 중 TotM 맵 전용 줄과 "레퍼런스 영상 측정 (TombOfTheMask)" 절은 빼고(후자는 video-measure로), 나머지 절은 그대로 | 1 |
| `docs/SYSTEM.md` | TotM `docs/SYSTEM.md` | 양식: 1장 원본 위치 표 머리 + 결정 기록 표 머리만 | 1 |
| `docs/GDD.md` | TotM `docs/GDD.md` | 양식: 장 제목과 마지막 장 "SO 필드 · 값 · 근거" 표 머리만(`gdd_so_match`가 읽는 형식 그대로) | 1 |
| `docs/PENDING.md` | TotM `docs/PENDING.md` | 양식: 표 머리 + 신뢰도 표기(✅ 측정 / 🔶 추정 / 확인 불가 / 사용자 확인) | 1 |
| `docs/DECISION_GATE.md`(새로) | TOOLKIT 7장 8번 | 새로: 3일차에 묶을 5가지(컨셉 · 화면 폭 · 판정 크기 · 뼈 이름 · UI 구조) 체크리스트와 결정 칸 | 1 |
| `docs/ART_GUIDE.md` | TotM · BH `docs/ART_GUIDE.md` | 양식: 판정 크기 합의표, 파일 이름 규칙(`그룹_이름_상태`), 그림 형식표(TOOLKIT 5장) | 2 |
| `docs/UI.md` | TotM `docs/UI.md` | 양식: 화면 목록 · 화면별 요소 · 흐름 표, `ui_<화면>_<요소>` 이름 규칙 | 2 |
| `docs/handoff/` | TotM `docs/handoff/2026-10-24_webgl_perf.md` 등 | 양식 1개(`_TEMPLATE.md`: 목표 · 한 것 · 남은 것 · 시작 프롬프트) | 1 |
| `docs/reports/daily/` | TotM `docs/reports/daily/` | 빈 폴더 + 양식 1개 | 2 |
| `docs/reports/` 리포트 A/B(클론 선택 모듈) | TotM `docs/reports/report_A_TombOfTheMask.md` · `report_B_TombOfTheMask.md`, 회사 양식 `리포트양식.png` · `과제내용.png` | 양식: 장 제목 · 표 머리만. 클론이 아니면 폴더째 지움 | 3 |
| `README.md` | TotM `README.md` | 양식: 실행 · 재생성(빌더 메뉴) · 검증 · 빌드 · 폰에서 보기 절 | 1 |
| `AGENTS.md` | TotM `AGENTS.md`(Codex용 같은 규칙) | 선택. Codex를 같이 쓸 때만 | 3 |

### Unity 골격 (`Assets/_Project/`)

| 키트 파일 | 출처 | 다루는 법 | 순위 |
|---|---|---|---|
| `Scripts/Editor/ProjectBuilder.cs` | TotM `Scripts/Editor/ProjectBuilder.cs` | 떼어 냄: `TombOfTheMask/Step N` 메뉴 골격 · Step 순서 · 씬 저장만. 나머지 `ProjectBuilder.*.cs`(SeaWall · ZoneThemes 등)는 게임 전용이라 참고 | 1 |
| `Scripts/Editor/ProjectBuilder.Settings.cs` · `.Layers.cs` · `.Tuning.cs` | TotM 같은 이름 | 떼어 냄: 플레이어 설정 · 정렬 레이어 · SO 에셋 만들기 패턴 | 1 |
| `Scripts/Editor/BuildScript.cs` | TotM `Scripts/Editor/BuildScript.cs` | 떼어 냄: WebGL · Android · 제출 빌드 메뉴, 빌드에서 뺄 폴더 숨기기(예외 3의 원작 소리 폴더 차단 같은 장치를 "빌드 제외 폴더 목록"으로 일반화) | 1 |
| `Scripts/Runtime/Data/LabelAttribute.cs` + `Scripts/Editor/LabelDrawer.cs` | TotM 같은 경로 | 그대로(인스펙터 한글 이름) | 1 |
| `Scripts/Runtime/Camera/AspectLetterbox.cs` | TotM 같은 경로 | 그대로(세로 비율 고정 · 정수 픽셀 영역, 10-27 고침) | 1 |
| `Scripts/Runtime/Camera/PixelSnapCamera.cs` | TotM 같은 경로 | 그대로. 도트 그림 과제일 때만 | 2 |
| `Scripts/Runtime/Debugging/EditorRunInBackground.cs` | TotM 같은 경로 | 그대로(CLI로 돌릴 때 에디터가 포커스 없이도 흐르게) | 1 |
| `*.Runtime.asmdef` · `*.Editor.asmdef` | TotM `TombOfTheMask.Runtime/Editor.asmdef` | 그대로, 이름만 | 1 |

### 검사 · 도구 (`tools/`)

| 키트 파일 | 출처 | 다루는 법 | 순위 |
|---|---|---|---|
| `tools/eval/run_all.ps1` | TotM 같은 경로 | 그대로(프로젝트 이름만) | 1 |
| `tools/eval/regression/gdd_so_match.cs` | TotM 같은 경로 | 그대로에 가까움(GDD 표 ↔ SO 값 대조) | 1 |
| `tools/eval/regression/fx_doc_match.cs` | TotM 같은 경로 | 떼어 냄(연출 SO ↔ 문서 표 대조). 연출 SO를 쓸 때 | 2 |
| `tools/eval/scratch/` · `slow/` · `capture/` | TotM 같은 경로 | 빈 폴더(`scratch/`는 git 무시) | 1 |
| 나머지 `tools/eval/regression/*.cs`(zone_rules · section_check · cave_fx 등) | TotM | 참고: "성질" 검사 예시. 10-24 오탐 2건(`cave_fx_b` · `feel_modes`)은 튜닝 숫자에 묶인 나쁜 예 | — |
| `tools/rules/Program.cs` · `TotmRules.csproj` · `run.ps1` | TotM `tools/rules/` | 떼어 냄: 에디터 없는 규칙 검사 러너 골격 + `gdd_so_match`. `run.ps1`에 `-Changed`(바뀐 폴더 → 검사 대응표) 추가. `bin/` · `obj/` · `gen/`는 넘기지 않음 | 1 |
| `tools/rules/Shim/UnityEngine.cs` · `UnityEditor.cs` · `UnityEngine.Scene.cs` | TotM 같은 경로 | 그대로(Unity 없이 컴파일되는 대체 타입). `Shim/Sfx.cs`는 게임 전용 | 1 |
| `tools/perf/run.ps1` · `tools/perf/phone/*` | TotM 같은 경로(profile.sh · tmon · gc_alloc.cs · diag_table.py 등) | 그대로: 폰 WebGL 프레임 · 할당 측정. webgl-mobile 패키지 문서와 같이 | 2 |
| `.gitlab-ci.yml` | 새로(TOOLKIT 6장 설계안) | 새로: 1단계 = Linux Docker + .NET + pwsh로 `tools/rules/run.ps1`, LFS 끔 | 1 |

### 저장소 설정 (루트)

| 키트 파일 | 출처 | 다루는 법 | 순위 |
|---|---|---|---|
| `.gitignore` · `.gitattributes`(LFS) | TotM 같은 파일 | 떼어 냄: `references/` 하위 · `Library` 등은 그대로, TotM 전용 줄(원작 소리 폴더 등)은 "빌드 · 커밋 제외 폴더" 예시로 남김 | 1 |
| `.claude/settings.json` | TotM 같은 파일 | 그대로: 마켓플레이스 `unity-agent-plugin` · `super-dev-skills`, 플러그인 `unity` · `assets` | 1 |
| `.claude/skill-profile.yaml` | 이 저장소 `templates/skill-profile.yaml`(채운 예: TotM `.claude/skill-profile.yaml`) | 양식: 1일차에 채움 | 1 |
| `.claude/sound_labels.json` | TotM 같은 파일 | 양식: `groups` · `labels` · `tempTones` 빈 틀 | 2 |
| `.claude/launch.json` | TotM 같은 파일 | 떼어 냄: 저장소 루트를 여는 `sound-board` 서버 항목 하나(PC별 Python 경로는 사용자 폴더 기준으로) | 2 |

## B. Unity 패키지

| 패키지 | 넣을 파일(출처) | 다루는 법 | 순위 |
|---|---|---|---|
| `com.pudin.webgl-mobile` | 공용 원본 `_shared`(TotM `Packages/com.pudin.webgl-mobile`에 임베드된 사본) | 그대로(있음) | 1 |
| `com.pudin.tuning` | TotM `Scripts/Runtime/Debugging/FeelTuner.cs` · `LaunchTuner.cs`(FEEL TUNE · LAUNCH TUNE 화면 패널), `Scripts/Editor/FxTunerWindow.cs`(SO 묶음 편집 창), `tools/eval/regression/gdd_so_match.cs`. BH `Scripts/Dev/PhysicsLabTuning.cs` · `Scripts/Editor/PhysicsLabWindow.cs`(물리 랩 튜닝 탭) | 참고 + 떼어 냄: URP Rendering Debugger에 SO 탭을 자동으로 붙이는 패널로 새로 짠다(★ · ● · A/B · JSON 저장) | 1 |
| `com.pudin.feel` | TotM `Scripts/Runtime/Core/Haptics.cs` + `Plugins/WebGL/Haptics.jslib`(Android VibrationEffect · 웹 진동 길이 환산 10-26), `Scripts/Runtime/Gameplay/FeelFeedback.cs`, `Scripts/Runtime/Data/FeedbackTuning.cs`. BH `Scripts/Core/TimeEffects.cs`(히트스톱) · `Scripts/Core/CameraShaker.cs` · `Scripts/Core/Haptics.cs` · `Scripts/Feedback/HapticHooks.cs` · `Scripts/Data/HapticTuning.cs` | 떼어 냄: 순간 하나 = FeelPreset 에셋 하나로 합침. DOTween 의존 방식을 먼저 정함 | 2 |
| feel 안 FX 배치 도구 | TotM `Scripts/Runtime/Gameplay/FxPlacementGuide.cs`, `Prefabs/Fx/Combo/`(배치 프리팹 예), `Scripts/Runtime/Data/Fx/FxSetting.cs` · `FxLibrary.cs`(이펙트별 SO), `docs/FX_TUNING.md` "배치 프리팹 고치기". BH `Scripts/Feedback/VfxAnchors.cs` · `Scripts/Data/VfxAnchorSet.cs` · `Scripts/Editor/VfxAnchorNameDrawer.cs` · `Scripts/Data/PlayerFxSheet.cs` | 떼어 냄: 배치 프리팹 + `fx_*` 소켓 + 씬 뷰 핸들. 이펙트별 SO 51개(`Data/Fx/*`)는 TotM 연출이라 참고 | 2 |
| `com.pudin.devtools` | TotM `Scripts/Runtime/Debugging/DevTools.cs` · `BuildInfoOverlay.cs` · `DiagToggles.cs`, `UI/GameFlow.Dev.cs`(DEV 키 연결 예). BH `Scripts/Dev/DevPerfOverlay.cs` · `Scripts/Dev/PhysicsLabRecorder.cs`. TotM `tools/perf/phone/gc_alloc.cs` | 떼어 냄: 무적 · 멈춤 · 배속 연결 지점, 성능 오버레이, 빌드 정보 표시, 기록기 2개 | 2 |
| `com.pudin.artsync` | 없음(새로) | 새로. 소유 규칙은 TotM `CLAUDE.md` "버전 관리"(Art 브랜치는 `Art/`만) | 3 |
| `com.pudin.psdguard` · `uipsd` | TotM `docs/PITFALLS.md` "PSD · 스프라이트" 절, `docs/ART_GUIDE.md` | 참고 | 3 |

## C. super-dev-skills(이 저장소)

| 플러그인 · 스킬 | 넣을 것(출처) | 상태 · 다루는 법 | 순위 |
|---|---|---|---|
| `assets`(web-sound-search · web-vfx-search) | 이 저장소 | 있음(0.1.1). 새 과제는 `skill-profile.yaml` · `sound_labels.json`만 채움 | 1 |
| `editor-lease`(훅) | TotM `CLAUDE.md` "Unity CLI"(editor_status 확인 · 다른 세션 확인 규칙), `docs/PITFALLS.md` "공유 환경 · 여러 세션" | 새로 | 2 |
| `measure`(video-measure) | TotM `.claude/skills/reference-frame-sheet/` + `references/_tools/`(git 무시, 이 PC), `docs/PITFALLS.md` "레퍼런스 영상 측정" 절. BH `.claude/skills/reference-anim-sheet/` + `references/_tools/frame_inspector.html` | 새로(HANDOFF 시작 프롬프트) | 3 |
| `unity-webgl-mobile` 스킬 | 이 PC `~/.claude/skills/unity-webgl-mobile/`(사용자 스킬) | 옮겨 넣을 후보: webgl-mobile 패키지와 짝. 프로젝트 경로가 있으면 프로필로 | 2 |
| report-docx | TotM `tools/report/build_report_docx.py`(+ `crop_shots.py` · `make_compare_images.py`), BH `tools/report_docx/build_report_docx.ps1` · `md2docx.pl` | 새로(두 도구 합침) | 3 |
| draft-art | TotM `tools/art/make_draft_art.py` · `make_contact_sheet.py` · `contact_sheet.tpl.html` | 새로(나머지 `tools/art/*.py`는 TotM 그림 전용이라 참고) | 3 |
| archify | 외부 스킬(TotM `skills-lock.json`: `tt-a1i/archify`) | 복사하지 않음. 필요하면 새 과제에서 같은 출처로 설치 | — |

## D. PC 환경(저장소 밖)

| 무엇 | 출처 · 위치 | 넘기는 법 |
|---|---|---|
| Unity 6000.x + 모듈(WebGL · Android), Unity CLI | TotM `CLAUDE.md` "환경" · "Unity CLI"(PC마다 CLI 설치 경로가 다를 수 있으니 새 PC에서 다시 확인) | 설치 목록 + CLAUDE.md 양식의 경로 칸 |
| Python 3.12(+ Pillow · numpy · opencv), ffmpeg, Node 22, .NET SDK, Git + LFS | TotM `CLAUDE.md` "측정 도구", 이 저장소 README "A. 새 PC" | 설치 목록. Python은 `-I`로, `python`은 WindowsApps 스텁일 수 있음 |
| Android 테스트 기기 · adb | TotM `README.md` "폰에서 보기" | 설치 목록. 에뮬레이터와 같이 붙어 있으면 `adb -s <시리얼>`로 기기를 고름 |
| 디자이너 PC | TOOLKIT 4장 · 5장 | 1쪽 설치 안내(새로, 3순위 artsync와 같이) |

## 넘기지 않는 것

| 무엇 | 위치 | 이유 |
|---|---|---|
| 원작 소리 · 디컴파일 · APK · 녹화 · Fandom 그림 | TotM `Assets/_Project/Audio/Original/`, `references/decompiled/` · `apk/` · `videos/` · `fandom_assets/` | 원작 자료. 비공개 조건의 TotM 예외일 뿐이라 키트에 넣지 않음 |
| 원작 섹션 맵 | TotM `Assets/_Project/Data/SectionsOriginal/`, `tools/orig_sections/` | 같은 이유(10-16 예외는 TotM 한정) |
| 게임 코드 · 그림 · 섹션 · 튜닝 값 | TotM `Scripts/Runtime/Gameplay/` · `Map/` · `Data/*Tuning.cs` · `Art/` · `Data/` 등 | 게임 전용. 구조는 참고만 |
| 리포트 결과물 | TotM `docs/reports/*.docx` · `img/` 등 | 결과물. 양식만 넘김 |
| 빌드 · 캐시 · 생성물 | `Library/` · `Temp/` · `Builds/` · `build/` · `webgl_sharing/` · `ProfilerCaptures/` · `tools/rules/bin` · `obj` · `*.csproj` · `*.slnx` | 다시 만들어짐 |
| Claude 메모리 | `~/.claude/projects/<프로젝트>/memory/` | 프로젝트 기록. 다음 과제에 쓸 교훈은 PITFALLS · PLAYBOOK으로 옮긴 것만 |
| 토큰 · 사내 자격 증명 | — | 이 저장소 규칙 |

## 새 과제를 시작할 때 넘길 묶음

새 과제의 첫 Claude 세션에는 아래만 넘기면 된다.

1. **이 저장소** `binnini/super-dev-skills`: `docs/HANDOFF.md`(정한 것 · 다음 할 일), `docs/TOOLKIT.md`(도구 계획), 이 문서(파일 목록).
2. **project-template**으로 만든 새 GitLab 저장소(A 묶음이 들어 있음).
3. 과제 내용(과제 설명 · 기간 · 산출물 · 레퍼런스 영상 유무).

시작 프롬프트 예:

> 새 과제 저장소다. super-dev-skills의 docs/HANDOFF.md · TOOLKIT.md 7장(1일차) · KIT.md를 읽고, CLAUDE.md 양식을 과제 내용으로 채운 뒤 1일차 순서대로 진행하자. 3일차 결정 게이트(docs/DECISION_GATE.md)는 달력에 먼저 잡는다. 과제 내용: ○○
