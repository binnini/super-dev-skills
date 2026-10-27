"""Freesound를 셸에서 훑기(여러 순간 · 여러 검색어). 브라우저 없이 된다(10-23 확인, Pixabay는 403이라 브라우저로).

실행(프로젝트 루트에서): <python> <skill_dir>/scripts/freesound_search.py <plan.json> <out.json> [순간마다 최대 개수=14]
  plan.json = {"<key>": {"queries": ["bubble shield", ...], "maxDur": 2.5, "loop": false}, ...}  (loop: true = 이름 거르기 끔)
  out.json  = {"<key>": [후보 항목, ...], ...}  — 여러 검색어에 걸린 것 · 앞 순위 · 내려받기 많은 것부터, 길이 · 엉뚱한 이름으로 거른다.
  고른 뒤 사람이 다시 훑어 빼는 것을 전제로 한다(이름만 보고 거르므로).
"""
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request

UA = {"User-Agent": "Mozilla/5.0"}
PLAYER = re.compile(r'<div\s+class="bw-player(?:\s[^"]*)?"[^>]*>')  # bw-player__img-container 같은 안쪽 요소는 빼고 카드 자체만
ATTR = re.compile(r'data-([a-z0-9-]+)="([^"]*)"')
LIC = re.compile(r'title="License: ([^"]+)"')
BAD = re.compile(r"music|loop|song|beat|ambien|melody|voice|vocal|speech|guitar|piano|drum|bass|chord|track|podcast|full mix", re.I)


def search(q):
    url = "https://freesound.org/search/?q=" + urllib.parse.quote(q)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        page = r.read().decode("utf-8", "replace")
    tags = list(PLAYER.finditer(page))
    out = []
    for i, m in enumerate(tags):
        a = {k: html.unescape(v) for k, v in ATTR.findall(m.group(0))}
        stop = tags[i + 1].start() if i + 1 < len(tags) else len(page)
        lic = LIC.search(page, m.end(), stop)
        sid = a.get("sound-id")
        if not sid or not a.get("mp3"):
            continue
        out.append({"src": "freesound", "id": sid, "title": a.get("title", sid), "user": a.get("username", ""),
                    "dur": round(float(a.get("duration", 0) or 0), 2), "lic": lic.group(1) if lic else "",
                    "url": f"https://freesound.org/people/{a.get('username', '')}/sounds/{sid}/", "mp3": a["mp3"],
                    "downloads": int(float(a.get("num-downloads", 0) or 0)), "rank": i})
    return out


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except AttributeError:
            pass
    plan = json.load(open(sys.argv[1], encoding="utf-8"))
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 14
    result = {}
    for key, p in plan.items():
        pool = {}
        for q in p["queries"]:
            try:
                for it in search(q):
                    cur = pool.get(it["id"])
                    if cur:
                        cur["hits"] += 1
                        cur["rank"] = min(cur["rank"], it["rank"])
                    else:
                        it["hits"] = 1
                        pool[it["id"]] = it
            except Exception as e:
                print(f"{key} '{q}': {e}", file=sys.stderr)
            time.sleep(0.3)
        # 계속 나는 소리(부스터 지속음 · 비행 물살 등)는 "loop" · "ambience" 이름이 맞는 후보라 "loop": true면 이름 거르기를 끈다
        ok = [c for c in pool.values() if 0 < c["dur"] <= p.get("maxDur", 3) and (p.get("loop") or not BAD.search(c["title"]))
              and c["lic"] in ("Creative Commons 0", "Attribution", "Attribution NonCommercial")]
        ok.sort(key=lambda c: (-c["hits"], c["rank"], -c["downloads"]))
        result[key] = [{k: v for k, v in c.items() if k not in ("rank", "hits")} for c in ok[:limit]]
        print(f"{key}: 모은 {len(pool)} → 남김 {len(result[key])}")
    json.dump(result, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
