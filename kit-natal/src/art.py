# Arte de linha original (SVG) para colorir e decorar. Traço grosso, formas simples.
import math, random

S = 'fill="none" stroke="#1d1d1d" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"'


def star_points(cx, cy, r1, r2, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        a = math.radians(rot + i * 180 / n)
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return " ".join(pts)


def estrela():
    return f'''<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
<polygon points="{star_points(200,190,150,62)}" {S}/>
<polygon points="{star_points(200,190,70,30)}" {S}/>
<path d="M200 355 v30 M120 360 l-15 20 M280 360 l15 20" {S}/>
<circle cx="70" cy="70" r="12" {S}/><circle cx="335" cy="60" r="9" {S}/><circle cx="345" cy="300" r="10" {S}/><circle cx="55" cy="290" r="8" {S}/>
</svg>'''


def anjo():
    return f'''<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
<ellipse cx="200" cy="58" rx="42" ry="12" {S}/>
<circle cx="200" cy="110" r="38" {S}/>
<path d="M183 108 q4 5 8 0 M209 108 q4 5 8 0 M188 126 q12 10 24 0" {S}/>
<path d="M200 150 L120 370 H280 Z" {S}/>
<path d="M170 180 C90 140 40 200 60 270 C100 250 130 240 160 230" {S}/>
<path d="M230 180 C310 140 360 200 340 270 C300 250 270 240 240 230" {S}/>
<path d="M150 260 L200 240 L250 260" {S}/>
<path d="M165 300 h70 M155 335 h90" {S}/>
</svg>'''


def manjedoura():
    return f'''<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
<polygon points="{star_points(200,55,40,16)}" {S}/>
<path d="M200 105 v25 M175 100 l-12 18 M225 100 l12 18" {S}/>
<path d="M80 210 H320 L290 290 H110 Z" {S}/>
<path d="M110 290 L70 380 M290 290 L330 380 M130 290 L250 380 M270 290 L150 380" {S}/>
<ellipse cx="200" cy="200" rx="80" ry="34" {S}/>
<circle cx="150" cy="182" r="26" {S}/>
<path d="M140 180 q4 4 8 0 M155 180 q4 4 8 0 M145 192 q6 5 12 0" {S}/>
<path d="M180 185 q40 -20 90 5 M190 205 q40 -10 80 5" {S}/>
<path d="M90 215 l-12 -18 M110 214 l-4 -22 M300 214 l8 -20 M318 216 l14 -16" {S}/>
</svg>'''


def presente():
    return f'''<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
<rect x="80" y="170" width="240" height="200" rx="10" {S}/>
<rect x="60" y="130" width="280" height="50" rx="10" {S}/>
<path d="M180 130 V370 M220 130 V370" {S}/>
<path d="M200 128 C150 60 90 90 130 125 Z" {S}/>
<path d="M200 128 C250 60 310 90 270 125 Z" {S}/>
<circle cx="200" cy="125" r="14" {S}/>
<polygon points="{star_points(120,260,26,11)}" {S}/>
<polygon points="{star_points(280,300,22,9)}" {S}/>
<circle cx="275" cy="225" r="10" {S}/><circle cx="130" cy="335" r="8" {S}/>
</svg>'''


def templo():
    return f'''<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
<path d="M50 140 L200 50 L350 140 Z" {S}/>
<rect x="60" y="140" width="280" height="24" {S}/>
<path d="M90 164 V330 M140 164 V330 M260 164 V330 M310 164 V330" {S}/>
<path d="M175 330 V240 Q200 215 225 240 V330" {S}/>
<rect x="45" y="330" width="310" height="22" {S}/>
<rect x="30" y="352" width="340" height="22" {S}/>
<circle cx="200" cy="110" r="14" {S}/>
</svg>'''


def pomba():
    return f'''<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
<path d="M120 220 C130 170 180 150 220 170 C250 140 300 130 340 150 C300 170 280 190 270 210 C300 230 300 270 260 280 C220 290 160 280 120 250 L60 270 L90 230 Z" {S}/>
<path d="M200 175 C170 110 120 80 80 90 C110 120 130 160 160 195" {S}/>
<circle cx="135" cy="215" r="5" fill="#1d1d1d"/>
<path d="M105 222 L80 228 L105 232" {S}/>
<path d="M60 340 q35 -25 70 0 t70 0 t70 0 t70 0" {S}/>
<path d="M90 375 q30 -20 60 0 t60 0 t60 0 t60 0" {S}/>
</svg>'''


def barco():
    return f'''<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
<path d="M60 230 H340 L300 300 H100 Z" {S}/>
<path d="M200 230 V60 L300 200 H200" {S}/>
<path d="M200 90 L120 200 H200" {S}/>
<path d="M40 330 q40 -25 80 0 t80 0 t80 0 t80 0" {S}/>
<path d="M90 370 c20 -18 50 -18 60 0 c-10 18 -40 18 -60 0 Z M150 370 l14 -10 v20 Z" {S}/>
<path d="M240 362 c20 -18 50 -18 60 0 c-10 18 -40 18 -60 0 Z M300 362 l14 -10 v20 Z" {S}/>
</svg>'''


def jarros():
    def j(x):
        return f'<path d="M{x-28} 150 h56 l-8 22 c40 30 40 150 0 190 h-72 c-40 -40 -40 -160 0 -190 Z" {S}/><path d="M{x-40} 250 h80" {S}/>'
    return f'''<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
{j(85)}{j(200)}{j(315)}
<path d="M185 95 q15 -30 30 0 q-15 25 -30 0 Z" {S}/>
<path d="M200 125 v10" {S}/>
</svg>'''


ART = {"estrela": estrela, "anjo": anjo, "manjedoura": manjedoura, "presente": presente,
       "templo": templo, "pomba": pomba, "barco": barco, "jarros": jarros}


def small_star(color="#E9B44C", size=28):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 100 100"><polygon points="{star_points(50,52,46,19)}" fill="{color}"/></svg>'


def maze(cols, rows, seed, cell=34, start_lbl="", end_lbl=""):
    rnd = random.Random(seed)
    walls = {(c, r): {"N", "S", "E", "W"} for c in range(cols) for r in range(rows)}
    seen = {(0, 0)}
    stack = [(0, 0)]
    D = {"N": (0, -1, "S"), "S": (0, 1, "N"), "E": (1, 0, "W"), "W": (-1, 0, "E")}
    while stack:
        c, r = stack[-1]
        opts = [(d, c + dx, r + dy, o) for d, (dx, dy, o) in D.items()
                if (c + dx, r + dy) in walls and (c + dx, r + dy) not in seen]
        if not opts:
            stack.pop(); continue
        d, nc, nr, o = rnd.choice(opts)
        walls[(c, r)].discard(d); walls[(nc, nr)].discard(o)
        seen.add((nc, nr)); stack.append((nc, nr))
    walls[(0, 0)].discard("W"); walls[(cols - 1, rows - 1)].discard("E")
    W, H = cols * cell, rows * cell
    lines = []
    for (c, r), ws in walls.items():
        x, y = c * cell, r * cell
        if "N" in ws: lines.append(f"M{x} {y}h{cell}")
        if "W" in ws: lines.append(f"M{x} {y}v{cell}")
        if "S" in ws and r == rows - 1: lines.append(f"M{x} {y+cell}h{cell}")
        if "E" in ws and c == cols - 1: lines.append(f"M{x+cell} {y}v{cell}")
        if "S" in ws and r < rows - 1: lines.append(f"M{x} {y+cell}h{cell}")
        if "E" in ws and c < cols - 1: lines.append(f"M{x+cell} {y}v{cell}")
    pad = 70
    return f'''<svg viewBox="{-pad} -10 {W + 2*pad} {H + 20}" xmlns="http://www.w3.org/2000/svg">
<path d="{' '.join(lines)}" fill="none" stroke="#1F3A5F" stroke-width="5" stroke-linecap="round"/>
<circle cx="{-pad/2}" cy="{cell/2}" r="22" fill="#E9B44C"/><text x="{-pad/2}" y="{cell/2+7}" text-anchor="middle" font-family="Baloo" font-size="20" font-weight="800" fill="#1F3A5F">INÍCIO</text>
<polygon points="{star_points(W + pad/2, H - cell/2, 30, 12)}" fill="#C0392B"/>
</svg>'''


def wordsearch(words, size, seed, diagonal=False):
    rnd = random.Random(seed)
    for _ in range(500):
        g = [[None] * size for _ in range(size)]
        dirs = [(1, 0), (0, 1)] + ([(1, 1)] if diagonal else [])
        placed = {}
        ok = True
        for w in sorted(words, key=len, reverse=True):
            for _try in range(300):
                dx, dy = rnd.choice(dirs)
                x = rnd.randrange(0, size - (len(w) - 1) * dx)
                y = rnd.randrange(0, size - (len(w) - 1) * dy)
                cells = [(x + i * dx, y + i * dy) for i in range(len(w))]
                if all(g[cy][cx] in (None, w[i]) for i, (cx, cy) in enumerate(cells)):
                    for i, (cx, cy) in enumerate(cells):
                        g[cy][cx] = w[i]
                    placed[w] = cells
                    break
            else:
                ok = False; break
        if ok:
            letters = "ABCDEFGHIJLMNOPRSTUV"
            for y in range(size):
                for x in range(size):
                    if g[y][x] is None:
                        g[y][x] = rnd.choice(letters)
            return g, placed
    raise RuntimeError("caça-palavras não coube")
