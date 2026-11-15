# Vídeos da oferta "500 Atividades Bíblicas" (CODEX colecao, prioridades 2 e 3).
# 100% em código (PIL + ffmpeg, reaproveitando kit-natal/src/video*.py). Só a voz vem do ElevenLabs (Gabriel Geral),
# em out/criativos/videos/voz/<nome>.mp3. Uso: python colecao/src/video_colecao.py [vid-01 vid-02 vid-03 vid-04 vid-05]
import sys, pathlib, math, glob, subprocess, json
ROOT = pathlib.Path(__file__).resolve().parent.parent; REPO = ROOT.parent
sys.path.insert(0, str(REPO / "kit-natal" / "src"))
ARGS = sys.argv[1:]; sys.argv = [sys.argv[0], "47,90", "19,90"]
import video4 as V4
V, V3, N3 = V4.V, V4.V3, V4.N3
from PIL import Image, ImageDraw

DEST = ROOT / "out" / "criativos" / "videos"; (DEST / "voz").mkdir(parents=True, exist_ok=True)
V4.DEST = V3.DEST = DEST; V4.VOZ = DEST / "voz"
VIMG = ROOT / "out" / "vimg"; VIMG.mkdir(parents=True, exist_ok=True); V3.IMG = VIMG
W, H = V.W, V.H
NAVY, GOLD, RED, WHITE, GREEN = V.NAVY, V.GOLD, V.RED, V.WHITE, V4.GREEN
TIPOS = ["Caça-palavras", "Labirinto", "Código secreto", "Pinte por número", "Complete o versículo",
         "Verdadeiro ou falso", "Ligue as colunas", "Palavras embaralhadas", "Copie e ilustre", "Acróstico"]


def preparar():
    """Páginas reais (110 dpi) e capas em out/vimg: t0..t9 = um tipo de cada, capa1..5, pacote."""
    pg = ROOT / "out" / "pg110"
    if not pg.exists():
        import criativos_colecao; criativos_colecao.garantir_paginas()
    for t in range(10):
        Image.open(pg / f"c{1 + t % 5}-p{3 + t}.png").convert("RGB").save(VIMG / f"t{t}.png")
    for n in range(1, 6):
        Image.open(ROOT / "out" / "capas" / f"colecao-{n}.png").convert("RGB").save(VIMG / f"capa{n}.png")
    Image.open(ROOT / "out" / "capas" / "pacote-500.png").convert("RGB").save(VIMG / "pacote.png")


_c = {}
def im_(n, w):
    k = (n, w)
    if k not in _c:
        p = Image.open(VIMG / f"{n}.png").convert("RGB"); _c[k] = p.resize((w, int(p.height * w / p.width)), Image.BILINEAR)
    return _c[k]


def paste_rot(base, img, cx, cy, ang, border=GOLD):
    fr = Image.new("RGB", (img.width + 14, img.height + 14), border); fr.paste(img, (7, 7))
    r = fr.convert("RGBA").rotate(ang, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", r.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 110), (0, 0), r)
    base.paste(sh, (int(cx - r.width / 2 + 10), int(cy - r.height / 2 + 18)), sh)
    base.paste(r, (int(cx - r.width / 2), int(cy - r.height / 2)), r)


def leque(nomes, w, cy, spread, rot, s, top=None, linhas=()):
    """Leque de páginas/capas que abre na entrada e 'respira'; textos opcionais acima."""
    def f(t, s):
        im = V.bg(); d = ImageDraw.Draw(im)
        a = V.ease(s / .45); n = len(nomes)
        for k, nm in enumerate(nomes):
            o = k - (n - 1) / 2
            paste_rot(im, im_(nm, w), W / 2 + o * spread * a, cy + abs(o) * 20 + 6 * math.sin(s * 3 + k), -o * rot * a)
        d = ImageDraw.Draw(im)
        if top: V3.pill(d, 280, top, RED, WHITE, 50)
        y = 400
        for txt, fnt, cor, quando in linhas:
            if s >= quando: y = V.text_c(d, y, txt, fnt, cor)
            else: y += int(fnt.size * 1.08)
        return im
    return f


def num500():
    def f(t, s):
        im = leque(["t0", "t3", "t1", "t2", "t4"], 300, 1150, 150, 7, s)(t, s); d = ImageDraw.Draw(im)
        z = .6 + .4 * V.ease(s / .4) + .05 * t
        d.text((W / 2, 420), "500", font=V.B(int(260 * z)), fill=GOLD, anchor="mm")
        V.text_c(d, 580, "atividades bíblicas para imprimir", V.B(70), WHITE)
        return im
    return f


def conta(fase):
    """A conta real: 5 avulsas R$ 99,50 -> pacote R$ 47,90 -> economize R$ 51,60."""
    def f(t, s):
        im = V.bg(); d = ImageDraw.Draw(im)
        a = V.ease(s / .4)
        for k in range(5):
            x = 120 + k * 210; y = 420 + int((1 - a) * 120) + int(5 * math.sin(s * 3 + k))
            paste_rot(im, im_(f"capa{k + 1}", 170), x, y + 120, (k - 2) * 3)
        d = ImageDraw.Draw(im)
        d.text((W / 2, 300), "5 coleções avulsas", font=V.B(70), fill=WHITE, anchor="mm")
        y = 720
        d.text((W / 2, y), "R$ 99,50", font=V.B(110), fill=(255, 180, 168), anchor="ma")
        if fase >= 1:
            d.line([(W / 2 - 250, y + 66), (W / 2 + 250, y + 66)], fill=(255, 180, 168), width=10)
            p = V.ease(s / .35) if fase == 1 else 1
            paste_rot(im, im_("pacote", int(520 * (.7 + .3 * p))), W / 2, 1060, -3)
            d = ImageDraw.Draw(im)
            d.text((W / 2, 1290), "Pacote completo", font=V.B(66), fill=WHITE, anchor="ma")
            z = 1 + .05 * math.sin(s * 4)
            d.text((W / 2, 1360), "R$ 47,90", font=V.B(int(140 * z)), fill=GOLD, anchor="ma")
        if fase >= 2 and s > .3:
            V3.pill(d, 1560, "Economize R$ 51,60", GREEN, WHITE, 56)
        return im
    return f


def frase(l1, l2=None, cor2=GOLD, sz=110, pagina=None):
    def f(t, s):
        im = V.bg(); d = ImageDraw.Draw(im)
        if pagina: paste_rot(im, im_(pagina, 440), W / 2, 1290 + int((1 - V.ease(s / .4)) * 300), 4 * math.sin(s * 2))
        d = ImageDraw.Draw(im)
        V.star(d, W / 2, 360, 50 + 8 * math.sin(s * 5), GOLD)
        y = V.text_c(d, 470 - int(30 * t), l1, V.B(84), WHITE)
        if l2:
            z = .7 + .3 * V.ease(s / .4) + .04 * t
            y = V.text_c(d, y + 10, l2, V.B(int(sz * z)), cor2)
        return im
    return f


def cta(l1, l2):
    def f(t, s):
        im = V.bg(); d = ImageDraw.Draw(im)
        paste_rot(im, im_("pacote", int(V3.lerp(820, 900, t))), W / 2, 700, 0)
        d = ImageDraw.Draw(im)
        y = V.text_c(d, 1110, "500 atividades bíblicas por", V.B(70), WHITE)
        y = V.text_c(d, y, "R$ 47,90", V.B(int(V3.lerp(150, 165, t))), GOLD)
        if s > .3: V3.pill(d, y + 30, l1, WHITE, NAVY, 50)
        if s > .9: V3.pill(d, y + 130, l2, GOLD, NAVY, 56)
        return im
    return f


def tipo(k, z0=1.0, z1=1.1):
    return V3.show(f"t{k}", None, top=TIPOS[k], z0=z0, z1=z1, f0=(.5, .3), f1=(.5, .42))


def tela_papel():
    """Metade cinza (celular apagado) x metade com páginas reais."""
    def f(t, s):
        im = V.bg(); d = ImageDraw.Draw(im, "RGBA")
        d.rectangle([0, 0, W // 2, H], fill=(0, 0, 0, 110))
        x0, y0 = 120, 620 + int(8 * math.sin(s * 2))
        d.rounded_rectangle([x0, y0, x0 + 300, y0 + 600], 46, fill=(43, 47, 53), outline=(85, 91, 99), width=14)
        d.rounded_rectangle([x0 + 22, y0 + 22, x0 + 278, y0 + 578], 26, fill=(15, 15, 15))
        a = V.ease(s / .4)
        paste_rot(im, im_("t3", 330), 790, 820 + int((1 - a) * 300), -5)
        paste_rot(im, im_("t1", 330), 820, 1150 + int((1 - a) * 400), 6)
        d = ImageDraw.Draw(im)
        V.text_c(d, 300, "Menos tela.", V.B(110), WHITE)
        if s > .5: V.text_c(d, 430, "Mais Bíblia.", V.B(110), GOLD)
        V3.pill(d, 1500, "500 atividades para imprimir", WHITE, NAVY, 50)
        return im
    return f


S, HK = V3.show, V3.hook
VID1 = [
    ("Seu filho pediu o celular de novo?", [(1.8, HK("Seu filho pediu", "o celular", "de novo?", big_size=170, y0=640)), (1.8, tela_papel())], False),
    ("Entregue uma destas: caça-palavras, labirinto, pinte por número, código secreto.",
     [(1.4, tipo(0)), (1.4, tipo(1)), (1.4, tipo(3)), (1.4, tipo(2))], True),
    ("Quinhentas atividades bíblicas para imprimir. Cinquenta histórias, de Gênesis a Jesus, em dez tipos de atividade.",
     [(1.8, num500()), (1.6, tipo(4)), (1.6, tipo(6))], True),
    ("Cinco coleções avulsas saem por noventa e nove e cinquenta. O pacote completo sai por quarenta e sete e noventa.",
     [(1.8, conta(0)), (1.8, conta(1)), (1.8, conta(2))], False),
    ("Chega no seu e-mail em minutos. Toque em saiba mais.",
     [(1.6, cta("Chega no e-mail em minutos", "Toque em Saiba mais")), (1.6, cta("Pagamento único · 7 dias de garantia", "Toque em Saiba mais"))], False),
]
VID2 = [
    ("Quinhentas atividades bíblicas por quarenta e sete e noventa.", [(2.0, HK("500 atividades bíblicas", "R$ 47,90", "pagamento único", y0=620)),
      (1.6, leque(["t0", "t3", "t1", "t2", "t4"], 300, 1150, 150, 7, 0, linhas=[("500 atividades", V.B(110), GOLD, 0), ("por R$ 47,90", V.B(90), WHITE, 0)])),
      (1.4, leque(["capa1", "capa2", "capa3", "capa4", "capa5"], 330, 1150, 160, 6, 0, linhas=[("5 coleções", V.B(110), GOLD, 0), ("pagamento único", V.B(80), WHITE, 0)]))], False),
    ("Caça-palavras. Labirinto. Código secreto. Pinte por número. Complete o versículo. Verdadeiro ou falso. Ligue as colunas. Palavras embaralhadas. Copie e ilustre. E acróstico.",
     [(1.2, tipo(k)) for k in range(10)], False),
    ("Dá menos de dez centavos por atividade. Imprima hoje. Toque em saiba mais.",
     [(1.8, frase("Menos de", "R$ 0,10 por atividade", sz=104, pagina="t0")), (1.6, frase("Imprima", "hoje", sz=170, pagina="t3")),
      (1.8, cta("500 atividades · pagamento único", "Toque em Saiba mais"))], False),
]
# Prioridade 3: sem voz, só legenda (duração fixa)
VID3 = [(1.5, tipo(k)) for k in range(10)]
VID4 = [(2.0, frase("5 coleções avulsas", "R$ 99,50", cor2=(255, 180, 168))), (2.0, conta(0)), (2.0, conta(1)), (2.0, conta(2)),
        (2.0, frase("Menos de", "R$ 0,10 por atividade", sz=104, pagina="t0")), (2.0, cta("Pagamento único", "Toque em Saiba mais"))]
VID5 = [(2.0, HK("Seu filho pediu", "o celular", "de novo?", big_size=170, y0=640)), (2.0, tela_papel()), (2.0, tela_papel()),
        (1.5, tipo(0)), (1.5, tipo(3)), (1.5, tipo(1)), (2.0, num500()), (2.0, cta("Imprima hoje", "Toque em Saiba mais"))]


def mudo(nome, cenas, legendas):
    """Vídeo sem voz: trilha instrumental do kit e legenda queimada."""
    cenas = [(d, V4.legenda(fn, legendas[i]) if legendas[i] else fn) for i, (d, fn) in enumerate(cenas)]
    total = sum(d for d, _ in cenas)
    V3.render(nome + "-mudo", cenas)
    (DEST / f"{nome}-mudo-quadros.png").replace(DEST / f"{nome}-quadros.png")
    mw = DEST / "_trilha.wav"; N3.music(total, mw)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(DEST / f"{nome}-mudo.mp4"), "-i", str(mw), "-filter_complex",
                    "[1:a]volume=0.5,loudnorm=I=-16:TP=-1.5[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                    "-shortest", str(DEST / f"{nome}.mp4")], check=True)
    for f in [DEST / f"{nome}-mudo.mp4", mw]: f.unlink()
    print(nome, f"{total:.1f}s")


if __name__ == "__main__":
    preparar()
    quais = ARGS or ["vid-01", "vid-02", "vid-03", "vid-04", "vid-05"]
    if "vid-01" in quais: V4.build("vid-01-teatro-500", VID1)
    if "vid-02" in quais: V4.build("vid-02-preco-500", VID2)
    if "vid-03" in quais: mudo("vid-03-tipos", VID3, TIPOS)
    if "vid-04" in quais: mudo("vid-04-economia", VID4, ["5 coleções avulsas: R$ 99,50", "5 avulsas: R$ 99,50", "Pacote completo: R$ 47,90",
                                                          "Economize R$ 51,60", "Menos de R$ 0,10 por atividade", "Toque em Saiba mais"])
    if "vid-05" in quais: mudo("vid-05-telas", VID5, ["", "Menos tela. Mais Bíblia.", "Papel, lápis e a Palavra", "Caça-palavras", "Pinte por número",
                                                      "Labirinto", "50 histórias · 10 tipos de atividade", "R$ 47,90 · pagamento único"])
