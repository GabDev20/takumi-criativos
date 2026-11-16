# -*- coding: utf-8 -*-
"""Order bumps: Rotina Visual (Trilha do Foco) e Fichas Relâmpago (Lê Comigo)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white
from gerar_foco import W, H, M, texto, forma, CINZA, CLARO, AMAR, ETAPAS
from gerar_leitura import SIMPLES, COMPLEXAS, limpa, CORES

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AZUL = HexColor("#123B7A")

ROTINA = {
    "Manhã": ["Acordar", "Ir ao banheiro", "Lavar o rosto", "Escovar os dentes", "Trocar de roupa", "Tomar café", "Arrumar a mochila", "Calçar o sapato"],
    "Tarde": ["Almoçar", "Descansar", "Fazer a lição", "Lanchar", "Brincar", "Guardar os brinquedos", "Tomar banho", "Ajudar em casa"],
    "Noite": ["Jantar", "Escovar os dentes", "Vestir o pijama", "Separar a roupa de amanhã", "Ler uma história", "Ir ao banheiro", "Deitar", "Dormir"],
}


def titulo(c, t, sub, cor=AZUL):
    c.setFillColor(cor); c.rect(0, H - 90, W, 90, stroke=0, fill=1)
    c.setFillColor(white); c.setFont("Baloo", 30); c.drawString(M, H - 52, t)
    texto(c, sub, M, H - 72, tam=10.5, larg=W - 2 * M, cor=white, lead=13)


def rotina(pasta):
    nome = "Trilha do Foco - BONUS Rotina Visual e Quadro de Combinados.pdf"
    c = canvas.Canvas(os.path.join(pasta, nome)); c.setTitle("Rotina Visual e Quadro de Combinados")
    c.setFillColor(AZUL); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(AMAR); c.setFont("Baloo", 20); c.drawCentredString(W / 2, H - 200, "TRILHA DO FOCO · MATERIAL EXTRA")
    texto(c, "Rotina Visual e Quadro de Combinados", W / 2, H - 290, fonte="Baloo", tam=46, larg=W - 100, cor=white, centro=True, lead=52)
    texto(c, "Cartões de rotina para recortar, quadros da semana, quadro de estrelas e termômetro da calma.", W / 2, 260, tam=15, larg=W - 140, cor=white, centro=True, lead=21)
    c.showPage()
    # cartões
    for per, itens in ROTINA.items():
        titulo(c, "Cartões da rotina · " + per, "Recorte, cole na parede na ordem do dia e vire o cartão quando a tarefa estiver feita.")
        cw, ch = (W - 2 * M) / 2, 170
        for i, it in enumerate(itens):
            x = M + (i % 2) * cw; y = H - 120 - (i // 2) * ch
            c.setStrokeColor(CLARO); c.setDash(5, 4); c.rect(x + 6, y - ch + 12, cw - 12, ch - 12); c.setDash()
            c.setFillColor(HexColor("#EAF1FC")); c.circle(x + 60, y - ch / 2 + 6, 36, fill=1, stroke=0)
            c.setFillColor(AZUL); c.setFont("Baloo", 30); c.drawCentredString(x + 60, y - ch / 2 - 4, str(i + 1))
            texto(c, it, x + 112, y - ch / 2 + 10, fonte="Baloo", tam=22, larg=cw - 130, lead=26)
            c.setStrokeColor(black); c.setLineWidth(1.4); c.rect(x + cw - 44, y - ch + 28, 22, 22)
        c.showPage()
    # quadro semanal
    for per, itens in ROTINA.items():
        titulo(c, "Minha semana · " + per, "Marque um X (ou cole uma estrelinha) a cada tarefa feita. No domingo, conte as estrelas!")
        dias = ["SEG", "TER", "QUA", "QUI", "SEX", "SÁB", "DOM"]
        x0, cw = M + 170, (W - 2 * M - 170) / 7; y = H - 130
        for j, d in enumerate(dias):
            c.setFont("Baloo", 14); c.setFillColor(AZUL); c.drawCentredString(x0 + j * cw + cw / 2, y, d)
        for i, it in enumerate(itens):
            yy = y - 20 - i * 62
            c.setFont("Baloo", 15); c.setFillColor(black); c.drawString(M, yy - 36, it)
            for j in range(7):
                c.setStrokeColor(CLARO); c.setLineWidth(1); c.rect(x0 + j * cw + 4, yy - 54, cw - 8, 54)
        c.showPage()
    # quadro de estrelas
    titulo(c, "Quadro de estrelas", "Combine 3 metas com a criança. Cada vez que cumprir, pinte uma estrela. 20 estrelas = um prêmio combinado.")
    y = H - 150
    for m in range(3):
        c.setFont("Baloo", 18); c.setFillColor(AZUL); c.drawString(M, y, "Meta %d: _______________________________" % (m + 1))
        for i in range(20): forma(c, "estrela", M + 18 + (i % 10) * 50, y - 45 - (i // 10) * 50, 18)
        y -= 175
    c.setFont("Baloo", 18); c.setFillColor(black); c.drawString(M, 80, "Prêmio combinado: ________________________________")
    c.showPage()
    # termômetro
    titulo(c, "Termômetro da calma", "Quando a criança estiver agitada, ela aponta onde está e escolhe uma estratégia para descer um nível.", HexColor("#C0392B"))
    niveis = [("5", "Explodindo", HexColor("#C0392B")), ("4", "Muito bravo", HexColor("#E67E22")), ("3", "Agitado", AMAR), ("2", "Um pouco inquieto", HexColor("#16A085")), ("1", "Calmo", HexColor("#2E6FD8"))]
    for i, (n, t, cor) in enumerate(niveis):
        y = H - 200 - i * 100
        c.setFillColor(cor); c.roundRect(M, y - 30, 90, 80, 14, fill=1, stroke=0)
        c.setFillColor(white); c.setFont("Baloo", 40); c.drawCentredString(M + 45, y - 4, n)
        c.setFillColor(black); c.setFont("Baloo", 22); c.drawString(M + 110, y + 10, t)
    c.setFont("Baloo", 16); c.setFillColor(black); c.drawString(M, 160, "Para descer um nível:")
    texto(c, "respirar fundo 5 vezes  ·  contar até 10  ·  beber água  ·  abraçar um travesseiro  ·  ir para o cantinho da calma  ·  desenhar o que sente", M, 136, tam=13, larg=W - 2 * M, lead=19)
    c.showPage()
    # combinados
    titulo(c, "Nossos combinados", "Escrevam juntos até 6 combinados da casa. Frases curtas, no positivo: \"falamos baixo\" em vez de \"não grite\".")
    for i in range(6):
        y = H - 160 - i * 100
        c.setFillColor(HexColor("#EAF1FC")); c.roundRect(M, y - 50, W - 2 * M, 80, 14, fill=1, stroke=0)
        c.setFillColor(AZUL); c.setFont("Baloo", 26); c.drawString(M + 20, y - 18, "%d." % (i + 1))
        c.setStrokeColor(CLARO); c.line(M + 60, y - 22, W - M - 20, y - 22)
    c.setFont("Nunito", 12); c.setFillColor(CINZA); c.drawString(M, 60, "Assinaturas: ______________________   ______________________")
    c.showPage(); c.save(); return nome


def fichas(pasta):
    nome = "Le Comigo - BONUS Fichas Relampago.pdf"
    c = canvas.Canvas(os.path.join(pasta, nome)); c.setTitle("Fichas Relâmpago · Lê Comigo")
    c.setFillColor(CORES[0]); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(white); c.setFont("Baloo", 20); c.drawCentredString(W / 2, H - 200, "LÊ COMIGO · MATERIAL EXTRA")
    texto(c, "Fichas Relâmpago: 240 palavras para recortar", W / 2, H - 290, fonte="Baloo", tam=44, larg=W - 100, cor=white, centro=True, lead=50)
    texto(c, "Jogo rápido de leitura: recorte, embaralhe e veja quantas palavras a criança lê em 1 minuto. Anote o recorde!", W / 2, 260, tam=15, larg=W - 140, cor=white, centro=True, lead=21)
    c.showPage()
    todas = [(f, limpa(p)) for f, _, ps in SIMPLES + COMPLEXAS for p in ps]
    cw, ch = (W - 2 * M) / 3, (H - 2 * M - 30) / 6
    for pg in range(0, len(todas), 18):
        c.setFont("Nunito", 10); c.setFillColor(CINZA); c.drawString(M, H - 34, "Fichas Relâmpago · recorte na linha pontilhada")
        for i, (f, p) in enumerate(todas[pg:pg + 18]):
            x = M + (i % 3) * cw; y = H - M - 10 - (i // 3) * ch
            c.setStrokeColor(CLARO); c.setDash(5, 4); c.rect(x, y - ch, cw, ch); c.setDash()
            c.setFont("Baloo", 30 if len(p) < 9 else 22); c.setFillColor(black); c.drawCentredString(x + cw / 2, y - ch / 2 - 8, p)
            c.setFont("Nunito", 9); c.setFillColor(CINZA); c.drawCentredString(x + cw / 2, y - ch + 10, f)
        c.showPage()
    # recordes
    c.setFillColor(CORES[0]); c.setFont("Baloo", 28); c.drawString(M, H - 80, "Meus recordes")
    for i in range(12):
        y = H - 130 - i * 52
        c.setFont("Baloo", 16); c.setFillColor(black); c.drawString(M, y, "Dia ___/___    Li ______ palavras em 1 minuto")
        for j in range(3): forma(c, "estrela", W - M - 80 + j * 30, y + 6, 11)
    c.showPage(); c.save(); return nome, len(todas)


if __name__ == "__main__":
    print(rotina(os.path.join(RAIZ, "out", "pdf")))
    print(fichas(os.path.join(RAIZ, "out", "pdf-leitura")))
