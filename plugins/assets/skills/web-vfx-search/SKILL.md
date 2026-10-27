---
name: web-vfx-search
description: 웹(itch.io · OpenGameArt)에서 도트 이펙트(VFX) 후보를 찾고, 맞는 게 없으면 Pixel Ability-fx Forge로 직접 만들어, 사용자가 실제 크기 · 움직임으로 보고 고르는 비교 페이지(캐릭터 1칸 표시, 밝은 배경 · 색 바꿔 보기, 라이선스 · 받는 값 표시, ☆ 고르기 · "이걸로 결정")를 만들고, 고른 것을 시트 · 낱장 · README 묶음(zip)으로 건네는 절차. "~ 이펙트 찾아줘", "~할 때 나오는 VFX 구해줘", "오라 · 폭발 · 반짝임 후보 보여줘", "무료 이펙트 어디서", "이런 느낌 이펙트 없을까", "별표 친 것 중에 결정할게", "이 이펙트 파일로 줘"처럼 이펙트 그림을 구하거나 고르려 할 때 먼저 쓴다.
---

# 웹에서 이펙트 찾기 → (없으면 만들기) → 비교 페이지 → 결정 → 묶음 전달

10-24 자석 오라(TombOfTheMask)를 찾던 방법을 정리한 것이다. Claude는 움직임의 "느낌"을 판단하지 않는다. **후보를 모으고, 받는 값 · 라이선스 · 크기를 숫자로 거르고, 실제 크기로 늘어놓는 것**까지 한다.

## 0. 프로필 읽기

프로젝트의 `.claude/skill-profile.yaml`을 먼저 읽는다(형식은 이 스킬 저장소 `templates/skill-profile.yaml`). 쓰는 값: `cell_px`(1칸 그림 px) · `character`(1칸 표시 이름) · `work_dir`(git 무시 작업 폴더) · `python` · `vfx.background`(무대 색) · `vfx.role_colors`(역할 색 문서) · `vfx.art_dir` · `vfx.ppu` · `docs.*`. 파일이 없으면 템플릿을 보여 주고 채워 달라고 한다. 아래 `<python>`은 프로필 값, `<skill_dir>`는 이 SKILL.md가 있는 폴더이고, 스크립트는 프로젝트 루트에서 돌린다(`<skill_dir>/scripts/…`).

## 1. 무엇을 찾는지 정하기

대화에서 읽고 빠진 것만 묻는다.
- **순간 · 지속**: 한 번 터짐(폭발) / 켜진 동안 반복(오라) / 따라다님(꼬리).
- **붙는 곳 · 방향**: 캐릭터 둘레(방향 없음)인지, 한쪽(방패 · 바닥 원)인지. 벽 · 천장에 붙는 캐릭터면 "옆에서 본 바닥 원"은 안 맞는다.
- **색**: 요청 색과 프로젝트 역할 색(`vfx.role_colors`)이 겹치면 페이지 `note`에 적는다(10-24: 노랑 = 수집물 색).
- **크기**: 몇 칸 안쪽인지. 도트는 줄이면 깨지므로 **원래 크기**로 판단한다.

## 2. 찾기와 값 확인

[references/sources.md](references/sources.md)의 검색어 · 사이트 순서로 훑는다. 후보마다 아래를 **받는 단계까지 들어가서** 확인한다.

1. **받는 값**: 설명의 "free"를 믿지 않는다. 내려받기 버튼을 눌렀을 때 나오는 것으로 정한다.
   - `Download Now` + "Name your own price" + 최소 0 → **0원 가능**(`licTag: zero`). 결제 창의 "No thanks, just take me to the downloads"로 받는다는 것을 `price`에 적는다.
   - `Buy Now` / 최소 금액 있음 → **유료**. 후보에 넣지 않고 `reference`(레퍼런스로만)에 둔다. 유료 에셋은 생김새를 보고 직접 그리거나 Forge 설정을 맞출 때만 참고한다.
2. **라이선스**: 상업 사용 · 수정 · 출처 표기 · 재배포를 카드에 쓴다(CC0 / 출처 표기 / 비상업은 쓰기 전 확인).
3. **규격**: 프레임 크기 · 프레임 수 · fps · 투명 배경 · 시트/낱장.
4. **미리보기**: 페이지의 GIF를 받아 `work_dir/vfx/<key>/prev/`에 둔다. 배율을 알면 `disp`(원본 1 px → 화면 3 px), 홍보 그림이면 `disp: null`.

## 3. 없으면 Forge로 만들기

맞는 무료 후보가 2개 미만이거나 사용자가 "만들어 줘"라고 하면 [references/forge.md](references/forge.md) 순서로 만든다. 요약:
- Forge(Apache 2.0)를 `work_dir/_forge/`에 받아 로컬 서버로 띄우고 `scripts/forge_gen.js`로 시드 16~24개를 한 번에 내보낸다.
- `atlas_tools.py contact`로 한눈 시트를 보고, **요청 모양(둘레형 · 가운데가 빔 등)에 맞는 것만** 남긴다. 고른 이유 · 뺀 이유를 `excluded`에 적는다.
- `atlas_tools.py gif` · `extent`로 미리보기와 크기(칸)를 카드에 넣는다. 캔버스 최소 128 px라 결과가 3.5~4칸으로 크다는 점을 `risk`에 적는다.
- 만든 그림의 사용 조건은 Forge에 적혀 있지 않다. `lic`에 "도구는 Apache 2.0, 결과물 조건은 따로 적혀 있지 않음(확인 권장)"으로 쓴다.

## 4. 비교 페이지

`work_dir/vfx/<key>_candidates.json`을 쓰고(형식은 [scripts/build_page.py](scripts/build_page.py) 맨 위) 만든다.

```bash
<python> <skill_dir>/scripts/build_page.py <work_dir>/vfx/<key>_candidates.json
```

- 순서: 직접 만든 것 · 0원 가능 중 조건에 가장 맞는 것부터 `rank`. 유료는 `reference`에만.
- 페이지 한 장에 그림이 다 들어가므로(1 MB 안팎) 파일로 바로 열거나 Artifact로 게시한다. 게시할 때는 같은 파일 경로로 다시 게시해 주소를 유지한다.
- 확인: 화면 폭 420 px에서 가로로 넘치지 않는지, 모든 그림이 뜨는지.

사용자에게: 주소, 후보 수(직접 만듦 / 0원 / 레퍼런스), 무엇을 숫자로 걸렀는지, ☆ · 결정 · "결정 · ☆ 목록 복사" 쓰는 법. Claude가 움직임을 보고 "좋다"고 말하지 않는다.

## 5. 결정 읽기

페이지는 `localStorage['<key>_stars']`, `['<key>_choice']`에 남긴다. 다른 브라우저 · 게시 페이지에서 골랐으면 "결정 · ☆ 목록 복사" 글(`[VFX 결정] …`)을 붙여 달라고 한다.

## 6. 파일로 건네기

1. **받은 에셋**이면 내려받기 허락(이름 · 출처 · 크기)을 받고 원본을 그대로 받는다.
2. **손질**: 사용자가 원하면 간단한 것만 한다 — `atlas_tools.py clear --radius N`(가운데 지우기, 10-24 일렁이는 테두리). 그림을 새로 그리는 손질은 디자이너 몫으로 남긴다.
3. **묶음**: [references/readme_template.txt](references/readme_template.txt)의 `<…>`를 채워 README(다시 만드는 설정 · 시드, 크기 칸, Unity 임포트 값 = Multiple · Grid 셀 · PPU `vfx.ppu` · Point · 압축 없음, 사용 조건)를 쓰고 `atlas_tools.py pack`으로 zip을 만들어 파일로 보낸다. 원본과 손질본을 둘 다 넣는다.

## 7. 게임에 넣기(사용자가 요청할 때)

- 그림은 `vfx.art_dir/<묶음>/`(Git LFS)에 둔다. 0원 · CC0 · 출처 표기 에셋은 `docs.credits_vfx`에 작성자 · 주소 · 라이선스 · 받은 날을 적는다.
- 위치 · 크기 · 타이밍은 코드에 숫자로 넣지 않는다. 프로젝트의 FX 배치 도구(프리팹 · 소켓 · 튜닝 SO)에 연결하고, 사람이 에디터에서 맞춘다.
- 문서: 규칙 · 값은 `docs.rules`, 결정은 `docs.decisions`, 눈으로 확인 대기는 `docs.pending`.
