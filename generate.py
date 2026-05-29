import json

data = json.load(open('distilled.json'))
data_js = json.dumps(data, ensure_ascii=False)

TEMPLATE = r'''<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<title>Valkompass 2026 – neutral & anonym</title>
<style>
  :root{
    --bg:#f4f5f7; --surface:#ffffff; --surface-2:#fafbfc;
    --ink:#16181d; --muted:#646b78; --faint:#9aa1ad;
    --border:#e6e8ec; --border-strong:#d6d9df;
    --accent:#3f6275; --accent-soft:#e8eef1; --accent-ink:#2c4756;
    --pos:#4f7a63; --neg:#8a5b5b; --neutral:#8a8f99;
    --radius:18px; --radius-sm:12px;
    --shadow:0 1px 2px rgba(16,20,30,.04), 0 8px 30px rgba(16,20,30,.06);
    --maxw:680px;
    --font:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  }
  @media (prefers-color-scheme: dark){
    :root{
      --bg:#0e1014; --surface:#171a20; --surface-2:#1c2027;
      --ink:#eef0f3; --muted:#9aa2af; --faint:#6b7280;
      --border:#262b33; --border-strong:#323844;
      --accent:#7fa7ba; --accent-soft:#1d2933; --accent-ink:#bcd4df;
      --pos:#7cae93; --neg:#c08e8e; --neutral:#878d98;
      --shadow:0 1px 2px rgba(0,0,0,.3), 0 10px 34px rgba(0,0,0,.4);
    }
  }
  *{box-sizing:border-box}
  html,body{margin:0;padding:0}
  body{
    background:var(--bg); color:var(--ink); font-family:var(--font);
    line-height:1.5; -webkit-font-smoothing:antialiased;
    padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left);
  }
  .wrap{max-width:var(--maxw); margin:0 auto; padding:20px 18px 64px}
  .screen{animation:fade .35s ease}
  @keyframes fade{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
  h1{font-size:30px; line-height:1.15; letter-spacing:-.02em; margin:0 0 10px; font-weight:740}
  h2{font-size:21px; letter-spacing:-.01em; margin:0 0 6px; font-weight:680}
  p{margin:0 0 14px; color:var(--muted)}
  .lead{font-size:16.5px}
  .tag{display:inline-flex; align-items:center; gap:7px; font-size:12.5px; font-weight:600;
    color:var(--accent-ink); background:var(--accent-soft); padding:5px 11px; border-radius:999px; letter-spacing:.01em}
  .card{background:var(--surface); border:1px solid var(--border); border-radius:var(--radius);
    box-shadow:var(--shadow); padding:22px}
  .stack>*+*{margin-top:14px}

  /* buttons */
  button{font-family:inherit; cursor:pointer; border:none; background:none; color:inherit}
  .btn{display:inline-flex; align-items:center; justify-content:center; gap:9px;
    background:var(--accent); color:#fff; font-size:16px; font-weight:640;
    padding:15px 26px; border-radius:14px; width:100%; transition:transform .12s, filter .15s, opacity .15s}
  .btn:hover{filter:brightness(1.06)}
  .btn:active{transform:scale(.985)}
  .btn:disabled{opacity:.4; cursor:not-allowed}
  .btn.ghost{background:transparent; color:var(--accent-ink); border:1px solid var(--border-strong); box-shadow:none}
  .btn.subtle{background:var(--accent-soft); color:var(--accent-ink); box-shadow:none}
  .linkbtn{color:var(--muted); font-size:14px; font-weight:560; text-decoration:underline; text-underline-offset:3px}
  .linkbtn:hover{color:var(--ink)}
  .row{display:flex; gap:10px; align-items:center}

  /* progress */
  .topbar{display:flex; align-items:center; gap:12px; margin-bottom:18px}
  .crumbs{display:flex; gap:6px; flex:1}
  .crumb{height:6px; flex:1; border-radius:999px; background:var(--border); overflow:hidden}
  .crumb i{display:block; height:100%; width:0; background:var(--accent); border-radius:999px; transition:width .4s cubic-bezier(.4,0,.2,1)}
  .stepmeta{font-size:13px; color:var(--faint); font-weight:560; white-space:nowrap}

  /* fairness chips */
  .fair{list-style:none; margin:18px 0 0; padding:0; display:grid; gap:10px}
  .fair li{display:flex; gap:12px; align-items:flex-start; font-size:14.5px; color:var(--ink)}
  .fair .ic{flex:none; width:30px; height:30px; border-radius:9px; background:var(--accent-soft);
    color:var(--accent-ink); display:grid; place-items:center; font-size:15px}
  .fair b{font-weight:640}
  .fair span{color:var(--muted)}

  /* statement card */
  .qtag{font-size:12.5px; font-weight:640; color:var(--accent-ink); text-transform:uppercase; letter-spacing:.05em}
  .qtext{font-size:23px; line-height:1.28; letter-spacing:-.01em; font-weight:660; margin:10px 0 4px; min-height:2.2em}
  .qnote{font-size:13px; color:var(--faint); margin-bottom:18px}
  .likert{display:grid; gap:9px}
  .lk{display:flex; align-items:center; gap:13px; width:100%; text-align:left;
    background:var(--surface-2); border:1.5px solid var(--border); border-radius:13px; padding:13px 15px;
    font-size:15.5px; font-weight:560; transition:border-color .12s, background .12s, transform .1s}
  .lk:hover{border-color:var(--border-strong)}
  .lk:active{transform:scale(.99)}
  .lk .dot{flex:none; width:18px; height:18px; border-radius:50%; border:2px solid var(--border-strong); transition:.12s}
  .lk[data-v="2"] .dot,.lk[data-v="1"] .dot{border-color:var(--pos)}
  .lk[data-v="-2"] .dot,.lk[data-v="-1"] .dot{border-color:var(--neg)}
  .lk.sel{border-color:var(--accent); background:var(--accent-soft)}
  .lk.sel .dot{background:var(--accent); border-color:var(--accent); box-shadow:inset 0 0 0 3px var(--surface)}
  .qfoot{display:flex; align-items:center; justify-content:space-between; margin-top:18px; gap:10px}
  .star{display:inline-flex; align-items:center; gap:8px; font-size:14px; font-weight:580; color:var(--muted);
    border:1.5px solid var(--border); border-radius:11px; padding:9px 13px; transition:.12s}
  .star.on{color:var(--accent-ink); border-color:var(--accent); background:var(--accent-soft)}
  .star svg{width:16px;height:16px}

  /* budget / priorities */
  .meter{display:flex; align-items:baseline; gap:8px; margin:2px 0 4px}
  .meter b{font-size:15px}
  .area{border:1px solid var(--border); border-radius:14px; padding:14px 15px; background:var(--surface-2)}
  .area+.area{margin-top:11px}
  .area h3{margin:0; font-size:16px; font-weight:640; letter-spacing:-.01em}
  .area p{margin:3px 0 11px; font-size:13px}
  .step{display:flex; align-items:center; gap:12px}
  .step .pm{flex:none; width:42px; height:42px; border-radius:12px; border:1.5px solid var(--border);
    background:var(--surface); color:var(--accent-ink); font-size:24px; line-height:1; font-weight:500;
    display:grid; place-items:center; transition:.12s}
  .step .pm:hover:not(:disabled){border-color:var(--accent); background:var(--accent-soft)}
  .step .pm:active:not(:disabled){transform:scale(.92)}
  .step .pm:disabled{opacity:.28; cursor:not-allowed}
  .step .val{flex:1; display:flex; flex-direction:column; align-items:center; gap:6px}
  .coins{display:flex; gap:5px}
  .coins i{width:13px; height:13px; border-radius:50%; background:var(--border); transition:background .15s, transform .15s}
  .coins i.f{background:var(--accent); transform:scale(1.06)}
  .step .lvl{font-size:12.5px; font-weight:620; color:var(--muted); letter-spacing:.01em}
  .area.funded{border-color:var(--accent); background:var(--accent-soft)}
  .budgetbar{position:sticky; bottom:10px; margin-top:18px; background:var(--surface); border:1px solid var(--border-strong);
    border-radius:14px; padding:13px 16px; box-shadow:var(--shadow); display:flex; align-items:center; gap:14px}
  .budgetbar .fill{flex:1; height:9px; border-radius:999px; background:var(--border); overflow:hidden}
  .budgetbar .fill i{display:block; height:100%; background:var(--accent); width:0; transition:width .3s}
  .budgetbar small{color:var(--muted); font-size:12.5px; white-space:nowrap; font-weight:560}
  .budgetbar small b{color:var(--ink); font-weight:740; font-variant-numeric:tabular-nums}
  .budgetbar.empty .fill i{background:var(--pos)}
  .budgetbar.empty small b{color:var(--pos)}

  /* results */
  .res{margin-top:14px}
  .pcard{border:1px solid var(--border); border-radius:14px; background:var(--surface); overflow:hidden; transition:border-color .15s}
  .pcard+.pcard{margin-top:11px}
  .pcard.top{border-color:var(--accent); box-shadow:0 0 0 3px var(--accent-soft)}
  .phead{display:flex; align-items:center; gap:14px; padding:15px 16px; width:100%; text-align:left}
  .chip{flex:none; width:46px; height:46px; border-radius:12px; display:grid; place-items:center;
    background:var(--surface-2); border:1px solid var(--border-strong); font-weight:720; font-size:15px; letter-spacing:-.02em; color:var(--ink)}
  .pmain{flex:1; min-width:0}
  .pname{font-size:15.5px; font-weight:650; display:flex; align-items:center; gap:8px}
  .rank{font-size:12px; color:var(--faint); font-weight:600}
  .pbar{height:7px; border-radius:999px; background:var(--border); overflow:hidden; margin-top:7px}
  .pbar i{display:block; height:100%; background:var(--accent); width:0; border-radius:999px; transition:width .8s cubic-bezier(.3,0,.2,1)}
  .pct{flex:none; font-size:19px; font-weight:740; letter-spacing:-.02em; min-width:48px; text-align:right}
  .chev{flex:none; color:var(--faint); transition:transform .2s}
  .pcard.open .chev{transform:rotate(180deg)}
  .pdetail{display:none; padding:2px 16px 18px; border-top:1px solid var(--border)}
  .pcard.open .pdetail{display:block; animation:fade .25s}
  .pdetail h4{margin:14px 0 7px; font-size:12.5px; text-transform:uppercase; letter-spacing:.05em; color:var(--faint); font-weight:680}
  .stmtline{display:flex; gap:9px; align-items:flex-start; font-size:13.5px; padding:5px 0; color:var(--ink)}
  .stmtline .m{flex:none; width:18px; height:18px; border-radius:6px; display:grid; place-items:center; font-size:12px; font-weight:800; margin-top:1px}
  .m.agree{background:rgba(79,122,99,.16); color:var(--pos)}
  .m.disagree{background:rgba(138,91,91,.16); color:var(--neg)}
  .m.mid{background:var(--border); color:var(--muted)}
  .taglist{display:flex; flex-wrap:wrap; gap:6px}
  .mini{font-size:12px; font-weight:580; padding:4px 10px; border-radius:999px; background:var(--surface-2); border:1px solid var(--border); color:var(--muted)}
  .cov{font-size:12px; color:var(--faint); margin-top:2px}
  .src a{color:var(--accent-ink); font-size:12.5px; text-decoration:underline; text-underline-offset:2px; display:block; margin-top:4px}
  .disclaim{font-size:12.5px; color:var(--faint); margin-top:18px; line-height:1.5}

  details.method{margin-top:16px; border:1px solid var(--border); border-radius:14px; background:var(--surface); overflow:hidden}
  details.method summary{cursor:pointer; padding:14px 16px; font-weight:620; font-size:14.5px; list-style:none; display:flex; justify-content:space-between; align-items:center}
  details.method summary::-webkit-details-marker{display:none}
  details.method[open] summary{border-bottom:1px solid var(--border)}
  details.method .body{padding:14px 16px; font-size:13.5px; color:var(--muted)}
  details.method .body p{font-size:13.5px}
  details.method .body b{color:var(--ink)}
  .foot{text-align:center; margin-top:26px; font-size:12px; color:var(--faint)}
  .hide{display:none!important}
</style>
</head>
<body>
<div class="wrap" id="app"></div>

<script>
const DATA = /*__DATA__*/;
const app = document.getElementById('app');

// ---------- helpers ----------
const $ = (h)=>{const t=document.createElement('template');t.innerHTML=h.trim();return t.content.firstChild;};
const esc = (s)=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
// session-seeded shuffle so statement order varies per visit
let SEED = (performance.now()*1000|0) ^ (window.history.length*7919) ^ (screen.width*31);
function rnd(){SEED=(SEED*1103515245+12345)&0x7fffffff;return SEED/0x7fffffff;}
function shuf(a){a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(rnd()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}

const QUESTIONS = DATA.questions;
const LIKERT_POOL = QUESTIONS.filter(q=>q.fmt==='likert');
const CHOOSE_POOL = QUESTIONS.filter(q=>q.fmt==='choose');
const AREAS = DATA.areas;
const PARTIES = DATA.parties;
const ORDER = DATA.party_order;
const FULL = DATA.party_full;
const ROUND_LIKERT = Math.min(10, LIKERT_POOL.length);
const ROUND_CHOOSE = Math.min(5, CHOOSE_POOL.length);

// state. answers[qid] = {u:-1..1, imp:bool}  (samma skala för båda format)
const state = { qs:[], i:0, answers:{}, prio:{} };
function sampleRound(){
  // lotta fram en omgång: påståenden först (steg 1), välj-alternativ sedan (steg 2)
  state.qs = shuf(LIKERT_POOL).slice(0,ROUND_LIKERT).concat(shuf(CHOOSE_POOL).slice(0,ROUND_CHOOSE));
  state.i=0; state.answers={}; state.prio={};
}

// ---------- SCREENS ----------
function start(){
  app.innerHTML='';
  const s=$(`<div class="screen"></div>`);
  s.innerHTML=`
    <div style="text-align:center; margin:18px 0 22px">
      <span class="tag">Anonym · neutral · källbaserad</span>
    </div>
    <div class="card stack">
      <h1>Vilket parti delar dina värderingar?</h1>
      <p class="lead">En valkompass byggd för att hitta <b>ditt</b> parti – inte för att putta dig mot något. Inga partinamn, färger eller logotyper syns medan du svarar. Du ser resultatet först på slutet.</p>
      <p style="font-size:14px;margin-top:-4px">Varje omgång lottar fram <b>${ROUND_LIKERT+ROUND_CHOOSE} frågor</b> ur en bank på ${QUESTIONS.length} – först påståenden, sedan välj‑alternativ där du avslutar meningen, och till sist budgetspelet. Kör om för nya frågor.</p>
      <button class="btn" id="go">Starta &nbsp;→</button>
      <div style="text-align:center"><button class="linkbtn" id="how">Hur räknas det ut?</button></div>
    </div>
    <ul class="fair">
      <li><span class="ic">⬚</span><span><b>Helt anonymt.</b> Partierna är dolda tills du är klar – du kan inte vinklas.</span></li>
      <li><span class="ic">=</span><span><b>Inget straffas på okänt.</b> Saknar ett parti tydlig position i källan räknas frågan varken för eller emot det.</span></li>
      <li><span class="ic">⤬</span><span><b>Slumpad ordning, neutralt språk.</b> Ingen fråga är ställd för att leda dig.</span></li>
      <li><span class="ic">◷</span><span><b>Källbaserat.</b> Allt bygger på partiernas eget publicerade 2026-material.</span></li>
    </ul>
    <p class="foot">Underlag: ${esc(DATA.meta.title)} · hämtat ${esc(DATA.meta.retrieved)}</p>`;
  app.appendChild(s);
  s.querySelector('#go').onclick=()=>{sampleRound();ask();};
  s.querySelector('#how').onclick=()=>methodScreen();
}

function topbar(stepFrac,label){
  return `<div class="topbar">
    <div class="crumbs">
      <div class="crumb"><i style="width:${Math.min(100,stepFrac[0]*100)}%"></i></div>
      <div class="crumb"><i style="width:${Math.min(100,stepFrac[1]*100)}%"></i></div>
      <div class="crumb"><i style="width:${Math.min(100,stepFrac[2]*100)}%"></i></div>
    </div>
    <div class="stepmeta">${label}</div>
  </div>`;
}

const LIKERT_OPTS=[
  {u:1,   t:'Instämmer helt'},
  {u:0.5, t:'Instämmer delvis'},
  {u:0,   t:'Neutral / vet ej'},
  {u:-0.5,t:'Tar delvis avstånd'},
  {u:-1,  t:'Tar helt avstånd'},
];
const STAR=`<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.5l2.9 6.1 6.6.8-4.9 4.5 1.3 6.6L12 17.9 6.1 21l1.3-6.6L2.5 9.9l6.6-.8z"/></svg>`;

// gemensam fot (extra viktigt + tillbaka) och hoppa-över
function qFoot(q){
  const cur=state.answers[q.id];
  return `<div class="qfoot">
      <button class="star ${cur&&cur.imp?'on':''}" id="imp">${STAR} Extra viktigt för mig</button>
      ${state.i>0?`<button class="linkbtn" id="back">← Tillbaka</button>`:`<span></span>`}
    </div>`;
}
function wireFoot(s,q,advance){
  const imp=s.querySelector('#imp');
  imp.onclick=()=>{const c=state.answers[q.id]||{u:0,imp:false};c.imp=!c.imp;state.answers[q.id]=c;imp.classList.toggle('on',c.imp);};
  const bk=s.querySelector('#back'); if(bk) bk.onclick=()=>{state.i--;ask();};
  s.querySelector('#skip').onclick=()=>{if(!state.answers[q.id])state.answers[q.id]={u:0,imp:false};state.i++;ask();};
}
function commit(q,u,el,all){
  const imp=(state.answers[q.id]&&state.answers[q.id].imp)||false;
  state.answers[q.id]={u,imp};
  all.forEach(x=>x.classList.toggle('sel',x===el));
  setTimeout(()=>{state.i++;ask();},170);
}

function ask(){
  if(state.i>=state.qs.length) return priorities();
  const q=state.qs[state.i];
  const inChoose=state.i>=ROUND_LIKERT;
  const stepLabel=inChoose
    ? `Välj alternativ ${state.i-ROUND_LIKERT+1} / ${ROUND_CHOOSE}`
    : `Påstående ${state.i+1} / ${ROUND_LIKERT}`;
  const frac=[Math.min(state.i,ROUND_LIKERT)/ROUND_LIKERT, Math.max(0,state.i-ROUND_LIKERT)/ROUND_CHOOSE, 0];
  app.innerHTML='';
  const s=$(`<div class="screen"></div>`);
  if(q.fmt==='likert'){
    const cur=state.answers[q.id];
    s.innerHTML=`
      ${topbar(frac,stepLabel)}
      <div class="card">
        <div class="qtag">Steg 1 · Påstående</div>
        <div class="qtext">${esc(q.text)}</div>
        <div class="likert">
          ${LIKERT_OPTS.map(l=>`<button class="lk ${cur&&cur.u===l.u?'sel':''}" data-u="${l.u}"><span class="dot"></span>${l.t}</button>`).join('')}
        </div>
        ${qFoot(q)}
      </div>
      <div style="text-align:center;margin-top:16px"><button class="linkbtn" id="skip">Hoppa över →</button></div>`;
    app.appendChild(s);
    const all=[...s.querySelectorAll('.lk')];
    all.forEach(b=>b.onclick=()=>commit(q,+b.dataset.u,b,all));
  }else{
    const cur=state.answers[q.id];
    s.innerHTML=`
      ${topbar(frac,stepLabel)}
      <div class="card">
        <div class="qtag">Steg 2 · Välj det som passar dig bäst</div>
        <div class="qtext">${esc(q.text)}</div>
        <div class="likert">
          ${q.options.map((o,k)=>`<button class="lk opt ${cur&&cur.u===o.val?'sel':''}" data-u="${o.val}"><span class="dot"></span>${esc(o.label)}</button>`).join('')}
        </div>
        ${qFoot(q)}
      </div>
      <div style="text-align:center;margin-top:16px"><button class="linkbtn" id="skip">Ingen åsikt / hoppa över →</button></div>`;
    app.appendChild(s);
    const all=[...s.querySelectorAll('.lk')];
    all.forEach(b=>b.onclick=()=>commit(q,+b.dataset.u,b,all));
  }
  wireFoot(s,q);
}

const BUDGET=20;            // fasta budgetpoäng att fördela
const MAXLVL=3;             // max per område
const LVLNAME=['Inte prioriterat','Lite','Mycket','Mest'];
function priorities(){
  app.innerHTML='';
  const s=$(`<div class="screen"></div>`);
  s.innerHTML=`
    ${topbar([1,1,0],'Budgetspelet')}
    <div class="card stack" style="margin-bottom:16px">
      <h2>💰 Du är finansminister</h2>
      <p>Du har <b>${BUDGET} budgetpoäng</b> att fördela – och inte en poäng mer. Lägg dem på det som betyder mest för dig. Vill du satsa mer på ett område måste du <b>dra ner på ett annat</b>. Det du lämnar på noll räknas inte.</p>
    </div>
    <div id="areas"></div>
    <div class="budgetbar">
      <div class="fill"><i id="bfill"></i></div>
      <small id="bnote"></small>
    </div>
    <div style="margin-top:16px"><button class="btn" id="result" disabled>Visa min matchning &nbsp;→</button></div>
    <div style="text-align:center;margin-top:12px"><button class="linkbtn" id="back2">← Tillbaka till frågorna</button></div>`;
  app.appendChild(s);
  const host=s.querySelector('#areas');
  const used=()=>AREAS.reduce((sum,a)=>sum+(state.prio[a.id]||0),0);
  const rows=[];
  AREAS.forEach(a=>{
    const el=$(`<div class="area">
      <h3>${esc(a.label)}</h3>
      <p>${esc(a.desc||'')}</p>
      <div class="step">
        <button class="pm minus" aria-label="Minska">−</button>
        <div class="val">
          <span class="coins">${Array.from({length:MAXLVL},(_,i)=>`<i data-i="${i}"></i>`).join('')}</span>
          <span class="lvl"></span>
        </div>
        <button class="pm plus" aria-label="Öka">+</button>
      </div>
    </div>`);
    const minus=el.querySelector('.minus'), plus=el.querySelector('.plus');
    minus.onclick=()=>{const c=state.prio[a.id]||0; if(c>0){state.prio[a.id]=c-1; refresh();}};
    plus.onclick =()=>{const c=state.prio[a.id]||0; if(c<MAXLVL && used()<BUDGET){state.prio[a.id]=c+1; refresh();}};
    host.appendChild(el);
    rows.push({a,el,minus,plus});
  });
  function refresh(){
    const u=used(), remaining=BUDGET-u, full=remaining<=0;
    rows.forEach(({a,el,minus,plus})=>{
      const c=state.prio[a.id]||0;
      el.classList.toggle('funded',c>0);
      el.querySelectorAll('.coins i').forEach(d=>d.classList.toggle('f',(+d.dataset.i)<c));
      el.querySelector('.lvl').textContent=LVLNAME[c];
      minus.disabled=c<=0;
      plus.disabled=c>=MAXLVL || full;
    });
    s.querySelector('#bfill').style.width=(100*u/BUDGET)+'%';
    s.querySelector('.budgetbar').classList.toggle('empty',full);
    s.querySelector('#bnote').innerHTML= full
      ? `<b>0</b> poäng kvar · budgeten är fördelad`
      : `<b>${remaining}</b> av ${BUDGET} poäng kvar`;
    s.querySelector('#result').disabled = u===0;
  }
  refresh();
  s.querySelector('#result').onclick=()=>results();
  s.querySelector('#back2').onclick=()=>{state.i=state.qs.length-1;ask();};
}

// ---------- SCORING ----------
// läsbar mening för resultatlistan; för välj-alternativ visas partiets ståndpunkt
function readable(q,p){
  if(q.fmt==='likert') return q.text;
  let best=q.options[0];
  q.options.forEach(o=>{ if(Math.abs(o.val-p)<Math.abs(best.val-p)) best=o; });
  const lbl=best.label;
  return q.text.includes('…') ? q.text.replace('…', lbl) : q.text+' → '+lbl;
}
function computeStatement(pid){
  let wsum=0, asum=0, cov=0, agree=[], disagree=[], mid=[];
  state.qs.forEach(q=>{
    const ans=state.answers[q.id];
    const p=q.positions[pid];
    if(!ans||ans.u===0) return;          // user neutral/skip -> ignore
    if(p===null||p===undefined) return;  // party unknown -> excluded (no penalty)
    cov++;
    const ag=1-Math.abs(ans.u-p)/2;      // 0..1
    const w=ans.imp?2:1;
    wsum+=w; asum+=ag*w;
    const rec={text:readable(q,p), ag};
    if(ag>=0.75) agree.push(rec); else if(ag<=0.25) disagree.push(rec); else mid.push(rec);
  });
  return {score: wsum? asum/wsum : null, cov, agree, disagree, mid};
}
function computePriority(pid){
  let dot=0, nu=0, np=0; const shared=[];
  AREAS.forEach(a=>{
    const u=state.prio[a.id]||0;
    const pe=a.parties[pid]? a.parties[pid].weight : 0;
    dot+=u*pe; nu+=u*u; np+=pe*pe;
    if(u>0 && pe>0) shared.push({label:a.label, u, pe, summary:a.parties[pid]?a.parties[pid].summary:''});
  });
  const score = (nu>0 && np>0)? dot/(Math.sqrt(nu)*Math.sqrt(np)) : null;
  shared.sort((x,y)=>(y.u*y.pe)-(x.u*x.pe));
  return {score, shared};
}

function results(){
  const anyStmt=Object.values(state.answers).some(a=>a.v!==0);
  const anyPrio=Object.values(state.prio).some(v=>v>0);
  const rows=ORDER.map(pid=>{
    const s1=computeStatement(pid);
    const s2=computePriority(pid);
    let parts=[], weights=[];
    if(s1.score!==null){parts.push(s1.score);weights.push(0.5*Math.min(1,s1.cov/4)+0.2);} // confidence scales with coverage
    if(s2.score!==null){parts.push(s2.score);weights.push(0.5);}
    let overall=null;
    if(parts.length){let ws=weights.reduce((a,b)=>a+b,0);overall=parts.reduce((a,p,i)=>a+p*weights[i],0)/ws;}
    return {pid, s1, s2, overall};
  }).filter(r=>r.overall!==null)
    .sort((a,b)=>b.overall-a.overall);

  app.innerHTML='';
  const s=$(`<div class="screen"></div>`);
  s.innerHTML=`
    ${topbar([1,1,1],'Ditt resultat')}
    <div class="card stack" style="margin-bottom:6px">
      <span class="tag">Klart!</span>
      <h1>Så ligger du till</h1>
      <p>Listan visar hur väl partiernas publicerade 2026-material stämmer med dina svar. <b>Det är en samstämmighet – inte en rekommendation.</b> Tryck på ett parti för att se exakt varför.</p>
    </div>
    <div class="res" id="res"></div>
    <p class="disclaim" id="disc"></p>
    <details class="method"><summary>Hur räknades detta ut? <span>▾</span></summary>
      <div class="body" id="mbody"></div></details>
    <div style="margin-top:18px"><button class="btn ghost" id="redo">↺ Gör om testet</button></div>
    <p class="foot">Underlag: ${esc(DATA.meta.title)} · ${esc(DATA.meta.retrieved)}</p>`;
  app.appendChild(s);

  const host=s.querySelector('#res');
  rows.forEach((r,i)=>{
    const pct=Math.round(r.overall*100);
    const card=$(`<div class="pcard ${i===0?'top':''}">
      <button class="phead">
        <span class="chip">${esc(r.pid)}</span>
        <span class="pmain">
          <span class="pname">${esc(FULL[r.pid]||r.pid)} ${i===0?'<span class="rank">Närmast dig</span>':''}</span>
          <span class="pbar"><i style="width:0%"></i></span>
        </span>
        <span class="pct">${pct}%</span>
        <span class="chev"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M6 9l6 6 6-6"/></svg></span>
      </button>
      <div class="pdetail"></div>
    </div>`);
    host.appendChild(card);
    setTimeout(()=>{card.querySelector('.pbar i').style.width=pct+'%';},60+i*40);
    const det=card.querySelector('.pdetail');
    det.innerHTML=detailHTML(r);
    card.querySelector('.phead').onclick=()=>{
      const open=card.classList.contains('open');
      host.querySelectorAll('.pcard').forEach(c=>c.classList.remove('open'));
      if(!open) card.classList.add('open');
    };
  });

  // disclaimer about excluded parties / coverage
  const excluded=ORDER.length-rows.length;
  s.querySelector('#disc').innerHTML=
    `Matchningen bygger på de frågor och områden där varje parti har en tydlig position i källan. `+
    (excluded>0?`${excluded} parti(er) hade för lite underlag mot dina svar för att rankas. `:``)+
    `Källan är en ögonblicksbild och inte en fullständig redovisning av all politik.`;

  s.querySelector('#mbody').innerHTML=methodHTML();
  s.querySelector('#redo').onclick=()=>{ start(); window.scrollTo(0,0); };
  window.scrollTo(0,0);
}

function detailHTML(r){
  const a=r.s1, p=r.s2;
  let h='';
  h+=`<h4>Sakfrågor</h4>`;
  if(a.score===null){h+=`<div class="cov">Partiet hade ingen tydlig position i källan på de frågor du tog ställning till.</div>`;}
  else{
    h+=`<div class="cov">Samstämmighet ${Math.round(a.score*100)}% · baserat på ${a.cov} fråg${a.cov===1?'a':'or'} där partiet har en tydlig position.</div>`;
    a.agree.slice(0,6).forEach(x=>h+=`<div class="stmtline"><span class="m agree">✓</span><span>${esc(x.text)}</span></div>`);
    a.disagree.slice(0,6).forEach(x=>h+=`<div class="stmtline"><span class="m disagree">✕</span><span>${esc(x.text)}</span></div>`);
    a.mid.slice(0,3).forEach(x=>h+=`<div class="stmtline"><span class="m mid">~</span><span>${esc(x.text)}</span></div>`);
  }
  h+=`<h4>Gemensamma prioriteringar</h4>`;
  if(!p.shared.length){h+=`<div class="cov">Inga av dina prioriterade områden låg bland partiets tyngsta i 2026-materialet.</div>`;}
  else{
    h+=`<div class="taglist">`+p.shared.slice(0,8).map(x=>`<span class="mini">${esc(x.label)}</span>`).join('')+`</div>`;
    const topShared=p.shared[0];
    if(topShared&&topShared.summary) h+=`<div class="cov" style="margin-top:8px">”${esc(topShared.summary)}”</div>`;
  }
  // sources
  const party=PARTIES.find(x=>x.id===r.pid);
  if(party&&party.sources&&party.sources.length){
    h+=`<h4>Källor</h4><div class="src">`+
      party.sources.filter(s=>s.url).slice(0,3).map(s=>`<a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.title||s.url)} ↗</a>`).join('')+`</div>`;
  }
  return h;
}

function methodHTML(){
  return `
  <p><b>Slumpat urval.</b> Varje omgång lottar fram ${ROUND_LIKERT} påståenden och ${ROUND_CHOOSE} välj-alternativ ur en bank på ${QUESTIONS.length} frågor. Kör du om får du nya frågor – men matchningen bygger på samma metod.</p>
  <p><b>Två likväga delar.</b> Dina svar jämförs med partiernas eget publicerade 2026-material på två sätt:</p>
  <p>1. <b>Frågor.</b> För varje fråga du svarat på mäts hur nära ditt svar ligger partiets position. “Extra viktigt” väger dubbelt. Frågor där partiet saknar tydlig position i källan räknas <b>inte alls</b> – varken för eller emot.</p>
  <p>2. <b>Prioriteringar.</b> Du fördelar en <b>fast budget</b> – mer på ett område kräver mindre på ett annat. Din fördelning jämförs med vilka områden partiet faktiskt lyfte tyngst i sitt 2026-material (mycket hög / hög / medel prioritet) via riktningslikhet.</p>
  <p><b>Hur positionerna är satta:</b> varje partis ståndpunkt är kodad direkt ur formuleringar i partiets eget material – inte ur tyckande. Där materialet är tyst lämnas positionen blank och påverkar inte matchningen.</p>
  <p><b>Neutralitet:</b> frågorna visas i slumpad ordning, med neutralt språk, och alla partier presenteras likadant i gråskala – medvetet utan blockfärger. Procenten är ett mått på överensstämmelse, inte ett betyg eller en rekommendation.</p>
  <p><b>Begränsning:</b> ${esc(DATA.meta.limitations[0])}</p>`;
}

function methodScreen(){
  app.innerHTML='';
  const s=$(`<div class="screen"></div>`);
  s.innerHTML=`
    <div class="card stack">
      <span class="tag">Metod & neutralitet</span>
      <h1>Hur räknas det ut?</h1>
      <div style="color:var(--muted)">${methodHTML()}</div>
      <button class="btn" id="b">← Tillbaka</button>
    </div>`;
  app.appendChild(s);
  s.querySelector('#b').onclick=start;
  window.scrollTo(0,0);
}

start();
</script>
</body>
</html>'''

html = TEMPLATE.replace('/*__DATA__*/', data_js)
open('index.html','w').write(html)
print('wrote index.html', len(html), 'bytes')
