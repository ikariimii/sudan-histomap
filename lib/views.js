// Shared helpers for lens/diff/era views. Reads data/ and db/ read-only.
// JSON is loaded with synchronous XHR so the existing synchronous render code keeps working.
// Works over http (python3 -m http.server) or headless Chrome with --allow-file-access-from-files.
window.V=(function(){
 const cache={};
 function loadJSON(p){if(p in cache)return cache[p];let r=null;try{const x=new XMLHttpRequest();x.open('GET',p+'?v='+Date.now(),false);x.send();if((x.status===200||x.status===0)&&x.responseText)r=JSON.parse(x.responseText);}catch(e){r=null}return cache[p]=r;}
 const LANGS={main:['Main dataset','البيانات الرئيسية'],zh:['Chinese sources','المصادر الصينية'],ru:['Russian sources','المصادر الروسية'],fr:['French sources','المصادر الفرنسية'],de:['German sources','المصادر الألمانية'],es:['Spanish sources','المصادر الإسبانية'],ar:['Arabic sources','المصادر العربية']};
 const STATUS={agree:['agrees','متوافق','#3f7d4a'],conflict:['conflicts','متعارض','#b3261e'],partial:['partial','جزئي','#c98a1a'],'no-conflict':['no conflict','لا تعارض','#5f7d8e'],'no-dates':['no dates','بلا تواريخ','#8a8a8a'],'unknown-era-id':['unknown era id','معرّف غير معروف','#8a8a8a']};
 function items(lens){if(!lens)return null;if(Array.isArray(lens))return lens;return lens.items||lens.sources||[];}
 function eraIds(it){const e=it.era_ids||it.eras||it.era_id;return e==null?[]:Array.isArray(e)?e:[e];}
 function srcTable(){return (window.HISTO&&HISTO.meta&&HISTO.meta.sources)||{};}
 function cite(id,lens){const T=srcTable();let r=T[id];
  if(!r&&lens){const it=items(lens).find(i=>i.id===id);if(it)r={author:it.author||it.outlet||it.author_outlet,title:it.title||it.title_original,publisher:it.publisher||it.outlet,year:it.year||it.date,url:it.url,lang:it.lang||it.original_language};}
  if(!r)return {html:`${id} <small>(unresolved ID)</small>`,lang:'',ok:false};
  const t=[r.author,r.year&&'('+r.year+')',r.title&&'<i>'+r.title+'</i>',r.edition,r.publisher,r.pages&&'pp. '+r.pages].filter(Boolean).join(' ');
  return {html:t+(r.url?` <a href="${r.url}" target="_blank">link</a>`:'')+(r.note?` <small>— ${r.note}</small>`:''),lang:r.lang||'',ok:true,text:[r.author,r.year&&'('+r.year+')',r.title].filter(Boolean).join(' ')};}
 function citeText(id){const c=cite(id);return c.text||id;}
 return {loadJSON,LANGS,STATUS,items,eraIds,cite,citeText,srcTable};
})();
