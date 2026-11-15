# Estáticos da oferta "500 Atividades Bíblicas" (CODEX colecao, prioridade 1).
# Páginas reais: renderizadas dos PDFs (pdftoppm -r 110 ou pypdfium2 equivalente) em out/pg110/.
# Versão com o preço R$ 27,90 (pacote + 5 músicas). Uso: python colecao/src/criativos_colecao_2790.py -> out/criativos/estaticos-2790/
import pathlib, base64, io, glob
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = ROOT.parent
PG = ROOT / "out" / "pg110"; CAPAS = ROOT / "out" / "capas"
OUT = ROOT / "out" / "criativos" / "estaticos-2790"; OUT.mkdir(parents=True, exist_ok=True)
FONTS = REPO / "kit-natal" / "fonts"
TIPOS = ["Caça-palavras", "Labirinto", "Código secreto", "Pinte por número", "Complete o versículo",
         "Verdadeiro ou falso", "Ligue as colunas", "Palavras embaralhadas", "Copie e ilustre", "Acróstico"]


def garantir_paginas():
    """Renderiza capa (pág. 1) e as 20 primeiras atividades (pág. 3 a 22) de cada coleção, a 110 dpi."""
    PG.mkdir(parents=True, exist_ok=True)
    if len(list(PG.glob("*.png"))) >= 105: return
    import pypdfium2 as pdfium
    for n in range(1, 6):
        d = pdfium.PdfDocument(glob.glob(str(ROOT / "out" / "pdf" / f"Colecao {n} -*.pdf"))[0])
        for i in [1] + list(range(3, 23)):
            d[i - 1].render(scale=110 / 72).to_pil().save(PG / f"c{n}-p{i}.png")


def pag(c, tipo, hist=0):
    """Página real: coleção c, tipo 0..9, história 0 ou 1."""
    return PG / f"c{c}-p{3 + hist * 10 + tipo}.png"


_cache = {}
def b64(p, w=640):
    p = pathlib.Path(p)
    if (p, w) not in _cache:
        im = Image.open(p).convert("RGB"); im.thumbnail((w, w * 2))
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=86)
        _cache[(p, w)] = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    return _cache[(p, w)]


f64 = lambda n: "data:font/woff2;base64," + base64.b64encode((FONTS / n).read_bytes()).decode()
CSS = f"""@font-face{{font-family:Baloo;font-weight:800;src:url({f64('baloo-2-latin-800-normal.woff2')})}}
@font-face{{font-family:Nunito;font-weight:700;src:url({f64('nunito-latin-700-normal.woff2')})}}
@font-face{{font-family:Nunito;font-weight:800;src:url({f64('nunito-latin-800-normal.woff2')})}}
*{{box-sizing:border-box}}body{{margin:0;background:radial-gradient(circle at 50% 35%,#2c4f7c,#1F3A5F 70%);font-family:Nunito;color:#fff;overflow:hidden;text-align:center;display:flex;flex-direction:column}}
.rib{{align-self:center;background:#C0392B;font-family:Baloo;font-weight:800;letter-spacing:.05em;text-transform:uppercase;padding:12px 34px 8px;font-size:32px;border-radius:999px;margin-top:40px}}
.h{{font-family:Baloo;font-weight:800;line-height:1.02;margin:22px 50px 0}}.g{{color:#E9B44C}}
.sub{{font-weight:800;font-size:38px;margin:14px 60px 0;color:#f3f6fa}}
.vis{{flex:1;position:relative;margin:20px 0 10px}}
.pg{{position:absolute;border:6px solid #E9B44C;border-radius:8px;box-shadow:0 20px 44px rgba(0,0,0,.45);background:#fff}}
.burst{{position:absolute;background:#E9B44C;color:#1F3A5F;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:Baloo;font-weight:800;line-height:.95;transform:rotate(-8deg);box-shadow:0 12px 0 rgba(0,0,0,.25);border:8px solid #fff;z-index:20}}
.burst span{{white-space:nowrap}}
.cta{{align-self:center;white-space:nowrap;background:#1E8E5A;color:#fff;font-family:Baloo;font-weight:800;border-radius:999px;box-shadow:0 8px 0 #14633e;font-size:46px;padding:16px 56px 12px;margin-bottom:44px}}
.chips{{display:flex;flex-wrap:wrap;justify-content:center;gap:12px;margin:18px 40px 0}}.chips span{{background:#fff;color:#1F3A5F;font-weight:800;font-size:31px;padding:8px 22px;border-radius:999px}}
.tag{{position:absolute;background:#1F3A5F;color:#fff;font-weight:800;font-size:24px;padding:4px 12px;border-radius:8px;white-space:nowrap;z-index:3}}"""


def page(W, H, ribbon, title, tsize, vis, cta, sub="", chips=None):
    tall = H > 1400
    pad = "padding:250px 0 250px" if tall else ""
    ch = "" if not chips else '<div class="chips">' + "".join(f"<span>{c}</span>" for c in chips) + "</div>"
    return f"""<html><head><style>{CSS} body{{width:{W}px;height:{H}px;{pad}}} .cta{{margin-bottom:{10 if tall else 44}px}} .rib{{margin-top:{0 if tall else 40}px}}</style></head><body>
<div class="rib">{ribbon}</div>
<div class="h" style="font-size:{tsize}px">{title.replace("R$ ", "R$&nbsp;")}</div>{f'<div class="sub">{sub}</div>' if sub else ''}{ch}
<div class="vis">{vis}</div>
<div class="cta">{cta}</div></body></html>"""


def fan(imgs, w, cx=540, top=20, spread=150, rot=7):
    n = len(imgs); out = ""
    for k, p in enumerate(imgs):
        o = k - (n - 1) / 2
        out += f'<img class="pg" src="{b64(p)}" style="width:{w}px;left:{cx - w / 2 + o * spread:.0f}px;top:{top + abs(o) * 18:.0f}px;transform:rotate({o * rot:.1f}deg);z-index:{10 - int(abs(o) * 2)}">'
    return out


def burst(txt_top, preco, txt_bot, right=30, bottom=10, size=300):
    return (f'<div class="burst" style="right:{right}px;bottom:{bottom}px;width:{size}px;height:{size}px">'
            f'<span style="font-size:{size * .12:.0f}px">{txt_top}</span><span style="font-size:{size * .25:.0f}px">{preco}</span>'
            f'<span style="font-size:{size * .095:.0f}px">{txt_bot}</span></div>')


def calendario(mes, ini, dias, x, y, w):
    cells = "".join("<i></i>" for _ in range(ini)) + "".join(f"<b>{d}</b>" for d in range(1, dias + 1))
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;background:#fff;border-radius:22px;overflow:hidden;box-shadow:0 18px 40px rgba(0,0,0,.4);color:#1F3A5F">'
            f'<div style="background:#C0392B;color:#fff;font-family:Baloo;font-weight:800;font-size:40px;padding:8px 0 4px">{mes}</div>'
            f'<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:6px;padding:14px;font-weight:800;font-size:22px">{cells}</div></div>')


CAL_CSS = "<style>.vis b{display:block;background:#FFF1CF;border-radius:6px;padding:4px 0}.vis i{display:block}</style>"


def criativos(W, H):
    tall = H > 1400
    vh = 1920 - 500 - 560 if tall else 1350 - 520  # altura aproximada da área visual
    S = lambda a, b: b if tall else a
    C = []
    # 01 número + preço
    v = fan([pag(1, 0), pag(2, 1), pag(3, 3), pag(4, 2), pag(5, 9), pag(2, 6, 1)], S(300, 340), top=S(10, 40), spread=S(125, 135))
    v += burst("tudo por", "R$ 27,90", "pagamento único", bottom=S(0, 10), size=S(300, 330))
    C.append(("est-01-500-preco", page(W, H, "Coleção Atividades Bíblicas", '<span class="g">500</span> atividades bíblicas para imprimir', S(80, 92), v,
                                       "Quero as 500 atividades", sub="5 a 11 anos · com gabarito")))
    # 02 centavos
    grid = "".join(f'<img class="pg" src="{b64(p, 420)}" style="width:{S(190, 220)}px;left:{60 + (k % 3) * S(220, 250) + S(70, 30)}px;top:{(k // 3) * S(270, 320) + 10}px;transform:rotate({[-4, 3, -2, 4, -3, 2][k]}deg)">'
                   for k, p in enumerate([pag(1, 1), pag(3, 0), pag(5, 3), pag(2, 7), pag(4, 4), pag(1, 2, 1)]))
    grid += burst("500 atividades", "R$ 27,90", "pagamento único", right=20, bottom=S(10, 40), size=S(270, 300))
    C.append(("est-02-centavos", page(W, H, "500 atividades · pagamento único", 'Menos de <span class="g">R$ 0,06</span> por atividade', S(96, 108), grid,
                                      "Imprima hoje", sub="R$ 27,90 ÷ 500 atividades = R$ 0,056 cada")))
    # 03 telas
    ph_h = S(560, 700)
    v = (f'<div style="position:absolute;left:0;top:0;width:50%;height:100%;background:rgba(0,0,0,.35)"></div>'
         f'<div style="position:absolute;left:{S(120, 110)}px;top:{S(40, 60)}px;width:{ph_h * .5:.0f}px;height:{ph_h}px;background:#2b2f35;border:14px solid #555b63;border-radius:46px;filter:grayscale(1)">'
         f'<div style="position:absolute;inset:18px;background:#111;border-radius:26px"></div><div style="position:absolute;top:8px;left:35%;width:30%;height:10px;background:#555b63;border-radius:6px"></div></div>'
         f'<div class="tag" style="left:{S(150, 140)}px;top:{S(40, 60) + ph_h + 24}px;background:#555b63;font-size:30px">tela apagada</div>'
         f'<img class="pg" src="{b64(pag(1, 3))}" style="width:{S(260, 300)}px;left:{S(600, 590)}px;top:{S(30, 50)}px;transform:rotate(-5deg)">'
         f'<img class="pg" src="{b64(pag(2, 1))}" style="width:{S(260, 300)}px;left:{S(760, 740)}px;top:{S(170, 230)}px;transform:rotate(6deg)">'
         f'<div class="tag" style="left:{S(650, 650)}px;top:{S(40, 60) + ph_h + 24}px;background:#1E8E5A;font-size:30px">papel e lápis</div>')
    C.append(("est-03-telas", page(W, H, "Atividades bíblicas para imprimir", 'Menos tela. <span class="g">Mais Bíblia.</span>', S(104, 116), v,
                                   "500 atividades por R$ 27,90", sub="Caça-palavras, labirinto, código secreto, pinte por número…")))
    # 04 economia
    caps = "".join(f'<img src="{b64(CAPAS / f"colecao-{n}.png", 360)}" style="position:absolute;width:{S(150, 170)}px;left:{40 + k * S(196, 200)}px;top:{S(10, 30)}px;border-radius:8px;box-shadow:0 10px 24px rgba(0,0,0,.4)">'
                   for k, n in enumerate(range(1, 6)))
    caps += "".join(f'<div class="tag" style="left:{40 + k * S(196, 200) + S(18, 28)}px;top:{S(220, 270)}px">R$ 19,90</div>' for k in range(5))
    caps += (f'<div style="position:absolute;left:0;right:0;top:{S(270, 330)}px;font-family:Baloo;font-weight:800;font-size:{S(54, 62)}px">5 avulsas: <s style="color:#ffb3a8">R$ 99,50</s></div>'
             f'<div style="position:absolute;left:0;right:0;top:{S(345, 420)}px;font-size:{S(60, 70)}px;color:#E9B44C">▼</div>'
             f'<img src="{b64(CAPAS / "pacote-500.png", 700)}" style="position:absolute;width:{S(470, 470)}px;left:{S(80, 60)}px;top:{S(420, 500)}px;border-radius:10px;box-shadow:0 14px 30px rgba(0,0,0,.4)">'
             + burst("pacote completo", "R$ 27,90", "economize R$ 71,60", right=S(40, 40), bottom=S(10, 60), size=S(300, 320)))
    C.append(("est-04-economia", page(W, H, "A conta é simples", '5 coleções avulsas: R$ 99,50<br><span class="g">Pacote completo: R$ 27,90</span>', S(72, 84), caps,
                                      "Economize R$ 71,60")))
    # 05 férias
    v = CAL_CSS + calendario("Dezembro", 2, 31, S(50, 50), S(20, 40), S(470, 480)) + calendario("Janeiro", 5, 31, S(560, 550), S(20, 40), S(470, 480))
    v += fan([pag(3, 1), pag(1, 0), pag(4, 3)], S(230, 280), cx=S(420, 420), top=S(370, 460), spread=S(170, 200))
    v += burst("500 atividades", "R$ 27,90", "imprima hoje", right=20, bottom=S(0, 20), size=S(270, 300))
    C.append(("est-05-ferias", page(W, H, "Dezembro e janeiro", 'Férias chegando: <span class="g">500 ideias sem tela</span>', S(88, 100), v,
                                    "Quero as 500 atividades")))
    # 06 10 tipos
    cw = S(176, 186); gx = (W - 5 * cw) / 6
    grid = ""
    for t in range(10):
        x = gx + (t % 5) * (cw + gx); y = (t // 5) * S(310, 390) + 10
        grid += f'<img class="pg" src="{b64(pag(1 + t % 5, t), 360)}" style="width:{cw}px;left:{x:.0f}px;top:{y}px;border-width:4px">'
        grid += f'<div class="tag" style="left:{x - 6:.0f}px;top:{y + cw * 1.41 - 10:.0f}px;width:{cw + 12}px;font-size:{S(19, 21)}px;white-space:normal;line-height:1.1">{TIPOS[t]}</div>'
    C.append(("est-06-10-tipos", page(W, H, "50 histórias da Bíblia", '<span class="g">10 tipos</span> de atividade × <span class="g">50 histórias</span>', S(80, 92), grid,
                                      "500 atividades por R$ 27,90", sub=S("", "Uma página de cada tipo, do jeito que você imprime"))))
    # 07 professora
    v = fan([pag(2, 4), pag(1, 1), pag(3, 0), pag(5, 6), pag(4, 3)], S(300, 340), top=S(10, 40), spread=S(150, 155))
    v += burst("pagamento único", "R$ 27,90", "500 atividades", bottom=S(0, 20), size=S(290, 320))
    C.append(("est-07-professora", page(W, H, "Para o ministério infantil", 'Um ano de atividades para a salinha por <span class="g">R$ 27,90</span>', S(80, 90), v,
                                        "Quero para a minha sala", chips=["50 histórias", "10 tipos", "5 a 11 anos", "com gabarito"])))
    # 08 coleções
    v = fan([CAPAS / f"colecao-{n}.png" for n in range(1, 6)], S(330, 380), top=S(20, 50), spread=S(150, 160), rot=6)
    v += burst("as 5 por", "R$ 27,90", "pagamento único", bottom=S(0, 20), size=S(280, 310))
    C.append(("est-08-colecoes", page(W, H, "Coleção Atividades Bíblicas", '5 coleções. <span class="g">500 atividades.</span> 1 pagamento.', S(84, 96), v,
                                      "Ver as 5 coleções", sub="Antigo Testamento · Vida de Jesus · Parábolas · Milagres · Orações e Salmos")))
    # 09 100 por 19,90
    v = (f'<img src="{b64(CAPAS / "colecao-2.png", 700)}" style="position:absolute;width:{S(400, 470)}px;left:{S(90, 70)}px;top:{S(10, 40)}px;border-radius:10px;box-shadow:0 20px 44px rgba(0,0,0,.45);transform:rotate(-4deg)">'
         f'<img class="pg" src="{b64(pag(2, 0))}" style="width:{S(270, 310)}px;left:{S(560, 590)}px;top:{S(60, 100)}px;transform:rotate(5deg)">'
         + burst("100 atividades", "R$ 19,90", "1 coleção", right=S(40, 50), bottom=S(10, 40), size=S(290, 320)))
    C.append(("est-09-100", page(W, H, "Comece com uma coleção", '100 atividades bíblicas por <span class="g">R$ 19,90</span>', S(90, 100), v,
                                 "ou leve as 500 por R$ 27,90")))
    # 10 imprima hoje
    st = S(300, 310); y0 = S(20, 40)
    passos = [("1", "Chega no e-mail", "em minutos"), ("2", "Você imprime", "papel A4 comum"), ("3", "A criança faz", "e você confere no gabarito")]
    v = ""
    for k, (n, a, b) in enumerate(passos):
        x = 45 + k * (st + 30)
        v += (f'<div style="position:absolute;left:{x}px;top:{y0}px;width:{st}px;height:{S(560, 760)}px;background:#fff;border-radius:26px;color:#1F3A5F;box-shadow:0 16px 36px rgba(0,0,0,.4)">'
              f'<div style="margin:18px auto 0;width:74px;height:74px;border-radius:50%;background:#E9B44C;font-family:Baloo;font-weight:800;font-size:50px;line-height:84px">{n}</div>'
              f'<div style="font-family:Baloo;font-weight:800;font-size:40px;margin-top:10px">{a}</div><div style="font-weight:800;font-size:25px;color:#5b6876">{b}</div></div>')
        img = [CAPAS / "pacote-500.png", pag(4, 0), pag(1, 3)][k]
        v += f'<img src="{b64(img, 420)}" style="position:absolute;left:{x + 25}px;top:{y0 + 230}px;width:{st - 50}px;border-radius:8px;border:3px solid #E9B44C">'
    C.append(("est-10-imprima-hoje", page(W, H, "500 atividades · R$ 27,90", 'Compre agora, <span class="g">imprima em 5 minutos</span>', S(90, 100), v,
                                          "Quero imprimir hoje")))
    return C


def main():
    garantir_paginas()
    feitos = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for sz, (W, H) in [("feed", (1080, 1350)), ("stories", (1080, 1920))]:
            for nome, html in criativos(W, H):
                pg = b.new_page(viewport={"width": W, "height": H}); pg.set_content(html); pg.wait_for_timeout(300)
                over = pg.evaluate("""() => { const b=document.body, r=[]; for (const e of b.querySelectorAll('.h,.sub,.cta,.chips,.rib')) {
                    const q=e.getBoundingClientRect(); if (q.top<0||q.bottom>innerHeight||q.left<0||q.right>innerWidth||e.scrollWidth>e.clientWidth+2) r.push(e.className) } return r }""")
                p = OUT / f"{nome}-{sz}.png"; pg.screenshot(path=str(p)); pg.close(); feitos.append(p)
                print(p.name, "CORTE:" + ",".join(over) if over else "ok")
        b.close()
    th = [Image.open(p) for p in feitos]
    th = [im.resize((270, int(im.height * 270 / 1080))) for im in th]
    c = Image.new("RGB", (10 * 280 + 10, 10 + 338 + 10 + 480 + 10), "white")
    for k, im in enumerate(th):
        c.paste(im, (10 + (k % 10) * 280, 10 if k < 10 else 358))
    c.save(OUT / "contato.png"); print("contato.png")


if __name__ == "__main__":
    main()
