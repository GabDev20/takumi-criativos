# Estáticos "formato bom" dos 3 quizzes (foco/CODEX.md, 16/11/2026).
# Foto realista (gpt-image, em out/criativos/_fotos/<produto>-<angulo>-<v>.png) + faixas montadas em código (Playwright).
# Uso: python foco/src/criativos_quiz.py [foco|leitura|biblico]
import sys, pathlib, base64, io
from PIL import Image, ImageFilter
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
FOTOS = ROOT / "out" / "criativos" / "_fotos"; SRC = ROOT / "out" / "criativos" / "_src"
FONTS = ROOT.parent / "kit-natal" / "fonts"
WIN = pathlib.Path("C:/Windows/Fonts")

# produto -> ângulo -> (balão, faixa verde, faixa vermelha, rodapé, mockup?)
ANG = {
    "foco": {
        "licao": ("Não consigo terminar!", "Mãe? A lição nunca termina?", "250 atividades de foco para imprimir · R$ 19,90", "Clique em saiba mais", True),
        "tela": ("Só mais 5 minutinhos!", "Troque 15 minutos de tela por 1 atividade", "250 atividades de atenção e calma · R$ 19,90", "Clique em saiba mais", True),
        "teste": ("Ué, o que era pra fazer?", "Qual habilidade de foco ele mais precisa treinar?", "Faça o teste de 1 minuto", "Faça o teste: toque em saiba mais", False),
    },
    "leitura": {
        "trava": ("Não sei ler isso!", "Mãe? Ele ainda trava na leitura?", "198 fichas da sílaba à frase · R$ 19,90", "Clique em saiba mais", True),
        "ferias": ("Já esqueci as letras...", "Férias chegando: ele vai esquecer o que aprendeu?", "15 minutos por dia de leitura em casa · R$ 19,90", "Clique em saiba mais", True),
        "fase": ("BA... BE... BI...", "Em que fase da leitura seu filho está?", "Descubra em 1 minuto: teste grátis", "Faça o teste: toque em saiba mais", False),
    },
    "biblico": {
        "celular": ("Só mais um vídeo!", "Mãe? Férias e ele só quer o celular?", "500 atividades bíblicas + 5 músicas · R$ 27,90", "Clique em saiba mais", True),
        "salinha": ("Que aula chataaa", "Tia? Já não sabe o que passar na salinha?", "500 atividades bíblicas para imprimir · R$ 27,90", "Clique em saiba mais", True),
        "plano": ("Agora é a minha vez!", "Monte o plano de férias sem tela em 1 minuto", "Responda 6 perguntas: é grátis", "Faça o teste: toque em saiba mais", False),
    },
}
MOCK = {"foco": SRC / "foco-p8.png", "leitura": SRC / "leitura-p4.png", "biblico": ROOT / "out" / "lovable" / "colecao" / "t-caca.jpg"}

# enquadramento por foto: (centro x 0..1, largura do recorte em fração da largura, lado do balão, y do balão em fração da foto)
CROP = {
    "foco-licao-1": (.50, .62, "r", .17), "foco-licao-2": (.52, .62, "l", .16), "foco-tela-1": (.56, .62, "l", .14),
    "foco-tela-2": (.50, .62, "r", .15), "foco-teste-1": (.44, .62, "r", .14), "foco-teste-2": (.53, .62, "l", .15),
    "leitura-trava-1": (.52, .62, "r", .12), "leitura-trava-2": (.50, .62, "r", .15), "leitura-ferias-1": (.55, .62, "r", .14),
    "leitura-ferias-2": (.42, .62, "r", .12), "leitura-fase-1": (.50, .62, "r", .12), "leitura-fase-2": (.45, .62, "r", .14),
    "biblico-celular-1": (.48, .62, "r", .12), "biblico-celular-2": (.50, .62, "r", .12), "biblico-salinha-1": (.55, .62, "l", .10),
    "biblico-salinha-2": (.42, .62, "r", .12), "biblico-plano-1": (.58, .80, "r", .08), "biblico-plano-2": (.47, .86, "r", .06),
}


def b64img(im, q=88):
    buf = io.BytesIO(); im.convert("RGB").save(buf, "JPEG", quality=q); return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def fundo(nome, W, H, top):
    """Recorte da foto na largura toda, começando em `top`; acima e abaixo, a própria foto desfocada."""
    src = Image.open(FOTOS / f"{nome}.png").convert("RGB")
    from PIL import ImageOps
    bbox = ImageOps.invert(src).point(lambda v: 255 if v > 12 else 0).getbbox()  # tira margens brancas que o gerador às vezes deixa
    if bbox: src = src.crop(bbox)
    cx, fw, _, _ = CROP[nome]
    fw = min(1.0, fw * 1280 / src.width) if src.width < 1200 else fw
    cw = int(src.width * fw); x0 = int(min(max(0, cx * src.width - cw / 2), src.width - cw))
    crop = src.crop((x0, 0, x0 + cw, src.height))
    fh = int(crop.height * W / crop.width)
    foto = crop.resize((W, fh), Image.LANCZOS)
    bg = src.resize((int(src.width * H / src.height), H), Image.LANCZOS)
    bx = (bg.width - W) // 2; bg = bg.crop((bx, 0, bx + W, H)).filter(ImageFilter.GaussianBlur(30))
    bg = Image.blend(bg, Image.new("RGB", bg.size, (20, 28, 40)), .25)
    bg.paste(foto, (0, top)); return bg, top, fh


f64 = lambda p, m: f"data:{m};base64," + base64.b64encode(pathlib.Path(p).read_bytes()).decode()
CSS = f"""@font-face{{font-family:Baloo;font-weight:800;src:url({f64(FONTS / 'baloo-2-latin-800-normal.woff2', 'font/woff2')})}}
@font-face{{font-family:Mao;src:url({f64(WIN / 'segoeprb.ttf', 'font/ttf')})}}
*{{box-sizing:border-box}}body{{margin:0;overflow:hidden;position:relative;font-family:Baloo}}
.bg{{position:absolute;inset:0;width:100%;height:100%}}
.fx{{position:absolute;left:50%;color:#fff;font-weight:800;text-align:center;line-height:1.08;padding:14px 30px 8px;border-radius:14px;box-shadow:0 8px 22px rgba(0,0,0,.35)}}
.verde{{background:#4CD964;transform:translateX(-50%) rotate(-2deg)}}
.verm{{background:#E53950;transform:translateX(-50%) rotate(-3deg)}}
.rod{{background:#4CD964;transform:translateX(-50%) rotate(-2deg);white-space:nowrap}}
.bal{{position:absolute;background:#fff;border:5px solid #111;border-radius:40px;padding:22px 30px;font-family:Mao,'Segoe Print','Comic Sans MS',Courier,monospace;font-size:44px;line-height:1.15;color:#111;text-align:center;box-shadow:0 6px 16px rgba(0,0,0,.25)}}
.bal:after,.bal:before{{content:"";position:absolute;bottom:-34px;border-style:solid}}
.bal:before{{border-width:36px 22px 0 22px;border-color:#111 transparent transparent transparent}}
.bal:after{{bottom:-25px;border-width:30px 17px 0 17px;border-color:#fff transparent transparent transparent}}
.bal.l:before{{right:70px}}.bal.l:after{{right:75px}}.bal.r:before{{left:70px}}.bal.r:after{{left:75px}}
.mock{{position:absolute;border:6px solid #fff;border-radius:8px;box-shadow:0 14px 30px rgba(0,0,0,.45);transform:rotate(6deg)}}"""


def html(prod, ang, v, W, H):
    nome = f"{prod}-{ang}-{v}"
    bal, verde, verm, rod, mock = ANG[prod][ang]
    tall = H > 1400
    top = 600 if tall else 375
    bg, top, fh = fundo(nome, W, H, top)
    _, _, lado, by = CROP[nome]
    y_verde = 270 if tall else 50
    y_verm = 1330 if tall else 1050
    y_rod = 1560 if tall else 1250
    y_bal = top - 155
    pos = "left:50px" if lado == "l" else "right:50px"
    mk = ""
    if mock:
        mw = 230
        mk = f'<img class="mock" src="{b64img(Image.open(MOCK[prod]).convert("RGB").resize((mw * 2, int(mw * 2 * 1.414))))}" style="width:{mw}px;{ "left:44px" if lado == "r" else "right:44px"};top:{y_verm - 380}px;{"transform:rotate(-6deg)" if lado == "r" else ""}">'
    return f"""<html><head><style>{CSS} body{{width:{W}px;height:{H}px}}</style></head><body>
<img class="bg" src="{b64img(bg)}">
<div class="fx verde" style="top:{y_verde}px;width:{W - 90}px;font-size:{60 if len(verde) < 40 else 56}px">{verde}</div>
<div class="bal {lado}" style="{pos};top:{y_bal}px;max-width:520px">{bal}</div>
{mk}
<div class="fx verm" style="top:{y_verm}px;width:{W - 70}px;font-size:{58 if len(verm) < 42 else 54}px">{verm.replace("R$ ", "R$&nbsp;")}</div>
<div class="fx rod" style="top:{y_rod}px;font-size:{54}px;padding:10px 34px 4px">{rod}</div>
</body></html>"""


def main(prods):
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for prod in prods:
            out = ROOT / "out" / "criativos" / prod; out.mkdir(parents=True, exist_ok=True); feitos = []
            for ang in ANG[prod]:
                for v in (1, 2):
                    for sz, (W, H) in [("feed", (1080, 1350)), ("stories", (1080, 1920))]:
                        pg = b.new_page(viewport={"width": W, "height": H}); pg.set_content(html(prod, ang, v, W, H)); pg.wait_for_timeout(250)
                        bad = pg.evaluate("""() => [...document.querySelectorAll('.fx,.bal')].filter(e => { const r=e.getBoundingClientRect();
                            return r.left<0||r.right>innerWidth||r.top<(innerHeight>1400?240:0)||r.bottom>(innerHeight>1400?1680:innerHeight)||e.scrollWidth>e.clientWidth+2 }).map(e=>e.className)""")
                        p = out / f"{prod}-{ang}-{v}-{sz}.png"; pg.screenshot(path=str(p)); pg.close(); feitos.append(p)
                        print(p.name, "PROBLEMA: " + ",".join(bad) if bad else "ok")
            th = [Image.open(p) for p in feitos]
            th = [im.resize((216, int(im.height * 216 / 1080))) for im in th]
            c = Image.new("RGB", (6 * 226 + 10, 10 + 270 + 10 + 384 + 10), "white")
            for k, im in enumerate(th):
                col = (k // 2) % 6 if False else (k // 2) % 6
                row = (k // 12); isst = k % 2
                x = 10 + ((k // 2) % 6) * 226; y = 10 + row * (270 + 384 + 20) + (280 if isst else 0)
                c.paste(im, (x, y))
            c.save(out / "contato.png"); print(prod, "contato.png")
        b.close()


if __name__ == "__main__":
    main(sys.argv[1:] or list(ANG))
