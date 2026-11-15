# -*- coding: utf-8 -*-
"""Gera as 5 coleções (100 atividades cada) em PDF A4. Uso: python3 src/gerar.py"""
import os, random, unicodedata, sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit
sys.path.insert(0, os.path.dirname(__file__))
from conteudo import COLECOES, ICONES

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = os.path.join(os.path.dirname(RAIZ), "kit-natal", "fonts")
pdfmetrics.registerFont(TTFont("Baloo", os.path.join(FONTES, "baloo-2-latin-800-normal.ttf")))
pdfmetrics.registerFont(TTFont("Nunito", os.path.join(FONTES, "nunito-latin-700-normal.ttf")))
W, H = A4
M = 42
CINZA = HexColor("#5b6876"); CLARO = HexColor("#c9d1d9"); OURO = HexColor("#E9B44C")
TIPOS = ["Caça-palavras", "Labirinto", "Código secreto", "Pinte por número", "Complete o versículo",
         "Verdadeiro ou falso", "Ligue as colunas", "Palavras embaralhadas", "Copie e ilustre", "Acróstico"]

def ascii_up(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.upper()) if unicodedata.category(c) != "Mn")

def texto(c, s, x, y, fonte="Nunito", tam=12, larg=None, cor=black, lead=None, centro=False):
    c.setFont(fonte, tam); c.setFillColor(cor)
    linhas = simpleSplit(s, fonte, tam, larg) if larg else [s]
    lead = lead or tam * 1.35
    for l in linhas:
        if centro: c.drawCentredString(x, y, l)
        else: c.drawString(x, y, l)
        y -= lead
    return y

def cabecalho(c, col, tema, k, tipo, instr):
    cor = HexColor(col["cor"])
    c.setFillColor(cor); c.rect(0, H - 54, W, 54, stroke=0, fill=1)
    c.setFillColor(white); c.setFont("Baloo", 13)
    c.drawString(M, H - 34, "Coleção %d · %s" % (col["n"], col["nome"]))
    c.setFont("Nunito", 10); c.drawRightString(W - M, H - 34, "Atividade %d de 100" % k)
    c.setFillColor(cor); c.setFont("Baloo", 24); c.drawString(M, H - 92, tipo)
    c.setFillColor(black); c.setFont("Baloo", 14); c.drawString(M, H - 114, "%s  ·  %s" % (tema["titulo"], tema["ref"]))
    y = texto(c, instr, M, H - 136, tam=11.5, larg=W - 2 * M, cor=CINZA)
    c.setFont("Nunito", 10); c.setFillColor(CINZA)
    c.drawString(M, 30, "Nome: ______________________________")
    c.drawRightString(W - M, 30, "Estrela Guia Kids · para imprimir")
    return y - 8

def caca(c, col, t, k, rnd):
    y = cabecalho(c, col, t, k, TIPOS[0], "Encontre no quadro as 8 palavras da história. Elas estão na horizontal, na vertical e na diagonal.")
    n = 12; g = [[None] * n for _ in range(n)]
    pal = [ascii_up(p) for p in t["palavras"]]
    for p in sorted(pal, key=len, reverse=True):
        for _ in range(400):
            dx, dy = rnd.choice([(1, 0), (0, 1), (1, 1)])
            x0 = rnd.randrange(0, n - (len(p) - 1) * dx); y0 = rnd.randrange(0, n - (len(p) - 1) * dy)
            if all(g[y0 + i * dy][x0 + i * dx] in (None, ch) for i, ch in enumerate(p)):
                for i, ch in enumerate(p): g[y0 + i * dy][x0 + i * dx] = ch
                break
        else:
            raise RuntimeError("não coube: " + p)
    cel = 34; x0 = (W - n * cel) / 2; ytop = y - 6
    c.setStrokeColor(CLARO); c.setLineWidth(0.6)
    for r in range(n):
        for q in range(n):
            ch = g[r][q] or rnd.choice("ABCDEFGHIJLMNOPRSTUV")
            c.rect(x0 + q * cel, ytop - (r + 1) * cel, cel, cel)
            c.setFont("Baloo", 17); c.setFillColor(black)
            c.drawCentredString(x0 + q * cel + cel / 2, ytop - (r + 1) * cel + 11, ch)
    yy = ytop - n * cel - 30
    c.setFont("Baloo", 13); c.setFillColor(HexColor(col["cor"])); c.drawString(M, yy, "Palavras:")
    for i, p in enumerate(t["palavras"]):
        c.setFont("Nunito", 13); c.setFillColor(black)
        c.drawString(M + (i % 4) * 128, yy - 22 - (i // 4) * 22, "•  " + p)

def labirinto(c, col, t, k, rnd):
    y = cabecalho(c, col, t, k, TIPOS[1], "Ajude a encontrar o caminho! Comece na estrela e chegue até \"%s\"." % t["palavras"][0])
    cols, rows, cel = 15, 17, 32
    vis = [[False] * cols for _ in range(rows)]
    pd = [[True] * cols for _ in range(rows)]; pb = [[True] * cols for _ in range(rows)]
    pilha = [(0, 0)]; vis[0][0] = True
    while pilha:
        r, q = pilha[-1]
        viz = [(r + a, q + b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= r + a < rows and 0 <= q + b < cols and not vis[r + a][q + b]]
        if not viz: pilha.pop(); continue
        nr, nq = rnd.choice(viz)
        if nr == r: pd[r][min(q, nq)] = False
        else: pb[min(r, nr)][q] = False
        vis[nr][nq] = True; pilha.append((nr, nq))
    x0 = (W - cols * cel) / 2; ytop = y - 18
    c.setStrokeColor(black); c.setLineWidth(2.2); c.setLineCap(1)
    c.line(x0 + cel, ytop, x0 + cols * cel, ytop); c.line(x0, ytop, x0, ytop - rows * cel)
    for r in range(rows):
        for q in range(cols):
            xa, ya = x0 + q * cel, ytop - r * cel
            if pd[r][q] and not (r == rows - 1 and q == cols - 1 and False): c.line(xa + cel, ya, xa + cel, ya - cel)
            if pb[r][q] and not (r == rows - 1 and q == cols - 1): c.line(xa, ya - cel, xa + cel, ya - cel)
    import math
    cx, cy = x0 + cel / 2, ytop + 14; pts = []
    for i in range(10):
        a = math.radians(90 + i * 36); rr = 12 if i % 2 == 0 else 5
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    pth = c.beginPath(); pth.moveTo(*pts[0])
    for q in pts[1:]: pth.lineTo(*q)
    pth.close(); c.setFillColor(OURO); c.drawPath(pth, fill=1, stroke=0)
    c.setFont("Baloo", 13); c.setFillColor(HexColor(col["cor"]))
    c.drawRightString(x0 + cols * cel, ytop - rows * cel - 18, "Chegada: " + t["palavras"][0])

def codigo(c, col, t, k, rnd):
    y = cabecalho(c, col, t, k, TIPOS[2], "Cada número vale uma letra. Use a tabela para descobrir a mensagem secreta desta história.")
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; cel = 39; x0 = (W - 13 * cel) / 2
    for i, l in enumerate(letras):
        xa = x0 + (i % 13) * cel; ya = y - 10 - (i // 13) * 62
        c.setStrokeColor(CLARO); c.setFillColor(HexColor("#FFF8EA")); c.rect(xa, ya - 52, cel, 52, fill=1)
        c.setFillColor(black); c.setFont("Baloo", 18); c.drawCentredString(xa + cel / 2, ya - 22, l)
        c.setFillColor(HexColor(col["cor"])); c.setFont("Nunito", 13); c.drawCentredString(xa + cel / 2, ya - 44, str(i + 1))
    yy = y - 190
    for palavra in t["frase"].split():
        x = M
        for ch in palavra:
            c.setStrokeColor(black); c.setLineWidth(1.2); c.line(x, yy, x + 34, yy)
            c.setFont("Nunito", 13); c.setFillColor(HexColor(col["cor"])); c.drawCentredString(x + 17, yy - 18, str(letras.index(ch) + 1))
            x += 44
        yy -= 78
    c.setFont("Nunito", 12); c.setFillColor(CINZA)
    texto(c, "Agora leia a mensagem em voz alta e conte para alguém o que ela quer dizer.", M, 86, larg=W - 2 * M, cor=CINZA)

def pinte(c, col, t, k, rnd):
    grade, cores = ICONES[t["icone"]]
    y = cabecalho(c, col, t, k, TIPOS[3], "Pinte cada quadradinho com a cor do seu número e descubra o desenho escondido. Os quadradinhos sem número ficam em branco.")
    n = 12; cel = 38; x0 = (W - n * cel) / 2; ytop = y - 6
    for r in range(n):
        for q in range(n):
            ch = grade[r][q] if q < len(grade[r]) else "."
            c.setStrokeColor(CLARO); c.setLineWidth(0.7); c.rect(x0 + q * cel, ytop - (r + 1) * cel, cel, cel)
            if ch != ".":
                c.setFont("Nunito", 14); c.setFillColor(CINZA); c.drawCentredString(x0 + q * cel + cel / 2, ytop - (r + 1) * cel + 13, ch)
    yy = ytop - n * cel - 30; x = M
    c.setFont("Baloo", 13); c.setFillColor(HexColor(col["cor"])); c.drawString(M, yy, "Cores:")
    for num, nome in sorted(cores.items()):
        c.setFont("Nunito", 13); c.setFillColor(black); c.drawString(x + 60, yy, "%s = %s" % (num, nome)); x += 118

def complete(c, col, t, k, rnd):
    y = cabecalho(c, col, t, k, TIPOS[4], "Complete o versículo com as palavras do quadro. Depois leia em voz alta.")
    pal = t["versiculo"].split()
    cand = sorted([i for i, p in enumerate(pal) if len(p.strip(".,;:!?")) >= 4], key=lambda i: -len(pal[i]))[:3]
    banco = [pal[i].strip(".,;:!?") for i in cand]
    partes = [("_" * 12 + (p[-1] if p[-1] in ".,;:!?" else "")) if i in cand else p for i, p in enumerate(pal)]
    yy = texto(c, " ".join(partes), M, y - 40, fonte="Baloo", tam=22, larg=W - 2 * M, lead=50)
    c.setFont("Nunito", 13); c.setFillColor(CINZA); c.drawString(M, yy - 4, "(" + t["ref"] + ")")
    yy -= 60
    c.setFillColor(HexColor("#FFF8EA")); c.setStrokeColor(OURO); c.setLineWidth(2)
    c.roundRect(M, yy - 60, W - 2 * M, 70, 12, fill=1)
    rnd.shuffle(banco)
    for i, b in enumerate(banco):
        c.setFont("Baloo", 18); c.setFillColor(black); c.drawCentredString(M + (W - 2 * M) * (i + 0.5) / len(banco), yy - 34, b)
    yy -= 110
    yy = texto(c, "O que este versículo ensina para você?", M, yy, fonte="Baloo", tam=14, cor=HexColor(col["cor"]))
    for i in range(5):
        c.setStrokeColor(CLARO); c.setLineWidth(1); c.line(M, yy - 24 - i * 34, W - M, yy - 24 - i * 34)
    return banco

def vf(c, col, t, k, rnd):
    y = cabecalho(c, col, t, k, TIPOS[5], "Leia cada frase sobre a história. Marque V se for verdadeira e F se for falsa.")
    yy = y - 20
    for s, _ in t["vf"]:
        c.setStrokeColor(black); c.setLineWidth(1.4)
        c.roundRect(M, yy - 30, 34, 34, 6); c.roundRect(M + 42, yy - 30, 34, 34, 6)
        c.setFont("Baloo", 16); c.setFillColor(CLARO); c.drawCentredString(M + 17, yy - 20, "V"); c.drawCentredString(M + 59, yy - 20, "F")
        texto(c, s, M + 92, yy - 8, tam=14, larg=W - 2 * M - 92, lead=19)
        yy -= 66
    c.setFont("Baloo", 14); c.setFillColor(HexColor(col["cor"])); c.drawString(M, yy - 6, "Desenhe a parte da história de que você mais gostou:")
    c.setStrokeColor(CLARO); c.setLineWidth(1.5); c.setDash(6, 5); c.roundRect(M, 60, W - 2 * M, yy - 82, 14); c.setDash()

def ligue(c, col, t, k, rnd):
    y = cabecalho(c, col, t, k, TIPOS[6], "Ligue cada palavra da esquerda com o que combina com ela na direita.")
    dir_ = [b for _, b in t["pares"]]; rnd.shuffle(dir_)
    yy = y - 30
    for i, (a, _) in enumerate(t["pares"]):
        c.setFillColor(HexColor("#eef4fb")); c.setStrokeColor(HexColor(col["cor"])); c.setLineWidth(1.5)
        c.roundRect(M, yy - 44, 170, 52, 10, fill=1); c.roundRect(W - M - 230, yy - 44, 230, 52, 10, fill=1)
        c.setFillColor(black)
        texto(c, a, M + 85, yy - 22 if len(a) < 20 else yy - 14, fonte="Baloo", tam=14, larg=160, centro=True, lead=16)
        texto(c, dir_[i], W - M - 115, yy - 22 if pdfmetrics.stringWidth(dir_[i], "Nunito", 13) < 215 else yy - 14, tam=13, larg=215, centro=True, lead=16)
        c.circle(M + 182, yy - 18, 4, fill=1); c.circle(W - M - 242, yy - 18, 4, fill=1)
        yy -= 84
    yy -= 6
    c.setFont("Baloo", 14); c.setFillColor(HexColor(col["cor"])); c.drawString(M, yy, "Escreva uma frase sobre esta história:")
    for i in range(4):
        c.setStrokeColor(CLARO); c.setLineWidth(1); c.line(M, yy - 34 - i * 36, W - M, yy - 34 - i * 36)
    return dir_

def embaralhadas(c, col, t, k, rnd):
    y = cabecalho(c, col, t, k, TIPOS[7], "As letras se misturaram! Coloque em ordem e escreva as palavras da história.")
    yy = y - 24; usados = []
    for p in sorted(t["palavras"], key=len, reverse=True)[:6]:
        a = ascii_up(p); l = list(a)
        for _ in range(20):
            rnd.shuffle(l)
            if "".join(l) != a: break
        usados.append(a)
        c.setFont("Baloo", 22); c.setFillColor(HexColor(col["cor"])); c.drawString(M, yy - 20, " ".join(l))
        x = W - M - len(a) * 30
        for i in range(len(a)):
            c.setStrokeColor(black); c.setLineWidth(1.2); c.rect(x + i * 30, yy - 28, 26, 32)
        yy -= 72
    texto(c, "Dica: todas as palavras aparecem no caça-palavras desta história.", M, 80, tam=11, cor=CINZA)
    return usados

def copie(c, col, t, k, rnd):
    y = cabecalho(c, col, t, k, TIPOS[8], "Copie o versículo com a sua letra mais bonita. Depois faça um desenho da história na moldura.")
    yy = texto(c, "“" + t["versiculo"] + "”", M, y - 30, fonte="Baloo", tam=19, larg=W - 2 * M, lead=28, cor=HexColor("#9aa6b2"))
    c.setFont("Nunito", 12); c.setFillColor(CINZA); c.drawString(M, yy, t["ref"])
    yy -= 30
    for i in range(4):
        c.setStrokeColor(black); c.setLineWidth(1); c.line(M, yy - i * 40, W - M, yy - i * 40)
        c.setStrokeColor(CLARO); c.setDash(3, 4); c.line(M, yy - i * 40 + 16, W - M, yy - i * 40 + 16); c.setDash()
    base = yy - 3 * 40 - 30
    c.setStrokeColor(OURO); c.setLineWidth(4); c.roundRect(M, 60, W - 2 * M, base - 60, 16)

def acrostico(c, col, t, k, rnd):
    p = ascii_up(max(t["palavras"][:3], key=len))[:8]
    y = cabecalho(c, col, t, k, TIPOS[9], "Para cada letra da palavra %s, escreva uma palavra ou uma frase que lembre a história ou o que você aprendeu." % p)
    passo = min(74, (y - 90) / len(p)); yy = y - 26
    for ch in p:
        c.setFillColor(HexColor(col["cor"])); c.roundRect(M, yy - 44, 52, 52, 10, fill=1, stroke=0)
        c.setFillColor(white); c.setFont("Baloo", 30); c.drawCentredString(M + 26, yy - 30, ch)
        c.setStrokeColor(CLARO); c.setLineWidth(1.2); c.line(M + 68, yy - 40, W - M, yy - 40)
        yy -= passo

def capa(c, col):
    cor = HexColor(col["cor"])
    c.setFillColor(cor); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(OURO); c.setFont("Baloo", 22); c.drawCentredString(W / 2, H - 150, "ESTRELA GUIA KIDS")
    c.setFillColor(white); c.setFont("Baloo", 30); c.drawCentredString(W / 2, H - 230, "COLEÇÃO %d" % col["n"])
    texto(c, col["nome"], W / 2, H - 300, fonte="Baloo", tam=44, larg=W - 100, cor=white, lead=50, centro=True)
    c.setFillColor(OURO); c.roundRect(W / 2 - 170, 300, 340, 90, 20, fill=1, stroke=0)
    c.setFillColor(cor); c.setFont("Baloo", 34); c.drawCentredString(W / 2, 348, "100 ATIVIDADES")
    c.setFont("Nunito", 15); c.drawCentredString(W / 2, 318, "bíblicas para imprimir")
    c.setFillColor(white); c.setFont("Nunito", 16); c.drawCentredString(W / 2, 250, col["sub"])
    c.setFont("Nunito", 13); c.drawCentredString(W / 2, 222, "10 histórias · 10 tipos de atividade · 5 a 11 anos · com gabarito")
    c.setFont("Nunito", 10); c.drawCentredString(W / 2, 50, "Uso pessoal, familiar e em sala de aula. Proibida a revenda.")
    c.showPage()

def como_usar(c, col):
    cor = HexColor(col["cor"])
    c.setFillColor(cor); c.setFont("Baloo", 28); c.drawString(M, H - 80, "Como usar esta coleção")
    y = H - 120
    for s in ["Cada história tem 10 atividades diferentes: " + ", ".join(x.lower() for x in TIPOS) + ".",
              "Leia a história na Bíblia (a referência está no topo de cada folha) ou conte com as suas palavras antes de entregar a atividade.",
              "Imprima só as folhas que vai usar, em papel A4 comum. Tudo foi feito em preto e branco para gastar pouca tinta.",
              "Sugestão por idade: 5 a 7 anos — pinte por número, labirinto, ligue as colunas e copie e ilustre. 8 a 11 anos — todas.",
              "O gabarito está nas últimas páginas."]:
        y = texto(c, "•  " + s, M, y, tam=13, larg=W - 2 * M, lead=19) - 10
    c.setFillColor(cor); c.setFont("Baloo", 20); c.drawString(M, y - 16, "As 10 histórias")
    y -= 46
    for i, t in enumerate(col["temas"]):
        c.setFont("Nunito", 13); c.setFillColor(black)
        c.drawString(M, y, "%2d. %s (%s)" % (i + 1, t["titulo"], t["ref"])); c.setFillColor(CINZA)
        c.drawRightString(W - M, y, "atividades %d a %d" % (i * 10 + 1, i * 10 + 10)); y -= 22
    c.showPage()

def gabarito(c, col, resp):
    cor = HexColor(col["cor"]); y = H - 70
    c.setFillColor(cor); c.setFont("Baloo", 26); c.drawString(M, y, "Gabarito"); y -= 30
    for t, r in zip(col["temas"], resp):
        linhas = ["Código secreto: " + t["frase"], "Complete: " + ", ".join(r["complete"]),
                  "Verdadeiro ou falso: " + " · ".join("V" if v else "F" for _, v in t["vf"]),
                  "Ligue: " + "; ".join("%s → %s" % p for p in t["pares"]), "Embaralhadas: " + ", ".join(r["emb"])]
        alt = 18 + sum(len(simpleSplit(l, "Nunito", 9.5, W - 2 * M)) for l in linhas) * 12.5
        if y - alt < 50: c.showPage(); y = H - 60
        c.setFont("Baloo", 12); c.setFillColor(cor); c.drawString(M, y, t["titulo"]); y -= 15
        for l in linhas: y = texto(c, l, M, y, tam=9.5, larg=W - 2 * M, lead=12.5)
        y -= 6
    c.showPage()

def gerar(col, pasta):
    nome = "Colecao %d - %s.pdf" % (col["n"], col["nome"])
    c = canvas.Canvas(os.path.join(pasta, nome), pagesize=A4)
    c.setTitle("Coleção %d · %s · 100 atividades bíblicas" % (col["n"], col["nome"])); c.setAuthor("Estrela Guia Kids")
    capa(c, col); como_usar(c, col)
    k = 0; resp = []
    for ti, t in enumerate(col["temas"]):
        r = {}
        for fi, f in enumerate([caca, labirinto, codigo, pinte, complete, vf, ligue, embaralhadas, copie, acrostico]):
            k += 1; rnd = random.Random(col["n"] * 10000 + ti * 100 + fi)
            out = f(c, col, t, k, rnd)
            if f is complete: r["complete"] = out
            if f is embaralhadas: r["emb"] = out
            c.showPage()
        resp.append(r)
    gabarito(c, col, resp); c.save()
    return nome, k

if __name__ == "__main__":
    pasta = os.path.join(RAIZ, "out", "pdf"); os.makedirs(pasta, exist_ok=True)
    for col in COLECOES:
        print(gerar(col, pasta))
