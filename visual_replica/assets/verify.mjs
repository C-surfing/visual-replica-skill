#!/usr/bin/env node
// State-aware verification adapter. Does not edit app code or approve a design.
import { chromium } from "playwright";
import fs from "node:fs";
import path from "node:path";

const [specFile, outputFile, screenshotFile] = process.argv.slice(2);
if (!specFile || !outputFile || !screenshotFile) {
  console.error("Usage: node verify.mjs scenario.json evidence.json screenshot.png");
  process.exit(2);
}
const spec = JSON.parse(fs.readFileSync(specFile, "utf8"));
fs.mkdirSync(path.dirname(outputFile), { recursive: true });
fs.mkdirSync(path.dirname(screenshotFile), { recursive: true });
const result = { status: "ERROR", scenario: spec.id, screenshot: null, assertions: [], dom: [], environment: {} };
let browser;
try {
  browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: spec.viewport.width, height: spec.viewport.height },
    deviceScaleFactor: spec.viewport.dpr ?? 1,
    reducedMotion: "reduce",
  });
  const page = await context.newPage();
  page.setDefaultTimeout(10000);
  await page.goto(spec.url, { waitUntil: "domcontentloaded", timeout: 30000 });
  if (spec.ready_selector) {
    await page.locator(spec.ready_selector).first().waitFor({ state: "visible" });
  }
  for (const action of spec.actions ?? []) {
    const loc = page.locator(action.selector).first();
    switch (action.type) {
      case "click": await loc.click(); break;
      case "fill": await loc.fill(action.value); break;
      case "press": await loc.press(action.value); break;
      case "check": await loc.check(); break;
      case "uncheck": await loc.uncheck(); break;
      case "wait_for": await loc.waitFor({ state: "visible" }); break;
      default: throw new Error("Unknown action: " + action.type);
    }
  }
  await page.addStyleTag({ content: "*,*::before,*::after{animation-duration:0s!important;transition-duration:0s!important;caret-color:transparent!important;scroll-behavior:auto!important}" });
  await page.evaluate(async () => {
    await document.fonts?.ready;
    await Promise.all([...document.images].map(i => i.decode?.().catch(() => {}) ?? Promise.resolve()));
  });

  for (const entry of spec.assertions ?? []) {
    const loc = page.locator(entry.selector).first();
    const visible = await loc.isVisible();
    let actual = visible;
    let passed = entry.condition === "visible" ? visible : !visible;
    if (entry.condition === "text_contains") {
      actual = await loc.count() ? await loc.textContent() : null;
      passed = typeof actual === "string" && actual.includes(entry.value);
    }
    result.assertions.push({
      selector: entry.selector, condition: entry.condition,
      expected: entry.value ?? null, actual, passed,
    });
  }
  for (const selector of spec.inspect_selectors ?? []) {
    const locator = page.locator(selector).first();
    if (!(await locator.count())) {
      result.dom.push({ selector, found: false });
      continue;
    }
    const bounds = await locator.boundingBox();
    const styles = await locator.evaluate(el => {
      const s = getComputedStyle(el);
      return {
        display: s.display, position: s.position, fontFamily: s.fontFamily,
        fontSize: s.fontSize, lineHeight: s.lineHeight, fontWeight: s.fontWeight,
        padding: s.padding, margin: s.margin, gap: s.gap, color: s.color,
        backgroundColor: s.backgroundColor, overflow: s.overflow,
      };
    });
    result.dom.push({ selector, found: true, bounds, styles });
  }
  result.environment = await page.evaluate(() => ({
    url: location.href, devicePixelRatio: devicePixelRatio,
    width: innerWidth, height: innerHeight,
    scrollWidth: document.documentElement.scrollWidth,
    fontsStatus: document.fonts?.status ?? "unknown",
  }));
  await page.screenshot({ path: screenshotFile, animations: "disabled" });
  result.screenshot = screenshotFile;
  result.status = result.assertions.some(a => !a.passed) ? "FAIL" : "PASS";
} catch (e) {
  result.error = String(e?.stack ?? e);
} finally {
  if (browser) await browser.close();
  fs.writeFileSync(outputFile, JSON.stringify(result, null, 2));
}
process.exit(result.status === "ERROR" ? 2 : 0);
