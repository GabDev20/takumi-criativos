# Vídeos no formato dos anúncios vencedores da Mães Que Treinam (Biblioteca de Anúncios, 23/11/2026):
# pessoa treinando em casa + narração + legenda palavra a palavra com a palavra ativa destacada + CTA para o quiz.
# Aqui: b-roll livre do Pexels (licença Pexels, uso comercial liberado) + voz ElevenLabs + legenda sincronizada
# pelas marcações de tempo do Whisper (assets/voz/words.json) + cartão do quiz no CTA.
# Uso: python3 src/ugc.py [v1 v2 v3]   ->  out/videos/<nome>.mp4
import sys, json, re, pathlib, asyncio, subprocess, shutil, wave
import numpy as np
from playwright.async_api import async_playwright
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from videos import trilha

ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "assets"; OUT = ROOT / "out/videos"; OUT.mkdir(parents=True, exist_ok=True)
W, H, FPS = 1080, 1920, 30
FIX = {"Reveillon,": "Réveillon,", "SaibaMais": "saiba mais"}

VIDEOS = {
    "v1-quiz": dict(voz="el-v1-quiz.mp3", hook="TEM UMA DATA MARCADA?",
                    clips=["8502425", "9001924", "8809586", "6437948", "8837123", "8027215"], cta_from="Faz",
                    destaque={"data", "marcada", "três", "perguntas", "40", "segundos", "plano", "teste"}),
    "v2-calendario": dict(voz="el-v2-calendario.mp3", hook="15 MIN POR DIA ATÉ A SUA DATA",
                          clips=["9001924", "6437948", "8809586", "8027215", "8837123", "8502425"], cta_from="Descubra",
                          destaque={"15", "minutos", "sala", "1", "7", "hábito", "21", "rotina", "plano", "teste"}),
    "v3-dezembro": dict(voz="el-v3-dezembro.mp3", hook="DEIXOU PRA DEZEMBRO?",
                        clips=["8502425", "8837123", "9001924", "6437948", "8809586"], cta_from="Faz",
                        destaque={"dezembro?", "tarde.", "30.", "15", "minutos", "teste", "treinos"}),
}


def palavras(nome, voz):
    ws = json.load(open(A / "voz/words.json"))[voz]
    out = []
    for w, s, e in ws:
        if nome == "v2-calendario" and w == "o" and out and out[-1][0] == "Virou":
            continue
        out.append([FIX.get(w, w), s + .15, e + .15])  # +0,15 s = atraso da voz na mixagem
    if nome == "v2-calendario":  # o Whisper não pontuou este áudio: pontua pelo roteiro
        fins = iter([("dia", "."), ("equipamento", "."), ("1", ":"), ("curto", "."), ("7", ":"), ("hábito", "."),
                     ("21", ":"), ("feita", "."), ("gratuito", "."), ("mais", ".")])
        alvo = next(fins, None)
        for w in out:
            if alvo and w[0].lower() == alvo[0]:
                w[0] += alvo[1]; alvo = next(fins, None)
    return out


def blocos(ws):
    """Agrupa em blocos de até 3 palavras, quebrando em pontuação."""
    bl, cur = [], []
    for w in ws:
        cur.append(w)
        if len(cur) == 3 or re.search(r"[.,?!:]$", w[0]):
            bl.append(cur); cur = []
    if cur: bl.append(cur)
    return bl


def cortes(ws, dur, n):
    """Cortes de b-roll nas pausas de frase, com no mínimo 1,8 s por plano."""
    t, cuts = 0.0, [0.0]
    for w in ws:
        if (re.search(r"[.,?!]$", w[0]) or w[2] - cuts[-1] >= 2.6) and w[2] - cuts[-1] >= 1.8 and dur - w[2] > 1.8:
            cuts.append(w[2])
    cuts.append(dur)
    return [(cuts[i], cuts[i + 1]) for i in range(len(cuts) - 1)]


def base(nome, cfg, dur, ws, tmp):
    segs = cortes(ws, dur, len(cfg["clips"]))
    parts = []
    for i, (a, b) in enumerate(segs):
        clip = A / f"broll/px-{cfg['clips'][i % len(cfg['clips'])]}.mp4"
        off = 1.0 + (i // len(cfg["clips"])) * 4
        p = tmp / f"seg{i:02d}.mp4"; d = b - a
        # cobre 9:16 e aproxima devagar (7% ao longo do plano)
        vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},"
              f"scale=w='{W}*(1+0.07*t/{d:.2f})':h=-2:eval=frame,crop={W}:{H},setsar=1")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "-1", "-ss", f"{off}", "-i", str(clip), "-t", f"{d:.3f}",
                        "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(p)], check=True)
        parts.append(p)
    lst = tmp / "lista.txt"; lst.write_text("".join(f"file '{p}'\n" for p in parts))
    out = tmp / "base.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(out)], check=True)
    return out, segs


HTML = """<html><head><meta charset=utf-8><style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;background:transparent;overflow:hidden;font-family:Inter;position:relative}
#grad{position:absolute;left:0;right:0;bottom:0;height:900px;background:linear-gradient(transparent,rgba(0,0,0,.55))}
#hook{position:absolute;left:60px;right:60px;top:170px;text-align:center;opacity:0}
#hook span{display:inline-block;background:#fff;color:#17181C;font:900 76px/1.12 Montserrat;padding:18px 34px;border-radius:22px;box-shadow:0 12px 40px rgba(0,0,0,.3)}
#cap{position:absolute;left:50px;right:50px;top:1300px;text-align:center;font:900 84px/1.25 Montserrat;color:#fff;text-transform:uppercase;
     text-shadow:0 4px 0 rgba(0,0,0,.55),0 0 24px rgba(0,0,0,.45)}
#cap b{font-weight:900;padding:2px 14px;border-radius:14px;margin:0 2px;display:inline-block}
#cap b.on{background:#FF5A36;text-shadow:none}
#cap b.hi{color:#F2B33D}
#card{position:absolute;left:150px;width:780px;top:330px;background:#fff;border-radius:44px;padding:44px;opacity:0;box-shadow:0 30px 80px rgba(0,0,0,.4)}
.tag{font:800 24px Inter;color:#6B6660;letter-spacing:.06em}.bar{height:12px;background:#F1E6D8;border-radius:9px;margin:14px 0 26px}.bar div{height:100%;width:33%;background:#FF5A36;border-radius:9px}
.q{font:800 44px/1.15 Montserrat;color:#17181C;margin-bottom:24px}.o{border:3px solid #EADFD2;border-radius:22px;padding:24px;font:700 36px Inter;color:#17181C;margin-bottom:14px}.o.on{border-color:#FF5A36;background:#FFF0EB}
#btn{position:absolute;left:0;right:0;top:1060px;text-align:center;opacity:0}#btn span{display:inline-block;background:#17181C;color:#fff;font:800 44px Montserrat;padding:30px 56px;border-radius:999px}
#brand{position:absolute;left:0;right:0;top:80px;text-align:center;font:800 26px Montserrat;letter-spacing:.2em;color:#fff;opacity:.9;text-shadow:0 2px 8px rgba(0,0,0,.5)}
</style></head><body>
<div id=grad></div><div id=brand>CONTAGEM REGRESSIVA</div><div id=hook><span>HOOK</span></div><div id=cap></div>
<div id=card><div class=tag>PERGUNTA 1 DE 3 · 40 SEGUNDOS</div><div class=bar><div></div></div>
<div class=q>Quantos dias faltam para a sua data?</div><div class=o>Menos de 15</div><div class=o id=op>15 a 40</div><div class=o>40 a 60</div><div class=o>Mais de 60</div></div>
<div id=btn><span>TOQUE EM SAIBA MAIS</span></div>
<script>
const E=x=>x<0?0:x>1?1:1-Math.pow(1-x,3);
window.setup=(hook,blocks,hi,cta,dur)=>{document.querySelector('#hook span').textContent=hook;window.B=blocks;window.HI=hi;window.CTA=cta;window.D=dur};
window.render=t=>{
 const h=document.getElementById('hook');const hv=Math.min(E(t/.25),1-E((t-2.6)/.3));h.style.opacity=hv;h.style.transform=`scale(${.9+.1*E(t/.25)})`;
 let cur=null;for(const b of B){if(t>=b.s-.05)cur=b}
 const c=document.getElementById('cap');
 if(cur&&t<cur.e+.6){let ai=-1;cur.w.forEach((w,i)=>{if(t>=w[1]-.05)ai=i});c.innerHTML=cur.w.map((w,i)=>{const on=i==ai;const k=w[0].toLowerCase();return `<b class="${on?'on':''} ${!on&&HI.includes(k)?'hi':''}">${w[0]}</b>`}).join(' ')}else c.innerHTML='';
 const k=E((t-CTA)/.4);const cd=document.getElementById('card');cd.style.opacity=t>=CTA?k:0;cd.style.transform=`translateY(${(1-k)*120}px)`;
 document.getElementById('op').classList.toggle('on',t>CTA+1.2);
 const bt=document.getElementById('btn');bt.style.opacity=t>=CTA+.5?E((t-CTA-.5)/.3):0;bt.style.transform=`scale(${1+.04*Math.sin(t*6)})`;
 c.style.top=(t>=CTA?1450:1300)+'px';}
</script></body></html>"""


async def overlay(cfg, ws, dur, cta, tmp):
    bl = blocos(ws)
    js = []
    for b in bl:
        ww = []
        for i, w in enumerate(b):
            fim = b[i + 1][1] if i + 1 < len(b) else w[2] + .15
            ww.append([w[0], w[1], w[2], fim])
        js.append({"s": b[0][1], "e": b[-1][2], "w": ww})
    fr = tmp / "ov"; fr.mkdir(exist_ok=True)
    async with async_playwright() as p:
        br = await p.chromium.launch(); pg = await br.new_page(viewport={"width": W, "height": H})
        await pg.set_content(HTML); await pg.wait_for_timeout(300)
        await pg.evaluate("([a,b,c,d,e])=>setup(a,b,c,d,e)", [cfg["hook"], js, [x.lower() for x in cfg["destaque"]], cta, dur])
        for i in range(int(dur * FPS)):
            await pg.evaluate(f"render({i / FPS})")
            await pg.screenshot(path=str(fr / f"{i:05d}.png"), omit_background=True)
        await br.close()
    return fr


def montar(nome):
    cfg = VIDEOS[nome]; tmp = OUT / f"_ugc_{nome}"; shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir()
    ws = palavras(nome, cfg["voz"])
    voz = A / "voz" / cfg["voz"]
    vd = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(voz)], capture_output=True, text=True).stdout)
    dur = round(vd + 0.9, 2)
    cta = next(w[1] for w in ws if w[0] == cfg["cta_from"]) - .1
    b, segs = base(nome, cfg, dur, ws, tmp)
    fr = asyncio.run(overlay(cfg, ws, dur, cta, tmp))
    tr = tmp / "trilha.wav"; trilha(dur, tr)
    out = OUT / f"{nome}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(b), "-framerate", str(FPS), "-i", str(fr / "%05d.png"),
                    "-i", str(voz), "-i", str(tr),
                    "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto[v];[2:a]adelay=150|150,volume=1.0[vz];[3:a]volume=0.13[t];[vz][t]amix=inputs=2:duration=longest:normalize=0[a]",
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
                    "-c:a", "aac", "-b:a", "192k", "-t", f"{dur}", "-movflags", "+faststart", str(out)], check=True)
    print("ok", out.name, dur, "s, planos:", len(segs))


if __name__ == "__main__":
    alvo = sys.argv[1:] or list(VIDEOS)
    for n in VIDEOS:
        if any(n.startswith(a) for a in alvo):
            montar(n)
