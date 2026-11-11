# Confere a página v3 em 390x844 (iPhone 13) e salva o print da página inteira.
# Serve a página em http://teste.local/ e responde /k6a7d2294/* com os arquivos de out/lovable/; bloqueia rede externa (pixel, Cakto).
import pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent; PAG = ROOT / "out/v3/pagina"; ASSETS = ROOT / "out/lovable"
html = (PAG / "index.html").read_text(encoding="utf-8")


def route(r):
    u = r.request.url
    if u.startswith("http://teste.local/k6a7d2294/"):
        f = ASSETS / u.rsplit("/", 1)[1]; return r.fulfill(path=str(f))
    if u.startswith("http://teste.local/"): return r.fulfill(body=html, content_type="text/html; charset=utf-8")
    if "fonts.g" in u: return r.continue_()
    return r.abort()


with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    pg.route("**/*", route); pg.goto("http://teste.local/?utm_source=FB&utm_content=teste"); pg.wait_for_timeout(1500)
    r = pg.evaluate("""() => { const b = document.querySelector('.hero .btn').getBoundingClientRect();
      return {scrollW: document.documentElement.scrollWidth, clientW: document.documentElement.clientWidth,
              btnBottom: b.bottom, faixa: document.getElementById('faixa').textContent,
              links: [...document.querySelectorAll('a[href*="pay.cakto"]')].map(a => a.href)} }""")
    print("rolagem horizontal:", r["scrollW"] > r["clientW"], r["scrollW"], r["clientW"])
    print("botão do hero visível sem rolar:", r["btnBottom"] <= 844 - 76, f"(base do botão em {r['btnBottom']:.0f}px; barra fixa ocupa os últimos 76px)")
    print("faixa:", r["faixa"]); print("links:", len(r["links"]), r["links"][0])
    pg.screenshot(path=str(PAG / "print-hero-390x844.png"))
    for _ in range(30): pg.mouse.wheel(0, 800); pg.wait_for_timeout(60)  # força o carregamento das imagens lazy
    pg.evaluate("window.scrollTo(0,0)"); pg.add_style_tag(content=".bar{position:static}body{padding-bottom:0}"); pg.wait_for_timeout(800)  # barra fixa no fim do print
    pg.screenshot(path=str(PAG / "print-mobile.png"), full_page=True)
    b.close()
