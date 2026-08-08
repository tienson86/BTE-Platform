/**
 * Capture Release C Result Page review screenshots.
 * Expects Vite harness on http://127.0.0.1:5179 (vite.result-page-screenshots.config.ts).
 */

import { chromium } from "playwright";
import path from "node:path";
import fs from "node:fs";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const outDir = path.resolve(
  __dirname,
  "../../../knowledge/releases/v1/visual/release_c_review",
);
const url = "http://127.0.0.1:5179/result-page-screenshots.html";

const VIEWPORTS = [
  { name: "desktop_full", width: 1440, height: 900, fullOnly: true },
  { name: "laptop", width: 1280, height: 800, fullOnly: true },
  { name: "tablet", width: 1024, height: 768, fullOnly: true },
  { name: "mobile", width: 390, height: 844, fullOnly: true },
];

const ZONE_SHOTS = [
  { selector: '[data-pattern="LP-001"]', file: "Executive Summary.png" },
  { selector: '[data-pattern="LP-005"]', file: "Recommendation.png" },
  { selector: '[data-pattern="LP-006"]', file: "Interpretation.png" },
  { selector: '[data-pattern="LP-007"]', file: "Knowledge.png" },
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
    await page.waitForTimeout(500);

    const overflowX = await page.evaluate(() => {
      return document.documentElement.scrollWidth > document.documentElement.clientWidth;
    });
    manifest.push({
      viewport: vp.name,
      pattern: "OVERFLOW_X",
      horizontalScroll: overflowX,
      size: `${vp.width}x${vp.height}`,
    });

    const fullPath = path.join(outDir, `${vp.name}.png`);
    await page.screenshot({ path: fullPath, fullPage: true });
    manifest.push({ viewport: vp.name, pattern: "FULL", file: path.basename(fullPath) });
    console.log(`Wrote ${path.basename(fullPath)} (overflowX=${overflowX})`);

    if (vp.name === "desktop_full") {
      for (const zone of ZONE_SHOTS) {
        const el = page.locator(zone.selector).first();
        await el.scrollIntoViewIfNeeded();
        await page.waitForTimeout(200);
        const filePath = path.join(outDir, zone.file);
        await el.screenshot({ path: filePath });
        manifest.push({
          viewport: vp.name,
          pattern: zone.file,
          file: zone.file,
        });
        console.log(`Wrote ${zone.file}`);
      }
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
