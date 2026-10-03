"""Genera icon.icns (mac), icon.ico (windows) e icon.png per l'app: barca stilizzata su fondo blu notte."""
import sys
from PIL import Image, ImageDraw

S = 1024
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# Fondo arrotondato, gradiente manuale a fasce
NAVY = (11, 31, 42)
TEAL = (14, 116, 144)
mask = Image.new("L", (S, S), 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle([16, 16, S - 16, S - 16], radius=200, fill=255)
grad = Image.new("RGBA", (S, S))
gd = ImageDraw.Draw(grad)
for y in range(S):
    t = y / S
    r = int(NAVY[0] + (TEAL[0] - NAVY[0]) * t)
    g = int(NAVY[1] + (TEAL[1] - NAVY[1]) * t)
    b = int(NAVY[2] + (TEAL[2] - NAVY[2]) * t)
    gd.line([(0, y), (S, y)], fill=(r, g, b, 255))
img.paste(grad, (0, 0), mask)

W = (255, 255, 255, 255)
AMBER = (245, 158, 11, 255)

# Onde
for i, y in enumerate([830, 880, 925]):
    x = -80 + i * 60
    while x < S + 80:
        d.arc([x, y, x + 160, y + 90], start=200, end=340, fill=W, width=22)
        x += 150

# Scafo
d.polygon([(190, 780), (834, 780), (740, 900), (284, 900)], fill=W)

# Albero
d.line([(512, 250), (512, 760)], fill=W, width=26)

# Vela principale (bianca)
d.polygon([(512, 260), (512, 730), (280, 730)], fill=W)
# Vela secondaria (ambra)
d.polygon([(546, 300), (546, 730), (760, 730)], fill=AMBER)

# Bandierina
d.polygon([(512, 250), (620, 285), (512, 320)], fill=AMBER)

img.save("icon.png")

# ico per Windows (setup e PyInstaller win)
img.save(
    "icon.ico",
    sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
)

# iconset → icns (solo macOS: iconutil non esiste altrove)
import os, subprocess, shutil
if sys.platform == "darwin":
    os.makedirs("icon.iconset", exist_ok=True)
    for size in [16, 32, 64, 128, 256, 512, 1024]:
        img.resize((size, size), Image.LANCZOS).save(f"icon.iconset/icon_{size}x{size}.png")
        if size <= 512:
            img.resize((size * 2, size * 2), Image.LANCZOS).save(f"icon.iconset/icon_{size}x{size}@2x.png")
    subprocess.run(
        ["iconutil", "-c", "icns", "icon.iconset", "-o", "icon.icns"],
        check=True,
    )
    shutil.rmtree("icon.iconset")
print("icon.png / icon.ico" + (" / icon.icns generate" if sys.platform == "darwin" else " generate"))
