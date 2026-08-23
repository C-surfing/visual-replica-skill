#!/usr/bin/env node
import { chromium } from "playwright";
import fs from "node:fs";
import path from "node:path";

function arg(name, fallback = undefined) { const i = process.argv.indexOf(`--${name}`); return i >= 0 ? process.argv[i + 1] : fallback; }
function flag(name) { return process.argv.includes(`--${name}`); }
const url = arg("url");
if (!url) { console.error("Usage: capture.mjs --url http://localhost:3000 [--width 390 --height 844 --out candidate.png]"); process.exit(2); }
const out = arg("out", ".visual-replica/candidate.png");
const width = Number(arg("width", "390")); const height = Number(arg("height", "844")); const dpr = Number(arg("dpr", "1"));
const selector = arg("selector"); const waitMs = Number(arg("wait-ms", "250")); const fullPage = flag("full-page");
const maskSelectors = (arg("mask", "") || "").split(",").map(x => x.trim()).filter(Boolean);
fs.mkdirSync(path.dirname(out), { recursive: true });
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: dpr, reducedMotion: "reduce" });
const page = await context.newPage();
await page.goto(url, { waitUntil: "networkidle" });
await page.addStyleTag({content:`*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition-duration:0s!important;transition-delay:0s!important;caret-color:transparent!important;scroll-behavior:auto!important}`});
await page.evaluate(async () => {
  if (document.fonts?.ready) await document.fonts.ready;
  await Promise.all([...document.images].map(async img => { try { if (img.decode) await img.decode(); } catch {} }));
});
await page.waitForTimeout(waitMs);
const masks = maskSelectors.map(s => page.locator(s));
if (selector) await page.locator(selector).first().screenshot({ path: out, animations: "disabled", mask: masks });
else await page.screenshot({ path: out, fullPage, animations: "disabled", mask: masks });
console.log(JSON.stringify({status:"OK",url,out,viewport:{width,height,dpr},selector:selector??null,fullPage,masked:maskSelectors},null,2));
await browser.close();
