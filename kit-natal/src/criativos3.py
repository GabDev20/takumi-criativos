# Criativos v3: 5 ângulos em feed 4:5 (1080x1350) e stories 9:16 (1080x1920, 250 px de respiro em cima e embaixo).
# Uso: python src/criativos3.py "19,90"   ->  out/v3/estaticos/*.png + contato.png
import pathlib, sys, base64
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent; IMG = ROOT / "out/img"
DEST = ROOT / "out/v3/estaticos"; DEST.mkdir(parents=True, exist_ok=True)
PRECO = sys.argv[1] if len(sys.argv) > 1 else "19,90"
b64 = lambda p, m="image/png": f"data:{m};base64," + base64.b64encode(pathlib.Path(p).read_bytes()).decode()
f64 = lambda n: "data:font/woff2;base64," + base64.b64encode((ROOT / "fonts" / n).read_bytes()).decode()
I = {n: b64(IMG / f"{n}.png") for n in ["mockup", "aula", "historia", "colorir", "labirinto", "cacapalavras", "teatro", "cartao", "marcadores"]}

CSS = f"""@font-face{{font-family:Baloo;font-weight:800;src:url({f64('baloo-2-latin-800-normal.woff2')})}}
@font-face{{font-family:Baloo;font-weight:700;src:url({f64('baloo-2-latin-700-normal.woff2')})}}
@font-face{{font-family:Nunito;font-weight:700;src:url({f64('nunito-latin-700-normal.woff2')})}}
@font-face{{font-family:Nunito;font-weight:800;src:url({f64('nunito-latin-800-normal.woff2')})}}
*{{box-sizing:border-box}}
body{{margin:0;background:#1F3A5F;font-family:Nunito;color:#fff;overflow:hidden;text-align:center;
 background-image:radial-gradient(circle at 50% 38%,#2b4f7f 0,#1F3A5F 62%)}}
.f{{display:flex;flex-direction:column;height:100%}}
.rib{{align-self:center;background:#C0392B;font-family:Baloo;font-weight:800;letter-spacing:.06em;text-transform:uppercase;font-size:30px;padding:10px 30px 6px;border-radius:999px}}
.h{{font-family:Baloo;font-weight:800;line-height:1.0;margin:18px 50px 0}}.g{{color:#E9B44C}}
.s{{font-weight:800;font-size:40px;margin:14px 60px 0;line-height:1.2}}
.chips{{display:flex;flex-wrap:wrap;justify-content:center;gap:12px;margin:22px 40px 0}}
.chips span{{background:#fff;color:#1F3A5F;font-weight:800;font-size:34px;padding:8px 24px;border-radius:999px}}
.stage{{flex:1;position:relative;margin-top:16px}}
.pg{{position:absolute;border:6px solid #E9B44C;box-shadow:0 24px 50px rgba(0,0,0,.45);background:#fff}}
.tag{{position:absolute;background:#C0392B;color:#fff;font-family:Baloo;font-weight:800;font-size:38px;padding:6px 20px 2px;border-radius:14px;white-space:nowrap}}
.foot{{display:flex;align-items:center;justify-content:center;gap:22px;margin-top:14px}}
.cta{{background:#1E8E5A;color:#fff;font-family:Baloo;font-weight:800;font-size:44px;border-radius:999px;padding:16px 44px 10px;box-shadow:0 8px 0 #14633e;white-space:nowrap}}
.pr{{background:#E9B44C;color:#1F3A5F;font-family:Baloo;font-weight:800;border-radius:24px;padding:8px 26px 2px;line-height:.95;border:5px solid #fff;transform:rotate(-4deg)}}
.pr small{{display:block;font-size:26px}}.pr b{{font-size:66px}}
.burst{{position:absolute;background:#E9B44C;color:#1F3A5F;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;
 font-family:Baloo;font-weight:800;line-height:.95;transform:rotate(-8deg);box-shadow:0 12px 0 rgba(0,0,0,.25);border:8px solid #fff}}
"""


def doc(W, H, inner):
    tall = H > 1400
    pad = "250px 0 250px" if tall else "36px 0 40px"
    return f"<html><head><style>{CSS} body{{width:{W}px;height:{H}px}} .f{{padding:{pad}}}</style></head><body><div class='f'>{inner(tall)}</div></body></html>"


def price_pill(top="Kit completo"):
    return f"<div class='pr'><small>{top}</small><b>R$ {PRECO}</b></div>"


def preco_a(tall):
    return f"""<div class='rib'>Kit de Natal · Ministério Infantil</div>
<div class='h' style='font-size:{78 if tall else 70}px'>Dezembro inteiro do ministério infantil por</div>
<div class='h g' style='font-size:{210 if tall else 180}px;margin-top:0;line-height:.95;text-shadow:0 8px 0 rgba(0,0,0,.25)'>R$ {PRECO}</div>
<div class='chips'><span>4 aulas</span><span>16 atividades</span><span>Teatro</span><span>Lembrancinhas</span></div>
<div class='stage'><img src='{I['mockup']}' style='position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);height:{'108%' if tall else '112%'}'></div>
<div class='foot'><div class='cta'>Baixe e imprima hoje</div></div>"""


def preco_b(tall):
    w = 400 if tall else 340
    return f"""<div class='rib'>Kit de Natal · Ministério Infantil</div>
<div class='h' style='font-size:{100 if tall else 92}px'>Menos de <span class='g'>R$ 5 por domingo</span></div>
<div class='s' style='font-size:{46 if tall else 42}px'>4 aulas de Natal prontas para imprimir</div>
<div class='stage'>
 <img class='pg' src='{I['aula']}' style='width:{w}px;left:30px;top:{'14%' if tall else '8%'};transform:rotate(-8deg)'>
 <img class='pg' src='{I['historia']}' style='width:{w}px;left:{540 - w // 2}px;top:{'8%' if tall else '2%'};transform:rotate(1deg);z-index:2'>
 <img class='pg' src='{I['colorir']}' style='width:{w}px;right:30px;top:{'14%' if tall else '8%'};transform:rotate(8deg)'>
 <div class='tag' style='left:50%;bottom:{'6%' if tall else '0'};transform:translateX(-50%);z-index:3;font-size:36px'>4 domingos · R$ {PRECO} no total</div>
</div>
<div class='foot'>{price_pill()}<div class='cta'>Baixe hoje</div></div>"""


def teatro(tall):
    return f"""<div class='rib'>Culto de Natal das crianças</div>
<div class='h' style='font-size:{90 if tall else 80}px'>Pediram um teatro de Natal?<br><span class='g'>Já está escrito.</span></div>
<div class='s' style='font-size:36px'>“O Presente Mais Esperado” · 8 a 10 min · papel para todas as crianças</div>
<div class='stage'>
 <img class='pg' src='{I['teatro']}' style='height:{'98%' if tall else '100%'};left:50%;top:0;transform:translateX(-58%) rotate(-3deg)'>
 <div class='burst' style='right:34px;bottom:{'8%' if tall else '4%'};width:280px;height:280px'><span style='font-size:30px'>+ 4 aulas</span><span style='font-size:64px'>R$ {PRECO}</span><span style='font-size:26px'>kit completo</span></div>
</div>
<div class='foot'><div class='cta'>Quero o roteiro pronto</div></div>"""


def sabado(tall):
    return f"""<div class='rib'>Ministério infantil</div>
<div class='h' style='font-size:{84 if tall else 72}px'>Sábado, 23h, e a aula de domingo <span class='g'>ainda não está pronta?</span></div>
<div class='stage'>
 <img class='pg' src='{I['aula']}' style='height:{'94%' if tall else '96%'};left:70px;top:2%;transform:rotate(-4deg)'>
 <img class='pg' src='{I['colorir']}' style='height:{'62%' if tall else '64%'};right:60px;top:{'26%' if tall else '20%'};transform:rotate(6deg)'>
 <div class='burst' style='right:40px;top:0;width:250px;height:250px'><span style='font-size:28px'>4 aulas por</span><span style='font-size:58px'>R$ {PRECO}</span></div>
</div>
<div class='h' style='font-size:{78 if tall else 68}px;margin-top:12px'>Imprima e dê aula.</div>
<div class='foot'><div class='cta' style='font-size:40px'>Kit de Natal pronto · R$ {PRECO}</div></div>"""


def idades(tall):
    w = 316
    cols = [("colorir", "3 a 5 anos", -5), ("labirinto", "3 a 8 anos", 0), ("cacapalavras", "6 a 11 anos", 5)]
    imgs = "".join(
        f"<img class='pg' src='{I[n]}' style='width:{w}px;left:{30 + i * (w + 26)}px;top:{'24%' if tall else '12%'};transform:rotate({r}deg)'>"
        f"<div class='tag' style='left:{30 + i * (w + 26) + w // 2}px;top:{'16%' if tall else '3%'};transform:translateX(-50%);z-index:3'>{t}</div>"
        for i, (n, t, r) in enumerate(cols))
    return f"""<div class='rib'>Uma sala, várias idades</div>
<div class='h' style='font-size:{86 if tall else 76}px'>Uma folha para <span class='g'>cada idade</span></div>
<div class='s'>De 3 a 11 anos, com gabarito · 16 atividades</div>
<div class='stage'>{imgs}</div>
<div class='foot'>{price_pill('4 aulas + teatro')}<div class='cta'>Baixe e imprima</div></div>"""


PECAS = [("preco-a", preco_a), ("preco-b", preco_b), ("teatro", teatro), ("sabado", sabado), ("idades", idades)]

if __name__ == "__main__":
    feitos = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for nome, fn in PECAS:
            for sz, (W, H) in [("feed", (1080, 1350)), ("stories", (1080, 1920))]:
                pg = b.new_page(viewport={"width": W, "height": H}); pg.set_content(doc(W, H, fn)); pg.wait_for_timeout(300)
                p = DEST / f"{nome}-{sz}.png"; pg.screenshot(path=str(p)); pg.close(); feitos.append(p); print(p.name)
        b.close()
    # folha de contato: feed em cima, stories embaixo, uma coluna por ângulo
    tw = 340; fnt = ImageFont.truetype(str(ROOT / "fonts/nunito-latin-700-normal.ttf"), 24)
    th_f, th_s = int(1350 * tw / 1080), int(1920 * tw / 1080)
    sheet = Image.new("RGB", (len(PECAS) * (tw + 20) + 20, th_f + th_s + 120), "white"); d = ImageDraw.Draw(sheet)
    for i, (nome, _) in enumerate(PECAS):
        x = 20 + i * (tw + 20)
        d.text((x, 12), nome, font=fnt, fill="black")
        sheet.paste(Image.open(DEST / f"{nome}-feed.png").convert("RGB").resize((tw, th_f)), (x, 50))
        sheet.paste(Image.open(DEST / f"{nome}-stories.png").convert("RGB").resize((tw, th_s)), (x, 70 + th_f))
    sheet.save(DEST / "contato.png"); print("contato.png")
