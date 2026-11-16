# -*- coding: utf-8 -*-
"""Lê Comigo: kit de leitura em casa, da sílaba à frase (4 a 8 anos). 3 apostilas PDF A4 P&B.
Uso: python3 src/gerar_leitura.py"""
import os, random, unicodedata
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
CINZA = HexColor("#5b6876"); CLARO = HexColor("#c9d1d9"); AMAR = HexColor("#F2B705")
MARCA = "Lê Comigo"
CORES = [HexColor("#E4572E"), HexColor("#17BEBB"), HexColor("#7B2CBF")]

# família: (sílabas, palavras) — palavras que começam com sílabas da família
SIMPLES = [
    ("B", ["BA", "BE", "BI", "BO", "BU"], ["BOLA", "BOCA", "BEBÊ", "BICO", "BULE", "BOTA", "BALA", "BIFE"]),
    ("C", ["CA", "CO", "CU"], ["CASA", "COLA", "CUCA", "CAMA", "COPO", "CAJU", "CUBO", "CAVALO"]),
    ("D", ["DA", "DE", "DI", "DO", "DU"], ["DADO", "DEDO", "DIA", "DOCE", "DUDA", "DAMA", "DOMINÓ", "DIVA"]),
    ("F", ["FA", "FE", "FI", "FO", "FU"], ["FACA", "FOCA", "FITA", "FUMAÇA", "FADA", "FEIJÃO", "FOGO", "FILA"]),
    ("G", ["GA", "GO", "GU"], ["GATO", "GALO", "GOLA", "GOMA", "GULA", "GALINHA", "GOTA", "GAVETA"]),
    ("J", ["JA", "JE", "JI", "JO", "JU"], ["JACARÉ", "JOGO", "JUBA", "JANELA", "JIBOIA", "JOANINHA", "JUDÔ", "JECA"]),
    ("L", ["LA", "LE", "LI", "LO", "LU"], ["LATA", "LEÃO", "LIXO", "LOJA", "LUA", "LAGO", "LIMÃO", "LUVA"]),
    ("M", ["MA", "ME", "MI", "MO", "MU"], ["MALA", "MESA", "MIMO", "MOLA", "MULA", "MACACO", "MENINO", "MOTO"]),
    ("N", ["NA", "NE", "NI", "NO", "NU"], ["NAVIO", "NETO", "NINHO", "NOVELO", "NUVEM", "NABO", "NEVE", "NOTA"]),
    ("P", ["PA", "PE", "PI", "PO", "PU"], ["PATO", "PETECA", "PIPA", "POTE", "PULO", "PANELA", "PERA", "PIÃO"]),
    ("R", ["RA", "RE", "RI", "RO", "RU"], ["RATO", "REDE", "RIO", "RODA", "RUA", "RAPOSA", "REI", "ROSA"]),
    ("S", ["SA", "SE", "SI", "SO", "SU"], ["SAPO", "SELO", "SINO", "SOFÁ", "SUCO", "SAPATO", "SEMENTE", "SOPA"]),
    ("T", ["TA", "TE", "TI", "TO", "TU"], ["TATU", "TELA", "TIGELA", "TOMATE", "TUCANO", "TAPETE", "TETO", "TOCA"]),
    ("V", ["VA", "VE", "VI", "VO", "VU"], ["VACA", "VELA", "VIOLÃO", "VOVÓ", "VULCÃO", "VASO", "VELHO", "VIOLA"]),
    ("X", ["XA", "XE", "XI", "XO", "XU"], ["XALE", "XERIFE", "XÍCARA", "XODÓ", "XAMPU", "XADREZ", "XERETA", "XUXA"]),
    ("Z", ["ZA", "ZE", "ZI", "ZO", "ZU"], ["ZEBRA", "ZERO", "ZÍPER", "ZOOLÓGICO", "ZUMBIDO", "ZANGADO", "ZELO", "ZORRO"]),
]
# palavras com sílaba marcada entre colchetes
COMPLEXAS = [
    ("NH", ["NHA", "NHE", "NHI", "NHO", "NHU"], ["MI[NHO]CA", "GALI[NHA]", "NI[NHO]", "PI[NHA]", "SO[NHO]", "BA[NHO]", "CARI[NHO]", "VI[NHO]"]),
    ("LH", ["LHA", "LHE", "LHI", "LHO", "LHU"], ["FO[LHA]", "PA[LHA]ÇO", "O[LHO]", "COE[LHO]", "TOA[LHA]", "AGU[LHA]", "ABE[LHA]", "MI[LHO]"]),
    ("CH", ["CHA", "CHE", "CHI", "CHO", "CHU"], ["[CHA]VE", "[CHU]VA", "[CHI]NELO", "[CHO]COLATE", "BI[CHO]", "MO[CHI]LA", "[CHA]PÉU", "FLE[CHA]"]),
    ("QU / GU", ["QUE", "QUI", "GUE", "GUI"], ["[QUE]IJO", "PA[QUE]", "[QUI]ABO", "MOS[QUI]TO", "FO[GUE]IRA", "[GUI]TARRA", "MAN[GUE]IRA", "PRE[GUI]ÇA"]),
    ("RR", ["RRA", "RRE", "RRI", "RRO", "RRU"], ["CA[RRO]", "TE[RRA]", "BA[RRI]GA", "CA[RRO]ÇA", "GA[RRA]FA", "SE[RRA]", "CA[RRI]NHO", "BU[RRO]"]),
    ("SS", ["SSA", "SSE", "SSI", "SSO", "SSU"], ["PÁ[SSA]RO", "O[SSO]", "MA[SSA]", "PE[SSO]A", "A[SSO]VIO", "VA[SSO]URA", "TO[SSE]", "ASSA[SSI]NO"][:7] + ["PA[SSE]IO"]),
    ("Ç", ["ÇA", "ÇO", "ÇU"], ["PRA[ÇA]", "PA[ÇO]CA", "CABE[ÇA]", "LOU[ÇA]", "LEN[ÇO]", "CAL[ÇA]", "PO[ÇO]", "CORA[ÇÃO]"]),
    ("BR / CR / DR", ["BRA", "BRI", "BRU", "CRA", "CRE", "DRA"], ["[BRA]ÇO", "CA[BRA]", "[CRA]VO", "PE[DRA]", "[DRA]GÃO", "[BRI]NQUEDO", "[CRE]ME", "[BRU]XA"]),
    ("FR / GR / PR / TR", ["FRU", "GRA", "PRA", "PRE", "TRA", "TRI"], ["[FRU]TA", "[GRA]MA", "[PRA]TO", "[TRA]TOR", "[PRE]SENTE", "[TRI]GO", "[TRA]VESSEIRO", "[GRA]VATA"]),
    ("BL / CL / FL / PL", ["BLU", "BLO", "CLA", "FLA", "FLO", "PLA"], ["[BLU]SA", "[PLA]CA", "[FLO]R", "[PLA]NTA", "[CLA]RO", "[FLA]UTA", "[CLA]RA", "[BLO]CO"]),
    ("R no fim da sílaba", ["AR", "ER", "IR", "OR", "UR"], ["[MAR]", "[POR]TA", "[CAR]TA", "[BOR]BOLETA", "[TAR]TARUGA", "[COR]DA", "[BAR]CO", "[TER]RA"][:7] + ["[FOR]MIGA"]),
    ("S no fim da sílaba", ["AS", "ES", "IS", "OS", "US"], ["[ES]COLA", "[POS]TE", "[CAS]CA", "[PAS]TEL", "[VES]TIDO", "[LIS]TA", "[CES]TA", "[MOS]CA"]),
    ("Sons nasais (M e N)", ["AN", "EN", "IN", "ON", "UN"], ["[BAN]CO", "[DEN]TE", "[PIN]TO", "[ON]DA", "[MUN]DO", "[CAM]PO", "[POM]BA", "[TAM]BOR"]),
    ("ÃO / ÕES", ["ÃO", "ÃE", "ÕE"], ["[MÃO]", "[PÃO]", "LI[MÃO]", "LE[ÃO]", "BA[LÃO]", "MA[MÃE]", "FO[GÃO]", "CA[MINHÃO]"]),
]
FRASES = [
    ["O GATO BEBE LEITE.", "A BOLA É AZUL.", "O SAPO PULA.", "A VACA DÁ LEITE.", "O PATO NADA NO LAGO."],
    ["A FADA TEM UMA VARINHA.", "O MENINO COME BOLO.", "A LUA ESTÁ NO CÉU.", "O RATO FOI PARA A TOCA.", "A VOVÓ FEZ SUCO."],
    ["O CACHORRO CORRE NO QUINTAL.", "A GALINHA BOTOU UM OVO.", "EU GOSTO DE BRINCAR DE BOLA.", "O PALHAÇO É ENGRAÇADO.", "A CHUVA MOLHOU O CHÃO."],
    ["MAMÃE FEZ PÃO DE QUEIJO.", "O PÁSSARO CANTA NA JANELA.", "A ZEBRA TEM LISTRAS.", "O BEBÊ DORME NO BERÇO.", "O PEIXE VIVE NA ÁGUA."],
    ["A BORBOLETA POUSOU NA FLOR.", "O TREM PASSOU BEM DEVAGAR.", "EU LAVEI AS MÃOS ANTES DO ALMOÇO.", "O LEÃO É O REI DA FLORESTA.", "A TARTARUGA ANDA DEVAGAR."],
    ["MEU IRMÃO GANHOU UMA BICICLETA.", "A PROFESSORA LEU UMA HISTÓRIA.", "O SOL ESQUENTA A PRAIA.", "O CAMINHÃO LEVOU AS FRUTAS.", "A FORMIGA CARREGA UMA FOLHA."],
]
TEXTOS = [
    ("O GATO MIMI", "MIMI É UMA GATA. ELA É BRANCA E PELUDA. MIMI GOSTA DE LEITE E DE DORMIR NO SOFÁ. DE NOITE, ELA OLHA A LUA PELA JANELA.",
     ["COMO É A MIMI?", "DO QUE ELA GOSTA?", "O QUE ELA FAZ DE NOITE?"]),
    ("A BOLA DO TETÊ", "TETÊ TEM UMA BOLA AMARELA. ELE CHUTOU A BOLA E ELA CAIU NO LAGO. O PATO NADOU E EMPURROU A BOLA DE VOLTA. TETÊ RIU MUITO.",
     ["DE QUE COR É A BOLA?", "ONDE A BOLA CAIU?", "QUEM AJUDOU O TETÊ?"]),
    ("O PIQUENIQUE", "NO DOMINGO, A FAMÍLIA FOI AO PARQUE. LEVARAM SUCO, PÃO E FRUTAS. A FORMIGA TAMBÉM QUIS COMER! TODOS DERAM RISADA.",
     ["QUANDO FOI O PASSEIO?", "O QUE ELES LEVARAM?", "QUEM TAMBÉM QUIS COMER?"]),
    ("A CHUVA", "O CÉU FICOU ESCURO E COMEÇOU A CHOVER. LUÍSA PEGOU O GUARDA-CHUVA E A BOTA. ELA PULOU NAS POÇAS E VOLTOU TODA MOLHADA.",
     ["COMO FICOU O CÉU?", "O QUE LUÍSA PEGOU?", "COMO ELA VOLTOU PARA CASA?"]),
    ("O DENTE DE LEITE", "O DENTE DO BETO ESTAVA MOLE. NA HORA DO ALMOÇO, ELE CAIU! BETO GUARDOU O DENTE NUMA CAIXINHA E MOSTROU PARA A VOVÓ.",
     ["COMO ESTAVA O DENTE?", "QUANDO O DENTE CAIU?", "PARA QUEM BETO MOSTROU?"]),
    ("A HORTA DA ESCOLA", "A TURMA PLANTOU SEMENTES NA HORTA. TODO DIA ELES REGAVAM A TERRA. UM MÊS DEPOIS, NASCERAM ALFACE, CENOURA E TOMATE.",
     ["O QUE A TURMA PLANTOU?", "O QUE ELES FAZIAM TODO DIA?", "O QUE NASCEU NA HORTA?"]),
]


def limpa(p): return p.replace("[", "").replace("]", "")


def ascii_up(s): return "".join(ch for ch in unicodedata.normalize("NFD", s.upper()) if unicodedata.category(ch) != "Mn")


def texto(c, s, x, y, fonte="Nunito", tam=12, larg=None, cor=black, lead=None, centro=False):
    c.setFont(fonte, tam); c.setFillColor(cor)
    linhas = simpleSplit(s, fonte, tam, larg) if larg else [s]
    lead = lead or tam * 1.35
    for l in linhas:
        (c.drawCentredString if centro else c.drawString)(x, y, l)
        y -= lead
    return y


def cab(c, ap, k, tot, nome, instr):
    cor = CORES[ap]
    c.setFillColor(cor); c.rect(0, H - 54, W, 54, stroke=0, fill=1)
    c.setFillColor(white); c.setFont("Baloo", 13)
    c.drawString(M, H - 34, ["Apostila 1 · Sílabas simples", "Apostila 2 · Sílabas complexas", "Apostila 3 · Frases e fluência"][ap])
    c.setFont("Nunito", 10); c.drawRightString(W - M, H - 34, "Ficha %d de %d" % (k, tot))
    c.setFillColor(cor); c.setFont("Baloo", 26); c.drawString(M, H - 94, nome)
    y = texto(c, instr, M, H - 118, tam=12.5, larg=W - 2 * M, lead=17)
    c.setFont("Nunito", 10); c.setFillColor(CINZA)
    c.drawString(M, 30, "Nome: ________________________   Data: ___/___")
    c.drawRightString(W - M, 30, MARCA)
    return y - 8


def caixa_letras(c, x, y, n, cel=30):
    c.setStrokeColor(black); c.setLineWidth(1.2)
    for i in range(n): c.rect(x + i * cel, y, cel - 4, cel + 6)


# ---------- fichas por família ----------
def f_leia(c, ap, k, tot, fam, sil, pal, rnd, complexa):
    y = cab(c, ap, k, tot, ("Sílabas com %s" if complexa else "Família do %s") % fam, "Leia as sílabas em voz alta, apontando com o dedo. Depois leia as palavras e circule a sílaba da família em cada uma.")
    cel = (W - 2 * M) / len(sil)
    for i, s in enumerate(sil):
        c.setFillColor(HexColor("#FFF4D6")); c.setStrokeColor(CORES[ap]); c.setLineWidth(2)
        c.roundRect(M + i * cel + 6, y - 100, cel - 12, 88, 14, fill=1)
        c.setFillColor(black); c.setFont("Baloo", 40 if len(s) < 4 else 32); c.drawCentredString(M + i * cel + cel / 2, y - 70, s)
        c.setFont("Nunito", 15); c.setFillColor(CINZA); c.drawCentredString(M + i * cel + cel / 2, y - 125, s.lower())
    yy = y - 175
    for i, p in enumerate(pal):
        x = M + (i % 2) * (W - 2 * M) / 2
        c.setFont("Baloo", 28); c.setFillColor(black); c.drawString(x + 10, yy - (i // 2) * 72, limpa(p))
        c.setFont("Nunito", 15); c.setFillColor(CINZA); c.drawString(x + 10, yy - (i // 2) * 72 - 22, limpa(p).lower())
    texto(c, "Leia de novo, agora mais rápido. Quantas palavras você leu sem ajuda? ______ de %d" % len(pal), M, 80, tam=12, larg=W - 2 * M, cor=CINZA)


def f_complete(c, ap, k, tot, fam, sil, pal, rnd, complexa):
    y = cab(c, ap, k, tot, "Complete a palavra", "Escolha no quadro a sílaba que falta e escreva no espaço. Depois leia a palavra inteira em voz alta.")
    c.setFillColor(HexColor("#FFF4D6")); c.setStrokeColor(AMAR); c.setLineWidth(2); c.roundRect(M, y - 60, W - 2 * M, 50, 12, fill=1)
    for i, s in enumerate(sil):
        c.setFont("Baloo", 24); c.setFillColor(black); c.drawCentredString(M + (W - 2 * M) * (i + .5) / len(sil), y - 44, s)
    yy = y - 110; resp = []
    for p in pal[:7]:
        if "[" in p:
            a, resto = p.split("["); alvo, b = resto.split("]")
        else:
            alvo = next((s for s in sorted(sil, key=len, reverse=True) if p.startswith(s)), p[:2]); a, b = "", p[len(alvo):]
        resp.append(limpa(p))
        c.setFont("Baloo", 30); c.setFillColor(black)
        x = M + 20; c.drawString(x, yy, a); x += pdfmetrics.stringWidth(a, "Baloo", 30) + 6
        c.setStrokeColor(black); c.setLineWidth(1.6); c.line(x, yy - 4, x + 80, yy - 4); x += 86
        c.drawString(x, yy, b)
        yy -= 72
    return resp


def f_ligue(c, ap, k, tot, fam, sil, pal, rnd, complexa):
    y = cab(c, ap, k, tot, "Ligue e escreva", "Ligue cada palavra à sílaba que aparece nela. Depois copie duas palavras com letra de mão nas linhas abaixo.")
    ps = pal[:5]; ss = []
    for p in ps:
        if "[" in p: ss.append(p.split("[")[1].split("]")[0])
        else: ss.append(next((s for s in sorted(sil, key=len, reverse=True) if p.startswith(s)), p[:2]))
    dir_ = ss[:]; rnd.shuffle(dir_)
    yy = y - 30
    for i, p in enumerate(ps):
        c.setFont("Baloo", 26); c.setFillColor(black); c.drawString(M + 10, yy - 10, limpa(p))
        c.circle(M + 230, yy - 2, 4, fill=1)
        c.setStrokeColor(CORES[ap]); c.setLineWidth(1.6); c.roundRect(W - M - 110, yy - 22, 100, 44, 10)
        c.drawCentredString(W - M - 60, yy - 10, dir_[i]); c.circle(W - M - 124, yy - 2, 4, fill=1)
        yy -= 66
    yy -= 10
    for i in range(4):
        c.setStrokeColor(black); c.setLineWidth(1); c.line(M, yy - i * 42, W - M, yy - i * 42)
        c.setStrokeColor(CLARO); c.setDash(3, 4); c.line(M, yy - i * 42 + 16, W - M, yy - i * 42 + 16); c.setDash()


def f_caca(c, ap, k, tot, fam, sil, pal, rnd, complexa):
    y = cab(c, ap, k, tot, "Caça-palavras da família", "Encontre as palavras no quadro. Elas estão deitadas (da esquerda para a direita) e em pé (de cima para baixo). Pinte cada palavra que achar.")
    n = 10; g = [[None] * n for _ in range(n)]
    pal_ = [ascii_up(limpa(p)) for p in pal if len(limpa(p)) <= 9][:6]
    for p in sorted(pal_, key=len, reverse=True):
        for _ in range(500):
            dx, dy = rnd.choice([(1, 0), (0, 1)])
            x0 = rnd.randrange(0, n - (len(p) - 1) * dx); y0 = rnd.randrange(0, n - (len(p) - 1) * dy)
            if all(g[y0 + i * dy][x0 + i * dx] in (None, ch) for i, ch in enumerate(p)):
                for i, ch in enumerate(p): g[y0 + i * dy][x0 + i * dx] = ch
                break
    cel = 40; x0 = (W - n * cel) / 2; top = y - 10
    for r in range(n):
        for q in range(n):
            c.setStrokeColor(CLARO); c.setLineWidth(.7); c.rect(x0 + q * cel, top - (r + 1) * cel, cel, cel)
            c.setFont("Baloo", 20); c.setFillColor(black); c.drawCentredString(x0 + q * cel + cel / 2, top - (r + 1) * cel + 12, g[r][q] or rnd.choice("ABCDEFGILMNOPRSTUV"))
    yy = top - n * cel - 34
    for i, p in enumerate(pal_):
        c.setFont("Baloo", 16); c.setFillColor(black); c.drawString(M + (i % 3) * 170, yy - (i // 3) * 26, "□  " + p)


def f_forme(c, ap, k, tot, fam, sil, pal, rnd, complexa):
    y = cab(c, ap, k, tot, "Separe e conte", "Leia cada palavra, bata uma palma para cada pedacinho (sílaba) e escreva quantas sílabas ela tem. Depois separe as sílabas nos quadradinhos.")
    yy = y - 30
    for p in pal[:6]:
        c.setFont("Baloo", 26); c.setFillColor(black); c.drawString(M + 10, yy - 8, limpa(p))
        c.setStrokeColor(black); c.setLineWidth(1.4); c.circle(M + 250, yy, 18)
        for i in range(4): c.rect(M + 290 + i * 54, yy - 18, 46, 38)
        yy -= 72


def f_ditado(c, ap, k, tot, fam, sil, pal, rnd, complexa):
    y = cab(c, ap, k, tot, "Ditado da família", "Um adulto dita uma palavra de cada vez (a lista está no rodapé, dobre a folha para a criança não ver). A criança escreve, depois confere sozinha.")
    for i in range(6):
        yy = y - 40 - i * 78
        c.setFont("Baloo", 18); c.setFillColor(CORES[ap]); c.drawString(M, yy, "%d." % (i + 1))
        c.setStrokeColor(black); c.setLineWidth(1); c.line(M + 30, yy - 4, W - M, yy - 4)
        c.setStrokeColor(CLARO); c.setDash(3, 4); c.line(M + 30, yy + 14, W - M, yy + 14); c.setDash()
    c.setStrokeColor(CLARO); c.setDash(6, 5); c.line(M - 20, 100, W - M + 20, 100); c.setDash()
    c.setFont("Nunito", 11); c.setFillColor(CINZA); c.drawString(M, 82, "Para o adulto (dobre aqui): " + ", ".join(limpa(p) for p in pal[:6]))


# ---------- apostila 3 ----------
def f_frases(c, k, tot, lista, nivel):
    y = cab(c, 2, k, tot, "Leia as frases (nível %d)" % nivel, "Leia cada frase 3 vezes. A cada leitura, pinte uma estrela. Na terceira vez, tente ler sem parar no meio.")
    yy = y - 30
    for f in lista:
        yy = texto(c, f, M, yy, fonte="Baloo", tam=26, larg=W - 2 * M - 110, lead=32)
        for i in range(3):
            from math import cos, sin, radians
            cx, cy = W - M - 90 + i * 32, yy + 32
            pts = [(cx + (12 if j % 2 == 0 else 5) * cos(radians(90 + j * 36)), cy + (12 if j % 2 == 0 else 5) * sin(radians(90 + j * 36))) for j in range(10)]
            p = c.beginPath(); p.moveTo(*pts[0]); [p.lineTo(*q) for q in pts[1:]]; p.close()
            c.setStrokeColor(black); c.setLineWidth(1.2); c.drawPath(p, stroke=1, fill=0)
        c.setFont("Nunito", 14); c.setFillColor(CINZA); c.drawString(M, yy + 8, f.lower()[0].upper() + f.lower()[1:])
        yy -= 40


def f_ordene(c, k, tot, lista, nivel, rnd):
    y = cab(c, 2, k, tot, "Frase embaralhada", "As palavras de cada frase se misturaram. Leia, coloque em ordem e escreva a frase certa na linha.")
    yy = y - 34
    for f in lista:
        ws = f.rstrip(".").split(); emb = ws[:]
        for _ in range(10):
            rnd.shuffle(emb)
            if emb != ws: break
        x = M
        for w_ in emb:
            wd = pdfmetrics.stringWidth(w_, "Baloo", 18) + 18
            c.setStrokeColor(CORES[2]); c.setLineWidth(1.3); c.roundRect(x, yy - 8, wd, 30, 8)
            c.setFont("Baloo", 18); c.setFillColor(black); c.drawString(x + 9, yy, w_); x += wd + 8
        c.setStrokeColor(black); c.setLineWidth(1); c.line(M, yy - 40, W - M, yy - 40)
        yy -= 92


def f_texto(c, k, tot, t):
    tit, corpo, perg = t
    y = cab(c, 2, k, tot, tit, "Leia o texto com um adulto. Depois leia sozinho. Responda às perguntas e marque quanto tempo levou para ler.")
    c.setFillColor(HexColor("#F4ECFB")); c.setStrokeColor(CORES[2]); c.setLineWidth(2)
    hh = len(simpleSplit(corpo, "Baloo", 21, W - 2 * M - 40)) * 30 + 30
    c.roundRect(M, y - 10 - hh, W - 2 * M, hh, 14, fill=1)
    texto(c, corpo, M + 20, y - 40, fonte="Baloo", tam=21, larg=W - 2 * M - 40, lead=30)
    yy = y - 50 - hh
    for p in perg:
        c.setFont("Baloo", 17); c.setFillColor(black); c.drawString(M, yy, p)
        c.setStrokeColor(black); c.setLineWidth(1); c.line(M, yy - 32, W - M, yy - 32)
        yy -= 72
    c.setFont("Nunito", 12); c.setFillColor(CINZA)
    c.drawString(M, 76, "1ª leitura: ____ min   2ª leitura: ____ min   3ª leitura: ____ min")


def capa(c, ap, titulo, sub):
    cor = CORES[ap]
    c.setFillColor(cor); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(white); c.setFont("Baloo", 22); c.drawCentredString(W / 2, H - 140, "LÊ COMIGO · KIT DE LEITURA EM CASA")
    c.setFont("Baloo", 30); c.drawCentredString(W / 2, H - 220, "APOSTILA %d" % (ap + 1))
    texto(c, titulo, W / 2, H - 300, fonte="Baloo", tam=50, larg=W - 100, cor=white, lead=56, centro=True)
    texto(c, sub, W / 2, 300, tam=16, larg=W - 140, cor=white, centro=True, lead=22)
    c.setFont("Nunito", 11); c.drawCentredString(W / 2, 60, "Uso pessoal, familiar e em sala de aula. Proibida a revenda.")
    c.showPage()


def como_usar(c, ap, linhas):
    c.setFillColor(CORES[ap]); c.setFont("Baloo", 28); c.drawString(M, H - 80, "Como usar")
    y = H - 118
    for s in linhas: y = texto(c, "•  " + s, M, y, tam=13.5, larg=W - 2 * M, lead=20) - 10
    c.showPage()


GERAL = ["Uma ficha por dia, 10 a 15 minutos, sentados juntos. Leitura é treino: pouco e todo dia.",
         "Sempre leia em voz alta. Aponte com o dedo embaixo da sílaba ou da palavra que está lendo.",
         "Se a criança travar, leia junto e peça para ela repetir. Elogie a tentativa, não só o acerto.",
         "Imprima em papel A4 comum, em preto e branco."]


def apostila(pasta, ap, titulo, sub, familias, complexa):
    nome = "Le Comigo - Apostila %d - %s.pdf" % (ap + 1, titulo)
    c = canvas.Canvas(os.path.join(pasta, nome), pagesize=A4); c.setTitle("Lê Comigo · Apostila %d · %s" % (ap + 1, titulo)); c.setAuthor(MARCA)
    capa(c, ap, titulo, sub)
    como_usar(c, ap, ["Siga a ordem das famílias. Cada família tem 6 fichas: leia, complete, ligue, caça-palavras, separe e ditado."] + GERAL)
    fichas = [f_leia, f_complete, f_ligue, f_caca, f_forme, f_ditado]
    tot = len(familias) * len(fichas); k = 0
    for fi, (fam, sil, pal) in enumerate(familias):
        for j, f in enumerate(fichas):
            k += 1; f(c, ap, k, tot, fam, sil, pal, random.Random(ap * 1000 + fi * 10 + j), complexa); c.showPage()
    c.save(); return nome, k


def apostila3(pasta):
    nome = "Le Comigo - Apostila 3 - Frases e fluencia.pdf"
    c = canvas.Canvas(os.path.join(pasta, nome), pagesize=A4); c.setTitle("Lê Comigo · Apostila 3 · Frases e fluência"); c.setAuthor(MARCA)
    capa(c, 2, "Frases e fluência", "Da palavra à frase e ao primeiro texto: frases progressivas, frases embaralhadas e textos curtos com perguntas.")
    como_usar(c, 2, ["Comece pelas frases do nível 1. Passe para o próximo nível quando a criança ler as frases sem parar no meio."] + GERAL)
    k = 0; tot = len(FRASES) * 2 + len(TEXTOS)
    for i, lst in enumerate(FRASES):
        k += 1; f_frases(c, k, tot, lst, i + 1); c.showPage()
        k += 1; f_ordene(c, k, tot, lst, i + 1, random.Random(i)); c.showPage()
    for t in TEXTOS:
        k += 1; f_texto(c, k, tot, t); c.showPage()
    c.save(); return nome, k


if __name__ == "__main__":
    pasta = os.path.join(RAIZ, "out", "pdf-leitura"); os.makedirs(pasta, exist_ok=True)
    print(apostila(pasta, 0, "Sílabas simples", "16 famílias silábicas, do B ao Z: leitura, complete, ligue, caça-palavras, separação de sílabas e ditado.", SIMPLES, False))
    print(apostila(pasta, 1, "Sílabas complexas", "NH, LH, CH, QU, GU, RR, SS, Ç, encontros consonantais, sílabas com R, S, M e N no fim, e ÃO.", COMPLEXAS, True))
    print(apostila3(pasta))
