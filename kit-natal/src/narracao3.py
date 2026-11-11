# Vídeos v3 COM narração (edge-tts, voz pt-BR-FranciscaNeural) + trilha suave original.
# Cada trecho de fala cobre um grupo de cenas; a duração das cenas se ajusta à fala para ficar sincronizado.
# Uso: python src/narracao3.py "19,90"  ->  out/v3/videos/video-preco.mp4, video-teatro.mp4 (+ -quadros.png)
import sys, pathlib, subprocess, asyncio, json, wave
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import video3 as V3
import edge_tts

VOZ, RATE = "pt-BR-FranciscaNeural", "+8%"
DEST = V3.DEST; TMP = DEST / "_tmp"; TMP.mkdir(exist_ok=True)
SR = 44100
P, T = V3.PRECO_V, V3.TEATRO_V

# (texto falado, cenas cobertas, folga em s depois da fala)
ROTEIROS = {
    "video-preco": [
        ("Dezembro inteiro do ministério infantil, por dezenove e noventa.", P[0:1], .25),
        ("São quatro aulas de Natal completas, com a história pronta para contar.", P[1:3], .2),
        ("Atividades para cada idade, de três a onze anos.", P[3:6], .2),
        ("Teatro para o culto de Natal.", P[6:7], .15),
        ("E lembrancinhas para recortar.", P[7:9], .15),
        ("Dá menos de cinco reais por domingo. Baixe e imprima hoje. Toque em saiba mais.", P[9:10], .8),
    ],
    "video-teatro": [
        ("Pediram um teatro de Natal para as crianças? Já está escrito.", T[0:1], .2),
        ("O Presente Mais Esperado: oito a dez minutos, falas curtas e figurino com o que você tem em casa.", T[1:4], .2),
        ("Tem papel para todas as crianças, até as de três anos.", T[4:5], .2),
        ("E ainda vêm quatro aulas de Natal, atividades por idade e lembrancinhas.", T[5:9], .15),
        ("Tudo por dezenove e noventa. Toque em saiba mais.", T[9:10], .8),
    ],
}
MIN_CENA = 1.0  # nenhuma página some em menos de 1 s


async def _tts(text, mp3):
    await edge_tts.Communicate(text, VOZ, rate=RATE).save(str(mp3))


def tts(text, idx, name):
    mp3, wav = TMP / f"{name}-{idx}.mp3", TMP / f"{name}-{idx}.wav"
    asyncio.run(_tts(text, mp3))
    # corta o silêncio do início e do fim da fala
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp3), "-af",
                    "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse",
                    "-ar", str(SR), "-ac", "1", str(wav)], check=True)
    with wave.open(str(wav)) as w: return wav, w.getnframes() / SR


def music(seconds, path, bpm=84):
    # mesma trilha de caixinha de música de src/audio.py (I–vi–IV–V em Sol maior)
    beat = 60 / bpm; n = int(seconds * SR); out = np.zeros(n + SR * 3)
    chords = [[55, 59, 62], [52, 55, 59], [48, 52, 55], [50, 54, 57]]
    f = lambda m: 440 * 2 ** ((m - 69) / 12)
    t_all = np.arange(int(SR * beat * 4)) / SR
    def bell(freq, dur=1.6):
        t = np.arange(int(SR * dur)) / SR
        return (np.sin(2 * np.pi * freq * t) + .35 * np.sin(2 * np.pi * freq * 2 * t) + .12 * np.sin(2 * np.pi * freq * 3.01 * t)) * np.exp(-t * 3.2)
    pos, k = 0, 0
    while pos < n:
        ch = chords[k % 4]
        pad = sum(np.sin(2 * np.pi * f(m) * t_all) for m in ch) / 3
        env = np.minimum(1, t_all / .4) * np.minimum(1, (t_all[::-1]) / .4)
        seg = pad * env * .10; out[pos:pos + len(seg)] += seg[:max(0, len(out) - pos)]
        for i, m in enumerate([ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 12, ch[0] + 24, ch[2] + 12, ch[1] + 12, ch[2] + 12]):
            p = pos + int(i * beat / 2 * SR); b = bell(f(m)) * .16; e = min(len(out), p + len(b)); out[p:e] += b[:e - p]
        pos += len(t_all); k += 1
    for d, g in [(.11, .35), (.23, .22), (.37, .12)]:
        s = int(d * SR); out[s:] += out[:-s] * g
    out = out[:n]; fade = int(SR * 1.5); out[-fade:] *= np.linspace(1, 0, fade)
    out = out / np.max(np.abs(out)) * .6
    with wave.open(str(path), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())


def build(name, roteiro):
    LEAD = .15  # a fala começa logo no início (o 1º quadro já tem texto)
    cenas, falas, t = [], [], LEAD
    for i, (texto, grupo, folga) in enumerate(roteiro):
        wav, d = tts(texto, i, name)
        vis = sum(s for s, _ in grupo); alvo = d + folga + (LEAD if i == 0 else 0)
        k = alvo / vis
        nov = [(max(MIN_CENA, s * k), fn) for s, fn in grupo]
        falas.append((wav, t, d)); cenas += nov; t += sum(s for s, _ in nov) - (LEAD if i == 0 else 0)
    total = sum(s for s, _ in cenas)
    V3.render(name + "-mudo", cenas)
    (DEST / f"{name}-mudo-quadros.png").replace(DEST / f"{name}-quadros.png")
    # trilha de voz: cada fala no seu tempo
    voz = np.zeros(int((total + .5) * SR))
    for wav, t0, d in falas:
        with wave.open(str(wav)) as w: a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32767
        s = int(t0 * SR); voz[s:s + len(a)] += a[:len(voz) - s]
    vw = TMP / f"{name}-voz.wav"
    with wave.open(str(vw), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(voz, -1, 1) * 32767).astype(np.int16).tobytes())
    mw = TMP / f"{name}-trilha.wav"; music(total, mw)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(DEST / f"{name}-mudo.mp4"), "-i", str(vw), "-i", str(mw),
                    "-filter_complex", "[1:a]volume=1.5,asplit=2[v1][v2];[2:a]volume=0.35[m];[m][v1]sidechaincompress=threshold=0.05:ratio=6:attack=20:release=400[md];"
                    "[md][v2]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", str(DEST / f"{name}.mp4")], check=True)
    (DEST / f"{name}-mudo.mp4").unlink()
    (DEST / f"{name}-roteiro.json").write_text(json.dumps(
        [{"inicio_s": round(t0, 2), "fim_s": round(t0 + d, 2), "fala": r[0]} for (_, t0, d), r in zip(falas, roteiro)], ensure_ascii=False, indent=1), encoding="utf-8")
    print(name, f"{total:.1f}s")


if __name__ == "__main__":
    for n, r in ROTEIROS.items(): build(n, r)
    for f in TMP.iterdir(): f.unlink()
    TMP.rmdir()
