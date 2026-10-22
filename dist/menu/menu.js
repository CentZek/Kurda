(() => {
 'use strict';
 const data=JSON.parse(document.querySelector('#menu-data').textContent);
 const ui=JSON.parse(document.querySelector('#menu-ui').textContent);
 const lang=document.documentElement.lang;
 const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
 const cats=data.categories, items=new Map(cats.flatMap(c=>c.items.map(i=>[i.id,{...i,category:c.id,group:c.group}])));
 const cards=new Map($$('[data-item]').map(el=>[el.dataset.item,el]));
 const sections=$$('[data-section]'), params=new URLSearchParams(location.search);
 const validGroups=['food','drinks','bar','gifts'];
 const state={group:validGroups.includes(params.get('section'))?params.get('section'):'food',category:'all',query:params.get('q')||'',sort:['low','high','az'].includes(params.get('sort'))?params.get('sort'):'menu',picks:params.get('picks')==='1'};
 if(cats.some(c=>c.id===params.get('category'))){state.category=params.get('category');state.group=cats.find(c=>c.id===state.category).group;}
 const hashCategory=location.hash.replace('#section-','');
 if(cats.some(c=>c.id===hashCategory)){state.category=hashCategory;state.group=cats.find(c=>c.id===hashCategory).group;}
 const storage={get(key){try{return localStorage.getItem(key);}catch{return null;}},set(key,value){try{localStorage.setItem(key,value);}catch{/* browsing still works without storage */}}};
 let saved=new Set();try{const list=JSON.parse(storage.get('kurda-menu-picks-v1')||'[]');if(Array.isArray(list))saved=new Set(list.filter(id=>items.has(id)));}catch{}
 let paused=storage.get('kurda-menu-motion')==='paused'||matchMedia('(prefers-reduced-motion: reduce)').matches;
 function motion(){document.documentElement.classList.toggle('motion-paused',paused);$('#motion').textContent=paused?ui.play:ui.pause;$('#motion').setAttribute('aria-pressed',String(paused));}
 const normalize=s=>s.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f\u064b-\u065f\u0670\u0640]/g,'').replace(/[يى]/g,'ی').replace(/ك/g,'ک').replace(/[أإآ]/g,'ا');
 const searchable=new Map(cats.flatMap(c=>c.items.map(i=>[i.id,normalize([...Object.values(i.names),...Object.values(c.names),...Object.values(i.flavoursByLanguage).flat()].join(' '))])));
 function syncLinks(){
  const p=new URLSearchParams();if(state.group!=='food')p.set('section',state.group);if(state.category!=='all')p.set('category',state.category);if(state.query)p.set('q',state.query);if(state.sort!=='menu')p.set('sort',state.sort);if(state.picks)p.set('picks','1');
  const suffix=p.size?'?'+p.toString():'';history.replaceState(null,'',location.pathname+suffix);
  $$('[data-language]').forEach(a=>{a.href='/menu'+(a.dataset.language==='en'?'':'/'+a.dataset.language+'/')+suffix;});
 }
 function saveButtons(){
  $$('[data-save]').forEach(b=>{const active=saved.has(b.dataset.save);b.setAttribute('aria-pressed',String(active));b.setAttribute('aria-label',(active?ui.remove:ui.save)+' '+items.get(b.dataset.save).names[lang]);});
  $('#picks-count').textContent=saved.size;$('#picks').setAttribute('aria-label',ui.saved+' ('+saved.size+')');
 }
 function render(animate=true){
  const query=normalize(state.query.trim()), global=!!query||state.picks;
  const tokens=query.split(/\s+/).filter(Boolean);let count=0;
  const minPrice=i=>{const p=Object.values(i.prices).filter(p=>p!==null);return p.length?Math.min(...p):null;};
  for(const c of cats){
   const section=$('[data-section="'+c.id+'"]');let shown=0;
   const sorted=[...c.items];if(state.sort!=='menu')sorted.sort((a,b)=>{if(state.sort==='az')return a.names[lang].localeCompare(b.names[lang],lang);const x=minPrice(a),y=minPrice(b);return x===null?(y===null?0:1):y===null?-1:state.sort==='low'?x-y:y-x;});
   const grid=section.querySelector('.card-grid');
   sorted.forEach(i=>{const match=(global||c.group===state.group)&&(state.category==='all'||c.id===state.category)&&(!state.picks||saved.has(i.id))&&tokens.every(t=>searchable.get(i.id).includes(t));const card=cards.get(i.id);card.hidden=!match;grid.append(card);if(match){shown++;count++;}});
   section.hidden=!shown;section.classList.remove('appear');if(shown&&animate){void section.offsetWidth;section.classList.add('appear');}
  }
  $$('[data-browse]').forEach(a=>{if(!global&&a.dataset.browse===state.group)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current');});
  $$('.category-tile').forEach(a=>{a.hidden=a.dataset.group!==state.group;if(a.dataset.category===state.category)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current');});
  $('.category-gallery').hidden=global;
  const select=$('#category-select'),available=cats.filter(c=>global||c.group===state.group);select.replaceChildren(new Option(ui.all,'all'),...available.map(c=>new Option(c.names[lang],c.id)));select.value=state.category;
  $('#result-count').textContent=(query?ui.results+' · ':'')+count+' '+ui.items;
  $('#empty').hidden=count>0;$('#picks-note').hidden=!state.picks;$('#picks').setAttribute('aria-pressed',String(state.picks));$('#clear-search').hidden=!state.query;
  saveButtons();syncLinks();
 }
 function scrollToMenu(){const top=$('.welcome').getBoundingClientRect().bottom+scrollY;window.scrollTo({top,behavior:paused?'instant':'smooth'});}
 $$('[data-browse]').forEach(a=>a.addEventListener('click',event=>{event.preventDefault();state.group=a.dataset.browse;state.category='all';state.query='';state.picks=false;$('#search').value='';render();$('.category-gallery').scrollLeft=0;scrollToMenu();}));
 $$('.category-tile').forEach(a=>a.addEventListener('click',event=>{event.preventDefault();state.category=state.category===a.dataset.category?'all':a.dataset.category;render();}));
 $('#category-select').addEventListener('change',event=>{state.category=event.target.value;render();});
 $('#sort').value=state.sort;$('#sort').addEventListener('change',event=>{state.sort=event.target.value;render();});
 $('#search').value=state.query;$('#search').addEventListener('input',event=>{state.query=event.target.value;state.category='all';state.picks=false;render(false);});
 $('#search-form').addEventListener('submit',event=>{event.preventDefault();$('#search').blur();scrollToMenu();});
 $('#clear-search').addEventListener('click',()=>{state.query='';state.category='all';$('#search').value='';render();$('#search').focus();});
 $('#picks').addEventListener('click',()=>{state.picks=!state.picks;state.query='';state.category='all';$('#search').value='';render();scrollToMenu();});
 $$('[data-save]').forEach(b=>b.addEventListener('click',()=>{const id=b.dataset.save;saved.has(id)?saved.delete(id):saved.add(id);storage.set('kurda-menu-picks-v1',JSON.stringify([...saved]));if(state.picks)render(false);else saveButtons();}));
 $('#reset').addEventListener('click',()=>{state.query='';state.picks=false;state.category='all';$('#search').value='';render();scrollToMenu();});
 $('#motion').addEventListener('click',()=>{paused=!paused;storage.set('kurda-menu-motion',paused?'paused':'running');motion();});
 const dock=$('#menu');new ResizeObserver(()=>document.documentElement.style.setProperty('--dock',dock.offsetHeight+'px')).observe(dock);
 motion();render(false);document.documentElement.classList.add('ready');
 if(hashCategory&&cats.some(c=>c.id===hashCategory))requestAnimationFrame(scrollToMenu);
})();
