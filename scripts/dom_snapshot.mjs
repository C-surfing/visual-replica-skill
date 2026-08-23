#!/usr/bin/env node
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

function arg(name, fallback = undefined) {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 ? process.argv[i + 1] : fallback;
}

const url = arg('url');
const out = arg('out', '.ui-replica/dom-snapshot.json');
const width = Number(arg('width', '390'));
const height = Number(arg('height', '844'));
const selector = arg('selector', 'body *');
const visibleOnly = arg('visible-only', 'true') !== 'false';

if (!url) {
  console.error("Usage: node scripts/dom_snapshot.mjs --url http://localhost:3000 --selector '.card, h1, button'");
  process.exit(2);
}

fs.mkdirSync(path.dirname(out), { recursive: true });
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width, height } });
await page.goto(url, { waitUntil: 'networkidle' });
await page.evaluate(async () => { if (document.fonts?.ready) await document.fonts.ready; });

const result = await page.evaluate(({ sel, visibleOnly }) => {
  const keys = [
    'display','position','box-sizing','margin-top','margin-right','margin-bottom','margin-left',
    'padding-top','padding-right','padding-bottom','padding-left','row-gap','column-gap','gap',
    'font-family','font-size','font-weight','line-height','letter-spacing','text-align',
    'color','background-color','border-top-width','border-right-width','border-bottom-width','border-left-width',
    'border-color','border-radius','box-shadow','overflow','object-fit','object-position','opacity',
    'align-items','justify-content','grid-template-columns','grid-template-rows'
  ];
  return [...document.querySelectorAll(sel)].map((el, index) => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    const visible = !!(r.width || r.height) && s.visibility !== 'hidden' && s.display !== 'none' && Number(s.opacity) !== 0;
    if (visibleOnly && !visible) return null;
    const style = Object.fromEntries(keys.map(k => [k, s.getPropertyValue(k)]));
    return {
      index,
      tag: el.tagName.toLowerCase(),
      id: el.id || null,
      classes: [...el.classList],
      role: el.getAttribute('role'),
      text: (el.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 220),
      rect: { x: r.x, y: r.y, width: r.width, height: r.height, right: r.right, bottom: r.bottom },
      visible,
      style,
    };
  }).filter(Boolean);
}, { sel: selector, visibleOnly });

fs.writeFileSync(out, JSON.stringify({ url, viewport: { width, height }, selector, elements: result }, null, 2));
console.log(`Wrote ${result.length} elements to ${out}`);
await browser.close();
