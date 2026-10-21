"""Genera immagini segnaposto (SVG) in stile "bozzetto" con i colori Monterra.
Uso: python3 scripts/make_placeholders.py
Le foto reali vanno in assets/img/photos/<nome>.jpg e sostituiscono automaticamente il segnaposto.
"""
import math, random, os

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img", "placeholders")

IMAGES = {
    # nome: (larghezza, altezza, palette)
    "hero":               (2400, 1500, "dawn"),
    "territorio":         (2400, 1300, "day"),
    "service-trail":      (1600, 1200, "forest"),
    "service-destination":(1600, 1200, "day"),
    "service-events":     (1600, 1200, "dusk"),
    "service-consulting": (1600, 1200, "fog"),
    "process":            (2400, 1100, "dusk"),
    "trail-hero":         (2400, 1500, "forest"),
    "trail-1":            (1400, 1750, "dawn"),
    "trail-2":            (1400, 1750, "fog"),
    "destination-hero":   (2400, 1400, "day"),
    "destination-1":      (1600, 1100, "dusk"),
    "contact":            (2400, 1400, "fog"),
}

PALETTES = {
    "dawn":   ["#f4f1eb", "#e3d7c3", "#c7b79c", "#9a6a3a", "#5d5a44", "#314238", "#1f2a24"],
    "day":    ["#eef0ea", "#dcd5c6", "#c7b79c", "#8c8a6c", "#4d5f4f", "#314238", "#1f2a24"],
    "forest": ["#e8e6dc", "#c9c4ae", "#8f937a", "#5d6b59", "#3f5245", "#314238", "#1b241f"],
    "dusk":   ["#e9dccb", "#d4b995", "#b58a5a", "#9a6a3a", "#5a4632", "#314238", "#1f1f1f"],
    "fog":    ["#f4f1eb", "#e6e2d8", "#cfc8b8", "#b0a893", "#7c7c6c", "#4d5a50", "#314238"],
}

def ridge(rng, w, h, base, amp, rough):
    pts, x = [], -50
    phase = rng.random() * 10
    while x <= w + 50:
        y = base - amp * (0.55 * math.sin(x / w * math.pi * rng.uniform(1.2, 2.4) + phase)
                          + 0.35 * math.sin(x / w * math.pi * 5.3 + phase * 2)) \
            - rng.uniform(-rough, rough)
        pts.append((x, y))
        x += rng.uniform(w / 40, w / 18)
    d = f"M-50,{h+10} " + " ".join(f"L{x:.0f},{y:.0f}" for x, y in pts) + f" L{w+50},{h+10} Z"
    return d

def trail(rng, w, h):
    # sentiero serpeggiante (richiama il logo)
    y0 = h * 0.62
    pts = []
    for i in range(7):
        t = i / 6
        x = w * (0.08 + 0.84 * t)
        y = y0 + h * 0.28 * t + (h * 0.07 if i % 2 else -h * 0.07)
        pts.append((x, y))
    d = f"M{pts[0][0]:.0f},{pts[0][1]:.0f} "
    for a, b in zip(pts, pts[1:]):
        cx = (a[0] + b[0]) / 2
        d += f"C{cx:.0f},{a[1]:.0f} {cx:.0f},{b[1]:.0f} {b[0]:.0f},{b[1]:.0f} "
    return d

def make(name, w, h, pal_name):
    rng = random.Random(name)
    p = PALETTES[pal_name]
    layers = []
    n = 5
    for i in range(n):
        base = h * (0.38 + i * 0.12)
        amp = h * (0.16 - i * 0.02)
        layers.append(f'<path d="{ridge(rng, w, h, base, amp, h*0.015)}" fill="{p[i+2]}"/>')
    sun_x, sun_y, sun_r = w * rng.uniform(0.6, 0.85), h * rng.uniform(0.16, 0.28), h * 0.07
    label = f"FOTO · {name}.jpg"
    size = f"{w} × {h}"
    fs = h * 0.022
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{p[0]}"/><stop offset="1" stop-color="{p[1]}"/></linearGradient>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.09 0"/></filter>
</defs>
<rect width="{w}" height="{h}" fill="url(#sky)"/>
<circle cx="{sun_x:.0f}" cy="{sun_y:.0f}" r="{sun_r:.0f}" fill="#f4f1eb" opacity="0.7"/>
{chr(10).join(layers)}
<path d="{trail(rng, w, h)}" fill="none" stroke="#9a6a3a" stroke-width="{h*0.028:.0f}" stroke-linecap="round" opacity="0.85"/>
<rect width="{w}" height="{h}" filter="url(#grain)"/>
<g font-family="Helvetica, Arial, sans-serif" fill="#f4f1eb" opacity="0.85">
<text x="{w*0.03:.0f}" y="{h - h*0.05:.0f}" font-size="{fs:.0f}" letter-spacing="{fs*0.15:.1f}">{label}</text>
<text x="{w*0.03:.0f}" y="{h - h*0.05 + fs*1.5:.0f}" font-size="{fs*0.75:.0f}" opacity="0.7">{size}</text>
</g>
</svg>'''
    with open(os.path.join(OUT, f"{name}.svg"), "w") as f:
        f.write(svg)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, (w, h, pal) in IMAGES.items():
        make(name, w, h, pal)
    print(f"{len(IMAGES)} segnaposto generati in {os.path.abspath(OUT)}")
