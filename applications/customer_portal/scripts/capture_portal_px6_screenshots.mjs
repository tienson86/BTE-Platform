import { chromium } from "playwright";
import path from "node:path";
import fs from "node:fs";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const outDir = path.resolve(__dirname, "../artifacts/px6_screenshots/after");
const url = "http://127.0.0.1:5181/portal-screenshots.html";

const VIEWPORTS = [
  { name: "desktop_1440", width: 1440, height: 900 },
  { name: "tablet_1024", width: 1024, height: 768 },
  { name: "mobile_390", width: 390, height: 844 },
];

const SCREENS = [
  { hash: "#/home", file: "01_landing" },
  { hash: "#/onboarding", file: "02_onboarding" },
  { hash: "#/analyze", file: "03_create" },
  { hash: "#/analyze/progress", file: "04_progress" },
  { hash: "#/result", file: "05_result" },
  { hash: "#/knowledge/article", file: "06_knowledge" },
  { hash: "#/complete", file: "07_saved" },
  { hash: "#/history", file: "08_history" },
  { hash: "#/dashboard", file: "09_return" },
  { hash: "#/premium", file: "10_premium" },
  { hash: "#/empty", file: "11_empty" },
  { hash: "#/error", file: "12_error" },
];

fs.mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch({ headless: true, channel: "chrome" });
const manifest = [];

try {
  for (const vp of VIEWPORTS) {
    const page = await browser.newPage({ viewport: { width: vp.width, height: vp.height }, deviceScaleFactor: 1 });
    await page.goto(url, { waitUntil: "networkidle", timeout: 90000 });
    await page.waitForSelector("[data-portal='px5']", { timeout: 60000 });
    const overflowX = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
    manifest.push({ viewport: vp.name, pattern: "OVERFLOW_X", horizontalScroll: overflowX });

    for (const screen of SCREENS) {
      await page.evaluate((hash) => {
        window.location.hash = hash;
      }, screen.hash);
      if (screen.file === "05_result") {
        await page.waitForSelector("#rv2-Hero", { timeout: 20000 });
        await page.waitForSelector(".pv-commercial", { timeout: 10000 });
      }
      await page.waitForTimeout(400);
      const filePath = path.join(outDir, `${screen.file}_${vp.name}.png`);
      await page.screenshot({ path: filePath, fullPage: true });
      manifest.push({ viewport: vp.name, screen: screen.file, file: path.basename(filePath) });
      console.log(`Wrote ${path.basename(filePath)}`);
    }
    await page.close();
  }
} finally {
  await browser.close();
}

fs.writeFileSync(path.join(outDir, "manifest.json"), JSON.stringify({ generatedAt: new Date().toISOString(), items: manifest }, null, 2));
console.log(`Done. Output: ${outDir}`);
