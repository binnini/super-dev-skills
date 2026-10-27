"""소리 후보 JSON → 비교 페이지 HTML(웹 소리 찾기 스킬).

실행(프로젝트 루트에서): <python> <skill_dir>/scripts/build_page.py <candidates.json> [out.html]
  out을 빼면 후보 파일 옆 <key>_candidates.html(보통 <work_dir>, git 무시).

candidates.json 형식(SKILL.md "후보 파일"):
{
  "key": "suction",                 # 페이지 이름 · 브라우저 저장 키(<key>_stars · <key>_choice)
  "title": "빨판 소리 후보",
  "purpose": "문어가 출발할 때 …",   # 페이지 머리 설명(HTML 가능)
  "searched": "2026-10-23",
  "queries": ["suction cup", ...],
  "pattern": {"name": "뚜두둑", "count": 3, "gap": 0.035, "spread": 0.15} 또는 null,
  "game": [{"src": "<work_dir에서 sound.sfx_dir까지 상대 경로>/...", "volume": 1, "pitch": 1, "delay": 0}, ...],  # 같이 들을 게임 소리(페이지 기준 경로)
  "gameLabel": "대시와 같이",
  "candidates": [{"src": "freesound|pixabay", "id": "...", "title": "...", "user": "...", "dur": 0.4,
                  "lic": "Creative Commons 0|Attribution|Attribution NonCommercial|Pixabay Content License",
                  "url": "사이트 페이지", "mp3": "미리듣기 mp3", "downloads": 123}, ...]
}
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.getcwd()  # 프로젝트 루트에서 실행한다(플러그인 캐시 위치와 무관)
TEMPLATE = os.path.join(HERE, "..", "assets", "page_template.html")
NEED = ("key", "title", "purpose", "searched", "queries", "candidates")
LICENSES = {"Creative Commons 0", "Attribution", "Attribution NonCommercial", "Pixabay Content License"}


def check(cfg):
    miss = [k for k in NEED if k not in cfg]
    if miss:
        sys.exit(f"빠진 항목: {miss}")
    seen, problems = set(), []
    for c in cfg["candidates"]:
        k = f'{c.get("src")}:{c.get("id")}'
        if k in seen:
            problems.append(f"중복 {k}")
        seen.add(k)
        for f in ("src", "id", "title", "dur", "lic", "url", "mp3"):
            if c.get(f) in (None, ""):
                problems.append(f"{k}: {f} 없음")
        if c.get("lic") not in LICENSES:
            problems.append(f"{k}: 모르는 라이선스 {c.get('lic')!r}")
    for g in cfg.get("game") or []:
        p = os.path.normpath(os.path.join(ROOT, "references", "web", g["src"]))
        if not os.path.exists(p):
            problems.append(f"게임 소리 없음: {g['src']}")
    return problems


def main():
    # Windows 콘솔(cp949)에서 한글이 깨지지 않게(-I는 PYTHONIOENCODING을 무시한다)
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except AttributeError:
            pass
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    cfg.setdefault("pattern", None)
    cfg.setdefault("game", [])
    problems = check(cfg)
    for p in problems:
        print("확인:", p, file=sys.stderr)
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), f'{cfg["key"]}_candidates.html')
    html = open(TEMPLATE, encoding="utf-8").read().replace("/*CONFIG*/null", json.dumps(cfg, ensure_ascii=False))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)
    rel = os.path.relpath(out, ROOT).replace("\\", "/")
    print(f"{out}: 후보 {len(cfg['candidates'])}개, 확인 {len(problems)}건")
    if not rel.startswith(".."):  # 저장소 루트를 여는 서버로 연다
        print(f"열기: http://localhost:<sound.preview_server port>/{rel}")


if __name__ == "__main__":
    main()
