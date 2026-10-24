# pudin-skills

게임 프로젝트마다 복사해 쓰던 Claude Code 스킬 · 훅을 한곳에 모은 저장소다. 저장소 자체가 **Claude Code 플러그인 마켓플레이스**라서, 각 프로젝트는 설정 한 줄로 받아 쓰고 여기서 고친 것을 업데이트로 받는다.

## 구조

```
pudin-skills/
├─ .claude-plugin/marketplace.json   마켓플레이스 목록(이름 pudin-skills, 플러그인 항목)
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
│  └─ project-settings.json          각 프로젝트 .claude/settings.json 에 넣을 부분
├─ tests/run_tests.py                구조 · 문법 · 스크립트 동작 검사
├─ .gitlab-ci.yml / .github/workflows/check.yml   위 검사를 푸시마다
└─ CHANGELOG.md                      플러그인 버전마다 한 줄 이상
```

### 플러그인 나누기

| 플러그인 | 스킬 · 훅 | 상태 |
|---|---|---|
| `assets` | `web-sound-search`, `web-vfx-search` | 있음 |
| `measure` | `video-measure`(영상 프레임 측정. reference-frame-sheet · reference-anim-sheet를 합침) | 다른 기기에서 만들 예정 |
| `ops` | `bottleneck-report`(세션 시간 · 에디터 대기 집계) | 예정 |
| `editor-lease` | PreToolUse 훅(Unity 에디터 잠금) | 예정. 훅은 켜면 바로 동작하므로 따로 켜고 끄게 별도 플러그인 |

나누는 기준: **같이 켜고 끄는 것끼리**. 스킬 이름은 `<플러그인>:<스킬>`로 불린다(예: `/assets:web-vfx-search`).

### 프로젝트 경로는 프로필에

스킬 본문에는 `Assets/_Project/...` 같은 프로젝트 경로를 적지 않는다. 각 프로젝트의 `.claude/skill-profile.yaml`(틀: `templates/skill-profile.yaml`)에 작업 폴더 · 1칸 px · 소리 슬롯 파일 · 문서 위치를 적고, 스킬이 처음에 그것을 읽는다. 그래서 같은 스킬이 TombOfTheMask, BigHunter, 다음 과제에서 그대로 돈다. `tests/run_tests.py`가 본문에 프로젝트 경로가 들어가면 실패시킨다.

스크립트는 **프로젝트 루트에서** 실행한다(플러그인은 설치하면 `~/.claude/plugins/cache/` 아래로 복사되므로 스크립트 위치로 프로젝트를 찾지 않는다).

## 프로젝트에서 쓰기

1. 프로젝트 `.claude/settings.json`에 `templates/project-settings.json` 내용을 합친다(주소만 바꿈). 커밋하면 팀원도 폴더를 신뢰할 때 자동으로 받는다.
   - 또는 프로젝트 루트에서 `claude plugin marketplace add https://<호스트>/<그룹>/pudin-skills.git --scope project` 후 `claude plugin install assets@pudin-skills --scope project`.
2. `templates/skill-profile.yaml`을 `.claude/skill-profile.yaml`로 복사해 채운다.
3. 예전에 복사해 둔 `.claude/skills/web-sound-search/`는 지운다(같은 스킬이 두 번 뜨지 않게).

**비공개 저장소 접근**: Claude Code는 이 PC의 git 자격 증명을 그대로 쓰고 묻지 않는다. HTTPS면 Git Credential Manager에 한 번 로그인해 두고(`git clone`이 비밀번호 없이 되면 됨), SSH면 키를 ssh-agent에 올려 둔다. GitLab 주소는 `owner/repo` 줄임이 안 되고 전체 `https://….git`을 쓴다. 클라우드 세션(claude.ai/code)은 사내 GitLab에 닿지 않을 수 있으니, 그때는 GitHub 비공개 저장소가 낫다.

## 고치기와 내보내기

1. 이 저장소를 받아 스킬을 고친다. 고치면서 바로 써 보려면 테스트 프로젝트에서 `claude plugin marketplace add <이 폴더 경로>`로 추가하면 파일을 직접 읽어 `/reload-plugins`만으로 반영된다.
2. `python -I tests/run_tests.py`와 `claude plugin validate .`이 통과해야 한다.
3. 고친 플러그인의 `plugin.json` `version`을 올리고(`0.1.0` → `0.1.1`, 절차가 바뀌면 `0.2.0`) `CHANGELOG.md`에 `## <플러그인> <버전> · 날짜` 줄을 쓴다. **버전을 안 올리면 사용자에게 가지 않는다.**
4. 커밋 · 푸시. 각 PC에서는 `/plugin` → Marketplaces → pudin-skills → **Enable auto-update**를 한 번 켜 두거나, `claude plugin marketplace update pudin-skills`로 받는다.

## 규칙

- Git LFS를 쓰지 않는다. 플러그인을 받을 때 LFS 파일은 포인터만 온다. 큰 그림 · 영상 예시는 넣지 않는다(테스트는 가짜 그림을 만들어 쓴다).
- 실행 파일 폴더 이름을 `bin/`으로 하지 않는다(조직 동기화가 거부함). `scripts/`에 둔다.
- 스킬 설명(`description`)은 1024자 이하, 언제 쓰는지(사용자가 하는 말)를 넣는다.
- 원작 에셋 · 유료 에셋 · 사내 비밀은 넣지 않는다.
