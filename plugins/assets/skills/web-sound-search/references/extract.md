# 사이트별 후보 뽑기 (브라우저 javascript_tool)

내장 브라우저(`mcp__Claude_Browser__*`)로 사이트를 한 번 연 뒤, 그 탭에서 아래 코드를 `javascript_tool`로 돌린다. 같은 사이트 안의 `fetch`라 검색 페이지를 여러 개 빠르게 훑는다. 결과는 탭을 옮기면 사라지니 `JSON.stringify(...)`로 바로 꺼내 후보 파일에 옮긴다(10-23 확인: 두 사이트 모두 봇 확인 없이 열렸다). 봇 확인(CAPTCHA)이 뜨면 풀지 말고 사용자에게 알린다.

## Freesound (freesound.org)

- 검색 결과 카드 `.bw-player[data-mp3]`에 미리듣기 mp3 · 길이 · 스펙트로그램 · 내려받기 수가 다 있다. 라이선스는 카드 위쪽 요소의 `title="License: ..."`.
- 검색 주소의 길이 필터(`f=duration:[0 TO 1.5]`)는 결과가 0개로 나왔다 → 필터 없이 받고 아래에서 길이로 거른다.
- 한 검색어에 첫 페이지(약 15개)만 본다. 여러 검색어로 넓힌다.

```js
const queries = ['suction cup', 'suction pop', 'plunger pop'];   // 바꿀 것
const seen = new Map();
for (const q of queries) {
  const html = await (await fetch('/search/?q=' + encodeURIComponent(q))).text();
  const doc = new DOMParser().parseFromString(html, 'text/html');
  doc.querySelectorAll('.bw-player[data-mp3]').forEach(p => {
    const id = p.dataset.soundId;
    if (seen.has(id)) { seen.get(id).q.push(q); return; }
    let c = p, lic = '';
    for (let i = 0; i < 8 && c; i++) { const l = c.querySelector && c.querySelector('[title^="License"]'); if (l) { lic = l.title.replace('License: ', ''); break; } c = c.parentElement; }
    seen.set(id, { src: 'freesound', id, title: p.dataset.title, user: p.dataset.username, dur: +(+p.dataset.duration).toFixed(2),
      lic, url: `https://freesound.org/people/${p.dataset.username}/sounds/${id}/`, mp3: p.dataset.mp3,
      downloads: +p.dataset.numDownloads, q: [q] });
  });
}
window.__fs = [...seen.values()];
window.__fs.map(s => `${s.id}|${s.dur}s|${s.lic}|dl${s.downloads}|${s.title}|${s.q}`).join('\n');   // 훑어보고 고르기
```

고른 id만 꺼내기: `JSON.stringify(window.__fs.filter(s => keep.includes(+s.id)).map(({q, ...s}) => s))`

## Pixabay (pixabay.com/sound-effects)

- 검색 페이지에는 mp3 주소가 없다(누르면 받아 온다). 카드 링크(`/sound-effects/<이름>-<번호>/`)와 목록의 길이(`[class*=duration]`, 초 단위 반올림)를 먼저 모으고, 고른 것만 항목 페이지를 받아 `cdn.pixabay.com/download/audio/...mp3`를 찾는다.
- 항목 페이지의 길이 표시는 다른 소리 것이라 쓰지 않는다 → 마지막에 진짜 길이를 잰다(아래).
- 올린 사람이 `freesound_community`면 Freesound 소리를 옮겨 온 것이다(원래 라이선스를 확인하는 게 안전).
- 라이선스는 모두 Pixabay Content License(출처 표기 없이 사용 가능).
- **항목 페이지를 한꺼번에 받지 않는다**(10-24): 순간 6개 × 10개를 `Promise.all`로 동시에 받으면 100개쯤에서 429("Just a moment…")가 돌아와 mp3가 0개가 된다. 한 개씩 0.4 s 간격으로 받고, 한 번에 30 s 안쪽까지만 받은 뒤 `localStorage`에 모아 다음 호출에서 이어 받는다. 429가 나면 사이트 첫 페이지를 다시 연 뒤 이어 받으면 됐다. 미리듣기 mp3(cdn)의 길이 재기는 제한에 걸리지 않았다.

```js
const queries = ['suction', 'plunger', 'wet pop'];   // 바꿀 것
const items = new Map();
const toSec = t => { const [m, s] = t.split(':').map(Number); return m * 60 + s; };
for (const q of queries) {
  const h = await (await fetch('/sound-effects/search/' + encodeURIComponent(q) + '/')).text();
  const doc = new DOMParser().parseFromString(h, 'text/html');
  doc.querySelectorAll('a[href*="/sound-effects/"]').forEach(a => {
    const href = a.getAttribute('href');
    if (!/^\/sound-effects\/[a-z0-9-]+-\d+\/$/.test(href)) return;
    let c = a, dur = null;
    for (let i = 0; i < 6 && c && dur == null; i++) { const d = c.querySelector && c.querySelector('[class*="duration"]'); if (d) dur = toSec(d.textContent.trim()); c = c.parentElement; }
    if (!items.has(href)) items.set(href, { href, dur, q: [q], title: a.textContent.trim() });
    else if (!items.get(href).q.includes(q)) items.get(href).q.push(q);
  });
}
window.__px = [...items.values()];
window.__px.filter(i => i.dur == null || i.dur <= 5).map((i, k) => `${k}|${i.dur}s|${i.title}|${i.q}|${i.href}`).join('\n');
```

고른 것의 mp3 · 올린 사람:

```js
const pick = ['film-special-effects-suction-cup-80187'];   // href의 가운데 부분
const out = [];
for (const p of pick) {
  const h = await (await fetch('/sound-effects/' + p + '/')).text();
  const mp3 = (h.match(/https:\/\/cdn\.pixabay\.com\/download\/audio\/[^"' ]+?\.mp3/) || [null])[0];
  const title = (new DOMParser().parseFromString(h, 'text/html').querySelector('h1') || {}).textContent || p;
  const user = (h.match(/"author"\s*:\s*\{[^}]*"name"\s*:\s*"([^"]+)"/) || [])[1];
  out.push({ src: 'pixabay', id: p.match(/(\d+)$/)[1], title: title.trim().replace(/ sound effect.*$/i, '').replace(/\. Free.*$/, ''),
    user, dur: null, lic: 'Pixabay Content License', url: 'https://pixabay.com/sound-effects/' + p + '/', mp3 });
}
JSON.stringify(out);
```

## 진짜 길이 재기 (어느 사이트든)

비교 페이지를 연 탭에서(후보가 `DATA`에 들어 있음) mp3 메타데이터로 잰다. 결과를 후보 파일의 `dur`에 넣고 페이지를 다시 만든다.

```js
const out = {};
for (const d of DATA) out[d.src + ':' + d.id] = await new Promise(r => { const a = new Audio(d.mp3); a.onloadedmetadata = () => r(+a.duration.toFixed(2)); a.onerror = () => r(null); });
JSON.stringify(out);
```
