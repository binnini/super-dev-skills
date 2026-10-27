# 인계: 클론 한 달 회고 → 다음 과제 준비 (2026-10-24)

BigHunter(9/29~10/13) · TombOfTheMask(10/14~10/27 마감)를 회고하고 다음 과제에 들고 갈 도구를 정한 대화(claude.ai/code 클라우드 세션)를 이어받기 위한 문서다. 다른 환경의 Claude는 그 대화를 볼 수 없으니, 여기 적힌 것이 기준이다.

- 다음 과제는 클론이 아닐 가능성이 높다. 다만 영상 레퍼런스를 프레임 단위로 분석하는 일은 계속한다.
- 도구 계획 전체는 [TOOLKIT.md](TOOLKIT.md). 이 문서는 **정한 것 · 남은 일 · 시작 프롬프트**만 모은다.

## 이어서 시작하는 법

새 세션에서 이 저장소를 열고:

> docs/HANDOFF.md를 읽고 "다음 할 일"의 ○○부터 하자.

게임 저장소 작업이면 그 저장소의 CLAUDE.md 규칙이 우선이다(Unity CLI · 에디터 사용 확인, 커밋은 요청할 때만 등).

## 만든 것

| 무엇 | 어디 | 비고 |
|---|---|---|
| 스킬 저장소 | 이 저장소. 플러그인 `assets` 0.1.0(web-sound-search, web-vfx-search) | 설치는 README "시작하기" |
| 작업 도구함 | [TOOLKIT.md](TOOLKIT.md) · 페이지 https://claude.ai/artifact/AzrnjGdJkP9CSyfukwMbdp | 페이지는 사람용(같은 claude.ai 계정에서 열림) |
| 클론 한 달 회고 페이지 | https://claude.ai/artifact/XNpHfouQmfVRGXMAhD6YXr | 커밋 · 교육 · 작업 방식 · 아트 리소스 · 떼어 낼 것 |
| 두 클론 아키텍처 지도 | https://claude.ai/artifact/Di6srmr7UHfRPNV4bSo4MC | BigHunter(MonoBehaviour + 정적 이벤트) vs TotM(GameplayController.Step) |
| 자석 오라 비교 페이지 | https://claude.ai/artifact/Q5nrPdzzr5tTEGstvjVXKr | web-vfx-search 시험(10-24). Forge 5개 + 0원 2개, 유료는 레퍼런스로만 |
| 자석 오라 · 일렁이는 테두리 묶음 | 사용자에게 zip으로 전달(magnet_aura_waves.zip) | Forge Aura · Solar · Radiance(holy) · 128 px · 24프레임 · 시드 215. 원본 + 가운데 지운 손질본 |

페이지는 모두 claude.ai 계정의 비공개 아티팩트다. 다른 사람에게 보여 주려면 페이지의 공유 메뉴에서 공유해야 한다.

## 정한 것

| 날짜 | 주제 | 결정 | 이유 · 근거 |
|---|---|---|---|
| 10-24 | 손맛 키트 | **Cinemachine Impulse + DOTween + 진동은 직접 작성.** Feel(유료)은 사지 않음 | 공식 · 사용자 많은 패키지로 충분. 진동은 Android VibrationEffect · WebGL navigator.vibrate 몇 줄 |
| 10-24 | 튜닝 키트 | URP Rendering Debugger에 SO 탭을 자동으로 붙이는 패널(com.pudin.tuning). 탭 배치(★ 자주 · SO별 · 프리셋 · 정보)는 미리 정해 둠 | 공식 UI라 만들 것이 적음. 바꾼 값을 폰에서 보려고 다시 빌드하는 일을 없앰 |
| 10-24 | 에디터 병목 | **에디터 3층**: L0 터미널 검사(모든 세션) · L1 검증 복제 프로젝트 · L2 메인 에디터 1개 + 잠금 훅 | 에디터 임포트 · 컴파일 · 플레이는 메인 스레드라 C# 멀티스레드로는 안 풀림. 병렬은 프로세스 단위로 |
| 10-24 | 멀티스레드 | 게임 쪽은 지금 규모에서 큰 이득 없음. WebGL은 일반 C# 스레드가 안 되고 Burst 잡만 조건부. 큰 계산(빛 지도 · 맵 생성 · 경로 탐색)이 프로파일러에서 무거울 때만 Job + Burst 검토 | 멀티코어 이득이 확실한 곳은 영상 분석(구간별 프로세스)과 헤드리스 검사 병렬 |
| 10-24 | 교육 적용 | 순서: **측정 → 구조 → 할당 0 → 검증 → 엔진 호출 → unsafe.** DOD 구조(Update 하나 + 시스템 순서, 프레임 이벤트 목록, 타이머 배열, 정해진 지점 삭제, 규칙 난수 분리)는 첫날부터. Span · stackalloc · ArrayPool은 핫패스만, unsafe는 실험 asmdef에서만, TransformHandle + Burst는 폰 프로파일을 보고 | 10/13 DOD(Anxi) · 10/20 .NET · Unity 최적화(Dandel) 교육. TotM은 DOD와 닮았지만 10/20 내용은 거의 안 쓰임 |
| 10-24 | 영상 분석 | 기존 두 스킬을 합쳐 **video-measure를 새로** 만든다(압축 · 빠르게). 다른 기기에서 시작 | `references/_tools`와 녹화가 그 기기(회사 PC)에만 있음 |
| 10-24 | 병목 모니터링 | bottleneck-report 하나만 만든다(Claude Code OpenTelemetry + 에디터 · 폰 기록기 + 잠금 기록 → duckdb) | 리깅 · 도트 작업 병목 조사 결과, 별도 도구보다 기록을 모아 보는 것이 맞음 |
| 10-24 | VFX 배치 | 연출 하나 = 배치 프리팹 하나, `fx_*` 소켓, 씬 뷰 핸들, 타이밍 표시. 위치 · 크기 · 타이밍 숫자는 **사람 소유 에셋**, AI는 도구 · 연결만 | AI가 코드로 위치를 바꾸면 사람이 따라갈 수 없었음. 한 번에 해 주는 공개 도구는 없음 |
| 10-24 | 테스트 | L0~L4 계층. 작업 세션은 L0 · L1만, L2는 합칠 때, 빌드는 CI 2단계 | 세션마다 빌드 · 전체 검사를 돌려 시간이 많이 들었음 |
| 10-24 | 빌드 | **사용자가 입력한 시각(점심 · 퇴근 전)에 예약 빌드 + 수동 빌드 버튼은 반드시.** 플레이어 스크립트 컴파일 검사를 빌드 앞에 둠 | 값 몇 개 고칠 때마다 다시 빌드하는 비효율. 값은 튜닝 패널, 코드는 컴파일 검사로 |
| 10-24 | CI | GitLab CI 3단계. 1 · 2단계는 작업 PC 하나로 가능(1단계 Linux Docker 공용 러너, 2단계 작업 PC Runner) | TotM tools/rules가 Linux에서 FAIL 0 · 26초로 돎(10-24 확인) |
| 10-24 | UI | 배치는 프리팹(사람), 움직임은 Animation Sequencer 또는 클립(사람), 내용 · 흐름은 코드(AI). uGUI 유지, `ui_<화면>_<요소>` 이름 연결 | UI를 코드가 배치해 나중에 고치기 어려웠음 |
| 10-24 | 그림 형식 | 리그 캐릭터 PSD, UI는 요소별 PNG + 배치 시안 PSD, 도트는 Aseprite/PNG 시트, 나머지 PNG | TOOLKIT 5장 |
| 10-24 | 디자이너 협업 | Unity 안 디자이너 작업 창(com.pudin.artsync, git을 백그라운드로) + 비상용 SourceTree/GitHub Desktop. 소유는 폴더(Art/), PSD · 프리팹은 GitLab 파일 잠금 | 디자이너는 Unity · Git에 서툼. 기존 Unity Git 도구는 보관 · 오류 보고로 불안 |
| 10-24 | 스킬 저장소 | 이 저장소(GitHub `binnini/super-dev-skills`)를 Claude Code 플러그인 마켓플레이스로. 프로젝트 경로는 `.claude/skill-profile.yaml` | 프로젝트마다 복사하던 스킬을 한곳에서 고치고 업데이트로 배포 |
| 10-24 | VFX 에셋 | **유료 에셋은 추천하지 않는다. 유료 에셋을 레퍼런스로 삼아 만드는 것은 허용.** 무료 여부는 실제 받는 단계로 확인 | 처음 찾은 후보가 받을 때 결제 창이 떠 유료로 보였음("원하는 만큼 내기"는 0원 가능) |
| 10-24 | VFX 생성 | 맞는 무료 에셋이 없으면 Pixel Ability-fx Forge(Apache 2.0)로 만든다. 모양은 시드로 고른다 | 10-24 headless로 24개 생성 · 비교. 결과물 사용 조건은 명시가 없어 확인 권장 |

## 다음 할 일

### 지금 · 마감(10/27) 전
- [ ] TotM 마감 작업(이 저장소 밖)
- [ ] 자석 오라: 비교 페이지에서 ☆ · 결정 → 고른 것을 TotM에 넣을지 정하기. 지금 게임의 자석 색은 분홍(`PowerupScreenFx.magnetColor` #FF4FA0)이고 CONCEPT에서 노랑 · 흰색은 수집물 색이라 헷갈릴 수 있음 → 같이 결정
- [ ] 각 게임 저장소에 이 스킬 저장소를 넣기(README "시작하기 B"). TotM은 10-27 완료(assets 0.1.1에 로컬 복사본의 현황 페이지 등을 옮긴 뒤 복사본을 지움, TotM 커밋 전). BigHunter 남음

### 10/27 마감 뒤 이틀 (TOOLKIT 8장)
- [ ] project-template + 플레이북 v2(테스트 계층 · `run.ps1 -Changed`)
- [ ] CI 1단계(`.gitlab-ci.yml`, Linux Docker + .NET + pwsh, LFS 끔)
- [ ] com.pudin.feel(FX 배치 도구 포함), com.pudin.tuning, com.pudin.devtools(기록기 포함)
- [ ] 플러그인 `editor-lease`(Unity 에디터가 있는 Windows PC에서 만들고 시험)
- [ ] 플러그인 `ops` · bottleneck-report
- [ ] com.pudin.artsync + 디자이너 1쪽 설치 안내

### 다른 기기에서
- [ ] 플러그인 `measure` · video-measure (아래 시작 프롬프트)

### 과제 첫 주 · 필요할 때
- [ ] new-project, daily-report · handoff 스킬, CI 2단계(예약 · 수동 빌드), 파일 잠금 · 그림 자동 검사 · 머지 요청 양식
- [ ] psdguard, uipsd, psd-drop, draft-art, report-docx, CI 3단계(GameCI)

## video-measure 시작 프롬프트

`references/_tools`와 녹화가 있는 기기에서, 이 저장소와 게임 저장소를 같이 연 세션에 붙여 넣는다.

````markdown
# 목표: 영상 레퍼런스 측정 스킬 `video-measure` 새로 만들기

super-dev-skills 저장소에 플러그인 `measure`를 새로 만들고 그 안에 스킬 `video-measure`를 둔다
(저장소 CLAUDE.md 규칙: 프로젝트 경로는 skill-profile, 버전 · CHANGELOG, tests/run_tests.py에 검사 추가).

## 배경
두 프로젝트에 같은 일을 하는 스킬이 따로 있다. 둘을 하나로 합치고, 더 압축하고, 더 빠르게 만든다.
다음 과제는 클론이 아닐 수 있으니 게임에 묶이지 않게 만든다.
- TombOfTheMask: `.claude/skills/reference-frame-sheet/` + `references/_tools/`의 Python 스크립트
  (tomtools · crops · track · dashes · zones · hudstrip · pano · gridify · shake · rot · rot_ecc · cyanblobs · screenstats · lava)
- BigHunter: `.claude/skills/reference-anim-sheet/` + `references/_tools/frame_inspector.html`(브라우저 JS, 느림, 45초 끊김 우회)
- 위치(회사 PC): `C:\Users\111percent\workspace\TombOfTheMask\references\_tools\`, `C:\Users\111percent\workspace\bighunter\references\_tools\`

## 지금 문제
1. 스킬이 두 개이고 도구도 두 벌이다.
2. SKILL.md에 절차 · 게임별 상수(1칸 68 px, 지면선 567) · 문서 갱신 체크리스트가 섞여 매번 전부 읽힌다.
3. 도구가 git 무시 폴더에 있어서 버전 관리가 안 된다.
4. 스크립트마다 영상을 다시 디코딩한다.
5. 숫자보다 그림을 먼저 봐서 토큰이 많이 든다.

## 만들 구조
plugins/measure/
  .claude-plugin/plugin.json
  skills/video-measure/
    SKILL.md            40줄 이하: 언제 쓰나, 3단계 흐름(사건 찾기 → 정밀 측정 → 근거 기록), 명령 표
    profiles/<game>.yaml 해상도 · fps · 1칸 px · 관심 영역 · 색 범위 · 지면선 (프로젝트 쪽에 두고 skill-profile.yaml에서 경로를 가리켜도 됨)
    scripts/vm.py       하위 명령: probe · cache · events · sheet · crops · track · clip · cite · selftest
    references/measure.md, references/report.md  (필요할 때만 읽음)
tests/에 golden 검사: 값을 아는 짧은 영상 대신 합성 영상(움직이는 사각형 · 섬광)을 테스트가 만들어 쓴다(LFS · 큰 파일 금지)

## 원칙
- 한 번만 디코딩: `vm cache`가 고정 프레임률로 바꾼 뒤 작은 흑백 사본을 numpy memmap으로 저장한다.
  통계와 검출은 이 배열을 읽고, 원본 해상도는 자를 때만 쓴다. 긴 영상은 구간별 multiprocessing.
- 숫자 먼저: `vm events`가 사건 타임라인 CSV를 만든다
  (섬광 = 밝기 급변, 멈춤 = 관심 영역 차이 ≈ 0 구간, 흔들림 = cv2.phaseCorrelate, HUD 변화, 컷 = 편집 영상일 때만 PySceneDetect).
  Claude는 요약 텍스트를 먼저 읽고, 필요한 순간의 그림만 본다.
- 시트: 칸마다 프레임 번호 · 시각, 관심 영역만, 긴 변 크기 고정, 같은 프레임 제거.
- 근거: CSV 행마다 영상 해시 · 프레임 번호 · 도구 버전. `vm cite`가 "영상 X · f123–f131 (0.267 s) ✅" 줄을 출력한다.
- 결과 캐시: (영상 해시, 명령, 인자)가 같으면 다시 계산하지 않는다.
- 브라우저 경로는 없앤다. CoTracker · SAM2는 색 · 템플릿 추적이 실패할 때만 쓰는 선택 부품으로 둔다.
- 기존 스크립트의 검증된 측정 로직(대시 통계, HUD 높이 검증, 회전 흔들림 ECC 등)은 profile 설정으로 옮겨 살린다.
- 기존 함정은 각 프로젝트 `docs/PITFALLS.md` "레퍼런스 영상 측정" 절에 있다. 먼저 읽는다.

## 완료 기준
- 기존 측정값 하나 이상(예: TotM 대시 속도 41.7칸/s)을 실제 녹화에서 `vm`이 같은 값으로 재현한다(로컬 확인, 녹화는 커밋하지 않음).
- 기존 두 스킬의 절차가 새 명령으로 모두 대체되고, 대응표를 README에 적는다.
- `python -I tests/run_tests.py`, `claude plugin validate .` 통과.
- 커밋 · 푸시는 내가 요청할 때만 한다.
````

## 알아 둘 것

- **클라우드 세션의 한계**: 이 회고 세션(claude.ai/code)에는 Unity 에디터 · 회사 PC 파일(`references/_tools`, 녹화)이 없다. 에디터 잠금 훅 · Unity 패키지 시험은 회사 PC에서 한다. 사내 GitLab에는 클라우드에서 닿는지 확인하지 못했다.
- **텔레메트리**: Claude Code OpenTelemetry는 저장소 설정으로 못 켠다. PC 환경 변수(`CLAUDE_CODE_ENABLE_TELEMETRY=1` + 수집기)로 켠다. 명령 내용 기록은 사내 정책 확인 뒤.
- **Forge 사용 조건**: 도구는 Apache 2.0이지만 만든 그림의 조건은 적혀 있지 않다. 게임에 넣기 전 한 번 확인.
- **GitLab 요금제**: LFS 파일 잠금은 Free에서 된다. merge train은 Premium.
