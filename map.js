// Sudan Histomap: one continuous map page. All data comes from window.MAP (built from data/eras + db/extents by web/build.py)
// and per-era files (/extents/<id>.json, /m/<id>.json). Nothing is invented; missing layers show 'Research in progress'.
(function(){
const M=window.MAP,Q=new URLSearchParams(location.search),L=Q.get('lang')==='ar'?'ar':'en',AR=L==='ar',T=M.t[L],ES=M.eras;
const RM=matchMedia('(prefers-reduced-motion: reduce)').matches,DUR=RM?0:650;
const $=id=>document.getElementById(id),esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const num=n=>AR?String(n).replace(/\d/g,d=>'٠١٢٣٤٥٦٧٨٩'[d]):String(n);
const fy=y=>y>=2026?(AR?'اليوم':'present'):y<0?num(-y)+(AR?' ق.م':' BCE'):num(y)+(AR?' م':' CE');
const BL={REPORTED:['REPORTED','مُبلَّغ عنه','#e0574c'],CONTESTED:['CONTESTED','متنازع عليها','#b07ae0'],'SINGLE-SOURCE':['SINGLE-SOURCE','مصدر واحد','#e0a63e']};/* 'مصدر واحد' pending native review */
const rep=p=>{const b=String(p.badge||'').toUpperCase().split(' (')[0];return BL[b]?b:''};
const unrep=s=>String(s||'').replace(/\s*\[(REPORTED|CONTESTED|مُبلَّغ عنه|متنازع عليها)\]/g,'');
const lab=p=>unrep(AR?(p.label_ar||p.label_en):(p.label_en||p.label_ar));
const short=s=>{s=String(s).split(/ [–—] /)[0];if(s.length>34)s=s.split(/[(（,،:]/)[0].trim();return s.length>40?s.slice(0,38)+'…':s};
// --- chrome
document.title=T.title+' · '+(AR?'Sudan Histomap':'خريطة تاريخ السودان');
$('brand').textContent=T.title;$('about').textContent=T.about;$('about').href=(AR?'/ar':'')+'/about/';
const lq=new URLSearchParams(Q);if(AR)lq.delete('lang');else lq.set('lang','ar');$('lang').textContent=T.lang;$('lang').setAttribute('hreflang',AR?'en':'ar');
$('lang').addEventListener('click',e=>{e.preventDefault();const q=new URLSearchParams(location.search);AR?q.delete('lang'):q.set('lang','ar');location.search=q.toString()});
$('lang').href='/?'+lq.toString();$('prev').setAttribute('aria-label',T.prev);$('next').setAttribute('aria-label',T.next);$('grab').setAttribute('aria-label',T.sheet);
$('reset').title=T.reset;$('reset').setAttribute('aria-label',T.reset);$('within').querySelector('label').textContent=T.within;
const LAY=['ctl','grp','rel','pop','cty','hml'],on=new Set((Q.get('layers')||'ctl').split(',').map(x=>x==='cities'?'cty':x==='homelands'?'hml':x).filter(x=>LAY.includes(x)));
LAY.forEach(k=>{const b=document.createElement('button');b.className='chip';b.type='button';b.textContent=T.l[k];b.setAttribute('aria-pressed',on.has(k));b.dataset.k=k;
 b.onclick=()=>{on.has(k)?on.delete(k):on.add(k);b.setAttribute('aria-pressed',on.has(k));url();render(false);if(k==='hml')hmlDraw()};$('layers').appendChild(b)});
document.addEventListener('click',ev=>{const t=ev.target.closest&&ev.target.closest('[data-hml]');if(!t)return;ev.preventDefault();if(!on.has('hml')){on.add('hml');const c=document.querySelector('#layers .chip[data-k=hml]');if(c)c.setAttribute('aria-pressed','true');url();render(false);hmlDraw()}});
// --- era index
let i=Math.max(0,ES.findIndex(e=>e.id===Q.get('era')));const r=$('r');r.max=ES.length-1;r.value=i;r.setAttribute('aria-label',T.era);
function url(){const q=new URLSearchParams();q.set('era',ES[i].id);if(AR)q.set('lang','ar');const ly=[...on].sort().join(',');if(ly!=='ctl')q.set('layers',ly);history.replaceState(null,'','/?'+q)}
// --- map
const svg=d3.select('#svg'),W=()=>innerWidth,H=()=>innerHeight,desk=()=>innerWidth>=1000;
const root=svg.append('g'),gB=root.append('g').attr('class','relief'),gL=root.append('g'),gC=root.append('g'),gX=root.append('g'),gN=root.append('g'),gG=root.append('g'),gH=root.append('g').attr('class','hml'),gY=root.append('g').attr('class','cities'),gR=root.append('g'),gP=root.append('g'),gK=root.append('g'),gT=root.append('g'),gF=root.append('g').attr('class','flags');
svg.append('defs').html('<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="#f08c6c"/></marker>');
const proj=d3.geoMercator(),path=d3.geoPath(proj);let K=1,TR=d3.zoomIdentity;
// topographic basemap: Natural Earth relief pre-rendered in Web Mercator over RELIEF_BOX (web/basemap/make_relief.py); placed by its corners, so the root zoom transform keeps it aligned. 900px by default, 1800px once zoomed in or on desktop.
const RELIEF_BOX=[12,-3,48,27];let RHI=false;function relief(){const a=proj([RELIEF_BOX[0],RELIEF_BOX[3]]),b=proj([RELIEF_BOX[2],RELIEF_BOX[1]]);if(!RHI&&(K>=2||desk()))RHI=true;gB.selectAll('image').data([RHI?'/img/relief-1800.webp':'/img/relief-900.webp']).join('image').attr('href',d=>d).attr('x',a[0]).attr('y',a[1]).attr('width',b[0]-a[0]).attr('height',b[1]-a[1]).attr('preserveAspectRatio','none')}
function fit(){const sh=$('sheet').getBoundingClientRect();const top=desk()?70:120,bot=desk()?H()-20:Math.max(top+160,H()-Math.min(sh.height,H()*.44)-8);
 const x1=desk()?(AR?sh.right+20:20):10,x2=desk()?(AR?W()-20:sh.left-20):W()-10;
 proj.fitExtent([[x1,top],[x2,bot]],{type:'MultiPoint',coordinates:[[21.8,3.4],[38.6,22.2]]});relief()}
const zoom=d3.zoom().scaleExtent([1,12]).on('zoom',ev=>{TR=ev.transform;root.attr('transform',ev.transform);K=ev.transform.k;scaleMarks();$('reset').hidden=K<1.05&&Math.abs(ev.transform.x)<2}).on('end',()=>{if(!RHI&&K>=2)relief();place();cityThin();hmlDraw()});
svg.call(zoom).on('dblclick.zoom',null);$('reset').onclick=()=>svg.transition().duration(DUR).call(zoom.transform,d3.zoomIdentity);
function scaleMarks(){root.selectAll('.mk').attr('transform',function(){return `translate(${this.__xy})scale(${1/K})`});clearTimeout(scaleMarks.t);scaleMarks.t=setTimeout(()=>{if(typeof hmlThin==='function')hmlThin()},120)}
const rw=f=>{const G=f.geometry,rv=a=>a.slice().reverse();if(G.type==='Polygon'){if(d3.geoArea(f)>2*Math.PI)G.coordinates=G.coordinates.map(rv)}else if(G.type==='MultiPolygon')G.coordinates=G.coordinates.map(p=>d3.geoArea({type:'Polygon',coordinates:p})>2*Math.PI?p.map(rv):p);return f};
let BASE=null;const C={},CARD={},LD={};
const getj=u=>fetch(u).then(x=>{if(!x.ok)throw new Error(u+' '+x.status);return x.json()});
function ext(e){if(!e.x)return Promise.resolve({features:[],lines:[]});return C[e.id]||(C[e.id]=getj('/extents/'+e.id+'.json').then(g=>{g.features.forEach(f=>{if(f.geometry.type!=='Point')rw(f)});g.lines=g.lines||[];return g}).catch(()=>({features:[],lines:[]})))}
function cardj(e){return CARD[e.id]||(CARD[e.id]=getj('/m/'+e.id+'.json').catch(()=>null))}
function layer(k){const f=M.layers[k];if(!f)return Promise.resolve(null);return LD[k]||(LD[k]=Promise.all([].concat(f).map(u=>getj(u).catch(()=>null))).then(a=>a.filter(Boolean)))}
// --- year within era (features carry their own start/end; end exclusive except the era's final year)
const act=(p,e,y)=>{const a=p.start??e.a,b=p.end??e.b;return a<=y&&(y<b||(y===b&&b>=e.b))};
let Y=null;function steps(e,g){const s=new Set([e.a]);g.features.forEach(f=>{const a=f.properties.start;if(a!=null&&a>e.a&&a<e.b)s.add(a)});return [...s].sort((x,z)=>x-z)}
// --- morph helpers: resample the largest projected outer ring to N points
const N=96;function ringOf(f){const G=f.geometry;const polys=G.type==='Polygon'?[G.coordinates]:G.coordinates;let best=null,ba=-1;polys.forEach(p=>{const a=d3.geoArea({type:'Polygon',coordinates:p});if(a>ba){ba=a;best=p[0]}});return best.map(c=>proj(c))}
function resample(pts){const L=[0];for(let k=1;k<pts.length;k++)L.push(L[k-1]+Math.hypot(pts[k][0]-pts[k-1][0],pts[k][1]-pts[k-1][1]));const tot=L[L.length-1]||1,o=[];let j=0;
 for(let k=0;k<N;k++){const d=k/N*tot;while(j<L.length-2&&L[j+1]<d)j++;const t=(d-L[j])/((L[j+1]-L[j])||1);o.push([pts[j][0]+(pts[j+1][0]-pts[j][0])*t,pts[j][1]+(pts[j+1][1]-pts[j][1])*t])}return o}
function align(a,b){let bi=0,bd=1e18;for(let k=0;k<N;k++){const d=Math.hypot(a[0][0]-b[k][0],a[0][1]-b[k][1]);if(d<bd){bd=d;bi=k}}return b.slice(bi).concat(b.slice(0,bi))}
const bbox=f=>path.bounds(f),iou=(A,B)=>{const x=Math.max(0,Math.min(A[1][0],B[1][0])-Math.max(A[0][0],B[0][0])),y=Math.max(0,Math.min(A[1][1],B[1][1])-Math.max(A[0][1],B[0][1]));const I=x*y,U=(A[1][0]-A[0][0])*(A[1][1]-A[0][1])+(B[1][0]-B[0][0])*(B[1][1]-B[0][1])-I;return U>0?I/U:0};
const dpts=p=>'M'+p.map(q=>q[0].toFixed(1)+','+q[1].toFixed(1)).join('L')+'Z';
// --- draw base
function drawBase(e){if(!BASE)return;const y=Y??e.b,post=y>=2011;
 gL.selectAll('path').data(BASE.features).join('path').attr('d',path).attr('class',d=>'land'+(d.properties.name==='Sudan'?' sdn':d.properties.name==='S. Sudan'?(post?' ssd':' ssd-old'):''));
 const ss=BASE.features.find(d=>d.properties.name==='S. Sudan');gC.selectAll('text').data(post&&ss?[ss]:[]).join('text').attr('class','cl').attr('text-anchor','middle').attr('transform',d=>`translate(${path.centroid(d)})`).text(T.ssd)}
let OLD=[];// previously drawn area features [{f,d,box}]
async function render(anim=true){
 const e=ES[i];r.value=i;url();const g=await ext(e);if(e!==ES[i])return;
 cam(e,g);
 const st=steps(e,g);if(Y==null||Y<e.a||Y>e.b)Y=st[st.length-1];
 const wi=$('within');wi.hidden=st.length<2;if(st.length>1){const w=$('w');w.min=0;w.max=st.length-1;w.value=Math.max(0,st.findIndex(s=>s===Y));$('wo').textContent=fy(Y)}
 document.documentElement.style.setProperty('--c',e.c);
 $('en').textContent=AR?e.ar:e.en;$('yrs').innerHTML=`<bdi>${fy(e.a)}</bdi> – <bdi>${fy(e.b)}</bdi> · ${esc(AR?e.sa:e.s)} · ${num(i+1)}/${num(ES.length)}`;
 $('nob').innerHTML=e.g==='pts'?`<span class="pts"${AR?' title="Arabic label under native-speaker review"':''}>${T.pts}</span>`:e.g==='none'?`<span class="none">${T.none}</span>`:e.g==='hml'?`<button type="button" class="hmlb" data-hml="1" aria-pressed="${on.has('hml')}">${AR?'معروض على طبقة الأوطان *':'Shown on the Homelands layer'}</button>`:'';
 drawBase(e);
 const ctl=on.has('ctl'),areas=ctl?g.features.filter(f=>f.geometry.type!=='Point'&&act(f.properties,e,Y)):[],pts=ctl?g.features.filter(f=>f.geometry.type==='Point'&&act(f.properties,e,Y)):[];
 // areas: morph matched shapes, crossfade the rest
 const D=anim?DUR:0,NEW=areas.map(f=>({f,box:bbox(f)})),used=new Set();
 gX.selectAll('path.ext').interrupt().remove();gX.selectAll('path.old').interrupt().remove();
 NEW.forEach(n=>{let bi=-1,bv=.25;OLD.forEach((o,k)=>{if(used.has(k))return;const v=iou(o.box,n.box);if(v>bv){bv=v;bi=k}});n.m=bi;if(bi>=0)used.add(bi)});
 OLD.forEach((o,k)=>{if(used.has(k)||!D)return;gX.append('path').attr('class','ext old').attr('d',path(o.f)).style('opacity',1).transition().duration(D).style('opacity',0).remove()});
 NEW.forEach(n=>{const p=gX.append('path').attr('class','ext'+(String(n.f.properties.certainty||'').toLowerCase()==='low'?' low':'')).datum(n.f).on('click',(ev)=>{ev.stopPropagation();feat(n.f,e)});
  if(D&&n.m>=0){const a=resample(ringOf(OLD[n.m].f)),b=align(a,resample(ringOf(n.f)));const it=d3.interpolateArray(a,b);p.attr('d',dpts(a)).transition().duration(D).ease(d3.easeCubicInOut).attrTween('d',()=>t=>dpts(it(t))).on('end',function(){d3.select(this).attr('d',path(n.f))})}
  else{p.attr('d',path(n.f)).style('opacity',D?0:1);if(D)p.transition().duration(D).style('opacity',1)}});
 OLD=NEW.map(n=>({f:n.f,box:n.box}));
 // points (diamonds) and capitals
 // open lines: never filled; dashed when the feature says so (line_style/style.dash), arrowhead only when it says arrow
 const lns=ctl?(g.lines||[]).filter(f=>act(f.properties,e,Y)):[];const dsh=p=>p.line_style==='dashed'||!!(p.style&&p.style.dash);
 gN.selectAll('path.ln').data(lns,f=>e.id+(f.properties.fid||JSON.stringify(f.geometry.coordinates[0]))).join(en=>en.append('path').call(p=>p.append('title')).on('click',(ev,f)=>{ev.stopPropagation();feat(f,e)}))
  .attr('class',f=>'ln'+(dsh(f.properties)?' dash':'')+(f.properties.arrow?' arr':'')).attr('fill','none').attr('d',f=>path(f.geometry)).attr('marker-end',f=>f.properties.arrow?'url(#ah-ln)':null).each(function(f){this.querySelector('title').textContent=lab(f.properties)||''});
 const pk=gP.selectAll('g.pt').data(pts,f=>e.id+f.geometry.coordinates);pk.exit().remove();
 const pn=pk.enter().append('g').attr('class',f=>'pt mk'+(String(f.properties.certainty||'').toLowerCase()==='low'?' low':'')).each(function(f){this.__xy=proj(f.geometry.coordinates)}).on('click',(ev,f)=>{ev.stopPropagation();feat(f,e)});
 pn.append('rect').attr('x',-5).attr('y',-5).attr('width',10).attr('height',10).attr('transform','rotate(45)');pn.append('title').text(f=>lab(f.properties));
 if(D)pn.style('opacity',0).transition().duration(D).style('opacity',1);
 const caps=(e.caps||[]).filter(c=>!pts.some(f=>Math.abs(f.geometry.coordinates[0]-c[1])<.05&&Math.abs(f.geometry.coordinates[1]-c[2])<.05));
 const ck=gK.selectAll('g.cap').data(caps,c=>e.id+c[0]);ck.exit().remove();const cn=ck.enter().append('g').attr('class','cap mk').each(function(c){this.__xy=proj([c[1],c[2]])});cn.append('circle').attr('r',4.5);cn.append('title').text(c=>c[0]);
 scaleMarks();
 // labels (priority thinning + leader lines, as on the era map)
 const LB=[];areas.forEach(f=>{const q=f.properties.label_point;const xy=q?proj(q):path.centroid(f);if(lab(f.properties))LB.push({xy,t:short(lab(f.properties)),pri:3,big:1})});
 pts.forEach(f=>LB.push({xy:proj(f.geometry.coordinates),t:short(lab(f.properties)),pri:rep(f.properties)?2.5:2,rep:rep(f.properties),dx:9}));caps.forEach(c=>LB.push({xy:proj([c[1],c[2]]),t:c[0],pri:2,dx:8}));
 LBS=LB;
 await layersDraw(e);if(on.has('hml'))hmlDraw();
 // card
 const cj=await cardj(e);if(e!==ES[i])return;$('card').innerHTML=cj?cj[L]:`<p><span class="gap">${T.wip}</span></p>`;layerInfo(e);$('feat').hidden=true;
 place()}
let LBS=[];
function nobPos(){const b=$('layers').getBoundingClientRect();document.documentElement.style.setProperty('--chipb',Math.round(b.bottom)+'px');$('nob').style.top=(b.bottom+6)+'px';setTimeout(lgFit,0)}
function place(){setTimeout(cityThin,0);nobPos();const t=TR;gT.selectAll('*').remove();const placed=[],hid=[];
 // obstacles: the card and the top chrome
 const ob=['sheet','top','layers','nob'].map(id=>$(id).getBoundingClientRect()).filter(b=>b.width).map(b=>({x:b.left,y:b.top,w:b.width,h:b.height}));
 root.selectAll('.mk').nodes().forEach(n=>{const s=n.querySelector('rect,circle,path');if(!s)return;const b=s.getBoundingClientRect();if(b.width)ob.push({x:b.left+1,y:b.top+1,w:Math.max(0,b.width-2),h:Math.max(0,b.height-2)})});
 const ov=(a,c)=>a.x<c.x+c.w&&c.x<a.x+a.w&&a.y<c.y+c.h&&c.y<a.y+a.h;
 LBS.slice().sort((a,b)=>b.pri-a.pri).forEach(o=>{const sx=t.applyX(o.xy[0]),sy=t.applyY(o.xy[1]);if(sx<0||sx>W()||sy<0||sy>H()){return}
  const gg=gT.append('g').attr('transform',`translate(${sx},${sy})`);const tx=gg.append('text').attr('class','lb'+(o.big?' big':'')).text(o.t);
  if(o.rep){tx.append('tspan').attr('class','rep').attr('fill',BL[o.rep][2]).text(' '+BL[o.rep][AR?1:0])}
  const lh=16,dx0=o.dx?(AR?-o.dx:o.dx):0,an0=o.big?'middle':'start';let ok=null;
  P:for(const k of [0,1,-1,2,-2,3,-3])for(const side of (o.dx?[0,1]:[0])){const dx=side?-dx0:dx0,an=o.big?'middle':(side?'end':'start');tx.attr('x',dx).attr('y',4+k*lh).attr('text-anchor',an);
   const b=tx.node().getBoundingClientRect(),bb={x:b.left-2,y:b.top-1,w:b.width+4,h:b.height+2};if(bb.x<2||bb.x+bb.w>W()-2)continue;if(!placed.some(p=>ov(p,bb))&&!ob.some(p=>ov(p,bb))){ok={k,dx,bb,an};break P}}
  if(!ok){gg.remove();hid.push(o);return}tx.attr('x',ok.dx).attr('y',4+ok.k*lh).attr('text-anchor',ok.an);placed.push(ok.bb);
  if(ok.k!==0&&o.pri>=2.5)gg.insert('line','text').attr('class','ld').attr('x1',0).attr('y1',0).attr('x2',ok.dx).attr('y2',ok.k*lh+(ok.k<0?2:-8))});
 $('hidden').innerHTML=hid.length?T.hidden+': '+[...new Set(hid.map(o=>o.t))].map(esc).join(AR?'، ':', '):''}
// --- tap a feature for details
function feat(f,e){const p=f.properties,b=rep(p);const det=AR?(p.label_detail_ar||p.label_detail_en):(p.label_detail_en||p.label_detail_ar);
 $('feat').innerHTML=`<button class="x" aria-label="close">×</button><b>${esc(lab(p)||'—')}</b>${b?` <span class="repb${b==='CONTESTED'?' cont':b==='SINGLE-SOURCE'?' single':''}">${esc(b==='SINGLE-SOURCE'&&!AR?p.badge:BL[b][AR?1:0])}</span>`:''}${p.certainty?` <small>[${esc(p.certainty)}]</small>`:''}`+
  (p.start!=null?`<br><small><bdi>${fy(p.start)}</bdi> – <bdi>${fy(p.end??e.b)}</bdi></small>`:'')+(det?`<p>${esc(det)}</p>`:'')+
  `<p class="extnote"><bdi dir="ltr">${esc(p.citation||p.source)}${p.pages?' pp. '+esc(p.pages):''}</bdi>${p.url?` <a href="${esc(p.url)}" rel="noopener">link</a>`:''}${p.source_pins?Object.entries(p.source_pins).map(([k,v])=>`<br><bdi dir="ltr">${esc(k)}: ${esc(v)}</bdi>`).join(''):''}${(p.badges||[]).filter(x=>x!==b).map(x=>` <span class="repb">${esc(BL[x]?BL[x][AR?1:0]:x)}</span>`).join('')}${p.geometry_citation?`<br>${AR?'الهندسة':'Geometry'}: <bdi dir="ltr">${esc(p.geometry_citation)}</bdi>`:''}</p>`;
 $('feat').hidden=false;$('feat').querySelector('.x').onclick=()=>{$('feat').hidden=true};if($('sheet').classList.contains('peek'))snap('half');$('feat').scrollIntoView({block:'nearest'})}
svg.on('click',()=>{$('feat').hidden=true});
// --- optional layers: drawn only from delivered, sourced files
const srcd=x=>!!(x&&(x.source||x.source_id||(x.source_ids&&x.source_ids.length)||(x.sources&&x.sources.length)||(x.properties&&(x.properties.source||(x.properties.source_ids||[]).length))));
const items=d=>!d?[]:Array.isArray(d)?d:d.features||d.groups||d.relations||d.series||d.data||d.items||[];
const yrIn=(x,e,y)=>{const p=x.properties||x;const a=p.start??p.from_year??-1e9,b=p.end??p.to_year??1e9;return a<=y&&y<=b};
const anchor=id=>{const e=ES.find(z=>z.id===id);if(!e)return null;const g=C[e.id];const c=e.caps&&e.caps[0];return c?[c[1],c[2]]:null};
const RC={alliance:'#4fb06b',conflict:'#e0574c',trade:'#e0a63e',subjugation:'#b07ae0',migration:'#5aa9e6'};
svg.select('defs').html(Object.entries(RC).map(([k,c])=>`<marker id="ah-${k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="${c}"/></marker>`).join('')+'<marker id="ah-ln" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="#f0d26c"/></marker>');
const GJ={};function glj(e){if(!M.layers.glBuilt||!(M.layers.g||[]).includes(e.id))return Promise.resolve([]);return GJ[e.id]||(GJ[e.id]=getj('/g/'+e.id+'.json').catch(()=>[]))}
function glTap(ev,f){ev.stopPropagation();const li=document.querySelector(`#card li[data-id="${CSS.escape(f.id)}"]`);$('feat').innerHTML='<button class="x" aria-label="close">×</button>'+(li?li.innerHTML:esc(AR?f.ar:f.en));$('feat').hidden=false;$('feat').querySelector('.x').onclick=()=>{$('feat').hidden=true};if($('sheet').classList.contains('peek'))snap('half')}
async function layersDraw(e){const fs=(on.has('grp')||on.has('rel'))?await glj(e):[];const D=RM?0:DUR;
 const pts=on.has('grp')?fs.filter(f=>f.k!=='relation'&&f.geo&&f.geo.type==='Point'):[];
 // stable ids: the same group feature glides to its new anchor between eras
 const s=gG.selectAll('g.grp').data(pts,f=>f.id);s.exit().remove();
 const n=s.enter().append('g').attr('class',f=>'grp mk '+(f.k||'')).on('click',glTap);n.append('circle').attr('r',7);n.append('title');
 n.merge(s).each(function(f){const to=proj(f.geo.coordinates),fr=this.__xy||to;this.__xy=to;if(D&&fr!==to&&(fr[0]!==to[0]||fr[1]!==to[1])){const el=this,it=d3.interpolateArray(fr,to);d3.select(el).transition().duration(D).tween('m',()=>t=>{el.__xy=it(t);el.setAttribute('transform',`translate(${el.__xy})scale(${1/K})`)})}}).select('title').text(f=>(AR?f.ar:f.en)+(f.b?' ['+f.b+']':''));
 const ln=on.has('rel')?fs.filter(f=>f.k==='relation'&&f.geo&&/LineString$/.test(f.geo.type)):[];
 const r=gR.selectAll('path.rel').data(ln,f=>f.id);r.exit().remove();
 r.enter().append('path').attr('class',f=>'rel '+(f.t||'')).on('click',glTap).append('title').merge(r.select('title')).text(f=>(AR?f.ar:f.en)+(f.b?' ['+f.b+']':''));
 gR.selectAll('path.rel').attr('stroke',f=>RC[f.t]||'#ccc').attr('marker-end',f=>RC[f.t]?`url(#ah-${f.t})`:null).attr('stroke-dasharray',f=>String(f.c).toLowerCase()==='low'?'5 4':null)
  .attr('d',f=>{if(f.geo.type==='MultiLineString')return path(f.geo);const c=f.geo.coordinates,a=proj(c[0]),b=proj(c[c.length-1]),mx=(a[0]+b[0])/2,my=(a[1]+b[1])/2,dx=b[0]-a[0],dy=b[1]-a[1];return `M${a}Q${mx-dy*.2},${my+dx*.2} ${b}`});
 await citiesDraw(e,D);flagsDraw(e);
 // population stays in the card (sparkline); no invented geography for it
 scaleMarks()}
async function layerInfo(e){const box=$('layerinfo');if(!box)return;let h='';
 const pl=document.querySelector('.poplayer');if(pl)pl.hidden=!on.has('pop');const gl=document.querySelector('.grplayer'),rl=document.querySelector('.rellayer');if(gl)gl.hidden=!on.has('grp');if(rl)rl.hidden=!on.has('rel');
 for(const k of ['grp','rel','pop']){if(!on.has(k)||(k==='pop'&&pl)||(k==='grp'&&gl)||(k==='rel'&&rl))continue;const d=await layer(k);const gapT={grp:T.grpgap,rel:T.relgap,pop:T.popgap}[k];
  if(!d||!d.length||!d.flatMap(items).length){h+=`<p class="lgap"><b>${T.l[k]}:</b> <span class="gap">${T.wip}</span> <span class="gapt">${esc(gapT)}</span></p>`;continue}
  if(k==='pop'){const s=d.flatMap(items).filter(x=>x.year!=null&&x.value!=null&&(x.lat==null)).sort((a,b)=>a.year-b.year);if(s.length<2){h+=`<p class="lgap"><b>${T.l.pop}:</b> <span class="gap">${T.wip}</span></p>`;continue}
   const x0=s[0].year,x1=s[s.length-1].year,v1=Math.max(...s.map(x=>+x.value)),X=y=>(y-x0)/(x1-x0||1)*300+10,Yv=v=>40-(+v/v1)*34;const inE=s.filter(x=>x.year>=e.a&&x.year<=e.b);const last=inE[inE.length-1];
   h+=`<p class="lgap"><b>${T.l.pop}</b>${last?` · <bdi>${fy(last.year)}</bdi>: <b>${num((+last.value).toLocaleString(AR?'ar':'en'))}</b>`:` · <span class="gap">${T.wip}</span>`}</p><svg class="spark" viewBox="0 0 320 46" role="img" aria-label="${esc(T.l.pop)}" style="transform:${AR?'scaleX(-1)':'none'}"><rect x="${X(Math.max(e.a,x0))}" y="0" width="${Math.max(2,X(Math.min(e.b,x1))-X(Math.max(e.a,x0)))}" height="46" fill="#8cc8f022"/><polyline fill="none" stroke="#8cc8f0" stroke-width="2" points="${s.map(x=>X(x.year)+','+Yv(x.value)).join(' ')}"/></svg><p class="extnote"><bdi dir="ltr">${esc([...new Set(s.flatMap(x=>[].concat(x.source||x.source_ids||[])))].join('; '))}</bdi></p>`;continue}
  const n=d.flatMap(items).filter(x=>srcd(x)).length;h+=`<p class="lgap"><b>${T.l[k]}:</b> ${num(n)}</p>`}
 if(on.has('cty')){const d=await cty();if(!d||!d.cities.length)h+=`<p class="lgap"><b>${T.l.cty}:</b> <span class="gap">${T.wip}</span> <span class="gapt">${esc(T.ctygap)}</span></p>`;
  else{const v=d.cities.filter(c=>cityVis(c,e)),nc=v.filter(c=>c.r[e.id]&&c.r[e.id].cap).length;h+=`<p class="lgap"><b>${T.l.cty}:</b> ${num(v.length)}${nc?` · ★ ${num(nc)}`:''}${d.stub?` <span class="gap">${esc(T.stub)}</span>`:''}</p>`;
  if(d.lo&&d.lo.length)h+=`<p class="lgap"><button class="lob" type="button">${esc(T.lolist)} (${num(d.lo.length)})</button></p>`}}
 box.innerHTML=h;legendDraw(e);const lb=box.querySelector('.lob');if(lb)lb.onclick=ev=>cityList(ev)}
const RK={capital:['Capital','عاصمة'],garrison:['Garrison','حامية'],port:['Port','ميناء'],religious:['Religious centre','مركز ديني'],trade:['Trade centre','مركز تجاري']};
Object.assign(BL,{'APPROXIMATE-COORDS':['Approximate location','موقع تقريبي *'],'FIRST-ATTESTED':BL['FIRST-ATTESTED']||['First attested','أول ذكر موثّق'],UNDATED:BL.UNDATED||['Undated','غير مؤرّخ'],'AR-REVIEW':BL['AR-REVIEW']||['Arabic under review','العربية قيد المراجعة'],APPROXIMATE:BL.APPROXIMATE||['Approximate','تقريبي'],'RUIN-UNDATED':BL['RUIN-UNDATED']||['Ruin, end undated','أطلال، نهاية غير مؤرّخة']});
async function cityList(ev){ev.stopPropagation();const d=await cty();if(!d)return;const B=x=>`<span class="repb">${esc(BL[x]?BL[x][AR?1:0]:x)}</span>`;
 $('feat').innerHTML=`<button class="x" aria-label="close">×</button><b>${esc(T.lolist)}</b><p class="gapt">${esc(T.lonote)}</p><ul class="lol">`+d.lo.map(c=>`<li><bdi>${esc(AR?(c.ar||c.en):(c.en||c.ar))}</bdi> ${(c.b||[]).map(B).join(' ')}${c.why&&!(AR&&/^no founded/i.test(c.why))?`<br><small class="gapt">${esc(c.why)}</small>`:''}</li>`).join('')+'</ul>';
 $('feat').hidden=false;if($('sheet').classList.contains('peek'))snap('half');const x=$('feat').querySelector('.x');if(x)x.onclick=()=>{$('feat').hidden=true;$('feat').classList.remove('on')}}
// --- cities & towns (db/cities.json → /c.json). Shown only while founded ≤ year ≤ abandoned (or now); nothing inferred.
let CJ=null;function cty(){if(!M.layers.cBuilt)return Promise.resolve(null);return CJ||(CJ=getj('/c.json').catch(()=>null))}
function cityVis(c,e){const a=c.a==null?Infinity:c.a;return Y!=null?(c.f<=Y&&a>=Y):(c.f<=e.b&&a>=e.a)}
const cName=c=>AR?(c.ar||c.en):(c.en||c.ar);
async function citiesDraw(e,D){const d=on.has('cty')?await cty():null;if(e!==ES[i])return;
 const vis=d?d.cities.filter(c=>cityVis(c,e)).map(c=>Object.assign(c,{cap:!!(c.r[e.id]&&c.r[e.id].cap)})):[];
 const s=gY.selectAll('g.cty').data(vis,c=>c.id);
 s.exit().classed('gone',true).interrupt().transition().duration(D).style('opacity',0).remove();
 const n=s.enter().append('g').attr('class','cty mk').each(function(c){this.__xy=proj(c.ll)}).attr('transform',function(){return `translate(${this.__xy})scale(${1/K})`}).style('opacity',D?0:1).on('click',cityTap);
 n.append('path');n.append('text').attr('class','ctl2');n.append('title');
 n.transition().duration(D).style('opacity',1);
 const m=n.merge(s);m.classed('key',isKey).classed('minor',c=>!isKey(c)&&!c.cap).classed('capital',c=>c.cap).classed('ruin',isRuin).classed('oe',c=>isRuin(c)&&c.a==null).raise();m.selectAll('text.rq').remove();m.filter(c=>isRuin(c)&&c.a==null).append('text').attr('class','rq').attr('x',3.2).attr('y',-3.2).text('?');
 m.select('path').attr('d',cShape);
 m.select('text').attr('x',AR?-9:9).attr('y',4).attr('direction',AR?'rtl':'ltr').attr('text-anchor','start').text(cName);
 m.select('title').text(c=>cName(c)+(c.cap?' · '+T.capital:''));
 cityThin()}
// label thinning: capitals first, then cities with a role this era, then the rest; greedy screen-space boxes
// role shapes (legend uses the same paths)
const CSH={capital:'M0,-7L2,-2.2L7,-2.2L3,1L4.5,6.5L0,3.2L-4.5,6.5L-3,1L-7,-2.2L-2,-2.2Z',garrison:'M-3.4,-3.4h6.8v6.8h-6.8z',trade:'M0,-4.6L4.6,0L0,4.6L-4.6,0Z',port:'M0,-4.4L4.4,3.6L-4.4,3.6Z',religious:'M-1.3,-4.4h2.6v3.1h3.1v2.6h-3.1v3.1h-2.6v-3.1h-3.1v-2.6h3.1z',other:'M-3.2,0a3.2,3.2 0 1,0 6.4,0a3.2,3.2 0 1,0 -6.4,0'};
CSH.town='M0,-4L3.5,-2L3.5,2L0,4L-3.5,2L-3.5,-2Z';CSH.cult_centre='M0,4.4L4.4,-3.6L-4.4,-3.6Z';CSH.political_centre='M0,-4.6L4.4,-1.4L2.7,3.7L-2.7,3.7L-4.4,-1.4Z';
CSH.ruin='M-3.6,0a3.6,3.6 0 1,0 7.2,0a3.6,3.6 0 1,0 -7.2,0';
const cY=()=>Y!=null?Y:ES[i].b;
function isRuin(c){const y=cY();if(!c.ru||c.f>y||(c.a!=null&&c.a<y))return false;if(Object.values(c.r).some(r=>(r.y0==null||r.y0<=y)&&(r.y1==null||y<=r.y1)))return false;return c.lr==null||y>c.lr}
const cShape=c=>{if(isRuin(c))return CSH.ruin;const e=ES[i],r=c.r[e.id],kr=e.kc&&e.kc[c.id];return c.cap?CSH.capital:CSH[r&&r.k]||CSH[kr]||CSH.other};
const isKey=c=>!!(ES[i].kc&&ES[i].kc[c.id]);// tier-1: data/eras key_cities
let HJ=null;const hj=()=>M.layers.hBuilt?(HJ||(HJ=getj('/g/_homelands.json').catch(()=>null))):Promise.resolve(null);
const hLab=p=>{const s=AR?(p.ar||p.en):(p.en||p.ar);return String(s||'').replace(/\s*\[Arabic text pending[^\]]*\]/,'')};
async function hmlDraw(){const d=on.has('hml')?await hj():null;const pts=d?d.pts:[];
 const s=gH.selectAll('g.hm').data(pts,p=>p.id);s.exit().remove();
 const n=s.enter().append('g').attr('class',p=>'hm mk'+(p.b==='APPROXIMATE'?' apx':'')+(p.b==='CONTESTED'?' cont':'')).each(function(p){this.__xy=proj(p.ll)}).attr('transform',function(){return `translate(${this.__xy})scale(${1/K})`}).on('click',hmlTap);
 n.filter(p=>p.b==='APPROXIMATE').append('circle').attr('class','halo').attr('r',6.5);n.append('circle').attr('class','dot').attr('r',4);n.append('text').attr('class','hl').attr('x',AR?-8:8).attr('y',3).attr('direction',AR?'rtl':'ltr').text(p=>hLab(p).split(/[:：]/)[0]);n.append('title').text(p=>hLab(p)+' · '+T.hnd);hmlThin()}
 // homeland labels: only past HK zoom, lowest priority, culled against every other visible label
const HK=2.5;function hmlThin(){const ts=gH.selectAll('text.hl').nodes();if(!ts.length)return;if(K<HK){ts.forEach(t=>t.setAttribute('visibility','hidden'));return}
 const vis=t=>{if(t.getAttribute('visibility')==='hidden'||t.style.display==='none')return false;const s=getComputedStyle(t);return s.visibility!=='hidden'&&s.display!=='none'};
 const box=b=>[b.left-2,b.top-1,b.right+2,b.bottom+1],hit=(a,b)=>a[0]<b[2]&&b[0]<a[2]&&a[1]<b[3]&&b[1]<a[3];
 const ob=[...svg.node().querySelectorAll('text')].filter(t=>!t.classList.contains('hl')&&vis(t)).map(t=>t.getBoundingClientRect()).filter(b=>b.width).map(box);
 ['sheet','top','layers','nob','lgb','lgp'].forEach(id=>{const e=$(id);if(e&&!e.hidden){const b=e.getBoundingClientRect();if(b.width)ob.push([b.left,b.top,b.right,b.bottom])}});
 const TRY=[[8,3,'start',10],[-8,3,'end',10],[0,-8,'middle',10],[0,14,'middle',10],[7,3,'start',8.5],[-7,3,'end',8.5],[0,-7,'middle',8.5],[0,12,'middle',8.5]];
 ts.forEach(t=>{t.setAttribute('visibility','visible');let ok=false;for(const [x,y,an,fs] of TRY){const xx=AR&&an!=='middle'?-x:x;t.setAttribute('x',xx);t.setAttribute('y',y);t.setAttribute('text-anchor',AR?(an==='start'?'end':an==='end'?'start':an):an);t.style.fontSize=fs+'px';t.removeAttribute('direction');if(AR)t.setAttribute('direction','rtl');
  const b=t.getBoundingClientRect(),bb=box(b);if(b.width&&b.left>=2&&b.right<=innerWidth-2&&!ob.some(o=>hit(o,bb))){ob.push(bb);ok=true;break}}
  if(!ok)t.setAttribute('visibility','hidden')})}
function hmlTap(ev,p){ev.stopPropagation();const ar=AR&&/\[Arabic text pending/.test(p.ar||'');
 const B=x=>`<span class="repb">${esc(BL[x]?BL[x][AR?1:0]:x)}</span>`;
 $('feat').innerHTML=`<button class="x" aria-label="close">×</button><b>${esc(hLab(p))}</b> ${p.b?B(p.b):''}${ar?' '+B('AR-REVIEW'):''}<p><small>${esc(T.hnd)}</small></p>`+
  `<p>${esc(AR?(p.da||p.de):p.de)}</p>`+(p.cite?`<p class="extnote"><bdi dir="ltr">${esc(p.cite)}</bdi></p>`:'')+
  (p.s&&p.s.length?`<ol class="src">${p.s.map(x=>`<li><bdi dir="ltr">${esc(x.c)}</bdi>${x.u?` <a href="${esc(x.u)}" rel="noopener">link</a>`:''}</li>`).join('')}</ol>`:'');
 $('feat').hidden=false;$('feat').querySelector('.x').onclick=()=>{$('feat').hidden=true}}
const LGC={};const lgj=id=>LGC[id]||(LGC[id]=fetch(`/lg/${id}.json`).then(r=>r.ok?r.json():null).catch(()=>null));
const LGS=fetch('/lg/_spec.json').then(r=>r.ok?r.json():null).catch(()=>null);
function lgSw(r){const w=(p,ex='')=>`<svg width="26" height="18" viewBox="-13 -9 26 18" aria-hidden="true"${ex}>${p}</svg>`;
 if(r.id.startsWith('city_')){const k=r.id.slice(5);return w(`<path d="${CSH[k]||CSH.other}" class="lgcty${k==='capital'?' capital':''}" fill="${k==='capital'?'#f0c24c':'#e8eef2'}" stroke="#0b141b" stroke-width=".8"/>`)}
 if(r.id.startsWith('relation_arrow_')){const k=r.id.slice(15);return w(`<line x1="-11" y1="0" x2="9" y2="0" stroke="${RC[k]||'#ccc'}" stroke-width="2" marker-end="url(#ah-${k})"/>`)}
 const sh={control_extent:'<rect x="-10" y="-6" width="20" height="12" fill="#7a6bd0" fill-opacity=".35" stroke="#7a6bd0"/>',control_extent_approx:'<rect x="-10" y="-6" width="20" height="12" fill="#7a6bd0" fill-opacity=".18" stroke="#7a6bd0" stroke-dasharray="4 3"/>',extent_label_point:'<circle r="3.5" fill="none" stroke="#e8eef2" stroke-width="1.5"/>',contested_point:'<path d="M0,-5L5,0L0,5L-5,0Z" fill="none" stroke="#e0a63e" stroke-width="1.5"/>',contested_boundary_line:'<line x1="-11" y1="0" x2="11" y2="0" stroke="#e0a63e" stroke-width="2" stroke-dasharray="4 3"/>',boundary_line:'<line x1="-11" y1="0" x2="11" y2="0" stroke="#e8eef2" stroke-width="1.5"/>',reported_point:'<path d="M0,-5L5,4L-5,4Z" fill="none" stroke="#e0574c" stroke-width="1.5"/>',group_control_point:'<rect x="-4" y="-4" width="8" height="8" fill="#5aa9e6"/>',homeland_point:'<circle r="6.5" fill="none" stroke="#009E73" stroke-dasharray="2 1.5"/><circle r="4" fill="#009E73" fill-opacity=".6" stroke="#fff" stroke-width=".8"/>',homeland_soft_area:'<rect x="-10" y="-6" width="20" height="12" fill="#009E73" fill-opacity=".12"/>',ruin:'<circle r="3.6" fill="none" stroke="#8a8f94" stroke-width="1.3" stroke-dasharray="2 1.5"/>',list_only_text:'<text x="0" y="4" text-anchor="middle" font-size="11" fill="#9fb3c2">≡</text>'}[r.id];
 return w(sh||'<text x="0" y="4" text-anchor="middle" font-size="11" fill="#9fb3c2">?</text>')}
const LGL={ctl:()=>T.l.ctl,cty:()=>T.l.cty,grp:()=>T.l.grp,rel:()=>T.l.rel,hml:()=>T.l.hml};
let lgOpen=false;
async function legendDraw(e){const b=$('lgb'),p=$('lgp');if(!b||!p)return;const d=await lgj(e.id),sp=await LGS;if(e!==ES[i])return;
 const rows=d?d.rows.filter(r=>on.has(r.l)):[];b.textContent=`${T.lg}${rows.length?' · '+num(rows.length):''}`;b.setAttribute('aria-expanded',lgOpen);
 let h='';const ls=[...new Set(rows.map(r=>r.l))];
 if(!rows.length)h=`<p><span class="gap">${T.wip}</span> <span class="gapt">${esc(T.lgnone)}</span></p>`;
 for(const l of ls){h+=`<h4>${esc(LGL[l]?LGL[l]():l)}</h4><ul>`+rows.filter(r=>r.l===l).map(r=>`<li role="listitem" aria-label="${esc((AR?(r.ar||r.en):r.en)+' '+r.n)}">${lgSw(r)}<span>${esc(AR?(r.ar||r.en):r.en)}${AR&&r.arw?' <sup title="'+esc(T.lgarw)+'">*</sup>':''}</span><span class="n"><bdi>${num(r.n)}</bdi></span></li>`).join('')+'</ul>';
  const bd=(d.badges||{})[l]||[];if(bd.length)h+=`<p>${bd.map(x=>`<span class="repb">${esc(AR?(x.ar||(BL[x.id]&&BL[x.id][1])||x.en):(x.en!==x.id?x.en:(BL[x.id]?BL[x.id][0]:x.en)))} <bdi>${num(x.n)}</bdi></span>`).join(' ')}</p>`;
  const sr=(d.src||{})[l]||[];if(sr.length)h+=`<details class="srcs"><summary>${esc(T.lgsrc)} (${num(sr.length)})</summary><ul>${sr.map(x=>`<li dir="ltr"><bdi>${esc(x.c)}</bdi>${x.u?` <a href="${esc(x.u)}" rel="noopener">link</a>`:''}</li>`).join('')}</ul></details>`}
 if(sp&&sp.credit)h+=`<details class="cr"><summary>${esc(T.lgcred)} ⓘ</summary><p dir="ltr">${esc(sp.credit)}</p><p>${esc(AR?(sp.dis_ar||sp.dis_en):sp.dis_en)}</p></details>`;
 p.innerHTML=h;p.hidden=!lgOpen;lgFit()}
function lgFit(){const b=$('lgb'),p=$('lgp'),s=$('sheet');if(!b||!p)return;const L=$('layers').getBoundingClientRect(),N=$('nob').getBoundingClientRect();const t0=Math.max(L.bottom,N.height?N.bottom:0)+8;b.style.top=t0+'px';const bt=b.getBoundingClientRect().bottom+6;p.style.top=bt+'px';if(p.hidden)return;const S=s?s.getBoundingClientRect():null,P=p.getBoundingClientRect();const cov=S&&S.width&&S.left<P.right&&S.right>P.left;const lim=(cov?S.top:innerHeight)-bt-8;p.style.maxHeight=Math.max(120,Math.min(lim,Math.round(innerHeight*(desk()?.6:.38))))+'px'}
addEventListener('resize',lgFit);
{const b=document.getElementById('lgb');if(b)b.onclick=ev=>{ev.stopPropagation();lgOpen=!lgOpen;b.setAttribute('aria-expanded',lgOpen);document.getElementById('lgp').hidden=!lgOpen;lgFit()}}
document.addEventListener('DOMContentLoaded',()=>{});
function cityThin(){const e=ES[i],W=svg.node().clientWidth||390,H=svg.node().clientHeight||600,sr=svg.node().getBoundingClientRect(),boxes=[...gT.selectAll('text').nodes(),...gK.selectAll('text').nodes()].filter(t=>t.style.display!=='none'&&t.getAttribute('visibility')!=='hidden').map(t=>{const b=t.getBoundingClientRect();return [b.left-sr.left-2,b.top-sr.top-2,b.right-sr.left+2,b.bottom-sr.top+2]}).filter(b=>b[2]>b[0]);
 const g=gY.selectAll('g.cty:not(.gone)').nodes().map(n=>({n,c:d3.select(n).datum()}));
 g.sort((a,b)=>(isKey(b.c)-isKey(a.c))||(b.c.cap-a.c.cap)||((!!b.c.r[e.id])-(!!a.c.r[e.id]))||String(a.c.id).localeCompare(b.c.id));
 const hit=(a,b)=>a[0]<b[2]&&a[2]>b[0]&&a[1]<b[3]&&a[3]>b[1];
 g.forEach(({n,c})=>{const p=TR.apply(n.__xy),w=cName(c).length*(AR?6:6.6)+10;let bx=AR?[p[0]-9-w,p[1]-9,p[0]+5,p[1]+6]:[p[0]-5,p[1]-9,p[0]+9+w,p[1]+6];
  let bx2=bx,fl=false;if(isKey(c)&&(bx[2]>W||bx[0]<0)){fl=true;bx2=AR?[p[0]-5,bx[1],p[0]+9+w,bx[3]]:[p[0]-9-w,bx[1],p[0]+5,bx[3]]}bx=bx2;const t=n.querySelector('text');t.setAttribute('x',(AR!==fl)?-9:9);t.setAttribute('text-anchor',fl?'end':'start');
  const ok=bx[0]>=0&&bx[2]<=W&&bx[1]>=0&&bx[3]<=H&&(isKey(c)||!boxes.some(b=>hit(b,bx)));if(ok)boxes.push(bx);n.querySelector('text').style.display=ok?'':'none'})}
function cityTap(ev,c){ev.stopPropagation();const e=ES[i],r=c.r[e.id],d=CJ&&CJ.then?null:null;
 const B=x=>`<span class="repb${x==='CONTESTED'?' cont':x==='SINGLE-SOURCE'?' single':''}">${esc(BL[x]?BL[x][AR?1:0]:x)}</span>`;
 const rk=r&&RK[r.k],role=r?(AR?(r.ar||(rk&&rk[1])||r.en):(rk?rk[0]:(r.en||r.ar))):null;
 $('feat').innerHTML=`<button class="x" aria-label="close">×</button><b>${esc(cName(c))}</b>${r&&r.cap?` <span class="capb">★ ${esc(T.capital)}</span>`:''} ${(c.b||[]).map(B).join(' ')}`+
  `<br><small>${esc(c.fb&&c.fb!=='founded'?T.firstatt:T.founded)}: <bdi>${fy(c.f)}</bdi>${c.fc?` [${esc(c.fc)}]`:''}${c.a!=null?` · ${esc(c.vb&&T['vb_'+c.vb]||T.abandoned)}: <bdi>${fy(c.a)}</bdi>`:(c.ru?` · ${esc(T.oe)}`:'')}</small>`+
  `<p><b>${esc(T.role)}:</b> ${role?esc(role):`<span class="gap">${esc(T.norole)}</span>`}</p>`+
  ((AR?(c.h_ar||c.h_en):(c.h_en||c.h_ar))?`<p>${esc(AR?(c.h_ar||c.h_en):(c.h_en||c.h_ar))}</p>`:'')+
  `<p class="extnote">${c.s.map(x=>`<bdi dir="ltr">${esc(x.c)}${x.p?' · '+esc(x.p):''}</bdi>${x.u?` <a href="${esc(x.u)}" rel="noopener">link</a>`:''}`).join('<br>')}${r&&r.s&&r.s.length?`<br><small>${esc(T.role)}: <bdi dir="ltr">${r.s.map(esc).join(', ')}</bdi></small>`:''}</p>`+
  (M.layers.cStub?`<p class="gap">${esc(T.stub)}</p>`:'');
 $('feat').hidden=false;$('feat').querySelector('.x').onclick=()=>{$('feat').hidden=true};if($('sheet').classList.contains('peek'))snap('half')}
// --- navigation
// era camera: fly to focus_view.bbox [w,s,e,n] (fallback: extent bounds, then whole region) inside the area not covered by the sheet/side card. Manual zoom is kept until the era changes.
let CE=null;function cam(e,g){if(e.id===CE)return;const first=CE===null;CE=e.id;
 let b=e.fv;if(!b&&g&&g.features&&g.features.length){const q=d3.geoBounds({type:'FeatureCollection',features:g.features});if(q.every(p=>p.every(isFinite)))b=[q[0][0],q[0][1],q[1][0],q[1][1]]}
 let t=d3.zoomIdentity;if(b){const sh=$('sheet').getBoundingClientRect(),top=desk()?70:120,bot=desk()?H()-20:Math.max(top+120,H()-Math.min(sh.height,H()*.44)-8),x1=desk()?(AR?sh.right+20:20):10,x2=desk()?(AR?W()-20:sh.left-20):W()-10;
  {const cx=(b[0]+b[2])/2,cy=(b[1]+b[3])/2,hx=Math.max((b[2]-b[0])/2,1.5),hy=Math.max((b[3]-b[1])/2,1.5);b=[cx-hx,cy-hy,cx+hx,cy+hy]}// min 3° window so point-like foci keep context
  const p=proj([b[0],b[3]]),q=proj([b[2],b[1]]),dx=Math.max(q[0]-p[0],8),dy=Math.max(q[1]-p[1],8);const k=Math.max(1,Math.min(6,.85*Math.min((x2-x1)/dx,(bot-top)/dy)));
  t=k<1.02?d3.zoomIdentity:d3.zoomIdentity.translate((x1+x2)/2-k*(p[0]+q[0])/2,(top+bot)/2-k*(p[1]+q[1])/2).scale(k)}
 if(first||RM)svg.interrupt().call(zoom.transform,t);else svg.interrupt().transition('cam').duration(1000).call(zoom.transform,t)}
function go(n){n=Math.max(0,Math.min(ES.length-1,n));if(n===i)return;i=n;Y=null;render(true)}
r.addEventListener('input',()=>go(+r.value));$('prev').onclick=()=>go(i-1);$('next').onclick=()=>go(i+1);
$('w').addEventListener('input',()=>{const e=ES[i];ext(e).then(g=>{Y=steps(e,g)[+$('w').value];render(true)})});
addEventListener('keydown',ev=>{if(ev.target.tagName==='INPUT')return;if(ev.key==='ArrowRight')go(i+(AR?-1:1));if(ev.key==='ArrowLeft')go(i+(AR?1:-1))});
let sx=null;const hd=$('head');hd.addEventListener('pointerdown',ev=>{sx=ev.clientX});hd.addEventListener('pointerup',ev=>{if(sx==null)return;const d=ev.clientX-sx;sx=null;if(Math.abs(d)>50)go(i+((d<0)!==AR?1:-1))});
const SN=['peek','half','full'];function snap(s){document.body.classList.toggle('sfull',s==='full');setTimeout(lgFit,350);const sh=$('sheet');SN.forEach(c=>sh.classList.remove(c));sh.classList.add(s);setTimeout(place,320)}
$('grab').onclick=()=>{const sh=$('sheet'),c=SN.find(x=>sh.classList.contains(x))||'half';snap(SN[(SN.indexOf(c)+1)%3])};
let rt;addEventListener('resize',()=>{clearTimeout(rt);rt=setTimeout(()=>{fit();OLD=[];render(false)},150)});
// era flags (db/era_symbols.json via db/legends/eras layers.flags): shown at era_focus flag_anchor only while the slider year is inside a used window; joint flags side by side; VERIFY = dashed frame + chip
function flagsDraw(e){const fl=e.fl,y=cY(),fs=fl?fl.f.filter(f=>f.w.some(w=>w[0]<=y&&y<=w[1])):[];const d=fs.length?[e.id+'|'+fs.map(f=>f.s).join()]:[];
 const s=gF.selectAll('g.flag').data(d,x=>x);s.exit().remove();
 const n=s.enter().append('g').attr('class','flag mk').each(function(){this.__xy=proj(fl.a)}).attr('transform',function(){return `translate(${this.__xy})scale(${1/K})`});
 n.each(function(){const g=d3.select(this),FW=22,FH=15,gap=3,tw=fs.length*FW+(fs.length-1)*gap;g.append('title').text((AR?'العلم':'Flag')+(fs.some(f=>f.v)?' · VERIFY':''));
  fs.forEach((f,j)=>{const x=-tw/2+j*(FW+gap),y0=-FH-6;g.append('rect').attr('class','fbd'+(f.v?' vfy':'')).attr('x',x-1).attr('y',y0-1).attr('width',FW+2).attr('height',FH+2);g.append('image').attr('href',f.s).attr('x',x).attr('y',y0).attr('width',FW).attr('height',FH).attr('preserveAspectRatio','none')});
  g.append('line').attr('x1',0).attr('x2',0).attr('y1',-6).attr('y2',0).attr('class','fpole');
  if(fs.some(f=>f.v))g.append('text').attr('class','fvchip').attr('x',0).attr('y',-FH-9).attr('text-anchor','middle').text('VERIFY')})}
// --- start
window.__hm={scale:k=>svg.call(zoom.scaleTo,k)};// test hook (QA only, no side effects)
fit();getj('/basemap-map.json').then(b=>{BASE=b;render(false)}).catch(()=>render(false));
})();

