# Gera prévias do kit, mockup, página de vendas e criativos estáticos.
import base64, pathlib, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build import fontcss, CSS as KCSS

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "out"; IMG = OUT / "img"; IMG.mkdir(exist_ok=True)
PDF = OUT / "kit-natal-ministerio-infantil.pdf"
PREV = {"capa": 1, "aula": 4, "historia": 5, "colorir": 7, "labirinto": 8, "cacapalavras": 9, "teatro": 32, "cartao": 34, "marcadores": 35}

for nome, p in PREV.items():
    subprocess.run(["pdftoppm", "-r", "80", "-png", "-singlefile", "-f", str(p), "-l", str(p), str(PDF), str(IMG / nome)], check=True)


def card(im, w):
    im = im.convert("RGB"); h = int(im.height * w / im.width); im = im.resize((w, h), Image.LANCZOS)
    ImageDraw.Draw(im).rectangle([0, 0, w - 1, h - 1], outline=(233, 180, 76), width=5)
    pad = 30; c = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", c.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([pad, pad + 10, pad + w, pad + h + 10], 12, fill=(0, 0, 0, 90))
    c = Image.alpha_composite(c, sh.filter(ImageFilter.GaussianBlur(14)))
    c.paste(im, (pad, pad)); return c


def mockup(names, size=(1400, 1000), out="mockup.png", bg=(0, 0, 0, 0)):
    M = Image.new("RGBA", size, bg)
    pos = [(-0.06, 0.18, -8), (0.62, 0.14, 7), (0.30, 0.04, 0)]
    for (x, y, rot), n in zip(pos, names):
        c = card(Image.open(IMG / f"{n}.png"), int(size[0] * 0.40)).rotate(rot, expand=True, resample=Image.BICUBIC)
        M.alpha_composite(c, (int(size[0] * x + size[0] * 0.04), int(size[1] * y)))
    M.save(IMG / out); return IMG / out


mockup(["colorir", "teatro", "capa"])
b64 = lambda p: "data:image/png;base64," + base64.b64encode(pathlib.Path(p).read_bytes()).decode()
def jpg64(n, w=520):
    im = Image.open(IMG / f"{n}.png").convert("RGB"); im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    p = IMG / f"{n}.jpg"; im.save(p, quality=82); return "data:image/jpeg;base64," + base64.b64encode(p.read_bytes()).decode()

MOCK = b64(IMG / "mockup.png")
FONT = fontcss(KCSS.split("@page")[0])
CHECKOUT = "#CHECKOUT"  # trocar pelo link do checkout (Cakto/Kiwify)

prev = "".join(f'<figure><img src="{jpg64(n)}" alt=""><figcaption>{t}</figcaption></figure>' for n, t in [
    ("aula", "Plano de aula completo"), ("historia", "História pronta para contar"), ("colorir", "Colorir (3 a 5 anos)"),
    ("labirinto", "Labirinto (3 a 8 anos)"), ("cacapalavras", "Caça-palavras (6 a 11 anos)"), ("teatro", "Teatro do culto de Natal"),
    ("cartao", "Cartão lembrancinha"), ("marcadores", "Marcadores com versículos")])

PAGE = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Natal no Ministério Infantil · Dezembro pronto</title>
<meta name="description" content="4 aulas de Natal prontas, atividades por idade, teatro e lembrancinhas para o ministério infantil. PDF para imprimir.">
<style>{FONT}
:root{{--azul:#1F3A5F;--ouro:#E9B44C;--verm:#C0392B;--creme:#FFF8EA;--txt:#22303f}}
*{{box-sizing:border-box}}body{{margin:0;font-family:Nunito,system-ui,sans-serif;color:var(--txt);background:#fff;line-height:1.55;font-size:17px}}
h1,h2,h3{{font-family:Baloo,system-ui,sans-serif;line-height:1.1;color:var(--azul);margin:0 0 12px}}
h1{{font-size:clamp(32px,6vw,54px)}}h2{{font-size:clamp(26px,4.5vw,38px);text-align:center}}h3{{font-size:21px}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 18px}}section{{padding:56px 0}}
.hero{{background:var(--azul);color:#fff;padding:40px 0 56px}}.hero h1{{color:#fff}}.hero .k{{color:var(--ouro);font-family:Baloo;font-weight:800;letter-spacing:.08em;text-transform:uppercase;font-size:14px}}
.hero .g{{display:grid;grid-template-columns:1.05fr 1fr;gap:28px;align-items:center}}.hero img{{width:100%}}
.lead{{font-size:19px;opacity:.95;max-width:560px}}
.btn{{display:inline-block;background:var(--ouro);color:var(--azul);font-family:Baloo;font-weight:800;font-size:21px;padding:16px 30px;border-radius:999px;text-decoration:none;box-shadow:0 6px 0 #b98a2c;margin-top:10px}}
.btn:active{{transform:translateY(3px);box-shadow:0 3px 0 #b98a2c}}.mini{{font-size:14px;opacity:.85;margin-top:10px}}
.dor{{background:var(--creme)}}.dor ul{{max-width:720px;margin:20px auto 0;padding:0;list-style:none}}.dor li{{background:#fff;border-radius:14px;padding:14px 18px;margin-bottom:10px;border-left:5px solid var(--verm)}}
.cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:26px}}.c{{border:2px solid #e3e8ee;border-radius:18px;padding:20px}}.c b{{color:var(--verm);font-family:Baloo;font-size:15px;text-transform:uppercase;letter-spacing:.05em}}
.prev{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:26px}}figure{{margin:0;background:#f4f6f9;border-radius:14px;padding:10px;text-align:center}}figure img{{width:100%;border-radius:6px;box-shadow:0 4px 14px rgba(0,0,0,.12)}}figcaption{{font-weight:700;font-size:14px;margin-top:8px}}
.steps{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:26px;counter-reset:s}}.steps div{{background:#eef4fb;border-radius:18px;padding:20px}}.steps div:before{{counter-increment:s;content:counter(s);display:inline-grid;place-items:center;width:38px;height:38px;border-radius:50%;background:var(--azul);color:#fff;font-family:Baloo;font-weight:800;margin-bottom:8px}}
.offer{{background:var(--azul);color:#fff;text-align:center}}.offer h2{{color:#fff}}.box{{background:#fff;color:var(--txt);max-width:560px;margin:24px auto 0;border-radius:22px;padding:28px;text-align:left}}
.box li{{margin-bottom:8px}}.price{{text-align:center;font-family:Baloo;color:var(--azul);font-size:56px;font-weight:800;line-height:1}}.price small{{font-size:20px}}
.gar{{display:flex;gap:18px;align-items:center;max-width:760px;margin:0 auto;background:var(--creme);border-radius:20px;padding:22px}}.seal{{flex:none;width:96px;height:96px;border-radius:50%;background:var(--ouro);display:grid;place-items:center;font-family:Baloo;font-weight:800;color:var(--azul);text-align:center;line-height:1}}
details{{max-width:760px;margin:0 auto 10px;border:2px solid #e3e8ee;border-radius:14px;padding:14px 18px}}summary{{font-weight:800;cursor:pointer}}
footer{{text-align:center;font-size:13px;color:#7a8794;padding:30px 18px}}
@media(max-width:820px){{.hero .g,.cards,.steps{{grid-template-columns:1fr}}.prev{{grid-template-columns:repeat(2,1fr)}}.hero{{text-align:center}}.lead{{margin:0 auto}}.gar{{flex-direction:column;text-align:center}}}}
</style></head><body>
<header class="hero"><div class="wrap g"><div>
<div class="k">Para líderes e professores do ministério infantil</div>
<h1>Seu dezembro no ministério infantil, pronto em um único PDF</h1>
<p class="lead">4 aulas de Natal completas, atividades para 3 a 11 anos, teatro para o culto de Natal e lembrancinhas para recortar. É só imprimir e dar aula.</p>
<a class="btn" href="{CHECKOUT}">Quero o kit de Natal</a><div class="mini">PDF enviado no seu e-mail logo após a compra · Garantia de 7 dias</div>
</div><img src="{MOCK}" alt="Páginas do kit de Natal"></div></header>

<section class="dor"><div class="wrap"><h2>Dezembro chega e a aula ainda não está pronta?</h2><ul>
<li>Você passa o sábado à noite procurando atividade de Natal na internet.</li>
<li>As crianças de 3 anos e as de 10 estão na mesma sala e nada serve para todas.</li>
<li>Pediram um teatro para o culto de Natal e ninguém sabe por onde começar.</li>
<li>Você quer que elas entendam o verdadeiro sentido do Natal, não só o Papai Noel.</li>
</ul></div></section>

<section><div class="wrap"><h2>O que vem no kit</h2><div class="cards">
<div class="c"><b>4 aulas completas</b><h3>Um domingo de cada vez</h3>O anjo visita Maria, José confia em Deus, Jesus nasce em Belém e os magos adoram Jesus. Cada aula tem verdade central, versículo, materiais, acolhida, roteiro de 40 minutos e oração.</div>
<div class="c"><b>História pronta</b><h3>É só ler e contar</h3>Texto narrado em linguagem de criança, com dicas de como contar e perguntas separadas por idade: 3 a 5, 6 a 8 e 9 a 11 anos.</div>
<div class="c"><b>16 atividades</b><h3>Para cada idade</h3>Colorir, labirinto, caça-palavras e desafio do versículo em todas as aulas, com gabarito para o professor.</div>
<div class="c"><b>Teatro de Natal</b><h3>“O Presente Mais Esperado”</h3>Roteiro de 8 a 10 minutos, com papel para todo mundo (até o coro de anjos) e figurino feito com o que você tem em casa.</div>
<div class="c"><b>Lembrancinhas</b><h3>Para recortar</h3>Cartão “Jesus é o melhor presente”, marcadores de página com os versículos do mês e estrela de porta para pintar.</div>
<div class="c"><b>Planejamento</b><h3>Dezembro organizado</h3>Cronograma dos 4 domingos e do culto de Natal, mais a lista de compras do mês.</div>
</div></div></section>

<section style="background:#f9fafb"><div class="wrap"><h2>Veja por dentro</h2><div class="prev">{prev}</div></div></section>

<section><div class="wrap"><h2>Como funciona</h2><div class="steps">
<div><h3>Compre</h3>O pagamento é por Pix ou cartão, e o acesso chega no seu e-mail na hora.</div>
<div><h3>Imprima</h3>Papel A4 comum. As páginas de atividade são em preto e branco para economizar tinta.</div>
<div><h3>Dê a aula</h3>Abra o plano do domingo, conte a história e entregue a atividade de cada idade.</div>
</div></div></section>

<section class="offer" id="oferta"><div class="wrap"><h2>Tudo isso por menos de R$ 5 por domingo</h2><div class="box"><ul>
<li>4 planos de aula de Natal completos</li><li>4 histórias prontas para contar</li><li>16 atividades por idade + gabarito</li>
<li>Teatro “O Presente Mais Esperado”</li><li>Cartões, marcadores e estrela de porta</li><li>Cronograma de dezembro e lista de compras</li></ul>
<div class="price"><small>R$</small> 19,90</div><p style="text-align:center;margin:6px 0 0">ou parcelado no cartão</p>
<div style="text-align:center"><a class="btn" href="{CHECKOUT}">Quero o kit de Natal</a></div></div></div></section>

<section><div class="wrap"><div class="gar"><div class="seal">7 dias<br>de garantia</div><div><h3>Risco zero</h3>Se o material não servir para a sua turma, peça o reembolso em até 7 dias pela própria plataforma de pagamento. Você recebe 100% do valor de volta, sem perguntas.</div></div></div></section>

<section style="padding-top:0"><div class="wrap"><h2>Perguntas frequentes</h2>
<details><summary>É um material físico?</summary>Não. É um PDF digital que você recebe por e-mail e imprime quantas vezes precisar para a sua turma.</details>
<details><summary>Serve para qual idade?</summary>De 3 a 11 anos. As atividades e as perguntas vêm separadas por faixa etária.</details>
<details><summary>Serve para qualquer igreja?</summary>Sim. O conteúdo segue as histórias do Natal nos Evangelhos, sem temas de doutrina denominacional. Os versículos estão em paráfrase para crianças, com a referência, e você pode ler na versão da Bíblia que a sua igreja usa.</details>
<details><summary>Posso usar em casa com meus filhos?</summary>Pode. Muitas famílias usam como devocional de Natal.</details>
<details><summary>Posso imprimir para toda a turma?</summary>Sim, para uso no seu ministério e na sua casa. Só não é permitido revender ou distribuir o arquivo.</details>
<details><summary>Como recebo?</summary>Logo após a confirmação do pagamento, o acesso chega no e-mail cadastrado. No Pix, a confirmação leva poucos minutos.</details>
<div style="text-align:center;margin-top:24px"><a class="btn" href="{CHECKOUT}">Garantir meu dezembro pronto</a></div></div></section>
<footer>Estrela Guia Kids · Material digital para ministério infantil.<br>Este site não faz parte do Facebook nem da Meta e não é endossado por eles.</footer>
</body></html>"""
(OUT / "pagina-de-vendas.html").write_text(PAGE, encoding="utf-8")

# criativos estáticos 1080x1350 (4:5)
ADS = [
    ("anuncio-1-dezembro-pronto", "Seu dezembro no ministério infantil", "PRONTO.", "4 aulas de Natal + teatro + lembrancinhas · PDF para imprimir"),
    ("anuncio-2-chega-de-improvisar", "Chega de improvisar", "a aula de Natal.", "Plano de aula, história, atividades de 3 a 11 anos e teatro do culto"),
    ("anuncio-3-preco", "Kit de Natal para o ministério infantil", "R$ 19,90", "Menos de R$ 5 por domingo · acesso imediato"),
]
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for fn, l1, l2, l3 in ADS:
        h = f"""<html><head><style>{FONT} body{{margin:0;width:1080px;height:1350px;background:#1F3A5F;font-family:Nunito;color:#fff;display:flex;flex-direction:column;align-items:center;text-align:center;overflow:hidden}}
.t{{font-family:Baloo;font-weight:800;font-size:66px;line-height:1.05;margin:80px 70px 0}}.t2{{font-family:Baloo;font-weight:800;font-size:110px;color:#E9B44C;line-height:1}}
.s{{font-size:36px;margin:20px 90px 0;opacity:.95}} img{{width:1000px;margin-top:10px}} .f{{position:absolute;bottom:40px;font-family:Baloo;font-weight:800;font-size:30px;background:#E9B44C;color:#1F3A5F;padding:16px 40px;border-radius:999px}}</style></head>
<body><div class="t">{l1}</div><div class="t2">{l2}</div><div class="s">{l3}</div><img src="{MOCK}"><div class="f">Saiba mais</div></body></html>"""
        pg.set_content(h); pg.wait_for_timeout(300); pg.screenshot(path=str(OUT / f"{fn}.png"))
    b.close()
print("ok")
