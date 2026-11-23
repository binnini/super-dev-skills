"""초록 배경(#00FF00) 생성 그림(JPG, 알파 없음)을 투명 PNG로 키잉하고 캔버스에 맞춘다(imagegen 스킬 8단계).

사이트 결과는 JPG라 알파가 없다. 투명 그림이 필요하면 프롬프트에 단색 초록 배경을 넣고 이 스크립트로 뺀다
(윤곽이 굵은 카툰은 깔끔하게 빠진다. CrazyArena 10-29 ~ 아이템 · 보석 · 바리케이드 그림).

실행(프로젝트 루트에서, Pillow · numpy 필요):
  <python> <skill_dir>/scripts/key_fit.py <in.jpg> <out.png> [--size 1024] [--height-frac 0.84] [--bottom 64(기본 높이/16)]
  --no-fit       키잉 + 그림 테두리로 자르기만(확인용)
  --fit-h H      그림 높이를 H px로 맞춘다(같은 종류 그림끼리 크기를 맞출 때). 기본 = size × height_frac
  --fit-w W      대신 너비를 맞춘다(가로로 긴 물건)
  --canvas WxH   정사각형이 아닌 캔버스(예: 256x768)
  --center-v     아래 맞춤 대신 세로 가운데
  --t0 / --t1    초록 정도가 t1보다 크면 투명, t0보다 작으면 불투명(사이는 부드러운 가장자리)
가장자리의 초록 번짐은 G를 max(R, B) 근처로 내려 줄인다.
"""
import argparse
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

try:
    import numpy as np
    from PIL import Image
except ImportError:
    sys.exit("Pillow · numpy가 필요하다: <python> -m pip install pillow numpy")

ap = argparse.ArgumentParser(description="초록 배경 키잉 + 캔버스 맞춤")
ap.add_argument("src")
ap.add_argument("dst")
ap.add_argument("--size", type=int, default=1024)
ap.add_argument("--canvas", default="")
ap.add_argument("--height-frac", type=float, default=0.84)
ap.add_argument("--bottom", type=int, default=-1, help="아래 여백 px(기본 = 캔버스 높이 / 16)")
ap.add_argument("--fit-h", type=int, default=0)
ap.add_argument("--fit-w", type=int, default=0)
ap.add_argument("--center-v", action="store_true")
ap.add_argument("--no-fit", action="store_true")
ap.add_argument("--t0", type=float, default=60.0)
ap.add_argument("--t1", type=float, default=140.0)
a = ap.parse_args()

rgb = np.asarray(Image.open(a.src).convert("RGB")).astype(np.float32)
r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
green = g - np.maximum(r, b)  # 순수 키 색 ≈ 240
alpha = np.clip((a.t1 - green) / (a.t1 - a.t0), 0.0, 1.0)
g2 = np.where(alpha < 1.0, np.minimum(g, np.maximum(r, b) + 10), g)
out = np.stack([r, g2, b, alpha * 255.0], axis=-1)
png = Image.fromarray(out.astype(np.uint8), "RGBA")

ys, xs = np.where(out[..., 3] > 8)
if len(xs) == 0:
    sys.exit("불투명한 곳이 없다(배경만 있음)")
x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
spr = png.crop((x0, y0, x1, y1))
print(f"{a.src}: 그림 {x1 - x0}x{y1 - y0} at ({x0},{y0})")
if a.no_fit:
    spr.save(a.dst)
    print("저장", a.dst, spr.size)
    sys.exit(0)

if a.canvas:
    cw, ch = [int(v) for v in a.canvas.lower().split("x")]
else:
    cw = ch = a.size
if a.fit_w:
    scale = a.fit_w / spr.width
elif a.fit_h:
    scale = a.fit_h / spr.height
else:
    scale = (ch * a.height_frac) / spr.height
bottom = a.bottom if a.bottom >= 0 else ch // 16
scale = min(scale, (cw - 16) / spr.width, (ch - (0 if a.center_v else bottom) - 8) / spr.height)  # 캔버스를 넘치지 않게
nw, nh = max(1, round(spr.width * scale)), max(1, round(spr.height * scale))
spr = spr.resize((nw, nh), Image.LANCZOS)
canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
px = (cw - nw) // 2
py = (ch - nh) // 2 if a.center_v else ch - bottom - nh
canvas.paste(spr, (px, py), spr)
canvas.save(a.dst)
print("저장", a.dst, canvas.size, "그림", (nw, nh), "at", (px, py))
