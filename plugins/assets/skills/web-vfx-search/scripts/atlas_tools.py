"""시트(atlas) PNG 다루기: 미리보기 GIF, 크기 재기, 한눈 시트, 가운데 지우기, 전달 묶음.

<python> <skill_dir>/scripts/atlas_tools.py gif     <atlas.png> <out.gif> [--cell 128] [--ms 60]
<python> <skill_dir>/scripts/atlas_tools.py extent  <atlas.png> [--cell 128] [--unit 24]
<python> <skill_dir>/scripts/atlas_tools.py contact <out.png> <atlas.png>... [--cell 128] [--unit 24] [--bg #0b1420]
<python> <skill_dir>/scripts/atlas_tools.py clear   <atlas.png> <out.png> --radius 15 [--cell 128]
<python> <skill_dir>/scripts/atlas_tools.py pack    <name> <out_dir> --atlas a.png [--cleared b.png] --readme readme.txt [--cell 128] [--ms 60]
  (<python> = 프로필 값, <skill_dir> = web-vfx-search 폴더)

시트는 왼쪽 위부터 가로로 읽는 칸 격자(Forge: 1024 x 384 = 8 x 3, 128 px)로 본다.
알파 60 이하는 투명으로 친다(GIF는 1비트 투명이라 미리보기 전용).
"""
import argparse, math, os, shutil, sys
from PIL import Image, ImageDraw

ALPHA = 60

for _s in (sys.stdout, sys.stderr):  # Windows 콘솔(cp949)에서 한글이 깨지지 않게(-I는 PYTHONIOENCODING을 무시)
    try:
        _s.reconfigure(encoding='utf-8')
    except AttributeError:
        pass



def frames(path, cell):
    a = Image.open(path).convert('RGBA')
    cols, rows = a.width // cell, a.height // cell
    return [a.crop((c * cell, r * cell, c * cell + cell, r * cell + cell)) for r in range(rows) for c in range(cols)]


def save_gif(frs, out, ms):
    ps = []
    for fr in frs:
        hole = fr.getchannel('A').point(lambda v: 0 if v > ALPHA else 255)
        p = fr.convert('RGB').quantize(255, dither=0)
        p.paste(255, mask=hole)
        ps.append(p)
    ps[0].save(out, save_all=True, append_images=ps[1:], duration=ms, loop=0, transparency=255, disposal=2)


def extent(frs):
    best = 0
    for fr in frs:
        b = fr.getchannel('A').point(lambda v: 255 if v > ALPHA else 0).getbbox()
        if b:
            best = max(best, b[2] - b[0], b[3] - b[1])
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['gif', 'extent', 'contact', 'clear', 'pack'])
    ap.add_argument('args', nargs='+')
    ap.add_argument('--cell', type=int, default=128)
    ap.add_argument('--unit', type=int, default=24)
    ap.add_argument('--ms', type=int, default=60)
    ap.add_argument('--radius', type=float, default=15)
    ap.add_argument('--bg', default='#0b1420')
    ap.add_argument('--atlas'); ap.add_argument('--cleared'); ap.add_argument('--readme')
    o = ap.parse_args()

    if o.cmd == 'gif':
        save_gif(frames(o.args[0], o.cell), o.args[1], o.ms)
    elif o.cmd == 'extent':
        px = extent(frames(o.args[0], o.cell))
        print(f'{px} px ≈ {px / o.unit:.1f}칸')
    elif o.cmd == 'contact':
        out, atlases = o.args[0], o.args[1:]
        sheet = Image.new('RGBA', (o.cell * len(atlases), o.cell + 14), o.bg)
        dr = ImageDraw.Draw(sheet)
        for i, a in enumerate(atlases):
            frs = frames(a, o.cell)
            sheet.alpha_composite(frs[len(frs) // 2], (i * o.cell, 14))
            h = o.unit // 2
            cx, cy = i * o.cell + o.cell // 2, 14 + o.cell // 2
            dr.rectangle((cx - h, cy - h, cx + h, cy + h), outline='#ff8a3d')
            dr.text((i * o.cell + 2, 1), os.path.basename(a)[:20], fill='#cfd8e3')
        sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(out)
    elif o.cmd == 'clear':
        a = Image.open(o.args[0]).convert('RGBA')
        px, c = a.load(), (o.cell - 1) / 2
        for y in range(a.height):
            for x in range(a.width):
                if math.hypot(x % o.cell - c, y % o.cell - c) <= o.radius:
                    px[x, y] = (0, 0, 0, 0)
        a.save(o.args[1])
    elif o.cmd == 'pack':
        name, out_dir = o.args[0], o.args[1]
        root = os.path.join(out_dir, name)
        for kind, src in (('original', o.atlas), ('center_cleared', o.cleared)):
            if not src:
                continue
            d = os.path.join(root, kind, 'frames')
            os.makedirs(d, exist_ok=True)
            shutil.copy(src, os.path.join(root, kind, f'{name}_sheet.png'))
            frs = frames(src, o.cell)
            for i, fr in enumerate(frs):
                fr.save(os.path.join(d, f'{name}_{i:02d}.png'))
            save_gif(frs, os.path.join(root, kind, f'{name}_preview.gif'), o.ms)
        if o.readme:
            shutil.copy(o.readme, os.path.join(root, 'README.txt'))
        print(shutil.make_archive(root, 'zip', out_dir, name))


if __name__ == '__main__':
    main()
