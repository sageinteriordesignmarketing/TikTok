// Screenshots every .slide in carousels.html to out/<template>/<n>.png at 1080x1350.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const dir = __dirname;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 1500 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(dir, 'carousels.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const ids = await p.$$eval('.slide', els => els.map(e => e.id));
  for (const id of ids) {
    const [tpl, n] = [id.slice(0, id.lastIndexOf('-')), id.slice(id.lastIndexOf('-') + 1)];
    const out = path.join(dir, 'out', tpl);
    fs.mkdirSync(out, { recursive: true });
    await (await p.$(`[id="${id}"]`)).screenshot({ path: path.join(out, `${tpl}-${n}.png`) });
  }
  const over = await p.$$eval('.slide', els => els.map(s => {
    const r = s.getBoundingClientRect();
    const bad = [...s.querySelectorAll('.body *')].filter(e => { const q = e.getBoundingClientRect(); return q.right > r.right - 60 || q.bottom > r.bottom - 60; }).length;
    return bad ? s.id : null;
  }).filter(Boolean));
  console.log(ids.length, 'slides; overflow:', JSON.stringify(over));
  await b.close();
})();
