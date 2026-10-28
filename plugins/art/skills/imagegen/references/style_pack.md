# 스타일 팩 형식

프로젝트마다 하나 둔다(경로 = 프로필 `imagegen.style_pack`, 프로젝트 git에 커밋). 프롬프트의 스타일 문장 · 금지 문장 · 참조 후보 · 대상 문장을 한곳에 모아, 누가 뽑아도 같은 톤이 나오게 한다. PyYAML 없이 읽도록 JSON이다.

## 형식
```json
{
  "version": 0,
  "updated": "2026-10-28",
  "source": "어떤 스타일인가 한 줄(예: 원작 IP 스타일, 디자이너 OO)",
  "style_block": "모든 프롬프트 앞에 붙는 영어 문장",
  "negative": "끝에 붙는 금지 문장",
  "palette": {"background": ["#1b1f4a"], "ui_frame": ["#2f6bff"]},
  "refs": [
    {"path": "프로젝트 기준 경로", "tags": ["ui_screen", "radar"], "approved": true,
     "by": "승인한 사람", "original": false, "note": "왜 기준인가"}
  ],
  "targets": {
    "ui_screen": "Mobile game UI mockup, portrait {ratio}, ...",
    "icon": "single game item icon, centered, plain background, ...",
    "character": "full body character, front view, ..."
  }
}
```
- `version`: 기준 그림 · 문장이 바뀔 때마다 1씩 올린다. 기록(`imagegen_log.py record`)에 남아 "어느 기준으로 뽑았나"를 알 수 있다.
- `palette`: 대표 그림에서 잰 색만 적는다. 선 굵기 · 질감 같은 느낌 문장은 Claude가 추측해 쓰지 않는다. 디자이너 · 사용자가 `style_block`에 쓴다.
- `refs[].approved`: 프로필 `imagegen.approvers`에 있는 사람만 켠다. Claude는 `false`로 후보만 더한다.
- `refs[].original`: 원작 그림이면 `true`. 프로필 `imagegen.original_refs` 규칙을 따른다(SKILL.md 2단계).
- `targets`: `{ratio}`는 브리프의 비율로 바꾼다.

## 갱신
1. 디자이너 그림이 프로젝트에 들어오면(아트 폴더) 대표가 될 만한 것을 사용자에게 묻는다.
2. `refs`에 `approved: false`로 더하고 `tags`를 붙인다.
3. 승인자가 `approved: true`로 바꾸면 `version`을 올리고 `updated`를 고친다.
4. 팀이 만든 임시 목업은 디자이너 그림이 생기면 `approved: false`로 내린다(줄은 지우지 않는다).

## v0 예(10-28 CrazyArena)
팀 목업 2장을 기준으로 시작했다. `style_block`은 그날 쓴 프롬프트 앞부분이다. 디자이너 그림이 들어오면 위 "갱신"으로 바꾼다.
