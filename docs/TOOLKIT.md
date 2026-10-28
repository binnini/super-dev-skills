# 다음 과제 작업 도구함

BigHunter · TombOfTheMask 회고에서 정한 것(2026-10-24). 다음 과제에 들고 갈 도구와 환경을 산출물 단위로 정리했다. 산출물마다 어떤 형태인지, 어떻게 쓰는지, 지금 상태, 언제 만드는지를 적는다. 다음 과제가 클론이 아니어도 쓸 수 있게 클론 전용 부분은 선택 항목으로 뺐다.

- 그림이 있는 사람용 페이지: https://claude.ai/artifact/AzrnjGdJkP9CSyfukwMbdp (claude.ai 계정 비공개 아티팩트. 내용은 이 문서와 같다)
- 상태 표기: **있음** · **떼어 옮김**(두 저장소에 있는 것을 꺼내 합침) · **새로** · **나중**
- 패키지 이름과 코드 예시는 설계안이며 만들 때 바뀔 수 있다.
- 산출물마다 어느 저장소의 어떤 파일을 꺼내는지는 [KIT.md](KIT.md)(10-27).

| 산출물 | 형태 | 내용 |
|---|---|---|
| 1. 저장소 템플릿 | GitLab 템플릿 1개 | 폴더 · 문서 · 검사 골격. 1일차에 복제 |
| 2. Unity 패키지 | UPM 5개 + 나중 2개 | 손맛 · 튜닝 · 개발 도구 · 디자이너 작업 창 · WebGL 모바일 |
| 3. Claude 스킬 · 훅 | 이 저장소(super-dev-skills) | 영상 측정, 소리 · VFX 찾기, 병목 리포트, 에디터 잠금 |
| 4. 환경 | 설치 목록 + 에디터 3층 | 회사 PC · 폰 · GitLab |

## 하루 작업 흐름 속 위치

매일 같은 고리를 돈다: 레퍼런스 측정 → 구현(여러 Claude 세션) → 헤드리스 검사 → 에디터 확인 → 빌드 → 폰에서 사람 확인 → 튜닝 → 결정 기록. 고리를 막던 두 병목은 이렇게 줄인다.

- **에디터 하나**: 잠금 훅(editor-lease) + 검증 복제 프로젝트(에디터 3층)
- **사람 한 명의 확인**: 튜닝 패널(com.pudin.tuning)로 빌드 없이 폰에서 값 바꾸기 + 예약 빌드

## 1. 저장소 템플릿

### project-template — 떼어 옮김
| | |
|---|---|
| 형태 | GitLab 템플릿 저장소 하나 |
| 내용 | `Assets/_Project/` 골격, 빌더 Step 골격과 BuildScript, `tools/eval/`(regression · capture · scratch + `run_all.ps1`), `tools/rules/`(에디터 없이 도는 .NET 규칙 검사와 Unity 대체 Shim), `.gitignore` · `.gitattributes`(LFS) |
| 출처 | TotM `ProjectBuilder*`, `tools/eval`, `tools/rules` |
| 사용 | 1일차에 복제하고 프로젝트 이름만 바꾼다 |

### docs 세트 + 플레이북 v2 — 떼어 옮김
| | |
|---|---|
| 형태 | 템플릿 안 `docs/` 폴더의 빈 양식 |
| 내용 | CLAUDE.md 양식, SYSTEM.md(첫 장 = 원본 위치 표), GDD.md(마지막 장 = SO 수치표), PENDING.md, PITFALLS.md(두 프로젝트 함정 합본), handoff/, reports/daily/, 사람용 1쪽 요약 자리 |
| v2 추가 | 3일차 결정 게이트(컨셉 · 화면 폭 · 판정 크기 · 뼈 이름 · UI 구조), 연출 예산, 클론 측정 자동화, 테스트 계층 L0~L4와 테스트 작성 규칙(아래 5장). 리포트 A/B 양식과 원작 신뢰도 표기는 클론 과제일 때만 쓰는 선택 모듈 |
| 사용 | new-project 스킬이 질문하며 채운다 |

## 2. Unity 패키지

모두 UPM 패키지다. 원본에서 고치고 각 프로젝트 `Packages/`에 넣거나(embedded), GitLab 저장소를 git URL로 추가한다. 옛 PC의 공용 원본 폴더(`D:\GameProject\_shared\`)는 지금 PC에 없다(10-28 확인). webgl-mobile의 지금 원본은 TotM 저장소의 `Packages/com.pudin.webgl-mobile`이고, 패키지가 늘면 패키지마다 GitLab 저장소로 빼 git URL로 받는 쪽이 맞다.

### com.pudin.webgl-mobile — 있음
WebGL 모바일 템플릿 · 설정, URL 쿼리, Unity Play 업로드. 그대로 추가해서 저녁 빌드 → 폰 브라우저로 확인한다.

### com.pudin.feel — 새로 · 일부 옮김
| | |
|---|---|
| 의존 | Cinemachine 3(Unity 공식), DOTween(Asset Store 무료). **Feel(유료)은 사지 않는다** |
| 내용 | 순간마다 설정 에셋 하나(FeelPreset: 흔들림 · 히트스톱 · 찌그러짐 · 진동 · 소리 세기), 직접 쓴 진동(Android VibrationEffect, WebGL navigator.vibrate), 히트스톱(timeScale은 여기서만), 자체 카메라가 Impulse 신호를 읽는 수신기, 손맛 모드 전환 |
| 출처 | TotM Haptics · FeelFeedback, BigHunter TimeEffects · CameraShaker |

```csharp
// 설계안: 순간 하나 = 에셋 하나 (Data/Feel/Land.asset)
feel.Play(FeelId.Land, strength: hitSpeed / maxSpeed, at: pos);
// → 흔들림 + 히트스톱 + 찌그러짐 + 진동 + 음높이를 한 번에
```

### FX 배치 도구(feel 안) — 새로 · 일부 옮김
VFX의 크기 · 위치 · 타이밍을 사람이 에디터에서 직접 맞추게 한다. 이 기능을 한 번에 해 주는 공개 도구는 없어서 공식 기능에 작은 연결 코드를 붙인다.

| | |
|---|---|
| 위치 | 연출 하나 = 배치 프리팹 하나(원점 = 나오는 자리). 캐릭터 안에 `fx_*` 소켓(빈 자식). 숫자 오프셋은 씬 뷰에서 끄는 화살표 · 크기 원 핸들로 바꿈. FxPlacementGuide 안내선을 기본으로 넣음 |
| 타이밍 | 동작 연동 = 랩과 게임이 같은 FX 표를 읽고, 랩 타임라인의 표시를 끌면 표 값이 바뀜. 여러 효과가 이어지는 장면 = Timeline. 게임 사건 연동 = 지연(초) 칸 |
| 크기 · 모양 | 파티클 프리팹 자체(공식 씬 뷰 패널: 속도 · 즉시 반영 · 선택만 보기). FeelPreset에는 프리팹 · 소켓 이름 · 지연 · 세기만 |
| 시험 | 프리팹 모드 "재생", 플레이 중 "여기서 터뜨리기", 0.1배속 · 한 프레임. 고칠 값은 SO · 프리팹 에셋에 두어 플레이를 끝내도 남게 |
| AI와 같이 | 배치 프리팹 · FX 표는 사람 소유(빌더 · AI는 만들 때 한 번만 쓰고 이후 읽기만). AI는 도구 · 연결 코드를 만들고, 보이는 숫자는 사람이 화면을 보며 정함. AI가 값을 제안할 때도 같은 에셋에 쓰고 바꾼 내용을 표로 남김 |
| 출처 | BigHunter PlayerFxSheet · VfxAnchors · 랩 FX 패널, TotM 콤보 배치 프리팹 · FxPlacementGuide |

### com.pudin.tuning — 새로 · 일부 옮김
| | |
|---|---|
| 의존 | URP 코어의 Rendering Debugger(Unity 공식) |
| 내용 | SO마다 탭 자동 생성, ★ 자주 탭, 에셋 값과 다르면 ● 표시, A/B 저장 · 바꾸기, 되돌리기, 폰에 JSON 저장, 바뀐 값 목록, eval로 SO 반영, GDD 수치표 대조 검사 |
| 효과 | 바꾼 값을 폰에서 보려고 다시 빌드하는 일을 없앰. 설치된 개발 빌드 안에서 바꾸고, 정한 값은 다음 예약 빌드가 담음 |
| 출처 | TotM FEEL TUNE · LAUNCH TUNE · gdd_so_match, BigHunter 물리 랩 튜닝 탭 |

```csharp
// 설계안
[Header("대시")]
[Tune(pin: true), Range(20, 80)] public float dashSpeed = 36f; // 칸/s
// 시작할 때 한 줄
TuningPanel.Register(playerTuning, cameraTuning, feelTuning);
```

### com.pudin.devtools — 새로 · 일부 옮김
- 무적 · 멈춤 · 한 프레임 · 배속 · 되감기 연결 지점, 성능 오버레이(FPS · ms · 할당 · GC), 프로파일러 마커 규칙
- 병목 리포트용 기록기 2개: 에디터(컴파일 · 리로드 · 플레이 진입 · Step 시간), 폰(ProfilerRecorder로 마커별 ms · 할당)
- 교육 내용 헬퍼: 할당 없는 숫자 텍스트(TMP `SetText(char[])`), 디버그 전용 Assert와 항상 켜는 Require, unsafe 실험용 별도 asmdef
- 출처: TotM DevTools · BuildInfoOverlay, BigHunter DevPerfOverlay, 10/20 교육 샘플

```csharp
scoreText.SetNumber(score);        // 할당 0
Assert.That(grid.IsFree(cell));    // 제출 빌드에서 사라짐
```

### com.pudin.artsync — 새로
| | |
|---|---|
| 형태 | Unity 안 디자이너 작업 창(에디터 스크립트 수백 줄). PC에 설치된 git · git lfs를 백그라운드로 실행. 디자이너 PC에는 Git for Windows만 설치 |
| 버튼 | 최신 받기(저장 · 플레이 멈춤 → Dev를 Art에 합침 → LFS → 다시 읽기, 충돌이면 자동 취소), 내 작업 올리기(Art/ + .meta만 → 커밋 → push → 머지 요청 페이지 열기), 되돌리기(사본을 남기고), 잠그기 · 풀기(GitLab 파일 잠금, Project 창에 🔒 표시), 도움 요청(기록 복사) |
| 보호 | 바뀐 파일 중 Art/만 미리보기와 함께 보여 주고 개발 파일은 못 올림. 올리기 전 검사(이름 규칙 · PNG 크기 · PSD 레이어 변화). 한글 파일 이름 인코딩 처리 |
| 비상용 | 외부 GUI(SourceTree나 GitHub Desktop)를 같이 설치해 두고, 창이 처리 못 하는 일은 개발자가 그래프를 보며 정리 |
| 왜 직접 | 기존 도구는 GitHub for Unity 보관(2024-12), UniGit 오류 보고 등으로 디자이너에게 맡기기 불안. 필요한 기능이 좁아 작은 창이 맞음 |

### com.pudin.psdguard · uipsd — 나중
PSD 가드: 드롭마다 md5 · GUID · 레이어 ID · rect · 정렬 검사와 ID 다시 잇기. UI PSD 레이아웃: 레이어 이름 · 위치로 uGUI 프리팹 골격 생성, 이름으로 연결, SafeArea. 디자이너 PSD 작업이 있는 과제일 때 만든다.

## 3. Claude 스킬과 훅

스킬은 이 저장소(super-dev-skills, Claude Code 플러그인 마켓플레이스)에 모은다. 각 프로젝트는 `.claude/settings.json`에 이 저장소를 적어 받고, 버전을 올리면 업데이트로 받는다. 플러그인은 같이 켜고 끄는 단위로 나눈다. 프로젝트 경로는 스킬에 적지 않고 각 프로젝트의 `.claude/skill-profile.yaml`에서 읽는다. 설치 방법은 README "시작하기".

| 플러그인 | 스킬 · 훅 | 상태 |
|---|---|---|
| `assets` | web-sound-search, web-vfx-search | 있음(0.1.0) |
| `measure` | video-measure | 새로 · 다른 기기에서 |
| `ops` | bottleneck-report | 새로 |
| `editor-lease` | 에디터 잠금 훅 | 새로 · 나중에 |

### video-measure — 새로 · 다른 기기에서
| | |
|---|---|
| 형태 | `plugins/measure/skills/video-measure/`: SKILL.md(40줄 이하), `profiles/*.yaml`(게임별 상수), `scripts/vm.py`, `tests/golden/` |
| 대체 | reference-frame-sheet(TotM) + reference-anim-sheet(BigHunter) + `references/_tools` |
| 사용 | "이 영상에서 착지 흔들림 재 줘" |
| 시작 | `docs/HANDOFF.md` "video-measure 시작 프롬프트" |

```
vm cache  rec01.mp4 --profile game.yaml
vm events rec01.mp4           → events.csv (섬광 · 멈춤 · 흔들림)
vm sheet  rec01.mp4 f120-f150 --roi player
vm cite   events.csv 3        → rec01 · f123–f131 (0.267 s) ✅
```

### web-sound-search — 있음
Freesound · Pixabay 후보를 듣고 고르는 비교 페이지, 고른 소리를 사운드 슬롯에 넣고 라이선스를 기록하는 단계. "착지할 때 나는 소리 찾아줘".

### web-vfx-search — 새로 · 10-24 시험함
| | |
|---|---|
| 형태 | 스킬 + 비교 페이지 생성(`build_page.py`) + 시트 도구(`atlas_tools.py`) + Forge 자동 생성(`forge_gen.js`, Playwright) |
| 내용 | itch.io · OpenGameArt에서 도트 이펙트 후보를 찾아, 움직이는 미리보기를 실제 크기(캐릭터 한 칸 표시와 같이)로 놓고 ☆ · "이걸로 결정"으로 고르는 페이지. 맞는 게 없으면 Pixel Ability-fx Forge(Apache 2.0)로 시드를 바꿔 여러 개 만들어 같은 페이지에 넣음 |
| 규칙 | ① 무료 여부는 설명이 아니라 실제 받는 단계로 판단(최소 금액 0 · "No thanks, just take me to the downloads"). ② 돈을 내야 받는 것은 후보에서 빼고 "레퍼런스로만"에 둠. ③ 라이선스(출처 표기 · 재배포)를 카드마다 표시. ④ Forge는 모양을 시드가 정하므로 시드로 고르고 설정 · 시드를 README에 남김. ⑤ Forge 캔버스 최소 128 px라 결과가 약 4칸으로 큼 → 손질 단계를 같이 안내 |
| 결과물 | 고른 이펙트 묶음 zip: 시트 PNG · 낱장 PNG · 미리보기 GIF · README(다시 만드는 설정, Unity 임포트 값, 사용 조건). 필요하면 가운데 지우기 같은 간단한 손질본도 |
| 사용 | "자석 먹으면 플레이어 둘레에 노란 오라 생기는 이펙트 찾아줘" |

```
후보 찾기 → 받는 단계 확인(유료 빼기) → 미리보기 GIF(실제 크기)
  ↘ 맞는 게 없으면 forge_gen.js 시드 N개 → 둘레형만 남김
→ 비교 페이지 ☆ · 결정 → zip 전달 → FX 배치 도구로 Unity에 놓기
```

### bottleneck-report — 새로
| | |
|---|---|
| 형태 | 스킬 + Python 집계 스크립트(duckdb). 기록은 devtools 기록기 · Claude Code OpenTelemetry · 잠금 훅 · PENDING · git에서 받음 |
| 답하는 것 | "오늘 세션 시간은 어디에 갔나": 모델 응답 / 도구 실행 / Unity 컴파일 · 리로드 / 에디터 잠금 대기 / 사람 승인 대기 / 빌드에서 확인까지. 가장 느린 도구 명령, 폰 마커별 ms |
| 사용 | "오늘 병목 리포트 만들어 줘" → 대시보드 페이지 갱신. 일일 보고에 한 줄 요약 |
| 준비 | Claude Code 텔레메트리는 저장소 설정으로는 못 켜고 PC 환경 변수로 켬(`CLAUDE_CODE_ENABLE_TELEMETRY=1` + 수집기). 명령 내용 기록(`OTEL_LOG_TOOL_DETAILS`)은 사내 정책 확인 뒤 |

```
events.jsonl · editor_timing.jsonl · lease.jsonl · perf.jsonl
  → duckdb 집계 → 대시보드 페이지
```

### editor-lease 훅 — 새로 · 나중에 만들기로 함
| | |
|---|---|
| 형태 | 플러그인 `editor-lease`의 PreToolUse · SessionEnd 훅 + `lease.ps1` |
| 동작 | Claude가 `unity.exe command`를 부르기 직전에 잠금 파일을 확인한다. 다른 세션이 쥐고 있으면 이유와 함께 막고, 10분 동안 쓰지 않으면 자동으로 푼다 |
| 사용 | 평소에는 자동. 직접 에디터를 쓸 때만 `lease.ps1 take` · `release` |
| 주의 | Unity 에디터가 있는 Windows PC에서만 의미가 있다. 클라우드 세션에서는 만들 수는 있어도 시험할 수 없다 |

### 나중에 만들 스킬 5개 — 나중
- **new-project**: 템플릿 복제 · CLAUDE.md 채우기 · 첫 폰 빌드
- **daily-report · handoff**: git log · PENDING에서 일일 보고와 인계 문서
- **report-docx**: md → 회사 양식 docx(두 도구 합침)
- **psd-drop**: PSD 받기 → 가드 → Step → 캡처 비교
- **draft-art**: 그림 목록의 빈 자리를 도트 시안으로

## 4. 환경

| 구분 | 무엇 | 쓰는 곳 | 상태 |
|---|---|---|---|
| 엔진 | Unity 6000.x, URP 2D, Input System, 2D Tilemap, PSD Importer, Aseprite Importer, Cinemachine 3, DOTween, Animation Sequencer(UI 움직임, MIT, 버전 고정), Device Simulator | 게임 | 있음. Cinemachine · DOTween · Sequencer 추가 |
| 디자이너 PC | Unity Hub + 같은 Unity 버전 · 모듈, Git for Windows(LFS · 로그인 관리자 포함), 비상용 외부 Git GUI 하나. 1쪽짜리 설치 안내 + 30분 같이 설치 | 디자이너 | 새로 |
| 에디터 조작 | Unity CLI(베타) `eval_file` · `status`. Unity MCP는 다중 에디터가 필요해지면 시험 | Claude 세션 | 있음 |
| 에디터 3층 | L0 터미널(모든 세션) · L1 검증 복제 프로젝트 1~2개 · L2 메인 에디터 1개. RAM 32 GB 이상, 기능별 asmdef, 플레이 진입 리로드 끄기 | 회사 PC | 구성 |
| 측정 | ffmpeg, Python 3.12(`-I` 실행) + numpy · opencv · pillow. 선택: Tracker · Kinovea(사람이 직접 측정) | video-measure | 있음 |
| 헤드리스 검사 | .NET SDK(`tools/rules`), PowerShell | L0 · 잠금 훅 | 있음 |
| 버전 관리 | Git + LFS, GitLab(Dev · Art · main). 선택: Unity Accelerator(임포트 캐시) | 팀 | 있음 |
| CI | GitLab CI 3단계(5장). 1단계는 Linux Docker 러너 + .NET · PowerShell만, Unity 라이선스 불필요 | 팀 · 저녁 빌드 | 새로 |
| 기기 | Android 개발 빌드(진동 · 손맛), 모바일 브라우저 WebGL(제출 · 공유) | 사람 확인 | 있음 |
| 코드 규칙 | Update 하나 + 시스템 순서, 프레임 이벤트 목록, 규칙 난수 분리, 고정 스텝, 할당 0, 마커 근거 없는 최적화 금지, unsafe는 실험 asmdef에서만 | 템플릿 · devtools | 규칙 |

## 5. 디자이너 협업 · UI — 사람이 화면에서 고치는 구조

두 프로젝트에서는 UI와 VFX를 코드가 배치해 사람이 나중에 고치기 어려웠고, 그림은 DM · 드라이브로 주고받아 버전이 섞였다. 다음 과제에서는 **배치 · 움직임 · 그림은 사람이 Unity에서 직접 고치고, AI는 도구 · 연결 · 흐름을 맡는다.**

### UI 작업 방식
| 무엇 | 어디에 두나 | 누가 고치나 |
|---|---|---|
| 배치(위치 · 크기 · 앵커 · 간격) | UI 프리팹의 RectTransform · Layout Group · SafeArea. 처음 골격은 디자이너 시안 PSD의 레이어 위치에서 자동 생성(uipsd). 코드가 꼭 움직여야 하는 UI(캐러셀 등)도 기준값은 프리팹에서 읽고 숫자는 그 컴포넌트 인스펙터에. `[ExecuteAlways]`로 편집 모드에서도 보이게 | 사람 |
| 움직임 | 짧고 반복되는 것(나타남 · 사라짐 · 튀어오름) = Animation Sequencer(상대값, 멈춰 있을 때 비용 없음, 편집 모드 미리보기). 프레임 단위 안무(로고 등장 등) = 애니메이션 클립 · Timeline, 위치는 자식을 움직여 배치와 부딪히지 않게. 코드는 `Show()` · `Hide()` · `Play()`만 | 사람 |
| 내용(숫자 · 글자 · 그림 바꾸기) | 화면별 뷰 스크립트. 자식 이름 `ui_<화면>_<요소>`로 찾아 연결(옮겨도 안 끊김). 숫자 텍스트는 할당 0 | AI |
| 흐름(어느 화면을 언제) | 화면 상태 기계 | AI |
| 확인 | Device Simulator(화면 비율 · 노치 · 안전 영역)를 에디터에서. 여러 비율 캡처 모음을 L2 검사에 | 사람 · 검사 |

UI 시스템은 uGUI를 유지한다(Unity 6 문서의 게임 안 UI 권장, 디자이너 스프라이트 · 도트에 맞음). Animator는 UI를 매 프레임 다시 그리게 만든다는 Unity 문서 경고가 있어 짧은 움직임은 Sequencer로 한다. UI 프리팹과 FX 배치 프리팹처럼 디자이너가 다듬는 프리팹은 `Art/` 아래로 옮겨 소유를 폴더로 표시하고, AI · 빌더는 골격을 처음 만들 때만 쓴다. 배치를 바꿔야 하면 AI는 말로 제안하거나, 요청받았을 때만 고치고 바꾼 값을 표로 남긴다.

### 그림 파일 형식
| 종류 | 형식 | 이유 |
|---|---|---|
| 리그가 있는 캐릭터 | PSD(큰 캔버스면 PSB) | 뼈 · 가중치 · 레이어 위치를 담을 곳이 이것뿐. PSD 가드를 반드시 같이 |
| UI | 요소별 PNG + 배치 시안 PSD 한 장 | 여러 화면에서 다시 쓰고 9칸 자르기 · 아틀라스가 필요. PSD를 그대로 넣으면 레이어 ID 문제와 큰 아틀라스가 따라옴. 시안 PSD는 위치 정보로만 씀 |
| 도트 · 프레임 애니메이션 | Aseprite(태그 = 상태) 또는 PNG 가로 시트 | Aseprite Importer가 태그를 클립으로. 같은 캔버스 · 같은 중심 |
| 배경 · 정지 소품 · VFX 텍스처 | PNG | 단순, 같은 이름 덮어쓰기로 교체 끝 |

주고받는 규칙: 파일 이름이 계약(`그룹_이름_상태`), 고칠 때는 같은 파일을 .meta째 덮어쓰기, PSD 레이어는 지우거나 새로 만들지 않고 고치기, 같은 대상의 프레임은 같은 캔버스 · 중심, 받는 쪽에서 자동 검사.

### 디자이너 협업 환경
| 영역 | 구성 | 디자이너가 하는 일 |
|---|---|---|
| 설치 | 1쪽짜리 설치 안내(Unity Hub, 정확한 버전 · 모듈, Git for Windows, 저장소 받기), 30분 같이 설치 | 따라 하기 한 번 |
| 받기 · 올리기 | Unity 안 디자이너 작업 창(com.pudin.artsync). 명령어 안내는 비상용으로만 | 버튼 4~5개 |
| 충돌 막기 | 소유를 폴더로(디자이너 = `Art/`). PSD · 프리팹은 GitLab 파일 잠금(Git LFS lock, Free 요금제 가능). 브랜치는 지금처럼 Art · Dev, 합치기는 개발자가 하루 한 번 | 고치기 전 "잠그기" |
| 자동 검사 | CI 1단계(Linux, Unity 없음): 파일 이름 규칙, PNG 크기 · 캔버스 · 반투명 픽셀, Art/ 밖 파일, PSD 레이어 이름 · 크기 대 메타(Python psd-tools). 결과는 머지 요청에 사람 말로 | 빨간 표시가 뜨면 안내대로 |
| 확인 · 플레이 | 예약 빌드의 Unity Play 링크(Unity 없이 브라우저), 랩 씬 · FX 배치 도구 · Device Simulator | 링크 열기, 재생 버튼 |
| 피드백 | 머지 요청 하나 = 대화 하나. 양식(무엇을 바꿨나 · 크기 바뀜 · 새 레이어) 체크박스, 개발자는 캡처를 붙여 댓글 | 체크박스 채우기 |

도입 순서: 1일차 = 설치 같이 하기 · 디자이너 작업 창(받기 · 올리기 · 되돌리기) · Art/ 경로 검사. 첫 주 = 파일 잠금 · PNG · PSD 자동 검사 · 머지 요청 양식. 그 뒤 = 디자이너 소유 UI · FX 프리팹을 Art/로, 랩 씬 정리.

## 6. 테스트 · CI

두 프로젝트에서는 세션마다 빌드와 전체 검사를 돌려 시간이 많이 들었다. 작업 세션은 가벼운 검사만, 전체 검사와 빌드는 합칠 때 한 곳에서 한 번 돌린다.

### 테스트 계층과 돌리는 사람
| 단계 | 내용 | 시간 | 누가 · 언제 |
|---|---|---|---|
| L0 컴파일 | 오프라인 컴파일(csc_check, dotnet build) | 초 | 모든 세션, 코드를 바꿀 때 |
| L1 영향 검사 | `tools/rules` 중 바뀐 폴더에 연결된 것만(`run.ps1 -Changed`) | 초~수십 초 | 모든 세션, 작업을 끝낼 때 + CI 1단계가 push마다 전체 |
| L2 전체 회귀 | 헤드리스 전체 + 에디터 run_all + 느린 검사 + 플레이어 스크립트 컴파일 검사(제출 · Android · WebGL 설정으로 스크립트만 컴파일, 수 초) | 분 | 통합 담당 하나, Dev에 합칠 때(에디터 잠금 차례) |
| L3 빌드 | APK(약 84초) · WebGL · 제출 빌드 | 분 | CI 2단계: 사용자가 입력한 시각(예: 점심 · 퇴근 전)의 예약 빌드 + 필요할 때 수동 빌드(필수), 제출 전. 작업 세션은 직접 빌드하지 않고 수동 빌드를 요청 |
| L4 사람 확인 | 폰 플레이 · 튜닝 패널 | 10분 | 저녁 빌드 뒤 |

### 무엇을 바꿨을 때 빌드가 필요한가
| 바꾼 것 | 확인 방법 | 빌드 |
|---|---|---|
| 값만(SO · 프리팹 수치) | 에디터 플레이 모드, 또는 이미 설치된 폰 개발 빌드의 튜닝 패널. 정한 값은 JSON 저장 → eval로 SO 반영 | 필요 없음. 다음 예약 빌드에 포함 |
| 코드 조금 | 에디터 플레이 모드 + 플레이어 스크립트 컴파일 검사(수 초) | 필요 없음. 다음 예약 빌드에 포함 |
| 플랫폼 코드, 튜닝 패널에 없는 것(그림 · 새 연출 · 새 기능)을 폰에서 봐야 할 때 | 수동 빌드 한 번 | 필요할 때만 |

빌드 횟수를 줄이는 데 가장 효과가 큰 것은 튜닝 패널을 1일차부터 넣는 것이다. 플레이어 스크립트 컴파일 검사(`PlayerBuildInterface.CompilePlayerScripts`)는 "코드가 빌드를 깨뜨렸나"를 빌드 없이 확인하고, 바꾼 값을 폰에서 보는 일은 튜닝 패널이 맡는다.

### 테스트 작성 규칙(플레이북 v2)
- **성질**: 숫자가 아니라 성질을 본다(연출을 켜든 끄든 결과가 같다, 모든 섹션을 탈출할 수 있다, 문서와 에셋이 같다). 기대값은 SO에서 읽어 계산. 10/24 오탐 2건이 튜닝 숫자에 묶인 검사였다.
- **안정**: 시드 · 봇에 기대는 검사는 여러 시드나 고정 입력 순서로.
- **대응표**: 폴더 → 검사(Map/ → zone_rules · section_check, Data/Tuning/ → gdd_so_match, Data/Fx/ → fx_doc_match, 연출 코드 → cave_fx).
- **관리**: 느린 검사도 L2에서 반드시 돌린다(목록 밖 검사는 썩는다). 새 검사는 망가뜨린 사본에서 FAIL이 나는지 먼저 확인. 커밋은 하나씩 컴파일되게.

### GitLab CI 3단계
| 단계 | 내용 |
|---|---|
| 1단계 | push마다 에디터 없는 검사. Linux Docker 러너에 .NET SDK + PowerShell만 있으면 됨. Unity 라이선스 불필요. TotM `tools/rules` 6개를 Linux에서 그대로 돌려 FAIL 0, 빌드 포함 26초 확인(10/24) |
| 2단계 | 예약 빌드 + 수동 빌드. 작업 PC에 GitLab Runner(shell, 내 Windows 계정)를 등록. 예약 시각은 GitLab 파이프라인 예약(Schedules)에 사용자가 입력하고, 수동 빌드는 "파이프라인 실행" 버튼에서 플랫폼(WebGL · Android · 제출)을 골라 실행. 순서 = 플레이어 스크립트 컴파일 검사(실패하면 바로 멈춤) → 빌드 → WebGL은 Unity Play 업로드, APK는 정해진 폴더로. 설치된 Unity를 쓰므로 라이선스 문제가 적음. 메인 에디터와 같은 폴더는 못 열므로 검증 복제 폴더에서 실행 |
| 3단계 | 필요할 때. GameCI Docker Unity로 에디터 회귀 · 빌드를 서버에서. Unity 라이선스 활성화 설정이 필요. 합치기 전 묶음 검사(merge train)는 GitLab Premium인지 확인 |
| 준비 | 사내 GitLab에 쓸 수 있는 러너가 있는지 관리자에게 확인. Git LFS 가져오기는 1단계에서 끔(그림이 필요 없음) |

```yaml
# .gitlab-ci.yml 1단계 (설계안)
rules:
  image: mcr.microsoft.com/dotnet/sdk:10.0
  variables: { GIT_LFS_SKIP_SMUDGE: "1" }
  script: [ pwsh -NoProfile -File tools/rules/run.ps1 ]
```

## 7. 새 과제 1일차

1. **템플릿 복제**: GitLab에서 project-template으로 새 저장소를 만들고 Dev · Art · main 브랜치를 연다.
2. **문서 채우기**: new-project 스킬(아직 없으면 CLAUDE.md 양식을 직접)로 원본 위치 표, 과제 범위, 클론 여부를 정한다. 클론이 아니면 리포트 A/B 모듈을 뺀다.
3. **패키지 추가**: webgl-mobile, tuning을 넣고 빌더 Step 1을 실행한다. feel(Cinemachine 3 · DOTween)과 devtools는 만들어 둔 뒤에 넣는다(8장 2순위).
4. **스킬 받기**: README "시작하기 B"대로 이 저장소를 프로젝트에 넣고 `.claude/skill-profile.yaml`을 채운다.
5. **폰에 빈 씬**: 저녁 전에 Android와 모바일 브라우저 양쪽에서 빈 씬이 뜨는지 확인한다. 튜닝 패널이 열리는지도 같이 본다.
6. **레퍼런스**: 영상이 있으면 video-measure로 사건 표부터 뽑아 `docs/references/`에 둔다.
7. **에디터 3층**: 검증 복제 프로젝트를 만들고 잠금 훅을 켠다(훅이 아직 없으면 첫 주 안에). 이후 세션은 영역별로 나눠 띄운다.
8. **3일차 결정 게이트를 달력에**: 컨셉 · 화면 폭 · 판정 크기 · 뼈 이름 · UI 구조를 그날 폰에서 회색 박스로 보고 묶는다.

## 8. 만드는 순서

10-27에 다시 정함. 처음 계획은 "마감 뒤 이틀"에 8가지를 모두 만드는 것이었지만 이틀로는 무리라, **TotM에서 시간이 가장 많이 샌 곳을 막는 것부터** 순위를 매겼다. 1순위 네 가지만 있어도 7장 1일차가 돈다. 나머지는 과제를 하며 필요할 때 떼어 온다.

| 순위 · 시점 | 만들 것 | 막는 것(TotM 근거) |
|---|---|---|
| **1순위** · 과제 시작 전 | ① project-template + docs 세트 + 플레이북 v2(테스트 작성 규칙 · 계층 · `run.ps1 -Changed`) | 문서 틀(원본 위치 표 · SO 수치표 · PENDING · PITFALLS)은 검증됨. 10-24 회귀 실패 2건이 튜닝 숫자에 묶인 검사였음 → 처음부터 "성질" 검사로 |
| | ② com.pudin.tuning(튜닝 패널) | 거의 모든 작업이 "폰 확인 대기"로 남고, 값 몇 개마다 다시 빌드 · 설치했음. 빌드 횟수를 줄이는 데 효과가 가장 큼 |
| | ③ CI 1단계(`.gitlab-ci.yml`, Linux Docker + .NET + pwsh, LFS 끔) | `tools/rules`가 Linux에서 FAIL 0 · 26초(10-24). 설정 파일 하나로 push마다 규칙 검사 |
| | ④ 3일차 결정 게이트(만들 것 없음, 달력 · 템플릿 체크리스트) | 어항 → 심해 동굴(10-19), 하강 전환 뒤 되돌림, 맵 13 → 10칸(10-20) 같은 늦은 방향 전환이 섹션 · 아트 · 검사 수정을 줄줄이 불렀음 |
| **2순위** · 과제 첫 주 | editor-lease 훅 + 검증 복제 프로젝트 | 에디터 하나를 여러 세션이 나눠 써서 "다른 세션이 쓰는 중이면 묻기"를 사람이 하고 있었음 |
| | 배치 소유 규칙(UI · FX 배치 프리팹은 `Art/` 아래, 사람 소유) | UI · 연출 수치를 코드 · SO 51개로 두어 디자이너가 화면을 보며 고치기 어려웠음(10-27 디자이너 UI). 정하기만 하면 되는 규칙 |
| | 디자이너 협업 최소판: `Art/` 소유 · LFS 파일 잠금 · CI 그림 자동 검사 · 머지 요청 양식 | 그림을 DM · 드라이브로 주고받아 버전이 섞였음 |
| | com.pudin.feel(FX 배치 도구 포함), com.pudin.devtools(기록기 포함) | feel은 **DOTween(Asset Store) 의존 방식을 먼저 정한다**(UPM 의존성으로 바로 안 걸림: 프로젝트에 먼저 설치 + asmdef 참조 등) |
| | new-project, daily-report · handoff 스킬, CI 2단계(예약 · 수동 빌드) | 실제 과제 하나를 셋업하면서 절차를 확정 |
| **3순위** · 필요할 때 | com.pudin.artsync(디자이너 작업 창) · 디자이너 설치 안내 | 비개발자용 git 자동화라 가장 위험함(충돌 · LFS 꼬임 수습은 개발자 몫). 최소판을 써 보고 디자이너가 실제로 막히는 지점을 본 뒤 만든다 |
| | bottleneck-report(`ops` 플러그인) | 위 항목들이 병목을 직접 줄인다. 텔레메트리 설정 · 사내 정책 확인도 필요 |
| | video-measure(`measure` 플러그인, 다른 기기에서) | 다음 과제가 클론이 아니면 급하지 않음. 영상 레퍼런스가 실제로 생길 때. 시작 프롬프트는 HANDOFF.md |
| | psdguard, uipsd, psd-drop, draft-art, report-docx, CI 3단계(GameCI) | 디자이너 PSD · 제출 문서 · 서버 빌드가 실제로 있을 때 |
