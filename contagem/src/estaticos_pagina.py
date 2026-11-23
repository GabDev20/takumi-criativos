# Estáticos modelados das telas do quiz de referência (1ª pergunta com cards de imagem, "problema encontrado", bloco de oferta).
# Mesma mecânica visual, texto e arte 100% nossos, ângulo Contagem Regressiva. Sem corpo, sem antes/depois, sem promessa de kg.
# Uso: python3 src/estaticos_pagina.py -> out/estaticos/p{4,5,6}-*-{feed,stories}.png
import pathlib, asyncio
from playwright.async_api import async_playwright
from estaticos import CSS, FORMATOS

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "out/estaticos"

ICON = {
 "Réveillon": '<svg viewBox="0 0 48 48" fill="none" stroke="#FF5A36" stroke-width="3" stroke-linecap="round"><path d="M14 6h20l-2 14a8 8 0 0 1-16 0zM24 28v12M16 42h16"/><path d="M38 8l4-4M40 14h5M6 14h4" stroke="#F2B33D"/></svg>',
 "Viagem": '<svg viewBox="0 0 48 48" fill="none" stroke="#FF5A36" stroke-width="3" stroke-linejoin="round"><path d="M4 26l40-14-10 30-8-12-12 6 4-10z"/></svg>',
 "Casamento": '<svg viewBox="0 0 48 48" fill="none" stroke="#FF5A36" stroke-width="3"><circle cx="18" cy="28" r="11"/><circle cx="30" cy="28" r="11"/><path d="M24 6l3 5h-6z" stroke="#F2B33D"/></svg>',
 "Formatura": '<svg viewBox="0 0 48 48" fill="none" stroke="#FF5A36" stroke-width="3" stroke-linejoin="round"><path d="M2 18l22-10 22 10-22 10z"/><path d="M12 23v10c6 5 18 5 24 0V23M42 20v12"/></svg>',
}
X = '<span style="flex:none;width:44px;height:44px;border-radius:12px;background:#FF5A36;display:inline-flex;align-items:center;justify-content:center"><svg width="24" height="24" viewBox="0 0 20 20"><path d="M5 5l10 10M15 5L5 15" stroke="#fff" stroke-width="3"/></svg></span>'
V = '<span style="flex:none;width:44px;height:44px;border-radius:12px;background:#1F9D6B;display:inline-flex;align-items:center;justify-content:center"><svg width="26" height="26" viewBox="0 0 20 20"><path d="M4 10l4 4 8-8" stroke="#fff" stroke-width="3" fill="none"/></svg></span>'

def p4(h):  # 1ª pergunta do quiz: cards com imagem
    big = h > 1500
    cards = "".join(f'<div style="background:#fff;border:4px solid {"#FF5A36" if n=="Réveillon" else "#EADFD2"};border-radius:32px;padding:{44 if big else 30}px 20px;text-align:center;box-shadow:0 14px 34px rgba(23,24,28,.08)"><div style="width:{120 if big else 96}px;height:{120 if big else 96}px;margin:0 auto 18px">{s}</div><div style="font:800 40px Montserrat">{n}</div></div>' for n, s in ICON.items())
    return f"""
<div style="position:absolute;left:72px;right:72px;top:{110 if big else 60}px;height:14px;background:#F1E6D8;border-radius:9px"><div style="width:12%;height:100%;background:var(--coral);border-radius:9px"></div></div>
<div style="position:absolute;left:72px;right:72px;top:{200 if big else 120}px;text-align:center">
  <span style="background:var(--ink);color:#fff;font:700 30px Inter;padding:6px 16px;border-radius:8px">Para começarmos, me conte:</span>
  <h1 style="font-size:{82 if big else 72}px;margin-top:30px">Qual é a <em>sua data?</em></h1>
</div>
<div style="position:absolute;left:72px;right:72px;top:{560 if big else 400}px;display:grid;grid-template-columns:1fr 1fr;gap:26px">{cards}</div>
<div style="position:absolute;left:72px;right:72px;bottom:{170 if big else 60}px;text-align:center">
  <p class=sub style="font-size:32px">Responda e veja quantos treinos de 15 minutos ainda cabem até lá.</p>
  <p style="font:700 26px Inter;color:var(--mute);margin-top:20px">TEMPO ESTIMADO: 40 SEGUNDOS</p>
</div>"""

def p5(h):  # tela "problema encontrado"
    big = h > 1500
    itens = ["Treino sem começo e fim definidos", "Treino longo demais para dezembro", "Sem saber o que fazer em cada dia", "Sem uma data puxando você"]
    lis = "".join(f'<div style="display:flex;gap:22px;align-items:center;font:600 38px/1.25 Inter">{X}<span>{t}</span></div>' for t in itens)
    return f"""
<div style="position:absolute;left:60px;right:60px;top:{150 if big else 60}px;background:var(--ink);color:#fff;border-radius:36px;padding:46px;text-align:center">
  <div style="font:800 30px Inter;color:var(--gold);letter-spacing:.12em">&#9888; PROBLEMA ENCONTRADO &#9888;</div>
  <h1 style="color:#fff;font-size:66px;margin-top:16px">Não é preguiça.<br>É falta de prazo.</h1>
</div>
<div style="position:absolute;left:72px;right:72px;top:{560 if big else 400}px;display:flex;flex-direction:column;gap:{34 if big else 24}px">{lis}</div>
<div style="position:absolute;left:72px;right:72px;bottom:{180 if big else 64}px;text-align:center">
  <p style="font:900 40px Montserrat;margin-bottom:30px">MAS CALMA, ISSO TEM SOLUÇÃO</p>
  <span class=cta>Fazer o teste gratuito <i></i></span>
</div>"""

def p6(h):  # bloco de oferta
    big = h > 1500
    itens = ["21 treinos guiados de 15 minutos", "Calendário da contagem regressiva", "Versão leve e puxada de cada exercício", "Plano adaptado se faltar menos de 21 dias"]
    lis = "".join(f'<div style="display:flex;gap:22px;align-items:center;font:600 36px/1.25 Inter">{V}<span>{t}</span></div>' for t in itens)
    return f"""
<div class=brand style="--top:{110 if big else 60}px">Contagem Regressiva<small>Em casa · sem equipamento</small></div>
<div style="position:absolute;left:72px;right:72px;top:{290 if big else 180}px"><h1 style="font-size:{74 if big else 64}px">Você vai receber <em>no desafio:</em></h1></div>
<div style="position:absolute;left:72px;right:72px;top:{560 if big else 400}px;display:flex;flex-direction:column;gap:{30 if big else 20}px">{lis}</div>
<div style="position:absolute;left:72px;right:72px;bottom:{170 if big else 56}px;border:5px dashed var(--coral);border-radius:36px;padding:{40 if big else 28}px;text-align:center;background:#fff">
  <span style="background:var(--ink);color:#fff;font:800 24px Inter;letter-spacing:.08em;padding:8px 18px;border-radius:999px">COMECE HOJE · ÚLTIMAS VAGAS</span>
  <div style="font:600 34px Inter;color:var(--mute);margin-top:22px;text-decoration:line-through">De R$ 97 por</div>
  <div style="font:900 {120 if big else 104}px/1 Montserrat">R$ 29,90</div>
</div>"""

PECAS = {"p4-qual-sua-data": p4, "p5-problema-encontrado": p5, "p6-oferta": p6}

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for nome, fn in PECAS.items():
            for fmt, h in FORMATOS.items():
                pg = await b.new_page(viewport={"width": 1080, "height": h})
                await pg.set_content(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body style='--h:{h}px'>{fn(h)}</body></html>")
                await pg.wait_for_timeout(250)
                await pg.screenshot(path=str(OUT / f"{nome}-{fmt}.png")); await pg.close()
        await b.close()

if __name__ == "__main__":
    asyncio.run(main())
