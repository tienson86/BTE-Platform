/**
 * Capture Result Page LP screenshots (expects vite on :5179).
 * Viewports: Desktop 1440 · Laptop 1280 · Tablet 1024 · Tablet Portrait 768 · Mobile 390.
 */

import { chromium } from "playwright";
import path from "node:path";
import fs from "node:fs";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const outDir = path.resolve(
  __dirname,
  "../../../knowledge/ui_reference/visual/visual_v2_screenshots/after",
);
const url = "http://127.0.0.1:5179/result-page-screenshots.html";

const VIEWPORTS = [
  { name: "desktop", width: 1440, height: 900 },
  { name: "laptop", width: 1280, height: 800 },
  { name: "tablet", width: 1024, height: 768 },
  { name: "tablet_portrait", width: 768, height: 1024 },
  { name: "mobile", width: 390, height: 844 },
];

const ZONES = [
  { id: "LP-001", selector: '[data-pattern="LP-001"]', file: "lp001_summary" },
  { id: "LP-003", selector: '[data-pattern="LP-003"]', file: "lp003_analysis" },
  { id: "LP-004", selector: '[data-pattern="LP-004"]', file: "lp004_visualization" },
  { id: "LP-005", selector: '[data-pattern="LP-005"]', file: "lp005_recommendation" },
  { id: "LP-006", selector: '[data-pattern="LP-006"]', file: "lp006_interpretation" },
  { id: "LP-007", selector: '[data-pattern="LP-007"]', file: "lp007_knowledge" },
];

fs.mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch({ headless: true });
const manifest = [];

try {
  for (const vp of VIEWPORTS) {
    const page = await browser.newPage({
      viewport: { width: vp.width, height: vp.height },
      deviceScaleFactor: 1,
    });
    await page.goto(url, { waitUntil: "networkidle", timeout: 90000 });
    await page.waitForSelector('[data-pattern="LP-001"]', { timeout: 60000 });
    await page.waitForTimeout(400);

    const overflowX = await page.evaluate(() => {
      const el = document.documentElement;
      return el.scrollWidth > el.clientWidth;
    });
    manifest.push({
      viewport: vp.name,
      pattern: "OVERFLOW_X",
      horizontalScroll: overflowX,
      size: `${vp.width}x${vp.height}`,
    });

    const fullPath = path.join(outDir, `full_${vp.name}.png`);
    await page.screenshot({ path: fullPath, fullPage: true });
    manifest.push({ viewport: vp.name, pattern: "FULL", file: path.basename(fullPath) });

    for (const zone of ZONES) {
      const el = page.locator(zone.selector).first();
      await el.scrollIntoViewIfNeeded();
      await page.waitForTimeout(150);
      const filePath = path.join(outDir, `${zone.file}_${vp.name}.png`);
      await el.screenshot({ path: filePath });
      manifest.push({
        viewport: vp.name,
        pattern: zone.id,
        file: path.basename(filePath),
        size: `${vp.width}x${vp.height}`,
      });
      console.log(`Wrote ${path.basename(filePath)}`);
    }
    await page.close();
  }
} finally {
  await browser.close();
}

fs.writeFileSync(
  path.join(outDir, "manifest.json"),
  JSON.stringify({ generatedAt: new Date().toISOString(), items: manifest }, null, 2),
);
console.log(`Done. Output: ${outDir}`);
