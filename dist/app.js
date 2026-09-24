(() => {
  'use strict';
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (!reduceMotion.matches) document.documentElement.classList.add('logo-motion');
  const intro = document.querySelector('#mountain-intro');
  const introSkip = intro.querySelector('.intro-skip');
  let introFinished = false;
  let introOpening = false;
  let introTimer;
  const finishIntro = () => {
    if (introFinished) return;
    introFinished = true;
    clearTimeout(introTimer);
    clearTimeout(window.kurdaIntroDeadline);
    const hadFocus = intro.contains(document.activeElement);
    document.documentElement.classList.remove('intro-active');
    document.documentElement.classList.add('site-revealed');
    document.querySelectorAll('[data-intro-inert]').forEach(el => {
      el.inert = false;
      el.removeAttribute('data-intro-inert');
    });
    intro.hidden = true;
    if (hadFocus) document.querySelector('.header .wordmark').focus({ preventScroll: true });
  };
  const openMountains = () => {
    if (introFinished || introOpening) return;
    introOpening = true;
    intro.classList.add('is-opening');
    introTimer = setTimeout(finishIntro, 2700);
  };
  introSkip.addEventListener('click', finishIntro);
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !introFinished) finishIntro();
  });
  intro.querySelector('.mountain-panel-left').addEventListener('transitionend', event => {
    if (event.propertyName === 'transform') finishIntro();
  });
  reduceMotion.addEventListener('change', event => { if (event.matches) finishIntro(); });
  if (document.documentElement.classList.contains('intro-active') && !reduceMotion.matches) {
    document.querySelectorAll('body > .skip-link, body > header, body > main, body > footer').forEach(el => {
      el.inert = true;
      el.setAttribute('data-intro-inert', '');
    });
    const wait = ms => new Promise(resolve => setTimeout(resolve, ms));
    const ready = Promise.all([...intro.querySelectorAll('img')].map(picture =>
      typeof picture.decode === 'function' ? picture.decode().catch(() => {}) : Promise.resolve()
    ));
    // Leave enough reading time once the mountain and both logos are ready.
    Promise.race([ready, wait(2200)]).then(() => wait(2800)).then(openMountains);
  } else finishIntro();
  const header = document.querySelector('.header');
  const toggle = document.querySelector('.menu-toggle');
  const menu = document.querySelector('#mobile-nav');
  const setMenu = (open) => {
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    menu.hidden = !open;
    header.classList.toggle('menu-open', open);
  };
  toggle.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
  menu.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setMenu(false)));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !menu.hidden) { setMenu(false); toggle.focus(); }
  });
  document.addEventListener('click', event => { if (!header.contains(event.target) && !menu.hidden) setMenu(false); });
  window.matchMedia('(min-width: 761px)').addEventListener('change', event => { if (event.matches) setMenu(false); });
  document.querySelector('#year').textContent = new Date().getFullYear();

  // Tall cards scroll fully into view before they pin and the next card overlaps.
  const serviceStack = document.querySelector('.service-stack');
  const serviceCards = [...serviceStack.querySelectorAll('.service-card')];
  const measureServiceCards = () => {
    serviceCards.forEach(card => {
      card.style.setProperty('--card-height', `${card.getBoundingClientRect().height}px`);
    });
    serviceStack.classList.add('stack-ready');
  };
  measureServiceCards();
  if ('ResizeObserver' in window) {
    const cardObserver = new ResizeObserver(measureServiceCards);
    serviceCards.forEach(card => cardObserver.observe(card));
  }
  window.addEventListener('resize', measureServiceCards, { passive: true });
  document.fonts.ready.then(measureServiceCards);

  const reveals = [...document.querySelectorAll('.reveal')];
  if ('IntersectionObserver' in window && !reduceMotion.matches) {
    document.documentElement.classList.add('motion');
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); } });
    }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });
    reveals.forEach(el => observer.observe(el));
    document.querySelectorAll('.facts .fact').forEach((el, index) => el.style.setProperty('--delay', `${index * 0.1}s`));
  }
  const layers = [...document.querySelectorAll('[data-parallax]')];
  let ticking = false;
  const paint = () => {
    if (!reduceMotion.matches) {
      layers.forEach(layer => {
        const section = layer.closest('section');
        const rect = section.getBoundingClientRect();
        if (rect.bottom > 0 && rect.top < innerHeight) {
          const offset = -rect.top * Number(layer.dataset.parallax);
          const limit = section.clientHeight * .065;
          layer.style.transform = `translate3d(0,${Math.max(-limit, Math.min(limit, offset)).toFixed(2)}px,0)`;
        }
      });
    }
    ticking = false;
  };
  const requestPaint = () => { if (!ticking) { ticking = true; requestAnimationFrame(paint); } };
  window.addEventListener('scroll', requestPaint, { passive: true });
  window.addEventListener('resize', requestPaint, { passive: true });
  reduceMotion.addEventListener('change', () => {
    if (reduceMotion.matches) { document.documentElement.classList.remove('motion'); layers.forEach(layer => layer.style.removeProperty('transform')); }
    else requestPaint();
  });
  requestPaint();
})();
