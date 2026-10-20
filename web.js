// Signature interactions. Data comes only from window.PAGE (generated from data/eras/*.json).
(function(){const P=window.PAGE,root=document.getElementById('viz');if(!P||!root)return;
const AR=P.lang==='ar',NS='http://www.w3.org/2000/svg';
const fy=y=>y>=2026?(AR?'اليوم':'present'):y<0?(AR?(-y)+' ق.م':(-y)+' BCE'):(AR?y+' م':y+' CE');
const el=(t,a={},p)=>{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e};
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const all=P.eras.concat(P.ctx);const a=P.a,b=P.mode==='era'?P.b:Math.max(P.b,...P.eras.map(e=>Math.min(e.b,P.b+50)));
const W=Math.max(340,Math.min(940,root.clientWidth||900));const X=y=>{const t=(y-a)/(b-a)*(W-20)+10;return AR?W-t:t};
function scrubber(onv){const d=document.createElement('div');d.className='scrub';const lo=Math.max(a,P.a),hi=Math.min(b,P.b);
 d.innerHTML=`<label for="yr">${P.t.year}</label><input id="yr" type="range" min="${lo}" max="${hi}" value="${Math.round((lo+hi)/2)}" step="1"><output aria-live="polite"></output><span class="steps">${[-100,-10,-1,1,10,100].map(v=>`<button type="button" data-s="${v}" aria-label="${v>0?'+':''}${v}">${v>0?'+':'−'}${Math.abs(v)}</button>`).join('')}</span>`;
 root.prepend(d);const i=d.querySelector('input'),o=d.querySelector('output');const up=()=>{o.textContent=fy(+i.value);onv(+i.value)};i.addEventListener('input',up);d.querySelectorAll('button').forEach(bt=>bt.addEventListener('click',()=>{i.value=Math.max(lo,Math.min(hi,+i.value+(+bt.dataset.s)));up();history.replaceState(null,'','#y='+i.value)}));
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
 const xg=svg.append('g');
 const X2=[];const PT=[];await Promise.all(P.eras.filter(e=>e.ext==='ok'||e.pts).map(async e=>{try{const g=await (await fetch('/extents/'+e.id+'.json')).json();g.features.forEach(f=>{if(!(f.properties&&f.properties.source))return;if(f.geometry.type==='Point'){PT.push({e,f});return}/* d3 uses spherical winding: GIS/RFC7946 rings may come inverted; rewind if area > hemisphere */const rw=r=>r.slice().reverse();const G=f.geometry;if(G.type==='Polygon'){if(d3.geoArea(f)>2*Math.PI)G.coordinates=G.coordinates.map(rw)}else if(G.type==='MultiPolygon'){G.coordinates=G.coordinates.map(p=>d3.geoArea({type:'Polygon',coordinates:p})>2*Math.PI?p.map(rw):p)}X2.push({e,f})})}catch(_){}}));
 const pts=[];all.forEach(e=>(e.caps||[]).forEach(c=>{if(c.lat!=null)pts.push({e,c,main:P.eras.includes(e)})}));
 const g=svg.append('g');const tip=document.createElement('p');tip.className='tip';tip.setAttribute('aria-live','polite');root.appendChild(tip);
 const short=s=>{s=String(s).split(/ [–—] /)[0];if(s.length>34)s=s.split(/[(（,،:]/)[0].trim();return s.length>40?s.slice(0,38)+'…':s};
 const full=o=>{const p=o.f.properties;return AR?(p.label_ar||p.label_en):(p.label_en||p.label_ar)};
 const dt=o=>{const p=o.f.properties;return (AR?(p.label_detail_ar||p.label_detail_en):(p.label_detail_en||p.label_detail_ar))||''};
 const drawX=y=>{const on=X2.filter(o=>{const a0=o.f.properties.start??o.e.a,b0=o.f.properties.end??o.e.b;return a0<=y&&(y<b0||(y===b0&&b0>=o.e.b))});/* half-open [start,end) so consecutive features don't double-draw at the boundary year */const s=xg.selectAll('g.x').data(on,o=>o.e.id+o.f.properties.citation+(o.f.properties.start??''));s.exit().remove();
  const n=s.enter().append('g').attr('class','x');n.append('path').attr('d',o=>path(o.f)).attr('fill',P.col).attr('fill-opacity',.16).attr('stroke',P.col).attr('stroke-opacity',.18).attr('stroke-width',10).attr('stroke-linejoin','round');
  n.append('path').attr('d',o=>path(o.f)).attr('fill','none').attr('stroke',P.col).attr('stroke-width',1.5).attr('stroke-dasharray','6 5').attr('stroke-opacity',.8);
  n.append('title').text(o=>[full(o),dt(o)].filter(Boolean).join('\n'));n.append('text').attr('transform',o=>{const q=o.f.properties.label_point;if(q&&q.length===2)return `translate(${pr(q)})`;const bb=path.bounds(o.f);return `translate(${(bb[0][0]+bb[1][0])/2},${bb[0][1]-8})`}).attr('dominant-baseline','middle').attr('text-anchor','middle').attr('font-size',12).attr('font-style','italic').attr('fill',P.col).attr('paint-order','stroke').attr('stroke','#fff').attr('stroke-width',3).text(o=>short(AR?(o.f.properties.label_ar||o.f.properties.label_en||''):(o.f.properties.label_en||''))+(AR?' (تقريبي)':' (approximate)'));
  return on};
 const declutter=()=>{/* nudge extent labels apart (and off capital labels); positions keep label_point as anchor */const placed=[];
  d3.selectAll(g.selectAll('text').nodes().concat(xg.selectAll('text').nodes(),pg.selectAll('text').nodes())).each(function(){const t=d3.select(this);if(this.__dx0==null)this.__dx0=+(t.attr('dx')||0),this.__dy0=+(t.attr('dy')||0);t.attr('dy',this.__dy0).attr('dx',this.__dx0);let b=bb(this),k=0;while(k<12&&placed.some(p=>p&&ov(p,b))){k++;t.attr('dy',this.__dy0+(k%2?1:-1)*Math.ceil(k/2)*(this.getBBox().height+2));b=bb(this)}/* keep label inside the map frame */const R=svg.node().getBoundingClientRect(),sc=600/R.width;b=bb(this);let sh=0;if(b.x<R.left+2)sh=R.left+2-b.x;else if(b.x+b.w>R.right-2)sh=R.right-2-(b.x+b.w);if(sh)t.attr('dx',this.__dx0+sh*sc);b=bb(this);placed.push(b)})};
 const bb=el=>{const r=el.getBoundingClientRect();return {x:r.left,y:r.top,w:r.width,h:r.height}},ov=(a,c)=>a.x<c.x+c.w&&c.x<a.x+a.w&&a.y<c.y+c.h&&c.y<a.y+a.h;
 const pg=svg.append('g');const drawP=y=>{const on=PT.filter(o=>{const a0=o.f.properties.start??o.e.a,b0=o.f.properties.end??o.e.b;return a0<=y&&(y<b0||(y===b0&&b0>=o.e.b))});const s=pg.selectAll('g.r').data(on,o=>o.e.id+o.f.geometry.coordinates);s.exit().remove();
  const n=s.enter().append('g').attr('class','r').attr('transform',o=>`translate(${pr(o.f.geometry.coordinates)})`);const low=o=>String(o.f.properties.certainty||'').toLowerCase()==='low';
  n.append('rect').attr('x',-4).attr('y',-4).attr('width',8).attr('height',8).attr('transform','rotate(45)').attr('fill',o=>low(o)?'#fff':P.col).attr('stroke',P.col).attr('stroke-width',1.5).attr('stroke-dasharray',o=>low(o)?'2 2':null);
  n.append('title').text(o=>[full(o),o.f.properties.certainty?'['+o.f.properties.certainty+']':'',o.f.properties.citation].filter(Boolean).join('\n'));
  n.append('text').attr('class','rl').attr('dx',AR?-8:8).attr('dy',4).attr('text-anchor',AR?'end':'start').attr('font-size',11).attr('fill',P.col).attr('paint-order','stroke').attr('stroke','#fff').attr('stroke-width',3).text(o=>short(full(o)||'')+(o.f.properties.certainty?' ['+o.f.properties.certainty+']':''));return on};
 const draw=y=>{const po=drawP(y);const xo=drawX(y).concat(po);const on=pts.filter(p=>p.e.a<=y&&p.e.b>=y);const s=g.selectAll('g.p').data(on,p=>p.e.id+p.c.name);s.exit().transition().duration(250).style('opacity',0).remove();
  const n=s.enter().append('g').attr('class','p').style('opacity',0);n.append('circle').attr('r',d=>d.main?7:4).attr('fill',d=>d.main?P.col:'#8a8a8a').attr('stroke','#fff');
  n.append('text').attr('dx',AR?-10:10).attr('dy',4).attr('text-anchor',AR?'end':'start').attr('font-size',d=>d.main?15:11).attr('paint-order','stroke').attr('stroke','#fff').attr('stroke-width',3).text(d=>d.c.name);
  n.merge(s).attr('transform',d=>`translate(${pr([d.c.lon,d.c.lat])})`).transition().duration(250).style('opacity',1);
  const es=[...new Set(on.map(p=>p.e))];tip.innerHTML=(es.map(e=>`<a href="${link(e)}" style="color:${P.eras.includes(e)?P.col:'#6b6257'}">${esc(e.n)}</a>`+(P.eras.includes(e)&&e.ext!=='ok'?` <span class="gap">${AR?'المنطقة: قيد البحث':'area: research in progress'}</span>`:'')).join(' · ')||'—')+(xo.length?'<br><small>≈ '+(AR?'المنطقة تقريبية — المصادر: ':'Areas are approximate — sources: ')+[...new Set(xo.flatMap(o=>{const p=o.f.properties;return [p.citation].concat(p.source_citations||[]).concat(p.geometry_citation?[(AR?'الهندسة: ':'Geometry: ')+p.geometry_citation]:[])}))].map(esc).join('; ')+'</small>'+(xo.length?'<ul class="xd">'+[...new Set(xo.map(o=>[full(o),dt(o)].filter(Boolean).join(' — ')).filter(Boolean))].map(d=>'<li>'+esc(d)+'</li>').join('')+'</ul>':''):'');declutter();setTimeout(declutter,320)};
 const s=scrubber(draw)}
function neighbors(){const tip=document.createElement('div');root.appendChild(tip);scrubber(y=>{const on=all.filter(e=>e.a<=y&&e.b>=y);const by={};on.forEach(e=>(by[e.sl]=by[e.sl]||[]).push(e));
 tip.innerHTML='<ul class="eras">'+Object.keys(by).map(k=>`<li><a href="${link(by[k][0])}" style="${P.eras.includes(by[k][0])?'':'border-color:#b9ad99'}"><small>${esc(k)}</small>${by[k].map(e=>'<b>'+esc(e.n)+'</b>').join('<br>')}</a></li>`).join('')+'</ul>'})}
function sources(){const ls=[...new Set(P.eras.flatMap(e=>e.langs))];const tbl=document.createElement('div');tbl.className='tw';
 tbl.innerHTML='<table><thead><tr><th></th><th>#</th>'+ls.map(l=>`<th>${esc(l)}</th>`).join('')+'<th>⇄</th></tr></thead><tbody>'+P.eras.map(e=>`<tr><td><a href="${link(e)}">${esc(e.n)}</a></td><td>${e.nsrc}</td>`+ls.map(l=>`<td>${e.langs.includes(l)?'<span style="display:inline-block;width:14px;height:14px;border-radius:50%;background:'+P.col+'" aria-label="'+l+'"></span>':''}</td>`).join('')+`<td>${e.comp.map(c=>`<span class="st st-${esc(c.status)}">${esc(c.lang)}</span>`).join(' ')||'<span class="gap">—</span>'}</td></tr>`).join('')+'</tbody></table>';root.appendChild(tbl)}
const M=P.mode;try{if(M==='duration')duration();else if(M==='map')map();else if(M==='lanes')lanes(P.eras,true);else if(M==='neighbors')neighbors();else if(M==='sources')sources();else if(M==='era')((P.eras[0].caps.length||P.eras[0].ext==='ok'||P.eras[0].pts)?map():null)}catch(err){root.textContent=''}
})();
