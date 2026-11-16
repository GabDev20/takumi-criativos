# -*- coding: utf-8 -*-
"""Trilha do Foco: 250 atividades de atenção, memória e autocontrole (5 a 12 anos), PDF A4 P&B.
Uso: python3 src/gerar_foco.py"""
import os, math, random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = os.path.join(os.path.dirname(RAIZ), "kit-natal", "fonts")
pdfmetrics.registerFont(TTFont("Baloo", os.path.join(FONTES, "baloo-2-latin-800-normal.ttf")))
pdfmetrics.registerFont(TTFont("Nunito", os.path.join(FONTES, "nunito-latin-700-normal.ttf")))
W, H = A4
M = 42
COR = HexColor("#2E6FD8"); CINZA = HexColor("#5b6876"); CLARO = HexColor("#c9d1d9"); AMAR = HexColor("#F2B705")
MARCA = "Trilha do Foco"

ETAPAS = [
    ("Sustentar", "atenção sustentada", "Ficar na tarefa até o fim, sem se perder no meio.", HexColor("#2E6FD8")),
    ("Selecionar", "atenção seletiva", "Achar o que importa no meio de muita coisa.", HexColor("#16A085")),
    ("Guardar", "memória de trabalho", "Guardar instruções e informações enquanto faz a tarefa.", HexColor("#8E44AD")),
    ("Planejar", "planejamento", "Pensar antes de fazer e seguir uma ordem.", HexColor("#E67E22")),
    ("Controlar", "autocontrole", "Parar, pensar e só depois agir.", HexColor("#C0392B")),
]
FORMAS = ["circulo", "quadrado", "triangulo", "estrela", "coracao", "losango"]
NOME_FORMA = {"circulo": "círculo", "quadrado": "quadrado", "triangulo": "triângulo", "estrela": "estrela", "coracao": "coração", "losango": "losango"}


def texto(c, s, x, y, fonte="Nunito", tam=12, larg=None, cor=black, lead=None, centro=False):
    c.setFont(fonte, tam); c.setFillColor(cor)
    linhas = simpleSplit(s, fonte, tam, larg) if larg else [s]
    lead = lead or tam * 1.35
    for l in linhas:
        (c.drawCentredString if centro else c.drawString)(x, y, l)
        y -= lead
    return y


def forma(c, k, x, y, s, fill=False, lw=1.6):
    """desenha forma k centrada em (x,y) com raio s"""
    c.setStrokeColor(black); c.setFillColor(black); c.setLineWidth(lw)
    p = c.beginPath()
    if k == "circulo":
        c.circle(x, y, s, stroke=1, fill=1 if fill else 0); return
    if k == "quadrado":
        c.rect(x - s * .85, y - s * .85, s * 1.7, s * 1.7, stroke=1, fill=1 if fill else 0); return
    if k == "triangulo":
        pts = [(x, y + s), (x - s * .95, y - s * .75), (x + s * .95, y - s * .75)]
    elif k == "losango":
        pts = [(x, y + s), (x + s * .8, y), (x, y - s), (x - s * .8, y)]
    elif k == "estrela":
        pts = [(x + (s if i % 2 == 0 else s * .45) * math.cos(math.radians(90 + i * 36)),
                y + (s if i % 2 == 0 else s * .45) * math.sin(math.radians(90 + i * 36))) for i in range(10)]
    elif k == "coracao":
        pts = [(x + s * 16 * math.sin(t) ** 3 / 17, y + s * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) / 17 + s * .1)
               for t in [i * 2 * math.pi / 40 for i in range(40)]]
    p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    p.close(); c.drawPath(p, stroke=1, fill=1 if fill else 0)


def seta(c, x, y, s, direcao):
    ang = {"direita": 0, "cima": 90, "esquerda": 180, "baixo": 270}[direcao]
    c.saveState(); c.translate(x, y); c.rotate(ang)
    c.setFillColor(black); p = c.beginPath()
    p.moveTo(-s, -s * .3); p.lineTo(s * .2, -s * .3); p.lineTo(s * .2, -s * .7); p.lineTo(s, 0)
    p.lineTo(s * .2, s * .7); p.lineTo(s * .2, s * .3); p.lineTo(-s, s * .3); p.close()
    c.drawPath(p, stroke=0, fill=1); c.restoreState()


def cab(c, et, k, nome, instr, nivel):
    nm, fun, _, cor = ETAPAS[et]
    c.setFillColor(cor); c.rect(0, H - 54, W, 54, stroke=0, fill=1)
    c.setFillColor(white); c.setFont("Baloo", 13); c.drawString(M, H - 34, "Etapa %d · %s (%s)" % (et + 1, nm, fun))
    c.setFont("Nunito", 10); c.drawRightString(W - M, H - 34, "Atividade %d de 250" % k)
    c.setFillColor(cor); c.setFont("Baloo", 24); c.drawString(M, H - 92, nome)
    c.setFont("Nunito", 11); c.setFillColor(CINZA); c.drawRightString(W - M - 54, H - 92, "Nível")
    for i in range(3):
        c.setStrokeColor(cor); c.setFillColor(cor); c.circle(W - M - 40 + i * 16, H - 88, 5.5, stroke=1, fill=1 if i < nivel else 0)
    y = texto(c, instr, M, H - 116, tam=12, larg=W - 2 * M, cor=black, lead=16)
    c.setFont("Nunito", 10); c.setFillColor(CINZA)
    c.drawString(M, 30, "Nome: ____________________   Data: ___/___   Tempo: ______")
    c.drawRightString(W - M, 30, MARCA)
    # carinha de autoavaliação
    c.drawString(M, 46, "Como foi?   ( ) fácil   ( ) mais ou menos   ( ) difícil")
    return y - 8


# ---------------- ETAPA 1: SUSTENTAR ----------------
def cancelamento(c, k, rnd, nv):
    alvo = rnd.choice(FORMAS)
    n = [8, 10, 12][nv - 1]
    y = cab(c, 0, k, "Caça ao " + NOME_FORMA[alvo] if alvo not in ("estrela",) else "Caça à estrela",
            "Risque com um X todos os %ss da folha, linha por linha, da esquerda para a direita. Não pule nenhuma linha! No fim, escreva quantos você achou." % NOME_FORMA[alvo], nv)
    outros = [f for f in FORMAS if f != alvo][: 2 + nv]
    cel = (W - 2 * M) / n; tot = 0; yy = y - 10
    linhas = int((yy - 110) // cel)
    for r in range(linhas):
        for q in range(n):
            f = alvo if rnd.random() < .22 else rnd.choice(outros)
            tot += f == alvo
            forma(c, f, M + q * cel + cel / 2, yy - r * cel - cel / 2, cel * .3, fill=rnd.random() < .3)
    c.setFont("Baloo", 15); c.setFillColor(black); c.drawString(M, 70, "Achei ______ %ss." % NOME_FORMA[alvo])
    return "Atividade %d: %d %ss" % (k, tot, NOME_FORMA[alvo])


def trilha_numeros(c, k, rnd, nv):
    alterna = nv == 3
    n = [15, 20, 24][nv - 1]
    if alterna:
        seq = []
        for i in range(n // 2): seq += [str(i + 1), "ABCDEFGHIJKL"[i]]
        instr = "Ligue em ordem alternando número e letra: 1 → A → 2 → B → 3 → C... sem levantar o lápis. Vá devagar e confira antes de cada traço."
    else:
        seq = [str(i + 1) for i in range(n)]
        instr = "Ligue os números em ordem, do 1 ao %d, sem levantar o lápis. Procure com calma o próximo número antes de traçar." % n
    y = cab(c, 0, k, "Caminho em ordem", instr, nv)
    pts = []
    while len(pts) < len(seq):
        p = (rnd.uniform(M + 25, W - M - 25), rnd.uniform(110, y - 30))
        if all((p[0] - a) ** 2 + (p[1] - b) ** 2 > 62 ** 2 for a, b in pts): pts.append(p)
    for (x, yy), s in zip(pts, seq):
        c.setStrokeColor(black); c.setLineWidth(1.4); c.setFillColor(white); c.circle(x, yy, 17, fill=1)
        c.setFillColor(black); c.setFont("Baloo", 14); c.drawCentredString(x, yy - 5, s)
    c.setFillColor(AMAR); c.setFont("Baloo", 12); c.drawCentredString(pts[0][0], pts[0][1] + 22, "início")


def labirinto(c, k, rnd, nv):
    cols, rows = [(9, 10), (13, 15), (17, 20)][nv - 1]
    y = cab(c, 0, k, "Labirinto", "Encontre o caminho da entrada (estrela) até a saída. Use o dedo primeiro, depois o lápis. Se errar, volte com calma.", nv)
    cel = min((W - 2 * M) / cols, (y - 120) / rows)
    vis = [[False] * cols for _ in range(rows)]; pd = [[True] * cols for _ in range(rows)]; pb = [[True] * cols for _ in range(rows)]
    pilha = [(0, 0)]; vis[0][0] = True
    while pilha:
        r, q = pilha[-1]
        viz = [(r + a, q + b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= r + a < rows and 0 <= q + b < cols and not vis[r + a][q + b]]
        if not viz: pilha.pop(); continue
        nr, nq = rnd.choice(viz)
        if nr == r: pd[r][min(q, nq)] = False
        else: pb[min(r, nr)][q] = False
        vis[nr][nq] = True; pilha.append((nr, nq))
    x0 = (W - cols * cel) / 2; yt = y - 20
    c.setStrokeColor(black); c.setLineWidth(2.2); c.setLineCap(1)
    c.line(x0 + cel, yt, x0 + cols * cel, yt); c.line(x0, yt, x0, yt - rows * cel)
    for r in range(rows):
        for q in range(cols):
            xa, ya = x0 + q * cel, yt - r * cel
            if pd[r][q] and not (r == rows - 1 and q == cols - 1): c.line(xa + cel, ya, xa + cel, ya - cel)
            if pb[r][q]: c.line(xa, ya - cel, xa + cel, ya - cel)
    c.setFillColor(AMAR); forma(c, "estrela", x0 + cel / 2, yt + 14, 11, fill=True)
    c.setFont("Baloo", 13); c.setFillColor(black); c.drawString(x0 + cols * cel + 4, yt - rows * cel + cel / 2 - 4, "saída")


# ---------------- ETAPA 2: SELECIONAR ----------------
def diferente(c, k, rnd, nv):
    y = cab(c, 1, k, "Qual é o diferente?", "Em cada linha, um item é diferente dos outros. Circule o diferente. Olhe com atenção: às vezes a diferença é pequena!", nv)
    pares = [("b", "d"), ("p", "q"), ("m", "n"), ("6", "9"), ("E", "F"), ("O", "Q"), ("u", "v"), ("a", "o"), ("C", "G"), ("3", "8"), ("i", "l"), ("12", "21"), ("ab", "ba"), ("58", "85")]
    yy = y - 20; n = [6, 8, 10][nv - 1]; resp = []
    for linha in range(10):
        a, b = rnd.choice(pares)
        if rnd.random() < .5: a, b = b, a
        pos = rnd.randrange(n); resp.append(pos + 1)
        c.setFont("Baloo", 14); c.setFillColor(CINZA); c.drawString(M, yy - 6, "%d." % (linha + 1))
        for i in range(n):
            c.setFont("Baloo", 26 if nv < 3 else 22); c.setFillColor(black)
            c.drawCentredString(M + 50 + i * ((W - 2 * M - 60) / n) + 15, yy - 8, b if i == pos else a)
        yy -= 64
    return "Atividade %d: posições %s" % (k, ", ".join(map(str, resp)))


def conte(c, k, rnd, nv):
    usadas = rnd.sample(FORMAS, 2 + nv)
    y = cab(c, 1, k, "Conte e registre", "Conte quantas vezes aparece cada forma. Dica: marque com um pontinho cada forma que você já contou para não contar duas vezes.", nv)
    n = [6, 8, 9][nv - 1]; cel = (W - 2 * M) / n; cont = {f: 0 for f in usadas}
    linhas = [4, 5, 6][nv - 1]
    for r in range(linhas):
        for q in range(n):
            f = rnd.choice(usadas); cont[f] += 1
            forma(c, f, M + q * cel + cel / 2 + rnd.uniform(-6, 6), y - 20 - r * cel - cel / 2 + rnd.uniform(-6, 6), cel * .28)
    yy = y - 30 - linhas * cel - 20
    for i, f in enumerate(usadas):
        forma(c, f, M + 20, yy - i * 46, 14)
        c.setFont("Baloo", 16); c.setFillColor(black); c.drawString(M + 48, yy - i * 46 - 6, "%s: ______" % NOME_FORMA[f])
    return "Atividade %d: " % k + ", ".join("%s %d" % (NOME_FORMA[f], v) for f, v in cont.items())


def letras_alvo(c, k, rnd, nv):
    alvo = rnd.choice(["A", "E", "O", "M", "S", "R", "T"]) if nv < 3 else rnd.choice(["b", "d", "p", "q"])
    y = cab(c, 1, k, "Caça-letra", "Circule todas as letras \"%s\". Siga linha por linha com o dedo. No fim, conte quantas circulou." % alvo, nv)
    pool = "ABCDEFGHIJLMNOPRSTUV" if nv < 3 else "bdpqbdpqhn"
    n = 14; cel = (W - 2 * M) / n; tot = 0
    for r in range(14):
        for q in range(n):
            ch = alvo if rnd.random() < .16 else rnd.choice(pool.replace(alvo, ""))
            tot += ch == alvo
            c.setFont("Baloo", 20); c.setFillColor(black); c.drawCentredString(M + q * cel + cel / 2, y - 26 - r * 34, ch)
    c.setFont("Baloo", 15); c.drawString(M, 75, "Circulei ______ letras %s." % alvo)
    return "Atividade %d: %d letras %s" % (k, tot, alvo)


# ---------------- ETAPA 3: GUARDAR ----------------
def observe(c, k, rnd, nv):
    n = [4, 6, 8][nv - 1]
    y = cab(c, 2, k, "Olhe, guarde e desenhe", "1) Olhe as figuras do quadro de cima por 20 segundos.  2) Dobre a folha na linha pontilhada para esconder.  3) Desenhe no quadro de baixo as figuras que você lembrar, no mesmo lugar.", nv)
    meio = (y + 60) / 2
    c.setStrokeColor(CLARO); c.setDash(6, 5); c.line(M - 20, meio, W - M + 20, meio); c.setDash()
    c.setFont("Nunito", 10); c.setFillColor(CINZA); c.drawString(M, meio + 4, "dobre aqui")
    cols = 4; rows = 2 if n <= 8 else 3
    cw = (W - 2 * M) / cols; ch = (y - meio - 30) / rows
    for box in (0, 1):
        top = y - 10 if box == 0 else meio - 14
        c.setStrokeColor(black); c.setLineWidth(1.5); c.roundRect(M, top - rows * ch, W - 2 * M, rows * ch, 12)
    lugares = rnd.sample([(r, q) for r in range(rows) for q in range(cols)], n)
    for r, q in lugares:
        forma(c, rnd.choice(FORMAS), M + q * cw + cw / 2, y - 10 - r * ch - ch / 2, min(cw, ch) * .28, fill=rnd.random() < .5)


def instrucoes(c, k, rnd, nv):
    y = cab(c, 2, k, "Ouça e faça", "Um adulto lê UMA instrução por vez, só uma vez. A criança guarda na cabeça e só então faz. Quanto mais longa a instrução, mais a memória trabalha.", nv)
    n = 8; cel = (W - 2 * M) / n; fs = [rnd.choice(FORMAS) for _ in range(n)]
    for i, f in enumerate(fs):
        forma(c, f, M + i * cel + cel / 2, y - 40, cel * .3)
        c.setFont("Nunito", 11); c.setFillColor(CINZA); c.drawCentredString(M + i * cel + cel / 2, y - 80, str(i + 1))
    acoes = ["faça um X no", "circule o", "pinte o", "faça um ponto dentro do", "sublinhe o"]
    yy = y - 120; feitos = []
    for j in range(6):
        partes = []
        for _ in range(nv if j < 3 else nv + 1):
            i = rnd.randrange(n); partes.append("%s %dº (%s)" % (rnd.choice(acoes), i + 1, NOME_FORMA[fs[i]]))
        frase = ", depois ".join(partes)
        yy = texto(c, "%d. %s." % (j + 1, frase[0].upper() + frase[1:]), M, yy, tam=13, larg=W - 2 * M, lead=18) - 12
    c.setStrokeColor(CLARO); c.line(M, 95, W - M, 95)
    texto(c, "Para o adulto: se a criança acertar 5 ou 6, tente ler duas instruções de uma vez na próxima.", M, 82, tam=10, larg=W - 2 * M, cor=CINZA)


def copie_grade(c, k, rnd, nv):
    n = [4, 5, 6][nv - 1]
    y = cab(c, 2, k, "Copie o desenho", "Copie o desenho da grade de cima na grade de baixo, ponto por ponto. Conte os pontos antes de traçar cada linha.", nv)
    cel = min(46, (y - 140) / (2 * n + 2)); x0 = (W - n * cel) / 2
    pts = [(rnd.randrange(n + 1), rnd.randrange(n + 1)) for _ in range(3 + nv * 2)]
    for g, top in enumerate((y - 20, y - 50 - (n + 1) * cel)):
        for i in range(n + 1):
            for j in range(n + 1):
                c.setFillColor(black); c.circle(x0 + i * cel, top - j * cel, 2.4, fill=1, stroke=0)
        if g == 0:
            c.setStrokeColor(COR); c.setLineWidth(3); c.setLineCap(1)
            for a, b in zip(pts, pts[1:]):
                c.line(x0 + a[0] * cel, top - a[1] * cel, x0 + b[0] * cel, top - b[1] * cel)


# ---------------- ETAPA 4: PLANEJAR ----------------
def sudoku(c, k, rnd, nv):
    n = 4 if nv < 3 else 6
    usadas = FORMAS[:n]
    y = cab(c, 3, k, "Sudoku de formas", "Desenhe as formas que faltam. Regra: cada forma aparece uma vez só em cada linha, em cada coluna e em cada bloco grosso. Pense antes de desenhar!", nv)
    if n == 4:
        base = [[0, 1, 2, 3], [2, 3, 0, 1], [1, 0, 3, 2], [3, 2, 1, 0]]; br, bc = 2, 2
    else:
        base = [[(r * 3 + r // 2 + q) % 6 for q in range(6)] for r in range(6)]; br, bc = 2, 3
    perm = list(range(n)); rnd.shuffle(perm)
    grid = [[perm[v] for v in row] for row in base]
    vazios = set(rnd.sample(range(n * n), [5, 8, 16][nv - 1]))
    cel = 90 if n == 4 else 70; x0 = (W - n * cel) / 2; top = y - 20
    for r in range(n):
        for q in range(n):
            c.setStrokeColor(black); c.setLineWidth(1); c.rect(x0 + q * cel, top - (r + 1) * cel, cel, cel)
            if r * n + q not in vazios: forma(c, usadas[grid[r][q]], x0 + q * cel + cel / 2, top - r * cel - cel / 2, cel * .28)
    c.setLineWidth(3.5)
    for r in range(0, n + 1, br): c.line(x0, top - r * cel, x0 + n * cel, top - r * cel)
    for q in range(0, n + 1, bc): c.line(x0 + q * cel, top, x0 + q * cel, top - n * cel)
    yy = top - n * cel - 40
    c.setFont("Nunito", 12); c.setFillColor(CINZA); c.drawString(M, yy, "Formas deste sudoku:")
    for i, f in enumerate(usadas): forma(c, f, M + 160 + i * 50, yy + 4, 13)


def sequencia(c, k, rnd, nv):
    y = cab(c, 3, k, "Complete a sequência", "Descubra a regra de cada sequência e desenhe as duas próximas figuras nos quadrados vazios.", nv)
    yy = y - 40; resp = []
    for linha in range(7):
        tam = [2, 3, 4][nv - 1] if linha % 2 == 0 else [2, 3, 3][nv - 1]
        padrao = rnd.sample(FORMAS, tam)
        if nv >= 2 and rnd.random() < .4: padrao = padrao + [padrao[0]]
        seqf = [padrao[i % len(padrao)] for i in range(8)]
        for i in range(8):
            x = M + 30 + i * 62
            if i < 6: forma(c, seqf[i], x, yy, 18)
            else:
                c.setStrokeColor(black); c.setLineWidth(1.4); c.setDash(4, 3); c.rect(x - 24, yy - 24, 48, 48); c.setDash()
        resp.append("/".join(NOME_FORMA[f] for f in seqf[6:]))
        yy -= 84
    return "Atividade %d: " % k + "; ".join(resp)


def plano(c, k, rnd, nv):
    situ = [("arrumar a mochila para a escola", ["guardar o caderno", "conferir o horário do dia", "colocar o estojo", "fechar o zíper", "pendurar a mochila na porta"]),
            ("tomar banho", ["pegar a toalha", "tirar a roupa", "ensaboar o corpo", "enxaguar", "secar e vestir o pijama"]),
            ("fazer a lição de casa", ["sentar à mesa", "pegar o material", "ler o enunciado", "fazer a tarefa", "guardar tudo na mochila"]),
            ("escovar os dentes", ["pegar a escova", "colocar a pasta", "escovar em cima e embaixo", "enxaguar a boca", "lavar a escova"]),
            ("preparar um sanduíche", ["lavar as mãos", "pegar o pão", "passar o recheio", "fechar o sanduíche", "limpar a mesa"]),
            ("arrumar o quarto", ["recolher os brinquedos do chão", "guardar na caixa", "dobrar a roupa", "arrumar a cama", "jogar o lixo fora"]),
            ("ir dormir", ["vestir o pijama", "escovar os dentes", "ir ao banheiro", "deitar na cama", "apagar a luz"])]
    nome, passos = situ[(k + nv) % len(situ)]
    y = cab(c, 3, k, "Primeiro, depois, por último", "Os passos para %s estão fora de ordem. Numere de 1 a %d na ordem certa. Depois, escreva uma tarefa sua e os passos dela." % (nome, len(passos)), nv)
    emb = passos[:]; rnd.shuffle(emb)
    yy = y - 24
    for p in emb:
        c.setStrokeColor(black); c.setLineWidth(1.4); c.roundRect(M, yy - 30, 40, 40, 8)
        c.setFont("Baloo", 17); c.setFillColor(black); c.drawString(M + 60, yy - 16, p)
        yy -= 56
    yy -= 10
    c.setFont("Baloo", 15); c.setFillColor(ETAPAS[3][3]); c.drawString(M, yy, "Minha tarefa: __________________________")
    for i in range(4):
        c.setFont("Baloo", 14); c.setFillColor(black); c.drawString(M, yy - 40 - i * 40, "%d." % (i + 1))
        c.setStrokeColor(CLARO); c.line(M + 24, yy - 42 - i * 40, W - M, yy - 42 - i * 40)
    return "Atividade %d: " % k + " → ".join(passos)


# ---------------- ETAPA 5: CONTROLAR ----------------
def setas(c, k, rnd, nv):
    dirs = ["direita", "esquerda", "cima", "baixo"]
    y = cab(c, 4, k, "Setas trocadas", ("Diga em voz alta para onde cada seta aponta, o mais rápido que conseguir sem errar." if nv == 1 else
                                         "Diga em voz alta para onde a seta aponta. ATENÇÃO: nas setas dentro de um quadrado, diga o CONTRÁRIO (direita vira esquerda, cima vira baixo)."), nv)
    n = 7; cel = (W - 2 * M) / n
    for r in range(8):
        for q in range(n):
            x = M + q * cel + cel / 2; yy = y - 30 - r * 66
            if nv > 1 and rnd.random() < [0, .3, .5][nv - 1]:
                c.setStrokeColor(black); c.setLineWidth(1.6); c.rect(x - 24, yy - 24, 48, 48)
            seta(c, x, yy, 17, rnd.choice(dirs))
    texto(c, "Para o adulto: marque o tempo. Na próxima vez, o objetivo é errar menos, não ir mais rápido.", M, 72, tam=10, larg=W - 2 * M, cor=CINZA)


def semaforo(c, k, rnd, nv):
    alvo, proib = rnd.sample(FORMAS, 2)
    y = cab(c, 4, k, "Sinal verde, sinal vermelho",
            "Um adulto aponta as figuras uma por uma. Quando for %s, a criança bate palma. Quando for %s, fica parada como estátua. Qualquer outra figura: diz \"passa\"." % (NOME_FORMA[alvo], NOME_FORMA[proib]) +
            (" Nível 3: no %s com fundo preto, troca: fica parada!" % NOME_FORMA[alvo] if nv == 3 else ""), nv)
    outros = [f for f in FORMAS if f not in (alvo, proib)]
    n = 7; cel = (W - 2 * M) / n
    for r in range(8):
        for q in range(n):
            u = rnd.random(); f = alvo if u < .35 else proib if u < .55 else rnd.choice(outros)
            forma(c, f, M + q * cel + cel / 2, y - 30 - r * 66, 20, fill=(nv == 3 and f == alvo and rnd.random() < .4))


def pare_pense(c, k, rnd, nv):
    sits = ["Seu irmão pegou seu brinquedo sem pedir.", "Você perdeu no jogo de tabuleiro.", "A professora pediu silêncio e você quer muito falar.",
            "Você quer jogar no celular, mas ainda não fez a lição.", "Um colega empurrou você na fila.", "Você derrubou suco na mesa.",
            "Sua mãe disse que agora não dá para ir ao parque.", "Você está esperando sua vez no escorregador.", "Você errou a conta e o lápis quebrou.",
            "Um amigo não quis brincar com você hoje.", "Você ganhou um doce, mas é só depois do almoço.", "A tarefa está difícil e você quer desistir."]
    s = sits[(k * 7 + nv) % len(sits)]
    y = cab(c, 4, k, "Pare, pense, faça", "Leia a situação com um adulto. Antes de responder, faça o sinal de PARE com a mão e respire fundo 3 vezes. Depois preencha.", nv)
    c.setFillColor(HexColor("#FDECEA")); c.setStrokeColor(ETAPAS[4][3]); c.setLineWidth(2); c.roundRect(M, y - 90, W - 2 * M, 80, 14, fill=1)
    texto(c, s, W / 2, y - 48, fonte="Baloo", tam=19, larg=W - 2 * M - 40, centro=True, lead=24)
    yy = y - 130
    for cor, tit in ((HexColor("#C0392B"), "PARE: o que eu sinto agora?"), (AMAR, "PENSE: o que eu posso fazer? (2 ideias)"), (HexColor("#16A085"), "FAÇA: qual ideia é a melhor e por quê?")):
        c.setFillColor(cor); c.circle(M + 14, yy + 4, 12, fill=1, stroke=0)
        c.setFont("Baloo", 16); c.setFillColor(black); c.drawString(M + 36, yy - 2, tit)
        for i in range(3):
            c.setStrokeColor(CLARO); c.setLineWidth(1); c.line(M, yy - 34 - i * 32, W - M, yy - 34 - i * 32)
        yy -= 150


TIPOS = [[cancelamento, trilha_numeros, labirinto], [diferente, conte, letras_alvo], [observe, instrucoes, copie_grade],
         [sudoku, sequencia, plano], [setas, semaforo, pare_pense]]


def capa(c):
    c.setFillColor(HexColor("#123B7A")); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(AMAR); c.setFont("Baloo", 20); c.drawCentredString(W / 2, H - 140, "5 A 12 ANOS · PARA IMPRIMIR")
    c.setFillColor(white); c.setFont("Baloo", 62); c.drawCentredString(W / 2, H - 230, "Trilha do Foco")
    texto(c, "250 atividades de atenção, memória e autocontrole", W / 2, H - 285, fonte="Baloo", tam=24, larg=W - 120, cor=white, centro=True, lead=30)
    for i, (nm, fun, _, cor) in enumerate(ETAPAS):
        y = H - 400 - i * 62
        c.setFillColor(cor); c.roundRect(110, y - 20, W - 220, 50, 25, fill=1, stroke=0)
        c.setFillColor(white); c.setFont("Baloo", 20); c.drawString(135, y - 2, "Etapa %d · %s" % (i + 1, nm))
        c.setFont("Nunito", 12); c.drawRightString(W - 135, y, fun)
    c.setFillColor(white); c.setFont("Nunito", 12)
    c.drawCentredString(W / 2, 90, "Material de apoio em casa e na escola. Não substitui avaliação ou acompanhamento profissional.")
    c.drawCentredString(W / 2, 70, "Uso pessoal, familiar, em sala de aula e em atendimento. Proibida a revenda.")
    c.showPage()


def como_usar(c):
    c.setFillColor(COR); c.setFont("Baloo", 28); c.drawString(M, H - 80, "Como usar a Trilha do Foco")
    y = H - 118
    for s in ["A trilha tem 5 etapas. Cada etapa treina uma habilidade por vez e tem 50 atividades, das mais fáceis (nível 1) às mais desafiadoras (nível 3).",
              "Faça 1 ou 2 atividades por dia, de 10 a 15 minutos. Pouco e todo dia funciona melhor do que muito de uma vez.",
              "Comece pela Etapa 1. Pode intercalar etapas, mas respeite a ordem dos níveis dentro de cada uma.",
              "Elogie o esforço e a calma, não a velocidade. Errar faz parte do treino.",
              "Marque o tempo e o \"como foi?\" no rodapé. Assim você vê a evolução de semana em semana.",
              "Imprima em papel A4 comum, em preto e branco. O gabarito está nas últimas páginas.",
              "Este é um material educativo de apoio. Não é tratamento e não substitui o acompanhamento de médico, psicólogo ou psicopedagogo."]:
        y = texto(c, "•  " + s, M, y, tam=13, larg=W - 2 * M, lead=19) - 10
    c.setFont("Baloo", 20); c.setFillColor(COR); c.drawString(M, y - 14, "As 5 etapas"); y -= 46
    for i, (nm, fun, desc, cor) in enumerate(ETAPAS):
        c.setFillColor(cor); c.roundRect(M, y - 10, 30, 30, 8, fill=1, stroke=0)
        c.setFillColor(white); c.setFont("Baloo", 16); c.drawCentredString(M + 15, y - 1, str(i + 1))
        c.setFillColor(black); c.setFont("Baloo", 15); c.drawString(M + 44, y + 2, "%s · %s" % (nm, fun))
        c.setFont("Nunito", 11); c.setFillColor(CINZA); c.drawString(M + 44, y - 12, desc + "  (atividades %d a %d)" % (i * 50 + 1, i * 50 + 50))
        y -= 50
    c.showPage()


def mapa(c):
    c.setFillColor(COR); c.setFont("Baloo", 28); c.drawString(M, H - 80, "Meu mapa da trilha")
    texto(c, "Pinte uma bolinha a cada atividade terminada. Ao completar uma etapa, ganhe uma estrela!", M, H - 110, tam=13, larg=W - 2 * M)
    y = H - 160
    for i, (nm, _, _, cor) in enumerate(ETAPAS):
        c.setFillColor(cor); c.setFont("Baloo", 16); c.drawString(M, y, "Etapa %d · %s" % (i + 1, nm))
        for j in range(50):
            c.setStrokeColor(cor); c.setLineWidth(1.3); c.circle(M + 10 + (j % 25) * 20.5, y - 22 - (j // 25) * 22, 8)
        forma(c, "estrela", W - M - 14, y - 30, 14)
        y -= 120
    c.showPage()


def certificado(c):
    c.setStrokeColor(AMAR); c.setLineWidth(8); c.rect(30, 30, W - 60, H - 60)
    c.setFillColor(COR); c.setFont("Baloo", 40); c.drawCentredString(W / 2, H - 200, "Certificado")
    c.setFont("Baloo", 22); c.setFillColor(black); c.drawCentredString(W / 2, H - 260, "Completei a Trilha do Foco!")
    c.setStrokeColor(black); c.setLineWidth(1); c.line(120, H / 2, W - 120, H / 2)
    c.setFont("Nunito", 13); c.drawCentredString(W / 2, H / 2 - 20, "nome")
    for i in range(5): forma(c, "estrela", W / 2 - 160 + i * 80, H / 2 - 120, 24)
    c.drawCentredString(W / 2, 140, "Data: ___/___/______")
    c.showPage()


def gerar(pasta):
    nome = "Trilha do Foco - 250 atividades.pdf"
    c = canvas.Canvas(os.path.join(pasta, nome), pagesize=A4)
    c.setTitle("Trilha do Foco · 250 atividades de atenção, memória e autocontrole"); c.setAuthor(MARCA)
    capa(c); como_usar(c); mapa(c)
    k = 0; gab = []
    for et in range(5):
        for i in range(50):
            k += 1; nv = 1 + i * 3 // 50
            f = TIPOS[et][i % 3]
            r = f(c, k, random.Random(k * 31 + 7), nv)
            if r: gab.append(r)
            c.showPage()
    c.setFillColor(COR); c.setFont("Baloo", 26); c.drawString(M, H - 70, "Gabarito"); y = H - 100
    for g in gab:
        for l in simpleSplit(g, "Nunito", 9, W - 2 * M):
            if y < 50: c.showPage(); y = H - 60
            c.setFont("Nunito", 9); c.setFillColor(black); c.drawString(M, y, l); y -= 11.5
    c.showPage(); certificado(c); c.save()
    return nome, k


if __name__ == "__main__":
    pasta = os.path.join(RAIZ, "out", "pdf"); os.makedirs(pasta, exist_ok=True)
    print(gerar(pasta))
