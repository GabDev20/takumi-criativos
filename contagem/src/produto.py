# Produto: "Desafio Contagem Regressiva - 21 treinos de 15 minutos" (PDF) + capa 300x250 e 1080x1080.
# Treinos só com peso do corpo, cada exercício com versão leve e versão puxada. Sem promessa de resultado.
# Uso: python3 src/produto.py -> out/produto/*.pdf, *.png
import pathlib, asyncio
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "out/produto"; OUT.mkdir(parents=True, exist_ok=True)

EX = {  # nome: (como fazer, versão leve, versão puxada)
 "Agachamento": ("Pés na largura do quadril, desça como se fosse sentar numa cadeira, peito aberto.", "Sente e levante de uma cadeira de verdade.", "Desça devagar em 3 segundos."),
 "Ponte de glúteo": ("Deitada, joelhos dobrados, eleve o quadril e aperte o glúteo em cima.", "Amplitude menor.", "Segure 2 segundos no alto."),
 "Prancha": ("Antebraços no chão, corpo em linha reta, umbigo para dentro.", "Joelhos apoiados.", "Toque o ombro com a mão oposta, alternando."),
 "Polichinelo sem salto": ("Abra um pé para o lado e suba os braços, alternando os lados.", "Só os braços acima da cabeça.", "Polichinelo normal com salto."),
 "Avanço alternado": ("Passo à frente, desça o joelho de trás perto do chão, volte e troque.", "Apoie a mão numa parede.", "Avanço para trás com joelho à frente."),
 "Flexão inclinada": ("Mãos num sofá ou mesa firme, desça o peito e empurre.", "Mãos na parede.", "Flexão com joelhos no chão."),
 "Perdigueiro (bird-dog)": ("Quatro apoios, estenda braço e perna opostos, volte devagar.", "Só a perna.", "Toque cotovelo no joelho entre as repetições."),
 "Escalador lento": ("Posição de flexão, traga um joelho ao peito de cada vez, devagar.", "Mãos num sofá.", "Ritmo mais rápido."),
 "Elevação de panturrilha": ("Em pé, suba na ponta dos pés e desça devagar.", "Segurando numa parede.", "Uma perna de cada vez."),
 "Dead bug": ("Deitada, braços para cima, joelhos a 90°, estenda braço e perna opostos.", "Só as pernas, alternando.", "Movimento mais lento, 3 segundos."),
 "Agachamento sumô": ("Pés bem afastados e pontas para fora, desça com o tronco reto.", "Amplitude menor.", "Fique 2 segundos embaixo."),
 "Passada lateral": ("Passo largo para o lado, dobre o joelho daquele lado, volte.", "Passo curto.", "Pequeno salto lateral (skater)."),
 "Superman": ("Deitada de bruços, eleve braços e pernas um pouco do chão.", "Só os braços.", "Segure 3 segundos em cima."),
 "Abdominal curto": ("Deitada, joelhos dobrados, eleve só os ombros do chão.", "Mãos nas coxas guiando.", "Braços estendidos acima da cabeça."),
 "Corrida parada": ("Corra no lugar, braços acompanhando.", "Marcha no lugar.", "Joelho alto."),
}
FASES = [
 ("Fase 1 - Pegar o ritmo", "Dias 1 a 7", "40 s de exercício / 20 s de pausa, 2 voltas",
  [["Agachamento","Ponte de glúteo","Polichinelo sem salto","Prancha","Perdigueiro (bird-dog)"],
   ["Avanço alternado","Flexão inclinada","Corrida parada","Dead bug","Elevação de panturrilha"],
   ["Agachamento sumô","Superman","Passada lateral","Abdominal curto","Ponte de glúteo"]]),
 ("Fase 2 - Hábito automático", "Dias 8 a 14", "40 s / 20 s, 2 voltas, versão normal ou puxada",
  [["Agachamento","Escalador lento","Flexão inclinada","Ponte de glúteo","Prancha"],
   ["Avanço alternado","Polichinelo sem salto","Dead bug","Agachamento sumô","Superman"],
   ["Passada lateral","Corrida parada","Perdigueiro (bird-dog)","Abdominal curto","Elevação de panturrilha"]]),
 ("Fase 3 - Reta final", "Dias 15 a 21", "45 s / 15 s, 2 voltas",
  [["Agachamento sumô","Escalador lento","Avanço alternado","Prancha","Corrida parada"],
   ["Agachamento","Flexão inclinada","Passada lateral","Dead bug","Ponte de glúteo"],
   ["Polichinelo sem salto","Superman","Avanço alternado","Abdominal curto","Escalador lento"]]),
]

def treinos():
    out = []
    for fi, (fase, dias, prot, circ) in enumerate(FASES):
        for j in range(7):
            d = fi * 7 + j + 1
            if j == 6:
                out.append((d, fase, "Treino leve + mobilidade", "Ritmo confortável, 1 volta de cada", circ[0] + ["Corrida parada"], True))
            else:
                out.append((d, fase, f"Treino {chr(65 + j % 3)}", prot, circ[j % 3], False))
    return out

CSS = """
@page{size:A4;margin:0}*{margin:0;padding:0;box-sizing:border-box}
body{font:11.5pt/1.45 Inter,sans-serif;color:#17181C}
.pg{width:210mm;height:297mm;padding:18mm 16mm;position:relative;page-break-after:always;overflow:hidden}
h1,h2,h3{font-family:Montserrat,sans-serif;font-weight:900}
h2{font-size:24pt;margin-bottom:6mm}h3{font-size:13pt;margin:5mm 0 2mm}
.co{color:#FF5A36}.mu{color:#6B6660}
.cover{background:linear-gradient(160deg,#1d2440 0%,#3b2a4a 55%,#ff7a4d 130%);color:#fff;display:flex;flex-direction:column;justify-content:center;padding:24mm}
.cover .big{font:900 150pt/0.9 Montserrat;color:#F2B33D}.cover h1{font-size:34pt;line-height:1.05;margin-top:6mm}
.box{background:#FFF4E8;border-radius:5mm;padding:6mm;margin:4mm 0}
.cal{display:grid;grid-template-columns:repeat(7,1fr);gap:3mm;margin:6mm 0}.cal div{height:24mm;border:.6mm solid #EADFD2;border-radius:3mm;padding:2mm;font:900 14pt Montserrat}
.cal div small{display:block;font:600 7pt Inter;color:#6B6660;margin-top:8mm}
table{width:100%;border-collapse:collapse;margin-top:2mm}td,th{border-bottom:.3mm solid #EADFD2;padding:2mm 1.5mm;text-align:left;vertical-align:top;font-size:10pt}th{font:800 9pt Inter;color:#6B6660}
.day{display:flex;justify-content:space-between;align-items:baseline;border-top:1mm solid #FF5A36;padding-top:2mm;margin-top:5mm}
.day b{font:900 15pt Montserrat}.tag{font:700 8.5pt Inter;background:#17181C;color:#fff;padding:1mm 2.5mm;border-radius:2mm}
ul{margin-left:5mm}li{margin:1.2mm 0}
.foot{position:absolute;bottom:10mm;left:16mm;right:16mm;font-size:8pt;color:#6B6660;display:flex;justify-content:space-between}
"""

def html():
    T = treinos(); pages = []
    pages.append("""<div class="pg cover"><div class="big">21</div><h1>Desafio<br>Contagem Regressiva</h1>
      <p style="font-size:15pt;margin-top:6mm;opacity:.9">21 treinos de 15 minutos. Em casa, sem equipamento, até a sua data.</p></div>""")
    pages.append(f"""<div class="pg"><h2>Antes de começar</h2>
      <div class="box"><b>Como funciona.</b> São 21 treinos de 15 minutos divididos em 3 fases. Cada treino tem aquecimento (3 min), circuito (10 min) e alongamento (2 min). Você só precisa de 2 metros de espaço e um cronômetro.</div>
      <h3>A regra da contagem</h3><ul><li>Escreva a sua data no calendário da próxima página.</li><li>Faça o treino do dia, marque com um X. Perdeu um dia? Faça o próximo, sem compensar.</li><li>Cada exercício tem versão <b>leve</b> e <b>puxada</b>. Comece pela que conseguir fazer com boa postura.</li></ul>
      <h3>Faltam menos de 21 dias?</h3><table><tr><th>Dias até a data</th><th>O que fazer</th></tr>
      <tr><td>14 a 20</td><td>Pule os treinos leves de mobilidade (dias 7, 14 e 21) e siga a ordem.</td></tr>
      <tr><td>7 a 13</td><td>Faça a Fase 1 (dias 1 a 6) e depois os dias 15 a 17 da Fase 3.</td></tr>
      <tr><td>menos de 7</td><td>Faça os dias 1 a 6, um por dia. É a sua largada, continue depois da data.</td></tr>
      <tr><td>mais de 21</td><td>Repita a Fase 2 antes da Fase 3 até completar a contagem.</td></tr></table>
      <h3>Aquecimento (3 min, todos os dias)</h3><ul><li>30 s marcha no lugar · 30 s círculos de braço · 30 s rotação de quadril</li><li>30 s agachamento curto · 30 s alcance lateral · 30 s marcha com joelho alto</li></ul>
      <h3>Alongamento (2 min)</h3><ul><li>Posterior de coxa, quadríceps em pé, peitoral na parede e postura da criança, 30 s cada.</li></ul>
      <div class="box" style="margin-top:6mm"><b>Segurança.</b> Este plano é de condicionamento geral e não substitui orientação médica ou de um profissional de educação física. Se você tem alguma condição de saúde, está grávida, em pós-parto recente ou sente dor, converse com seu médico antes de começar. Pare se sentir tontura, falta de ar fora do normal ou dor.</div>
      <div class="foot"><span>Desafio Contagem Regressiva</span><span>2</span></div></div>""")
    cal = "".join(f'<div>{i}<small>{"DIA DA LARGADA" if i==1 else ("MINHA DATA" if i==21 else "")}</small></div>' for i in range(1, 22))
    pages.append(f"""<div class="pg"><h2>Meu calendário</h2><p>A minha data é: ____________________ &nbsp;&nbsp; Faltam ______ dias.</p><div class="cal">{cal}</div>
      <h3>Checklist da semana da data</h3><ul><li>Mantenha os treinos até a véspera, sem aumentar a intensidade.</li><li>Na véspera, faça o treino leve de mobilidade.</li><li>Durma bem nas 2 últimas noites e beba água ao longo do dia.</li><li>No dia: aproveite. Depois, recomece a contagem para a próxima data.</li></ul>
      <div class="foot"><span>Desafio Contagem Regressiva</span><span>3</span></div></div>""")
    # treinos: 2 por página
    pn = 4
    for i in range(0, 21, 2):
        blocos = ""
        for d, fase, nome, prot, exs, leve in T[i:i + 2]:
            rows = "".join(f"<tr><td><b>{e}</b><br><span class=mu>{EX[e][0]}</span></td><td>{EX[e][1]}</td><td>{EX[e][2]}</td></tr>" for e in exs)
            blocos += f"""<div class="day"><b>Dia {d} <span class="co">·</span> {nome}</b><span class="tag">{fase.split(' - ')[0]}</span></div>
              <p class="mu" style="margin:1mm 0">{prot}</p><table><tr><th style="width:52%">Exercício</th><th>Versão leve</th><th>Versão puxada</th></tr>{rows}</table>"""
        pages.append(f'<div class="pg">{blocos}<div class="foot"><span>Desafio Contagem Regressiva</span><span>{pn}</span></div></div>'); pn += 1
    pages.append(f"""<div class="pg"><h2>Você chegou.</h2><p style="font-size:14pt">21 treinos de 15 minutos são mais de 5 horas de treino que você não tinha antes. Escolha a próxima data e comece a contagem de novo, agora com a versão puxada.</p>
      <div class="box" style="margin-top:8mm">Dúvidas sobre o acesso ou reembolso: responda o e-mail de compra. Garantia de 7 dias pela plataforma de pagamento.</div>
      <div class="foot"><span>Desafio Contagem Regressiva</span><span>{pn}</span></div></div>""")
    return f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"

CAPA = """<html><head><meta charset=utf-8><style>*{margin:0;padding:0;box-sizing:border-box}
body{width:%dpx;height:%dpx;background:linear-gradient(160deg,#1d2440 0%%,#3b2a4a 55%%,#ff7a4d 130%%);color:#fff;font-family:Montserrat;display:flex;align-items:center;padding:0 %dpx;gap:%dpx;overflow:hidden}
.n{font:900 %dpx/0.85 Montserrat;color:#F2B33D}.t{font:900 %dpx/1.05 Montserrat}.s{font:700 %dpx Inter;opacity:.85;margin-top:%dpx;letter-spacing:.04em}</style></head>
<body><div class=n>21</div><div><div class=t>DESAFIO<br>CONTAGEM<br>REGRESSIVA</div><div class=s>15 MIN POR DIA · EM CASA</div></div></body></html>"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.set_content(html()); await pg.wait_for_timeout(500)
        await pg.pdf(path=str(OUT / "desafio-contagem-regressiva.pdf"), format="A4", print_background=True)
        for nome, w, h, sc in [("capa-300x250", 300, 250, 3), ("capa-1080", 1080, 1080, 1)]:
            k = w / 300
            pg2 = await b.new_page(viewport={"width": w, "height": h}, device_scale_factor=sc)
            await pg2.set_content(CAPA % (w, h, int(20*k), int(12*k), int(88*k), int(21*k), int(9*k), int(8*k))); await pg2.wait_for_timeout(300)
            await pg2.screenshot(path=str(OUT / f"{nome}.png"))
        await b.close()

asyncio.run(main())
