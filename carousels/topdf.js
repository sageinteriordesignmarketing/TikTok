// Exports each carousel series in carousels.html to its own multi-page PDF (1080x1350 px pages).
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const dir = __dirname;
  const out = path.join(dir, 'pdf');
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto('file://' + path.join(dir, 'carousels.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const groups = await p.$$eval('.slide', els => [...new Set(els.map(e => e.id.slice(0, e.id.lastIndexOf('-'))))]);
  for (const g of groups) {
    await p.evaluate((g) => {
      document.querySelectorAll('.slide').forEach(s => { s.style.display = s.id.startsWith(g + '-') ? '' : 'none'; s.style.margin = '0'; s.style.breakAfter = 'page'; });
      document.body.style.background = 'none'; document.body.style.margin = '0';
    }, g);
    await p.pdf({ path: path.join(out, `Sage-${g}.pdf`), width: '1080px', height: '1350px', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
    console.log('pdf', g);
  }
  await b.close();
})();
