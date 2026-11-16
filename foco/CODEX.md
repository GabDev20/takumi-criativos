# Tarefa para o Codex: estáticos "formato bom" para os 3 quizzes (16/11/2026)

Repositório `GabDev20/takumi-criativos`, branch `claude/kit-natal-ministerio-infantil`, pasta `foco/`.
Faça commit ao fim de cada produto. Saída em `foco/out/criativos/<produto>/`.

## O formato (modelado do reel "criativo ruim × criativo bom")

O criativo ruim é o mockup do produto com lista de benefícios. O bom parece post nativo, não anúncio:

1. **Foto realista gerada por IA** (gpt-image) de uma criança no estado-problema, cenário de casa ou sala real, luz natural, nada de estúdio.
   Rosto expressivo (tédio, frustração, birra leve). Nenhuma criança real, nenhuma marca, nenhum personagem conhecido.
2. **Balão de fala** branco, contorno preto, fonte "mão" (Courier/handwriting), com a fala da criança.
3. **Faixa verde no topo** (fundo #4CD964, texto branco, fonte grossa arredondada, leve rotação -2°): pergunta direta para quem decide a compra.
4. **Faixa vermelha embaixo** (fundo #E53950, texto branco, rotação -3°): a oferta, com número e preço.
5. **Faixa verde pequena** no rodapé: "Clique em saiba mais" (ou "Faça o teste: toque em saiba mais" nos de quiz).
6. Opcional: um mini-mockup real do produto (página do PDF) no canto, tamanho 25% no máximo.

Tamanhos: 1080x1350 (feed) e 1080x1920 (stories, com 250 px livres no topo e na base). Texto de faixa com no mínimo 54 px.
Faça a foto com o gpt-image e monte as faixas em código (Playwright ou PIL), para o texto sair perfeito.
As páginas reais dos produtos estão em `foco/out/pdf/` e `foco/out/pdf-leitura/` (gere com `pdftoppm -r 110 -png`).

## Regras (não negociáveis)

- Nada de "seu filho tem TDAH?", "diagnóstico", "cura", "resultado garantido". Não afirmar condição de saúde de quem vê o anúncio.
- Nada de depoimento, número de vendas, "de R$ 97 por", contador, selo falso.
- Usar só os números abaixo.

## Os produtos (fatos)

| Produto | Página (quiz) | Preço | Números permitidos |
|---|---|---|---|
| Trilha do Foco | https://egk-7d2294.lovable.app/trilha-do-foco | R$ 19,90 | 250 atividades, 5 etapas, 3 níveis, 5 a 12 anos, menos de R$ 0,08 por atividade |
| Lê Comigo | https://egk-7d2294.lovable.app/le-comigo | R$ 19,90 | 198 fichas, 3 apostilas, 16 famílias silábicas, 4 a 8 anos, cerca de R$ 0,10 por ficha |
| Plano bíblico (oferta atual) | https://egk-7d2294.lovable.app/plano-biblico | R$ 27,90 | 500 atividades bíblicas + 5 músicas, 5 coleções, 5 a 11 anos; 1 coleção R$ 19,90 |

## 18 estáticos (3 ângulos × 2 variações por produto)

Nome do arquivo: `<produto>-<angulo>-<v>-feed.png` e `-stories.png`.

### Trilha do Foco (`foco`)
| Ângulo | Foto | Balão | Faixa verde | Faixa vermelha |
|---|---|---|---|---|
| licao | menino de 8 anos debruçado na lição, lápis largado | "Não consigo terminar!" | "Mãe? A lição nunca termina?" | "250 atividades de foco para imprimir · R$ 19,90" |
| tela | menina de 7 anos agarrada ao tablet, mãe estendendo a mão | "Só mais 5 minutinhos!" | "Troque 15 minutos de tela por 1 atividade" | "250 atividades de atenção e calma · R$ 19,90" |
| teste | menino distraído olhando a janela, caderno aberto | "Ué, o que era pra fazer?" | "Qual habilidade de foco ele mais precisa treinar?" | "Faça o teste de 1 minuto" |
v2 de cada ângulo: outra criança (outro gênero e idade), mesmo texto.

### Lê Comigo (`leitura`)
| Ângulo | Foto | Balão | Faixa verde | Faixa vermelha |
|---|---|---|---|---|
| trava | menina de 6 anos com livro aberto, cara de frustração | "Não sei ler isso!" | "Mãe? Ele ainda trava na leitura?" | "198 fichas da sílaba à frase · R$ 19,90" |
| ferias | menino de 6 anos de férias, mochila jogada no canto | "Já esqueci as letras..." | "Férias chegando: ele vai esquecer o que aprendeu?" | "15 minutos por dia de leitura em casa · R$ 19,90" |
| fase | menina de 5 anos apontando uma sílaba no papel | "BA... BE... BI..." | "Em que fase da leitura seu filho está?" | "Descubra em 1 minuto: teste grátis" |

### Plano bíblico (`biblico`)
| Ângulo | Foto | Balão | Faixa verde | Faixa vermelha |
|---|---|---|---|---|
| celular | menino de 9 anos no sofá, só com o celular | "Só mais um vídeo!" | "Mãe? Férias e ele só quer o celular?" | "500 atividades bíblicas + 5 músicas · R$ 27,90" |
| salinha | menina de 6 anos sentada de braços cruzados numa salinha de igreja colorida | "Que aula chataaa" | "Tia? Já não sabe o que passar na salinha?" | "500 atividades bíblicas para imprimir · R$ 27,90" |
| plano | duas crianças pintando uma atividade na mesa da cozinha | "Agora é a minha vez!" | "Monte o plano de férias sem tela em 1 minuto" | "Responda 6 perguntas: é grátis" |

Aceite: 36 PNGs (18 × 2 tamanhos) + `contato.png` por produto. Nenhum texto cortado, nenhuma mão ou rosto deformado (refaça a foto se tiver).

## Textos dos anúncios (já prontos, usar no Gerenciador)

Arquivo `foco/out/criativos/textos.md` (gerado por Claude junto com este brief).
