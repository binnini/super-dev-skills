"""Freesound 소리 id 목록 → 후보 항목(JSON). 브라우저에서 고른 id만 넘기면 각 소리 페이지에서 제목 · 올린 사람 · 길이 · 라이선스 · 미리듣기를 읽는다.

실행(프로젝트 루트에서): <python> <skill_dir>/scripts/freesound_ids.py <ids.json> <out.json>
  ids.json = {"<key>": ["123", "456", ...], ...}  → out.json = {"<key>": [후보 항목, ...], ...}
Freesound는 셸(curl/urllib)로 읽힌다(10-23 확인). Pixabay는 403이라 브라우저(references/extract.md)로만.
"""
import html
import json
import re
import sys
import time
import urllib.request

UA = {"User-Agent": "Mozilla/5.0"}
ATTR = re.compile(r'data-([a-z0-9-]+)="([^"]*)"')


def player_attrs(page, sid):
    # 소리 페이지의 bw-player 태그(data-sound-id가 그 소리인 것)
    for m in re.finditer(r'<div\s+class="bw-player[^>]*>', page):  # 소리 페이지는 속성마다 줄을 바꾼다
        tag = m.group(0)
        if f'data-sound-id="{sid}"' in tag:
            return {k: html.unescape(v) for k, v in ATTR.findall(tag)}
    return None


def license_of(page):
    # 소리 페이지의 라이선스 링크(creativecommons.org/...). 사이트 안내 문구의 다른 링크와 섞이지 않게 처음 것을 쓴다
    m = re.search(r'creativecommons\.org/(publicdomain/zero|licenses/by-nc|licenses/by|licenses/sampling\+?)/', page)
    if not m:
        return ""
    return {"publicdomain/zero": "Creative Commons 0", "licenses/by-nc": "Attribution NonCommercial",
            "licenses/by": "Attribution"}.get(m.group(1), m.group(1))


def fetch(sid):
    url = f"https://freesound.org/s/{sid}/"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        final, page = r.geturl(), r.read().decode("utf-8", "replace")
    a = player_attrs(page, sid)
    if not a:
        return None
    user = a.get("username") or (re.search(r"/people/([^/]+)/", final) or [None, ""])[1]  # 소리 페이지는 username이 비어 있다
    return {"src": "freesound", "id": sid, "title": a.get("title", sid), "user": user,
            "dur": round(float(a.get("duration", 0)), 2), "lic": license_of(page), "url": final,
            "mp3": a.get("mp3", ""), "downloads": int(float(a.get("num-downloads", 0) or 0))}


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except AttributeError:
            pass
    ids = json.load(open(sys.argv[1], encoding="utf-8"))
    out = {}
    for key, lst in ids.items():
        out[key] = []
        for sid in lst:
            try:
                item = fetch(sid)
            except Exception as e:  # 한 소리가 실패해도 나머지는 계속
                print(f"{key} {sid}: {e}", file=sys.stderr)
                continue
            if item:
                out[key].append(item)
            else:
                print(f"{key} {sid}: 페이지에서 소리를 못 찾음", file=sys.stderr)
            time.sleep(0.2)
        print(f"{key}: {len(out[key])}/{len(lst)}")
    json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
