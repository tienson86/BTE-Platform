import { chromium } from "playwright";
import path from "node:path";
import fs from "node:fs";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const outDir = path.resolve(__dirname, "../artifacts/px5_screenshots/after");
const url = "http://127.0.0.1:5181/portal-screenshots.html";

const VIEWPORTS = [
  { name: "desktop_1440", width: 1440, height: 900 },
  { name: "tablet_1024", width: 1024, height: 768 },
  { name: "mobile_390", width: 390, height: 844 },
];

const SCREENS = [
  { hash: "#/home", file: "home" },
  { hash: "#/dashboard", file: "dashboard" },
  { hash: "#/analyze", file: "analyze" },
  { hash: "#/analyze/birth", file: "birth" },
  { hash: "#/analyze/chart", file: "chart_input" },
  { hash: "#/analyze/progress", file: "progress" },
  { hash: "#/results", file: "result_list" },
  { hash: "#/result", file: "result_viewer" },
  { hash: "#/knowledge", file: "knowledge" },
  { hash: "#/profile", file: "profile" },
  { hash: "#/history", file: "history" },
  { hash: "#/settings", file: "settings" },
  { hash: "#/help", file: "help" },
  { hash: "#/about", file: "about" },
  { hash: "#/404", file: "notfound" },
  { hash: "#/error", file: "error" },
  { hash: "#/loading", file: "loading" },
  { hash: "#/empty", file: "empty" },
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
      if (screen.file === "result_viewer") {
        await page.waitForSelector("#rv2-Hero", { timeout: 20000 });
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
