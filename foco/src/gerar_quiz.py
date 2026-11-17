# -*- coding: utf-8 -*-
"""Gera as 3 páginas de quiz gamificado (Lovable public/). Uso: python3 src/gerar_quiz.py
Checkout: preencha CHECKOUT abaixo quando os produtos existirem na Cakto."""
import os, json, re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(RAIZ, "out", "lovable")
PIXEL = "1579712183467308"

CHECKOUT = {
    "foco": "https://pay.cakto.com.br/3eg6aa2",
    "leitura": "https://pay.cakto.com.br/apih4oo",
    "biblico": "https://pay.cakto.com.br/nwy8sx8_1326449",
    "biblico_1": "https://pay.cakto.com.br/v6xmhrk_1326452",
}

CSS = """
:root{--p:%(p)s;--p2:%(p2)s;--ac:%(ac)s;--bg:%(bg)s;--txt:#1f2a37;--cinza:#5b6876}
*{box-sizing:border-box}body{margin:0;font-family:Nunito,system-ui,sans-serif;color:var(--txt);background:var(--bg);line-height:1.5;font-size:17px}
h1,h2,h3{font-family:'Baloo 2',system-ui,sans-serif;line-height:1.1;margin:0 0 10px;color:var(--p)}
img{max-width:100%%;display:block}
.w{max-width:560px;margin:0 auto;padding:0 16px}
.top{background:var(--p);color:#fff;text-align:center;font-weight:800;font-size:13px;padding:8px 12px}
.card{background:#fff;border-radius:18px;box-shadow:0 6px 24px rgba(0,0,0,.07);padding:22px 18px;margin:16px 0}
.hero{text-align:center;padding:18px 0 4px}
.hero h1{font-size:31px}.hero p{color:var(--cinza);margin:0 0 14px}
.tag{display:inline-block;background:var(--ac);color:#1f2a37;font-weight:800;font-size:13px;border-radius:99px;padding:4px 12px;margin-bottom:10px}
.btn{display:block;width:100%%;text-align:center;background:var(--p2);color:#fff;font-weight:800;font-size:19px;border:0;border-radius:14px;padding:17px 14px;cursor:pointer;text-decoration:none;box-shadow:0 5px 0 rgba(0,0,0,.18);font-family:inherit}
.btn:active{transform:translateY(3px);box-shadow:0 2px 0 rgba(0,0,0,.18)}
.btn.alt{background:#fff;color:var(--p);border:2px solid var(--p);box-shadow:none;font-size:16px;padding:13px}
.mini{font-size:13px;color:var(--cinza);text-align:center;margin-top:8px}
.prog{height:10px;background:#e6e9ee;border-radius:99px;overflow:hidden;margin:14px 0 6px}.prog i{display:block;height:100%%;background:var(--p2);width:0;transition:width .35s}
.pnum{font-size:13px;color:var(--cinza);font-weight:700}
.q h2{font-size:25px;margin:8px 0 14px}
.q img{border-radius:12px;margin:0 auto 14px;max-height:220px}
.op{display:flex;align-items:center;gap:12px;width:100%%;text-align:left;background:#fff;border:2px solid #e3e7ed;border-radius:14px;padding:14px;margin:9px 0;font-size:17px;font-weight:700;color:var(--txt);cursor:pointer;font-family:inherit}
.op:hover{border-color:var(--p)}.op.sel{border-color:var(--p2);background:#f3fbf6}
.op b{font-size:22px;width:30px;text-align:center}
.load{text-align:center;padding:40px 0}
.spin{width:64px;height:64px;border:7px solid #e3e7ed;border-top-color:var(--p2);border-radius:50%%;margin:0 auto 18px;animation:s 1s linear infinite}@keyframes s{to{transform:rotate(360deg)}}
.steps div{opacity:.25;font-weight:700;margin:6px 0;transition:opacity .3s}.steps div.on{opacity:1}
.bar{margin:10px 0}.bar span{display:flex;justify-content:space-between;font-weight:800;font-size:15px}
.bar em{display:block;height:12px;border-radius:99px;background:#e6e9ee;overflow:hidden;margin-top:4px}.bar em i{display:block;height:100%%;border-radius:99px}
.lock{position:relative;margin-top:14px}.lock .blur{filter:blur(6px);user-select:none;pointer-events:none}
.lock .over{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;background:linear-gradient(180deg,rgba(255,255,255,.2),rgba(255,255,255,.92) 45%%);padding:16px;border-radius:14px}
.over strong{font-family:'Baloo 2';font-size:21px;color:var(--p)}
.preco{text-align:center;margin:12px 0}.preco .v{font-family:'Baloo 2';font-size:56px;color:var(--p2);line-height:1}.preco small{display:block;color:var(--cinza);font-weight:700}
.list{padding:0;margin:10px 0;list-style:none}.list li{padding:7px 0 7px 30px;position:relative}.list li:before{content:'✔';position:absolute;left:4px;color:var(--p2);font-weight:800}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin:12px 0}.grid img{border-radius:8px;border:1px solid #e3e7ed}
.gar{display:flex;gap:12px;align-items:center;background:#fff8e1;border-radius:14px;padding:14px;font-size:15px}
.gar b{font-size:34px}
.faq details{background:#fff;border-radius:12px;padding:12px 14px;margin:8px 0}.faq summary{font-weight:800;cursor:pointer}
.aviso{font-size:12.5px;color:var(--cinza);text-align:center;margin:18px 0 90px}
.sticky{position:fixed;left:0;right:0;bottom:0;background:#fff;box-shadow:0 -4px 18px rgba(0,0,0,.12);padding:10px 14px;display:block;z-index:9}
.quiz-pad{height:70px}
.sticky .w{display:flex;gap:10px;align-items:center;padding:0}.sticky div{flex:1;font-weight:800;font-size:14px;line-height:1.2}.sticky b{display:block;font-family:'Baloo 2';font-size:22px;color:var(--p2)}
.sticky a{background:var(--p2);color:#fff;text-decoration:none;font-weight:800;border-radius:12px;padding:13px 16px}
.hide{display:none}
"""

JS = r"""
var C=__CFG__;var R={},i=0,area={};
function $(s){return document.querySelector(s)}
function track(n,d){try{fbq('trackCustom',n,d||{})}catch(e){}}
function show(id){['#ini','#quiz','#load','#res'].forEach(function(s){$(s).classList.add('hide')});$(id).classList.remove('hide');window.scrollTo(0,0)}
function start(){track('QuizStart',{quiz:C.id});show('#quiz');render()}
function render(){var q=C.qs[i];$('#prog').style.width=(i/C.qs.length*100)+'%';$('#pnum').textContent='Pergunta '+(i+1)+' de '+C.qs.length;
var h='<h2>'+q.t+'</h2>'+(q.img?'<img src="'+q.img+'" alt="">':'');
q.o.forEach(function(o,k){h+='<button class="op" onclick="pick('+k+',this)"><b>'+o[0]+'</b><span>'+o[1]+'</span></button>'});$('#qbox').innerHTML=h}
function pick(k,el){el.classList.add('sel');var q=C.qs[i];R[q.id]=k;if(q.a){area[q.a]=(area[q.a]||0)+k}
setTimeout(function(){i++;if(i<C.qs.length)render();else carregar()},260)}
function carregar(){show('#load');track('QuizComplete',{quiz:C.id});var d=$('#steps').children,n=0;
var t=setInterval(function(){if(n<d.length){d[n].classList.add('on');n++}else{clearInterval(t);resultado()}},850)}
function addq(u){var q=location.search.slice(1);return q?u+(u.indexOf('?')>-1?'&':'?')+q:u}
function resultado(){var r=window.RESULT(R,area);$('#rtit').innerHTML=r.tit;$('#rsub').innerHTML=r.sub;$('#rbars').innerHTML=r.bars||'';
$('#rlivre').innerHTML=r.livre;var m=r.lock.match(/^(<h3>[\s\S]*?<\/h3>\s*<p>[\s\S]*?<\/p>)([\s\S]*)$/);if(m){$('#rlivre').innerHTML+='<div style="background:#f3fbf6;border-radius:12px;padding:12px 14px;margin-top:10px">'+m[1]+'</div>';$('#rlock').innerHTML=m[2];}else{$('#rlock').innerHTML=r.lock;}show('#res');
try{fbq('track','ViewContent',{content_name:C.produto,value:C.valor,currency:'BRL'})}catch(e){}}
document.addEventListener('DOMContentLoaded',function(){document.querySelectorAll('a.ck').forEach(function(a){a.href=addq(a.getAttribute('data-u'))})});
function bar(nome,v,max,cor){var p=Math.max(8,Math.round(v/max*100));return '<div class="bar"><span>'+nome+'<small>'+p+'%</small></span><em><i style="width:'+p+'%;background:'+cor+'"></i></em></div>'}
"""

PAGE = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s</title><meta name="description" content="%(desc)s">
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@700;800&family=Nunito:wght@400;700;800&display=swap" rel="stylesheet">
<script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init','%(pixel)s');fbq('track','PageView');</script>
<style>%(css)s</style></head><body>
<div class="top">%(topo)s</div>
<div class="w">
<section id="ini" class="hero">
<span class="tag">%(tag)s</span>
<h1>%(h1)s</h1><p>%(sub)s</p>
<img src="%(heroimg)s" alt="" style="border-radius:16px;margin:0 auto 16px;max-height:300px;box-shadow:0 6px 22px rgba(0,0,0,.12)">
<button class="btn" onclick="start()">%(cta)s</button>
<div class="mini">%(mini)s</div>
<a class="btn alt ck" style="margin-top:12px" data-u="%(ck)s" href="%(ck)s">Já quero o kit: %(preco)s</a>
<div class="mini">Pix ou cartão · chega no e-mail em 2 minutos · garantia de 7 dias</div>
</section>
<section id="quiz" class="hide"><div class="prog"><i id="prog"></i></div><div class="pnum" id="pnum"></div><div class="card q" id="qbox"></div></section>
<section id="load" class="hide load"><div class="spin"></div><h2>%(loadtit)s</h2><div class="steps" id="steps">%(steps)s</div></section>
<section id="res" class="hide">
<div class="card"><span class="tag">%(restag)s</span><h2 id="rtit"></h2><p id="rsub" style="color:var(--cinza);margin-top:0"></p><div id="rbars"></div><div id="rlivre"></div>
<div class="lock"><div class="blur" id="rlock"></div><div class="over"><strong>%(locktit)s</strong><p style="margin:6px 0 12px">%(locktxt)s</p><a class="btn ck" data-u="%(ck)s" href="%(ck)s">%(lockbtn)s</a></div></div></div>
<div class="card" id="oferta"><h2 style="text-align:center">%(oftit)s</h2>
<img src="%(ofimg)s" alt="" style="border-radius:12px;margin:8px auto">
<ul class="list">%(itens)s</ul>
<div class="grid">%(grid)s</div>
<div class="preco"><small>%(precoantes)s</small><div class="v">%(preco)s</div><small>%(precodepois)s</small></div>
<a class="btn ck" data-u="%(ck)s" href="%(ck)s">%(btn)s</a>
%(extra)s
<div class="mini">Pagamento único · Pix ou cartão · chega no e-mail em 2 minutos · garantia de 7 dias</div></div>
<div class="gar"><b>7</b><div><strong>Garantia de 7 dias.</strong> Se não gostar, pede o reembolso dentro de 7 dias e recebe 100%% de volta.</div></div>
<div class="faq" style="margin-top:14px">%(faq)s</div>
<p class="aviso">%(aviso)s</p>
<div class="quiz-pad"></div></section>
</div>
<div class="sticky"><div class="w"><div>%(stxt)s<b>%(preco)s</b></div><a class="ck" data-u="%(ck)s" href="%(ck)s">%(sbtn)s</a></div></div>
<script>%(js)s</script>
<script>window.RESULT=%(result)s;</script>
<script src="https://api.cakto.com.br/api/product/checkout/tracker.js" async></script>
</body></html>"""


LP = {
    "trilha-do-foco.html": {"topo": "Pagamento único · chega no e-mail em 2 minutos", "sub": "250 atividades de atenção e calma para imprimir, em 5 etapas e 3 níveis, de 5 a 12 anos. 15 minutos por dia, longe da tela."},
    "plano-biblico.html": {"topo": "Pagamento único · chega no e-mail em 2 minutos", "sub": "500 atividades bíblicas para imprimir + 5 músicas, de 5 a 11 anos. Uma atividade por dia troca a tela pelas histórias da Bíblia."},
}


def pagina(nome, cores, cfg, d):
    d = dict(d)
    d["css"] = CSS % cores
    d["js"] = JS.replace("__CFG__", json.dumps(cfg, ensure_ascii=False))
    d["pixel"] = PIXEL
    d["steps"] = "".join("<div>%s</div>" % s for s in d.pop("steps_l"))
    d["itens"] = "".join("<li>%s</li>" % s for s in d.pop("itens_l"))
    d["grid"] = "".join('<img src="%s" alt="">' % s for s in d.pop("grid_l"))
    d["faq"] = "".join("<details><summary>%s</summary><p>%s</p></details>" % qa for qa in d.pop("faq_l"))
    d.setdefault("extra", "")
    with open(os.path.join(OUT, nome), "w") as f: f.write(PAGE % d)
    lp = LP.get(nome)
    if lp:
        h = PAGE % dict(d, topo=lp["topo"], sub=lp["sub"], mini="Pix ou cartão · chega no e-mail em 2 minutos · garantia de 7 dias")
        h = h.replace('<button class="btn" onclick="start()">%s</button>' % d["cta"], '<a class="btn ck" data-u="%s" href="%s">Quero o kit por %s</a>' % (d["ck"], d["ck"], d["preco"]), 1)
        h = re.sub(r'<a class="btn alt ck" style="margin-top:12px".*?</a>\s*<div class="mini">.*?</div>', '<a class="btn alt" style="margin-top:12px" href="#oferta">Ver o que vem no kit ↓</a>', h, count=1, flags=re.S)
        h = h.replace('<section id="res" class="hide">\n<div class="card">', '<section id="res">\n<div class="card" style="display:none">', 1)
        h = h.replace('</body>', "<script>try{fbq('track','ViewContent',{content_name:%s,currency:'BRL'})}catch(e){}</script></body>" % json.dumps(d["title"], ensure_ascii=False), 1)
        with open(os.path.join(OUT, nome.replace(".html", "-lp.html")), "w") as f: f.write(h)


FAQ_COMUM = [("Como recebo?", "Logo após o pagamento, o link de acesso chega no seu e-mail. É só baixar o PDF e imprimir em papel A4 comum."),
             ("Preciso de impressora colorida?", "Não. Tudo foi feito em preto e branco para gastar pouca tinta."),
             ("É assinatura?", "Não. Pagamento único, acesso para sempre.")]

# ------------------------------------------------------------------ FOCO
foco_cfg = {"id": "foco", "produto": "Trilha do Foco 250", "valor": 19.90, "qs": [
    {"id": "licao", "a": "sus", "t": "Na hora da lição de casa, ele(a)...", "img": "/foco/foco-p5.jpg", "o": [["😊", "Faz sozinho até o fim"], ["🙂", "Precisa ser lembrado algumas vezes"], ["😕", "Levanta toda hora e não termina"], ["😩", "Só faz com você sentado do lado"]]},
    {"id": "tres", "a": "mem", "t": "Quando você pede 3 coisas seguidas (\"guarda o tênis, lava a mão e vem jantar\")...", "o": [["✅", "Faz as três"], ["🤏", "Esquece uma"], ["1️⃣", "Faz só a primeira"], ["🌀", "Nem começa, se distrai no caminho"]]},
    {"id": "ruido", "a": "sel", "t": "Com TV ligada ou barulho por perto, ele(a) consegue se concentrar?", "o": [["🎯", "Consegue sim"], ["🙂", "Às vezes se distrai"], ["😕", "Perde o foco fácil"], ["😩", "É impossível"]]},
    {"id": "nao", "a": "con", "t": "Quando perde um jogo ou ouve um \"não\"...", "img": "/foco/foco-p206.jpg", "o": [["😌", "Aceita bem"], ["😒", "Reclama, mas passa"], ["😭", "Chora ou grita"], ["🌋", "Explode e demora a se acalmar"]]},
    {"id": "comeco", "a": "pla", "t": "Para começar uma tarefa (arrumar o quarto, a mochila)...", "o": [["🚀", "Começa sozinho"], ["⏳", "Enrola um pouco"], ["🧩", "Precisa de ajuda para organizar"], ["❓", "Não sabe por onde começar"]]},
]}
foco_result = r"""function(R,A){
var ar=[['sus','Atenção sustentada','Sustentar',1,'#2E6FD8',3],['sel','Atenção seletiva','Selecionar',2,'#16A085',3],['mem','Memória de trabalho','Guardar',3,'#8E44AD',3],['pla','Planejamento','Planejar',4,'#E67E22',3],['con','Autocontrole','Controlar',5,'#C0392B',3]];
var pior=ar[0],b='';ar.forEach(function(a){var v=A[a[0]]||0;var forca=a[5]-v;b+=bar(a[1],forca,a[5],a[4]);if(v/a[5]>(A[pior[0]]||0)/pior[5])pior=a});
var tot=0;ar.forEach(function(a){tot+=(A[a[0]]||0)});
var nivel=tot<=4?'leve':tot<=9?'moderado':'alto';
return {tit:'Perfil de atenção: desafio '+nivel,
sub:'Pelas suas respostas, a habilidade que mais pede treino agora é <b>'+pior[1].toLowerCase()+'</b>. As barras mostram o quanto cada habilidade já está forte.',
bars:b,
livre:'<p><b>O que isso quer dizer:</b> dificuldade de foco não é falta de vontade. Atenção, memória e autocontrole são habilidades, e habilidade se treina, um degrau de cada vez, começando pelo que está mais fraco. Trocar 15 minutos de tela por 1 atividade no papel por dia já é um bom começo.</p><p><b>Ponto de partida recomendado:</b> Etapa '+pior[3]+' · '+pior[2]+'.</p>',
lock:'<h3>Seu plano de 4 semanas</h3><p>Semana 1: Etapa '+pior[3]+', níveis 1 e 2, 1 atividade por dia de 10 minutos.</p><p>Semana 2: Etapa 1 e Etapa '+pior[3]+' intercaladas, nível 2.</p><p>Semana 3: Etapas 3 e 4, nível 2 e 3, com o quadro de rotina.</p><p>Semana 4: Etapa 5 (autocontrole) e revisão do mapa da trilha.</p><p>As 250 atividades, na ordem certa para este perfil.</p>'};}"""

pagina("trilha-do-foco.html", {"p": "#123B7A", "p2": "#16A34A", "ac": "#F2B705", "bg": "#F3F6FB"}, foco_cfg, {
    "title": "Teste rápido: perfil de atenção do seu filho · Trilha do Foco",
    "desc": "Responda 5 perguntas e veja qual habilidade de foco seu filho mais precisa treinar, com plano de atividades para imprimir.",
    "topo": "Teste gratuito · 1 minuto · resultado na hora",
    "tag": "Para pais de crianças de 5 a 12 anos",
    "h1": "Seu filho não termina nada que começa?",
    "sub": "Responda 5 perguntas rápidas e descubra qual habilidade de foco ele mais precisa treinar agora, e por onde começar.",
    "heroimg": "/foco/foco-p1.jpg", "cta": "Começar o teste →", "mini": "Não é diagnóstico. É um retrato da rotina, a partir das suas respostas.",
    "loadtit": "Montando o perfil...", "steps_l": ["✔ Analisando atenção na lição", "✔ Analisando memória e instruções", "✔ Analisando autocontrole", "✔ Escolhendo o ponto de partida"],
    "restag": "Seu resultado", "locktit": "Plano de 4 semanas bloqueado", "locktxt": "O plano completo e as 250 atividades na ordem certa estão na Trilha do Foco.", "lockbtn": "Desbloquear meu plano",
    "ck": CHECKOUT["foco"],
    "oftit": "Trilha do Foco: 250 atividades para treinar atenção, memória e autocontrole",
    "ofimg": "/foco/foco-p4.jpg",
    "itens_l": ["250 atividades para imprimir, de 5 a 12 anos", "5 etapas: sustentar, selecionar, guardar, planejar e controlar", "3 níveis em cada etapa: começa fácil e vai subindo", "Labirintos, caça ao símbolo, sudoku de formas, setas trocadas, sinal verde/vermelho, pare-pense-faça e mais", "Mapa da trilha para pintar o progresso + certificado", "Gabarito e guia de 1 página para os pais"],
    "grid_l": ["/foco/foco-p5.jpg", "/foco/foco-p55.jpg", "/foco/foco-p104.jpg", "/foco/foco-p154.jpg", "/foco/foco-p156.jpg", "/foco/foco-p205.jpg"],
    "precoantes": "250 atividades por", "preco": "R$ 12,90", "precodepois": "cerca de R$ 0,05 por atividade · pagamento único",
    "btn": "Quero a Trilha do Foco",
    "extra": '<p class="mini" style="margin-top:12px">No checkout você pode incluir a <b>Rotina Visual e Quadro de Combinados</b> (cartões de rotina, quadro de estrelas e termômetro da calma).</p>',
    "faq_l": FAQ_COMUM + [("Serve para criança com TDAH?", "Serve para qualquer criança que precisa treinar foco, com ou sem diagnóstico. É material educativo de apoio: não é tratamento e não substitui o acompanhamento profissional."), ("Quanto tempo por dia?", "10 a 15 minutos, 1 ou 2 atividades. Pouco e todo dia funciona melhor.")],
    "aviso": "Este teste não é diagnóstico e não substitui avaliação de médico, psicólogo ou psicopedagogo. O resultado é um retrato da rotina a partir das suas respostas.",
    "stxt": "Trilha do Foco · 250 atividades", "sbtn": "Quero", "result": foco_result,
})

# ------------------------------------------------------------------ LEITURA
leit_cfg = {"id": "leitura", "produto": "Le Comigo", "valor": 19.90, "qs": [
    {"id": "letras", "a": "f", "t": "Ela reconhece as letras do alfabeto?", "o": [["🔤", "Todas"], ["🙂", "A maioria"], ["🤏", "Algumas"], ["❓", "Poucas ou nenhuma"]]},
    {"id": "bola", "a": "f", "t": "Mostrando a palavra BOLA, ela...", "img": "/leitura/leitura-p3.jpg", "o": [["📖", "Lê sozinha: \"bola\""], ["🐢", "Lê devagar, sílaba por sílaba"], ["🔡", "Fala as letras, mas não junta"], ["🙈", "Não tenta ler"]]},
    {"id": "escrita", "a": "f", "t": "Pedindo para escrever GATO, ela escreve...", "o": [["✍️", "GATO"], ["✏️", "GTO ou GAO (falta letra)"], ["🔠", "Letras soltas, sem relação com o som"], ["🖍️", "Desenha ou rabisca"]]},
    {"id": "frase", "a": "f", "t": "Uma frase curta, como \"O GATO BEBE LEITE\"...", "o": [["😃", "Lê e entende"], ["🐢", "Lê bem devagar, sem entender direito"], ["😕", "Lê só algumas palavras"], ["🙈", "Ainda não lê frases"]]},
]}
leit_result = r"""function(R,A){var f=A.f||0;var fases=[
['Fase 4 · Lendo frases','Lê palavras e começa a ler frases. Agora o treino é de fluência: ler sem parar no meio e entender o que leu.','Apostila 3 · Frases e fluência','Apostila 2 nas sílabas em que trava'],
['Fase 3 · Lendo palavras','Já junta as sílabas, mas ainda lê devagar e trava nas sílabas difíceis (NH, LH, CH, R, S).','Apostila 2 · Sílabas complexas','Apostila 3 a partir da semana 3'],
['Fase 2 · Juntando sílabas','Conhece letras e começa a entender que elas formam sílabas. É a hora certa das famílias silábicas.','Apostila 1 · Sílabas simples','Apostila 2 depois das 16 famílias'],
['Fase 1 · Descobrindo as letras','Ainda está conhecendo as letras e os sons. A leitura vai começar pelas sílabas mais simples, com muita repetição.','Apostila 1 · Sílabas simples, devagar','Fichas de leitura em voz alta todo dia']];
var k=f<=2?0:f<=5?1:f<=8?2:3;var z=fases[k];var pct=Math.max(8,Math.round((12-f)/12*100));
return {tit:z[0],sub:'Estimativa a partir das suas respostas. A professora pode confirmar a fase com uma sondagem.',
bars:bar('Caminho da leitura percorrido',pct,100,'#E4572E'),
livre:'<p>'+z[1]+'</p><p><b>Por onde começar:</b> '+z[2]+'.</p><p>Com 10 a 15 minutos por dia, uma ficha de cada vez, a criança avança uma família silábica a cada poucos dias.</p>',
lock:'<h3>Plano de 30 dias para a sua fase</h3><p>Semana 1: '+z[2]+', 1 ficha por dia.</p><p>Semana 2: continua, com ditado da família no fim da semana.</p><p>Semana 3: '+z[3]+'.</p><p>Semana 4: fichas relâmpago e leitura de frases em voz alta, com o recorde de palavras por minuto.</p>'};}"""

pagina("le-comigo.html", {"p": "#7B2CBF", "p2": "#16A34A", "ac": "#FFD23F", "bg": "#FBF7F2"}, leit_cfg, {
    "title": "Teste rápido: em que fase da leitura seu filho está? · Lê Comigo",
    "desc": "4 perguntas para descobrir a fase de leitura do seu filho e por onde começar em casa, com fichas para imprimir.",
    "topo": "Teste gratuito · 1 minuto · resultado na hora",
    "tag": "Para pais de crianças de 4 a 8 anos",
    "h1": "Seu filho ainda não está lendo?",
    "sub": "Descubra em 30 segundos em que fase da leitura ele está, e o que fazer em casa para ele começar a ler sozinho.",
    "heroimg": "/leitura/leitura-p3.jpg", "cta": "Descobrir a fase →", "mini": "4 perguntas. Funciona para crianças da educação infantil ao 2º ano.",
    "loadtit": "Calculando a fase...", "steps_l": ["✔ Letras e sons", "✔ Leitura de sílabas", "✔ Escrita", "✔ Frases e compreensão"],
    "restag": "Fase de leitura", "locktit": "Plano de 30 dias bloqueado", "locktxt": "O plano completo e as fichas para cada fase estão no kit Lê Comigo.", "lockbtn": "Desbloquear meu plano",
    "ck": CHECKOUT["leitura"],
    "oftit": "Lê Comigo: o kit para destravar a leitura em casa",
    "ofimg": "/leitura/leitura-p1.jpg",
    "itens_l": ["3 apostilas para imprimir, com 198 fichas progressivas", "Apostila 1: 16 famílias silábicas, do B ao Z", "Apostila 2: NH, LH, CH, QU, GU, RR, SS, Ç, BR, PL, sílabas com R, S, M e N no fim e ÃO", "Apostila 3: frases em 6 níveis, frases embaralhadas e textos curtos com perguntas", "Cada família tem: leitura, complete, ligue, caça-palavras, separar sílabas e ditado", "Feito para os pais aplicarem em 10 a 15 minutos por dia"],
    "grid_l": ["/leitura/leitura-p3.jpg", "/leitura/leitura-p4.jpg", "/leitura/leitura-p6.jpg", "/leitura/leitura2-p3.jpg", "/leitura/leitura3-p3.jpg", "/leitura/leitura3-p15.jpg"],
    "precoantes": "198 fichas por", "preco": "R$ 12,90", "precodepois": "cerca de R$ 0,07 por ficha · pagamento único",
    "btn": "Quero o kit Lê Comigo",
    "extra": '<p class="mini" style="margin-top:12px">No checkout você pode incluir as <b>Fichas Relâmpago</b>: 240 palavras para recortar e jogar o desafio de leitura de 1 minuto.</p>',
    "faq_l": FAQ_COMUM + [("Serve para professora?", "Serve. As fichas podem ser usadas em sala de aula e no reforço. Só não podem ser revendidas."), ("E se meu filho já lê um pouco?", "O teste mostra a fase dele. Você começa direto na apostila certa e pula o que ele já sabe.")],
    "aviso": "O resultado é uma estimativa a partir das suas respostas e não substitui a avaliação da escola.",
    "stxt": "Lê Comigo · 198 fichas", "sbtn": "Quero", "result": leit_result,
})

# ------------------------------------------------------------------ BÍBLICO (oferta atual remodelada)
bib_cfg = {"id": "biblico", "produto": "Colecao Atividades Biblicas 500", "valor": 27.90, "qs": [
    {"id": "gosta", "t": "O que ela mais gosta de fazer?", "img": "/colecao/t-caca.jpg", "o": [["🎨", "Pintar e desenhar"], ["🧩", "Desafios: labirinto, caça-palavras"], ["✍️", "Escrever e criar"], ["👂", "Ouvir histórias"]]},
    {"id": "conhece", "t": "Ela conhece as histórias da Bíblia?", "o": [["📖", "Conhece muitas"], ["🙂", "Conhece as principais"], ["🤏", "Conhece poucas"], ["🌱", "Está começando agora"]]},
    {"id": "tela", "t": "Quanto tempo de tela por dia?", "o": [["📵", "Menos de 1 hora"], ["📱", "1 a 2 horas"], ["📱📱", "2 a 4 horas"], ["🔋", "Mais de 4 horas"]]},
    {"id": "dias", "t": "Quantos dias de férias você quer preencher sem tela?", "img": "/colecao/t-codigo.jpg", "o": [["📅", "15 dias"], ["🗓️", "30 dias"], ["📆", "60 dias"], ["🎉", "As férias inteiras"]]},
]}
bib_result = r"""function(R,A){
var col=[['Coleção 3 · Parábolas de Jesus','Coleção 4 · Milagres e Amigos de Jesus'],['Coleção 1 · Heróis do Antigo Testamento','Coleção 4 · Milagres e Amigos de Jesus'],['Coleção 2 · A Vida de Jesus','Coleção 1 · Heróis do Antigo Testamento'],['Coleção 2 · A Vida de Jesus','Coleção 5 · Orações, Salmos e Valores']][R.conhece];
var tipos=[['pinte por número','copie e ilustre','labirinto'],['labirinto','caça-palavras','código secreto'],['acróstico','complete o versículo','palavras embaralhadas'],['verdadeiro ou falso','ligue as colunas','pinte por número']][R.gosta];
var dias=[15,30,60,75][R.dias];
var tela=['menos de 1 hora','1 a 2 horas','2 a 4 horas','mais de 4 horas'][R.tela];
return {tit:'Plano de '+dias+' dias com a Bíblia, sem tela',
sub:'Montado a partir das suas respostas.',
bars:'',
livre:'<p><b>Comece por:</b> '+col[0]+'.</p><p><b>Atividades preferidas para este perfil:</b> '+tipos.join(', ')+'.</p><p>Com '+tela+' de tela por dia hoje, trocar 20 minutos por 1 atividade no papel já muda a rotina. Com 2 atividades por dia, as 500 do pacote cobrem '+dias+' dias de férias e ainda sobram para o ano todo.</p>',
lock:'<h3>Calendário dia a dia</h3><p>Dias 1 a 10: '+col[0]+', histórias 1 a 10.</p><p>Dias 11 a 20: '+col[1]+'.</p><p>Dias 21 a 30: as outras coleções, com '+tipos[0]+' e '+tipos[1]+'.</p><p>Músicas de bônus para cantar juntos ao fim de cada semana.</p>'};}"""

pagina("plano-biblico.html", {"p": "#1F3A5F", "p2": "#16A34A", "ac": "#E9B44C", "bg": "#FFF8EA"}, bib_cfg, {
    "title": "Monte o plano de férias sem tela com a Bíblia · Estrela Guia Kids",
    "desc": "4 perguntas para montar o plano de férias do seu filho com atividades bíblicas para imprimir.",
    "topo": "Gratuito · 1 minuto · plano na hora",
    "tag": "Para crianças de 5 a 11 anos",
    "h1": "Férias chegando e seu filho só quer o celular?",
    "sub": "Responda 4 perguntas e receba um plano de férias sem tela, com as histórias da Bíblia certas para a idade dele.",
    "heroimg": "/colecao/pacote-500.jpg", "cta": "Montar o plano →", "mini": "Funciona em casa, no ministério infantil e na escola dominical.",
    "loadtit": "Montando o plano...", "steps_l": ["✔ Idade e preferências", "✔ Escolhendo as histórias", "✔ Escolhendo os tipos de atividade", "✔ Dividindo pelos dias de férias"],
    "restag": "Seu plano", "locktit": "Calendário completo bloqueado", "locktxt": "As 500 atividades para seguir o plano dia a dia estão no Pacote Completo.", "lockbtn": "Desbloquear o calendário",
    "ck": CHECKOUT["biblico"],
    "oftit": "Pacote Completo: 500 atividades bíblicas para imprimir + 5 músicas",
    "ofimg": "/colecao/pacote-500.jpg",
    "itens_l": ["5 coleções com 100 atividades cada, de 5 a 11 anos", "50 histórias da Bíblia, do Antigo Testamento a Jesus", "10 tipos de atividade: caça-palavras, labirinto, código secreto, pinte por número e mais", "Gabarito em todas as coleções", "Bônus: 5 músicas para cantar com as crianças"],
    "grid_l": ["/colecao/t-caca.jpg", "/colecao/t-codigo.jpg", "/colecao/t-complete.jpg", "/colecao/t-acrostico.jpg", "/colecao/capa-1.jpg", "/colecao/capa-2.jpg"],
    "precoantes": "500 atividades + 5 músicas por", "preco": "R$ 17,90", "precodepois": "pagamento único · menos de R$ 0,04 por atividade",
    "btn": "Quero o Pacote Completo",
    "extra": "",
    "faq_l": FAQ_COMUM + [("Posso usar na igreja?", "Pode. Uso pessoal, familiar, no ministério infantil e em sala de aula. Só não pode revender.")],
    "aviso": "Estrela Guia Kids · material para imprimir · uso pessoal e em sala de aula.",
    "stxt": "500 atividades + 5 músicas", "sbtn": "Quero", "result": bib_result,
})
print("ok")
