# Pixel Ability-fx Forge로 만들기

- 저장소: https://github.com/GameDev-Toolkit/pixel-ability-fx-generator (Apache 2.0, 빌드 없는 JS)
- 소개: https://announcerua.itch.io/pixel-ability-fx-forge

## 준비(처음 한 번)
```bash
git clone --depth 1 https://github.com/GameDev-Toolkit/pixel-ability-fx-generator <work_dir>/_forge
cd <work_dir> && npm i -D playwright && npx playwright install chromium   # 이미 있으면 건너뜀
```

## 돌리기
```bash
python -m http.server 8731 --directory <work_dir>/_forge   # 백그라운드
node .../web-vfx-search/scripts/forge_gen.js jobs.json <work_dir>/vfx/<key>/gen
python -I .../atlas_tools.py contact <work_dir>/vfx/<key>/gen_view.png <work_dir>/vfx/<key>/gen/*.png --unit <cell_px>
```
`jobs.json` 예: `[{"name":"s201","family":"aura","power":"solar","element":"holy","canvas":128,"frames":24,"seed":201}, ...]` — 시드만 바꿔 16~24개.

## 알아 둘 것(10-24 시험)
- **모양은 시드가 정한다.** `motifSelect`를 바꿔도 시드가 덮어쓴다. 원하는 모양은 시드를 많이 돌려 고른다. 같은 설정 · 시드면 같은 결과.
- **캔버스 최소 128 px.** Aura는 가장 넓을 때 83~102 px(24 px 1칸 기준 3.5~4.2칸). 줄이면 도트가 깨지므로, 작게 쓰려면 바깥 고리를 손으로 지운다.
- 시트는 1024 × 384(8 × 3칸, 24프레임). 내보내기는 시트 · PNG 낱장 · GIF.
- Aura + Radiance(holy)에서 둘레 오라로 쓸 만했던 모양: radar, clockwork, mandala(궤도형), waves. 가운데가 차서 뺀 것: spiral, eclipse. 한쪽으로 흐르는 것: fire, waterfall, comet, meteorRain, vine, smoke.
- 만든 그림의 사용 조건은 적혀 있지 않다(도구 라이선스만 있음). 카드와 README에 "확인 권장"으로 적는다.
