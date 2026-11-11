# VSL horizontal 1920x1080 COM narração (Kokoro TTS offline, voz pf_dora) + trilha suave.
# A duração de cada cena se ajusta à fala. Uso: python3 src/vsl_h.py
# Requer: pip install kokoro-onnx soundfile ; modelo em /tmp/kk/kokoro.onnx e voices.bin
#   (https://huggingface.co/fastrtc/kokoro-onnx/resolve/main/kokoro-v1.0.onnx e voices-v1.0.bin)
import sys, pathlib, subprocess, wave
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import video as V
from narracao3 import music  # mesma trilha de caixinha de música  # noqa
from PIL import Image, ImageDraw

W, H, FPS, SR = 1920, 1080, 30, 44100
NAVY, GOLD, RED, WHITE = V.NAVY, V.GOLD, V.RED, V.WHITE
B, N, ease, star = V.B, V.N, V.ease, V.star
OUT = V.OUT; IMG = OUT / "img"; TMP = OUT / "_vslh"; TMP.mkdir(exist_ok=True)
KK = pathlib.Path("/tmp/kk")
_c = {}


def page(n, h):
    if (n, h) not in _c:
        im = Image.open(IMG / f"{n}.png").convert("RGB"); _c[(n, h)] = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    return _c[(n, h)]


def bg():
    im = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(im)
    for x, y, r in [(110, 110, 14), (1800, 140, 11), (1840, 960, 15), (80, 980, 9), (980, 1020, 8), (1000, 60, 7)]:
        star(d, x, y, r, GOLD)
    return im


def lines(d, txt, font, maxw):
    out, cur = [], ""
    for w_ in txt.split():
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: out.append(cur); cur = w_
    return out + [cur]


def text(d, x, y, txt, font, fill, maxw, anchor="ma", lh=1.1):
    for ln in lines(d, txt, font, maxw):
        d.text((x, y), ln, font=font, fill=fill, anchor=anchor); y += int(font.size * lh)
    return y


def pill(d, x, y, txt, color, tc, size, anchor="l"):
    f = B(size); tw = d.textlength(txt, font=f)
    x0 = x if anchor == "l" else x - tw / 2 - 34
    d.rounded_rectangle([x0, y - 8, x0 + tw + 68, y + size + 16], 36, fill=color)
    d.text((x0 + 34, y), txt, font=f, fill=tc)


def hook(l1, l2, sub=None):
    def f(t, s):
        im = bg(); d = ImageDraw.Draw(im); a = ease(s / .6)
        h1, h2 = lines(d, l1, B(84), 1500), lines(d, l2, B(130), 1600)
        tot = len(h1) * 92 + len(h2) * 143 + (70 if sub else 0)
        y = (H - tot) / 2 + 50 - int(50 * (1 - a))
        star(d, W / 2, y - 110, 70 * a + 1, GOLD)
        y = text(d, W / 2, y, l1, B(84), WHITE, 1500)
        y = text(d, W / 2, y + 6, l2, B(130), GOLD, 1600)
        if sub: text(d, W / 2, y + 24, sub, N(46), WHITE, 1500)
        return im
    return f


def show(n, cap, top, focus=.0):
    def f(t, s):
        im = bg(); d = ImageDraw.Draw(im)
        z = 1 + .10 * t; ph = int(900 * z); p = page(n, ph)
        if ph > 900:  # zoom lento com recorte, foco vertical
            oy = int((ph - 900) * focus); ox = (p.width - int(p.width * 900 / ph)) // 2
            p = p.crop((ox, oy, p.width - ox, oy + 900))
        sl = ease(s / .4); cx = 1340 + int((1 - sl) * 300)
        V.shadow_paste(im, p, cx, H / 2)
        pill(d, 120, 330, top, RED, WHITE, 46)
        text(d, 120, 440, cap, B(78), WHITE, 760, anchor="la")
        return im
    return f


def oferta(nome, desc, preco, extra=None, destaque=False):
    def f(t, s):
        im = bg(); d = ImageDraw.Draw(im)
        m = Image.open(IMG / "mockup.png").convert("RGBA"); m = m.resize((900, int(m.height * 900 / m.width)))
        im.paste(m, (1000, (H - m.height) // 2 + 20), m)
        if destaque: pill(d, 120, 210, "Recomendado", GOLD, NAVY, 40)
        y = text(d, 120, 300, nome, B(76), GOLD, 860, anchor="la")
        y = text(d, 120, y + 6, desc, N(44), WHITE, 860, anchor="la", lh=1.25)
        a = ease((s - .3) / .5)
        if a > 0:
            y = text(d, 120, y + 30, preco, B(int(150 * (.6 + .4 * a))), GOLD, 900, anchor="la")
            if extra: text(d, 120, y + 6, extra, N(44), WHITE, 860, anchor="la")
        return im
    return f


# (fala, cena) — a cena dura o tempo da fala + folga
ROTEIRO = [
    ("Professora do ministério infantil, isto é pra você.", hook("Professora do ministério infantil,", "isto é pra você", "assista até o fim"), .3),
    ("Dezembro chegando, e a aula de Natal ainda não está pronta?", hook("Dezembro chegando e a aula de Natal", "ainda não está pronta?"), .3),
    ("Sábado, onze da noite, procurando atividade na internet, de novo?", hook("Sábado, 23h, procurando atividade na internet", "de novo?"), .3),
    ("Crianças de três e de dez anos na mesma sala, e nada serve para as duas idades.", hook("Crianças de 3 e de 10 anos na mesma sala", "e nada serve", "para as duas idades"), .3),
    ("E ainda pediram um teatro para o culto de Natal.", hook("E ainda pediram um teatro", "para o culto de Natal"), .3),
    ("E se o mês inteiro já estivesse pronto?", hook("E se o mês inteiro", "já estivesse pronto?"), .5),
    ("São quatro aulas de Natal, com o plano de cada domingo.", show("aula", "Plano de cada domingo, 40 minutos", "4 aulas de Natal", .1), .3),
    ("A história vem pronta. É só ler e contar.", show("historia", "É só ler e contar", "História pronta", .2), .3),
    ("Atividades para colorir,", show("colorir", "Colorir · 3 a 5 anos", "Atividade por idade"), .1),
    ("labirinto,", show("labirinto", "Labirinto · 3 a 8 anos", "Atividade por idade"), .2),
    ("e caça-palavras, separadas por idade, de três a onze anos.", show("cacapalavras", "Caça-palavras · 6 a 11 anos", "Atividade por idade"), .3),
    ("E o teatro do culto de Natal vem pronto, com papel para todas as crianças.", show("teatro", "Papel para todas as crianças", "Teatro de Natal", .1), .3),
    ("E lembrancinhas: cartões, marcadores e estrela de porta.", show("cartao", "Cartões, marcadores e estrela de porta", "Lembrancinhas"), .3),
    ("Você imprime em casa, em papel A4 comum, abre o plano e dá aula.", hook("Você imprime em casa,", "abre o plano e dá aula", "Papel A4 comum"), .4),
    ("No pacote essencial, o kit de Natal sai por dezenove e noventa.",
     oferta("Pacote Essencial", "Kit de Natal: 4 aulas, histórias, 16 atividades, teatro e lembrancinhas", "R$ 19,90"), .5),
    ("No pacote completo, você leva também o Janeiro Pronto e os certificados e convites de Natal, por vinte e nove e noventa. Comprando separado, daria quarenta e quatro reais e setenta centavos.",
     oferta("Pacote Completo", "Kit de Natal + Janeiro Pronto + Certificados e Convites", "R$ 29,90", "valem R$ 44,70 separados", True), .6),
    ("Você tem sete dias de garantia. Se não servir, devolvemos cem por cento.", hook("7 dias de garantia", "risco zero", "não serviu, devolvemos 100%"), .4),
    ("Escolha o seu pacote logo abaixo e receba o acesso na hora, no seu e-mail.", hook("Escolha seu pacote", "logo abaixo", "acesso imediato no seu e-mail"), 1.2),
]


def tts_all():
    from kokoro_onnx import Kokoro
    import soundfile as sf
    k = Kokoro(str(KK / "kokoro.onnx"), str(KK / "voices.bin")); res = []
    for i, (fala, _, _) in enumerate(ROTEIRO):
        a, sr = k.create(fala, voice="pf_dora", speed=1.08, lang="pt-br")
        raw = TMP / f"f{i}.wav"; wav = TMP / f"f{i}-44.wav"; sf.write(raw, a, sr)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-af",
                        "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse",
                        "-ar", str(SR), "-ac", "1", str(wav)], check=True)
        with wave.open(str(wav)) as w: res.append((wav, w.getnframes() / SR))
    return res


def main(name="vsl-kit-natal-h"):
    falas = tts_all(); LEAD = .2; t = LEAD; cenas, pos = [], []
    for (wav, d), (_, cena, folga) in zip(falas, ROTEIRO):
        dur = d + folga + (LEAD if not cenas else 0); cenas.append((max(1.0, dur), cena))
        pos.append((wav, t)); t += max(1.0, dur) - (LEAD if len(cenas) == 1 else 0)
    total = sum(s for s, _ in cenas)
    mudo = TMP / "mudo.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "23", str(mudo)], stdin=subprocess.PIPE)
    for dur, fn in cenas:
        nf = int(round(dur * FPS))
        for i in range(nf): p.stdin.write(fn(i / max(1, nf - 1), i / FPS).tobytes())
    p.stdin.close(); p.wait()
    voz = np.zeros(int((total + .5) * SR))
    for wav, t0 in pos:
        with wave.open(str(wav)) as w: a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32767
        s = int(t0 * SR); voz[s:s + len(a)] += a[:len(voz) - s]
    vw = TMP / "voz.wav"
    with wave.open(str(vw), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(voz, -1, 1) * 32767).astype(np.int16).tobytes())
    mw = TMP / "trilha.wav"; music(total, mw)
    dest = OUT / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mudo), "-i", str(vw), "-i", str(mw),
                    "-filter_complex", "[1:a]volume=1.5,asplit=2[v1][v2];[2:a]volume=0.30[m];[m][v1]sidechaincompress=threshold=0.05:ratio=6:attack=20:release=400[md];"
                    "[md][v2]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", "-shortest", str(dest)], check=True)
    # pôster: quadro do gancho
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1.5", "-i", str(dest), "-frames:v", "1", "-q:v", "3", str(OUT / f"{name}-poster.jpg")], check=True)
    print(name, f"{total:.1f}s")


if __name__ == "__main__":
    main()
