// Renders text-free background layers for one series: node render_bg.js 2-big-stat
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const series = process.argv[2];
  const dir = __dirname;
  const out = path.join(dir, 'bg', series);
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 1500 } });
  await p.goto('file://' + path.join(dir, 'carousels.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.addStyleTag({ content: '.sc,.rc,.rl,.scr,.body,.folio,.rule,.pill,.k,.it,.line,.big,.hair{visibility:hidden!important}' });
  const ids = await p.$$eval('.slide', els => els.map(e => e.id));
  for (const id of ids.filter(i => i.startsWith(series + '-'))) {
    await (await p.$(`[id="${id}"]`)).screenshot({ path: path.join(out, `${id}.jpg`), type: 'jpeg', quality: 92 });
  }
  console.log('done', series);
  await b.close();
})();
