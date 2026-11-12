# Vídeos v5 (no estilo do video-teatro-v4, que vendeu): 2 ângulos novos, voz do ElevenLabs, trilha natalina ORIGINAL.
#   video-teatro-completo: ênfase no pacote Completo (janeiro + certificados + âncora R$ 44,70 -> R$ 29,90)
#   video-teatro-ensaio:   urgência do prazo ("faltam poucos domingos") + facilidade de ensaiar
# Entrada: out/v5/videos/voz/<nome>.mp3. Uso: python src/video5.py [essencial] [completo]
import sys, pathlib, math, wave
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import video4 as V4
V, V3, N3 = V4.V, V4.V3, V4.N3
from PIL import Image, ImageDraw

ESS, COMP = V4.ESS, V4.COMP
DEST = V.ROOT / "out/v5/videos"; (DEST / "voz").mkdir(parents=True, exist_ok=True)
V4.DEST = V3.DEST = DEST; V4.VOZ = DEST / "voz"
W, H, SR = V.W, V.H, 44100
NAVY, GOLD, RED, WHITE, GREEN = V.NAVY, V.GOLD, V.RED, V.WHITE, V4.GREEN


# ---------- trilha original: caixinha de música + guizos + baixo, 100 bpm, Dó maior (C–G–Am–F) ----------
def musica_natal(seconds, path, bpm=100):
    rng = np.random.default_rng(7)
    beat = 60 / bpm; n = int(seconds * SR); out = np.zeros(n + SR * 3)
    f = lambda m: 440 * 2 ** ((m - 69) / 12)
    chords = [[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]]
    def tone(freq, dur, decay, harm=(1, .35, .12)):
        t = np.arange(int(SR * dur)) / SR
        return sum(a * np.sin(2 * np.pi * freq * (k + 1) * t) for k, a in enumerate(harm)) * np.exp(-t * decay)
    def add(sig, at):
        p = int(at * SR); e = min(len(out), p + len(sig)); out[p:e] += sig[:e - p]
    bell = rng.standard_normal(int(.06 * SR)) * np.exp(-np.arange(int(.06 * SR)) / SR * 70)
    bell = np.diff(bell, prepend=0)  # passa-alta simples: som de guizo
    bar, k = 0.0, 0
    while bar * SR < n:
        ch = chords[k % 4]
        add(tone(f(ch[0] - 24), beat * 4, 1.2, (1, .2)) * .22, bar)                     # baixo
        for i, m in enumerate([ch[0] + 12, ch[2] + 12, ch[1] + 12, ch[2] + 12, ch[0] + 24, ch[2] + 12, ch[1] + 12, ch[2] + 12]):
            add(tone(f(m), 1.2, 3.5) * .13, bar + i * beat / 2)                         # caixinha de música
        for i in range(8):
            add(bell * (.05 if i % 2 else .09), bar + i * beat / 2)                      # guizos em colcheias
        bar += beat * 4; k += 1
    for d, g in [(.09, .3), (.19, .18), (.31, .1)]:
        s = int(d * SR); out[s:] += out[:-s] * g
    out = out[:n]; fi, fo = int(SR * .3), int(SR * 1.5)
    out[:fi] *= np.linspace(0, 1, fi); out[-fo:] *= np.linspace(1, 0, fo)
    out = out / np.max(np.abs(out)) * .6
    with wave.open(str(path), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())
N3.music = musica_natal


# ---------- cenas novas ----------
def bump(arquivo, top):
    """Imagem quadrada do produto (Janeiro Pronto, Certificados) entrando e com zoom lento."""
    src = Image.open(V.ROOT / "out" / arquivo).convert("RGB")
    def f(t, s):
        im = V.bg(); d = ImageDraw.Draw(im)
        z = 1 + .08 * t; w = int(960 * z); p = src.resize((w, w), Image.BILINEAR)
        c = (w - 960) // 2; p = p.crop((c, c, c + 960, c + 960))
        V.shadow_paste(im, p, W / 2 + int((1 - V.ease(s / .3)) * 400), 400 + 480)
        V.label(d, 280, top, RED, WHITE, 50)
        return im
    return f


def ancora():
    """Completo em destaque: preço separado riscado, preço do pacote e economia."""
    def f(t, s):
        im = V.bg(); d = ImageDraw.Draw(im)
        a = V.ease(s / .4); y = 300 + int((1 - a) * 200) + int(8 * math.sin(s * 3))
        d.rounded_rectangle([90, y, W - 90, y + 1100], 44, fill=WHITE, outline=GOLD, width=12)
        fb = V.B(44); tw = d.textlength("Recomendado", font=fb)
        d.rounded_rectangle([W / 2 - tw / 2 - 30, y - 38, W / 2 + tw / 2 + 30, y + 38], 34, fill=RED)
        d.text((W / 2, y), "Recomendado", font=fb, fill=WHITE, anchor="mm")
        d.text((W / 2, y + 70), "Pacote Completo", font=V.B(86), fill=NAVY, anchor="ma")
        yy = y + 200
        for it in ["Dezembro: 4 aulas + teatro", "Janeiro: + 4 aulas prontas", "Certificados e convites", "Uso para toda a equipe"]:
            d.line([(170, yy + 26), (184, yy + 42), (210, yy + 10)], fill=GREEN, width=8)
            d.text((235, yy), it, font=V.N(46), fill=NAVY); yy += 74
        if s > .5:
            txt = "Separado: R$ 44,70"; fs = V.N(50); tw = d.textlength(txt, font=fs)
            d.text((W / 2, yy + 30), txt, font=fs, fill=(120, 130, 140), anchor="ma")
            d.line([(W / 2 - tw / 2, yy + 62), (W / 2 + tw / 2, yy + 62)], fill=RED, width=6)
        if s > .9:
            z = 1 + .05 * math.sin(s * 4)
            d.text((W / 2, yy + 120), f"R$ {COMP}", font=V.B(int(150 * z)), fill=GREEN, anchor="ma")
        if s > 1.3: V.label(d, y + 1120 - 30, "Você economiza R$ 14,80", GOLD, NAVY, 50)
        return im
    return f


def cta2(l1, preco, l2, l3):
    """CTA com o preço escolhido (o V3.cta usa sempre o do Essencial)."""
    m = Image.open(V.ROOT / "out/img/mockup.png").convert("RGBA")
    def f(t, s):
        im = V.bg(); d = ImageDraw.Draw(im)
        mw = int(V3.lerp(980, 1080, t)); mm = m.resize((mw, int(m.height * mw / m.width)), Image.BILINEAR)
        im.paste(mm, (int((W - mw) / 2), 300), mm)
        y = V.text_c(d, 1040, l1, V.B(78), WHITE)
        y = V.text_c(d, y, f"R$ {preco}", V.B(int(V3.lerp(150, 165, t))), GOLD)
        if s > .5: V3.pill(d, y + 40, l2, WHITE, NAVY, 52)
        if s > 1.2: V3.pill(d, y + 150, l3, GOLD, NAVY, 56)
        return im
    return f


S, HK = V3.show, V3.hook
COMPLETO = [
    ("O culto de Natal está chegando, e as crianças ainda não têm apresentação?",
     [(3, HK("O culto de Natal está chegando…", "E a apresentação?", big_size=120))], False),
    ("O teatro já está pronto: O Presente Mais Esperado, com papel para todas as crianças.",
     [(1.8, S("teatro", None, top="Teatro pronto", z0=1.0, z1=1.1, f0=(.5, .1))),
      (1.8, S("teatro", None, top="Papel para todos", z0=1.35, z1=1.5, f0=(.3, .12), f1=(.3, .16)))], True),
    ("Mas não para no Natal.", [(1.5, HK("Mas não para", "no Natal.", big_size=150, y0=640))], False),
    ("No pacote Completo você leva dezembro e janeiro: oito aulas prontas, para começar o ano com Jesus.",
     [(3, bump("bump-janeiro-pronto.png", "+ Janeiro Pronto"))], True),
    ("E ainda os certificados e convites para a festa de Natal, com uso liberado para toda a equipe da igreja.",
     [(3, bump("bump-certificados-convites.png", "+ Certificados e Convites"))], True),
    ("Separado, tudo isso sairia quarenta e quatro e setenta. No Completo, vinte e nove e noventa.", [(4, ancora())], False),
    ("Sete dias de garantia. Toque em saiba mais e escolha o Completo.",
     [(3.5, cta2("Dezembro + janeiro por", COMP, "7 dias de garantia", "Escolha o Completo"))], False),
]
ENSAIO = [
    ("Faltam poucos domingos para o Natal, e o teatro das crianças nem começou?",
     [(3, HK("Faltam poucos domingos para o Natal…", "E o teatro nem começou?", big_size=110))], False),
    ("Dá tempo. O roteiro já está escrito, e dá para ensaiar em dois domingos.",
     [(1.2, HK("Calma,", "dá tempo.", big_size=150, y0=640)), (2.2, S("teatro", None, top="Roteiro pronto", z0=1.0, z1=1.1, f0=(.5, .1)))], True),
    ("Falas curtas, fáceis de decorar, e figurino com lençol, toalha e papel dourado.",
     [(1.8, S("teatro", None, top="Falas curtas", z0=1.35, z1=1.5, f0=(.3, .45), f1=(.3, .55))),
      (1.8, S("teatro", None, top="Figurino simples", z0=1.35, z1=1.5, f0=(.3, .12), f1=(.3, .16)))], True),
    ("Até as crianças de três anos participam, como ovelhas e coro de anjos.",
     [(2.6, HK("Até as crianças de 3 anos", "participam!", "como ovelhas e coro de anjos", big_size=130, y0=600))], False),
    ("E junto vêm quatro aulas de Natal, atividades por idade e lembrancinhas.",
     [(1.2, S("aula", None, top="4 aulas de Natal", f0=(.5, .2), f1=(.5, .4))), (1.2, S("colorir", None, top="Atividades por idade")),
      (1.2, S("cartao", None, top="Lembrancinhas"))], True),
    ("Escolha o Essencial, por dezenove e noventa, ou o Completo, que já traz as aulas de janeiro.", [(4, V4.pacotes("Escolha o seu pacote"))], False),
    ("Toque em saiba mais e comece a ensaiar neste domingo.",
     [(3, V3.cta("Comece a ensaiar neste domingo", "7 dias de garantia", "Toque em Saiba mais"))], False),
]

if __name__ == "__main__":
    V4.build("video-teatro-completo", COMPLETO)
    V4.build("video-teatro-ensaio", ENSAIO)
