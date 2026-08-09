/**
 * Capture Result Page V2 screenshots (expects vite on :5180).
 * Viewports: Desktop 1440 · Tablet 1024 · Mobile 390.
 */

import { chromium } from "playwright";
import path from "node:path";
import fs from "node:fs";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const outDir = path.resolve(__dirname, "../artifacts/px4_screenshots/after");
const url = "http://127.0.0.1:5180/result-v2-screenshots.html";

const VIEWPORTS = [
  { name: "desktop_1440", width: 1440, height: 900 },
  { name: "tablet_1024", width: 1024, height: 768 },
  { name: "mobile_390", width: 390, height: 844 },
];

const ZONES = [
  { id: "Hero", selector: "#rv2-Hero", file: "hero" },
  { id: "Summary", selector: "#rv2-Summary", file: "summary" },
  { id: "Recommendation", selector: "#rv2-Recommendation", file: "recommendation" },
  { id: "DomainCareer", selector: "#rv2-DomainCareer", file: "domain" },
  { id: "Technical", selector: "#rv2-Technical", file: "technical" },
  { id: "Knowledge", selector: "#rv2-Knowledge", file: "knowledge" },
  { id: "Footer", selector: ".rv2-footer", file: "footer" },
];

fs.mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch({
  headless: true,
  channel: "chrome",
});
const manifest = [];

try {
  for (const vp of VIEWPORTS) {
    const page = await browser.newPage({
      viewport: { width: vp.width, height: vp.height },
      deviceScaleFactor: 1,
    });
    await page.goto(url, { waitUntil: "networkidle", timeout: 90000 });
    await page.waitForSelector("#rv2-Hero", { timeout: 60000 });
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
