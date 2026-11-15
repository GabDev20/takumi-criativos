# -*- coding: utf-8 -*-
"""Capas das 5 coleções + capa do pacote, a partir das páginas reais dos PDFs.
Saída: out/capas/colecao-N.png (1200x1600), out/capas/colecao-N-cakto.png (600x500), pacote-500.png, mockup-500.png"""
import os, sys, glob, subprocess, base64, asyncio
sys.path.insert(0, os.path.dirname(__file__))
from conteudo import COLECOES
from playwright.async_api import async_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = os.path.join(os.path.dirname(RAIZ), "kit-natal", "fonts")
OUT = os.path.join(RAIZ, "out", "capas"); os.makedirs(OUT, exist_ok=True)
PG = os.path.join(RAIZ, "out", "paginas"); os.makedirs(PG, exist_ok=True)

def b64(p):
    return base64.b64encode(open(p, "rb").read()).decode()

def paginas(col):
    pdf = glob.glob(os.path.join(RAIZ, "out", "pdf", "Colecao %d -*.pdf" % col["n"]))[0]
    res = []
    for pg in (3, 6, 4, 12):  # caça-palavras, pinte, labirinto, (2ª história) caça
        dst = os.path.join(PG, "c%d-p%d" % (col["n"], pg))
        if not os.path.exists(dst + ".png"):
            subprocess.run(["pdftoppm", "-r", "70", "-f", str(pg), "-l", str(pg), "-png", "-singlefile", pdf, dst], check=True)
        res.append(dst + ".png")
    return res

FONT_CSS = """
@font-face{font-family:B;src:url(data:font/woff2;base64,%s)}
@font-face{font-family:N;src:url(data:font/woff2;base64,%s)}
*{margin:0;box-sizing:border-box}body{font-family:N}
""" % (b64(os.path.join(FONTES, "baloo-2-latin-800-normal.woff2")), b64(os.path.join(FONTES, "nunito-latin-800-normal.woff2")))

def capa_html(col, imgs, w=1200, h=1600):
    c = col["cor"]
    pages = "".join('<img src="data:image/png;base64,%s" style="position:absolute;width:%dpx;left:%dpx;top:%dpx;transform:rotate(%ddeg);border-radius:10px;box-shadow:0 18px 40px rgba(0,0,0,.35);border:6px solid #fff">'
                    % (b64(p), 470, x, y, r) for p, (x, y, r) in zip(imgs[:3], [(90, 760, -9), (640, 760, 8), (365, 700, 0)]))
    return f"""<html><head><style>{FONT_CSS}</style></head><body>
<div style="width:{w}px;height:{h}px;position:relative;overflow:hidden;background:radial-gradient(circle at 50% 30%,{c}ee,{c} 60%,#0d1b2a 140%)">
 <div style="position:absolute;inset:0;background:repeating-linear-gradient(45deg,rgba(255,255,255,.04) 0 18px,transparent 18px 36px)"></div>
 <div style="position:absolute;top:70px;width:100%;text-align:center;font-family:B;color:#E9B44C;font-size:46px;letter-spacing:6px">ESTRELA GUIA KIDS</div>
 <div style="position:absolute;top:150px;left:50%;transform:translateX(-50%);background:#E9B44C;color:{c};font-family:B;font-size:54px;padding:6px 40px;border-radius:60px">COLEÇÃO {col['n']}</div>
 <div style="position:absolute;top:270px;width:100%;padding:0 70px;text-align:center;font-family:B;color:#fff;font-size:104px;line-height:1.02;text-shadow:0 6px 0 rgba(0,0,0,.25)">{col['nome']}</div>
 <div style="position:absolute;top:560px;width:100%;text-align:center;color:#fff;font-size:40px;opacity:.95">{col['sub']}</div>
 {pages}
 <div style="position:absolute;bottom:70px;left:50%;transform:translateX(-50%);background:#fff;color:{c};font-family:B;font-size:72px;padding:10px 54px;border-radius:24px;box-shadow:0 10px 0 #E9B44C;white-space:nowrap">100 ATIVIDADES</div>
 <div style="position:absolute;bottom:22px;width:100%;text-align:center;color:#fff;font-size:28px;opacity:.9">bíblicas para imprimir · 5 a 11 anos</div>
</div></body></html>"""

def pacote_html(capas, w=1600, h=1200):
    imgs = "".join('<img src="data:image/png;base64,%s" style="position:absolute;width:380px;left:%dpx;top:%dpx;transform:rotate(%ddeg);border-radius:14px;box-shadow:0 24px 50px rgba(0,0,0,.45)">'
                   % (b64(p), x, y, r) for p, (x, y, r) in zip(capas, [(90, 470, -14), (370, 420, -7), (610, 400, 0), (850, 420, 7), (1130, 470, 14)]))
    return f"""<html><head><style>{FONT_CSS}</style></head><body>
<div style="width:{w}px;height:{h}px;position:relative;overflow:hidden;background:radial-gradient(circle at 50% 20%,#2c5282,#1F3A5F 55%,#0d1b2a)">
 <div style="position:absolute;top:50px;width:100%;text-align:center;font-family:B;color:#E9B44C;font-size:44px;letter-spacing:6px">ESTRELA GUIA KIDS</div>
 <div style="position:absolute;top:110px;width:100%;text-align:center;font-family:B;color:#fff;font-size:150px;line-height:1">500 ATIVIDADES</div>
 <div style="position:absolute;top:270px;width:100%;text-align:center;font-family:B;color:#E9B44C;font-size:70px">BÍBLICAS PARA IMPRIMIR</div>
 {imgs}
 <div style="position:absolute;bottom:40px;width:100%;text-align:center;color:#fff;font-size:40px">5 coleções · 50 histórias · 10 tipos de atividade</div>
</div></body></html>"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(device_scale_factor=1)
        capas = []
        for col in COLECOES:
            await pg.set_viewport_size({"width": 1200, "height": 1600})
            await pg.set_content(capa_html(col, paginas(col))); await pg.wait_for_timeout(300)
            f = os.path.join(OUT, "colecao-%d.png" % col["n"]); await pg.screenshot(path=f); capas.append(f)
            # versão Cakto 600x500 (capa centralizada)
            await pg.set_viewport_size({"width": 600, "height": 500})
            await pg.set_content(f'<body style="margin:0;background:{col["cor"]};display:flex;align-items:center;justify-content:center;height:500px"><img src="data:image/png;base64,{b64(f)}" style="height:470px;border-radius:10px;box-shadow:0 10px 30px rgba(0,0,0,.4)"></body>')
            await pg.screenshot(path=os.path.join(OUT, "colecao-%d-cakto.png" % col["n"]))
        await pg.set_viewport_size({"width": 1600, "height": 1200})
        await pg.set_content(pacote_html(capas)); await pg.wait_for_timeout(300)
        await pg.screenshot(path=os.path.join(OUT, "pacote-500.png"))
        await pg.set_viewport_size({"width": 600, "height": 500})
        await pg.set_content(f'<body style="margin:0"><img src="data:image/png;base64,{b64(os.path.join(OUT, "pacote-500.png"))}" style="width:600px;height:500px;object-fit:cover"></body>')
        await pg.screenshot(path=os.path.join(OUT, "pacote-500-cakto.png"))
        await b.close()

asyncio.run(main())
for f in sorted(os.listdir(OUT)): print(f)
