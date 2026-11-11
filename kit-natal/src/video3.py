# Vídeos v3 (1080x1920, 30 fps, H.264, sem áudio). Reaproveita src/video.py.
# Uso: python src/video3.py "19,90"  ->  out/v3/videos/video-preco.mp4, video-teatro.mp4 e as folhas de quadros
# Área segura: todo texto entre y=250 e y=1670. Toda cena tem movimento contínuo (zoom/pan) e o 1º quadro já tem texto.
import sys, pathlib, subprocess
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import video as V
from PIL import Image, ImageDraw

PRECO = sys.argv[1] if len(sys.argv) > 1 else "19,90"
IMG = V.OUT / "img"; DEST = V.OUT / "v3/videos"; DEST.mkdir(parents=True, exist_ok=True)
W, H, FPS = V.W, V.H, V.FPS
_c = {}


def src(n):
    if n not in _c: _c[n] = Image.open(IMG / f"{n}.png").convert("RGB")
    return _c[n]


def lerp(a, b, t): return a + (b - a) * t


def pill(d, y, txt, color=V.GOLD, tc=V.NAVY, size=54):
    V.label(d, y, txt, color, tc, size)


def hook(l1, big=None, sub=None, y0=560, big_size=190):
    """Texto já visível no 1º quadro; o destaque (preço) entra com zoom de 60% a 100%, depois 'respira'."""
    def f(t, s):
        im = V.bg(); d = ImageDraw.Draw(im)
        V.star(d, W / 2, y0 - 120, 60 + 30 * V.ease(s / .5), V.GOLD)
        y = V.text_c(d, y0 - int(30 * (1 - V.ease(s / .4))), l1, V.B(92), V.WHITE)
        if big:
            z = .6 + .4 * V.ease(s / .5) + .04 * t  # zoom de entrada + leve crescimento contínuo
            layer = Image.new("RGBA", (W, 400), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
            ld.text((W / 2, 200), big, font=V.B(int(big_size * z)), fill=V.GOLD, anchor="mm")
            im.paste(layer, (0, y - 60), layer); y += 300
        if sub: V.text_c(d, y + 10, sub, V.N(50), V.WHITE)
        return im
    return f


def show(n, cap, top=None, z0=1.0, z1=1.12, f0=(.5, .5), f1=None, win=(860, 1080)):
    """Página real com zoom/pan contínuo. Janela visível win=(largura, altura); foco f=(x,y) em frações da página."""
    f1 = f1 or f0
    def f(t, s):
        im = V.bg(); d = ImageDraw.Draw(im)
        z = lerp(z0, z1, t); fx, fy = lerp(f0[0], f1[0], t), lerp(f0[1], f1[1], t)
        p = src(n); sw = int(win[0] * z); p = p.resize((sw, int(p.height * sw / p.width)), Image.BILINEAR)
        ww, wh = min(win[0], p.width), min(win[1], p.height)
        x0 = int(max(0, min(p.width - ww, fx * p.width - ww / 2))); y0 = int(max(0, min(p.height - wh, fy * p.height - wh / 2)))
        card = p.crop((x0, y0, x0 + ww, y0 + wh))
        slide = V.ease(s / .3)
        V.shadow_paste(im, card, W / 2 + int((1 - slide) * 400), 400 + 1080 / 2)
        if top: pill(d, 280, top, V.RED, V.WHITE, 50)
        if cap: pill(d, 1520, cap)
        return im
    return f


def cta(l1, l2, l3):
    """Mockup com zoom contínuo + linhas que entram em sequência."""
    m = Image.open(IMG / "mockup.png").convert("RGBA")
    def f(t, s):
        im = V.bg(); d = ImageDraw.Draw(im)
        mw = int(lerp(980, 1080, t)); mm = m.resize((mw, int(m.height * mw / m.width)), Image.BILINEAR)
        im.paste(mm, (int((W - mw) / 2), 300), mm)
        y = V.text_c(d, 1040, l1, V.B(78), V.WHITE)
        y = V.text_c(d, y, f"R$ {PRECO}", V.B(int(lerp(150, 165, t))), V.GOLD)
        if s > .5: pill(d, y + 40, l2, V.WHITE, V.NAVY, 52)
        if s > 1.2: pill(d, y + 150, l3, V.GOLD, V.NAVY, 56)
        return im
    return f


def render(name, scenes):
    out = DEST / f"{name}.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "20", "-movflags", "+faststart", str(out)],
                         stdin=subprocess.PIPE)
    frames, k = [], 0
    for dur, fn in scenes:
        nf = int(round(dur * FPS))
        for i in range(nf):
            fr = fn(i / max(1, nf - 1), i / FPS)
            if k % (2 * FPS) == 0: frames.append((k / FPS, fr.resize((270, 480))))
            p.stdin.write(fr.tobytes()); k += 1
    p.stdin.close(); p.wait()
    # folha de quadros a cada 2 s
    cols = 6; rows = (len(frames) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 280 + 10, rows * 520 + 10), "white"); d = ImageDraw.Draw(sheet)
    for i, (ts, fr) in enumerate(frames):
        x, y = 10 + (i % cols) * 280, 10 + (i // cols) * 520
        sheet.paste(fr, (x, y)); d.text((x, y + 485), f"{ts:.0f} s", font=V.N(24), fill="black")
    sheet.save(DEST / f"{name}-quadros.png")
    print(name, f"{k / FPS:.1f}s")


PRECO_V = [
    (2.0, hook("Dezembro inteiro do ministério infantil", f"R$ {PRECO}", "4 aulas de Natal prontas")),
    (1.5, show("aula", "4 aulas completas", f0=(.5, .2), f1=(.5, .45))),
    (1.5, show("historia", "História pronta para contar", f0=(.5, .25), f1=(.5, .4))),
    (1.5, show("colorir", "Colorir · 3 a 5 anos")),
    (1.5, show("labirinto", "Labirinto · 3 a 8 anos")),
    (1.5, show("cacapalavras", "Caça-palavras · 6 a 11 anos")),
    (1.5, show("teatro", "Teatro do culto de Natal", f0=(.5, .2), f1=(.5, .4))),
    (1.5, show("cartao", "Cartões lembrancinha")),
    (1.5, show("marcadores", "Marcadores com versículos")),
    (6.0, cta("Menos de R$ 5 por domingo", "Baixe e imprima hoje", "Toque em Saiba mais")),
]

TEATRO_V = [
    (2.4, hook("Pediram um teatro de Natal para as crianças?", "Já está escrito.", "Roteiro completo, pronto para ensaiar", y0=560, big_size=130)),
    (2.0, show("teatro", "8 a 10 minutos", top="O Presente Mais Esperado", z0=1.0, z1=1.1, f0=(.5, .1))),
    (2.0, show("teatro", "Falas curtas, fáceis de decorar", top="Roteiro completo", z0=1.35, z1=1.5, f0=(.3, .45), f1=(.3, .55))),
    (2.0, show("teatro", "Figurino com o que tem em casa", top="Personagens e figurino", z0=1.35, z1=1.5, f0=(.3, .12), f1=(.3, .16))),
    (2.0, hook("Papel para todas as crianças,", None, "até as de 3 anos (ovelhas e coro de anjos)", y0=660)),
    (1.5, show("aula", "E mais 4 aulas de Natal", f0=(.5, .2), f1=(.5, .4))),
    (1.5, show("historia", "Histórias prontas para contar", f0=(.5, .25), f1=(.5, .4))),
    (1.5, show("colorir", "16 atividades por idade")),
    (1.5, show("cartao", "Lembrancinhas para o culto")),
    (5.0, cta("Teatro + 4 aulas + lembrancinhas", "Menos de R$ 5 por domingo", "Toque em Saiba mais")),
]

if __name__ == "__main__":
    render("video-preco", PRECO_V)
    render("video-teatro", TEATRO_V)
