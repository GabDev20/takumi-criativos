# Vídeo v2 (teatro de Natal), 1080x1920. Uso: python3 video2.py "19,90"
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import video as V
from PIL import Image
PRECO = sys.argv[1] if len(sys.argv) > 1 else "19,90"
IMG = V.OUT / "img"; _c = {}
def page(n, w):
    k = (n, w)
    if k not in _c:
        im = Image.open(IMG / f"{n}.png").convert("RGB"); _c[k] = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    return _c[k]
V.page = page
S = [
    (2.6, V.hook("Pediram um teatro de Natal para as crianças?", "Já está escrito.")),
    (3.0, V.show("teatro", "8 a 10 minutos", top="O Presente Mais Esperado", focus=.05)),
    (2.6, V.show("teatro", "Papel para todas as crianças", top="De 3 a 11 anos", focus=.5, zoom=(1.15, 1.25))),
    (2.2, V.hook("E dezembro inteiro", "vem junto", "4 aulas de Natal prontas para imprimir")),
    (1.6, V.show("aula", "Plano de cada domingo", focus=.1)),
    (1.5, V.show("historia", "História pronta para contar", focus=.2)),
    (1.4, V.show("colorir", "Atividades por idade")),
    (1.4, V.show("cartao", "Lembrancinhas")),
    (3.8, V.cta("Teatro + 4 aulas + lembrancinhas", f"R$ {PRECO}", "Toque em Saiba mais")),
]
V.render(f"video-v2-teatro-{PRECO.replace(',', '')}", S)
