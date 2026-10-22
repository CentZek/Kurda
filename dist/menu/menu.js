/* Progressive enhancement: all 53 dishes and prices are already in the HTML. */
(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('menu-data').textContent);
  const results = document.getElementById('results');
  const initial = results.innerHTML;
  const search = document.getElementById('search');
  const sort = document.getElementById('sort');
  const categories = document.getElementById('categories');
  const savedFilter = document.getElementById('saved-filter');
  const empty = document.getElementById('empty-state');
  const resultCount = document.getElementById('result-count');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const motionToggle = document.getElementById('motion-toggle');
  let motionPaused = false;
  try {motionPaused = localStorage.getItem('kurda-menu-motion') === 'paused';} catch {}
  function updateMotion() {
    document.documentElement.classList.toggle('motion-paused', motionPaused);
    motionToggle.setAttribute('aria-pressed', String(motionPaused));
    document.getElementById('motion-label').textContent = motionPaused ? 'Play motion' : 'Pause motion';
  }
  motionToggle.addEventListener('click', () => {motionPaused = !motionPaused; updateMotion(); try {localStorage.setItem('kurda-menu-motion', motionPaused ? 'paused' : 'playing');} catch {}});
  updateMotion();
  const items = data.categories.flatMap(category => category.items.map(item => ({...item, category: category.id, categoryName: category.name})));
  const itemMap = new Map(items.map(item => [item.id, item]));
  const templates = new Map([...results.querySelectorAll('[data-item]')].map(card => [card.dataset.item, card.outerHTML]));
  let category = 'all', onlySaved = false, searchTimer, toastTimer;
  let saved = new Set();
  try {
    const stored = JSON.parse(localStorage.getItem('kurda-menu-picks-v1') || '[]');
    if (Array.isArray(stored)) saved = new Set(stored.filter(id => itemMap.has(id)));
  } catch { /* Browsing remains available when storage is restricted. */ }
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const minimum = item => Math.min(...Object.values(item.prices));
  let observer;
  if ('IntersectionObserver' in window) observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      if (!reducedMotion.matches) entry.target.classList.add('reveal');
      observer.unobserve(entry.target);
    });
  }, {threshold: .08});
  function animateCards() {
    observer?.disconnect();
    results.querySelectorAll('.menu-card').forEach((card, index) => {
      card.style.setProperty('--delay', `${(index % 3) * 45}ms`);
      observer?.observe(card);
    });
  }
  function updateSavedButtons() {
    document.getElementById('saved-count').textContent = saved.size;
    document.querySelectorAll('[data-save]').forEach(button => {
      const active = saved.has(button.dataset.save);
      button.setAttribute('aria-pressed', String(active));
      button.setAttribute('aria-label', `${active ? 'Remove' : 'Save'} ${itemMap.get(button.dataset.save).name}${active ? ' from my picks' : ''}`);
    });
  }
  function render() {
    const query = normalize(search.value.trim());
    const matching = items.filter(item => (category === 'all' || item.category === category) && (!onlySaved || saved.has(item.id)) && (!query || normalize([item.name, item.categoryName, ...(item.flavours || [])].join(' ')).includes(query)));
    const matchIds = new Set(matching.map(item => item.id));
    if (sort.value === 'menu') {
      results.innerHTML = initial;
      results.querySelectorAll('[data-item]').forEach(card => {if (!matchIds.has(card.dataset.item)) card.remove();});
      results.querySelectorAll('[data-section]').forEach(section => {if (!section.querySelector('[data-item]')) section.remove();});
    } else {
      matching.sort(sort.value === 'name' ? (a,b) => a.name.localeCompare(b.name) : sort.value === 'low' ? (a,b) => minimum(a)-minimum(b) : (a,b) => minimum(b)-minimum(a));
      const heading = document.createElement('div');
      heading.className = 'sorted-heading';
      const title = document.createElement('h3');
      title.textContent = onlySaved ? 'Your picks' : category === 'all' ? 'The whole menu' : data.categories.find(cat => cat.id === category).name;
      heading.append(title);
      if (sort.value !== 'name') {const hint = document.createElement('p'); hint.textContent = 'Sorted by lowest available size price'; heading.append(hint);}
      results.replaceChildren(heading);
      const grid = document.createElement('div'); grid.className = 'card-grid';
      grid.innerHTML = matching.map(item => templates.get(item.id)).join(''); results.append(grid);
    }
    empty.hidden = matching.length > 0;
    results.hidden = matching.length === 0;
    document.getElementById('empty-title').textContent = onlySaved && saved.size === 0 ? 'Your favourites start here.' : 'No matches just yet.';
    document.getElementById('empty-copy').textContent = onlySaved && saved.size === 0 ? 'Tap the heart beside anything you love. Your picks will be waiting here.' : 'Try another search, or explore the whole menu.';
    const label = onlySaved ? 'saved pick' : 'item';
    resultCount.textContent = matching.length === 53 && !onlySaved && !query && category === 'all' ? '53 things to love' : `${matching.length} ${label}${matching.length === 1 ? '' : 's'}${query ? ' matching your search' : ''}`;
    document.querySelector('.search-clear').hidden = !search.value;
    document.getElementById('saved-note').hidden = !onlySaved || saved.size === 0;
    savedFilter.setAttribute('aria-pressed', String(onlySaved));
    categories.querySelectorAll('[data-category]').forEach(button => {const active = button.dataset.category === category; button.classList.toggle('active', active); button.setAttribute('aria-pressed', String(active));});
    updateSavedButtons(); animateCards();
  }
  function bringResultsIntoView() {
    const tools = document.getElementById('menu-tools');
    const target = document.querySelector('.menu-intro').offsetTop + document.querySelector('.menu-intro').offsetHeight;
    window.scrollTo({top: target, behavior: reducedMotion.matches ? 'instant' : 'smooth'});
  }
  categories.addEventListener('click', event => {
    const button = event.target.closest('[data-category]'); if (!button) return;
    category = button.dataset.category; render();
    const railRect = categories.getBoundingClientRect(), buttonRect = button.getBoundingClientRect();
    categories.scrollBy({left: buttonRect.left - railRect.left - (railRect.width-buttonRect.width)/2, behavior: reducedMotion.matches ? 'instant' : 'smooth'});
    bringResultsIntoView();
  });
  search.addEventListener('input', () => {clearTimeout(searchTimer); searchTimer = setTimeout(render, 90);});
  search.addEventListener('keydown', event => {if (event.key === 'Escape') {search.value = ''; render();}});
  document.querySelector('.search-clear').addEventListener('click', () => {search.value = ''; render(); search.focus();});
  sort.addEventListener('change', () => {render(); bringResultsIntoView();});
  savedFilter.addEventListener('click', () => {onlySaved = !onlySaved; category = 'all'; search.value = ''; render(); bringResultsIntoView();});
  document.getElementById('reset').addEventListener('click', () => {onlySaved = false; category = 'all'; search.value = ''; sort.value = 'menu'; render(); categories.querySelector('button').focus({preventScroll:true}); bringResultsIntoView();});
  results.addEventListener('click', event => {
    const button = event.target.closest('[data-save]'); if (!button) return;
    const id = button.dataset.save, removing = saved.has(id);
    if (removing) saved.delete(id); else saved.add(id);
    let persisted = true;
    try {localStorage.setItem('kurda-menu-picks-v1', JSON.stringify([...saved]));} catch {persisted = false;}
    updateSavedButtons();
    if (onlySaved && removing) {render(); const next = results.querySelector('[data-save]'); (next || document.getElementById('reset')).focus({preventScroll:true});}
    const toast = document.getElementById('toast');
    toast.textContent = removing ? 'Removed from your picks' : persisted ? 'Saved to My picks · show your server when ready' : 'Saved for this visit · device storage is unavailable';
    clearTimeout(toastTimer); toast.classList.add('visible'); toastTimer = setTimeout(() => toast.classList.remove('visible'), 2400);
  });
  // Keep anchor offsets correct with text zoom, rotation and mobile safe areas.
  if ('ResizeObserver' in window) new ResizeObserver(entries => {
    document.documentElement.style.setProperty('--tools-height', `${entries[0].target.offsetHeight}px`);
  }).observe(document.getElementById('menu-tools'));
  document.querySelector('.back-top').addEventListener('click', event => {event.preventDefault(); window.scrollTo({top:0,behavior:reducedMotion.matches?'instant':'smooth'}); document.querySelector('.brand').focus({preventScroll:true});});
  document.addEventListener('visibilitychange', () => {document.querySelectorAll('.hero-sun,.hero-drinks,.ticker>div').forEach(el => {el.style.animationPlayState = document.hidden ? 'paused' : 'running';});});
  updateSavedButtons(); animateCards();
})();
