# Tarefa para o Codex: criativos da oferta "500 Atividades Bíblicas" (15/11/2026)

Repositório `GabDev20/takumi-criativos`, branch `claude/kit-natal-ministerio-infantil`, pasta `colecao/`.
Siga as regras de `kit-natal/CODEX.md` (identidade, formatos, área segura). Este arquivo só traz o que é novo.
Faça commit ao fim de cada prioridade. Se o limite de tokens estiver perto, pare ao fim da prioridade em curso e liste o que faltou.

## A oferta (fatos; use só estes números)

- Marca: Estrela Guia Kids. Produto: **Coleção Atividades Bíblicas**, PDFs para imprimir, 5 a 11 anos.
- **5 coleções de 100 atividades** (50 histórias, 10 tipos de atividade por história, com gabarito):
  1. Heróis do Antigo Testamento · 2. A Vida de Jesus · 3. Parábolas de Jesus · 4. Milagres e Amigos de Jesus · 5. Orações, Salmos e Valores.
- Tipos: caça-palavras, labirinto, código secreto, pinte por número, complete o versículo, verdadeiro ou falso, ligue as colunas, palavras embaralhadas, copie e ilustre, acróstico.
- Preços: **Pacote Completo (500 atividades) R$ 47,90** · 1 coleção (100 atividades) R$ 19,90.
- Ancoragem permitida (é conta real): "5 coleções avulsas = R$ 99,50. Pacote completo: R$ 47,90. Economize R$ 51,60." e "menos de R$ 0,10 por atividade".
- Entrega: link no e-mail em minutos. Pagamento único. Garantia de 7 dias.
- Página: `https://egk-7d2294.lovable.app/atividades-biblicas`
- Os PDFs estão em `colecao/out/pdf/`. Gere as imagens das páginas reais com `pdftoppm -r 110 -png` (capa = pág. 1; atividades = pág. 3 a 102). **Todo criativo mostra páginas reais do produto.**

## Tom: agressivo, mas só com fatos

Pode: preço gigante, "500", contraste tela × papel, economia em reais, "imprima hoje", urgência real do fim de ano ("férias de dezembro e janeiro sem tela").
Não pode: depoimento, número de vendas ou de famílias, "de R$ 197 por", contador, promessa de comportamento da criança ou resultado espiritual, texto que afirme a fé de quem lê ("você, mãe cristã"). Nada de personagens ou arte de concorrentes.

## Prioridade 1: 10 estáticos (o mais importante)

Saída em `colecao/out/criativos/estaticos/`, cada um em 1080x1350 e 1080x1920 (respiro de 250 px no topo e na base no stories). Reaproveite `kit-natal/src/criativos2.py` (Playwright + fontes de `kit-natal/fonts/`). Título com no mínimo 64 px.

| Arquivo | Ângulo | Título |
|---|---|---|
| `est-01-500-preco` | Número + preço gigante | "500 atividades bíblicas para imprimir · **R$ 47,90**" + leque com 6 páginas reais |
| `est-02-centavos` | Preço por unidade | "Menos de **R$ 0,10** por atividade" + "500 atividades · pagamento único" |
| `est-03-telas` | Tela × papel (duas metades) | "Menos tela. **Mais Bíblia.**" esquerda: celular apagado em cinza; direita: páginas coloridas à mão |
| `est-04-economia` | Conta real | "5 coleções avulsas: R$ 99,50 → **Pacote completo: R$ 47,90**" + selo "Economize R$ 51,60" |
| `est-05-ferias` | Férias | "Férias chegando: **500 ideias sem tela**" + calendário dez/jan |
| `est-06-10-tipos` | Variedade | "10 tipos de atividade × 50 histórias da Bíblia" + grade 2x5 com uma página de cada tipo |
| `est-07-professora` | Ministério infantil | "Um ano de atividades para a salinha por **R$ 47,90**" |
| `est-08-colecoes` | As 5 capas | "5 coleções. 500 atividades. 1 pagamento." + as 5 capas em leque |
| `est-09-100` | Entrada barata | "100 atividades bíblicas por **R$ 19,90**" + "ou leve as 500 por R$ 47,90" |
| `est-10-imprima-hoje` | Imediatismo | "Compre agora, **imprima em 5 minutos**" + 3 passos (e-mail → imprime → a criança faz) |

Gere `out/criativos/estaticos/contato.png` com todas as miniaturas. Aceite: 20 PNGs + contato, sem texto cortado.

## Prioridade 2: 2 vídeos em código (PIL/Playwright + ffmpeg)

Saída em `colecao/out/criativos/videos/`, 1080x1920, 30 fps, H.264 + AAC, 20 a 30 s. **Vídeo 100% em código** (reaproveite `kit-natal/src/video4.py` e `video5.py`). **Só a voz vem do ElevenLabs** (voz "Gabriel Geral", a mesma dos vídeos v5; reaproveite `kit-natal/src/narracao3.py`/`audio.py`). Não gere vídeo no ElevenLabs. Legenda queimada na área segura (250 a 1670 px), primeiro quadro já com texto, nenhum quadro parado por mais de 2 s.

1. `vid-01-teatro-500.mp4` — modelado no **teatroV4** (mesma estrutura de cortes, ritmo e estilo de legenda), roteiro novo:
   - 0–2 s: "Seu filho pediu o celular de novo?"
   - 2–8 s: páginas reais passando rápido (caça-palavras, labirinto, pinte por número, código secreto), legenda: "Entregue uma destas."
   - 8–16 s: "500 atividades bíblicas para imprimir. 50 histórias, de Gênesis a Jesus. 10 tipos de atividade."
   - 16–22 s: as 5 capas + "5 coleções avulsas: R$ 99,50. Pacote completo: R$ 47,90."
   - 22–26 s: "Chega no e-mail em minutos. Toque em Saiba mais."
2. `vid-02-preco-500.mp4` — modelado no **vídeo 03 / an 03** (preço em destaque desde o primeiro quadro):
   - 0–2 s: "500 atividades bíblicas" + **R$ 47,90** entrando com zoom.
   - 2–14 s: uma página de cada um dos 10 tipos, 1,2 s cada, com o nome do tipo em barra.
   - 14–20 s: "Menos de R$ 0,10 por atividade" → "Imprima hoje" → "Toque em Saiba mais".

Gere `<nome>-quadros.png` (um quadro a cada 2 s). Aceite: 2 MP4 com áudio, duração conferida com `ffprobe`.

## Prioridade 3 (se sobrar limite): 3 vídeos extras sem voz

`vid-03-tipos.mp4` (10 tipos em 15 s), `vid-04-economia.mp4` (a conta de R$ 99,50 → R$ 47,90 animada), `vid-05-telas.mp4` (tela × papel). Mesmo formato, só legenda.

## Textos do anúncio

Gere `out/criativos/textos.md` com, para cada criativo, 1 texto principal (até 220 caracteres), 1 título (até 40) e a URL com UTM:
`https://egk-7d2294.lovable.app/atividades-biblicas?utm_source=meta&utm_medium=paid&utm_campaign=colecao500&utm_content=<nome-do-arquivo>`

## Ao terminar

`git add colecao/out/criativos colecao/src` → commit → push no branch. Responda com o que ficou pronto, o que faltou e os caminhos. Não mexa em Lovable, Cakto ou Meta.
