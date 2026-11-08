import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from video import B, N, star, NAVY, GOLD, WHITE, RED, text_c, shadow_paste, page
from PIL import Image, ImageDraw
ROOT = pathlib.Path(__file__).resolve().parent.parent; O = ROOT / "out/facebook"
def stars(d, w, h, pts):
    for x, y, r in pts: star(d, x * w, y * h, r, GOLD)
# perfil
im = Image.new("RGB", (1080, 1080), NAVY); d = ImageDraw.Draw(im)
star(d, 540, 470, 300, GOLD); stars(d, 1080, 1080, [(.2, .25, 18), (.8, .22, 14), (.78, .78, 16), (.24, .74, 12)])
f = B(92); d.text((540, 830), "Estrela Guia", font=f, fill=WHITE, anchor="ma"); d.text((540, 920), "KIDS", font=B(64), fill=GOLD, anchor="ma")
im.save(O / "foto-de-perfil-1080.png")
# capa
W, H = 1640, 624; im = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(im)
stars(d, W, H, [(.05, .15, 12), (.4, .1, 9), (.55, .85, 11), (.95, .12, 10), (.08, .88, 8)])
m = Image.open(ROOT / "out/img/mockup.png").convert("RGBA"); m = m.resize((760, int(m.height * 760 / m.width))); im.paste(m, (860, 40), m)
d.text((420, 170), "Material pronto para o", font=B(56), fill=WHITE, anchor="ma")
d.text((420, 240), "ministério infantil", font=B(86), fill=GOLD, anchor="ma")
d.text((420, 370), "Aulas, atividades por idade e teatro", font=N(36), fill=WHITE, anchor="ma")
d.text((420, 420), "É só imprimir e dar aula", font=N(36), fill=WHITE, anchor="ma")
im.save(O / "capa-facebook-1640x624.png")
# posts de prévia 1080x1350
for fn, n, l1, l2 in [("post-4-colorir", 7, "Veja por dentro:", "atividade de colorir para 3 a 5 anos"),
                      ("post-5-teatro", 32, "Teatro de Natal pronto", "papel para todas as crianças"),
                      ("post-6-lembrancinha", 34, "Lembrancinha do culto", "“Jesus é o melhor presente”")]:
    im = Image.new("RGB", (1080, 1350), NAVY); d = ImageDraw.Draw(im)
    y = text_c(d, 70, l1, B(78), WHITE); text_c(d, y, l2, B(56), GOLD)
    shadow_paste(im, page(n, 700), 540, 830)
    im.save(O / f"{fn}.png")
print("ok")
