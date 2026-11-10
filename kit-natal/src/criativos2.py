# Criativos v2: (A) volume + preço, (B) teatro de Natal. Feed 4:5 e Stories 9:16. Uso: python3 criativos2.py "19,90"
import pathlib, sys, base64
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent; OUT = ROOT / "out"; IMG = OUT / "img"
PRECO = sys.argv[1] if len(sys.argv) > 1 else "19,90"
TAG = PRECO.replace(",", "")
b64 = lambda p, m="image/png": f"data:{m};base64," + base64.b64encode(pathlib.Path(p).read_bytes()).decode()
f64 = lambda n: "data:font/woff2;base64," + base64.b64encode((ROOT / "fonts" / n).read_bytes()).decode()
FONT = f"""@font-face{{font-family:Baloo;font-weight:800;src:url({f64('baloo-2-latin-800-normal.woff2')})}}
@font-face{{font-family:Baloo;font-weight:700;src:url({f64('baloo-2-latin-700-normal.woff2')})}}
@font-face{{font-family:Nunito;font-weight:700;src:url({f64('nunito-latin-700-normal.woff2')})}}
@font-face{{font-family:Nunito;font-weight:800;src:url({f64('nunito-latin-800-normal.woff2')})}}"""
MOCK = b64(IMG / "mockup.png"); TEATRO = b64(IMG / "teatro.png"); COLORIR = b64(IMG / "colorir.png"); AULA = b64(IMG / "aula.png")
BASE = FONT + """*{box-sizing:border-box}body{margin:0;background:#1F3A5F;font-family:Nunito;color:#fff;overflow:hidden;position:relative;text-align:center}
.rib{background:#C0392B;font-family:Baloo;font-weight:800;letter-spacing:.06em;text-transform:uppercase;padding:18px 0 14px;font-size:34px}
.h{font-family:Baloo;font-weight:800;line-height:1.02;margin:0 60px}.g{color:#E9B44C}
.chips{display:flex;flex-wrap:wrap;justify-content:center;gap:14px;margin:26px 50px 0}.chips span{background:#fff;color:#1F3A5F;font-weight:800;font-size:33px;padding:10px 24px;border-radius:999px}
.burst span{white-space:nowrap}.burst{position:absolute;background:#E9B44C;color:#1F3A5F;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:Baloo;font-weight:800;line-height:.95;transform:rotate(-8deg);box-shadow:0 12px 0 rgba(0,0,0,.25);border:8px solid #fff}
.cta{position:absolute;left:50%;transform:translateX(-50%);white-space:nowrap;background:#1E8E5A;color:#fff;font-family:Baloo;font-weight:800;border-radius:999px;box-shadow:0 8px 0 #14633e}
.pg{position:absolute;border:7px solid #E9B44C;box-shadow:0 24px 50px rgba(0,0,0,.45);background:#fff}"""

def A(W, H):
    tall = H > 1400
    return f"""<html><head><style>{BASE} body{{width:{W}px;height:{H}px}}</style></head><body>
<div class="rib" style="{'margin-top:150px' if tall else ''}">Kit de Natal · Ministério Infantil</div>
<div class="h" style="font-size:{92 if tall else 84}px;margin-top:{50 if tall else 34}px">Dezembro inteiro <span class="g">pronto para imprimir</span></div>
<div class="chips"><span>4 aulas completas</span><span>16 atividades</span><span>Teatro do culto</span><span>Lembrancinhas</span><span>3 a 11 anos</span></div>
<img src="{MOCK}" style="position:absolute;left:{-10}px;top:{760 if tall else 560}px;width:{1100}px">
<div class="burst" style="right:40px;top:{1200 if tall else 860}px;width:330px;height:330px"><span style="font-size:40px">tudo por</span><span style="font-size:76px">R$ {PRECO}</span><span style="font-size:30px">pagamento único</span></div>
<div class="cta" style="bottom:{250 if tall else 44}px;font-size:46px;padding:20px 56px">Baixe e imprima hoje</div>
</body></html>"""

def B(W, H):
    tall = H > 1400
    return f"""<html><head><style>{BASE} body{{width:{W}px;height:{H}px}}</style></head><body>
<div class="rib" style="{'margin-top:150px' if tall else ''}">Culto de Natal das crianças</div>
<div class="h" style="font-size:{88 if tall else 80}px;margin-top:{50 if tall else 32}px">Pediram um teatro de Natal?<br><span class="g">Já está escrito.</span></div>
<div style="font-size:38px;font-weight:800;margin:22px 70px 0">“O Presente Mais Esperado” · 8 a 10 minutos<br>Papel para todas as crianças, de 3 a 11 anos</div>
<img class="pg" src="{TEATRO}" style="left:{250}px;top:{760 if tall else 590}px;width:{580 if tall else 520}px;transform:rotate(-4deg)">
<img class="pg" src="{COLORIR}" style="left:{40}px;top:{980 if tall else 760}px;width:300px;transform:rotate(-13deg)">
<img class="pg" src="{AULA}" style="left:{745}px;top:{960 if tall else 740}px;width:300px;transform:rotate(11deg)">
<div class="burst" style="right:36px;top:{1260 if tall else 900}px;width:300px;height:300px"><span style="font-size:32px">+ 4 aulas prontas</span><span style="font-size:70px">R$ {PRECO}</span><span style="font-size:28px">kit completo</span></div>
<div class="cta" style="bottom:{250 if tall else 44}px;font-size:46px;padding:20px 56px">Quero o roteiro pronto</div>
</body></html>"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    for nome, fn in [("v2-A-dezembro-pronto", A), ("v2-B-teatro", B)]:
        for sz, (W, H) in [("feed", (1080, 1350)), ("stories", (1080, 1920))]:
            pg = b.new_page(viewport={"width": W, "height": H}); pg.set_content(fn(W, H)); pg.wait_for_timeout(400)
            p = OUT / f"anuncio-{nome}-{sz}-{TAG}.png"; pg.screenshot(path=str(p)); pg.close(); print(p.name)
    b.close()
