# Narração (Piper, pt_BR) + trilha original (caixinha de música sintetizada) e mixagem nos vídeos.
import pathlib, subprocess, sys, wave
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import video

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "out"; A = OUT / "audio"; A.mkdir(exist_ok=True)
VOICE = pathlib.Path(sys.argv[1])  # caminho do modelo .onnx
SR = 44100

ROT = {
    "video-1-folheando-o-kit": (video.V1,
        "O dezembro inteiro do seu ministério infantil, pronto. São quatro aulas de Natal, com plano completo e história para contar. "
        "Atividades para cada idade: colorir, labirinto e caça-palavras. Teatro para o culto de Natal, e lembrancinhas para recortar. "
        "Tudo isso por dezenove e noventa. Toque em saiba mais."),
    "video-3-uma-aula-do-kit": (video.V3,
        "Olha como fica uma aula do kit de Natal. Primeiro, o planejamento: verdade central, versículo e materiais. "
        "Depois, a acolhida, com uma dinâmica pronta. Aí você conta a história, que já vem escrita. "
        "Em seguida, perguntas separadas por idade. E, para fechar, uma atividade para cada faixa etária. "
        "São quatro aulas assim, mais teatro e lembrancinhas. Seu dezembro pronto, por dezenove e noventa."),
}


def tts(text, path):
    subprocess.run([sys.executable, "-m", "piper", "-m", str(VOICE), "-f", str(path), "--length-scale", "0.92", "--sentence-silence", "0.25"],
                   input=text.encode(), check=True, capture_output=True)
    with wave.open(str(path)) as w: return w.getnframes() / w.getframerate()


def music(seconds, path, bpm=84):
    # progressão I–vi–IV–V em Sol maior, caixinha de música + pad suave
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
        seg = (pad * env * .10)
        out[pos:pos + len(seg)] += seg[:max(0, len(out) - pos)]
        arp = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 12, ch[0] + 24, ch[2] + 12, ch[1] + 12, ch[2] + 12]
        for i, m in enumerate(arp):
            p = pos + int(i * beat / 2 * SR); b = bell(f(m)) * .16
            e = min(len(out), p + len(b)); out[p:e] += b[:e - p]
        pos += len(t_all); k += 1
    # reverb simples
    for d, g in [(.11, .35), (.23, .22), (.37, .12)]:
        s = int(d * SR); out[s:] += out[:-s] * g
    out = out[:n]; fade = int(SR * 1.5); out[-fade:] *= np.linspace(1, 0, fade)
    out = out / np.max(np.abs(out)) * .6
    pcm = (out * 32767).astype(np.int16)
    with wave.open(str(path), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


for name, (scenes, text) in ROT.items():
    vo = A / f"{name}-voz.wav"; d = tts(text, vo)
    total = sum(s for s, _ in scenes); target = d + 1.8
    k = target / total
    scaled = [(s * k, fn) for s, fn in scenes]
    video.render(name + "-mudo", scaled)
    mus = A / f"{name}-trilha.wav"; music(target, mus)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(OUT / f"{name}-mudo.mp4"), "-i", str(vo), "-i", str(mus),
                    "-filter_complex", "[1:a]adelay=500|500,volume=1.6,asplit=2[v1][v2];[2:a]volume=0.55[m];[m][v1]sidechaincompress=threshold=0.05:ratio=6:attack=20:release=400[md];[md][v2]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5,apad[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-t", f"{target:.2f}", str(OUT / f"{name}.mp4")], check=True)
    (OUT / f"{name}-mudo.mp4").unlink()
    print(name, f"voz {d:.1f}s, vídeo {target:.1f}s")
