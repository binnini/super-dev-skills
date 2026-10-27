"""여러 순간의 후보 페이지를 묶는 목차 페이지(웹 소리 찾기 스킬).

실행(프로젝트 루트에서): <python> <skill_dir>/scripts/build_index.py <out.html> <제목> <a_candidates.json> <b_candidates.json> ...
  각 후보 파일의 key · title · purpose · current(지금 게임 소리, 선택) · 후보 수를 카드로 늘어놓고,
  같은 브라우저의 localStorage(<key>_stars · <key>_choice)를 읽어 ☆ 수 · 결정을 보여 준다(페이지는 같은 서버 · 같은 폴더에 둔다).
"""
import html
import json
import os
import sys

PAGE = """<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root { --bg: #f6f5f2; --card: #fff; --ink: #1d1d1b; --sub: #6b6a66; --line: #e2e0da; --accent: #d9a400; --ok-bg: #dcefe0; --ok-ink: #1f6b35; --chip: #efede7; }
@media (prefers-color-scheme: dark) { :root { --bg: #141417; --card: #1e1e23; --ink: #ecebe6; --sub: #9a988f; --line: #2e2e35; --accent: #ffd23f; --ok-bg: #1d3a26; --ok-ink: #8fdca4; --chip: #2a2a30; } }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink); font: 14px/1.5 "Pretendard", "Apple SD Gothic Neo", "Malgun Gothic", system-ui, sans-serif; }
main { max-width: 1100px; margin: 0 auto; padding: 16px; }
h1 { font-size: 18px; margin: 0 0 4px; }
.lead { color: var(--sub); font-size: 13px; margin: 0 0 14px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 12px; }
a.card { display: flex; flex-direction: column; gap: 6px; background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 12px 14px; color: inherit; text-decoration: none; }
a.card:hover { border-color: var(--accent); }
a.card.done { border-color: var(--ok-ink); }
.t { font-weight: 600; font-size: 15px; }
.p { color: var(--sub); font-size: 12px; }
.row { display: flex; gap: 6px; flex-wrap: wrap; }
.chip { font-size: 12px; border-radius: 6px; padding: 1px 8px; background: var(--chip); color: var(--sub); }
.chip.ok { background: var(--ok-bg); color: var(--ok-ink); }
.chip b { color: var(--ink); }
</style></head><body><main>
<h1>__TITLE__</h1>
<p class="lead">순간마다 후보 페이지를 열어 듣고 ☆ · "이걸로 결정"을 누르면 여기에 모인다(이 브라우저에 저장). 결정이 다 모이면 <b>결정 목록 복사</b>를 눌러 Claude에게 붙여 넣는다(다른 브라우저에서 골랐어도 그대로 전달된다).</p>
<p><button id="copy" style="font:inherit;font-size:13px;padding:6px 14px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer">결정 목록 복사</button> <span id="copied" class="p"></span></p>
<div class="grid" id="grid"></div>
</main><script>
const ITEMS = /*ITEMS*/null;
const get = k => { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } };
const g = document.getElementById('grid');
for (const it of ITEMS) {
  const stars = (get(it.key + '_stars') || []).length, ch = get(it.key + '_choice');
  const a = document.createElement('a');
  a.href = it.page; a.className = 'card' + (ch ? ' done' : '');
  a.innerHTML = `<div class="t">${it.title}</div><div class="p">${it.purpose}</div>` +
    `<div class="row"><span class="chip">후보 <b>${it.count}</b></span><span class="chip">☆ <b>${stars}</b></span>` +
    (ch ? `<span class="chip ok">결정: <b>${ch.title}</b></span>` : '<span class="chip">결정 전</span>') + `</div>` +
    (it.current ? `<div class="p">지금 게임: ${it.current}</div>` : '');
  g.appendChild(a);
}
addEventListener('pageshow', e => { if (e.persisted) location.reload(); }); // 뒤로 가기로 돌아오면 ☆ · 결정 새로
// 결정 목록 복사: 순간마다 결정(사이트 · id · 제목 · 반복 겹 설정)과 ☆ 목록을 글로. Claude가 붙여 넣은 글에서 그대로 읽는다
document.getElementById('copy').onclick = async () => {
  const lines = ITEMS.map(it => {
    const ch = get(it.key + '_choice'), st = get(it.key + '_stars') || [];
    const mode = ch && ch.mode ? ' ' + JSON.stringify(ch.mode) : '';
    return `${it.key}: ${ch ? `${ch.src} ${ch.id} "${ch.title}"${mode}` : '결정 없음'} | ☆ ${st.join(', ') || '-'}`;
  });
  const text = '[소리 결정] ' + document.title + '\\n' + lines.join('\\n');
  try { await navigator.clipboard.writeText(text); document.getElementById('copied').textContent = '복사했다. Claude에게 붙여 넣는다.'; }
  catch (e) { prompt('이 글을 복사해 Claude에게 붙여 넣는다', text); }
};
</script></body></html>
"""


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except AttributeError:
            pass
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    out, title, files = sys.argv[1], sys.argv[2], sys.argv[3:]
    items = []
    for f in files:
        c = json.load(open(f, encoding="utf-8"))
        purpose = c.get("summary") or c["purpose"]
        items.append({"key": c["key"], "title": c["title"], "purpose": purpose, "current": c.get("current", ""),
                      "count": len(c["candidates"]), "page": f'{c["key"]}_candidates.html'})
    page = PAGE.replace("__TITLE__", html.escape(title)).replace("/*ITEMS*/null", json.dumps(items, ensure_ascii=False))
    open(out, "w", encoding="utf-8").write(page)
    print(f"{out}: 순간 {len(items)}개")


if __name__ == "__main__":
    main()
