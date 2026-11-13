# Tarefa para o Codex: Oferta Premium R$ 97 (produtos, página, criativos e entrega)

Repositório: `GabDev20/takumi-criativos`, pasta `kit-natal/` (ou o projeto "Kit Natal Criativos" onde o premium está sendo montado).
Siga **todas as instruções que o Gabriel já te deu para os outros produtos** (identidade visual, voz, formato dos PDFs, nomes de arquivos) e as regras do `CODEX.md`. Este arquivo só acrescenta o que é novo.

Trabalhe por etapas. Ao fim de cada etapa, faça commit. Se o limite de tokens estiver perto, pare no fim da etapa em curso, faça commit e liste o que faltou.

---

## Contexto da oferta (decidido com o Gabriel)

**Produto de entrada que já vende:** Kit Natal no Ministério Infantil.
- R$ 19,90 (Essencial) e R$ 29,90 (Completo); confirme os preços na Cakto.
- Campanha atual "KIT NATAL | Teste orçamento alto | B 500". O anúncio que vende é o **an 06 video teatroV4**. **Não mexa** nessa campanha nem na página atual.

**Nova oferta, funil separado, com o premium na frente:**

| Etapa | Produto | Preço | Para quem aparece |
|---|---|---|---|
| Frente | Premium (kit completo + vídeos, músicas, áudios, orações, histórias bíblicas) | R$ 97 | Tráfego frio da campanha nova |
| Upsell | Complemento: conteúdo **que não está no premium** | R$ 67 | Quem comprou o 97 |
| Downsell do upsell | Versão menor do complemento (parte do conteúdo do 67) | R$ 37 | Quem comprou o 97 e recusou o 67 |
| Recuperação | Kit Completo atual | R$ 29,90 | Quem **não** comprou o 97: pop-up de saída da página e recuperação de checkout abandonado |
| Upgrade (Systeme.io) | Premium para quem já comprou o kit de R$ 19,90/29,90 | R$ 77 | Compradores do produto de entrada, por mensagem do Systeme.io |

**Regras de lógica do funil:**
1. Ninguém pode receber oferta de algo que já comprou. O kit de R$ 29,90 está dentro do 97, então **nunca** aparece depois da compra do 97.
2. O 67 não pode repetir nada do 97, e o 37 não pode repetir nada do 97. O 37 é um subconjunto do 67.
3. O upgrade de R$ 77 é uma **oferta separada** na Cakto, com checkout próprio. Ele segue para o upsell de 67 e o downsell de 37, mas **sem** o kit de 29,90.

**Públicos do premium:**
- **Atual:** líderes e professores de ministério infantil.
- **Novo:** mães, avós, professoras e público cristão em geral que quer viver o Natal com as crianças em casa.

---

## Etapa 1: Inventário e verificação dos produtos

1. Liste tudo o que existe hoje de cada produto: 97, 67, 37 e 29,90. Para cada item, dê o nome, o tipo (PDF, vídeo, áudio, música), a quantidade e o caminho ou link.
2. Gere `kit-natal/out/premium97/INVENTARIO.md` com uma tabela por produto e uma matriz de sobreposição. A matriz mostra item × produto e prova que o 67 e o 37 não repetem o 97.
3. **Se o produto de 67 não existir, produza.** Siga as mesmas instruções de produção dos outros produtos. Sugestões de conteúdo complementar que não está no premium; escolha o que fizer sentido com o que já existe:
   - Janeiro e fevereiro prontos: aulas de volta às aulas da EBD/ministério.
   - Culto de Natal da família: roteiro de devocional em casa, com 7 noites até o Natal.
   - Pacote de certificados, convites, cartazes e decoração para a festa de Natal da igreja.
   - Cantata ou musical curto com playback e partitura simplificada, se houver música própria.
4. **Se o produto de 37 não existir, produza** como versão menor do 67: mais ou menos metade dos itens, sem repetir o 97.
5. Revise cada PDF: ortografia, numeração de páginas, capa, sumário, gabaritos e links internos funcionando.
6. Revise cada vídeo e áudio: abre, tem som, legenda dentro da área segura e duração certa.

## Etapa 2: Entrega pelo Google Drive

1. Organize uma pasta de entrega por produto: `Premium 97`, `Complemento 67`, `Complemento Essencial 37` e `Kit Completo 29,90`. Cada pasta leva um PDF ou arquivo "COMECE AQUI" com o índice e os links.
2. Coloque **somente essas pastas de entrega** como "Qualquer pessoa com o link: Leitor". Não altere o compartilhamento de nenhuma outra pasta ou arquivo do Drive do Gabriel.
3. Teste cada link numa janela anônima. Ele precisa abrir sem login e sem pedir acesso.
4. Peça as permissões de que precisar. Se não conseguir alterar o compartilhamento, diga exatamente qual pasta falta e por quê.

## Etapa 3: Página de vendas do Premium R$ 97 (arquivo novo)

Crie `kit-natal/out/premium97/pagina/index.html`.
- **Base:** clone a página que já vendeu (`out/lovable/index.html` e v4) e mantenha a identidade visual: azul `#1F3A5F`, ouro `#E9B44C`, Baloo 2 e Nunito.
- **Scripts:** copie **sem alterar** o Meta Pixel (`1579712183467308`), o script que repassa as UTMs para os links da Cakto e o `tracker.js` da Cakto.
- **Botões:** todos apontam para o checkout do **97**. Deixe a URL numa constante no topo do arquivo para trocar fácil.

**Antes de escrever:** pesquise 3 a 5 páginas de produtos digitais cristãos ou infantis que vendem bem (Hotmart, Kiwify, Cakto, Eduzz) e anote em `out/premium97/pagina/REFERENCIAS.md` o que você vai aproveitar de cada uma. Use apenas as técnicas, nunca copie o texto.

**Estrutura (mobile first, a pessoa decide nos primeiros 3 segundos):**
1. **Primeira tela:** título com a transformação ("O Natal das crianças pronto: aulas, histórias, músicas e vídeos em um só lugar"), subtítulo para os dois públicos (igreja e casa) e mockup de tudo junto. Mostre o preço R$ 97 e "acesso imediato" já na primeira tela, com um botão verde grande.
2. **VSL curta** (60 a 120 s) logo abaixo do título, com a voz do Gabriel no ElevenLabs e legenda. Mostre o conteúdo real, abrindo os arquivos.
3. **Para quem é:** cards para "líder do ministério infantil", "professora", "mãe" e "avó", cada um com uma frase de situação real.
4. **O que você recebe:** blocos por tipo de conteúdo, com imagem real e quantidade exata do inventário. Os números saem da Etapa 1, nada estimado.
5. **Como funciona:** 3 passos: compra, link no e-mail e WhatsApp, abre no celular ou imprime.
6. **Comparação honesta:** "Kit Completo (R$ 29,90)" × "Premium (R$ 97)", mostrando o que só o premium tem. Esta é a ancoragem permitida: preços reais que existem de verdade. **Proibido** "de R$ 297 por R$ 97" inventado.
7. **Oferta:** lista final com preço, Pix ou cartão, parcelamento se a Cakto oferecer, e botão.
8. **Garantia de 7 dias** com selo.
9. **FAQ** com as objeções reais:
   - Serve para igreja católica e evangélica?
   - Serve para usar em casa?
   - Preciso imprimir tudo?
   - Abre no celular?
   - Como recebo?
   - E se eu já comprei o kit de R$ 19,90? (responda apontando para o upgrade)
10. **Rodapé** com botão repetido. Na rolagem do celular, mostre uma barra fixa com o botão a partir da seção 3.
11. **Pop-up de saída e retorno de aba:** "Ainda não é a hora do completo? Leve o Kit Completo por R$ 29,90", com link para o checkout do 29,90 com UTM `utm_content=exit97`. Aparece uma vez por visita.

**Técnicas obrigatórias:**
- Prova só com fatos: imagens reais do produto, contagem de itens e garantia.
- Sem depoimentos inventados, sem números de vendas e sem contador falso.
- Prazo real permitido: "use em dezembro", a data do Natal.
- Desempenho: imagens em WebP e com lazy-load, vídeo com pôster, primeira tela carregando em menos de 2,5 s em 4G.

**Aceite:**
- Print do celular (390 px) e do desktop em `out/premium97/pagina/prints/`.
- Sem rolagem horizontal.
- Os 3 scripts presentes: confira por grep `1579712183467308`, `pay.cakto.com.br` e `tracker.js`.
- Todos os links de compra testados.

## Etapa 4: Página de upgrade para compradores do kit de entrada

Crie `out/premium97/upgrade/index.html`: uma página curta para quem já comprou o kit.
- Título: "Você já tem o Kit. Complete com vídeos, músicas e histórias".
- Mostre só o que o premium tem a mais.
- Preço de upgrade R$ 77, com botão para o checkout da oferta de upgrade (constante no topo).
- Mesmos scripts obrigatórios.

## Etapa 5: Sequência do Systeme.io (verificar)

O Gabriel diz que o Systeme.io já está configurado. **Verifique e corrija** só o que estiver faltando.

1. **Gatilho:** compra do kit de R$ 19,90 ou R$ 29,90.
2. **Mensagens:**
   - **Mensagem 1** (até 15 min após a compra): agradece, reforça o link de acesso e apresenta o upgrade por R$ 77.
   - **Mensagem 2** (dia seguinte): mostra um trecho de vídeo ou música do premium e repete o upgrade.
   - **Mensagem 3** (2 dias depois): último lembrete, com o prazo real do Natal.
   - Remova o contato da sequência se ele comprar o upgrade ou o 97.
3. **Links:** todos com `utm_source=systeme&utm_medium=email&utm_campaign=upgrade97`. Se houver WhatsApp, use `utm_medium=whatsapp`.
4. **Teste:** faça uma compra de teste e confirme que a mensagem 1 chega.

## Etapa 6: Criativos para a oferta de R$ 97

Gere em `out/premium97/criativos/`. **Nenhum criativo desta oferta mostra R$ 19,90 ou R$ 29,90.**

**Vídeos (1080x1920, 15 a 35 s):**
- Estilo do teatroV4, que é o que vende: primeiro quadro com texto, nenhum quadro parado mais de 2 s, legenda entre 250 e 1670 px de altura.
- Voz do Gabriel no ElevenLabs.
- Gere uma folha de quadros a cada 2 s para revisão.

| Nome | Ângulo | Gancho (0 a 2 s) |
|---|---|---|
| `an 10 video teatroPremium` | Reedição do teatroV4 vencedor, sem preço antigo, terminando no premium | "Pediram um teatro de Natal para as crianças?" |
| `an 11 video tudoPronto` | Abre os arquivos no celular: aulas, vídeos, músicas, orações | "Todo o Natal das crianças em um só lugar" |
| `an 12 video maeAvo` | Público novo: casa, família | "Quer viver o verdadeiro Natal com seus filhos e netos?" |
| `an 13 video professora` | Sala de aula, EBD, escola cristã | "Dezembro inteiro de aulas de Natal prontas" |
| `an 14 video musica` | Trecho de música ou áudio do premium tocando | Começa com a música, texto "As crianças vão cantar o Natal" |
| `an 15 video preco97` | Preço com a lista do que vem | "Tudo isso por R$ 97, acesso na hora" |

**Estáticos (1080x1350 e 1080x1920):**
- 3 ângulos: `tudoPronto`, `maeAvo` e `comparativo`.
- Todos com páginas e telas reais do produto.

**Textos do anúncio:** para cada criativo, gere 2 textos principais, 2 títulos e 1 descrição em `out/premium97/criativos/textos.md`.

**Folha de contato:** gere `out/premium97/criativos/contato.png` com todas as miniaturas.

## Etapa 7: Verificação final e entrega de "PRONTO"

Rode uma checagem completa e só então escreva `out/premium97/PRONTO.md` com:

1. **Status:** uma linha por item, OK ou PENDENTE e o motivo:
   - os 5 produtos;
   - pastas do Drive públicas e testadas;
   - página 97;
   - página de upgrade;
   - sequência do Systeme.io;
   - criativos;
   - scripts de rastreamento.
2. **Bloco para o Claude configurar a Cakto e o Meta** (o Gabriel vai colar no outro chat), com:
   - **Cakto:** nome e ID de cada produto e oferta e a URL de checkout de cada uma (97, 67, 37, 29,90 e upgrade 77). Se algum produto ou oferta ainda não existir na Cakto, marque PENDENTE: o Claude cria.
   - **Funil na Cakto:**
     - 97 → upsell 67 → se recusar, downsell 37;
     - upgrade 77 → upsell 67 → se recusar, downsell 37;
     - 29,90 sem upsell para o 97 (quem compra o 29,90 entra no Systeme.io).
   - **Entrega:** o link de entrega do Drive de cada produto, que é o que vai em cada produto na Cakto.
   - **Páginas:** a URL publicada da página 97 e da página de upgrade. Se não publicou, diga onde está o arquivo e o que falta para publicar.
   - **Criativos:** lista com nome exato do anúncio, caminho do arquivo e textos.
   - **Systeme.io:** nome da sequência e confirmação do teste.
3. Faça o commit de tudo e coloque o hash do commit no PRONTO.md.

**Limites:** não crie nem edite campanhas no Meta e não altere a campanha "KIT NATAL | Teste orçamento alto | B 500". A configuração final da Cakto e do Meta será feita depois, com o OK do Gabriel.
