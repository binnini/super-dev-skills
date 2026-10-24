# 어디서 · 어떻게 찾나

## 사이트 순서
1. **itch.io** `https://itch.io/game-assets/free/tag-pixel-art/tag-effects` 와 검색 `https://itch.io/search?q=<검색어>&type=game-assets`
   - "free" 목록에도 유료가 섞인다. 상세 페이지의 버튼이 `Download Now`인지 `Buy Now`인지, 가격 칸이 "Name your own price"인지 본다.
   - 확실히 하려면 `Download Now`를 눌러 결제 창이 뜨는지, 그 아래 "No thanks, just take me to the downloads"가 있는지 본다(10-24: XYEzawr Fire aura · nerijs PVFX가 이 경우. 처음엔 유료로 보였음).
   - 상세 페이지 HTML의 `"min_price":0` 같은 값으로도 거를 수 있다.
2. **OpenGameArt** `https://opengameart.org/art-search-advanced?keys=<검색어>&field_art_type_tid[]=9` (2D Art). 라이선스 칸이 CC0 · CC-BY · GPL 중 무엇인지 본다.
3. (선택) **Kenney** `https://kenney.nl/assets?q=particle` — CC0, 도트보다 매끈한 그림이 많음.

## 검색어(영어, 6~10개)
- 종류: `aura`, `buff`, `shield`, `ring`, `orbit`, `magnetic`, `glow`, `sparkle`, `burst`, `explosion`, `hit`, `trail`
- 화풍: `pixel art`, `pixel vfx`, `16x16`, `32x32`, `spritesheet`
- 색 · 재질: `gold`, `yellow`, `electric`, `holy`

## 거르는 기준(숫자로)
| 기준 | 빼는 경우 |
|---|---|
| 받는 값 | 최소 금액이 있음 → `reference`로 |
| 방향 | 요청이 둘레형인데 옆에서 본 바닥 원 · 한쪽 호 |
| 가운데 | 캐릭터를 가리는 꽉 찬 가운데(지울 수 없는 경우) |
| 크기 | 원래 크기로 요청 칸 수의 2배를 넘음 |
| 라이선스 | 비상업만 · 조건 불명(표시만 하고 사용자에게 물음) |
