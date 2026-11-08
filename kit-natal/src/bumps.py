import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from video import B, N, star, GOLD, WHITE, text_c
from PIL import Image, ImageDraw, ImageFilter
R = pathlib.Path(__file__).resolve().parent.parent; P = R / "out/video/pg"; O = R / "out"
def card(n, w, rot):
    im = Image.open(P / f"{n}.png").convert("RGB"); im = im.resize((w, int(im.height * w / im.width)))
    ImageDraw.Draw(im).rectangle([0, 0, w - 1, im.height - 1], outline=GOLD, width=5)
    pad = 30; c = Image.new("RGBA", (w + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", c.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle([pad, pad + 12, pad + w, pad + im.height + 12], fill=(0, 0, 0, 110))
    c = Image.alpha_composite(c, sh.filter(ImageFilter.GaussianBlur(14))); c.paste(im, (pad, pad))
    return c.rotate(rot, expand=True, resample=Image.BICUBIC)
for fn, bgc, pages, l1, l2 in [("bump-janeiro-pronto", (46, 94, 78), ["j4", "j30", "j1"], "Janeiro Pronto", "+4 aulas para começar o ano"),
                               ("bump-certificados-convites", (142, 42, 42), ["c2", "c3", "c1"], "Certificados e Convites", "para o Natal das crianças")]:
    im = Image.new("RGBA", (1080, 1080), bgc + (255,)); d = ImageDraw.Draw(im)
    for x, y, r in [(90, 90, 14), (990, 120, 10), (980, 980, 14), (80, 1000, 9)]: star(d, x, y, r, GOLD)
    for (x, y, rot), n in zip([(60, 360, 8), (600, 360, -8), (300, 290, 0)], pages):
        c = card(n, 400, rot); im.alpha_composite(c, (x, y))
    d = ImageDraw.Draw(im)
    y = text_c(d, 40, l1, B(84), WHITE); text_c(d, y + 4, l2, B(50), GOLD)
    im.convert("RGB").save(O / f"{fn}.png")
print("ok")
