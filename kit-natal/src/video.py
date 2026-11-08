# Gera os vídeos verticais (1080x1920, 30 fps) a partir das páginas do kit.
import math, pathlib, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
PG = ROOT / "out/video/pg"; OUT = ROOT / "out"
W, H, FPS = 1080, 1920, 30
NAVY, GOLD, RED, WHITE = (31, 58, 95), (233, 180, 76), (192, 57, 43), (255, 255, 255)
B = lambda s: ImageFont.truetype(str(ROOT / "fonts/baloo-2-latin-800-normal.ttf"), s)
N = lambda s: ImageFont.truetype(str(ROOT / "fonts/nunito-latin-700-normal.ttf"), s)
_cache = {}


def page(n, w):
    k = (n, w)
    if k not in _cache:
        im = Image.open(PG / f"p{n}.png").convert("RGB")
        im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
        _cache[k] = im
    return _cache[k]


def ease(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3


def text_c(d, y, txt, font, fill, maxw=940, lh=1.08):
    words, lines, cur = txt.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w_
    lines.append(cur)
    for ln in lines:
        d.text((W / 2, y), ln, font=font, fill=fill, anchor="ma"); y += int(font.size * lh)
    return y


def star(d, cx, cy, r, fill):
    pts = [(cx + (r if i % 2 == 0 else r * .42) * math.cos(math.radians(-90 + i * 36)),
            cy + (r if i % 2 == 0 else r * .42) * math.sin(math.radians(-90 + i * 36))) for i in range(10)]
    d.polygon(pts, fill=fill)


def bg():
    im = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(im)
    for x, y, r in [(120, 160, 14), (940, 260, 10), (980, 1500, 16), (90, 1700, 9), (860, 1780, 12), (160, 1180, 7)]:
        star(d, x, y, r, GOLD)
    return im


def shadow_paste(base, card, x, y, rot=0):
    pad = 40
    c = Image.new("RGBA", (card.width + pad * 2, card.height + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", c.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle([pad, pad + 14, pad + card.width, pad + card.height + 14], fill=(0, 0, 0, 120))
    c = Image.alpha_composite(c, sh.filter(ImageFilter.GaussianBlur(18))); c.paste(card, (pad, pad))
    ImageDraw.Draw(c).rectangle([pad, pad, pad + card.width - 1, pad + card.height - 1], outline=GOLD, width=6)
    if rot: c = c.rotate(rot, expand=True, resample=Image.BICUBIC)
    base.paste(c, (int(x - c.width / 2), int(y - c.height / 2)), c)


def label(d, y, txt, color=GOLD, tc=NAVY, size=54):
    f = B(size); tw = d.textlength(txt, font=f)
    d.rounded_rectangle([W / 2 - tw / 2 - 36, y - 10, W / 2 + tw / 2 + 36, y + size + 18], 40, fill=color)
    d.text((W / 2, y), txt, font=f, fill=tc, anchor="ma")


# --- cenas: cada cena é (duração_s, função(t_local 0..1, segundos) -> Image)
def hook(l1, l2, sub=None):
    def f(t, s):
        im = bg(); d = ImageDraw.Draw(im); a = ease(s / .6)
        y = 640 - int(60 * (1 - a))
        star(d, W / 2, y - 140, 90 * a + 1, GOLD)
        y = text_c(d, y, l1, B(96), WHITE)
        y = text_c(d, y + 10, l2, B(150), GOLD)
        if sub: text_c(d, y + 30, sub, N(48), WHITE)
        return im
    return f


def show(n, cap, top=None, zoom=(1.0, 1.08), focus=.5, w=860):
    def f(t, s):
        im = bg(); d = ImageDraw.Draw(im)
        z = zoom[0] + (zoom[1] - zoom[0]) * t
        p = page(n, int(w * z))
        slide = ease(s / .35)
        y = H / 2 + 40 + int((1 - slide) * 300)
        if p.height * 1 > 1500:  # recorte vertical com foco
            ch = 1450; top_y = int((p.height - ch) * focus); p = p.crop((0, top_y, p.width, top_y + ch))
        shadow_paste(im, p, W / 2, y)
        if top: label(d, 120, top, RED, WHITE, 50)
        if cap: label(d, H - 220, cap)
        return im
    return f


def cta(l1, price, l3):
    def f(t, s):
        im = bg(); d = ImageDraw.Draw(im)
        m = Image.open(OUT / "img/mockup.png").convert("RGBA"); m = m.resize((1060, int(m.height * 1060 / m.width)))
        im.paste(m, (10, 260), m)
        y = text_c(d, 1110, l1, B(76), WHITE)
        y = text_c(d, y + 10, price, B(170), GOLD)
        if s > .6: label(d, y + 40, l3, GOLD, NAVY, 58)
        return im
    return f


def render(name, scenes):
    out = OUT / f"{name}.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "20", "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    total = 0
    for dur, fn in scenes:
        nf = int(dur * FPS)
        for i in range(nf):
            p.stdin.write(fn(i / max(1, nf - 1), i / FPS).tobytes())
        total += dur
    p.stdin.close(); p.wait(); print(name, f"{total:.1f}s")


V1 = [
    (2.8, hook("O dezembro inteiro do ministério infantil", "PRONTO.")),
    (1.7, show(1, "4 aulas de Natal")),
    (1.7, show(4, "Plano de cada domingo", focus=.2)),
    (1.7, show(5, "História pronta para contar", focus=.25)),
    (1.5, show(7, "Colorir · 3 a 5 anos")),
    (1.5, show(8, "Labirinto · 3 a 8 anos")),
    (1.5, show(9, "Caça-palavras · 6 a 11 anos")),
    (1.7, show(32, "Teatro do culto de Natal", focus=.2)),
    (1.5, show(34, "Cartões lembrancinha")),
    (1.5, show(35, "Marcadores com versículos")),
    (3.8, cta("4 aulas + teatro + lembrancinhas", "R$ 19,90", "Toque em Saiba mais")),
]
V3 = [
    (2.8, hook("Olha como fica uma aula do", "Kit de Natal", "Aula 1 · O anjo visita Maria")),
    (3.2, show(4, "Verdade, versículo e materiais", top="1 · Planejamento", focus=.05)),
    (3.0, show(4, "Dinâmica de abertura pronta", top="2 · Acolhida", focus=.95, zoom=(1.15, 1.25))),
    (3.4, show(5, "É só ler e contar", top="3 · História", focus=.3)),
    (3.2, show(6, "Perguntas por idade", top="4 · Conversa", focus=.15)),
    (2.2, show(7, "3 a 5 anos", top="5 · Atividade")),
    (2.0, show(8, "3 a 8 anos", top="5 · Atividade")),
    (2.0, show(9, "6 a 11 anos", top="5 · Atividade")),
    (2.0, show(10, "9 a 11 anos", top="5 · Atividade")),
    (2.6, hook("São 4 aulas assim", "+ teatro", "e lembrancinhas para o culto de Natal")),
    (3.8, cta("Seu dezembro pronto por", "R$ 19,90", "Toque em Saiba mais")),
]

if __name__ == "__main__":
    render("video-1-folheando-o-kit", V1)
    render("video-3-uma-aula-do-kit", V3)
