// Shared helpers for lens/diff/era views. Reads data/ and db/ read-only.
// JSON is loaded with synchronous XHR so the existing synchronous render code keeps working.
// Works over http (python3 -m http.server) or headless Chrome with --allow-file-access-from-files.
window.V=(function(){
 const cache={};
 function loadJSON(p){if(p in cache)return cache[p];let r=null;try{const x=new XMLHttpRequest();x.open('GET',p+'?v='+Date.now(),false);x.send();if((x.status===200||x.status===0)&&x.responseText)r=JSON.parse(x.responseText);}catch(e){r=null}return cache[p]=r;}
 const LANGS={en:['English-language sources','مصادر بالإنجليزية'],main:['Main dataset','البيانات الرئيسية'],zh:['Chinese sources','المصادر الصينية'],ru:['Russian sources','المصادر الروسية'],fr:['French sources','المصادر الفرنسية'],de:['German sources','المصادر الألمانية'],es:['Spanish sources','المصادر الإسبانية'],ar:['Arabic sources','المصادر العربية']};
 const STATUS={agree:['agrees','متوافق','#3f7d4a'],conflict:['conflicts','متعارض','#b3261e'],partial:['partial','جزئي','#c98a1a'],'no-conflict':['no conflict','لا تعارض','#5f7d8e'],'no-dates':['no dates','بلا تواريخ','#8a8a8a'],'unknown-era-id':['unknown era id','معرّف غير معروف','#8a8a8a']};
 function items(lens){if(!lens)return null;if(Array.isArray(lens))return lens;return lens.items||lens.sources||[];}
 function eraIds(it){const e=it.era_ids||it.eras||it.era_id;return e==null?[]:Array.isArray(e)?e:[e];}
 const EXTRA={};const real=r=>r&&(r.title||r.author||r.title_original||r.outlet);
 function addSources(o){if(o&&typeof o==='object')Object.keys(o).forEach(k=>{const r=o[k];if(real(r)&&!real(EXTRA[k]))EXTRA[k]=r});}
 function addGeo(){const g=loadJSON('db/geopolitics_sources.json');const L=Array.isArray(g)?g:(g&&(g.sources||g.items))||[];const o={};
  L.forEach(x=>{if(x&&x.id)o[x.id]={author:x.outlet||x.author,title:x.title_original||x.title,title_en:x.title_en&&x.title_en!=='same'?x.title_en:'',year:x.date||x.year,url:x.url,lang:(x.language||x.lang||'').toLowerCase(),affiliation:x.affiliation_bias||'',verification:x.verification||'',kind:x.source_type||''}});addSources(o);}
 const isAR=()=>document.documentElement.lang==='ar'||/[?&]lang=ar/.test(location.search);
 function badges(r){if(!r)return '';const B=(t,c)=>`<span class="badge" style="display:inline-block;font:bold 10px sans-serif;color:#fff;background:${c};padding:0 4px;border-radius:2px;margin-inline-start:3px">${t}</span>`,ar=isAR();let h='';
  if(/VERIFY/.test(r.verification||''))h+=B(ar?'غير مُتحقَّق':'unverified','#b3261e');
  if(/opinion/i.test([r.kind,r.source_type,r.publisher].join(' ')))h+=B(ar?'رأي':'opinion','#6b4c9a');
  const af=r.affiliation||r.affiliation_bias;if(af)h+=` <small class="affil" style="color:#5a4a30">[${ar?'الانتماء':'Affiliation'}: <bdi>${af}</bdi>]</small>`;return h;}
 function lensItem(lang,id){if(!['ar','de','es','fr','ru','zh'].includes(lang))return null;const f=loadJSON('db/lens_'+lang+'.json');if(!f)return null;if(f.meta)addSources(f.meta.sources);return items(f).find(i=>i.id===id)||null;}
 function srcTable(){return Object.assign({},EXTRA,(window.HISTO&&HISTO.meta&&HISTO.meta.sources)||{});}
 function resolved(id){return !!srcTable()[id];}
 const PENDING=['citation pending','المرجع قيد التوثيق'];
 function cite(id,lens){const T=srcTable();let r=T[id];
  if(!r&&lens){const it=items(lens).find(i=>i.id===id);if(it)r={author:it.author||it.outlet||it.author_outlet,title:it.title||it.title_original,publisher:it.publisher||it.outlet,year:it.year||it.date,url:it.url,lang:it.lang||it.original_language};}
  if(!r){const ar=document.documentElement.lang==='ar'||/[?&]lang=ar/.test(location.search);return {html:`<span class="pending" title="${String(id).replace(/"/g,'')}" style="color:#8a5a00;font-style:italic">⧗ ${PENDING[ar?1:0]}</span>`,lang:'',ok:false,text:PENDING[ar?1:0]};}
  const t=[r.lang&&r.lang!=='en'?'<b style="font:bold 10px sans-serif">['+r.lang.toUpperCase()+']</b>':'',r.author,r.year&&'('+r.year+')',r.title&&'<i>'+r.title+'</i>'+(r.title_en&&r.title_en!==r.title?' ['+r.title_en+']':''),r.edition,r.publisher,r.pages&&'pp. '+r.pages].filter(Boolean).join(' ');
  return {html:t+(r.url?` <a href="${r.url}" target="_blank">link</a>`:'')+(r.note?` <small>— ${r.note}</small>`:'')+badges(r),lang:r.lang||'',ok:true,text:[r.author,r.year&&'('+r.year+')',r.title].filter(Boolean).join(' ')};}
 function citeText(id){const c=cite(id);return c.text||id;}
 return {loadJSON,LANGS,STATUS,items,eraIds,cite,citeText,srcTable,addSources,addGeo,badges,lensItem,resolved,PENDING};
})();
