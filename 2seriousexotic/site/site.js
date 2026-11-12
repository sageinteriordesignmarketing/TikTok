(() => {
  const $ = id => document.getElementById(id);
  const usd = (n, d = 0) => (n < 0 ? '-$' : '$') + Math.abs(n).toLocaleString('en-US', {minimumFractionDigits: d, maximumFractionDigits: d});
  const num = v => { const n = parseFloat(String(v).replace(/[^0-9.\-]/g, '')); return isFinite(n) ? n : 0; };

  // header + menu
  const hdr = $('hdr');
  const sc = () => hdr && hdr.classList.toggle('solid', scrollY > 60 || !document.querySelector('.hero, .phero:not(.short)'));
  addEventListener('scroll', sc, {passive: true}); sc();
  const ov = $('overlay'), open = $('menu-open'), close = $('menu-close');
  const setMenu = on => { ov.classList.toggle('open', on); ov.setAttribute('aria-hidden', !on); open.setAttribute('aria-expanded', on); document.body.style.overflow = on ? 'hidden' : ''; if (on) close.focus(); };
  open && open.addEventListener('click', () => setMenu(true));
  close && close.addEventListener('click', () => setMenu(false));
  addEventListener('keydown', e => { if (e.key === 'Escape' && ov.classList.contains('open')) setMenu(false); });

  // home: hero slideshow
  const slides = [...document.querySelectorAll('.slide')];
  if (slides.length && $('bars')) {
    const bars = [...$('bars').children], names = ['Lamborghini · Aventador S', 'Ferrari · SF90 Stradale', 'Bentley · Flying Spur', 'Bugatti · Chiron'];
    let i = 0, t;
    const show = n => {
      slides[i].classList.remove('on'); bars.forEach((b, k) => { b.classList.remove('on'); b.classList.toggle('done', k < n); });
      i = n; slides[i].classList.add('on'); void bars[i].offsetWidth; bars[i].classList.add('on');
      $('h-i').textContent = String(i + 1).padStart(2, '0'); $('h-make').textContent = names[i];
      clearTimeout(t); t = setTimeout(() => show((i + 1) % slides.length), 6000);
    };
    bars.forEach((b, k) => b.addEventListener('click', () => show(k)));
    t = setTimeout(() => show(1), 6000);
  }

  // home: model selector
  if ($('tabs')) {
    const M = [
      ['Bentley', 'Flying Spur', 'https://images.unsplash.com/photo-1618418721668-0d1f72aa4bab?w=2000&q=80', '48 mo', '7,500', '$50K', '$2,300'],
      ['Lamborghini', 'Huracán EVO', 'https://images.unsplash.com/photo-1612825173281-9a193378527e?w=2000&q=80', '36 mo', '5,000', '$45K', '$2,680'],
      ['Rolls-Royce', 'Wraith', 'https://images.unsplash.com/photo-1631295868223-63265b40d9e4?w=2000&q=80', '48 mo', '5,000', '$60K', '$3,500'],
      ['Ferrari', 'SF90 Stradale', 'https://images.unsplash.com/photo-1632441730372-d8509de481d1?w=2000&q=80', '39 mo', '3,000', '$95K', '$4,810'],
      ['McLaren', 'Artura Spider', 'img/artura.jpg', '60 mo', '3,500', '$54.5K', '$3,894'],
      ['Bugatti', 'Chiron', 'img/chiron.jpg', '60 mo', '2,000', 'Bespoke', 'On request'],
    ];
    const tabs = $('tabs');
    const pick = k => {
      const [make, model, img, term, miles, down, from] = M[k];
      [...tabs.children].forEach((b, j) => b.setAttribute('aria-selected', j === k));
      const el = $('carimg'); el.style.opacity = 0;
      setTimeout(() => { el.onload = () => el.style.opacity = 1; el.src = img; el.alt = make + ' ' + model; }, 200);
      $('ghost').textContent = make; $('m-make').textContent = make; $('m-model').textContent = model;
      $('m-term').textContent = term; $('m-miles').textContent = miles; $('m-down').textContent = down;
      $('m-from').innerHTML = from.startsWith('$') ? from + '<span style="font-size:.5em;color:var(--mute)"> /mo</span>' : from;
    };
    M.forEach((m, k) => { const b = document.createElement('button'); b.setAttribute('role', 'tab'); b.textContent = m[0]; b.setAttribute('aria-selected', k === 0); b.onclick = () => pick(k); tabs.appendChild(b); });
    pick(0);
  }

  // home: slider configurator
  if ($('f') && $('price')) {
    const calc = () => {
      ['price', 'down', 'term', 'res'].forEach(id => { const e = $(id); e.style.setProperty('--p', ((e.value - e.min) / (e.max - e.min) * 100) + '%'); });
      const p = +$('price').value, d = +$('down').value, n = +$('term').value, r = +$('res').value;
      const resid = p * r / 100, adj = p - d, mf = .00285;
      const dep = Math.max(0, (adj - resid) / n), rent = (adj + resid) * mf, tax = (dep + rent) * .07;
      $('o-price').textContent = usd(p); $('o-down').textContent = usd(d); $('o-term').textContent = n + ' months'; $('o-res').textContent = r + '%';
      $('pay').innerHTML = usd(dep + rent + tax) + '<small>/ MO</small>';
      $('b1').textContent = usd(dep); $('b2').textContent = usd(rent); $('b3').textContent = usd(tax);
    };
    $('f').addEventListener('input', calc); calc();
  }

  // collection filter
  const filt = document.querySelector('.filters[aria-label="Filter by class"]');
  if (filt) filt.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    [...filt.children].forEach(x => x.setAttribute('aria-pressed', x === b));
    document.querySelectorAll('.vcard').forEach(c => c.hidden = !(b.dataset.f === 'All' || c.dataset.type === b.dataset.f));
  });

  // full calculator
  if ($('fc')) {
    const P = {
      artura:   {msrp: '234,327.50', cap: '234,327.50', term: 60, miles: '3,500', resid: '27.1842', mf: '0.00693', down: '54,527.13', trade: '0', fees: '11,578.72', tax: '7.5'},
      huracan:  {msrp: '268,000', cap: '262,000', term: 36, miles: '5,000', resid: '62', mf: '0.00285', down: '45,000', trade: '0', fees: '1,995', tax: '7'},
      cullinan: {msrp: '395,000', cap: '385,000', term: 48, miles: '7,500', resid: '55', mf: '0.00275', down: '70,000', trade: '0', fees: '2,495', tax: '7'},
      trx:      {msrp: '98,000', cap: '96,000', term: 60, miles: '10,000', resid: '45', mf: '0.00310', down: '20,000', trade: '0', fees: '1,495', tax: '7'},
    };
    const ids = ['msrp', 'cap', 'term', 'miles', 'resid', 'mf', 'down', 'trade', 'fees', 'tax'];
    const run = () => {
      const v = Object.fromEntries(ids.map(k => [k, num($(k).value)]));
      const isApr = v.mf > 0.1, mf = isApr ? v.mf / 2400 : v.mf;
      $('mf-n').textContent = isApr ? `Read as APR → MF ${mf.toFixed(5)}` : `≈ ${(mf * 2400).toFixed(2)}% APR`;
      const residual = v.msrp * v.resid / 100; $('resid-n').textContent = usd(residual, 2) + ' at term end';
      const adj = v.cap - v.down - v.trade, n = Math.max(1, v.term);
      const dep = Math.max(0, (adj - residual) / n), rent = Math.max(0, (adj + residual) * mf), base = dep + rent, tax = base * v.tax / 100, m = base + tax;
      $('fpay').innerHTML = usd(m) + '<small>/ MO</small>';
      $('o-dep').textContent = usd(dep, 2); $('o-rent').textContent = usd(rent, 2); $('o-tax').textContent = usd(tax, 2); $('o-base').textContent = usd(base, 2);
      $('o-das').textContent = usd(v.down + v.fees + m, 2); $('o-total').textContent = usd(m * n + v.down + v.trade + v.fees, 2);
      $('bd').style.flexGrow = dep; $('br').style.flexGrow = rent; $('bt').style.flexGrow = tax;
    };
    const pre = $('presets');
    pre.addEventListener('click', e => {
      const b = e.target.closest('button'); if (!b) return;
      const d = P[b.dataset.p]; ids.forEach(k => $(k).value = d[k]);
      [...pre.children].forEach(x => x.setAttribute('aria-pressed', x === b)); run();
    });
    $('fc').addEventListener('input', () => { [...pre.children].forEach(x => x.setAttribute('aria-pressed', 'false')); run(); });
    $('fc').addEventListener('submit', e => e.preventDefault());
    run();
  }

  // application steps
  if ($('af')) {
    const steps = [...document.querySelectorAll('#af fieldset')], prog = [...$('prog').children];
    let s = 0;
    const go = n => {
      s = n;
      steps.forEach((f, k) => { f.hidden = k !== s; f.style.display = k === s ? 'contents' : 'none'; });
      prog.forEach((p, k) => { p.className = k < s ? 'done' : k === s ? 'now' : ''; });
      $('back').hidden = s === 0; $('next').textContent = s === 3 ? 'Submit request' : 'Continue';
      if (s === 3) {
        const use = [...document.querySelectorAll('input[name=use]')].findIndex(r => r.checked);
        const rows = [['Vehicle', $('a-car').value], ['Condition', $('a-cond').value], ['Price', '$' + $('a-price').value], ['Use', ['Personal', 'Business', 'Rental fleet'][use]],
          ['Name', ($('a-first').value + ' ' + $('a-last').value).trim() || '–'], ['Contact', [$('a-email').value, $('a-phone').value].filter(Boolean).join(' · ') || '–'],
          ['Term', $('a-term').value], ['Miles', $('a-miles').value + ' / yr'], ['Down', '$' + $('a-down').value], ['Trade-in', $('a-trade').value]];
        $('review').innerHTML = rows.map(([k, v]) => `<div style="display:flex;justify-content:space-between;gap:20px;padding:14px 0;border-top:1px solid var(--hair)"><span class="mute">${k}</span><span>${String(v).replace(/</g, '&lt;')}</span></div>`).join('');
      }
    };
    $('back').addEventListener('click', () => go(s - 1));
    $('af').addEventListener('submit', e => {
      e.preventDefault();
      if (s < 3) return go(s + 1);
      $('sent').hidden = false; $('sent').textContent = 'Request ready. (Mockup: connect this form to the CRM before launch.)';
    });
  }
})();
