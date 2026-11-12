# Vídeos v4: narrados com a voz clonada do Gabriel (ElevenLabs, "Gabriel Geral"), legendados, com os 2 pacotes.
# Entrada: out/v4/videos/voz/<nome>.mp3 (narração inteira, uma frase por trecho, com pausa entre elas).
# A narração é dividida nas N-1 maiores pausas; cada frase manda no tempo das cenas que cobre.
# Uso: python src/video4.py [preco_essencial] [preco_completo]   (padrão 19,90 e 29,90, como na página v4)
import sys, pathlib, subprocess, json
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).parent))
ESS = sys.argv[1] if len(sys.argv) > 1 else "19,90"
COMP = sys.argv[2] if len(sys.argv) > 2 else "29,90"
sys.argv = [sys.argv[0], ESS]  # video3 lê o preço do argv
import video as V
import video3 as V3
import narracao3 as N3
from PIL import Image, ImageDraw

ROOT = V.ROOT; DEST = ROOT / "out/v4/videos"; VOZ = DEST / "voz"; DEST.mkdir(parents=True, exist_ok=True)
V3.DEST = DEST
W, H, SR = V.W, V.H, 44100
NAVY, GOLD, RED, WHITE, GREEN = V.NAVY, V.GOLD, V.RED, V.WHITE, (30, 142, 90)


def legenda(fn, texto):
    """Legenda da fala em caixa escura, dentro da área segura (até 1670 px)."""
    def f(t, s):
        im = fn(t, s); d = ImageDraw.Draw(im, "RGBA"); fnt = V.B(50)
        words, lines, cur = texto.split(), [], ""
        for w_ in words:
            tt = (cur + " " + w_).strip()
            if d.textlength(tt, font=fnt) <= 900: cur = tt
            else: lines.append(cur); cur = w_
        lines.append(cur)
        lh = 60; h = lh * len(lines) + 30; y0 = 1650 - h
        d.rounded_rectangle([60, y0, W - 60, 1650], 28, fill=(10, 20, 35, 225))
        for i, ln in enumerate(lines):
            d.text((W / 2, y0 + 16 + i * lh), ln, font=fnt, fill=GOLD if i == 0 else WHITE, anchor="ma")
        return im
    return f


def pacotes(titulo):
    """Os dois pacotes lado a lado; o Completo cresce e ganha o selo de recomendado."""
    def card(d, x, y, w, h, nome, preco, itens, destaque):
        d.rounded_rectangle([x, y, x + w, y + h], 34, fill=WHITE, outline=GOLD if destaque else (200, 210, 222), width=10 if destaque else 4)
        d.text((x + w / 2, y + 40), nome, font=V.B(62), fill=NAVY, anchor="ma")
        yy = y + 130
        for it in itens:
            d.line([(x + 34, yy + 24), (x + 46, yy + 38), (x + 68, yy + 10)], fill=GREEN, width=7); d.text((x + 80, yy), it, font=V.N(38), fill=NAVY); yy += 58
        d.text((x + w / 2, y + h - 150), f"R$ {preco}", font=V.B(96), fill=GREEN if destaque else NAVY, anchor="ma")
    def f(t, s):
        im = V.bg(); d = ImageDraw.Draw(im)
        V.text_c(d, 300, titulo, V.B(76), WHITE)
        a = V.ease(s / .4); grow = V.ease((s - .5) / .5)
        card(d, 50, 560 + int((1 - a) * 200), 470, 760, "Essencial", ESS, ["Dezembro inteiro", "4 aulas + teatro", "16 atividades", "Lembrancinhas"], False)
        x2, y2 = 560, 520 - int(20 * grow)
        card(d, x2, y2 + int((1 - a) * 260), 470, 800 + int(40 * grow), "Completo", COMP, ["Tudo do Essencial", "+ Aulas de janeiro", "+ Certificados", "+ Convites de Natal", "Toda a equipe"], True)
        if s > .5:
            fb = V.B(40); tw = d.textlength("Recomendado", font=fb); cx = x2 + 235
            d.rounded_rectangle([cx - tw / 2 - 26, y2 - 34, cx + tw / 2 + 26, y2 + 34], 30, fill=RED)
            d.text((cx, y2), "Recomendado", font=fb, fill=WHITE, anchor="mm")
        return im
    return f


def falas_por_pausa(mp3, n, textos_len):
    wav = DEST / "_voz.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp3), "-ac", "1", "-ar", str(SR), str(wav)], check=True)
    import wave
    with wave.open(str(wav)) as w: a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32767
    hop = int(.02 * SR); rms = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a) - hop, hop)])
    fala = 20 * np.log10(rms + 1e-9) > -38
    idx = np.where(fala)[0]; ini, fim = idx[0] * .02, (idx[-1] + 1) * .02
    gaps, i = [], idx[0]
    while i <= idx[-1]:
        if not fala[i]:
            j = i
            while not fala[j]: j += 1
            gaps.append((j - i, i * .02, j * .02)); i = j
        else: i += 1
    # cada corte vai para a pausa mais perto de onde a frase deveria acabar (proporcional ao número de letras)
    gaps = [g for g in gaps if g[0] >= 6]  # pausas de 120 ms ou mais
    cortes, usados = [], -1
    for k in range(1, n):
        esp = ini + (fim - ini) * sum(textos_len[:k]) / sum(textos_len)
        cand = [(abs((g[1] + g[2]) / 2 - esp) - .02 * g[0], j) for j, g in enumerate(gaps) if j > usados]
        j = min(cand)[1]; cortes.append(gaps[j]); usados = j
    segs, s0 = [], ini
    for _, g0, g1 in cortes: segs.append((s0, g0)); s0 = g1
    segs.append((s0, fim))
    return wav, a, segs


def build(nome, roteiro):
    mp3 = VOZ / f"{nome}.mp3"; wav, a, segs = falas_por_pausa(mp3, len(roteiro), [len(r[0]) for r in roteiro])
    assert len(segs) == len(roteiro), (nome, len(segs))
    cenas, marcos = [], []
    for i, ((texto, grupo, leg), (s0, s1)) in enumerate(zip(roteiro, segs)):
        t0 = 0 if i == 0 else s0
        t1 = segs[i + 1][0] if i + 1 < len(segs) else s1 + .9
        alvo = t1 - t0; vis = sum(d for d, _ in grupo)
        nov = [(max(.9, d * alvo / vis), legenda(fn, texto) if leg else fn) for d, fn in grupo]
        k = alvo / sum(d for d, _ in nov); nov = [(d * k, fn) for d, fn in nov]  # fecha exatamente no tempo da fala
        cenas += nov; marcos.append({"inicio_s": round(s0, 2), "fim_s": round(s1, 2), "fala": texto})
    total = sum(d for d, _ in cenas)
    V3.render(nome + "-mudo", cenas)
    (DEST / f"{nome}-mudo-quadros.png").replace(DEST / f"{nome}-quadros.png")
    mw = DEST / "_trilha.wav"; N3.music(total, mw)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(DEST / f"{nome}-mudo.mp4"), "-i", str(wav), "-i", str(mw),
                    "-filter_complex", "[1:a]volume=1.4,apad,asplit=2[v1][v2];[2:a]volume=0.30[m];[m][v1]sidechaincompress=threshold=0.05:ratio=6:attack=20:release=400[md];"
                    "[md][v2]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", str(DEST / f"{nome}.mp4")], check=True)
    for f in [DEST / f"{nome}-mudo.mp4", mw, wav]: f.unlink()
    (DEST / f"{nome}-roteiro.json").write_text(json.dumps(marcos, ensure_ascii=False, indent=1), encoding="utf-8")
    print(nome, f"{total:.1f}s")


S = V3.show; HK = V3.hook
PRECO = [
    ("Se você dá aula no ministério infantil, para um segundo.", [(2, HK("Se você dá aula no ministério infantil,", "PARA UM SEGUNDO.", big_size=120))], False),
    ("O seu dezembro inteiro já está pronto, por dezenove e noventa.", [(2, HK("Seu dezembro inteiro pronto por", f"R$ {ESS}"))], False),
    ("São quatro aulas de Natal completas, com a história pronta para contar.",
     [(1.5, S("aula", None, top="4 aulas de Natal", f0=(.5, .2), f1=(.5, .45))), (1.5, S("historia", None, top="História pronta", f0=(.5, .25), f1=(.5, .4)))], True),
    ("Atividade para cada idade, de três a onze anos, com gabarito.",
     [(1, S("colorir", None, top="3 a 5 anos")), (1, S("labirinto", None, top="3 a 8 anos")), (1, S("cacapalavras", None, top="6 a 11 anos"))], True),
    ("Teatro para o culto de Natal, e lembrancinhas para recortar.",
     [(1.4, S("teatro", None, top="Teatro do culto", f0=(.5, .2), f1=(.5, .4))), (1, S("cartao", None, top="Lembrancinhas")), (1, S("marcadores", None, top="Marcadores"))], True),
    ("Dá menos de cinco reais por domingo. E no pacote Completo ainda vêm as aulas de janeiro e os certificados.", [(5, pacotes("Menos de R$ 5 por domingo"))], False),
    ("Chega no seu e-mail na hora, com sete dias de garantia. Toque em saiba mais e escolha o seu pacote.",
     [(5, V3.cta("PDF no e-mail na hora · a partir de", "7 dias de garantia", "Toque em Saiba mais"))], False),
]
TEATRO = [
    ("Pediram um teatro de Natal para as crianças, e ninguém sabe por onde começar?",
     [(3, HK("Pediram um teatro de Natal para as crianças?", None, "E ninguém sabe por onde começar?", y0=620))], False),
    ("Calma. Já está escrito.", [(1.6, HK("Calma.", "Já está escrito.", big_size=130, y0=700))], False),
    ("O Presente Mais Esperado: oito a dez minutos, falas curtas, e figurino com o que você tem em casa.",
     [(1.6, S("teatro", None, top="O Presente Mais Esperado", z0=1.0, z1=1.1, f0=(.5, .1))),
      (1.6, S("teatro", None, top="Falas curtas", z0=1.35, z1=1.5, f0=(.3, .45), f1=(.3, .55))),
      (1.6, S("teatro", None, top="Figurino simples", z0=1.35, z1=1.5, f0=(.3, .12), f1=(.3, .16)))], True),
    ("E tem papel para todas as crianças, até as de três anos.", [(2.4, HK("Papel para todas as crianças,", "até as de 3 anos", big_size=110, y0=620))], False),
    ("Junto vêm quatro aulas de Natal, atividades por idade e lembrancinhas.",
     [(1.2, S("aula", None, top="4 aulas de Natal", f0=(.5, .2), f1=(.5, .4))), (1.2, S("colorir", None, top="Atividades por idade")), (1.2, S("cartao", None, top="Lembrancinhas"))], True),
    ("Tudo a partir de dezenove e noventa, com sete dias de garantia.", [(4, pacotes("Escolha o seu pacote"))], False),
    ("Toque em saiba mais e deixe o culto de Natal resolvido hoje.",
     [(3.5, V3.cta("Culto de Natal resolvido hoje", "7 dias de garantia", "Toque em Saiba mais"))], False),
]

if __name__ == "__main__":
    build("video-preco-v4", PRECO)
    build("video-teatro-v4", TEATRO)
