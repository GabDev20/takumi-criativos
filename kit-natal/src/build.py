import sys, pathlib, html
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from content import NATAL, JANEIRO, TEATRO, MARCA
from art import ART, small_star, maze, wordsearch, star_points

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "fonts"
OUT = ROOT / "out"; OUT.mkdir(exist_ok=True)
e = html.escape

CSS = """
@font-face{font-family:Baloo;src:url(FONTS/baloo-2-latin-700-normal.woff2);font-weight:700}
@font-face{font-family:Baloo;src:url(FONTS/baloo-2-latin-800-normal.woff2);font-weight:800}
@font-face{font-family:Baloo;src:url(FONTS/baloo-2-latin-400-normal.woff2);font-weight:400}
@font-face{font-family:Nunito;src:url(FONTS/nunito-latin-400-normal.woff2);font-weight:400}
@font-face{font-family:Nunito;src:url(FONTS/nunito-latin-700-normal.woff2);font-weight:700}
@font-face{font-family:Nunito;src:url(FONTS/nunito-latin-800-normal.woff2);font-weight:800}
@page{size:A4;margin:0}
*{box-sizing:border-box}
body{margin:0;font-family:Nunito,sans-serif;color:#22303f;font-size:12.5pt;line-height:1.45}
.page{width:210mm;height:297mm;padding:14mm 15mm 16mm;position:relative;overflow:hidden;page-break-after:always;background:#fff}
h1,h2,h3{font-family:Baloo,sans-serif;margin:0;line-height:1.1;color:#1F3A5F}
h1{font-size:30pt;font-weight:800} h2{font-size:21pt;font-weight:800} h3{font-size:14pt;font-weight:800;margin-bottom:2mm}
.band{display:flex;justify-content:space-between;align-items:center;border-bottom:3px solid #E9B44C;padding-bottom:3mm;margin-bottom:5mm}
.tag{font-family:Baloo;font-weight:800;font-size:10.5pt;letter-spacing:.06em;text-transform:uppercase;color:#C0392B}
.ref{font-weight:700;color:#5b6b7c}
.foot{position:absolute;left:15mm;right:15mm;bottom:7mm;display:flex;justify-content:space-between;font-size:8.5pt;color:#8a96a3}
.box{border:2px solid #e3e8ee;border-radius:5mm;padding:4mm 5mm;margin-bottom:4mm}
.box.gold{background:#fff7e3;border-color:#f1d48f}
.box.blue{background:#eef4fb;border-color:#c9daee}
.box.red{background:#fdeeee;border-color:#f2c4c0}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:4mm}
.verse{font-family:Baloo;font-size:17pt;font-weight:700;color:#1F3A5F;line-height:1.2}
ul{margin:1mm 0 0;padding-left:5mm} li{margin-bottom:1mm}
table.rot{width:100%;border-collapse:collapse;font-size:11pt}
table.rot td{border-bottom:1px solid #e3e8ee;padding:2mm 1mm;vertical-align:top}
table.rot td:first-child{font-family:Baloo;font-weight:800;color:#C0392B;width:20mm}
.story p{margin:0 0 3mm;font-size:12.5pt}
.tip{font-size:10.5pt;color:#5b6b7c}
.name{display:flex;gap:6mm;margin-bottom:4mm;font-weight:700}
.name span{flex:1;border-bottom:2px solid #22303f;height:8mm}
.art{display:flex;justify-content:center;align-items:center;height:190mm}
.art svg{height:100%}
.line{border-bottom:1.5px solid #9aa7b4;height:9mm}
.ws{border-collapse:collapse;margin:0 auto}
.ws td{width:12mm;height:12mm;text-align:center;font-family:Baloo;font-weight:700;font-size:17pt;border:1.5px solid #c9daee}
.words{display:flex;flex-wrap:wrap;gap:3mm;justify-content:center;margin-top:6mm}
.words span{border:2px solid #E9B44C;border-radius:4mm;padding:1mm 4mm;font-family:Baloo;font-weight:800;font-size:13pt}
.cover{background:#1F3A5F;color:#fff;padding:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.cover h1{color:#fff;font-size:44pt}
.cover .sub{font-family:Baloo;font-size:18pt;color:#E9B44C;font-weight:700}
.cut{border:2px dashed #9aa7b4;border-radius:4mm;padding:5mm;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.cards4{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:6mm;height:250mm}
.marks{display:grid;grid-template-columns:repeat(4,1fr);gap:5mm;height:250mm}
.script p{margin:0 0 2mm} .script b{color:#C0392B;font-family:Baloo;font-size:12.5pt}
.check{display:flex;gap:3mm;align-items:flex-start;margin-bottom:2.5mm}
.check i{flex:none;width:5mm;height:5mm;border:2px solid #1F3A5F;border-radius:1mm;margin-top:1mm}
.small{font-size:10.5pt}
.cert{border:6px double #E9B44C;border-radius:6mm;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:12mm}
.fill{display:inline-block;border-bottom:2px solid #22303f;min-width:110mm;height:10mm}
"""


def page(inner, foot_left="", cls=""):
    f = f'<div class="foot"><span>{e(MARCA)} · uso na sua igreja e na sua casa</span><span>{e(foot_left)}</span></div>' if foot_left is not None else ""
    return f'<section class="page {cls}">{inner}{f}</section>'


def band(tag, title, ref=""):
    return f'<div class="band"><div><div class="tag">{e(tag)}</div><h2>{e(title)}</h2></div><div class="ref">{e(ref)}</div></div>'


def name_line():
    return '<div class="name">Nome: <span></span> Idade: <span style="flex:.25"></span></div>'


def cover(title, sub, line3, color="#1F3A5F"):
    stars = "".join(f'<div style="position:absolute;left:{x}%;top:{y}%">{small_star("#E9B44C", s)}</div>'
                    for x, y, s in [(10, 8, 30), (82, 12, 22), (70, 30, 14), (15, 70, 18), (85, 78, 34), (40, 90, 16), (25, 30, 12)])
    big = f'<svg width="150" height="150" viewBox="0 0 100 100"><polygon points="{star_points(50,52,46,19)}" fill="#E9B44C"/></svg>'
    return f'''<section class="page cover" style="background:{color}">{stars}
<div style="font-family:Baloo;font-weight:800;letter-spacing:.2em;color:#fff;opacity:.85;margin-bottom:8mm">{e(MARCA.upper())}</div>
{big}<h1 style="margin:8mm 15mm 4mm">{e(title)}</h1><div class="sub">{e(sub)}</div>
<div style="margin-top:10mm;font-size:13pt;opacity:.9;max-width:150mm">{e(line3)}</div></section>'''


def roteiro_rows():
    return [("5 min", "Acolhida e dinâmica de abertura"), ("10 min", "História bíblica (página seguinte)"),
            ("7 min", "Conversa: perguntas por faixa etária"), ("3 min", "Oração e versículo para memorizar"),
            ("15 min", "Atividade impressa por idade"), ("2 min", "Missão da semana e despedida")]


def lesson_pages(L, mes, total_label):
    tag = f"{mes} · Aula {L['n']}"
    rows = "".join(f"<tr><td>{a}</td><td>{e(b)}</td></tr>" for a, b in roteiro_rows())
    mats = "".join(f"<li>{e(m)}</li>" for m in L["materiais"])
    p1 = band(tag, L["titulo"], L["ref"]) + f'''
<div class="box gold"><div class="tag">Verdade central</div><div class="verse">{e(L["verdade"])}</div></div>
<div class="box blue"><div class="tag">Versículo para memorizar</div><div class="verse">“{e(L["versiculo"])}”</div><div class="ref small">{e(L["vref"])}</div></div>
<div class="grid2"><div class="box"><h3>Objetivo da aula</h3>{e(L["objetivo"])}</div><div class="box"><h3>Materiais</h3><ul>{mats}</ul></div></div>
<div class="box"><h3>Roteiro (cerca de 40 minutos)</h3><table class="rot">{rows}</table></div>
<div class="box red"><h3>Acolhida</h3>{e(L["acolhida"])}</div>'''
    story = "".join(f"<p>{e(x)}</p>" for x in L["historia"])
    p2 = band(tag, "História para contar", L["ref"]) + f'''
<div class="tip box blue">Dica: leia antes da aula e conte com suas palavras, olhando para as crianças. Faça pausas, mude a voz dos personagens e use os objetos da acolhida.</div>
<div class="story">{story}</div>'''
    qs = "".join(f'<div class="box"><div class="tag">{e(k)}</div><ul>{"".join(f"<li>{e(q)}</li>" for q in v)}</ul></div>' for k, v in L["perguntas"].items())
    p3 = band(tag, "Conversa, oração e missão", L["ref"]) + f'''
{qs}
<div class="box gold"><h3>Oração</h3>{e(L["oracao"])}</div>
<div class="box red"><h3>Missão da semana</h3>{e(L["missao"])}</div>
<div class="box"><h3>Atividades desta aula</h3><table class="rot"><tr><td>3 a 5</td><td>Colorir + labirinto</td></tr><tr><td>6 a 8</td><td>Labirinto + caça-palavras</td></tr><tr><td>9 a 11</td><td>Caça-palavras + desafio do versículo</td></tr></table></div>'''
    # atividades
    a1 = band(f"{tag} · 3 a 5 anos", "Pinte com capricho!", L["ref"]) + name_line() + f'<div class="art">{ART[L["desenho"]]()}</div><div style="text-align:center;font-family:Baloo;font-size:17pt;font-weight:800;color:#1F3A5F">{e(L["verdade"])}</div>'
    a, b = L["lab"]
    a2 = band(f"{tag} · 3 a 8 anos", "Labirinto", L["ref"]) + name_line() + f'<p style="text-align:center;font-weight:700;font-size:14pt">Ajude {e(a)} a chegar até {e(b)}! Comece no INÍCIO e vá até a estrela.</p><div style="height:200mm;display:flex;justify-content:center">{maze(11, 13, seed=f"{mes}{L["n"]}", cell=40)}</div>'
    g, placed = wordsearch(L["palavras"], 12, seed=f"{mes}{L['n']}ws")
    grid = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in g)
    words = "".join(f"<span>{w}</span>" for w in L["palavras"])
    a3 = band(f"{tag} · 6 a 11 anos", "Caça-palavras", L["ref"]) + name_line() + f'<p style="text-align:center;font-weight:700">Encontre as {len(L["palavras"])} palavras da história. Elas estão na horizontal e na vertical.</p><table class="ws">{grid}</table><div class="words">{words}</div>'
    verse_words = L["versiculo"].rstrip(".").split()
    keys = sorted(verse_words, key=lambda w: -len(w.strip(",.")))[:3]
    blanked = " ".join("<span style='display:inline-block;border-bottom:2px solid #22303f;min-width:30mm'>&nbsp;</span>" if w in keys else e(w) for w in verse_words)
    q911 = L["perguntas"]["9 a 11 anos"]
    resp = "".join(f'<p style="font-weight:700;margin:3mm 0 0">{i+1}. {e(q)}</p><div class="line"></div><div class="line"></div>' for i, q in enumerate(q911))
    a4 = band(f"{tag} · 9 a 11 anos", "Desafio do versículo", L["ref"]) + name_line() + f'''
<div class="box blue"><h3>Complete o versículo</h3><div class="verse" style="font-size:16pt;line-height:2">“{blanked}.”</div><div class="ref small">{e(L["vref"])} · Palavras: {", ".join(e(k.strip(",.")) for k in keys)}</div></div>
<div class="box"><h3>Pense e responda</h3>{resp}</div>
<div class="box gold"><h3>Desenhe ou escreva como você vai cumprir a missão da semana</h3><div style="height:42mm"></div></div>'''
    pages = [page(p1, total_label), page(p2, total_label), page(p3, total_label),
             page(a1, total_label), page(a2, total_label), page(a3, total_label), page(a4, total_label)]
    return pages, (L, g, placed, keys)


def gabarito(items, title):
    cells = []
    for L, g, placed, keys in items:
        sol = {c for cs in placed.values() for c in cs}
        grid = "".join("<tr>" + "".join(
            f'<td style="width:6mm;height:6mm;font-size:9pt;border:1px solid #e3e8ee;{"background:#E9B44C;" if (x, y) in sol else "color:#c3ccd6;"}">{c}</td>'
            for x, c in enumerate(row)) + "</tr>" for y, row in enumerate(g))
        cells.append(f'<div class="box"><h3>Aula {L["n"]} · {e(L["titulo"])}</h3><table class="ws" style="margin:0">{grid}</table><p class="small"><b>Versículo:</b> {e(", ".join(k.strip(",.") for k in keys))}</p></div>')
    return page(band("Para o professor", title) + f'<div class="grid2">{"".join(cells)}</div>', "Gabarito")


def intro_page(titulo, linhas, total_label):
    lis = "".join(f'<div class="check"><i></i><div>{x}</div></div>' for x in linhas)
    return page(band("Comece por aqui", titulo) + lis, total_label)


def build_natal():
    lab = "Kit Natal no Ministério Infantil"
    pages = [cover("Natal no Ministério Infantil", "Dezembro pronto: 4 aulas + teatro + lembrancinhas",
                   "Planos de aula completos, histórias para contar, atividades por idade (3 a 11 anos), mini teatro de Natal e lembrancinhas para recortar. É só imprimir e usar.")]
    pages.append(intro_page("Como usar este kit", [
        "<b>Imprima</b> as páginas de atividade de cada aula na quantidade de crianças da turma (frente apenas, papel A4 comum).",
        "<b>Leia o plano</b> da aula com antecedência: verdade central, versículo, materiais e acolhida estão na primeira página de cada aula.",
        "<b>Conte a história</b> com suas palavras. O texto está pronto, mas fica muito melhor quando você olha nos olhos das crianças.",
        "<b>Separe as atividades por idade</b>: colorir (3 a 5), labirinto (3 a 8), caça-palavras (6 a 11) e desafio do versículo (9 a 11).",
        "<b>Teatro de Natal</b>: ensaie nos domingos 3 e 4 e apresente no culto de Natal. Tem papel para todo mundo, inclusive para o coro de anjos.",
        "<b>Lembrancinhas</b>: imprima em papel mais firme (180 g) se puder. O cartão “Jesus é o melhor presente” é a missão da Aula 3.",
        "<b>Gabarito</b> do caça-palavras e do desafio está no final do kit.",
        "Os versículos estão em <b>paráfrase para crianças</b>, com a referência bíblica. Se preferir, leia na versão da Bíblia que a sua igreja usa.",
    ], lab))
    sched = [("1º domingo de dezembro", "Aula 1 · O anjo visita Maria"), ("2º domingo", "Aula 2 · José confia em Deus"),
             ("3º domingo", "Aula 3 · Jesus nasce em Belém + 1º ensaio do teatro"), ("4º domingo", "Aula 4 · Os magos adoram Jesus + ensaio geral"),
             ("Culto de Natal", "Apresentação do teatro + entrega das lembrancinhas")]
    rows = "".join(f'<div class="check"><i></i><div><b>{a}</b>: {b}<div class="line" style="height:7mm"></div></div></div>' for a, b in sched)
    pages.append(page(band("Planejamento", "Seu dezembro no ministério") + '<p>Anote a data de cada domingo e marque quando concluir.</p>' + rows +
                      '<div class="box gold"><h3>Lista de compras do mês</h3>Caixa de presente · lenço para vendar · lanterna · 3 caixinhas embrulhadas · estrela de papel grande · lápis de cor e giz de cera · papel 180 g para lembrancinhas · boneco para o teatro</div>', lab))
    gab = []
    for L in NATAL:
        ps, info = lesson_pages(L, "Dezembro", lab)
        pages += ps; gab.append(info)
    # teatro
    T = TEATRO
    pers = ", ".join(T["personagens"])
    sc_html = []
    for nome, falas in T["cenas"]:
        sc_html.append(f'<h3 style="margin-top:3mm">{e(nome)}</h3>' + "".join(f"<p><b>{e(p)}:</b> {e(f)}</p>" for p, f in falas))
    half = (len(sc_html) + 1) // 2
    pages.append(page(band("Culto de Natal", f"Teatro: {T['titulo']}", T["duracao"]) +
                      f'<div class="box blue small"><b>Personagens:</b> {e(pers)}.<br><b>Figurino simples:</b> {e(T["figurino"])}</div><div class="script">{"".join(sc_html[:half])}</div>', lab))
    pages.append(page(band("Culto de Natal", f"Teatro: {T['titulo']} (continuação)") + f'<div class="script">{"".join(sc_html[half:])}</div>' +
                      '<div class="box gold small"><b>Dica de ensaio:</b> crianças de 3 a 5 anos ficam ótimas como ovelhas e coro de anjos (não precisam decorar falas). Deixe as falas mais longas para quem tem 9 a 11 anos. O narrador pode ser um adolescente ou o próprio professor.</div>', lab))
    # lembrancinhas
    card = lambda: f'<div class="cut">{small_star("#E9B44C", 60)}<div style="font-family:Baloo;font-weight:800;font-size:20pt;color:#1F3A5F;margin:3mm 0">Jesus é o melhor presente!</div><div class="small">“Hoje nasceu para vocês o Salvador.” Lucas 2.11</div><div style="margin-top:4mm" class="small">De: ________________ Para: ________________</div></div>'
    pages.append(page(band("Lembrancinha · Missão da Aula 3", "Cartão: Jesus é o melhor presente") + f'<div class="cards4">{card()}{card()}{card()}{card()}</div>', lab))
    marks = "".join(f'<div class="cut" style="justify-content:space-between">{small_star("#C0392B", 40)}<div class="verse" style="font-size:15pt">“{e(L["versiculo"])}”</div><div class="small ref">{e(L["vref"].replace(" (paráfrase)", ""))}</div>{ART[L["desenho"]]().replace("<svg ", "<svg width=\'90\' ")}</div>' for L in NATAL)
    pages.append(page(band("Lembrancinha", "Marcadores de página com os versículos do mês") + f'<div class="marks">{marks}</div>', lab))
    pages.append(page(band("Lembrancinha · Culto de Natal", "Estrela de porta para pintar e pendurar") +
                      f'<div style="display:flex;justify-content:center;height:225mm"><svg viewBox="0 0 400 400" style="height:100%"><polygon points="{star_points(200,205,190,80)}" fill="none" stroke="#22303f" stroke-width="3" stroke-dasharray="10 6"/><circle cx="200" cy="40" r="9" fill="none" stroke="#22303f" stroke-width="3"/><text x="200" y="195" text-anchor="middle" font-family="Baloo" font-weight="800" font-size="30" fill="#1F3A5F">Jesus,</text><text x="200" y="230" text-anchor="middle" font-family="Baloo" font-weight="800" font-size="24" fill="#1F3A5F">a luz do mundo</text></svg></div><p class="small" style="text-align:center">Recorte na linha tracejada, faça um furo no círculo e passe uma fita.</p>', lab))
    pages.append(gabarito(gab, "Gabarito do caça-palavras e do desafio"))
    return pages


def build_janeiro():
    lab = "Janeiro Pronto"
    pages = [cover("Janeiro Pronto", "4 aulas para começar o ano com Jesus", "Mesma estrutura do kit de dezembro: plano de aula, história, perguntas por idade, missão da semana e atividades de 3 a 11 anos.", "#2E5E4E")]
    pages.append(intro_page("Como usar", [
        "Use uma aula por domingo de janeiro. Cada aula tem plano, história, conversa e 4 atividades por idade.",
        "A Aula 1 usa o <b>Cartão de metas</b> do final deste material: imprima um por criança.",
        "Gabarito no final.",
    ], lab))
    gab = []
    for L in JANEIRO:
        ps, info = lesson_pages(L, "Janeiro", lab)
        pages += ps; gab.append(info)
    meta = lambda: f'<div class="cut" style="align-items:flex-start;text-align:left"><div style="font-family:Baloo;font-weight:800;font-size:18pt;color:#2E5E4E">Minhas metas com Jesus para este ano</div><p class="small">Jesus crescia em sabedoria, em tamanho e no carinho de Deus e das pessoas. Lucas 2.52</p>' + "".join(f'<p style="margin:2mm 0 0"><b>{t}</b></p><div class="line" style="width:100%"></div>' for t in ["Com Deus, eu quero:", "Na escola, eu quero:", "Em casa, eu quero:"]) + "</div>"
    pages.append(page(band("Atividade da Aula 1", "Cartão de metas") + f'<div style="display:grid;grid-template-rows:1fr 1fr;gap:6mm;height:250mm">{meta()}{meta()}</div>', lab))
    pages.append(gabarito(gab, "Gabarito"))
    return pages


def build_certs():
    lab = "Certificados e Convites de Natal"
    pages = [cover("Certificados e Convites", "Para o Natal do ministério infantil", "Convites para o culto de Natal e 4 modelos de certificado. Imprima e preencha à mão com caneta bonita.", "#8E2A2A")]
    conv = lambda: f'<div class="cut" style="height:100%">{small_star("#E9B44C", 50)}<div class="tag" style="margin-top:3mm">Você é nosso convidado!</div><div style="font-family:Baloo;font-weight:800;font-size:26pt;color:#1F3A5F">Culto de Natal das Crianças</div><p>Venha ver o teatro <b>“O Presente Mais Esperado”</b></p><p>Dia: ______ / ______ às ______ h</p><p>Local: ______________________________</p><p class="small">Convidado por: ______________________</p></div>'
    pages.append(page(band("Convite", "Culto de Natal (2 por folha)") + f'<div style="display:grid;grid-template-rows:1fr 1fr;gap:8mm;height:250mm">{conv()}{conv()}</div>', lab))
    certs = [("Certificado de Participação", "participou com alegria das aulas de Natal do ministério infantil"),
             ("Certificado de Frequência", "esteve presente em todos os domingos de dezembro. Parabéns pela fidelidade!"),
             ("Estrela do Teatro de Natal", "brilhou no teatro “O Presente Mais Esperado”, contando a todos que Jesus é o melhor presente"),
             ("Guardião da Palavra", "memorizou os 4 versículos de Natal e guardou a Palavra de Deus no coração")]
    for t, txt in certs:
        pages.append(page(f'<div class="cert">{small_star("#E9B44C", 80)}<div class="tag" style="margin-top:6mm">{e(MARCA)}</div><h1 style="font-size:34pt;margin:4mm 0 10mm">{e(t)}</h1><p style="font-size:14pt">Certificamos que</p><div class="fill"></div><p style="font-size:14pt;max-width:150mm">{e(txt)}.</p><p style="margin-top:12mm">Igreja: <span class="fill" style="min-width:90mm"></span></p><div style="display:flex;gap:20mm;margin-top:14mm"><div><div class="fill" style="min-width:60mm"></div><div class="small">Professor(a)</div></div><div><div class="fill" style="min-width:40mm"></div><div class="small">Data</div></div></div></div>', None))
    return pages


import base64, re
def fontcss(css):
    def sub(m):
        f = FONTS / m.group(1)
        return "url(data:font/woff2;base64," + base64.b64encode(f.read_bytes()).decode() + ")"
    return re.sub(r"url\(FONTS/([^)]+)\)", sub, css)


def render(name, pages):
    doc = f"<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><style>{fontcss(CSS)}</style></head><body>{''.join(pages)}</body></html>"
    p = OUT / f"{name}.html"; p.write_text(doc, encoding="utf-8")
    return p


if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    jobs = {"kit-natal-ministerio-infantil": build_natal(), "bonus-janeiro-pronto": build_janeiro(),
            "bonus-certificados-e-convites-natal": build_certs()}
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page()
        for name, pages in jobs.items():
            h = render(name, pages)
            pg.goto(h.as_uri()); pg.wait_for_timeout(500)
            pg.pdf(path=str(OUT / f"{name}.pdf"), format="A4", print_background=True, prefer_css_page_size=True)
            print(name, len(pages), "páginas")
        b.close()
