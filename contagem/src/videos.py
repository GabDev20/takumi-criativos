# Vídeos 9:16 do ângulo "Contagem Regressiva", renderizados por código (HTML + Playwright quadro a quadro + ffmpeg).
# Legenda grande na tela (funciona no mudo) + trilha original gerada aqui. A narração do ElevenLabs entra depois
# com src/mux_voz.sh quando os mp3 estiverem em out/videos/voz/ (o ambiente não consegue baixá-los direto).
# Uso: python3 src/videos.py [v1 v2 v3]
import sys, pathlib, asyncio, subprocess, wave, shutil
import numpy as np
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "out/videos"; OUT.mkdir(parents=True, exist_ok=True)
FPS, W, H, SR = 30, 1080, 1920, 44100

BASE = """
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--cream:#FFF4E8;--ink:#17181C;--coral:#FF5A36;--gold:#F2B33D;--mute:#6B6660}
body{width:1080px;height:1920px;background:var(--cream);font-family:Inter,sans-serif;color:var(--ink);overflow:hidden;position:relative}
.a{position:absolute;opacity:0;will-change:transform,opacity}
.brand{left:72px;top:96px;font:800 28px Montserrat;letter-spacing:.18em;color:var(--coral);opacity:1}
.cap{left:64px;right:64px;font:900 92px/1.04 Montserrat;letter-spacing:-.02em}
.cap em{font-style:normal;color:var(--coral)}
.pill{background:var(--ink);color:#fff;border-radius:999px;font:800 46px Montserrat;padding:34px 56px;display:inline-block}
.chip{background:#fff;border:3px solid #EADFD2;border-radius:24px;font:800 50px Montserrat;padding:26px 40px}
.phone{left:170px;top:700px;width:740px;height:1120px;background:#fff;border-radius:70px;border:16px solid var(--ink);box-shadow:0 40px 90px rgba(23,24,28,.25);overflow:hidden}
.scr{position:absolute;inset:0;padding:70px 46px;opacity:0}
.q{font:800 46px/1.18 Montserrat;margin:26px 0 34px}
.opt{border:3px solid #EADFD2;border-radius:24px;padding:30px 30px;font:700 38px Inter;margin-bottom:18px}
.opt.on{border-color:var(--coral);background:#FFF0EB}
.bar{height:12px;background:#F1E6D8;border-radius:9px}.bar>div{height:100%;background:var(--coral);border-radius:9px}
.tag{font:700 24px Inter;color:var(--mute);letter-spacing:.06em}
.dot{width:90px;height:90px;border-radius:50%;background:rgba(255,90,54,.35);border:5px solid var(--coral)}
.cell{border-radius:22px;height:150px;padding:16px 18px;font:900 50px Montserrat;background:#fff;border:3px solid #EADFD2;position:relative}
.ck{position:absolute;right:20px;bottom:30px;width:36px;height:18px;border-left:8px solid var(--gold);border-bottom:8px solid var(--gold);transform:rotate(-45deg)}
</style>
<script>
const E=x=>x<0?0:x>1?1:1-Math.pow(1-x,3);
// mostra el entre t0 e t1 com entrada de baixo (dy) e saída em fade
function show(id,t,t0,t1,dy=60,sc=0){const el=document.getElementById(id);if(!el)return;
  const i=E((t-t0)/.35),o=t1?1-E((t-t1)/.25):1;const v=Math.min(i,o);
  el.style.opacity=v;el.style.transform=`translateY(${(1-i)*dy}px) scale(${1-sc*(1-i)})`;}
</script>
"""

# ---------------------------------------------------------------- V1: o quiz em 3 toques (narração 18,9 s)
V1 = """
<div class="a brand" id=br>CONTAGEM REGRESSIVA</div>
<div class="a cap" id=c1 style="top:230px">Tem uma data marcada no <em>seu calendário?</em></div>
<div class=a id=chips style="left:64px;right:64px;top:780px;display:flex;flex-direction:column;gap:26px;align-items:flex-start">
  <div class="a chip" id=k1 style="position:relative">Réveillon</div><div class="a chip" id=k2 style="position:relative">Viagem</div>
  <div class="a chip" id=k3 style="position:relative">Casamento</div><div class="a chip" id=k4 style="position:relative">Formatura</div></div>
<div class="a cap" id=c2 style="top:230px;font-size:80px">Responda <em>3 perguntas</em></div>
<div class="a cap" id=c3 style="top:230px;font-size:80px">Sai o seu plano, <em>dia a dia</em>, até a data</div>
<div class="a phone" id=ph>
  <div class=scr id=q1><div class=tag>PERGUNTA 1 DE 3</div><div class=bar style="margin-top:14px"><div style="width:33%"></div></div>
    <div class=q>Quantos dias faltam para a sua data?</div><div class=opt>Menos de 15</div><div class=opt id=o1>15 a 40</div><div class=opt>40 a 60</div><div class=opt>Mais de 60</div></div>
  <div class=scr id=q2><div class=tag>PERGUNTA 2 DE 3</div><div class=bar style="margin-top:14px"><div style="width:66%"></div></div>
    <div class=q>Quanto tempo você tem por dia?</div><div class=opt>10 minutos</div><div class=opt id=o2>15 minutos</div><div class=opt>20 minutos</div></div>
  <div class=scr id=q3><div class=tag>PERGUNTA 3 DE 3</div><div class=bar style="margin-top:14px"><div style="width:100%"></div></div>
    <div class=q>Onde você vai treinar?</div><div class=opt id=o3>Em casa, na sala</div><div class=opt>No quarto</div><div class=opt>Na academia</div></div>
  <div class=scr id=r><div class=tag>SEU PLANO ESTÁ PRONTO</div>
    <div style="font:900 64px/1.05 Montserrat;margin:26px 0">21 treinos de <span style="color:var(--coral)">15 min</span> até a sua data</div>
    <div id=rows style="display:flex;flex-direction:column;gap:14px"></div></div>
  <div class="a dot" id=tap></div>
</div>
<div class=a id=cta style="left:0;right:0;top:1500px;text-align:center"><span class=pill>Faça o teste no link</span>
  <div style="font:600 34px Inter;color:var(--mute);margin-top:24px">40 segundos · gratuito</div></div>
<script>
const rows=document.getElementById('rows');
[['Dia 1','Ativação · 15 min'],['Dia 2','Pernas e glúteos · 14 min'],['Dia 3','Core em pé · 15 min'],['Dia 4','Mobilidade · 12 min']].forEach((r,i)=>{
 rows.innerHTML+=`<div id=rw${i} style="display:flex;justify-content:space-between;background:#FFF4E8;border-radius:20px;padding:24px 26px;font:700 32px Inter;opacity:0"><b>${r[0]}</b><span style="color:#6B6660">${r[1]}</span></div>`});
function tapAt(t,t0,id){const o=document.getElementById(id);const tp=document.getElementById('tap');
 if(t>=t0-.5&&t<t0+.5){const y=o.offsetTop+o.offsetHeight/2-45, x=o.offsetLeft+o.offsetWidth*.7-45;
  tp.style.left=x+'px';tp.style.top=y+'px';const k=(t-(t0-.5));tp.style.opacity=k<.4?E(k/.4):1-E((k-.6)/.4);
  tp.style.transform=`scale(${k>.5&&k<.7?.8:1})`;}
 o.classList.toggle('on',t>=t0);}
window.render=t=>{
 show('c1',t,0,4.9);['k1','k2','k3','k4'].forEach((k,i)=>show(k,t,.5+i*.4,4.9,0,.4));show('chips',t,0,4.9,0);
 show('c2',t,5.0,10.6);show('ph',t,5.0,16.4,200);
 const scr=(id,a,b)=>{const el=document.getElementById(id);el.style.opacity=t>=a&&t<b?1:0};
 scr('q1',5,7.4);scr('q2',7.4,9.4);scr('q3',9.4,11.0);scr('r',11.0,99);
 document.getElementById('tap').style.opacity=0;
 if(t<7.4)tapAt(t,6.9,'o1');else if(t<9.4)tapAt(t,8.9,'o2');else if(t<11)tapAt(t,10.5,'o3');
 show('c3',t,10.8,16.4);for(let i=0;i<4;i++)show('rw'+i,t,11.8+i*.5,99,30);
 show('cta',t,16.5,0,80);show('c1b',t,0,0);
 document.getElementById('br').style.opacity=1;}
</script>"""

# ---------------------------------------------------------------- V2: calendário de 21 dias (narração 16,9 s)
V2 = """
<div class="a brand" id=br>CONTAGEM REGRESSIVA</div>
<div class="a cap" id=c1 style="top:260px;font-size:130px"><em>15 minutos</em><br>por dia.</div>
<div class=a id=ring style="left:290px;top:860px;width:500px;height:500px">
  <svg width=500 height=500><circle cx=250 cy=250 r=220 fill=none stroke="#F1E6D8" stroke-width=34 />
  <circle id=arc cx=250 cy=250 r=220 fill=none stroke="#FF5A36" stroke-width=34 stroke-linecap=round transform="rotate(-90 250 250)" stroke-dasharray="1382" stroke-dashoffset=0 /></svg>
  <div id=clk style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font:900 120px Montserrat">15:00</div></div>
<div class="a cap" id=c2 style="top:260px;font-size:110px">Na sala.<br><em>Sem equipamento.</em></div>
<div class=a id=grid style="left:64px;right:64px;top:760px;display:grid;grid-template-columns:repeat(7,1fr);gap:14px"></div>
<div class="a cap" id=d1 style="top:300px;font-size:96px"><em>Dia 1:</em> um treino curto.</div>
<div class="a cap" id=d7 style="top:300px;font-size:96px"><em>Dia 7:</em> virou hábito.</div>
<div class="a cap" id=d21 style="top:240px;font-size:88px"><em>Dia 21:</em> você chega na sua data com a rotina feita.</div>
<div class=a id=cta style="left:0;right:0;top:1380px;text-align:center"><span class=pill>Descubra o seu plano</span>
  <div style="font:600 34px Inter;color:var(--mute);margin-top:24px">Teste gratuito · toque em saiba mais</div></div>
<script>
const g=document.getElementById('grid');
for(let d=1;d<=21;d++)g.innerHTML+=`<div class=cell id=d_${d}>${d}<div style="font:800 17px Inter;letter-spacing:.06em;margin-top:6px" id=l_${d}></div></div>`;
window.render=t=>{
 show('c1',t,0,2.9);show('ring',t,0,5.6,80);
 const p=Math.min(1,t/5.6);document.getElementById('arc').style.strokeDashoffset=1382*p*.25;
 const s=Math.round(900-p*15);document.getElementById('clk').textContent=`${Math.floor(s/60)}:${String(s%60).padStart(2,'0')}`;
 show('c2',t,3.0,5.6);show('grid',t,5.6,0,120);
 show('d1',t,5.7,8.0);show('d7',t,8.1,10.3);show('d21',t,10.4,14.6);
 for(let d=1;d<=21;d++){const c=document.getElementById('d_'+d),l=document.getElementById('l_'+d);
  const tick=d==1?6.6:d<=7?8.4+(d-2)*.25:10.6+(d-8)*.18;const done=t>=tick;
  c.style.background=d==21&&t>=13.2?'#F2B33D':done?'#17181C':'#fff';c.style.color=done&&!(d==21)?'#fff':'#17181C';
  c.style.borderColor=done||(d==21&&t>=13.2)?'transparent':'#EADFD2';
  c.querySelector('.ck')||(done&&d<21&&(c.innerHTML+='<div class=ck></div>'));
  if(!done){const k=c.querySelector('.ck');k&&k.remove()}
  l.textContent=d==21&&t>=13.2?'SUA DATA':'';
  const pop=t>=tick&&t<tick+.25?1+.08*Math.sin((t-tick)/.25*Math.PI):1;c.style.transform=`scale(${pop})`;}
 show('cta',t,14.7,0,80);document.getElementById('br').style.opacity=1;}
</script>"""

# ---------------------------------------------------------------- V3: "deixou pra dezembro?" (narração 13,0 s)
V3 = """
<div style="position:absolute;inset:0;background:linear-gradient(170deg,#1d2440 0%,#3b2a4a 60%,#7a3b45 100%)"></div>
<div class="a brand" id=br style="color:#F2B33D">CONTAGEM REGRESSIVA</div>
<div class="a cap" id=c1 style="top:260px;color:#fff;font-size:120px">Deixou pra<br><span style="color:#F2B33D">dezembro?</span></div>
<div class="a cap" id=c2 style="top:260px;color:#fff;font-size:130px">Não é<br><span style="color:#F2B33D">tarde.</span></div>
<div class="a cap" id=c3 style="top:230px;color:#fff;font-size:92px">O que não dá é começar no <span style="color:#FF5A36">dia 30.</span></div>
<div class=a id=cal style="left:90px;right:90px;top:760px;background:#fff;border-radius:40px;padding:34px;box-shadow:0 30px 80px rgba(0,0,0,.35)">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:22px"><b style="font:900 54px Montserrat">Dezembro</b><span style="font:700 30px Inter;color:#6B6660">2026</span></div>
  <div id=cg style="display:grid;grid-template-columns:repeat(7,1fr);gap:10px"></div></div>
<div class="a cap" id=c4 style="top:230px;color:#fff;font-size:88px"><span style="color:#F2B33D">15 minutos</span> por dia, contados até a sua data.</div>
<div class=a id=big style="left:0;right:0;top:820px;text-align:center;color:#fff">
  <div style="font:600 40px Inter;opacity:.8">de hoje até 31/12</div>
  <div id=num style="font:900 360px/1 Montserrat;color:#F2B33D">37</div>
  <div style="font:800 58px Montserrat">treinos ainda cabem</div></div>
<div class=a id=cta style="left:0;right:0;top:1500px;text-align:center"><span class=pill style="background:#fff;color:#17181C">Faça o teste</span>
  <div style="font:600 34px Inter;color:#e9dcf0;margin-top:24px">e veja quantos cabem até a sua data</div></div>
<script>
const cg=document.getElementById('cg');for(let i=0;i<2;i++)cg.innerHTML+='<div></div>';
for(let d=1;d<=31;d++)cg.innerHTML+=`<div id=z${d} style="height:86px;border-radius:16px;background:#FFF4E8;display:flex;align-items:center;justify-content:center;font:800 36px Montserrat;position:relative">${d}</div>`;
window.render=t=>{
 show('c1',t,0,2.0);show('c2',t,2.05,3.6,40,.2);show('c3',t,3.65,6.4);show('cal',t,3.65,6.4,120);
 const z=document.getElementById('z30');const on=t>=4.9;z.style.background=on?'#FF5A36':'#FFF4E8';z.style.color=on?'#fff':'#17181C';
 z.style.transform=`scale(${on?1+.15*Math.max(0,1-(t-4.9)/.4):1})`;
 for(let d=1;d<=29;d++){document.getElementById('z'+d).style.opacity=t>5.3?.35:1}
 show('c4',t,6.5,13.3);show('big',t,6.5,0,80);
 const n=Math.round(37-Math.max(0,Math.min(1,(t-7.2)/0))*0);document.getElementById('num').textContent=37;
 show('cta',t,9.9,0,80);document.getElementById('br').style.opacity=1;}
</script>"""

VIDEOS = {"v1-quiz": (V1, 20.0), "v2-calendario": (V2, 18.0), "v3-dezembro": (V3, 14.0)}


def trilha(seconds, path, bpm=112):
    """Batida original leve (kick, palma, hi-hat, baixo e acorde), volume baixo para ficar sob a voz."""
    n = int(seconds * SR); out = np.zeros(n + SR); beat = 60 / bpm; rng = np.random.default_rng(3)
    f = lambda m: 440 * 2 ** ((m - 69) / 12)
    def add(sig, at):
        p = int(at * SR); e = min(len(out), p + len(sig))
        if e > p: out[p:e] += sig[:e - p]
    tk = np.arange(int(.25 * SR)) / SR
    kick = np.sin(2 * np.pi * (50 + 90 * np.exp(-tk * 30)) * tk) * np.exp(-tk * 14)
    hat = np.diff(rng.standard_normal(int(.04 * SR)), prepend=0) * np.exp(-np.arange(int(.04 * SR)) / SR * 90)
    clap = rng.standard_normal(int(.12 * SR)) * np.exp(-np.arange(int(.12 * SR)) / SR * 30)
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G
    bar, k = 0.0, 0
    while bar * SR < n:
        ch = chords[k % 4]; tb = np.arange(int(beat * 4 * SR)) / SR
        pad = sum(np.sin(2 * np.pi * f(m) * tb) + .3 * np.sin(2 * np.pi * f(m) * 2 * tb) for m in ch) / 3
        add(pad * np.minimum(1, tb / .05) * np.exp(-tb * .5) * .09, bar)
        for b in range(4):
            add(kick * .5, bar + b * beat)
            if b % 2: add(clap * .12, bar + b * beat)
            add(np.sin(2 * np.pi * f(ch[0] - 24) * tk) * np.exp(-tk * 6) * .3, bar + b * beat + beat / 2)
        for i in range(8): add(hat * (.10 if i % 2 else .05), bar + i * beat / 2)
        bar += beat * 4; k += 1
    out = out[:n]; fi, fo = int(SR * .2), int(SR * 1.2)
    out[:fi] *= np.linspace(0, 1, fi); out[-fo:] *= np.linspace(1, 0, fo)
    out = out / np.max(np.abs(out)) * .5
    with wave.open(str(path), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())


async def render(nome, html, dur):
    tmp = OUT / f"_frames_{nome}"; shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir()
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": W, "height": H})
        await pg.set_content(f"<html><head><meta charset=utf-8>{BASE}</head><body>{html}</body></html>")
        await pg.wait_for_timeout(300)
        for i in range(int(dur * FPS)):
            await pg.evaluate(f"render({i / FPS})")
            await pg.screenshot(path=str(tmp / f"{i:05d}.jpg"), type="jpeg", quality=88)
        for i, tt in enumerate([1.5, 6.5, 11.0, 16.0]):  # quadros-chave para conferência
            if tt < dur:
                await pg.evaluate(f"render({tt})"); await pg.screenshot(path=str(tmp / f"k{i}.png"))
        await b.close()
    wav = tmp / "trilha.wav"; trilha(dur, wav)
    mp4 = OUT / f"{nome}-sem-voz.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(tmp / "%05d.jpg"), "-i", str(wav),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium", "-c:a", "aac", "-b:a", "160k",
                    "-shortest", "-movflags", "+faststart", str(mp4)], check=True)
    shutil.copy(wav, OUT / f"{nome}-trilha.wav")
    return tmp


if __name__ == "__main__":
    alvo = sys.argv[1:] or list(VIDEOS)
    for nome in VIDEOS:
        if any(nome.startswith(a) for a in alvo):
            html, dur = VIDEOS[nome]; asyncio.run(render(nome, html, dur)); print("ok", nome)
