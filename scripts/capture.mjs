#!/usr/bin/env node
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

function arg(name, fallback = undefined) {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 ? process.argv[i + 1] : fallback;
}
function allArgs(name) {
  const out = [];
  for (let i = 0; i < process.argv.length; i++) {
    if (process.argv[i] === `--${name}` && process.argv[i + 1]) out.push(process.argv[i + 1]);
  }
  return out;
}
function flag(name) { return process.argv.includes(`--${name}`); }

const url = arg('url');
const out = arg('out', '.ui-replica/candidate/candidate.png');
const width = Number(arg('width', '390'));
const height = Number(arg('height', '844'));
const dpr = Number(arg('dpr', '1'));
const scale = arg('scale', 'css'); // css | device
const selector = arg('selector');
const readySelector = arg('ready-selector');
const waitMs = Number(arg('wait-ms', '250'));
const fullPage = flag('full-page');
const stabilizeCss = arg('stabilize-css');
const stateJson = arg('state-json');
const maskSelectors = allArgs('mask-selector');

if (!url) {
  console.error('Usage: node scripts/capture.mjs --url http://localhost:3000 --width 390 --height 844 [--dpr 1] [--scale css|device] [--out file.png]');
  process.exit(2);
}
if (!['css','device'].includes(scale)) {
  console.error('--scale must be css or device');
  process.exit(2);
}

fs.mkdirSync(path.dirname(out), { recursive: true });
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width, height },
  deviceScaleFactor: dpr,
  reducedMotion: 'reduce',
});
const page = await context.newPage();

await page.addInitScript(() => {
  // Stable time helps common dashboards; app code may still override this.
  const fixed = 1700000000000;
  Date.now = () => fixed;
});

await page.goto(url, { waitUntil: 'networkidle' });

const defaultCss = `
*,*::before,*::after {
  animation-duration: 0s !important;
  animation-delay: 0s !important;
  transition-duration: 0s !important;
  transition-delay: 0s !important;
  caret-color: transparent !important;
  scroll-behavior: auto !important;
}`;
await page.addStyleTag({ content: defaultCss });
if (stabilizeCss) {
  await page.addStyleTag({ content: fs.readFileSync(stabilizeCss, 'utf8') });
}

if (readySelector) await page.locator(readySelector).first().waitFor({ state: 'visible' });

await page.evaluate(async () => {
  if (document.fonts?.ready) await document.fonts.ready;
  await Promise.all([...document.images].map(async img => {
    try {
      if (!img.complete) {
        await new Promise(resolve => {
          img.addEventListener('load', resolve, { once: true });
          img.addEventListener('error', resolve, { once: true });
        });
      }
      if (img.decode) await img.decode().catch(() => {});
    } catch {}
  }));
});

if (stateJson) {
  const spec = JSON.parse(fs.readFileSync(stateJson, 'utf8'));
  for (const action of (spec.actions || [])) {
    const loc = action.selector ? page.locator(action.selector).first() : null;
    switch (action.type) {
      case 'click': await loc.click(); break;
      case 'hover': await loc.hover(); break;
      case 'focus': await loc.focus(); break;
      case 'fill': await loc.fill(action.value ?? ''); break;
      case 'press': await loc.press(action.key); break;
      case 'waitFor': await loc.waitFor({ state: action.state || 'visible' }); break;
      case 'wait': await page.waitForTimeout(Number(action.ms || 100)); break;
      case 'evaluate':
        throw new Error('Arbitrary evaluate actions are intentionally unsupported for safer deterministic capture.');
      default: throw new Error(`Unknown state action: ${action.type}`);
    }
  }
}

await page.waitForTimeout(waitMs);

const mask = maskSelectors.map(s => page.locator(s));
const shotOptions = { path: out, animations: 'disabled', scale, mask };
if (selector) {
  await page.locator(selector).first().screenshot(shotOptions);
} else {
  await page.screenshot({ ...shotOptions, fullPage });
}

console.log(JSON.stringify({
  ok: true,
  url,
  out,
  viewport: { width, height, dpr, scale },
  fullPage,
  selector: selector ?? null,
  readySelector: readySelector ?? null,
  masks: maskSelectors,
  stateJson: stateJson ?? null,
}, null, 2));

await browser.close();
