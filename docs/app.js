const menu = document.querySelector('.menu-toggle');
menu?.addEventListener('click', () => {
 const nav=document.querySelector('.nav'); const open=nav.classList.toggle('open');
 menu.setAttribute('aria-expanded',String(open)); menu.textContent=open?'Close':'Menu';
});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu){document.querySelector('.nav').classList.remove('open');menu.setAttribute('aria-expanded','false');menu.textContent='Menu';}});
const filterForm=document.querySelector('[data-filter-form]');
if(filterForm){
 const cards=[...document.querySelectorAll('[data-search]')];
 const search=filterForm.querySelector('input');
 const normal=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
 function filter(){
  const query=normal(search?.value||'').trim();
  let count=0;
  cards.forEach(card=>{
   let visible=query.split(/\s+/).every(word=>normal(card.dataset.search).includes(word));
   filterForm.querySelectorAll('select').forEach(select=>{const val=select.value; if(val && !(card.dataset[select.name]||'').split('|').includes(val))visible=false;});
   card.hidden=!visible;if(visible)count++;
  });
  document.querySelector('[data-result-count]').textContent=`${count} of ${cards.length} ${filterForm.dataset.noun||'publications'}`;
  document.querySelector('[data-empty]').hidden=count>0;
 }
 filterForm.addEventListener('input',filter);filterForm.addEventListener('change',filter);
 document.querySelector('[data-reset]')?.addEventListener('click',()=>{filterForm.reset();filter();search?.focus();});
 filterForm.addEventListener('submit',e=>e.preventDefault());
}
document.querySelectorAll('[data-print]').forEach(b=>b.addEventListener('click',()=>window.print()));
