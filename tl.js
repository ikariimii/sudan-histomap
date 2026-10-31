/* Timeline (/timeline/): type filter (?type=all|ev|bat), spring scroll to periods, FLIP card transitions.
   Cards are server-rendered links (work without JS); enter/press motion is CSS (Map Designer card spec). prefers-reduced-motion: no FLIP, instant jumps. */
(function(){
'use strict';
var D=document,R=D.documentElement,TL=window.TL||{},RM=matchMedia('(prefers-reduced-motion: reduce)');
var rm=function(){return RM.matches};
var num=function(n){return TL.ar?String(n).replace(/\d/g,function(d){return '٠١٢٣٤٥٦٧٨٩'[d]}):String(n)};
var bar=D.querySelector('.bar'),cnt=D.getElementById('cnt'),cards=[].slice.call(D.querySelectorAll('.cd')),secs=[].slice.call(D.querySelectorAll('.per'));
R.classList.add('js');
/* sticky offsets follow the real header height (it wraps on phones) */
var bh=0;function setBh(){var h=bar?Math.round(bar.getBoundingClientRect().height):56;if(h!==bh){bh=h;R.style.setProperty('--bh',h+'px')}}
setBh();if(window.ResizeObserver&&bar)new ResizeObserver(setBh).observe(bar);else addEventListener('resize',setBh);
/* damped spring scroll (critically damped-ish, like a UIScrollView setContentOffset); any user input cancels it */
var raf=0;function stop(){if(raf){cancelAnimationFrame(raf);raf=0}}
['wheel','touchstart','keydown','mousedown'].forEach(function(t){addEventListener(t,stop,{passive:true})});
function springTo(el,done){
 stop();var target=function(){return Math.max(0,el.getBoundingClientRect().top+scrollY-bh)};
 if(rm()){scrollTo(0,target());done&&done();return}
 var x=scrollY,v=0,k=170,c=26,last=performance.now();
 (function step(now){var dt=Math.min(.032,(now-last)/1000);last=now;var T=target(),f=-k*(x-T)-c*v;v+=f*dt;x+=v*dt;scrollTo(0,x);
  if(Math.abs(T-x)<.5&&Math.abs(v)<4){scrollTo(0,T);raf=0;done&&done();return}raf=requestAnimationFrame(step)})(last);
}
D.addEventListener('click',function(ev){
 var a=ev.target.closest&&ev.target.closest('.jump a');if(!a||ev.metaKey||ev.ctrlKey||ev.shiftKey||ev.button)return;
 var s=D.getElementById(a.getAttribute('href').slice(1));if(!s||s.hidden)return;ev.preventDefault();
 var h=s.querySelector('.ph');history.replaceState(null,'',location.pathname+location.search+'#'+s.id);
 springTo(s,function(){if(h)h.focus({preventScroll:true})});
});
/* filter: radios (native arrow-key navigation), state in ?type=, FLIP of on-screen cards, scroll anchored to the first visible card */
var flt=D.querySelector('.flt'),N=cards.length;
function vis(c,t){return t==='all'||c.getAttribute('data-t')===t}
function count(t){var n=0;cards.forEach(function(c){if(vis(c,t))n++});if(cnt)cnt.textContent=(TL.cnt||'{n} / {N}').replace('{n}',String(n)).replace('{N}',String(N))}
function anchor(){var top=bh+8;for(var i=0;i<cards.length;i++){var c=cards[i];if(c.hidden)continue;var r=c.getBoundingClientRect();if(r.bottom>top)return {el:c,y:r.top}}return null}
function apply(t,anim){
 var vh=innerHeight,moving=[],first=new Map(),a=anchor();
 if(anim)cards.forEach(function(c){if(c.hidden)return;var r=c.getBoundingClientRect();if(r.bottom>-50&&r.top<vh+50)first.set(c,r.top)});
 var keep=a&&vis(a.el,t)?a:null;
 if(!keep&&a){for(var i=cards.indexOf(a.el);i<cards.length;i++)if(vis(cards[i],t)){keep={el:cards[i],y:a.y};break}}
 cards.forEach(function(c){c.hidden=!vis(c,t)});
 secs.forEach(function(s){var j=0;[].forEach.call(s.querySelectorAll('.cd'),function(c){if(!c.hidden)c.classList.toggle('r',!!(j++%2))});s.hidden=!j});
 if(keep){var d=keep.el.getBoundingClientRect().top-keep.y;if(Math.abs(d)>1)scrollTo(0,scrollY+d)}
 count(t);
 if(!anim||rm()||!Element.prototype.animate)return;
 cards.forEach(function(c){if(c.hidden)return;var r=c.getBoundingClientRect();if(r.bottom<-50||r.top>vh+50)return;
  var f=first.get(c);
  if(f==null)c.animate([{opacity:0,transform:'translateY(14px) scale(.97)'},{opacity:1,transform:'none'}],{duration:420,easing:'cubic-bezier(.32,1.28,.54,1)'});
  else if(Math.abs(f-r.top)>1)c.animate([{transform:'translateY('+(f-r.top)+'px)'},{transform:'none'}],{duration:520,easing:'cubic-bezier(.32,1.28,.54,1)'});
 });
}
var Q=new URLSearchParams(location.search),t0=Q.get('type');
if(flt){
 if(t0==='ev'||t0==='bat'){var r0=flt.querySelector('input[value='+t0+']');if(r0){r0.checked=true;apply(t0,false)}}
 flt.addEventListener('change',function(ev){var t=ev.target.value,q=new URLSearchParams(location.search);if(t==='all')q.delete('type');else q.set('type',t);
  var s=q.toString();history.replaceState(null,'',location.pathname+(s?'?'+s:'')+location.hash);apply(t,true)});
}
/* bfcache: restore the card after coming back from the map */
addEventListener('pageshow',function(e){if(e.persisted&&D.getAnimations)D.getAnimations().forEach(function(a){a.cancel()})});
})();
