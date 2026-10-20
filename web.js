// Signature interactions. Data comes only from window.PAGE (generated from data/eras/*.json).
(function(){const P=window.PAGE,root=document.getElementById('viz');if(!P||!root)return;
const AR=P.lang==='ar',NS='http://www.w3.org/2000/svg';
const fy=y=>y>=2026?(AR?'اليوم':'present'):y<0?(AR?(-y)+' ق.م':(-y)+' BCE'):(AR?y+' م':y+' CE');
const el=(t,a={},p)=>{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e};
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const all=P.eras.concat(P.ctx);const a=P.a,b=P.mode==='era'?P.b:Math.max(P.b,...P.eras.map(e=>Math.min(e.b,P.b+50)));
const W=Math.max(340,Math.min(940,root.clientWidth||900));const X=y=>{const t=(y-a)/(b-a)*(W-20)+10;return AR?W-t:t};
function scrubber(onv){const d=document.createElement('div');d.className='scrub';const lo=Math.max(a,P.a),hi=Math.min(b,P.b);
 d.innerHTML=`<label for="yr">${P.t.year}</label><input id="yr" type="range" min="${lo}" max="${hi}" value="${Math.round((lo+hi)/2)}" step="1"><output aria-live="polite"></output>`;
 root.prepend(d);const i=d.querySelector('input'),o=d.querySelector('output');const up=()=>{o.textContent=fy(+i.value);onv(+i.value)};i.addEventListener('input',up);
 const h=new URLSearchParams(location.hash.slice(1)).get('y');if(h!=null&&!isNaN(+h))i.value=+h;
 i.addEventListener('change',()=>history.replaceState(null,'','#y='+i.value));up();return i}
function link(e){return (AR?'/ar':'')+'/eras/'+e.id+'/'}
function axis(svg,y0){[a,(a+b)/2,b].forEach((y,k)=>{const t=el('text',{x:X(y),y:y0,'font-size':13,fill:'#6b6257','text-anchor':k==0?(AR?'end':'start'):k==2?(AR?'start':'end'):'middle'},svg);t.textContent=fy(Math.round(y))})}
function lanes(list,withScrub){const streams=[...new Set(list.map(e=>e.s))];const rows=[];list.forEach(e=>{let r=rows.findIndex(R=>R.s===e.s&&R.end<=e.a);if(r<0){rows.push({s:e.s,end:e.b});r=rows.length-1}else rows[r].end=e.b;e._r=r});
 const H=rows.length*34+40;const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':list.map(e=>e.n).join(', ')});root.appendChild(svg);
 const line=el('line',{y1:0,y2:H-24,stroke:P.col,'stroke-width':2},svg);
 const bars=list.map(e=>{const g=el('a',{href:link(e)},svg);const x1=X(Math.max(e.a,a)),x2=X(Math.min(e.b,b));const r=el('rect',{x:Math.min(x1,x2),y:e._r*34+4,width:Math.max(3,Math.abs(x2-x1)),height:28,rx:3,fill:P.col,class:'bar'},g);
  el('title',{},r).textContent=e.n+' · '+fy(e.a)+' – '+fy(e.b);const t=el('text',{x:Math.min(x1,x2)+6*(AR?-1:1)+(AR?Math.abs(x2-x1):0),y:e._r*34+23,'font-size':14,fill:'#fff','pointer-events':'none'},g);t.textContent=e.n;
  const cp=el('clipPath',{id:'c'+e.id},svg);el('rect',{x:Math.min(x1,x2),y:0,width:Math.abs(x2-x1),height:H},cp);t.setAttribute('clip-path','url(#c'+e.id+')');return [e,r]});
 axis(svg,H-6);
 if(withScrub){const tip=document.createElement('p');tip.className='tip';tip.setAttribute('aria-live','polite');root.appendChild(tip);
  scrubber(y=>{line.setAttribute('x1',X(y));line.setAttribute('x2',X(y));const on=bars.filter(([e,r])=>{const k=e.a<=y&&e.b>=y;r.setAttribute('opacity',k?1:.25);return k});
   tip.innerHTML=on.length?on.map(([e])=>`<a href="${link(e)}">${esc(e.n)}</a>`).join(' · '):'—'})}}
function duration(){const list=P.eras.slice().sort((x,y)=>(y.b-y.a)-(x.b-x.a));const mx=Math.max(...list.map(e=>e.b-e.a));const H=list.length*36+10;
 const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img'});root.appendChild(svg);const tip=document.createElement('p');tip.className='tip';tip.setAttribute('aria-live','polite');root.appendChild(tip);
 list.forEach((e,i)=>{const w=(e.b-e.a)/mx*(W-20);const g=el('g',{tabindex:0,class:'bar',role:'button','aria-label':e.n},svg);const r=el('rect',{x:AR?W-10-w:10,y:i*36+4,width:w,height:30,rx:3,fill:P.col,opacity:.85},g);
  const t=el('text',{x:AR?W-16:16,y:i*36+24,'font-size':14,fill:w>300?'#fff':P.col,'text-anchor':'start'},g);if(w<=300)t.setAttribute('x',AR?W-20-w:20+w);t.textContent=e.n+' — '+(e.b-e.a).toLocaleString(AR?'ar':'en')+(AR?' سنة':' yrs');
  const pick=()=>{svg.querySelectorAll('rect').forEach(x=>x.setAttribute('opacity',.35));r.setAttribute('opacity',1);
   const others=list.filter(o=>o!==e).map(o=>`${esc(o.n)}: ×${((e.b-e.a)/(o.b-o.a)).toFixed(1)}`).join(' · ');tip.innerHTML=`<a href="${link(e)}"><b>${esc(e.n)}</b></a> ${fy(e.a)} – ${fy(e.b)}<br><small>${others}</small>`};
  g.addEventListener('click',pick);g.addEventListener('keydown',ev=>{if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();pick()}})})}
function load(src){return new Promise((ok,no)=>{const s=document.createElement('script');s.src=src;s.onload=ok;s.onerror=no;document.head.appendChild(s)})}
async function map(){const box=document.createElement('div');box.textContent='…';root.appendChild(box);
 await load('/lib/d3.min.js');await load('/lib/topojson.min.js');const topo=await (await fetch('/data/countries-50m.json')).json();box.remove();
 const obj=topo.objects.countries||topo.objects[Object.keys(topo.objects)[0]];const land=topojson.feature(topo,obj);
 const Wm=600,Hm=560,pr=d3.geoMercator().center([33,16]).scale(950).translate([Wm/2,Hm/2]),path=d3.geoPath(pr);
 const svg=d3.select(root).append('svg').style('max-width','620px').style('margin','0 auto').attr('viewBox',`0 0 ${Wm} ${Hm}`).attr('role','img').style('background','#dfe9ee');
 svg.append('g').selectAll('path').data(land.features).join('path').attr('d',path).attr('fill',d=>['729','728'].includes(String(d.id))?'#efe0c6':'#f4efe6').attr('stroke','#b9ad99').attr('stroke-width',.6);
 const pts=[];all.forEach(e=>(e.caps||[]).forEach(c=>{if(c.lat!=null)pts.push({e,c,main:P.eras.includes(e)})}));
 const g=svg.append('g');const tip=document.createElement('p');tip.className='tip';tip.setAttribute('aria-live','polite');root.appendChild(tip);
 const draw=y=>{const on=pts.filter(p=>p.e.a<=y&&p.e.b>=y);const s=g.selectAll('g.p').data(on,p=>p.e.id+p.c.name);s.exit().transition().duration(250).style('opacity',0).remove();
  const n=s.enter().append('g').attr('class','p').style('opacity',0);n.append('circle').attr('r',d=>d.main?7:4).attr('fill',d=>d.main?P.col:'#8a8a8a').attr('stroke','#fff');
  n.append('text').attr('dx',AR?-10:10).attr('dy',4).attr('text-anchor',AR?'end':'start').attr('font-size',d=>d.main?15:11).attr('paint-order','stroke').attr('stroke','#fff').attr('stroke-width',3).text(d=>d.c.name);
  n.merge(s).attr('transform',d=>`translate(${pr([d.c.lon,d.c.lat])})`).transition().duration(250).style('opacity',1);
  const es=[...new Set(on.map(p=>p.e))];tip.innerHTML=es.map(e=>`<a href="${link(e)}" style="color:${P.eras.includes(e)?P.col:'#6b6257'}">${esc(e.n)}</a>`).join(' · ')||'—'};
 const s=scrubber(draw)}
function neighbors(){const tip=document.createElement('div');root.appendChild(tip);scrubber(y=>{const on=all.filter(e=>e.a<=y&&e.b>=y);const by={};on.forEach(e=>(by[e.sl]=by[e.sl]||[]).push(e));
 tip.innerHTML='<ul class="eras">'+Object.keys(by).map(k=>`<li><a href="${link(by[k][0])}" style="${P.eras.includes(by[k][0])?'':'border-color:#b9ad99'}"><small>${esc(k)}</small>${by[k].map(e=>'<b>'+esc(e.n)+'</b>').join('<br>')}</a></li>`).join('')+'</ul>'})}
function sources(){const ls=[...new Set(P.eras.flatMap(e=>e.langs))];const tbl=document.createElement('div');tbl.className='tw';
 tbl.innerHTML='<table><thead><tr><th></th><th>#</th>'+ls.map(l=>`<th>${esc(l)}</th>`).join('')+'<th>⇄</th></tr></thead><tbody>'+P.eras.map(e=>`<tr><td><a href="${link(e)}">${esc(e.n)}</a></td><td>${e.nsrc}</td>`+ls.map(l=>`<td>${e.langs.includes(l)?'<span style="display:inline-block;width:14px;height:14px;border-radius:50%;background:'+P.col+'" aria-label="'+l+'"></span>':''}</td>`).join('')+`<td>${e.comp.map(c=>`<span class="st st-${esc(c.status)}">${esc(c.lang)}</span>`).join(' ')||'<span class="gap">—</span>'}</td></tr>`).join('')+'</tbody></table>';root.appendChild(tbl)}
const M=P.mode;try{if(M==='duration')duration();else if(M==='map')map();else if(M==='lanes')lanes(P.eras,true);else if(M==='neighbors')neighbors();else if(M==='sources')sources();else if(M==='era')(P.eras[0].caps.length?map():null)}catch(err){root.textContent=''}
})();
