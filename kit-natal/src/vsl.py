# VSL legendada (sem áudio), 1080x1920. Uso: python3 src/vsl.py
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import video as V
V.render.__globals__["subprocess"]  # crf set via env

from PIL import Image
IMG = V.OUT / "img"; _c = {}
def page(n, w):
    k = (n, w)
    if k not in _c:
        im = Image.open(IMG / f"{n}.png").convert("RGB"); _c[k] = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    return _c[k]
V.page = page
H = V.hook; S = V.show
SC = [
    (3.5, H("Professora do ministério infantil,", "isto é pra você", "assista até o fim")),
    (4.0, H("Dezembro chegando e a aula de Natal", "ainda não está pronta?")),
    (4.0, H("Sábado, 23h, procurando atividade na internet", "de novo?")),
    (4.0, H("Crianças de 3 e de 10 anos na mesma sala", "e nada serve", "para as duas idades")),
    (4.0, H("E ainda pediram um teatro", "para o culto de Natal")),
    (3.5, H("E se o mês inteiro", "já estivesse pronto?")),
    (4.0, S("aula", "Plano de cada domingo, 40 minutos", top="4 aulas de Natal", focus=.1)),
    (3.5, S("historia", "É só ler e contar", top="História pronta", focus=.2)),
    (2.5, S("colorir", "3 a 5 anos", top="Atividade por idade")),
    (2.5, S("labirinto", "3 a 8 anos", top="Atividade por idade")),
    (2.5, S("cacapalavras", "6 a 11 anos", top="Atividade por idade")),
    (4.0, S("teatro", "Papel para todas as crianças", top="Teatro do culto de Natal", focus=.1)),
    (3.0, S("cartao", "Cartões, marcadores e estrela", top="Lembrancinhas")),
    (4.0, H("Você imprime em casa,", "abre o plano e dá aula", "Papel A4 comum")),
    (4.5, H("Pacote Essencial: o kit de Natal", "R$ 19,90")),
    (5.0, H("Pacote Completo: + Janeiro Pronto + Certificados e Convites", "R$ 29,90", "valem R$ 44,70 separados")),
    (3.5, H("7 dias de garantia", "risco zero", "não serviu, devolvemos 100%")),
    (4.0, H("Escolha seu pacote", "logo abaixo", "acesso imediato no seu e-mail")),
]
V.render("vsl-kit-natal", SC)
