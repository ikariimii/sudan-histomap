// Sudan Histomap: one continuous map page. All data comes from window.MAP (built from data/eras + db/extents by web/build.py)
// and per-era files (/extents/<id>.json, /m/<id>.json). Nothing is invented; missing layers show 'Research in progress'.
(function(){
const M=window.MAP,Q=new URLSearchParams(location.search),L=/^\/ar\//.test(location.pathname)||Q.get('lang')==='ar'?'ar':'en',AR=L==='ar',T=M.t[L],ES=M.eras;
const RM=matchMedia('(prefers-reduced-motion: reduce)').matches,DUR=RM?0:650;
const $=id=>document.getElementById(id),esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const num=n=>AR?String(n).replace(/\d/g,d=>'٠١٢٣٤٥٦٧٨٩'[d]):String(n);
const fy=y=>y>=2026?(AR?'اليوم':'present'):y<0?num(-y)+(AR?' ق.م':' BCE'):num(y)+(AR?' م':' CE');
const BL={REPORTED:['REPORTED','مُبلَّغ عنه','#e0574c'],CONTESTED:['CONTESTED','متنازع عليها','#b07ae0'],'SINGLE-SOURCE':['SINGLE-SOURCE','مصدر واحد','#e0a63e'],VERIFY:['VERIFY','يحتاج تحقق *','#e0a63e']};const VFL=AR?'هذه المعلومة تحتاج إلى تحقق *':'Needs verification';/* 'مصدر واحد' pending native review */
const rep=p=>{const b=String(p.badge||'').toUpperCase().split(' (')[0];return BL[b]?b:''};
const unrep=s=>String(s||'').replace(/\s*\[(REPORTED|CONTESTED|مُبلَّغ عنه|متنازع عليها)\]/g,'');
const lab=p=>unrep(AR?(p.label_ar||p.label_en):(p.label_en||p.label_ar));
const short=s=>{s=String(s).split(/ [–—] /)[0];if(s.length>34)s=s.split(/[(（,،:]/)[0].trim();return s.length>40?s.slice(0,38)+'…':s};
// --- chrome
document.title=T.title+' · '+(AR?'Sudan Histomap':'خريطة تاريخ السودان');
$('brand').textContent=T.title;$('about').textContent=T.about;$('about').href=(AR?'/ar':'')+'/about/';
const lq=new URLSearchParams(Q);lq.delete('lang');const lsw=()=>{const q=new URLSearchParams(location.search);q.delete('lang');const s=q.toString();return (AR?'/':'/ar/')+(s?'?'+s:'')};$('lang').textContent=T.lang;$('lang').setAttribute('hreflang',AR?'en':'ar');
$('lang').addEventListener('click',e=>{e.preventDefault();location.href=lsw()});
$('lang').href=(AR?'/':'/ar/')+(lq.toString()?'?'+lq:'');$('prev').setAttribute('aria-label',T.prev);$('next').setAttribute('aria-label',T.next);$('grab').setAttribute('aria-label',T.sheet);
$('skip').textContent=T.skip;$('map').setAttribute('aria-label',T.mapl);$('svg').setAttribute('aria-label',T.mapl+'. '+T.featl);$('svgt').textContent=T.mapl;$('layers').setAttribute('aria-label',T.layersl);
$('grab').setAttribute('aria-label',T.sheet+' · '+T.sheetst.half);$('grab').setAttribute('aria-expanded','true');
$('reset').title=T.reset;$('reset').setAttribute('aria-label',T.reset);$('within').querySelector('label').textContent=T.within;
const LAY=['ctl','grp','rel','eth','pop','cty','hml','trd','evd','now'].concat(M.layers.bat?['bat']:[]),on=new Set((Q.get('layers')||'ctl').split(',').map(x=>x==='cities'?'cty':x==='homelands'?'hml':x==='trade'?'trd':x==='evidence'?'evd':x==='then-now'?'now':x==='battles'?'bat':x).filter(x=>LAY.includes(x)));
LAY.forEach(k=>{const b=document.createElement('button');b.className='chip';b.type='button';b.textContent=T.l[k]||(k==='bat'?(AR?'المعارك *':'Battles'):k);b.setAttribute('aria-pressed',on.has(k));b.dataset.k=k;if(k==='trd')b.setAttribute('aria-label',T.l.trd_aria);
 b.onclick=()=>{on.has(k)?on.delete(k):on.add(k);if(k==='eth'&&on.has(k))eth1932();b.setAttribute('aria-pressed',on.has(k));url();if(k==='evd'){evdStyle();layerInfo(ES[i]);return}if(k==='now'){cmpDraw();return}render(false);if(k==='hml')hmlDraw()};$('layers').appendChild(b)});
document.addEventListener('click',ev=>{const t=ev.target.closest&&ev.target.closest('[data-hml]');if(!t)return;ev.preventDefault();if(!on.has('hml')){on.add('hml');const c=document.querySelector('#layers .chip[data-k=hml]');if(c)c.setAttribute('aria-pressed','true');url();render(false);hmlDraw()}});
// --- era index
let i=Math.max(0,ES.findIndex(e=>e.id===Q.get('era')));const r=$('r');r.max=ES.length-1;r.value=i;r.setAttribute('aria-label',T.era);
function url(){const q=new URLSearchParams();q.set('era',ES[i].id);if(STY)q.set('story',STY.s);if(Q.get('embed')==='1')q.set('embed','1');const ly=[...on].sort().concat(BDQ?['borders-draft']:[]).join(',');if(ly!=='ctl')q.set('layers',ly);history.replaceState(null,'',(AR?'/ar/':'/')+'?'+q)}
// --- map
const svg=d3.select('#svg'),W=()=>innerWidth,H=()=>innerHeight,desk=()=>innerWidth>=1000;
const root=svg.append('g'),gB=root.append('g').attr('class','relief'),gZ=root.append('g').attr('class','zones'),gL=root.append('g'),gC=root.append('g'),gX=root.append('g'),gN=root.append('g'),gG=root.append('g'),gH=root.append('g').attr('class','hml'),gY=root.append('g').attr('class','cities'),gR=root.append('g'),gP=root.append('g'),gK=root.append('g'),gT=root.append('g'),gF=root.append('g').attr('class','flags');
svg.append('defs').html('<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="#f08c6c"/></marker>');
const proj=d3.geoMercator(),path=d3.geoPath(proj);let K=1,TR=d3.zoomIdentity;
// topographic basemap: Natural Earth relief pre-rendered in Web Mercator over RELIEF_BOX (web/basemap/make_relief.py); placed by its corners, so the root zoom transform keeps it aligned. 900px by default, 1800px once zoomed in or on desktop.
const RELIEF_BOX=[12,-3,48,27];let RHI=false;function relief(){const a=proj([RELIEF_BOX[0],RELIEF_BOX[3]]),b=proj([RELIEF_BOX[2],RELIEF_BOX[1]]);if(!RHI&&(K>=2||desk()))RHI=true;gB.selectAll('image').data([RHI?'/img/relief-1800.webp':'/img/relief-900.webp']).join('image').attr('href',d=>d).attr('x',a[0]).attr('y',a[1]).attr('width',b[0]-a[0]).attr('height',b[1]-a[1]).attr('preserveAspectRatio','none')}
function fit(){const sh=$('sheet').getBoundingClientRect();const top=desk()?70:120,bot=desk()?H()-20:Math.max(top+160,H()-Math.min(sh.height,H()*.44)-8);
 const x1=desk()?(AR?sh.right+20:20):10,x2=desk()?(AR?W()-20:sh.left-20):W()-10;
 proj.fitExtent([[x1,top],[x2,bot]],{type:'MultiPoint',coordinates:[[21.8,3.4],[38.6,22.2]]});relief()}
const zoom=d3.zoom().scaleExtent([1,12]).on('zoom',ev=>{TR=ev.transform;root.attr('transform',ev.transform);K=ev.transform.k;scaleMarks();cmpClip();rsHide(K<1.05&&Math.abs(ev.transform.x)<2)}).on('end',()=>{if(!RHI&&K>=2)relief();place();cityThin();hmlDraw()});
svg.call(zoom).on('dblclick.zoom',null);
// labels are placed in screen space by place(): keep their group outside the zoomed root (else K is applied twice) and hide it mid-zoom
svg.node().appendChild(gT.node());zoom.on('start.lb',()=>gT.style('display','none'));$('reset').onclick=()=>svg.transition().duration(DUR).call(zoom.transform,d3.zoomIdentity);
// WCAG 2.4.3: never hide #reset while it holds focus; hand focus to the era scrubber, else #tour
function rsHide(h){const rs=$('reset');if(!rs||rs.hidden===h)return;if(h&&document.activeElement===rs){const vis=e=>e&&!e.hidden&&!e.disabled&&e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden';const t=[$('r'),$('tour')].find(vis);if(t)t.focus({preventScroll:true})}rs.hidden=h}
function scaleMarks(){root.selectAll('.mk').attr('transform',function(){return `translate(${this.__xy})scale(${1/K})`});clearTimeout(scaleMarks.t);scaleMarks.t=setTimeout(()=>{if(typeof hmlThin==='function')hmlThin()},120)}
const rw=f=>{const G=f.geometry,rv=a=>a.slice().reverse();if(G.type==='Polygon'){if(d3.geoArea(f)>2*Math.PI)G.coordinates=G.coordinates.map(rv)}else if(G.type==='MultiPolygon')G.coordinates=G.coordinates.map(p=>d3.geoArea({type:'Polygon',coordinates:p})>2*Math.PI?p.map(rv):p);return f};
let BASE=null;const C={},CARD={},LD={};
const getj=u=>fetch(u).then(x=>{if(!x.ok)throw new Error(u+' '+x.status);return x.json()});
function ext(e){if(!e.x)return Promise.resolve({features:[],lines:[]});return C[e.id]||(C[e.id]=getj('/extents/'+e.id+'.json').then(g=>{g.features.forEach(f=>{if(f.geometry.type!=='Point')rw(f)});g.lines=g.lines||[];return g}).catch(()=>({features:[],lines:[]})))}
// neighbour prefetch: once the current era has drawn and the browser is idle, warm the per-era files of the eras either side
// (skipped on Save-Data / 2G). Same fetch caches as on demand, so a prefetched era is not downloaded twice.
function prefetch(k){const n=navigator.connection;if(n&&(n.saveData||/2g/.test(n.effectiveType||'')))return;clearTimeout(prefetch.t);prefetch.t=setTimeout(()=>(window.requestIdleCallback||setTimeout)(()=>{if(k!==i)return;[k+1,k-1].forEach(x=>{const e=ES[x];if(!e)return;ext(e);cardj(e);if(typeof lgj==='function')lgj(e.id)})}),1200)}
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
 const ss=BASE.features.find(d=>d.properties.name==='S. Sudan');gC.selectAll('text').data(post&&ss?[ss]:[]).join('text').attr('class','cl mk').attr('text-anchor','middle').style('display',null).each(function(d){this.__xy=path.centroid(d)}).attr('transform',function(){return `translate(${this.__xy})scale(${1/K})`}).text(T.ssd)}// counter-scaled like markers so the label stays 11px during fly/zoom
let OLD=[];// previously drawn area features [{f,d,box}]
async function render(anim=true){
 const e=ES[i];r.value=i;url();const g=await ext(e);if(e!==ES[i])return;
 cam(e,g);
 const st=steps(e,g);if(Y==null||Y<e.a||Y>e.b)Y=st[st.length-1];ST=st;
 const wi=$('within');wi.hidden=st.length<2;if(st.length>1){const w=$('w');w.min=0;w.max=st.length-1;w.value=Math.max(0,st.findIndex(s=>s===Y));$('wo').textContent=fy(Y)}
 document.documentElement.style.setProperty('--c',e.c);
 $('en').textContent=AR?e.ar:e.en;r.setAttribute('aria-valuetext',`${AR?e.ar:e.en}${AR?'،':','} ${fy(e.a)} – ${fy(e.b)}`);if(render.last!==e.id){if(render.last)$('live').textContent=`${AR?e.ar:e.en}. ${fy(e.a)} – ${fy(e.b)}. ${num(i+1)} ${T.live_of} ${num(ES.length)}`;render.last=e.id}$('yrs').innerHTML=`<bdi>${fy(e.a)}</bdi> – <bdi>${fy(e.b)}</bdi> · ${esc(AR?e.sa:e.s)} · ${num(i+1)}/${num(ES.length)}`;
 $('nob').innerHTML=e.g==='pts'?`<span class="pts"${AR?' title="Arabic label under native-speaker review"':''}>${T.pts}</span>`:e.g==='none'?`<span class="none">${T.none}</span>`:e.g==='hml'?`<button type="button" class="hmlb" data-hml="1" aria-pressed="${on.has('hml')}">${AR?'معروض على طبقة الأوطان *':'Shown on the Homelands layer'}</button>`:'';if(BD)$('nob').insertAdjacentHTML('beforeend',`<span class="bdb" role="note">${esc(T.bd.badge)}</span>`);
 drawBase(e);
 const ctl=on.has('ctl'),areas=ctl?g.features.filter(f=>f.geometry.type!=='Point'&&!f.properties.zone&&act(f.properties,e,Y)):[],pts=ctl?g.features.filter(f=>f.geometry.type==='Point'&&act(f.properties,e,Y)):[];
 // areas: morph matched shapes, crossfade the rest
 const D=anim?(RM?240:DUR):0,NEW=areas.map(f=>({f,box:bbox(f)})),used=new Set();
 gX.selectAll('path.ext').interrupt().remove();gX.selectAll('path.old').interrupt().remove();
 NEW.forEach(n=>{let bi=-1,bv=.25;OLD.forEach((o,k)=>{if(used.has(k))return;const v=iou(o.box,n.box);if(v>bv){bv=v;bi=k}});n.m=bi;if(bi>=0)used.add(bi)});
 OLD.forEach((o,k)=>{if(used.has(k)||!D)return;gX.append('path').attr('class','ext old').attr('d',path(o.f)).style('opacity',1).transition().duration(D).style('opacity',0).remove()});
 NEW.forEach(n=>{const p=gX.append('path').attr('class','ext'+(String(n.f.properties.certainty||'').toLowerCase()==='low'?' low':'')).datum(n.f).on('click',(ev)=>{ev.stopPropagation();feat(n.f,e)});
  if(D&&!RM&&n.m>=0){const a=resample(ringOf(OLD[n.m].f)),b=align(a,resample(ringOf(n.f)));const it=d3.interpolateArray(a,b);p.attr('d',dpts(a)).transition().duration(D).ease(d3.easeCubicInOut).attrTween('d',()=>t=>dpts(it(t))).on('end',function(){d3.select(this).attr('d',path(n.f))})}
  else{p.attr('d',path(n.f)).style('opacity',D?0:1);if(D)p.transition().duration(D).style('opacity',1)}});
 OLD=NEW.map(n=>({f:n.f,box:n.box}));evdStyle();cmpDraw();
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
 await layersDraw(e);batDraw(e);if(gEp)gEp.selectAll('*').remove();if(on.has('hml'))hmlDraw();prefetch(i);zonesDraw(e,D,ctl?g.features.filter(f=>f.properties.zone&&f.geometry.type!=='Point'):[]);
 // card
 const cj=await cardj(e);if(e!==ES[i])return;$('card').innerHTML=cj?cj[L]:`<p><span class="gap">${T.wip}</span></p>`;evList(e);shareBtn(e);layerInfo(e);msPanel(e);$('feat').hidden=true;
 place()}
render.last=null;let LBS=[];
new MutationObserver(()=>{const x=$('feat').querySelector('.x');if(x)x.setAttribute('aria-label',T.close)}).observe($('feat'),{childList:true});
// keyboard access to map features: every tappable mark is a focusable button named by its <title>
const FSEL='g.bt,path.zn,g.pt,path.ext,path.ln,g.cty,g.hm,g.grp,path.rel';function a11yMarks(){root.selectAll(FSEL).each(function(){const t=this.querySelector('title');const l=(t&&t.textContent)||this.getAttribute('aria-label')||(this.__data__&&this.__data__.properties&&lab(this.__data__.properties))||'';if(!l){this.removeAttribute('tabindex');return}this.setAttribute('tabindex','0');this.setAttribute('role','button');this.setAttribute('aria-label',l)})}
let LASTF=null;svg.on('keydown.a11y',ev=>{const t=ev.target;if(!(t.matches&&t.matches(FSEL)))return;if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();LASTF=t;t.dispatchEvent(new MouseEvent('click',{bubbles:true}));setTimeout(()=>{if(!$('feat').hidden)$('feat').focus()},60)}});
new MutationObserver(()=>{clearTimeout(a11yMarks.t);a11yMarks.t=setTimeout(a11yMarks,80)}).observe(document.getElementById('svg'),{childList:true,subtree:true});
function nobPos(){const b=$('layers').getBoundingClientRect();document.documentElement.style.setProperty('--chipb',Math.round(b.bottom)+'px');$('nob').style.top=(b.bottom+6)+'px';setTimeout(lgFit,0)}
function place(){setTimeout(cityThin,0);nobPos();const t=TR;gT.style('display',null).selectAll('*').remove();const placed=[],hid=[];
 // obstacles: the card and the top chrome
 const ob=['sheet','top','layers','nob'].map(id=>$(id).getBoundingClientRect()).filter(b=>b.width).map(b=>({x:b.left,y:b.top,w:b.width,h:b.height}));
 root.selectAll('.mk').nodes().forEach(n=>{const s=n.querySelector('rect,circle,path');if(!s)return;const b=s.getBoundingClientRect();if(b.width)ob.push({x:b.left+1,y:b.top+1,w:Math.max(0,b.width-2),h:Math.max(0,b.height-2)})});
 gC.selectAll('text.cl').nodes().forEach(n=>{if(n.style.display==='none')return;const b=n.getBoundingClientRect();if(b.width)ob.push({x:b.left-2,y:b.top-1,w:b.width+4,h:b.height+2})}); // country label (S. Sudan) is an obstacle too
 const ov=(a,c)=>a.x<c.x+c.w&&c.x<a.x+a.w&&a.y<c.y+c.h&&c.y<a.y+a.h;
 LBS.slice().sort((a,b)=>b.pri-a.pri).forEach(o=>{const sx=t.applyX(o.xy[0]),sy=t.applyY(o.xy[1]);if(sx<0||sx>W()||sy<0||sy>H()){return}
  const gg=gT.append('g').attr('transform',`translate(${sx},${sy})`);const tx=gg.append('text').attr('class','lb'+(o.big?' big':'')).text(o.t);if(o.t===T.ssd)gC.selectAll('text.cl').style('display','none');
  if(o.rep&&!BL[o.rep].slice(0,2).some(w=>o.t.includes(w))&&!(o.rep==='CONTESTED'&&/disputed/i.test(o.t))){tx.append('tspan').attr('class','rep').attr('fill',BL[o.rep][2]).text(' '+BL[o.rep][AR?1:0])}
  const lh=16,dx0=o.dx?(AR?-o.dx:o.dx):0,an0=o.big?'middle':'start';let ok=null;
  P:for(const k of [0,1,-1,2,-2,3,-3])for(const side of (o.dx?[0,1]:[0])){const dx=side?-dx0:dx0,an=o.big?'middle':(side?'end':'start');tx.attr('x',dx).attr('y',4+k*lh).attr('text-anchor',an);
   const b=tx.node().getBoundingClientRect(),bb={x:b.left-2,y:b.top-1,w:b.width+4,h:b.height+2};if(bb.x<2||bb.x+bb.w>W()-2)continue;if(!placed.some(p=>ov(p,bb))&&!ob.some(p=>ov(p,bb))){ok={k,dx,bb,an};break P}}
  if(!ok){gg.remove();hid.push(o);return}tx.attr('x',ok.dx).attr('y',4+ok.k*lh).attr('text-anchor',ok.an);placed.push(ok.bb);
  if(ok.k!==0&&o.pri>=2.5)gg.insert('line','text').attr('class','ld').attr('x1',0).attr('y1',0).attr('x2',ok.dx).attr('y2',ok.k*lh+(ok.k<0?2:-8))});
 $('hidden').innerHTML=hid.length?T.hidden+': '+[...new Set(hid.map(o=>o.t))].map(esc).join(AR?'، ':', '):''}
// --- Evidence mode (?layers=evd): areas fade by their confidence score and are hatched below 0.5; no score = faint dashed outline. Tap shows cite + pages.
const gEv=root.insert('g',function(){return gX.node().nextSibling}).attr('class','evh').attr('pointer-events','none');
const cf=p=>typeof p.confidence==='number'?p.confidence:null;
function evdStyle(){zdefs();const ev=on.has('evd');document.body.classList.toggle('evd',ev);gEv.selectAll('*').remove();
 [...gX.selectAll('path.ext:not(.old)').nodes(),...gZ.selectAll('path.zn').nodes()].forEach(function(n){const f=n.__data__;(function(){const zn=this.classList.contains('zn');const c=f?cf(f.properties):null,s=this.style;if(!ev){s.fillOpacity='';s.strokeDasharray='';s.strokeOpacity='';return}
  s.fillOpacity=c==null?'.06':String(.08+.5*c);s.strokeOpacity=c==null?'.6':String(.4+.6*c);s.strokeDasharray=c==null?'2 4':(c<.5?'6 4':'');
  if(!zn&&c!=null&&c<.5)gEv.append('path').attr('d',this.getAttribute('d')).attr('fill','url(#lowconf)').style('opacity',.9*(1-c))}).call(n)})}
// --- Then and now (?layers=now): range splits the screen; historical areas on one side, today's borders (the existing
// Natural Earth admin-0 basemap, BASE) on the other. No new geometry. Native range = keyboard; no animation (reduced-motion safe).
const gNow=root.append('g').attr('class','nowb').attr('pointer-events','none');let CMP=50;
function cmpY(){let t=0,b=H();for(const id of ['layers','lgb','hint','lgp','nob','reset','wai']){const e=$(id);if(e&&!e.hidden&&getComputedStyle(e).display!=='none'){const r=e.getBoundingClientRect();if(r.height&&r.bottom<H()*.8)t=Math.max(t,r.bottom)}}const sh=$('sheet');if(sh&&!desk()){const r=sh.getBoundingClientRect();b=Math.min(b,r.top)}return b-t>=52?Math.round((t+b)/2):$('hint')?null:Math.round(H()*.42)}
function cmpDiv(s){cmpDiv.s=s;let g=svg.select('g.cmpdv');if(s==null){g.remove();cmpPos();return}
 if(g.empty()){g=svg.append('g').attr('class','cmpdv').attr('aria-hidden','true');g.append('line');const h=g.append('g').attr('class','cmph');h.append('circle').attr('class','hit').attr('r',22);h.append('circle').attr('class','knob').attr('r',14);h.append('path').attr('d','M-5,-5l-4,5l4,5M5,-5l4,5l-4,5');
  const hn=h.node();let dr=false;const mv=ev=>{if(!dr)return;const p=Math.max(0,Math.min(100,Math.round(100*ev.clientX/W())));CMP=AR?100-p:p;const r=$('cmpr');if(r){r.value=CMP;r.oninput()}};
  ['mousedown','touchstart','wheel'].forEach(t=>hn.addEventListener(t,ev=>ev.stopPropagation(),{passive:true}));hn.addEventListener('pointerdown',ev=>{ev.stopPropagation();ev.preventDefault();dr=true;try{hn.setPointerCapture(ev.pointerId)}catch(_){}});hn.addEventListener('pointermove',mv);['pointerup','pointercancel'].forEach(t=>hn.addEventListener(t,()=>{dr=false}));cmpPos();setTimeout(cmpPos,700);if(!cmpDiv.l){cmpDiv.l=1;const sh=$('sheet');if(sh)sh.addEventListener('transitionend',()=>{if(cmpDiv.s!=null)cmpPos()})}}
 g.select('line').attr('x1',s).attr('x2',s).attr('y1',0).attr('y2',H());{const y=cmpY();g.select('.cmph').style('display',y==null?'none':null).attr('transform',`translate(${s},${y||0})`)}}
// keep the corner buttons clear of the open then/now bar (it lives inside #layers)
function cmpPos(){const b=$('cmpbar'),o=b&&!b.hidden,lb=$('layers').getBoundingClientRect().bottom;const rs=$('reset'),wa=$('wai');if(rs)rs.style.top=o?(lb+8)+'px':'';if(wa)wa.style.top=o?(lb+56)+'px':'';nobPos();if(cmpDiv.s!=null){const h=svg.select('g.cmpdv .cmph');if(!h.empty()){const y=cmpY();h.style('display',y==null?'none':null).attr('transform',`translate(${cmpDiv.s},${y||0})`)}}}
function cmpClip(){const d=svg.select('defs');if(!on.has('now')){gX.attr('clip-path',null);gZ.attr('clip-path',null);gNow.attr('clip-path',null);cmpDiv(null);return}
 ['cThen','cNow'].forEach(id=>{if(d.select('#'+id).empty())d.append('clipPath').attr('id',id).attr('clipPathUnits','userSpaceOnUse').append('rect')});
 const s=AR?W()*(1-CMP/100):W()*CMP/100,x=(s-TR.x)/TR.k,BIG=1e5,L=[-BIG,x-(-BIG)],R=[x,BIG];const th=AR?R:L,nw=AR?L:R;
 d.select('#cThen rect').attr('x',th[0]).attr('width',th[1]).attr('y',-BIG).attr('height',2*BIG);d.select('#cNow rect').attr('x',nw[0]).attr('width',nw[1]).attr('y',-BIG).attr('height',2*BIG);
 gX.attr('clip-path','url(#cThen)');gZ.attr('clip-path','url(#cThen)');gNow.attr('clip-path','url(#cNow)');cmpDiv(s)}
function cmpDraw(){const ok=on.has('now')&&BASE;let b=$('cmpbar');gNow.selectAll('*').remove();
 if(!ok){if(b)b.hidden=true;cmpClip();cmpPos();return}
 if(!b){b=document.createElement('div');b.id='cmpbar';b.innerHTML=`<span>${esc(T.cmp.then)}</span><input id="cmpr" type="range" min="0" max="100" step="1" aria-label="${esc(T.cmp.aria)}"><span>${esc(T.cmp.now)}</span><small>${esc(T.cmp.src)}${BASE.source?': <bdi dir="ltr">'+esc(typeof BASE.source==='string'?BASE.source:(BASE.source.name||BASE.source.citation||''))+'</bdi>':''}</small>`;$('layers').append(b);
  const r=b.querySelector('input');r.value=CMP;r.oninput=()=>{CMP=+r.value;r.setAttribute('aria-valuetext',`${T.cmp.then} ${num(CMP)}% · ${T.cmp.now} ${num(100-CMP)}%`);cmpClip()};r.oninput()}
 b.hidden=false;gNow.selectAll('path').data(BASE.features).join('path').attr('d',path);cmpClip();cmpPos()}
// --- 1932 ethnographic label markers (?layers=eth): per-era /eth/<id>.json; dashed unfilled halo, never an area.
const gEt=root.append('g').attr('class','eth'),ETH={};
async function ethDraw(e){const has=(M.layers.eth||[]).includes(e.id),c=document.querySelector('#layers .chip[data-k=eth]');if(c)c.hidden=!has;gEt.selectAll('*').remove();if(!has||!on.has('eth'))return;
 const d=ETH[e.id]||(ETH[e.id]=await fetch('/eth/'+e.id+'.json').then(r=>r.ok?r.json():[]).catch(()=>[]));if(e!==ES[i])return;
 d.filter(m=>m.pre==null||(e.a<m.pre&&(Y==null||Y<m.pre))).forEach(m=>{const [x,y]=proj(m.c),r=Math.abs(proj([m.c[0],m.c[1]+m.km/111])[1]-y);const g=gEt.append('g').attr('class','ethm').attr('tabindex',0).attr('role','button').attr('aria-label',`${m.n}: ${T.ethcap}`).on('click',ev=>{ev.stopPropagation();ethCard(m)}).on('keydown',ev=>{if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();ethCard(m)}});
  g.append('circle').attr('cx',x).attr('cy',y).attr('r',r).attr('fill','none').attr('stroke','#c9a227').attr('stroke-opacity',m.op).attr('stroke-width',1.4).attr('stroke-dasharray','5 4').attr('vector-effect','non-scaling-stroke');
  g.append('circle').attr('cx',x).attr('cy',y).attr('r',3).attr('fill','#c9a227');
  g.append('text').attr('x',x).attr('y',y-6).attr('text-anchor','middle').attr('class','ethl').text(m.n)})}
function ethCard(m){$('feat').innerHTML=`<button class="x" aria-label="${esc(T.close)}">×</button><b lang="en">${esc(m.n)}</b> ${m.b.map(x=>`<span class="repb"${x==='VERIFY'?` aria-label="${esc(VFL)}"`:''}>${esc(BL[x]?BL[x][AR?1:0]:x)}</span>`).join(' ')}<p>${esc(AR?(m.cap_ar||T.ethcap):T.ethcap)}${AR&&!m.cap_ar?` <span class="repb">${esc(BL.VERIFY?BL.VERIFY[1]:'VERIFY')}</span>`:''}</p>${m.dn&&!AR?`<p><small>${esc(m.dn)}</small></p>`:''}<p class="extnote"><bdi dir="ltr">${esc(m.src)}${m.pl?' · '+esc(m.pl):''}</bdi>${m.u?` <a href="${esc(m.u)}" rel="noopener">${esc(T.lnk)}</a>`:''}</p>`;$('feat').hidden=false;$('feat').querySelector('.x').onclick=()=>{$('feat').hidden=true}}
// --- tap a feature for details
function feat(f,e){const p=f.properties,b=rep(p);const det=AR?(p.label_detail_ar||p.label_detail_en):(p.label_detail_en||p.label_detail_ar);
 $('feat').innerHTML=`<button class="x" aria-label="close">×</button><b>${esc(lab(p)||'—')}</b>${b?` <span class="repb${b==='CONTESTED'?' cont':b==='SINGLE-SOURCE'?' single':''}">${esc(b==='SINGLE-SOURCE'&&!AR?p.badge:BL[b][AR?1:0])}</span>`:''}${p.certainty?` <small>[${esc(p.certainty)}]</small>`:''}`+
  (on.has('evd')?`<br><small class="evc">${esc(cf(p)!=null?T.evc+': '+num(cf(p)):T.evn)}</small>`:'')+(p.start!=null?`<br><small><bdi>${fy(p.start)}</bdi> – <bdi>${fy(p.end??e.b)}</bdi></small>`:'')+(det?`<p>${esc(det)}</p>`:'')+
  `<p class="extnote"><bdi dir="ltr">${esc(p.citation||p.source)}${p.pages?' pp. '+esc(p.pages):''}</bdi>${p.url?` <a href="${esc(p.url)}" rel="noopener">${esc(T.lnk)}</a>`:''}${p.source_pins?Object.entries(p.source_pins).map(([k,v])=>`<br><bdi dir="ltr">${esc(k)}: ${esc(v)}</bdi>`).join(''):''}${(p.badges||[]).filter(x=>x!==b).map(x=>` <span class="repb">${esc(BL[x]?BL[x][AR?1:0]:x)}</span>`).join('')}${p.geometry_citation?`<br>${AR?'الهندسة':'Geometry'}: <bdi dir="ltr">${esc(p.geometry_citation)}</bdi>`:''}</p>`;
 $('feat').hidden=false;$('feat').querySelector('.x').onclick=()=>{$('feat').hidden=true};if($('sheet').classList.contains('peek'))snap('half');$('feat').scrollIntoView({block:'nearest'})}
svg.on('click',()=>{$('feat').hidden=true});
// --- border zones (db/border_drafts). Unlisted: only with ?layers=borders-draft (DRAFT badge, no chip, no legend row) unless the build sets bdPub.
const BDQ=(Q.get('layers')||'').split(',').includes('borders-draft'),BD=BDQ||!!M.layers.bdPub,ZJ={};
const zj=e=>(M.layers.bd||[]).includes(e.id)?(ZJ[e.id]||(ZJ[e.id]=getj('/bd/'+e.id+'.json').then(g=>{g.features.forEach(rw);return g.features}).catch(()=>[]))):Promise.resolve([]);
function zdefs(){if(document.getElementById('lowconf'))return;svg.select('defs').each(function(){this.insertAdjacentHTML('beforeend','<pattern id="lowconf" patternUnits="userSpaceOnUse" width="6" height="6" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="#e8eef2" stroke-width="1"/></pattern><pattern id="conthatch" patternUnits="userSpaceOnUse" width="6" height="6" patternTransform="rotate(-45)"><line x1="0" y1="0" x2="0" y2="6" stroke="#e0a63e" stroke-width="2"/></pattern><filter id="zfeather"><feGaussianBlur stdDeviation="6"/></filter>')});}
const ZO=['influence','claimed','core','contested'],ZW=c=>c>=.7?T.bd.hi:c>=.4?T.bd.med:T.bd.lo;
async function zonesDraw(e,D,pub=[]){zdefs();const fs=pub.concat(BD?await zj(e):[]);if(e!==ES[i])return;const red=matchMedia('(prefers-reduced-motion: reduce)').matches;D=red?0:D;
 gZ.selectAll('g.z').interrupt().transition().duration(D?350:0).style('opacity',0).remove();
 const g=gZ.append('g').attr('class','z');const sorted=fs.slice().sort((a,b)=>ZO.indexOf(a.properties.zone)-ZO.indexOf(b.properties.zone));
 sorted.forEach(f=>{const p=f.properties,z=p.zone,d=path(f),k=ZO.indexOf(z);const s=g.append('g').attr('class','zf zf-'+z).style('opacity',D?0:1);
  const a=s.append('path').attr('d',d).attr('class','zn').datum(f).attr('tabindex',0).attr('role','button').attr('aria-label',`${T.bd[z]||z}: ${p.basis||''}`).on('click',ev=>{ev.stopPropagation();zcard(f)});
  if(z==='influence')a.attr('fill','#7a6bd0').attr('fill-opacity',.08).attr('stroke','none').attr('filter','url(#zfeather)');
  else if(z==='claimed')a.attr('fill','#7a6bd0').attr('fill-opacity',.18).attr('stroke','#7a6bd0').attr('stroke-width',1.2).attr('stroke-dasharray','4 3').attr('vector-effect','non-scaling-stroke');
  else if(z==='contested')a.attr('fill','url(#conthatch)').attr('stroke','#e0a63e').attr('stroke-width',1.2).attr('vector-effect','non-scaling-stroke');
  else a.attr('fill','#7a6bd0').attr('fill-opacity',.35).attr('stroke','#7a6bd0').attr('stroke-width',1.2).attr('vector-effect','non-scaling-stroke');
  if(p.confidence<.5)s.append('path').attr('d',d).attr('fill','url(#lowconf)').style('opacity',.5*(1-p.confidence)).attr('pointer-events','none');
  if(D)s.transition().delay(k*80).duration(350).style('opacity',1)});evdStyle()}
function zcard(f){const p=f.properties;
 $('feat').innerHTML=`<button class="x" aria-label="${esc(T.close)}">×</button>${p.signoff!=='approved'?'<span class="bdb">DRAFT</span> ':''}<b>${esc(T.bd[p.zone]||p.zone)}</b>${on.has('evd')?` <small class="evc">${esc(cf(p)!=null?T.evc+': '+num(cf(p)):T.evn)}</small>`:''} ${(p.badges||[]).map(x=>`<span class="repb">${esc(BL[x]?BL[x][AR?1:0]:x)}</span>`).join(' ')}<br><small>${esc(T.bd.conf)}: ${esc(ZW(p.confidence))} (${num(p.confidence)})${p.signoff!=='approved'?' · '+esc(T.bd.nv):''}</small>`+
  `<p>${esc(T.bd.basis)}: <bdi dir="ltr">${esc(p.basis||'—')}</bdi></p><p class="extnote">${(p.sources||[]).map(s=>`<bdi dir="ltr">${esc(s.citation)}</bdi>${s.url?` <a href="${esc(s.url)}" rel="noopener">${esc(T.lnk)}</a>`:''}`).join('<br>')}<br><small>${esc(p.version||'')}</small></p>`;
 $('feat').hidden=false;$('feat').querySelector('.x').onclick=()=>{$('feat').hidden=true};if($('sheet').classList.contains('peek'))snap('half');$('feat').scrollIntoView({block:'nearest'})}
// --- optional layers: drawn only from delivered, sourced files
const srcd=x=>!!(x&&(x.source||x.source_id||(x.source_ids&&x.source_ids.length)||(x.sources&&x.sources.length)||(x.properties&&(x.properties.source||(x.properties.source_ids||[]).length))));
const items=d=>!d?[]:Array.isArray(d)?d:d.features||d.groups||d.relations||d.series||d.data||d.items||[];
const yrIn=(x,e,y)=>{const p=x.properties||x;const a=p.start??p.from_year??-1e9,b=p.end??p.to_year??1e9;return a<=y&&y<=b};
const anchor=id=>{const e=ES.find(z=>z.id===id);if(!e)return null;const g=C[e.id];const c=e.caps&&e.caps[0];return c?[c[1],c[2]]:null};
const RC={alliance:'#4fb06b',conflict:'#e0574c',trade:'#e0a63e',subjugation:'#b07ae0',migration:'#5aa9e6'};
svg.select('defs').html(Object.entries(RC).map(([k,c])=>`<marker id="ah-${k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="${c}"/></marker>`).join('')+'<marker id="ah-ln" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="#f0d26c"/></marker>');
const GJ={};function glj(e){if(!M.layers.glBuilt||!(M.layers.g||[]).includes(e.id))return Promise.resolve([]);return GJ[e.id]||(GJ[e.id]=getj('/g/'+e.id+'.json').catch(()=>[]))}
function glTap(ev,f){ev.stopPropagation();const li=document.querySelector(`#card li[data-id="${CSS.escape(f.id)}"]`);$('feat').innerHTML='<button class="x" aria-label="close">×</button>'+(li?li.innerHTML:esc(AR?f.ar:f.en));$('feat').hidden=false;$('feat').querySelector('.x').onclick=()=>{$('feat').hidden=true};if($('sheet').classList.contains('peek'))snap('half')}
let TRD=null;const gTr=root.append('g').attr('class','trade');
async function tradeDraw(e){gTr.selectAll('*').remove();if(!on.has('trd'))return;if(!TRD)TRD=await fetch('/trade.json').then(r=>r.ok?r.json():[]).catch(()=>[]);const ar=document.documentElement.lang==='ar';
 TRD.filter(r=>r.eras.includes(e.id||e)&&r.w.length>1).forEach(r=>{gTr.append('path').attr('d',path({type:'LineString',coordinates:r.w.map(w=>[w[0],w[1]])})).attr('fill','none').attr('stroke','#e8b04a').attr('stroke-width',2).attr('stroke-dasharray',r.w.some(w=>w[2])?'5 4':null).attr('vector-effect','non-scaling-stroke').attr('tabindex',0).attr('role','img').attr('aria-label',(ar&&r.ar||r.en)+' — '+r.s.map(s=>s.c).join('; ')).append('title').text((ar&&r.ar||r.en)+'\n'+r.s.map(s=>s.c).join('\n'))})}
async function layersDraw(e){tradeDraw(e);ethDraw(e);{const hg=!!M.layers.glBuilt&&(M.layers.g||[]).includes(e.id);['grp','rel'].forEach(k=>{const c=document.querySelector('#layers .chip[data-k='+k+']');if(c)c.hidden=!hg})}const fs=(on.has('grp')||on.has('rel'))?await glj(e):[];const D=RM?0:DUR;
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
 const pl=document.querySelector('.poplayer');if(pl)pl.hidden=!on.has('pop');const el=document.querySelector('.evdlayer');if(el)el.hidden=!on.has('evd');const gl=document.querySelector('.grplayer'),rl=document.querySelector('.rellayer');if(gl)gl.hidden=!on.has('grp');if(rl)rl.hidden=!on.has('rel');
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
  (p.s&&p.s.length?`<ol class="src">${p.s.map(x=>`<li><bdi dir="ltr">${esc(x.c)}</bdi>${x.u?` <a href="${esc(x.u)}" rel="noopener">${esc(T.lnk)}</a>`:''}</li>`).join('')}</ol>`:'');
 $('feat').hidden=false;$('feat').querySelector('.x').onclick=()=>{$('feat').hidden=true}}
const LGC={};const lgj=id=>LGC[id]||(LGC[id]=fetch(`/lg/${id}.json`).then(r=>r.ok?r.json():null).catch(()=>null));
const LGS=fetch('/lg/_spec.json').then(r=>r.ok?r.json():null).catch(()=>null);
function lgSw(r){const w=(p,ex='')=>`<svg width="26" height="18" viewBox="-13 -9 26 18" aria-hidden="true"${ex}>${p}</svg>`;
 if(r.id.startsWith('city_')){const k=r.id.slice(5);return w(`<path d="${CSH[k]||CSH.other}" class="lgcty${k==='capital'?' capital':''}" fill="${k==='capital'?'#f0c24c':'#e8eef2'}" stroke="#0b141b" stroke-width=".8"/>`)}
 if(r.id.startsWith('relation_arrow_')){const k=r.id.slice(15);return w(`<line x1="-11" y1="0" x2="9" y2="0" stroke="${RC[k]||'#ccc'}" stroke-width="2" marker-end="url(#ah-${k})"/>`)}
 const sh={control_extent:'<rect x="-10" y="-6" width="20" height="12" fill="#7a6bd0" fill-opacity=".35" stroke="#7a6bd0"/>',control_extent_approx:'<rect x="-10" y="-6" width="20" height="12" fill="#7a6bd0" fill-opacity=".18" stroke="#7a6bd0" stroke-dasharray="4 3"/>',extent_label_point:'<circle r="3.5" fill="none" stroke="#e8eef2" stroke-width="1.5"/>',contested_point:'<path d="M0,-5L5,0L0,5L-5,0Z" fill="none" stroke="#e0a63e" stroke-width="1.5"/>',contested_boundary_line:'<line x1="-11" y1="0" x2="11" y2="0" stroke="#e0a63e" stroke-width="2" stroke-dasharray="4 3"/>',boundary_line:'<line x1="-11" y1="0" x2="11" y2="0" stroke="#e8eef2" stroke-width="1.5"/>',reported_point:'<path d="M0,-5L5,4L-5,4Z" fill="none" stroke="#e0574c" stroke-width="1.5"/>',group_control_point:'<rect x="-4" y="-4" width="8" height="8" fill="#5aa9e6"/>',homeland_point:'<circle r="6.5" fill="none" stroke="#009E73" stroke-dasharray="2 1.5"/><circle r="4" fill="#009E73" fill-opacity=".6" stroke="#fff" stroke-width=".8"/>',homeland_soft_area:'<rect x="-10" y="-6" width="20" height="12" fill="#009E73" fill-opacity=".12"/>',ruin:'<circle r="3.6" fill="none" stroke="#8a8f94" stroke-width="1.3" stroke-dasharray="2 1.5"/>',list_only_text:'<text x="0" y="4" text-anchor="middle" font-size="11" fill="#9fb3c2">≡</text>'}[r.id];
 return w(sh||'<text x="0" y="4" text-anchor="middle" font-size="11" fill="#9fb3c2">?</text>')}
const LGR={trade_route:['Trade route (schematic)','طريق تجاري (تخطيطي) *']},LGB={DERIVED:'مشتق *','APPROXIMATE-COORDS':'إحداثيات تقريبية *','AR-REVIEW':'بانتظار مراجعة عربية *','LAST-ATTESTED':'آخر توثيق *','LAST-ATTESTED+APPROXIMATE':'آخر توثيق، تقريبي *'};
const lgN=r=>{const f=LGR[r.id];if(AR)return r.ar||(f&&f[1])||r.en;return(r.en===r.id&&f)?f[0]:r.en};
const LGL={ctl:()=>T.l.ctl,cty:()=>T.l.cty,grp:()=>T.l.grp,rel:()=>T.l.rel,hml:()=>T.l.hml};
let lgOpen=false;
async function legendDraw(e){const b=$('lgb'),p=$('lgp');if(!b||!p)return;p.setAttribute('role','region');p.setAttribute('aria-label',T.legendl||T.lg);const d=await lgj(e.id),sp=await LGS;if(e!==ES[i])return;
 const rows=d?d.rows.filter(r=>on.has(r.l)):[];b.textContent=`${T.lg}${rows.length?' · '+num(rows.length):''}`;b.setAttribute('aria-expanded',lgOpen);
 let h='';const ls=[...new Set(rows.map(r=>r.l))];
 if(!rows.length)h=`<p><span class="gap">${T.wip}</span> <span class="gapt">${esc(T.lgnone)}</span></p>`;
 for(const l of ls){h+=`<h4>${esc(LGL[l]?LGL[l]():l)}</h4><ul>`+rows.filter(r=>r.l===l).map(r=>`<li role="listitem" aria-label="${esc(lgN(r)+' '+r.n)}">${lgSw(r)}<span>${esc(lgN(r))}${AR&&r.arw?' <sup title="'+esc(T.lgarw)+'">*</sup>':''}</span><span class="n"><bdi>${num(r.n)}</bdi></span></li>`).join('')+'</ul>';
  const bd=(d.badges||{})[l]||[];if(bd.length)h+=`<p>${bd.map(x=>`<span class="repb">${esc(AR?(x.ar||(BL[x.id]&&BL[x.id][1])||LGB[x.id]||x.en):(x.en!==x.id?x.en:(BL[x.id]?BL[x.id][0]:x.en)))} <bdi>${num(x.n)}</bdi></span>`).join(' ')}</p>`;
  const sr=(d.src||{})[l]||[];if(sr.length)h+=`<details class="srcs"><summary>${esc(T.lgsrc)} (${num(sr.length)})</summary><ul>${sr.map(x=>`<li dir="ltr"><bdi>${esc(x.c)}</bdi>${x.u?` <a href="${esc(x.u)}" rel="noopener">${esc(T.lnk)}</a>`:''}</li>`).join('')}</ul></details>`}
 if(on.has('bat')&&M.layers.bat)h+=`<h4>${esc(AR?'المعارك *':'Battles')}</h4><ul><li role="listitem"><svg width="26" height="26" viewBox="-13 -13 26 26" aria-hidden="true" class="bts"><g class="bt cur"><circle class="bth" r="12"/><circle class="btc" r="8"/><path d="M-4,-4L4,4M4,-4L-4,4"/></g></svg><span>${esc(BT.cur)}</span></li><li role="listitem"><svg width="26" height="26" viewBox="-13 -13 26 26" aria-hidden="true" class="bts"><g class="bt past"><circle class="btc" r="8"/><path d="M-4,-4L4,4M4,-4L-4,4"/></g></svg><span>${esc(BT.past)}</span></li></ul>`;
 if(sp&&sp.credit)h+=`<details class="cr"><summary>${esc(T.lgcred)} ⓘ</summary><p dir="ltr">${esc(sp.credit)}</p><p>${esc(AR?(sp.dis_ar||sp.dis_en):sp.dis_en)}</p></details>`;
 h+=`<p class="lgm"><a href="${AR?'/ar':''}/methodology/">${esc(T.meth||'')}</a></p>`;
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
  `<p class="extnote">${c.s.map(x=>`<bdi dir="ltr">${esc(x.c)}${x.p?' · '+esc(x.p):''}</bdi>${x.u?` <a href="${esc(x.u)}" rel="noopener">${esc(T.lnk)}</a>`:''}`).join('<br>')}${r&&r.s&&r.s.length?`<br><small>${esc(T.role)}: <bdi dir="ltr">${r.s.map(esc).join(', ')}</bdi></small>`:''}</p>`+
  (M.layers.cStub?`<p class="gap">${esc(T.stub)}</p>`:'');
 $('feat').hidden=false;$('feat').querySelector('.x').onclick=()=>{$('feat').hidden=true};if($('sheet').classList.contains('peek'))snap('half')}
// --- navigation
// era camera: fly to focus_view.bbox [w,s,e,n] (fallback: extent bounds, then whole region) inside the area not covered by the sheet/side card. Manual zoom is kept until the era changes.
let CE=null;function cam(e,g){if(e.id===CE)return;const first=CE===null;CE=e.id;
 let b=e.fv;if(!b){// planar bbox of the era's extents (geoBounds returns the whole globe for reverse-wound rings), then its capitals
  const xs=[],ys=[],w=c=>{if(typeof c[0]==='number'){if(isFinite(c[0])&&isFinite(c[1])){xs.push(c[0]);ys.push(c[1])}}else c.forEach(w)};
  ((g&&g.features)||[]).forEach(f=>f.geometry&&w(f.geometry.coordinates));if(!xs.length)(e.caps||[]).forEach(c=>{xs.push(c[1]);ys.push(c[2])});
  if(xs.length)b=[Math.min(...xs),Math.min(...ys),Math.max(...xs),Math.max(...ys)]}
 let t=d3.zoomIdentity;if(b){const sh=$('sheet').getBoundingClientRect(),top=desk()?70:120,bot=desk()?H()-20:Math.max(top+120,H()-Math.min(sh.height,H()*.44)-8),x1=desk()?(AR?sh.right+20:20):10,x2=desk()?(AR?W()-20:sh.left-20):W()-10;
  {const cx=(b[0]+b[2])/2,cy=(b[1]+b[3])/2,hx=Math.max((b[2]-b[0])/2,1.5),hy=Math.max((b[3]-b[1])/2,1.5);b=[cx-hx,cy-hy,cx+hx,cy+hy]}// min 3° window so point-like foci keep context
  const p=proj([b[0],b[3]]),q=proj([b[2],b[1]]),dx=Math.max(q[0]-p[0],8),dy=Math.max(q[1]-p[1],8);const k=Math.max(1,Math.min(6,.85*Math.min((x2-x1)/dx,(bot-top)/dy)));
  t=d3.zoomIdentity.translate((x1+x2)/2-k*(p[0]+q[0])/2,(top+bot)/2-k*(p[1]+q[1])/2).scale(k)}
 if(first||RM)svg.interrupt().call(zoom.transform,t);else svg.interrupt().transition('cam').duration(1000).call(zoom.transform,t)}
function go(n){n=Math.max(0,Math.min(ES.length-1,n));if(n===i)return;i=n;Y=null;render(true)}
r.addEventListener('input',()=>{tourStop();go(+r.value)});
// era tour: play/pause next to the scrubber; flies to each era's area (camera is instant under reduced motion), dwells, stops at the last era.
// Any manual era change pauses it; hidden tabs pause it. The live region already announces each era.
const TB=document.createElement('button');TB.type='button';TB.id='tour';TB.className='nav tour';
let TT=null;const tourSet=p=>{TB.setAttribute('aria-pressed',p);TB.setAttribute('aria-label',p?T.tour_pause:T.tour_play);TB.title=p?T.tour_pause:T.tour_play;TB.innerHTML=p?'<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M3 2h4v12H3zM9 2h4v12H9z" fill="currentColor"/></svg>':'<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M4 2l10 6-10 6z" fill="currentColor"/></svg>'};
function tourStop(){if(TT){clearTimeout(TT);TT=null;tourSet(false)}}
function tourStep(){if(i>=ES.length-1){tourStop();return}go(i+1);TT=setTimeout(tourStep,RM?5000:4200)}
document.addEventListener('keydown',ev=>{if(ev.key==='Escape'&&TT)tourStop()},true);
TB.onclick=()=>{if(TT){tourStop();return}tourSet(true);if(i>=ES.length-1){go(0);TT=setTimeout(tourStep,RM?5000:4200)}else tourStep()};
tourSet(false);$('scrub').appendChild(TB);
document.addEventListener('visibilitychange',()=>{if(document.hidden)tourStop()});
['prev','next'].forEach(id=>$(id).addEventListener('click',tourStop,true));
// slider keys (APG): arrows step one era (mirrored in RTL), Up/Down step, PageUp/PageDown ±5, Home/End first/last
r.addEventListener('keydown',ev=>{tourStop();const k=ev.key,m={ArrowRight:AR?-1:1,ArrowLeft:AR?1:-1,ArrowUp:1,ArrowDown:-1,PageUp:5,PageDown:-5};let n=null;if(k in m)n=i+m[k];else if(k==='Home')n=0;else if(k==='End')n=ES.length-1;if(n==null)return;ev.preventDefault();go(n)});
addEventListener('keydown',ev=>{if(ev.key===' '&&TT&&!(ev.target.closest&&ev.target.closest('button,input,select,textarea,a,[role=button],summary'))){ev.preventDefault();tourStop()}});
addEventListener('keydown',ev=>{if(ev.key!=='Escape')return;if(!$('feat').hidden){$('feat').hidden=true;if(LASTF&&LASTF.isConnected)LASTF.focus();return}if(lgOpen){$('lgb').click();$('lgb').focus();return}if($('sheet').classList.contains('full'))snap('half')});$('prev').onclick=()=>go(i-1);$('next').onclick=()=>go(i+1);
$('w').addEventListener('input',()=>{const e=ES[i];ext(e).then(g=>{Y=steps(e,g)[+$('w').value];render(true)})});
addEventListener('keydown',ev=>{if(ev.target.tagName==='INPUT')return;if(ev.key==='ArrowRight'||ev.key==='ArrowLeft')tourStop();if(ev.key==='ArrowRight')go(i+(AR?-1:1));if(ev.key==='ArrowLeft')go(i+(AR?1:-1))});
let sx=null;const hd=$('head');hd.addEventListener('pointerdown',ev=>{sx=ev.clientX});hd.addEventListener('pointerup',ev=>{if(sx==null)return;const d=ev.clientX-sx;sx=null;if(Math.abs(d)>50)go(i+((d<0)!==AR?1:-1))});
const SN=['peek','half','full'];function snap(s){$('grab').setAttribute('aria-label',T.sheet+' · '+T.sheetst[s]);$('grab').setAttribute('aria-expanded',s!=='peek');document.body.classList.toggle('sfull',s==='full');setTimeout(lgFit,350);const sh=$('sheet');SN.forEach(c=>sh.classList.remove(c));sh.classList.add(s);setTimeout(place,320)}
$('grab').onclick=()=>{const sh=$('sheet'),c=SN.find(x=>sh.classList.contains(x))||'half';snap(SN[(SN.indexOf(c)+1)%3])};
let rt;addEventListener('resize',()=>{clearTimeout(rt);rt=setTimeout(()=>{fit();OLD=[];render(false)},150)});
// era flags (db/era_symbols.json via db/legends/eras layers.flags): shown at era_focus flag_anchor only while the slider year is inside a used window; joint flags side by side; VERIFY = dashed frame + chip
function flagsDraw(e){const fl=e.fl,y=cY(),fs=fl?fl.f.filter(f=>f.w.some(w=>w[0]<=y&&y<=w[1])):[];const d=fs.length?[e.id+'|'+fs.map(f=>f.s).join()]:[];
 const s=gF.selectAll('g.flag').data(d,x=>x);s.exit().remove();
 const n=s.enter().append('g').attr('class','flag mk').each(function(){this.__xy=proj(fl.a)}).attr('transform',function(){return `translate(${this.__xy})scale(${1/K})`});
 n.each(function(){const g=d3.select(this),FW=22,FH=15,gap=3,tw=fs.length*FW+(fs.length-1)*gap;g.append('title').text((AR?'العلم':'Flag')+(fs.some(f=>f.v)?' · '+VFL:''));
  fs.forEach((f,j)=>{const x=-tw/2+j*(FW+gap),y0=-FH-6;g.append('rect').attr('class','fbd'+(f.v?' vfy':'')).attr('x',x-1).attr('y',y0-1).attr('width',FW+2).attr('height',FH+2);g.append('image').attr('href',f.s).attr('x',x).attr('y',y0).attr('width',FW).attr('height',FH).attr('preserveAspectRatio','none')});
  g.append('line').attr('x1',0).attr('x2',0).attr('y1',-6).attr('y2',0).attr('class','fpole');
  if(fs.some(f=>f.v))g.append('text').attr('class','fvchip').attr('x',0).attr('y',-FH-9).attr('text-anchor','middle').attr('lang',AR?'ar':'en').text(BL.VERIFY[AR?1:0])})}
// share: copies /era/<id>/ (or /ar/era/<id>/); native share sheet on touch devices when available; polite live 'Link copied'
function shareBtn(e){const h=$('card').querySelector('h2,h1');if(!h)return;const u=location.origin+(AR?'/ar':'')+'/era/'+e.id+'/';const w=document.createElement('p');w.className='sharep';
 w.innerHTML=`<button type="button" class="share">${esc(T.share)}</button> <span class="sharemsg" aria-live="polite"></span>`;h.after(w);const m=w.querySelector('.sharemsg');
 w.querySelector('button').onclick=async()=>{if(navigator.share&&matchMedia('(pointer:coarse)').matches){try{await navigator.share({title:h.textContent,url:u});return}catch(x){if(x&&x.name==='AbortError')return}}
  try{await navigator.clipboard.writeText(u);m.textContent=T.copied}catch(x){m.innerHTML=`${esc(T.copyno)} <bdi dir="ltr">${esc(u)}</bdi>`}}}
// Map sources panel (lazy): /ms/<id>.json, inserted after the card; open state kept per session
const MSC={};function msPanel(e){const old=document.getElementById('msrc');if(old)old.remove();if(!((M.layers||{}).ms||[]).includes(e.id))return;
 (MSC[e.id]||(MSC[e.id]=getj('/ms/'+e.id+'.json').catch(()=>null))).then(j=>{if(!j||e!==ES[i])return;const w=document.createElement('div');w.id='msrc';w.innerHTML=j[L];$('card').after(w)})}
// era search: header button opens a small dialog-less panel; matches EN+AR names (Arabic folded: harakat, alef/ya/ta-marbuta forms)
const fold=s=>(s||'').toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f\u064B-\u0655\u0670\u0640]/g,'').replace(/[أإآٱ]/g,'ا').replace(/ى/g,'ي').replace(/ة/g,'ه').replace(/ؤ/g,'و').replace(/ئ/g,'ي').replace(/[^\p{L}\p{N}]+/gu,' ').trim();
(()=>{const S=T.srch;if(!S)return;const b=document.createElement('button');b.type='button';b.id='srchb';b.className='chip';b.textContent=S.b;b.setAttribute('aria-expanded','false');b.setAttribute('aria-controls','srch');$('about').before(b);
 const p=document.createElement('div');p.id='srch';p.hidden=true;p.setAttribute('role','search');p.innerHTML=`<label for="srchi" class="sr">${esc(S.l)}</label><input id="srchi" type="search" autocomplete="off" placeholder="${esc(S.ph)}" aria-describedby="srchn"><button type="button" class="chip" id="srchx" aria-label="${esc(S.x)}">×</button><p id="srchn" class="sr" aria-live="polite"></p><ul id="srchr"></ul>`;document.body.appendChild(p);
 const I=$('srchi'),R=$('srchr'),F=ES.map(e=>fold(e.en+' '+e.ar+' '+e.id.replace(/-/g,' ')));
 const close=f=>{p.hidden=true;b.setAttribute('aria-expanded','false');if(f!==false)b.focus()};
 const pick=k=>{close(false);tourStop();go(k);setTimeout(()=>$('sheet').focus(),50)};
 const run=()=>{const q=fold(I.value);R.innerHTML='';if(!q){$('srchn').textContent='';return}const w=q.split(' ');const hit=[];F.forEach((t,k)=>{if(w.every(x=>t.includes(x)))hit.push(k)});
  $('srchn').textContent=hit.length===1?S.n1:hit.length?`${num(hit.length)} ${S.n}`:S.z;hit.slice(0,12).forEach(k=>{const e=ES[k],li=document.createElement('li'),a=document.createElement('button');a.type='button';a.innerHTML=`${esc(AR?e.ar:e.en)} <small><bdi>${fy(e.a)}</bdi> – <bdi>${fy(e.b)}</bdi></small>`;a.onclick=()=>pick(k);li.appendChild(a);R.appendChild(li)})};
 b.onclick=()=>{if(p.hidden){p.hidden=false;b.setAttribute('aria-expanded','true');I.focus();run()}else close()};$('srchx').onclick=()=>close();I.addEventListener('input',run);
 p.addEventListener('keydown',ev=>{if(ev.key==='Escape'){ev.stopPropagation();close()}else if(ev.key==='Enter'&&ev.target===I){const f=R.querySelector('button');if(f)f.click()}else if(ev.key==='ArrowDown'||ev.key==='ArrowUp'){const L=[I,...R.querySelectorAll('button')];const k=L.indexOf(document.activeElement);if(k<0)return;ev.preventDefault();L[Math.max(0,Math.min(L.length-1,k+(ev.key==='ArrowDown'?1:-1)))].focus()}});})();
// story mode: ?story=<chapter> steps through that chapter's eras (prev/next/exit bar); era cards offer "play this chapter"
var STY=null;
(()=>{const SM=M.t.en.story,S=T.story;if(!SM||!S)return;const ix=id=>ES.findIndex(e=>e.id===id);
 const CS=SM.c.map(c=>({...c,k:c.ids.map(ix).filter(k=>k>=0)})) // order = data/story_chapters.json ids.filter(c=>c.k.length>1);
 const bar=document.createElement('div');bar.id='story';bar.hidden=true;bar.setAttribute('role','region');bar.setAttribute('aria-label',S.lbl);
 bar.innerHTML=`<span id="stt"></span><span id="stn" aria-live="polite"></span><button type="button" class="nav" id="stp">‹</button><button type="button" class="nav" id="stx2">›</button><button type="button" class="chip" id="stx">×</button>`;
 $('scrub').before(bar);$('stp').setAttribute('aria-label',S.prev);$('stx2').setAttribute('aria-label',S.next);$('stx').setAttribute('aria-label',S.x);$('stx').title=S.x;
 const pos=()=>STY.k.indexOf(i);
 const upd=()=>{if(!STY)return;const p=pos();$('stn').textContent=p<0?S.out:`${S.step} ${num(p+1)} ${S.of} ${num(STY.k.length)}`;
  $('stp').disabled=p===0;$('stx2').disabled=p===STY.k.length-1;};
 const step=d=>{tourStop();const p=pos();let k;if(p<0){k=d>0?STY.k.find(x=>x>i):[...STY.k].reverse().find(x=>x<i);if(k==null)k=STY.k[d>0?STY.k.length-1:0]}else k=STY.k[Math.max(0,Math.min(STY.k.length-1,p+d))];go(k);upd()};
 const start=(c,first)=>{STY=c;bar.hidden=false;document.body.classList.add('storyon');$('stt').innerHTML=`${esc(S.ch)} ${num(c.n)}: <b>${esc(AR?c.ar:c.en)}</b>`;if(first&&pos()<0)go(c.k[0]);upd();url()};
 const stop=()=>{STY=null;bar.hidden=true;document.body.classList.remove('storyon');url();const b=document.querySelector('#stcta button');if(b)b.focus()};
 $('stp').onclick=()=>step(-1);$('stx2').onclick=()=>step(1);$('stx').onclick=stop;
 bar.addEventListener('keydown',ev=>{if(ev.key==='Escape'){ev.stopPropagation();stop()}});
 const g0=go;go=n=>{g0(n);upd();cta()};
 function cta(){const o=$('stcta');if(o)o.remove();const cs=CS.filter(c=>c.k.includes(i));if(!cs.length||!$('card'))return;const w=document.createElement('div');w.id='stcta';
  cs.forEach(c=>{const b=document.createElement('button');b.type='button';b.className='chip';b.innerHTML=`▶ ${esc(S.watch)} <small>(${esc(S.inch)} ${num(c.n)}: ${esc(AR?c.ar:c.en)})</small>`;b.onclick=()=>{start(c,false);$('stx2').focus()};w.appendChild(b)});$('card').after(w)}
 new MutationObserver(()=>{if(!$('stcta'))cta()}).observe($('card').parentNode,{childList:true});new MutationObserver(cta).observe($('card'),{childList:true});
 const q=Q.get('story'),c0=CS.find(c=>c.s===q);if(c0)start(c0,!Q.get('era'));cta()})();
// embed snippet: "Embed" next to Share opens copyable <iframe> code for this era; ?embed=1 = framed view (no about/lang/search, brand links out)
(()=>{const B=T.emb;if(!B)return;const EMB=Q.get('embed')==='1';
 if(EMB){document.body.classList.add('embed');const br=$('brand');const a=document.createElement('a');a.id='embo';a.className='chip';a.target='_blank';a.rel='noopener';a.textContent=B.open+' ↗';br.after(a);
  const ou=()=>{const q=new URLSearchParams(location.search);q.delete('embed');a.href=B.site+(AR?'/ar/':'/')+'?'+q.toString()};ou();addEventListener('click',()=>setTimeout(ou,0),true)}
 const s0=shareBtn;shareBtn=e=>{s0(e);const w=$('card').querySelector('.sharep');if(!w||EMB)return;const b=document.createElement('button');b.type='button';b.className='share';b.textContent=B.b;b.setAttribute('aria-expanded','false');
  const src=B.site+(AR?'/ar/':'/')+'?era='+encodeURIComponent(e.id)+'&embed=1',code=`<iframe src="${src}" title="${esc(AR?e.ar:e.en)} · Sudan Histomap" width="100%" height="600" style="border:0" loading="lazy" allow="clipboard-write"></iframe>`;
  const box=document.createElement('div');box.className='embbox';box.hidden=true;const id='embc-'+e.id;
  box.innerHTML=`<label for="${id}">${esc(B.l)}</label><textarea id="${id}" readonly rows="3" dir="ltr" spellcheck="false"></textarea><button type="button" class="share">${esc(B.c)}</button> <span class="sharemsg" aria-live="polite"></span>`;
  const ta=box.querySelector('textarea');ta.value=code;ta.onfocus=()=>ta.select();
  box.querySelector('button').onclick=async()=>{const m=box.querySelector('.sharemsg');try{await navigator.clipboard.writeText(code);m.textContent=B.ok}catch(x){ta.focus();ta.select()}};
  b.onclick=()=>{box.hidden=!box.hidden;b.setAttribute('aria-expanded',String(!box.hidden));if(!box.hidden)ta.focus()};
  w.querySelector('.share').after(' ',b);w.after(box)}})();
// Where am I: one-shot browser geolocation -> marker on the map. On-device only: kept in memory, never stored, sent or added to the URL
(()=>{const WI=T.wai;if(!WI||!navigator.geolocation)return;let P=null;const gW=root.append('g').attr('class','wai');
 const b=document.createElement('button');b.type='button';b.id='wai';b.className='chip';b.textContent='◎';b.title=WI.b;b.setAttribute('aria-label',WI.b);b.setAttribute('aria-pressed','false');$('reset').after(b);
 const st=document.createElement('p');st.id='waim';st.setAttribute('aria-live','polite');st.className='sr';document.body.appendChild(st);
 const say=(t,vis)=>{st.textContent=t;st.className=vis?'':'sr';clearTimeout(say.t);if(vis)say.t=setTimeout(()=>{st.className='sr'},6000)};
 const draw=()=>{gW.selectAll('*').remove();if(!P)return;const xy=proj(P);const m=gW.append('g').attr('class','mk waimk');m.node().__xy=xy;m.attr('transform',`translate(${xy})scale(${1/K})`);
  m.append('circle').attr('r',13).attr('class','wair');m.append('circle').attr('r',6).attr('class','waid');m.append('title').text(WI.here);return xy};
 addEventListener('resize',()=>setTimeout(draw,60));
 b.onclick=()=>{if(b.getAttribute('aria-busy')==='true')return;if(P){P=null;draw();b.setAttribute('aria-pressed','false');say(WI.off,true);return}
  const busy=v=>{if(v){b.setAttribute('aria-disabled','true');b.setAttribute('aria-busy','true')}else{b.removeAttribute('aria-disabled');b.removeAttribute('aria-busy')}};busy(true);navigator.geolocation.getCurrentPosition(g=>{busy(false);P=[g.coords.longitude,g.coords.latitude];b.setAttribute('aria-pressed','true');const xy=draw();
   const inb=P[0]>=RELIEF_BOX[0]&&P[0]<=RELIEF_BOX[2]&&P[1]>=RELIEF_BOX[1]&&P[1]<=RELIEF_BOX[3];
   if(inb){const sh=$('sheet').getBoundingClientRect(),c=desk()?[AR?(sh.right+W())/2:sh.left/2,H()/2]:[W()/2,(120+Math.min(sh.top,H()))/2];svg.transition().duration(RM?0:DUR).call(zoom.translateTo,xy[0],xy[1],c)}say((inb?WI.here:WI.out)+'. '+WI.note,true)},
   ()=>{busy(false);say(WI.err+'. '+WI.note,true)},{enableHighAccuracy:false,timeout:15000,maximumAge:300000})}})();
// first-visit hint: points to play tour / search / layers; dismissal remembered in localStorage only; not in embed or story mode
(()=>{const H=T.hint;if(!H||Q.get('embed')==='1'||Q.get('story'))return;const K1='hm_hint1';try{if(localStorage.getItem(K1))return}catch(_){}
 let prev=document.activeElement;const trk=e=>{if(e.target&&e.target.closest&&!e.target.closest('#hint'))prev=e.target};const pd=e=>{const c=e.target&&e.target.closest&&e.target.closest('button,a[href],input,select,textarea,[tabindex]');if(c&&!c.closest('#hint'))prev=c};document.addEventListener('focusin',trk);document.addEventListener('pointerdown',pd,true);const vis=x=>x&&x!==document.body&&x.isConnected&&!x.closest('#hint')&&!x.disabled&&x.getClientRects().length>0;const back=()=>{document.removeEventListener('focusin',trk);document.removeEventListener('pointerdown',pd,true);const ae=document.activeElement;if(vis(ae))prev=ae;const t=vis(prev)?prev:$('tour');if(t)t.focus()};const d=document.createElement('section');d.id='hint';d.setAttribute('aria-label',H.l);d.innerHTML=`<b>${esc(H.h)}</b><p>${esc(H.t)}</p><div><button type="button" class="chip" id="hintp">${esc(H.p)}</button><button type="button" class="chip" id="hintx">${esc(H.x)}</button></div>`;document.body.appendChild(d);
 const off=()=>{try{localStorage.setItem(K1,'1')}catch(_){}d.remove();removeEventListener('keydown',ek);if(cmpDiv.s!=null)cmpDiv(cmpDiv.s)},ek=e=>{if(e.key==='Escape'&&d.isConnected){off();back()}};addEventListener('keydown',ek);
 $('hintx').onclick=()=>{off();back()};$('hintp').onclick=()=>{off();const t=$('tour');if(t){t.click();t.focus()}}})();
// --- start
window.__hm={scale:k=>svg.call(zoom.scaleTo,k)};// test hook (QA only, no side effects)
const eth1932=()=>{const e=ES[i];if(on.has('eth')&&(M.layers.eth||[]).includes(e.id)&&e.a<=1932&&1932<=e.b)Y=1932};eth1932();
// --- Battles layer (?layers=battles) + era Events timeline. Built only when web/features.json turns them on and the
// data passed the build cite checks (or a local HM_DEV_STUB build: EXAMPLE DATA badge). Every item carries a cite.
var BTD=null,gBt=null,gEp=null,ST=null,EVD=null;const BT=AR?{d:'التاريخ *',sd:'الأطراف *',oc:'النتيجة *',src:'المصدر *',img:'الصورة *',ev:'أحداث العصر *',war:'الحرب *',stub:'بيانات مثال (تجريبية)، ليست بحثًا *',fly:'اعرض على الخريطة *',pg:'ص',cur:'معركة هذا العام *',past:'معركة سابقة في هذا العصر *'}:{d:'Date',sd:'Sides',oc:'Outcome',src:'Source',img:'Image',ev:'Events in this era',war:'War',stub:'EXAMPLE DATA (stub), not research',fly:'Show on map',pg:'p.',cur:'Battle this year',past:'Earlier battle in this era'};
const bpick=a=>a?(AR?(a[1]||a[0]):(a[0]||a[1]))||'':'';
const bcite=s=>s.map(c=>`<bdi dir="ltr">${esc(c.c)}${c.p?', '+esc(/^\s*(pp?\.|ص)/.test(c.p)?c.p:(/^\d/.test(c.p)?'p. '+c.p:c.p)):''}</bdi>${c.u?` <a href="${esc(c.u)}" rel="noopener">${esc(T.lnk||'link')}</a>`:''}`).join('<br>');
async function batDraw(e){if(!M.layers.bat)return;gBt=gBt||root.append('g').attr('class','bts');if(!on.has('bat')){gBt.selectAll('*').remove();return}
 if(!BTD)BTD=await getj('/b.json').catch(()=>({battles:[]}));if(e!==ES[i])return;const y=Y??e.b,y2=Math.min(e.b,((ST||[]).find(t=>t>y)??e.b+1)-1);// a scrubber step stands for [step, next step)
 // window = the wider of the battle's war range (db/wars.json) and the active era; earlier battles in it show muted, the current (or nearest earlier) one highlighted, later ones hidden
 const win=b=>b.w&&b.w.a!=null?[Math.min(e.a,b.w.a),Math.max(e.b,b.w.b??b.w.a)]:[e.a,e.b];
 const rel=b=>(b.a<=e.b&&b.b>=e.a)||(b.w&&b.w.a!=null&&b.w.a<=e.b&&(b.w.b??b.w.a)>=e.a);// battle in this era, or its war overlaps it
 const B=BTD.battles.filter(b=>{if(!rel(b))return false;const w=win(b);return w[0]<=y2&&y<=w[1]&&b.a<=y2});
 const ma=B.length?Math.max(...B.map(b=>b.a)):null,C=new Set(B.filter(b=>b.a===ma).map(b=>b.id));// highlight: the latest battle at or before the step (ties share it)
 const k=gBt.selectAll('g.bt').data(B,b=>b.id);k.exit().remove();
 const n=k.enter().append('g').each(function(b){this.__xy=proj(b.ll)}).on('click',(ev,b)=>{ev.stopPropagation();batCard(b)});
 n.append('circle').attr('class','bth').attr('r',12);n.append('circle').attr('class','btc').attr('r',8);n.append('path').attr('d','M-4,-4L4,4M4,-4L-4,4');n.append('title');
 n.merge(k).attr('class',b=>'bt mk pr-'+b.pr+(C.has(b.id)?' cur':' past')).select('title').text(b=>bpick([b.en,b.ar])+' · '+(C.has(b.id)?BT.cur:BT.past));scaleMarks();a11yMarks()}
// war line + end_badge (battle_style.json end_badge, Map Designer 93199e3): 'from – to?' with the end year dimmed, pill badge; end_note on hover (title) and tap (toggle)
function batWar(w){if(!w)return'';const e=BTD.ebs||{},raw=w.eb&&w.eb.toUpperCase()!=='VERIFY'?w.eb+' · ':'',lb=raw+(AR?e.ar:e.en),nt=w.nt?(AR?(w.nt[1]||(w.nt[0]?w.nt[0]+' [VERIFY]':'')):(w.nt[0]||'')):'';
 return `<p><b>${BT.war}:</b> <span dir="auto">${esc(bpick([w.en,w.ar]))}</span> <bdi dir="ltr">${esc(fy(w.a))} – <span class="${w.eb?'wye':''}">${esc(fy(w.b))}${w.eb?'?':''}</span></bdi>`+(w.eb?` <button type="button" class="ebd" aria-expanded="false" aria-controls="ebn"${nt?` title="${esc(nt)}"`:''}>${esc(lb)}</button>`:'')+'</p>'+(w.eb&&nt?`<p id="ebn" class="ebn" dir="auto" hidden>${esc(nt)}</p>`:'')+`<p class="extnote"><b>${BT.war} · ${BT.src}:</b> ${bcite(w.s)}</p>`}
function batCard(b){const p=$('feat'),dt=bpick(b.dt)||(b.a===b.b?fy(b.a):fy(b.a)+' – '+fy(b.b));
 p.innerHTML=`<button class="x" aria-label="${esc(T.close)}">×</button><b dir="auto">${esc(bpick([b.en,b.ar]))}</b>${BTD.stub?` <span class="repb">${esc(BT.stub)}</span>`:''}`+
  `<p><b>${BT.d}:</b> <bdi>${esc(dt)}</bdi></p>`+(b.sd.length?`<p><b>${BT.sd}:</b> ${b.sd.map(s=>`<bdi>${esc(bpick(s))}</bdi>`).join(' · ')}</p>`:'')+(bpick(b.oc)?`<p><b>${BT.oc}:</b> <span dir="auto">${esc(bpick(b.oc))}</span></p>`:'')+
  (b.im?`<figure class="btim"><img src="${esc(b.im.src)}" alt="${esc(bpick(b.im.alt)||bpick([b.en,b.ar]))}" loading="lazy" decoding="async"><figcaption><bdi dir="auto">${esc(b.im.cr)}</bdi>${b.im.li?' · <bdi dir="ltr">'+esc(b.im.li)+'</bdi>':''}${b.im.u?` <a href="${esc(b.im.u)}" rel="noopener">${esc(T.lnk||'link')}</a>`:''}</figcaption></figure>`:'')+
  batWar(b.w)+`<p class="extnote"><b>${BT.src}:</b> ${bcite(b.s)}</p>`;
 p.hidden=false;p.querySelector('.x').onclick=()=>{p.hidden=true};const eb=p.querySelector('.ebd');if(eb)eb.onclick=()=>{const n=$('ebn'),o=n.hidden;n.hidden=!o;eb.setAttribute('aria-expanded',o)};if($('sheet').classList.contains('peek'))snap('half');p.scrollIntoView({block:'nearest'})}
async function evList(e){if(!M.layers.ev||!(M.layers.evE||[]).includes(e.id))return;const d=await getj('/ev/'+e.id+'.json').catch(()=>null);if(!d||e!==ES[i]||!d.events.length)return;
 const s=document.createElement('section');s.className='evt';s.setAttribute('aria-labelledby','evth');
 s.innerHTML=`<h2 id="evth">${BT.ev}</h2>${d.stub?`<p><span class="repb">${esc(BT.stub)}</span></p>`:''}<ol>`+d.events.map((v,k)=>{const y=`<bdi class="evy">${v.ap?'c. ':''}${fy(v.y)}${v.y2!=null?' – '+fy(v.y2):''}</bdi>`,t=`<span dir="auto">${esc(bpick(v.t))}</span>`;
  return `<li>${v.pl?`<button type="button" class="evgo" data-k="${k}" aria-label="${esc(bpick(v.t)+' · '+BT.fly+(bpick(v.pl.n)?': '+bpick(v.pl.n):''))}">${y} ${t} <span class="evp" aria-hidden="true">⌖</span></button>`:`<p class="evn">${y} ${t}</p>`}<small class="extnote">${bcite(v.s)}</small></li>`}).join('')+'</ol>';
 $('card').appendChild(s);EVD=d.events;if(!evList.on){evList.on=1;$('card').addEventListener('click',ev=>{const b=ev.target.closest&&ev.target.closest('.evgo');if(b&&EVD)evFly(EVD[+b.dataset.k])})}}
function evFly(v){const [x,y]=proj(v.pl.ll),sh=$('sheet').getBoundingClientRect(),k=Math.max(K,4);
 const cx=desk()?(AR?(sh.right+W())/2:sh.left/2):W()/2,cy=desk()?H()/2:Math.max(140,(sh.top+120)/2);
 gEp=gEp||root.append('g').attr('class','evpin');gEp.selectAll('*').remove();const g=gEp.append('g').attr('class','mk evpm').each(function(){this.__xy=[x,y]});g.append('circle').attr('r',7);scaleMarks();
 $('live').textContent=bpick(v.t)+(bpick(v.pl.n)?' · '+bpick(v.pl.n):'');
 svg.transition().duration(RM?0:DUR).call(zoom.transform,d3.zoomIdentity.translate(cx,cy).scale(k).translate(-x,-y))}
fit();getj('/basemap-map.json').then(b=>{BASE=b;render(false)}).catch(()=>render(false));
})();