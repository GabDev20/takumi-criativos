// Gera perfil, capa e 4 posts para as páginas Trilha do Foco e Lê Comigo. Uso: node src/arte_paginas.js
const { chromium } = require('playwright');
const path = require('path'); const fs = require('fs');
const OUT = path.join(__dirname, '..', 'out', 'paginas');
const SRC = path.join(OUT, '_src');
const F = path.join(__dirname, '..', '..', 'kit-natal', 'fonts');
const img = n => 'file://' + path.join(SRC, n);
const css = `@font-face{font-family:B;src:url(file://${F}/baloo-2-latin-800-normal.woff2)}
@font-face{font-family:N;src:url(file://${F}/nunito-latin-700-normal.woff2)}@font-face{font-family:N8;src:url(file://${F}/nunito-latin-800-normal.woff2)}
*{box-sizing:border-box;margin:0}body{font-family:N;overflow:hidden}
.b{font-family:B;line-height:1.02}.pg{border-radius:14px;box-shadow:0 14px 40px rgba(0,0,0,.28);background:#fff}`;
const marca = {
  foco: { nome: 'Trilha do Foco', c1: '#123B7A', c2: '#2E6FD8', ac: '#F2B705', bg: '#EAF1FC', site: 'egk-7d2294.lovable.app/trilha-do-foco',
    logo: `<div style="display:flex;gap:10px;align-items:flex-end;justify-content:center">${['#2E6FD8','#16A085','#8E44AD','#E67E22','#C0392B'].map((c,i)=>`<div style="width:64px;height:${60+i*42}px;background:${c};border-radius:14px"></div>`).join('')}</div>` },
  leitura: { nome: 'Lê Comigo', c1: '#7B2CBF', c2: '#E4572E', ac: '#FFD23F', bg: '#FBF3E8', site: 'egk-7d2294.lovable.app/le-comigo',
    logo: `<div style="display:flex;gap:12px;justify-content:center">${[['BA','#E4572E'],['BE','#17BEBB'],['BI','#7B2CBF']].map(([s,c])=>`<div class="b" style="width:120px;height:120px;background:${c};color:#fff;border-radius:22px;font-size:64px;display:flex;align-items:center;justify-content:center">${s}</div>`).join('')}</div>` },
};
const pecas = [];
for (const k of ['foco', 'leitura']) {
  const m = marca[k];
  pecas.push([`${k}-perfil.png`, 1080, 1080, `<div style="width:1080px;height:1080px;background:${m.bg};display:flex;flex-direction:column;align-items:center;justify-content:center;gap:40px">
    <div style="transform:scale(1.6)">${m.logo}</div><div class="b" style="font-size:118px;color:${m.c1};margin-top:60px">${m.nome}</div></div>`]);
  const pags = k === 'foco' ? ['foco-capa.png', 'foco-6.png', 'foco-55.png', 'foco-155.png', 'foco-205.png'] : ['le-capa1.png', 'le-capa2.png', 'le-capa3.png', 'le-p3.png', 'le-txt.png'];
  const sub = k === 'foco' ? '250 atividades de atenção, memória e autocontrole para imprimir · 5 a 12 anos' : 'Kit de leitura em casa: da sílaba à frase, em 15 minutos por dia · 4 a 8 anos';
  pecas.push([`${k}-capa-facebook.png`, 1640, 624, `<div style="width:1640px;height:624px;background:linear-gradient(120deg,${m.c1},${m.c2});position:relative;color:#fff">
    <div style="position:absolute;left:120px;top:140px;width:640px"><div class="b" style="font-size:96px">${m.nome}</div><div style="font-family:N8;font-size:34px;margin-top:18px;line-height:1.3">${sub}</div>
    <div style="display:inline-block;margin-top:28px;background:${m.ac};color:#1f2a37;font-family:N8;font-size:28px;padding:12px 26px;border-radius:99px">Teste grátis de 1 minuto no link</div></div>
    ${pags.slice(0, 3).map((p, i) => `<img class="pg" src="${img(p)}" style="position:absolute;right:${60 + i * 150}px;top:${70 + (i % 2) * 40}px;height:440px;transform:rotate(${[-6, 3, -2][i]}deg)">`).join('')}</div>`]);
  const posts = k === 'foco' ? [
    ['O que é a Trilha do Foco', '250 atividades em 5 etapas:', ['Sustentar · ficar na tarefa até o fim', 'Selecionar · achar o que importa', 'Guardar · lembrar das instruções', 'Planejar · pensar antes de fazer', 'Controlar · parar, pensar e agir'], 'foco-capa.png'],
    ['3 jeitos de treinar o foco em 10 minutos', '', ['1 atividade por dia, sempre no mesmo horário', 'Celular longe da mesa durante a atividade', 'Elogie a calma, não a velocidade'], 'foco-6.png'],
    ['Por dentro: labirinto, sudoku de formas e setas trocadas', 'Cada etapa começa fácil e vai subindo de nível.', [], 'foco-155.png'],
    ['Seu filho começa tudo e não termina nada?', 'Faça o teste de 1 minuto e veja qual habilidade de foco ele mais precisa treinar.', ['Grátis · resultado na hora', 'Não é diagnóstico'], 'foco-205.png'],
  ] : [
    ['O que é o Lê Comigo', '3 apostilas, 198 fichas para imprimir:', ['Sílabas simples · 16 famílias, do B ao Z', 'Sílabas complexas · NH, LH, CH, RR, BR...', 'Frases e fluência · frases e textos curtos'], 'le-capa1.png'],
    ['Leitura em casa em 4 passos', '', ['Sente junto, 15 minutos por dia', 'Aponte com o dedo embaixo da sílaba', 'Leia junto quando travar e peça para repetir', 'Comemore cada palavra lida sozinho'], 'le-p6.png'],
    ['Por dentro: família do B', 'Leia, complete, ligue, caça-palavras, separe as sílabas e ditado.', [], 'le-p3.png'],
    ['Em que fase da leitura seu filho está?', 'Responda 8 perguntas e descubra em 1 minuto, com o plano para começar hoje.', ['Grátis · resultado na hora'], 'le-txt.png'],
  ];
  posts.forEach(([t, s, li, p], i) => pecas.push([`${k}-post-${i + 1}.png`, 1080, 1350, `<div style="width:1080px;height:1350px;background:${m.bg};padding:70px 70px 0;position:relative;overflow:hidden">
    <div style="display:flex;align-items:center;gap:16px;margin-bottom:34px"><div style="transform:scale(.38);transform-origin:left center;width:120px;height:70px">${m.logo}</div><div class="b" style="font-size:40px;color:${m.c1};margin-left:60px">${m.nome}</div></div>
    <div class="b" style="font-size:80px;color:${m.c1}">${t}</div>
    ${s ? `<div style="font-family:N8;font-size:36px;color:#33404d;margin-top:22px;line-height:1.3">${s}</div>` : ''}
    ${li.length ? `<div style="margin-top:26px">${li.map(x => `<div style="font-family:N8;font-size:${li.length > 3 ? 32 : 36}px;color:#1f2a37;background:#fff;border-left:12px solid ${m.c2};border-radius:12px;padding:14px 22px;margin:12px 0;width:${li.length > 3 ? 600 : 940}px">${x}</div>`).join('')}</div>` : ''}
    <img class="pg" src="${img(p)}" style="position:absolute;right:60px;bottom:-${li.length > 3 ? 160 : (li.length ? 260 : 40)}px;width:${li.length > 3 ? 360 : 560}px;transform:rotate(-4deg)">
    </div>`]));
}
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage();
  for (const [n, w, h, html] of pecas) {
    await pg.setViewportSize({ width: w, height: h });
    const f=path.join(OUT,'_tmp.html');fs.writeFileSync(f,`<html><head><meta charset=utf-8><style>${css}</style></head><body>${html}</body></html>`);await pg.goto('file://'+f);await pg.waitForTimeout(500);
    await pg.screenshot({ path: path.join(OUT, n) });
  }
  await b.close(); console.log(pecas.length, 'peças');
})();
