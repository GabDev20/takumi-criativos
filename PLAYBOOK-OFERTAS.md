# Playbook de ofertas: minerar, decidir, modelar, testar, escalar

Base: vídeos do Del Francco (YouTube EUlDspUSkCU e reel Dfxp3VFveEj), mais regras de operação da Takumi.
Vale para toda oferta nova daqui em diante.

## 1. Minerar (Biblioteca de Anúncios, BR)
- Buscar por palavra-chave de nicho ("atividades para…", "kit…", "para imprimir", "PDF") com a extensão de mineração.
- Anotar por oferta: dias no ar do anúncio mais antigo ativo, nº de anúncios ativos, nº de ângulos diferentes, tipo de funil, ticket, link da página.

## 2. Decidir se testa (os 3 filtros, nesta ordem)
1. **Tempo no ar.** Menos de 7 dias: ignorar. De 7 a 29 dias: observar. 30 dias ou mais: validada, pode modelar. Pesa mais que o nº de anúncios.
2. **Ângulos.** Listar os públicos e dores possíveis (público × dor).
   - 3 ou menos: oferta "pega caixa", com teto de R$100–500/dia de faturamento. Serve para gerar caixa, não para apostar alto.
   - 5 ou mais: oferta com potencial de escala.
3. **Funil.**
   - Low ticket com página de texto simples (TSL): modelar e **gamificar** (quiz, relatório, preço).
   - High ticket com VSL longa: pular (no Brasil não compensa).

Só entra em produção se passar no 1 e no 3. O 2 define o tamanho da aposta.

## 3. Modelar
- **Por ângulo:** copiar estrutura, página e criativos, e trocar o tema para um público maior ou vizinho (autismo para TDAH, inglês para italiano). Leilão diferente, teto maior.
- **Por criativo:** mesma oferta, com ângulos de anúncio que o concorrente não usa.
- **Melhor:** os dois juntos.
- **Criativo base:** transcrever o validado, trocar o tema, narrar (ElevenLabs) e usar estáticos (Codex). Depois melhorar com UGC/avatar.
- **Gamificação:** quiz de 6 a 10 perguntas, relatório personalizado, trecho desfocado e o preço com os benefícios. O relatório completo precisa estar no produto pago.

## 4. Limites (não negociáveis)
- Nada de cloaking, página falsa para revisão ou promessa enganosa.
- Saúde e atributos pessoais: o anúncio não afirma nem insinua condição do público ("seu filho tem TDAH?"). O quiz informa que não é diagnóstico.
- Eventos de pixel e CAPI disparando (PageView, ViewContent, InitiateCheckout, Purchase) antes de ligar o orçamento.

## 5. Testar
- **Estrutura:** 1 campanha com objetivo Compra, 1 conjunto aberto (BR, 25–55+, sem interesse), orçamento na campanha.
- **Criativos:** 3 ângulos × 2 criativos = 6 anúncios.
- **Orçamento:** R$40–60/dia por oferta.
- **Ticket de entrada:** R$19,90–27,90, com 1–2 order bumps.
- **Cortes:**
  - Anúncio com gasto de 1× o ticket e 0 IC: pausar.
  - Anúncio com gasto de 2× o ticket médio e 0 venda: pausar.
  - Oferta com R$150 gastos e 0 venda:
    - CTR do link abaixo de 1%: problema de criativo. Novos ângulos, 1 rodada.
    - CTR ok mas página não converte em IC: problema de página ou oferta.
    - IC ok sem venda: problema de checkout ou preço.
  - Duas rodadas sem venda: matar a oferta.

## 6. Escalar
- **Critério:** CPA abaixo de 80% do ticket médio (produto + bumps, já descontada a taxa) por 3 dias seguidos.
- **Vertical:** subir 20–30% do orçamento a cada 48h enquanto o CPA se mantiver.
- **Horizontal:** cada ângulo vencedor ganha a própria campanha. Testar 2 ângulos novos por semana até esgotar a lista do filtro 2.
- **Teto:** quando o CPA sobe 3 dias seguidos após um aumento, voltar ao último orçamento bom e escalar por ângulo novo, não por orçamento.

## Registro de validação (16/11/2026, Biblioteca de Anúncios BR)
- TDAH/foco: "Escada do Foco – 250 Atividades TDAH" (jornadapratica.com/TDAH, Kiwify, R$ 24,90, página de texto simples). Anúncio ativo desde 12/08/2026 (96 dias). O mesmo operador roda "Kit Autismo Pro 900 Atividades" desde 20/04/2026: modelagem por ângulo autismo → TDAH confirmada. Passa nos filtros 1 e 3.
- Alfabetização: Prof. Luana Rodrigues (profluanarodrigues.com.br, Hotmart), 46 anúncios ativos, mais antigo de 30/09/2026 (47 dias), 6 kits diferentes. "Kit Destrave a Leitura" R$ 37 (de R$ 89,90), público professora. Também: Clube das Atividades (10.000 atividades R$ 10, desde 13/09), Atividades Cursiva (desde 29/05). Passa nos filtros 1 e 3.
- Nossa modelagem: mesma oferta (kit de atividades em PDF, ticket baixo), ângulo trocado para os pais, página de texto trocada por quiz.
