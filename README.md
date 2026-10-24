# super-dev-skills

게임 프로젝트마다 복사해 쓰던 Claude Code 스킬 · 훅을 한곳에 모은 저장소다. 저장소 자체가 **Claude Code 플러그인 마켓플레이스**(이름 `super-dev-skills`)라서, 각 프로젝트는 설정 한 줄로 받아 쓰고 여기서 고친 것을 업데이트로 받는다.

BigHunter(9/29~10/13) · TombOfTheMask(10/14~10/27) 회고에서 정한 다음 과제용 도구 계획도 여기 있다.

| 문서 | 내용 |
|---|---|
| [docs/HANDOFF.md](docs/HANDOFF.md) | **다른 환경에서 이어서 할 때 먼저 읽는 것.** 정한 것 · 다음 할 일 · 시작 프롬프트 |
| [docs/TOOLKIT.md](docs/TOOLKIT.md) | 작업 도구함: 다음 과제에 들고 갈 패키지 · 스킬 · 환경 · 테스트 · 협업 방식 |
| [CLAUDE.md](CLAUDE.md) | 이 저장소에서 스킬을 고칠 때의 규칙(Claude가 자동으로 읽음) |
| [CHANGELOG.md](CHANGELOG.md) | 바뀐 것 |

## 시작하기

### A. 새 PC에서 처음 한 번

1. **필요한 것**: Git, Claude Code(`claude --version`), Python 3.12(+ Pillow), Node 22. VFX 스킬의 Forge 생성까지 쓰려면 작업 폴더에서 `npm i -D playwright && npx playwright install chromium`.
2. **이 저장소 접근**(비공개): Claude Code는 이 PC의 git 로그인을 그대로 쓰고 묻지 않는다. 아래 둘 중 하나로 `git clone https://github.com/binnini/super-dev-skills`가 비밀번호 없이 되게 해 둔다.
   - `gh auth login` → `gh auth setup-git` (SSH 키가 없으면 환경 변수 `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1`도)
   - 또는 GitHub SSH 키를 ssh-agent에 올려 둠
3. 자동 업데이트를 켜려면 Claude Code 안에서 `/plugin` → Marketplaces → `super-dev-skills` → **Enable auto-update**. 끄고 쓰면 `claude plugin marketplace update super-dev-skills`로 받는다.

### B. 게임 프로젝트에 스킬 넣기

프로젝트 루트에서:

```bash
claude plugin marketplace add binnini/super-dev-skills --scope project
claude plugin install assets@super-dev-skills --scope project
```

- 두 명령이 프로젝트 `.claude/settings.json`에 `templates/project-settings.json`과 같은 내용을 쓴다. 이 파일을 커밋하면 다른 PC · 팀원도 폴더를 신뢰할 때 같은 스킬을 받는다.
- `templates/skill-profile.yaml`을 프로젝트의 `.claude/skill-profile.yaml`로 복사해 채운다(작업 폴더, 1칸 px, 소리 슬롯 파일, 문서 위치 등). 스킬은 경로를 여기서 읽는다.
- 예전에 복사해 둔 `.claude/skills/web-sound-search/`가 있으면 지운다(같은 스킬이 두 번 뜨지 않게).
- 확인: `claude plugin details assets` → `Skills (2) web-sound-search, web-vfx-search`.
- 쓰기: 대화에서 "착지할 때 나는 소리 찾아줘", "자석 먹으면 둘레에 노란 오라 이펙트 찾아줘"라고 하거나 `/assets:web-vfx-search`.

### C. 클라우드 세션(claude.ai/code)에서

세션을 만들 때 이 저장소(`binnini/super-dev-skills`)를 같이 연결한다. 이미 시작한 세션이면 "binnini/super-dev-skills 저장소 연결해 줘"라고 한다. 게임 저장소의 `.claude/settings.json`에 B의 설정이 커밋되어 있으면 세션이 스킬을 받는다.

### D. 회고에서 이어서 일하기

새 Claude 세션에서 이 저장소를 열고 이렇게 시작한다.

> super-dev-skills의 docs/HANDOFF.md를 읽고 "다음 할 일"의 ○○부터 이어서 하자.

영상 측정 스킬(video-measure)은 `references/_tools`와 녹화가 있는 기기에서 시작한다. 시작 프롬프트는 HANDOFF.md "video-measure 시작 프롬프트"에 있다.

## 구조

```
super-dev-skills/
├─ .claude-plugin/marketplace.json   마켓플레이스 목록(이름 super-dev-skills, 플러그인 항목)
├─ plugins/
│  └─ assets/                        플러그인 = 묶어서 켜고 끄는 단위
│     ├─ .claude-plugin/plugin.json  이름 · 버전
│     └─ skills/
│        ├─ web-sound-search/        효과음 · 배경음 찾기 (TotM 10-23에서 옮김)
│        └─ web-vfx-search/          도트 이펙트 찾기 · Forge로 만들기 (10-24)
│           ├─ SKILL.md              절차(Claude가 읽음)
│           ├─ scripts/              build_page.py · atlas_tools.py · forge_gen.js
│           ├─ assets/               page_template.html
│           └─ references/           sources.md · forge.md · readme_template.txt
├─ templates/
│  ├─ skill-profile.yaml             각 프로젝트 .claude/skill-profile.yaml 의 틀
│  └─ project-settings.json          각 프로젝트 .claude/settings.json 에 들어갈 부분
├─ docs/                             HANDOFF.md · TOOLKIT.md
├─ tests/run_tests.py                구조 · 문법 · 스크립트 동작 검사
├─ .github/workflows/check.yml       위 검사를 푸시마다(GitLab으로 옮기면 .gitlab-ci.yml)
├─ CLAUDE.md
└─ CHANGELOG.md                      플러그인 버전마다 한 줄 이상
```

### 플러그인 나누기

| 플러그인 | 스킬 · 훅 | 상태 |
|---|---|---|
| `assets` | `web-sound-search`, `web-vfx-search` | 있음(0.1.0) |
| `measure` | `video-measure`(영상 프레임 측정. reference-frame-sheet · reference-anim-sheet를 합침) | 다른 기기에서 만들 예정 |
| `ops` | `bottleneck-report`(세션 시간 · 에디터 대기 집계) | 예정 |
| `editor-lease` | PreToolUse 훅(Unity 에디터 잠금) | 예정. 훅은 켜면 바로 동작하므로 따로 켜고 끄게 별도 플러그인 |

나누는 기준은 **같이 켜고 끄는 것끼리**다. 스킬 이름은 `<플러그인>:<스킬>`로 불린다(예: `/assets:web-vfx-search`).

### 프로젝트 경로는 프로필에

스킬 본문에는 `Assets/_Project/...` 같은 프로젝트 경로를 적지 않는다. 각 프로젝트의 `.claude/skill-profile.yaml`에 적고 스킬이 처음에 읽는다. 그래서 같은 스킬이 TombOfTheMask, BigHunter, 다음 과제에서 그대로 돈다. `tests/run_tests.py`가 본문에 프로젝트 경로가 들어가면 실패시킨다.

스크립트는 **프로젝트 루트에서** 실행한다. 플러그인은 설치하면 `~/.claude/plugins/cache/` 아래로 복사되므로 스크립트 위치로 프로젝트를 찾지 않는다.

## 고치기와 내보내기

1. 이 저장소를 받아 스킬을 고친다. 고치면서 바로 써 보려면 시험 프로젝트에서 `claude plugin marketplace add <이 폴더 경로>`로 추가한다. 그러면 파일을 직접 읽어 `/reload-plugins`만으로 반영된다.
2. `python -I tests/run_tests.py`와 `claude plugin validate .`이 통과해야 한다.
3. 고친 플러그인의 `plugin.json` `version`을 올리고(`0.1.0` → `0.1.1`, 절차가 바뀌면 `0.2.0`) `CHANGELOG.md`에 `## <플러그인> <버전> · 날짜` 줄을 쓴다. **버전을 안 올리면 사용자에게 가지 않는다.**
4. 커밋 · 푸시하면 GitHub Actions `check`가 같은 검사를 돌린다.

## 규칙

- Git LFS를 쓰지 않는다. 플러그인을 받을 때 LFS 파일은 포인터만 온다. 큰 그림 · 영상 예시는 넣지 않는다(테스트는 가짜 그림을 만들어 쓴다).
- 실행 파일 폴더 이름을 `bin/`으로 하지 않는다(조직 동기화가 거부함). `scripts/`에 둔다.
- 스킬 설명(`description`)은 1024자 이하로, 언제 쓰는지(사용자가 하는 말)를 넣는다.
- 원작 에셋 · 유료 에셋 · 사내 비밀(토큰, 사내 주소의 자격 증명)은 넣지 않는다.
