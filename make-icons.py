from PIL import Image, ImageDraw
import os
RES = "android/app/src/main/res"
src = Image.open("icon.png").convert("RGBA")
px = src.getpixel((0, 0))
bg = (143, 211, 255) if px[3] < 128 else px[:3]
hexbg = "#%02x%02x%02x" % bg

def save(img, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)

legacy = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
adaptive = {"mdpi": 108, "hdpi": 162, "xhdpi": 216, "xxhdpi": 324, "xxxhdpi": 432}

for d, s in legacy.items():
    im = src.resize((s, s), Image.LANCZOS)
    save(im, f"{RES}/mipmap-{d}/ic_launcher.png")
    mask = Image.new("L", (s * 4, s * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, s * 4 - 1, s * 4 - 1), fill=255)
    mask = mask.resize((s, s), Image.LANCZOS)
    rnd = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    rnd.paste(im, (0, 0), mask)
    save(rnd, f"{RES}/mipmap-{d}/ic_launcher_round.png")

for d, s in adaptive.items():
    logo = int(s * 0.62)
    canvas = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    canvas.paste(src.resize((logo, logo), Image.LANCZOS), ((s - logo) // 2, (s - logo) // 2))
    save(canvas, f"{RES}/mipmap-{d}/ic_launcher_foreground.png")

xml = ('<?xml version="1.0" encoding="utf-8"?>\n'
       '<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
       '    <background android:drawable="@color/ic_launcher_background"/>\n'
       '    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>\n'
       '</adaptive-icon>\n')
for n in ("ic_launcher.xml", "ic_launcher_round.xml"):
    save_path = f"{RES}/mipmap-anydpi-v26/{n}"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    open(save_path, "w").write(xml)
os.makedirs(f"{RES}/values", exist_ok=True)
open(f"{RES}/values/ic_launcher_background.xml", "w").write(
    f'<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">{hexbg}</color>\n</resources>\n')
print("Icons written, background", hexbg)
