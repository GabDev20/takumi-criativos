# Tarefa para o Codex: Kit Natal v3 (criativos, vídeos e página)

Repositório: `GabDev20/takumi-criativos`, branch `claude/kit-natal-ministerio-infantil`, pasta `kit-natal/`.
Faça na ordem de prioridade abaixo. **Se o limite de tokens estiver perto, pare ao fim da prioridade em curso, faça commit do que estiver pronto e liste o que faltou.** Cada prioridade é independente e entregável sozinha.

## Contexto (leia antes, não reescreva)

- Produto: "Kit Natal no Ministério Infantil" (marca Estrela Guia Kids), PDF para imprimir, **R$ 19,90**, vendido na Cakto. Público: líderes e professores de ministério infantil (igrejas evangélicas e católicas), mulheres 25 a 55 anos, celular.
- O que já vendeu (dados reais, 09/11): anúncio que **mostra o preço R$ 19,90 em destaque** ("an 03"), CTR de 5% a 6%, clique a menos de R$ 1. Página simples. Venda às 22h, pelo celular.
- O que vem no kit: 4 aulas de Natal (anjo visita Maria, José confia em Deus, Jesus nasce em Belém, magos adoram Jesus), 4 histórias prontas, 16 atividades por idade (3 a 11 anos) com gabarito, teatro "O Presente Mais Esperado" (8 a 10 min, papel para todas as crianças), lembrancinhas (cartão, marcadores, estrela de porta), cronograma de dezembro e lista de compras. Garantia de 7 dias.
- Ferramentas já prontas, **reaproveite em vez de criar do zero**:
  - `src/criativos2.py`: gera estáticos 1080x1350 e 1080x1920 com Playwright (fontes embutidas de `fonts/`). Uso: `python3 src/criativos2.py "19,90"`.
  - `src/video.py` + `src/video2.py`: geram vídeo vertical 1080x1920 com PIL + ffmpeg a partir das imagens em `out/img/` (`capa`, `aula`, `historia`, `colorir`, `labirinto`, `cacapalavras`, `teatro`, `cartao`, `marcadores`, `mockup`).
  - `out/lovable/index.html`: página de vendas atual (v2). Mantenha a identidade visual dela (azul `#1F3A5F`, ouro `#E9B44C`, fontes Baloo 2 e Nunito).

## Regras que não podem ser quebradas

1. Nada de depoimento inventado, número de vendas inventado, "de R$ 67 por…" falso ou contador de escassez falso. Só fatos do produto.
2. Sem promessa de resultado espiritual ou de comportamento das crianças.
3. Na página, copie **sem alterar** estes blocos da v2: o script do Meta Pixel (ID `1579712183467308`, eventos PageView, ViewContent e InitiateCheckout), o script que repassa a query string (UTMs) para os links da Cakto, e `<script src="https://api.cakto.com.br/api/product/checkout/tracker.js" async></script>`.
4. Todos os botões de compra apontam para `https://pay.cakto.com.br/9r765aw_1299013`.
5. Não substitua a página atual. A v3 é um arquivo novo, para teste A/B.
6. Não faça deploy, não mexa em Lovable, Cakto ou Meta. Só gere arquivos e faça commit.

## Prioridade 1: estáticos novos (o mais importante)

Gere em `out/v3/estaticos/`, cada um em 1080x1350 (feed) e 1080x1920 (stories, com respiro de 250 px no topo e na base para a interface do app):

| Arquivo | Ângulo | Título (pode ajustar a redação, mantendo a ideia) |
|---|---|---|
| `preco-a` | Preço gigante (o que já vendeu) | "Dezembro inteiro do ministério infantil por **R$ 19,90**" + 4 selos: 4 aulas, 16 atividades, teatro, lembrancinhas |
| `preco-b` | Preço por domingo | "Menos de **R$ 5 por domingo**" + "4 aulas de Natal prontas para imprimir" |
| `teatro` | Dor do culto de Natal | "Pediram um teatro de Natal? **Já está escrito.**" + página do teatro em destaque |
| `sabado` | Dor da preparação | "Sábado, 23h, e a aula de domingo ainda não está pronta?" + "Imprima e dê aula" |
| `idades` | Uma sala, várias idades | "Uma folha para cada idade: 3 a 5, 6 a 8, 9 a 11 anos" + 3 páginas de atividade lado a lado |

Requisitos: texto principal legível no celular (mínimo 64 px no título), no máximo 20% da área com texto pequeno, mostrar páginas reais do kit (imagens de `out/img/`), preço sempre visível. Gere também `out/v3/estaticos/contato.png`, uma folha de contato com todas as miniaturas, para revisão rápida.

Aceite: 10 PNGs + contato, todos abrindo, sem texto cortado (confira renderizando o contato).

## Prioridade 2: dois vídeos melhores

Gere em `out/v3/videos/`, 1080x1920, 30 fps, H.264, entre 15 e 22 segundos, **sem áudio** (o Gabriel coloca a música no Gerenciador). Reaproveite as funções de `src/video.py`.

1. `video-preco.mp4` (prioridade): versão em vídeo do anúncio que vendeu.
   - 0 a 2 s: gancho com movimento, "Dezembro inteiro do ministério infantil" e o preço **R$ 19,90** entrando com zoom.
   - 2 a 14 s: páginas reais passando rápido (aula, história, colorir, labirinto, teatro, cartão), cada uma com legenda curta em barra (1 s a 1,5 s cada).
   - 14 a 20 s: mockup, "Menos de R$ 5 por domingo", "Baixe e imprima hoje", "Toque em Saiba mais".
2. `video-teatro.mp4`: "Pediram um teatro de Natal para as crianças?", roteiro do teatro com zoom nas falas, "Papel para todas as crianças, até as de 3 anos", depois o resto do kit e o preço no fim.

Requisitos: legendas sempre dentro da área segura (entre 250 px e 1670 px de altura), nenhum quadro parado mais de 2 s, primeiro quadro já com texto (vira a miniatura). Gere uma folha de contato de quadros a cada 2 s para revisão: `out/v3/videos/<nome>-quadros.png`.

Aceite: 2 MP4 que tocam, duração entre 15 e 22 s, conferido com `ffprobe`.

## Prioridade 3: página v3 (para teste A/B)

Crie `out/v3/pagina/index.html`, página única, sem dependências além do Google Fonts, imagens referenciadas como `/k6a7d2294/p1.jpg` … `/k6a7d2294/p8.jpg` e `/k6a7d2294/mockup.webp` (já publicadas).

Estrutura, nesta ordem:
1. Faixa no topo: "Faltam X dias para o primeiro domingo de dezembro" (calculado em JS, como na v2).
2. Hero: título curto com o preço visível já na primeira tela do celular ("Seu dezembro no ministério infantil pronto por R$ 19,90"), mockup, botão verde grande, linha "Pix ou cartão · PDF no e-mail na hora · 7 dias de garantia".
3. "Veja por dentro": as 8 prévias em carrossel horizontal com rolagem por toque (CSS `scroll-snap`, sem biblioteca).
4. Dores (4 itens curtos, as mesmas da v2) e a virada.
5. O que vem no kit em lista com ✓ (curta, sem cards grandes).
6. Bloco do teatro.
7. Oferta com preço, "menos de R$ 5 por domingo" e botão.
8. Garantia, FAQ (copiar da v2) e rodapé.
9. Barra fixa de compra no rodapé do celular (como na v2).

Requisitos: página inteira com menos de 60 KB de HTML, nenhuma rolagem horizontal em 390 px de largura, botão de compra visível sem rolar na tela de um iPhone 13 (390x844). Confira com Playwright e salve `out/v3/pagina/print-mobile.png` (página inteira, 390 px).

Aceite: os 3 scripts obrigatórios presentes (busque `1579712183467308`, `pay.cakto.com.br` e `tracker.js`), print gerado, sem rolagem horizontal.

## Ao terminar

- `git add kit-natal/out/v3 kit-natal/src` e commit com mensagem descritiva no branch `claude/kit-natal-ministerio-infantil`, depois push.
- Responda com: o que ficou pronto, o que faltou (se faltou) e os caminhos dos arquivos.

---

# Guia para o Gabriel subir a campanha nova (se for fazer você mesmo)

**Antes de tudo:** cadastro validado na Cakto e bloqueio de Pix resolvido com o suporte. Sem isso, parte de quem quer comprar é barrada no pagamento.

**Campanha:** "KIT NATAL | Vendas | v3", objetivo Vendas, otimização para **Compra** no pixel `1579712183467308`, orçamento **por conjunto** (não na campanha). A campanha atual fica parada como está, sem edições.

**4 conjuntos de R$ 15/dia** (R$ 60/dia, cerca de 5 dias até R$ 300), mesmo público em todos (o da campanha que vendeu), **um anúncio por conjunto**:

| Conjunto | Criativo | Destino |
|---|---|---|
| 1 · Preço estático | `preco-a` (feed + stories) | Página atual |
| 2 · Preço vídeo | `video-preco.mp4` | Checkout direto |
| 3 · Teatro | `teatro` ou `video-teatro.mp4` | Página atual |
| 4 · Página v3 | `preco-a` (mesmo do conjunto 1) | Página v3 (comparação justa de página) |

**Parâmetros de URL** em todos os anúncios (sem "?" no começo):
`utm_source=FB&utm_campaign={{campaign.name}}&utm_medium={{adset.name}}&utm_content={{ad.name}}&utm_term={{placement}}`

**Régua por conjunto:**
- Pausar: R$ 20 gastos sem nenhum início de checkout, ou R$ 40 sem venda paga.
- Manter: vendeu com custo por venda até cerca de R$ 30.
- Escalar: 3 vendas no mesmo conjunto, +20% a 30% de orçamento a cada 48 h.
- **Não editar anúncio que está rodando.** Mudança = anúncio novo.
