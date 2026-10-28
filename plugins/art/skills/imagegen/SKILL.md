---
name: imagegen
description: 사내 이미지 생성 플랫폼(웹)에서 게임 UI 화면 · 캐릭터 · 아이콘 · 배경 시안을 뽑는 절차. 프로젝트 스타일 팩(디자이너가 승인한 참조 그림 · 스타일 문장 · 금지 문장)으로 프롬프트를 조립하고, 참조 이미지를 올리고, 비율 · 모델을 맞춰 생성한 뒤, 프롬프트 · 모델 · 참조 · 스타일 팩 버전을 기록하고, 고른 것만 프로젝트에 넣는다. "이미지 생성해줘", "imagegen으로 그려줘", "UI 시안 뽑아줘", "컨셉 이미지 만들어줘", "디자이너 스타일에 맞춰 그려줘", "이 프롬프트로 다시 뽑아줘", "지난번 시안 어떻게 뽑았지?", "스타일 팩에 이 그림 추가해줘"처럼 생성 이미지로 시안을 만들거나 고르거나 기록을 찾을 때 먼저 쓴다.
---

# 사내 이미지 생성으로 시안 뽑기 → 기록 → 고르기 → 넣기

10-28 CrazyArena에서 UI 목업 2장을 뽑은 방법을 정리한 것이다. Claude는 그림의 좋고 나쁨을 판단하지 않는다. **브리프를 정리하고, 스타일 팩으로 프롬프트를 조립하고, 사이트를 조작하고, 기록을 남기고, 나란히 보여 주는 것**까지 한다.

## 0. 프로필 · 스타일 팩 읽기

프로젝트의 `.claude/skill-profile.yaml`을 먼저 읽는다(형식은 이 스킬 저장소 `templates/skill-profile.yaml`의 `imagegen:` 절).
- 쓰는 값: `imagegen.site`(워크스페이스 주소) · `imagegen.model`(기본 모델) · `imagegen.style_pack` · `imagegen.out_dir`(고른 시안) · `imagegen.draft_dir`(게임 임시 그림) · `imagegen.original_refs`(원작 그림 참조 규칙) · `imagegen.approvers` · `work_dir` · `python`
- 값이 비면 템플릿을 보여 주고 채워 달라고 한다. 사이트 주소는 이 저장소에 적지 않는다(사내 주소).
- 스타일 팩 형식은 [references/style_pack.md](references/style_pack.md)다. 없으면 그 문서의 v0 예를 보여 주고 같이 만든다.
- 아래 `<python>`은 프로필 값, `<skill_dir>`는 이 SKILL.md가 있는 폴더다. 스크립트는 프로젝트 루트에서 돌린다.

## 1. 브리프

대화에서 읽고 빠진 것만 묻는다.
- **대상 종류**: 스타일 팩 `targets`의 키(예: `ui_screen` · `icon` · `character`). 없는 종류면 대상 문장을 새로 쓰고, 쓸 만하면 팩에 더하자고 제안한다.
- **용도**: `draft`(기획서 · 컨셉 시안) / `game`(게임에 들어갈 임시 그림). 원작 그림 참조 허용 여부가 여기서 갈린다.
- **내용**: 화면 요소 · 라벨 글자 · 배치. 기획 문서(프로필 `docs.rules` 등)에서 근거를 찾고, 없으면 묻는다. 수치 · 기능을 추측해 그림에 넣지 않는다.
- **비율 · 장수 · 모델**: 기본은 프로필 `imagegen.model`, 1장. 사이트 사용량 한도를 모르면 한 번에 3장을 넘기지 않는다.

## 2. 참조 고르기

- 스타일 팩 `refs`에서 `approved: true`이고 `tags`가 대상과 맞는 것을 2~4장 추천한다. 사용자가 고른다.
- **원작 그림**(`original: true`)은 프로필 `imagegen.original_refs`를 따른다.
  - `never`: 쓰지 않는다.
  - `draft_only`: 용도가 `draft`일 때만 쓴다. `game` 용도에는 쓰지 않는다.
  - `allow`: 제한 없음.
- 참조 파일은 **세션이 읽을 수 있는 폴더**(프로젝트 안)에 있어야 올릴 수 있다. 임시 폴더 파일은 `work_dir` 아래로 복사한다. webp 등 사이트가 받지 않는 형식은 ffmpeg로 png로 바꾼다.

## 3. 프롬프트 조립

`스타일 문장(style_block) + 대상 문장(targets[종류]) + 브리프 내용 + 금지 문장(negative)` 순서로 잇는다.
- 그림 모델은 영어 지시를 잘 따른다. 화면에 들어갈 글자(한글 라벨)만 따옴표로 넣는다.
- "Clean layout, no overlapping elements, readable labels" 같은 정리 문장을 끝에 둔다(10-28: 겹침이 줄었다).
- 조립한 프롬프트를 `<work_dir>/imagegen/<key>/prompt.txt`에 저장한다. `<key>`는 `ui_radar`처럼 짧은 영어 이름이다.

## 4. 확인받기

보내기 전에 한 번에 보여 주고 승인을 받는다. 생성은 사내 서비스로 보내는 일이다.
- 프롬프트 전문, 모델, 비율, 장수, 참조 파일 목록(원작 그림이면 표시), 용도

## 5. 사이트 조작

**Claude in Chrome**(사용자의 Chrome)으로 한다. 앱 안 브라우저는 참조 이미지를 올릴 수 없다. 화면 순서와 함정은 [references/site.md](references/site.md)를 따른다.
- 요약: 워크스페이스 열기 → 참조 `file_upload` → 생성 설정에서 비율 · 장수 → 빈 곳을 눌러 닫기 → 설정 글자 확인 → 프롬프트 입력 → 생성 → 결과 열어 보기.
- 로그인 · 계정 권한 승인은 사용자가 한다.

## 6. 기록

생성을 보낼 때마다 기록한다.

```bash
<python> <skill_dir>/scripts/imagegen_log.py record --key ui_radar --purpose draft --model "GEM 3.1" --ratio 9:16 --count 1 --prompt-file <work_dir>/imagegen/ui_radar/prompt.txt --ref <참조1> [--ref ...] [--original-ref <원작 참조>] [--library <사이트 라이브러리 이름>] [--note "..."]
```
- `<work_dir>/imagegen/<key>/<번호>.json`과 `<work_dir>/imagegen/log.jsonl`에 남는다. 스타일 팩 버전도 같이 적힌다.
- `--original-ref`가 프로필 `original_refs` 규칙에 걸리면 기록하지 않고 멈춘다. 그때는 생성도 보내지 않는다.
- 지난 기록 보기: `imagegen_log.py list [--key ui_radar]`

## 7. 보여 주고 고르기

- 결과를 사이트에서 열어 사용자에게 보여 준다. 브리프와 다른 점(칸 수 · 빠진 요소 · 글자 오류)만 숫자 · 사실로 적는다. 좋고 나쁨은 사용자가 정한다.
- 다시 뽑으면 같은 `<key>`로 기록해 나란히 비교할 수 있게 한다.

## 8. 넣기

고른 것만 내려받아 넣는다. 내려받기는 사용자 확인 뒤에 한다.

```bash
<python> <skill_dir>/scripts/imagegen_log.py pick --key ui_radar --id 1 --file <내려받은 파일>
```
- 용도 `draft`면 `imagegen.out_dir`, `game`이면 `imagegen.draft_dir`로 복사하고 기록에 `picked`를 남긴다. 파일 이름은 `<key>_<번호>.<확장자>`다.
- 넣은 파일은 프로젝트 git(LFS)으로 커밋할 수 있다. 커밋은 사용자가 요청할 때만 한다. 고르지 않은 결과는 사이트와 `work_dir`에만 둔다.

## 9. 스타일 팩 갱신

디자이너 그림이 들어오면 [references/style_pack.md](references/style_pack.md) "갱신"을 따른다. `approved`는 프로필 `imagegen.approvers`에 있는 사람이 켠다. Claude는 후보로만 더한다(`approved: false`).
