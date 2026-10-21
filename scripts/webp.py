# Genera versioni WebP responsive (800w, 1600w, originale) di ogni foto in assets/img/photos.
# Uso: python3 scripts/webp.py   (richiede Pillow)
from pathlib import Path
from PIL import Image

PHOTOS = Path(__file__).resolve().parent.parent / "assets/img/photos"
WIDTHS = (800, 1600)

for jpg in sorted(PHOTOS.glob("*.jpg")):
    img = Image.open(jpg).convert("RGB")
    for w in sorted({*WIDTHS, img.width}):
        if w > img.width:
            continue
        out = PHOTOS / (f"{jpg.stem}.webp" if w == img.width else f"{jpg.stem}-{w}.webp")
        im = img if w == img.width else img.resize((w, round(img.height * w / img.width)), Image.LANCZOS)
        im.save(out, "WEBP", quality=70, method=6)
        print(f"{out.name:32} {out.stat().st_size // 1024:5} KB")
