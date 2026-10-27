"""스킬 저장소 검사. 저장소 루트에서: python -I tests/run_tests.py

1. 구조: 마켓플레이스 항목 ↔ 플러그인 이름 · 버전, SKILL.md 머리(name = 폴더 이름, description 1024자 이하)
2. 바뀐 것: 플러그인 버전마다 CHANGELOG 줄이 있는지
3. 문법: scripts/*.py 컴파일, *.js는 node --check(node가 있으면)
4. 동작: web-vfx-search 스크립트를 작은 가짜 시트로 끝까지 돌림, web-sound-search 비교 페이지 · 현황 페이지 만들기
"""
import json, os, py_compile, re, shutil, subprocess, sys, tempfile

for _s in (sys.stdout, sys.stderr):  # Windows 콘솔(cp949)에서 한글 · 기호가 깨지거나 멈추지 않게(-I는 PYTHONIOENCODING을 무시)
    try:
        _s.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
fails = []


def check(ok, msg):
    print(('PASS ' if ok else 'FAIL ') + msg)
    if not ok:
        fails.append(msg)


def frontmatter(path):
    s = open(path, encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---\n', s, re.S)
    if not m:
        return {}
    return dict(l.split(':', 1) for l in m.group(1).splitlines() if ':' in l)


def run(args, **kw):
    r = subprocess.run(args, capture_output=True, text=True, encoding='utf-8', **kw)
    return r.returncode, r.stdout + r.stderr


# 1 · 2 구조와 바뀐 것
market = json.load(open(os.path.join(ROOT, '.claude-plugin', 'marketplace.json'), encoding='utf-8'))
changelog = open(os.path.join(ROOT, 'CHANGELOG.md'), encoding='utf-8').read()
for entry in market['plugins']:
    pdir = os.path.join(ROOT, entry['source'])
    manifest = json.load(open(os.path.join(pdir, '.claude-plugin', 'plugin.json'), encoding='utf-8'))
    check(manifest['name'] == entry['name'], f"{entry['name']}: 마켓플레이스 이름 = plugin.json 이름")
    ver = manifest.get('version')
    check(bool(ver) and 'version' not in entry, f"{entry['name']}: 버전은 plugin.json에만 ({ver})")
    check(f"## {entry['name']} {ver}" in changelog, f"{entry['name']} {ver}: CHANGELOG에 '## {entry['name']} {ver}' 줄")
    sdir = os.path.join(pdir, 'skills')
    for name in sorted(os.listdir(sdir)) if os.path.isdir(sdir) else []:
        fm = frontmatter(os.path.join(sdir, name, 'SKILL.md'))
        check(fm.get('name', '').strip() == name, f'{name}: SKILL.md name = 폴더 이름')
        d = fm.get('description', '').strip()
        check(0 < len(d) <= 1024, f'{name}: description 길이 {len(d)} (1~1024)')
        body = open(os.path.join(sdir, name, 'SKILL.md'), encoding='utf-8').read()
        check('Assets/_Project' not in body.split('---', 2)[2].replace('예:', ''),
              f'{name}: 본문에 프로젝트 경로를 적지 않음(프로필 키로)')

# 3 문법
for dp, _, fs in os.walk(os.path.join(ROOT, 'plugins')):
    for f in fs:
        p = os.path.join(dp, f)
        if f.endswith('.py'):
            try:
                py_compile.compile(p, doraise=True, cfile=os.path.join(tempfile.gettempdir(), 'pc.pyc'))
                check(True, f'컴파일 {os.path.relpath(p, ROOT)}')
            except py_compile.PyCompileError as e:
                check(False, f'컴파일 {os.path.relpath(p, ROOT)}: {e}')
        elif f.endswith('.js') and shutil.which('node'):
            code, out = run(['node', '--check', p])
            check(code == 0, f'node --check {os.path.relpath(p, ROOT)} {out.strip()}')

# 4 동작
try:
    from PIL import Image, ImageDraw
except ImportError:
    Image = None
check(Image is not None, 'Pillow 있음(web-vfx-search 동작 검사에 필요)')
if Image:
    V = os.path.join(ROOT, 'plugins', 'assets', 'skills', 'web-vfx-search', 'scripts')
    tmp = tempfile.mkdtemp()
    atlas = os.path.join(tmp, 'a.png')
    im = Image.new('RGBA', (256, 128), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    for i in range(2):  # 칸마다 고리 + 가운데 점
        cx = i * 128 + 64
        dr.ellipse((cx - 40 + i, 24, cx + 40 + i, 104), outline=(255, 200, 40, 255), width=3)  # 칸마다 달라야 GIF가 프레임을 합치지 않음
        dr.rectangle((cx - 4, 60, cx + 4, 68), fill=(255, 255, 255, 255))
    im.save(atlas)
    T = [PY, '-I', os.path.join(V, 'atlas_tools.py')]
    code, out = run(T + ['extent', atlas, '--unit', '24'])
    check(code == 0 and out.startswith('81 px'), f'extent: {out.strip()} (기대 81 px)')
    gif = os.path.join(tmp, 'a.gif')
    code, out = run(T + ['gif', atlas, gif])
    check(code == 0 and Image.open(gif).n_frames == 2, 'gif: 2프레임')
    cleared = os.path.join(tmp, 'c.png')
    code, out = run(T + ['clear', atlas, cleared, '--radius', '15'])
    check(code == 0 and Image.open(cleared).getpixel((64, 64))[3] == 0 and Image.open(cleared).getpixel((64, 24))[3] > 0,
          'clear: 가운데만 지움')
    code, out = run(T + ['contact', os.path.join(tmp, 'v.png'), atlas, cleared])
    check(code == 0, 'contact')
    readme = os.path.join(tmp, 'r.txt'); open(readme, 'w').write('x')
    code, out = run(T + ['pack', 'fx', os.path.join(tmp, 'out'), '--atlas', atlas, '--cleared', cleared, '--readme', readme])
    check(code == 0 and os.path.exists(os.path.join(tmp, 'out', 'fx.zip')), 'pack: zip')

    os.makedirs(os.path.join(tmp, 'prev'))
    shutil.copy(gif, os.path.join(tmp, 'prev', 'a.gif'))
    card = {'id': 'a', 'rank': 1, 'name': '시험 고리', 'by': 'test', 'url': 'https://example.com', 'img': 'prev/a.gif',
            'pw': 128, 'disp': 3, 'price': '0원', 'lic': 'CC0', 'licTag': 'own', 'spec': 's', 'fit': ['f'], 'risk': ['r']}
    cfg = {'key': 'vfx_test', 'title': '시험 <후보>', 'need': ['노랑'], 'unitPx': 24, 'unitLabel': '문어 1칸',
           'candidates': [card], 'reference': [['유료', 'https://example.com', '레퍼런스']], 'excluded': []}
    src = os.path.join(tmp, 'vfx_test_candidates.json')
    json.dump(cfg, open(src, 'w', encoding='utf-8'), ensure_ascii=False)
    code, out = run([PY, '-I', os.path.join(V, 'build_page.py'), src])
    page = open(src.replace('.json', '.html'), encoding='utf-8').read() if code == 0 else ''
    left = re.findall(r'__[A-Z]+__', page)
    check(code == 0 and not left and 'data:image/gif;base64,' in page and '시험 &lt;후보&gt;' in page,
          f'vfx build_page: 자리표시 남은 것 {left}')
    cfg['candidates'][0]['licTag'] = 'paid'
    json.dump(cfg, open(src, 'w', encoding='utf-8'), ensure_ascii=False)
    code, out = run([PY, '-I', os.path.join(V, 'build_page.py'), src])
    check(code != 0 and 'reference' in out, 'vfx build_page: 유료 후보를 막음')
    shutil.rmtree(tmp)

S = os.path.join(ROOT, 'plugins', 'assets', 'skills', 'web-sound-search', 'scripts')
tmp = tempfile.mkdtemp()
cfg = {'key': 'snd_test', 'title': '시험 소리', 'purpose': 'p', 'searched': '2026-10-24', 'queries': ['pop'],
       'candidates': [{'src': 'freesound', 'id': '1', 'title': 't', 'user': 'u', 'dur': 0.3, 'lic': 'Creative Commons 0',
                       'url': 'https://freesound.org/s/1/', 'mp3': 'https://example.com/1.mp3', 'downloads': 1}]}
src = os.path.join(tmp, 'c.json'); json.dump(cfg, open(src, 'w', encoding='utf-8'))
out_html = os.path.join(tmp, 'c.html')
code, out = run([PY, '-I', os.path.join(S, 'build_page.py'), src, out_html], cwd=tmp)
check(code == 0 and '/*CONFIG*/null' not in open(out_html, encoding='utf-8').read(), f'sound build_page: {out.strip()[:80]}')
shutil.rmtree(tmp)

# web-sound-search 현황 페이지: 가짜 프로젝트(프로필 · enum · 소리 SO · .meta · 이름표)로 끝까지
tmp = tempfile.mkdtemp()
def put(rel, text):
    p = os.path.join(tmp, rel); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'w', encoding='utf-8').write(text)
put('.claude/skill-profile.yaml', 'work_dir: web\nsound:\n  slots: Game/Sound.cs   # 주석\n  enum: SoundId\n'
    '  tuning_asset: Game/Sound.asset\n  audio_dir: Game/Audio\n  labels: .claude/labels.json\n'
    '  preview_server: { name: board, port: 8093 }\ndocs:\n  credits_sound: docs/credits.md\n')
put('Game/Sound.cs', 'public enum SoundId { Dash, Land, // 착지\n Dot }\n')
put('Game/Sound.asset', '  useOriginal: 0\n  useTempTones: 1\n  volume: 1\n'
    '  - id: 0\n    clip: \n    volume: 0.8\n    layers:\n    - clip: {fileID: 8300000, guid: abc123, type: 3}\n      volume: 1\n      pitch: 1.2\n      delay: 0\n'
    '  - id: 2\n    clip: \n    volume: 1\n    layers: []\n')
put('Game/Audio/Sfx/dash.wav', 'x')
put('Game/Audio/Sfx/dash.wav.meta', 'fileFormatVersion: 2\nguid: abc123\n')
put('.claude/labels.json', json.dumps({'groups': ['플레이어'], 'labels': {'Dash': ['대시', '플레이어']}, 'tempTones': ['Dot']}))
put('docs/credits.md', '## BY — 출처 표기\n| 순간 | 파일 | 원본 |\n|---|---|---|\n| 대시 | `Sfx/dash.wav` | [Swish](https://freesound.org/s/1/) |\n')
code, out = run([PY, '-I', os.path.join(S, 'build_status.py')], cwd=tmp)
page = open(os.path.join(tmp, 'web', 'sound_status.html'), encoding='utf-8').read() if code == 0 else ''
m = re.search(r'const DATA = (\{.*?\});\n', page)
data = json.loads(m.group(1)) if m else {}
st = {r['id']: r['state'] for r in data.get('rows', [])}
dash = next((r for r in data.get('rows', []) if r['id'] == 'Dash'), {})
check(code == 0 and st == {'Dash': 'own', 'Dot': 'temp'} and 'Land: 에셋에 항목 없음' in out
      and dash.get('layers', [{}])[0].get('src') == '../Game/Audio/Sfx/dash.wav'
      and dash['layers'][0].get('credit', {}).get('lic') == 'BY' and data.get('hasOriginal') is False
      and 'localhost:8093/web/sound_status.html' in out, f'sound build_status: {st} {out.strip()[:120]}')
os.remove(os.path.join(tmp, '.claude', 'skill-profile.yaml'))
code, out = run([PY, '-I', os.path.join(S, 'build_status.py')], cwd=tmp)
check(code != 0 and 'skill-profile.yaml' in out, 'sound build_status: 프로필이 없으면 멈춤')
shutil.rmtree(tmp)

print(f"\n{'FAIL ' + str(len(fails)) if fails else 'ALL PASS'}")
sys.exit(1 if fails else 0)
