# Página v3 (teste A/B). Copia SEM ALTERAR da v2 (out/lovable/index.html): Meta Pixel, script de UTMs/contagem e tracker da Cakto,
# além das dores e do FAQ. Uso: python src/pagina3.py  ->  out/v3/pagina/index.html
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
v2 = (ROOT / "out/lovable/index.html").read_text(encoding="utf-8")
cut = lambda a, b, inc_b=False: v2[v2.index(a): v2.index(b) + (len(b) if inc_b else 0)]
pixel = cut("<!-- Meta Pixel -->", "<!-- End Meta Pixel -->", True)
utm = cut("<script>\n(function(){", '</script>\n<script src="https://api.cakto') + "</script>"
tracker = '<script src="https://api.cakto.com.br/api/product/checkout/tracker.js" async></script>'
faq = cut("<details><summary>É um material", '<div class="ctr" style="margin-top:24px">')
dores = cut("<li><b>Sábado, 23h.</b>", '</ul><p class="vira">')
vira = re.search(r'<p class="vira">(.*?)</p>', v2).group(1)
C = "https://pay.cakto.com.br/9r765aw_1299013"
caps = ["Plano de aula completo", "História pronta para contar", "Colorir (3 a 5 anos)", "Labirinto (3 a 8 anos)",
        "Caça-palavras (6 a 11 anos)", "Teatro do culto de Natal", "Cartão lembrancinha", "Marcadores com versículos"]
car = "".join(f'<figure><img loading="lazy" width="520" height="735" src="/k6a7d2294/p{i + 1}.jpg" alt="{c}"><figcaption>{c}</figcaption></figure>'
              for i, c in enumerate(caps))

CSS = """:root{--azul:#1F3A5F;--ouro:#E9B44C;--verm:#C0392B;--verde:#1E8E5A;--creme:#FFF8EA;--txt:#22303f}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:Nunito,system-ui,sans-serif;color:var(--txt);background:#fff;line-height:1.5;font-size:17px;padding-bottom:76px;overflow-x:hidden}
h1,h2,h3{font-family:'Baloo 2',system-ui,sans-serif;line-height:1.08;color:var(--azul);margin:0 0 10px}
h1{font-size:clamp(29px,7.4vw,50px)}h2{font-size:clamp(25px,6vw,38px);text-align:center}
.wrap{max-width:860px;margin:0 auto;padding:0 18px}section{padding:40px 0}
.top{background:var(--verm);color:#fff;text-align:center;font-weight:800;font-size:14px;padding:8px 12px;line-height:1.3}
.hero{background:var(--azul);color:#fff;text-align:center;padding:16px 0 30px}.hero h1{color:#fff;margin-bottom:4px}.hero h1 em{color:var(--ouro);font-style:normal;white-space:nowrap}
.k{color:var(--ouro);font-family:'Baloo 2';font-weight:800;letter-spacing:.06em;text-transform:uppercase;font-size:13px}
.hero img{display:block;width:100%;max-width:520px;height:auto;margin:0 auto;aspect-ratio:1100/786;max-height:30vh;object-fit:contain}
.btn{display:block;max-width:460px;margin:14px auto 0;background:var(--verde);color:#fff;font-family:'Baloo 2';font-weight:800;font-size:22px;line-height:1.15;padding:16px 20px;border-radius:999px;text-decoration:none;box-shadow:0 6px 0 #14633e;text-align:center}
.btn:active{transform:translateY(3px);box-shadow:0 3px 0 #14633e}
.mini{font-size:14px;opacity:.92;margin-top:12px}
.car{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;padding:6px 18px 14px;margin:18px -18px 0;scrollbar-width:none}.car::-webkit-scrollbar{display:none}
.car figure{flex:0 0 72%;max-width:300px;scroll-snap-align:center;margin:0;background:#f4f6f9;border-radius:14px;padding:10px;text-align:center}
.car img{width:100%;height:auto;border-radius:6px;box-shadow:0 4px 14px rgba(0,0,0,.12)}figcaption{font-weight:700;font-size:14px;margin-top:8px}
.dica{text-align:center;font-size:14px;color:#6b7a89;margin:4px 0 0}
.dor{background:var(--creme)}.dor ul{max-width:720px;margin:18px auto 0;padding:0;list-style:none}.dor li{background:#fff;border-radius:14px;padding:13px 16px;margin-bottom:10px;border-left:5px solid var(--verm)}
.vira{max-width:720px;margin:20px auto 0;text-align:center;font-size:20px;font-weight:800;color:var(--azul)}
.ok{list-style:none;padding:0;margin:18px auto 0;max-width:620px}.ok li{padding:9px 0 9px 32px;border-bottom:1px dashed #d9e0e8;position:relative}
.ok li:before{content:"✓";position:absolute;left:0;top:9px;width:22px;height:22px;border-radius:50%;background:var(--ouro);color:var(--azul);display:grid;place-items:center;font-size:14px;font-weight:800}
.teatro{background:var(--azul);color:#fff}.teatro h2{color:#fff}.teatro .ok li{border-color:rgba(255,255,255,.2)}
.teatro .g{display:grid;grid-template-columns:1fr 1.2fr;gap:24px;align-items:center;max-width:820px;margin:20px auto 0}.teatro img{width:100%;height:auto;border-radius:10px;box-shadow:0 10px 30px rgba(0,0,0,.35)}
.offer{background:var(--creme);text-align:center}.price{font-family:'Baloo 2';color:var(--azul);font-size:64px;font-weight:800;line-height:1;margin-top:10px}.price small{font-size:22px}
.sub{margin:6px 0 0;font-weight:800;color:var(--azul)}
.gar{display:flex;gap:18px;align-items:center;max-width:760px;margin:0 auto;background:var(--creme);border-radius:20px;padding:22px}.seal{flex:none;width:92px;height:92px;border-radius:50%;background:var(--ouro);display:grid;place-items:center;font-family:'Baloo 2';font-weight:800;color:var(--azul);text-align:center;line-height:1}
details{max-width:760px;margin:0 auto 10px;border:2px solid #e3e8ee;border-radius:14px;padding:13px 16px}summary{font-weight:800;cursor:pointer}
footer{text-align:center;font-size:13px;color:#7a8794;padding:28px 18px}
.bar{position:fixed;left:0;right:0;bottom:0;background:#fff;box-shadow:0 -4px 18px rgba(0,0,0,.18);padding:10px 14px;display:flex;gap:12px;align-items:center;justify-content:center;z-index:9}
.bar div{font-weight:800;color:var(--azul);line-height:1.15;font-size:15px}.bar div b{font-family:'Baloo 2';font-size:22px;display:block}
.bar a{background:var(--verde);color:#fff;font-family:'Baloo 2';font-weight:800;font-size:18px;padding:12px 22px;border-radius:999px;text-decoration:none;white-space:nowrap}
@media(max-width:700px){.teatro .g{grid-template-columns:1fr}.gar{flex-direction:column;text-align:center}}
@media(min-width:701px){.car figure{flex-basis:30%}}"""

HTML = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kit de Natal para o Ministério Infantil · Seu dezembro pronto por R$ 19,90</title>
<meta name="description" content="4 aulas de Natal prontas, 16 atividades por idade, teatro para o culto e lembrancinhas. PDF para imprimir por R$ 19,90.">
<meta name="robots" content="noindex,nofollow">
<link rel="preload" as="image" href="/k6a7d2294/mockup.webp">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@700;800&family=Nunito:wght@400;700;800&display=swap" rel="stylesheet">
{pixel}
<style>
{CSS}
</style></head><body>
<div class="top" id="faixa">Dezembro está chegando. Deixe as 4 aulas de Natal prontas ainda hoje.</div>

<header class="hero"><div class="wrap">
<div class="k">Para o ministério infantil · 3 a 11 anos</div>
<h1>Seu dezembro no ministério infantil pronto por <em>R$ 19,90</em></h1>
<img src="/k6a7d2294/mockup.webp" width="1100" height="786" alt="Páginas do kit de Natal para o ministério infantil">
<a class="btn" href="{C}">Quero meu kit por R$ 19,90</a>
<div class="mini">Pix ou cartão · PDF no e-mail na hora · 7 dias de garantia</div>
</div></header>

<section style="padding-bottom:28px"><div class="wrap"><h2>Veja por dentro</h2>
<div class="car">{car}</div><p class="dica">Arraste para o lado para ver mais páginas →</p></div></section>

<section class="dor"><div class="wrap"><h2>Todo dezembro é a mesma correria?</h2><ul>
{dores}</ul><p class="vira">{vira}</p></div></section>

<section><div class="wrap"><h2>O que vem no kit</h2><ul class="ok">
<li><b>4 aulas de Natal:</b> o anjo visita Maria, José confia em Deus, Jesus nasce em Belém, os magos adoram Jesus</li>
<li><b>4 histórias prontas</b> para ler e contar, com perguntas por idade</li>
<li><b>16 atividades</b> para 3 a 11 anos, com gabarito</li>
<li><b>Teatro</b> “O Presente Mais Esperado” para o culto de Natal</li>
<li><b>Lembrancinhas:</b> cartão, marcadores de página e estrela de porta</li>
<li><b>Cronograma de dezembro</b> e lista de compras</li>
</ul><a class="btn" href="{C}">Quero receber tudo agora</a></div></section>

<section class="teatro"><div class="wrap"><div class="k" style="text-align:center">Incluso no kit</div><h2>A apresentação de Natal das crianças já está escrita</h2>
<div class="g"><img loading="lazy" width="520" height="735" src="/k6a7d2294/p6.jpg" alt="Roteiro do teatro O Presente Mais Esperado"><div>
<ul class="ok" style="margin-top:0"><li>“O Presente Mais Esperado”: 8 a 10 minutos de apresentação</li><li>Falas curtas, fáceis de decorar</li><li>Papel para todas as crianças, até as de 3 anos (ovelhas e coro de anjos)</li><li>Figurino com lençol, toalha e papel dourado</li><li>Dá para ensaiar em dois domingos</li></ul>
</div></div></div></section>

<section class="offer" id="oferta"><div class="wrap"><h2>O mês inteiro por menos de R$ 5 por domingo</h2>
<div class="price"><small>R$</small> 19,90</div><p class="sub">Pagamento único · sem mensalidade</p>
<a class="btn" href="{C}">Quero meu kit de Natal agora</a>
<p class="mini">Acesso imediato por e-mail · Pix ou cartão</p></div></section>

<section><div class="wrap"><div class="gar"><div class="seal">7 dias<br>de garantia</div><div><h3>Você não arrisca nada</h3>Baixe, olhe página por página. Se o material não servir para a sua turma, peça o reembolso em até 7 dias pela própria plataforma de pagamento e receba 100% do valor de volta, sem perguntas.</div></div></div></section>

<section style="padding-top:0"><div class="wrap"><h2>Perguntas frequentes</h2>
{faq}<a class="btn" href="{C}">Garantir meu dezembro por R$ 19,90</a></div></section>
<footer>Estrela Guia Kids · Material digital para ministério infantil.<br>Este site não faz parte do Facebook nem da Meta e não é endossado por eles.</footer>

<div class="bar"><div>Kit de Natal completo<b>R$ 19,90</b></div><a href="{C}">Quero o meu</a></div>
{utm}
{tracker}
</body></html>
"""

if __name__ == "__main__":
    out = ROOT / "out/v3/pagina/index.html"; out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(HTML, encoding="utf-8")
    for blk in (pixel, utm, tracker): assert blk in HTML and blk in v2
    print(out, len(HTML.encode()), "bytes")
