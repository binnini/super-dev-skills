"""후보 파일(json) → VFX 비교 페이지(html 한 장, 그림은 안에 넣음).

<python> <skill_dir>/scripts/build_page.py <work_dir>/vfx/<key>_candidates.json [out.html]

후보 파일 형식(그림 경로는 json 파일 기준):
{
  "key": "vfx_magnet_aura",                # localStorage 키(☆ · 결정 저장)
  "title": "자석 오라 후보",
  "eyebrow": "VFX 검색 · <프로젝트> · 2026-10-24",
  "lede": "무엇을 찾았고 어떻게 거렀는지 한두 문장(HTML 가능)",
  "need": ["순간: 자석 먹음 → 켜진 동안 계속", "노랑", ...],   # 조건 칩
  "note": "먼저 정할 것(HTML, 없으면 생략)",
  "unitPx": 24, "unitLabel": "문어 1칸",   # 프로필 cell_px · 캐릭터 이름
  "stageBg": "#0b1620",                    # 프로필 vfx.background
  "tintLabel": "노랗지 않은 후보를 노란색으로 보기",
  "tintFilter": "grayscale(1) sepia(1) saturate(6) hue-rotate(5deg) brightness(1.15)",
  "candidates": [{
      "id", "rank", "name", "by", "url",
      "img": "prev/x.gif", "pw": 128,      # 미리보기 그림 폭(px)
      "disp": 3,                           # 원본 1 px → 화면 3 px가 되는 배율. 모르면 null(홍보 그림)
      "price": "0원 가능(...)", "lic": "...", "licTag": "own|zero|cc0|free|check",
      "spec": "...", "fit": ["..."], "risk": ["..."], "recolor": false
  }],
  "reference": [["이름", "url", "왜 레퍼런스로만"]],     # 유료
  "excluded":  [["이름", "url", "왜 뺐나"]]
}
"""
import base64, html, json, mimetypes, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, '..', 'assets', 'page_template.html')

for _s in (sys.stdout, sys.stderr):  # Windows 콘솔(cp949)에서 한글이 깨지지 않게(-I는 PYTHONIOENCODING을 무시)
    try:
        _s.reconfigure(encoding='utf-8')
    except AttributeError:
        pass



def data_uri(path):
    mime = mimetypes.guess_type(path)[0] or 'application/octet-stream'
    with open(path, 'rb') as f:
        return f'data:{mime};base64,' + base64.b64encode(f.read()).decode()


def rows(items):
    return ''.join(f'<li><a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(n)}</a> · {html.escape(w)}</li>'
                   for n, u, w in items)


def build(src, out):
    with open(src, encoding='utf-8') as f:
        d = json.load(f)
    base = os.path.dirname(os.path.abspath(src))
    for c in d['candidates']:
        if c['licTag'] == 'paid':
            raise SystemExit(f"{c['id']}: 유료 후보는 candidates가 아니라 reference에 둔다")
        c['img'] = data_uri(os.path.join(base, c['img']))
    note = d.get('note')
    t = open(TEMPLATE, encoding='utf-8').read()
    for k, v in {
        '__DATA__': json.dumps(d['candidates'], ensure_ascii=False),
        '__TITLEJSON__': json.dumps(d['title'], ensure_ascii=False),
        '__KEYJSON__': json.dumps(d['key']),
        '__UNITPX__': str(int(d.get('unitPx', 24))),
        '__UNITLABEL__': json.dumps(d.get('unitLabel', '캐릭터 1칸'), ensure_ascii=False),
        '__STAGEBG__': d.get('stageBg', '#0b1620'),
        '__TINTLABEL__': html.escape(d.get('tintLabel', '색을 바꿔 보기')),
        '__TINTFILTER__': d.get('tintFilter', 'none'),
        '__TITLE__': html.escape(d['title']),
        '__EYEBROW__': html.escape(d.get('eyebrow', '')),
        '__LEDE__': d.get('lede', ''),
        '__NEED__': ''.join(f'<span>{html.escape(x)}</span>' for x in d.get('need', [])),
        '__NOTE__': f'<div class="note"><p>{note}</p></div>' if note else '',
        '__REFERENCE__': rows(d.get('reference', [])) or '<li>없음</li>',
        '__EXCLUDED__': rows(d.get('excluded', [])) or '<li>없음</li>',
    }.items():
        t = t.replace(k, v)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(t)
    print(out, os.path.getsize(out) // 1024, 'KB')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else src.replace('_candidates.json', '_candidates.html')
    build(src, out)
