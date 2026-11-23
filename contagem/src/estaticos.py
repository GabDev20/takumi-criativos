# Estáticos do ângulo "Contagem Regressiva" (modelagem do quiz do Desafio Desincha Barriga, outro público/gatilho).
# Gatilho: uma data marcada (Réveillon, viagem, casamento, formatura). Sem corpo, sem antes/depois, sem promessa de resultado.
# Uso: python3 src/estaticos.py  ->  out/estaticos/*.png (feed 1080x1350 e stories 1080x1920)
import pathlib, asyncio
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "out/estaticos"; OUT.mkdir(parents=True, exist_ok=True)

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
:root{--cream:#FFF4E8;--ink:#17181C;--coral:#FF5A36;--gold:#F2B33D;--green:#1F9D6B;--mute:#6B6660}
body{width:1080px;height:var(--h);background:var(--cream);font-family:'Inter',sans-serif;color:var(--ink);overflow:hidden;position:relative}
.brand{position:absolute;left:72px;top:var(--top);font:800 26px 'Montserrat';letter-spacing:.18em;text-transform:uppercase;color:var(--coral)}
.brand small{display:block;color:var(--mute);letter-spacing:.12em;font-size:20px;margin-top:6px}
h1{font:900 86px/1.02 'Montserrat';letter-spacing:-.02em}
h1 em{font-style:normal;color:var(--coral)}
.sub{font:500 36px/1.35 'Inter';color:#3a3632}
.cta{display:inline-flex;align-items:center;gap:18px;background:var(--ink);color:#fff;font:800 34px 'Montserrat';padding:30px 46px;border-radius:999px}
.cta i{display:inline-block;width:22px;height:22px;border-top:5px solid var(--gold);border-right:5px solid var(--gold);transform:rotate(45deg)}
.note{font:500 22px 'Inter';color:var(--mute)}
.check{display:inline-block;width:34px;height:18px;border-left:7px solid currentColor;border-bottom:7px solid currentColor;transform:rotate(-45deg) translate(3px,-4px)}
"""

# ---------- S1: o quiz ----------
def s1(h):
    big = h > 1500
    return f"""
<div class=brand style="--top:{110 if big else 64}px">Contagem Regressiva<small>Desafio de 21 dias · 15 min por dia</small></div>
<div style="position:absolute;left:72px;right:72px;top:{300 if big else 200}px">
  <h1>Tem uma data marcada no <em>seu calendário?</em></h1>
  <p class=sub style="margin-top:26px">Réveillon, viagem, casamento, formatura. Responda e receba o seu plano dia a dia até lá.</p>
</div>
<div style="position:absolute;left:72px;right:72px;top:{860 if big else 640}px;background:#fff;border-radius:36px;padding:44px;box-shadow:0 24px 60px rgba(23,24,28,.12)">
  <div style="display:flex;justify-content:space-between;font:700 22px Inter;color:var(--mute)"><span>PERGUNTA 1 DE 3</span><span>40 SEGUNDOS</span></div>
  <div style="height:10px;background:#F1E6D8;border-radius:9px;margin:18px 0 30px"><div style="width:33%;height:100%;background:var(--coral);border-radius:9px"></div></div>
  <div style="font:800 40px/1.2 Montserrat;margin-bottom:28px">Quantos dias faltam para a sua data?</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:18px">
    {''.join(f'<div style="border:3px solid {"var(--coral)" if i==1 else "#EADFD2"};background:{"#FFF0EB" if i==1 else "#fff"};border-radius:22px;padding:26px 24px;font:700 32px Inter">{t}</div>' for i,t in enumerate(["Menos de 15","15 a 40","40 a 60","Mais de 60"]))}
  </div>
</div>
<div style="position:absolute;left:72px;bottom:{170 if big else 70}px;display:flex;align-items:center;gap:28px">
  <span class=cta>Fazer o teste <i></i></span><span class=note>Gratuito. Não é avaliação médica.</span>
</div>"""

# ---------- S2: o calendário de 21 dias ----------
def s2(h):
    big = h > 1500
    cells = ""
    for d in range(1, 22):
        done = d <= 6; today = d == 7; last = d == 21
        bg = "var(--ink)" if done else ("var(--coral)" if today else ("var(--gold)" if last else "#fff"))
        fg = "#fff" if (done or today) else "var(--ink)"
        mark = '<span class=check style="color:var(--gold);position:absolute;right:16px;bottom:22px;width:26px;height:14px;border-width:6px"></span>' if done else ""
        lab = "HOJE" if today else ("SUA DATA" if last else "")
        cells += f'<div style="position:relative;background:{bg};color:{fg};border-radius:20px;height:118px;padding:14px 16px;border:2px solid {"transparent" if (done or today or last) else "#EADFD2"}"><div style="font:900 40px Montserrat">{d}</div><div style="font:800 15px Inter;letter-spacing:.08em;margin-top:6px">{lab}</div>{mark}</div>'
    return f"""
<div class=brand style="--top:{110 if big else 64}px">Contagem Regressiva<small>Desafio de 21 dias</small></div>
<div style="position:absolute;left:72px;right:72px;top:{300 if big else 190}px">
  <h1 style="font-size:92px"><em>15 minutos</em> por dia.<br>Na sala. Sem equipamento.</h1>
</div>
<div style="position:absolute;left:72px;right:72px;top:{720 if big else 560}px;display:grid;grid-template-columns:repeat(7,1fr);gap:12px">{cells}</div>
<div style="position:absolute;left:72px;right:72px;top:{1160 if big else 980}px" class=sub>Um treino curto por dia, contado até a sua data. Você só abre e aperta o play.</div>
<div style="position:absolute;left:72px;bottom:{170 if big else 64}px"><span class=cta>Montar meu plano <i></i></span></div>"""

# ---------- S3: notificações da tela de bloqueio ----------
def s3(h):
    big = h > 1500
    def notif(app, title, body, when, accent):
        return f"""<div style="background:rgba(255,255,255,.92);border-radius:30px;padding:26px 30px;display:flex;gap:22px;align-items:flex-start;box-shadow:0 10px 30px rgba(0,0,0,.18)">
          <div style="width:64px;height:64px;border-radius:16px;background:{accent};flex:none;display:flex;align-items:center;justify-content:center;color:#fff;font:900 30px Montserrat">{app}</div>
          <div style="flex:1"><div style="display:flex;justify-content:space-between;font:600 22px Inter;color:#6b6660"><span>{title}</span><span>{when}</span></div>
          <div style="font:600 30px/1.3 Inter;color:#17181C;margin-top:6px">{body}</div></div></div>"""
    return f"""
<div style="position:absolute;inset:0;background:linear-gradient(160deg,#1d2440 0%,#3b2a4a 55%,#ff7a4d 130%)"></div>
<div style="position:absolute;left:0;right:0;top:{150 if big else 70}px;text-align:center;color:#fff">
  <div style="font:600 30px Inter;opacity:.85">terça-feira, 24 de novembro</div>
  <div style="font:300 190px/1 'Inter Display';letter-spacing:-.03em">7:02</div>
</div>
<div style="position:absolute;left:60px;right:60px;top:{560 if big else 400}px;display:flex;flex-direction:column;gap:18px">
  {notif("31","Calendário","Réveillon na praia. Faltam 37 dias.","agora","#FF5A36")}
  {notif("21","Contagem Regressiva","Treino de hoje: 15 minutos. Dia 1 de 21.","agora","#17181C")}
</div>
<div style="position:absolute;left:72px;right:72px;bottom:{220 if big else 80}px;color:#fff">
  <h1 style="color:#fff;font-size:84px">Ainda dá tempo.<br><span style="color:var(--gold)">Se começar hoje.</span></h1>
  <div style="margin-top:34px;display:flex;align-items:center;gap:26px"><span class=cta style="background:#fff;color:var(--ink)">Ver meu plano <i></i></span><span class=note style="color:#e9dcf0">Teste gratuito de 40 s</span></div>
</div>"""

PECAS = {"s1-quiz-data": s1, "s2-calendario-21": s2, "s3-notificacao": s3}
FORMATOS = {"feed": 1350, "stories": 1920}

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for nome, fn in PECAS.items():
            for fmt, h in FORMATOS.items():
                pg = await b.new_page(viewport={"width": 1080, "height": h}, device_scale_factor=1)
                await pg.set_content(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body style='--h:{h}px'>{fn(h)}</body></html>")
                await pg.wait_for_timeout(250)
                await pg.screenshot(path=str(OUT / f"{nome}-{fmt}.png"))
                await pg.close()
        await b.close()

if __name__ == "__main__":
    asyncio.run(main())
