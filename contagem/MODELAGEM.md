# Contagem Regressiva: modelagem dos anúncios do Desafio Desincha Barriga

Fonte: Biblioteca de Anúncios BR, página "Andressa Carolina - Mães Que Treinam", ordenada por impressões (23/11/2026).
Cerca de 99 anúncios ativos, quase todos em vídeo, todos com a mesma copy ("Vem aí o Desafio Desincha Barriga... treinos AO VIVO... Clique em SAIBA MAIS").
Os mais antigos ainda ativos são de 19/03/2026. Lotes novos entraram em 08 e 10/10/2026 (até 6 anúncios usando o mesmo criativo).
O criativo é o que varia, a copy não muda.

## Estrutura dos 4 vídeos com mais impressões (transcritos)

| Bloco | O que eles fazem | Como modelamos (sem copiar texto) |
|---|---|---|
| Gancho (0–5 s) | Chamada do público + número: "7 dias pra desinchar...", "Mamãe, ficou com barriga pochete?" | Chamada pela data: "Tem uma data marcada?", "Deixou pra dezembro?", "15 minutos por dia" |
| Identificação | "Se você teve filho há meses ou há anos" | "Réveillon, viagem, casamento" |
| Mecanismo | "Não é dieta nem academia, é um protocolo específico e seguro para mães" | "Não é falta de tempo, é falta de plano: 15 min por dia contados até a sua data" |
| Prova | Antes/depois (Suzy, Emily), "50 mil mulheres", quilos | **Não modelado**: antes/depois, peso e depoimento são proibidos pelas nossas regras e pela Meta |
| Urgência | "Na próxima semana abre uma nova turma" | A própria data ("quantos treinos ainda cabem até lá") |
| CTA | "Toca em saiba mais e faz um teste rápido... no final eu te mostro o protocolo ideal... menos de um minuto" | Igual na mecânica: teste rápido, plano no final, menos de um minuto |

Formato: uma pessoa treinando em casa, sala clara, legenda grande palavra a palavra com a palavra ativa destacada.
Modelado com b-roll do Pexels (licença livre para uso comercial) + voz + legenda sincronizada + cartão do quiz no CTA.

## Entregues (com voz)
- v1-quiz.mp4 (20 s): gancho "Tem uma data marcada?" + bloco do teste + CTA.
- v2-calendario.mp4 (18 s): gancho "15 minutos por dia" + mecanismo dia 1 / 7 / 21 + CTA.
- v3-dezembro.mp4 (14 s): gancho de objeção "Deixou pra dezembro?" + urgência pela data + CTA.

## Versões longas, mais fiéis à estrutura (aguardando crédito do ElevenLabs)
A) "Vem aí" (modelo do anúncio 4)
Ei, você que tem uma data marcada pra esse fim de ano! Réveillon, viagem, casamento... Vem aí o Desafio Contagem Regressiva. São treinos de quinze minutos por dia, em casa e sem equipamento, montados do dia um até a sua data. Nada de dieta maluca, nada de passar horas na academia. E pra participar é muito simples: toca no botão saiba mais e faz um teste rápido. Em menos de um minuto, você me diz quantos dias faltam e quanto tempo você tem por dia, e no final eu te mostro o seu plano. Mas corre, porque a contagem já começou.

B) Problema + mecanismo (modelo dos anúncios 2 e 3)
Você marcou a viagem, comprou a roupa da festa... e agora olha pro calendário e pensa: não vai dar tempo. Calma, que isso tem solução. O problema não é falta de tempo, é falta de plano. Quem deixa pra resolver na última semana, com dieta radical e treino pesado, quase sempre desiste no meio. O que funciona na reta final é constância: quinze minutos por dia, todo dia, contados até a sua data. E é exatamente isso que o Desafio Contagem Regressiva faz. Então faz assim: toca em saiba mais e faz o teste rápido. No final, eu te mostro quantos treinos ainda cabem até a sua data, e o seu plano dia a dia. É menos de um minuto. Faz agora.

C) Gancho numérico (modelo do anúncio 1)
Trinta e sete dias até o Réveillon. Dá pra encaixar trinta e sete treinos de quinze minutos. Topa o desafio? É o Desafio Contagem Regressiva: treinos curtos, em casa, pra você chegar na sua data com a rotina em dia, em vez de começar tudo no dia trinta. E não importa se a sua data é o Réveillon, uma viagem ou um casamento. Toca no botão saiba mais e faz o teste: em menos de um minuto ele monta o seu plano até a data que você marcou.

Para gerar: voz Viviane (ElevenLabs, eleven_v4), salvar em assets/voz/, rodar o Whisper (words.json) e `python3 src/ugc.py`.
