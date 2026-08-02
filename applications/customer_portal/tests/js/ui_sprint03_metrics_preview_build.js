/**
 * UI Sprint 03 — Metrics Workspace preview.
 * Run: node applications/customer_portal/tests/js/ui_sprint03_metrics_preview_build.js
 */
const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");
const vm = require("vm");

const root = path.join(__dirname, "../..");
const outDir = path.join(root, "../../docs/reports/ui_sprint03_metrics/preview");
const css = [
  "tokens.css",
  "base.css",
  "components.css",
  "layout.css",
  "pages.css",
  "domain.css",
  "report.css",
]
  .map((n) => fs.readFileSync(path.join(root, "static/css", n), "utf8"))
  .join("\n");

const catalog = JSON.parse(
  fs.readFileSync(path.join(root, "static/i18n/vi.json"), "utf8")
);

function deepGet(obj, key) {
  return String(key)
    .split(".")
    .reduce(
      (node, p) => (node && typeof node === "object" ? node[p] : undefined),
      obj
    );
}

const sandbox = { window: {}, BteI18n: {
  t(key, vars) {
    let text = deepGet(catalog, key);
    if (typeof text !== "string") return key;
    if (!vars) return text;
    return text.replace(/\{(\w+)\}/g, (_, n) =>
      vars[n] != null ? String(vars[n]) : `{${n}}`
    );
  },
}};
sandbox.global = sandbox.window;
sandbox.window.BteI18n = sandbox.BteI18n;

[
  "ui/components.js",
  "presenters/summary_builder.js",
  "presenters/narrative.js",
  "presenters/discussion.js",
  "presenters/interpretation.js",
  "report/icons.js",
  "report/charts.js",
  "report/pillars.js",
  "report/metrics.js",
  "report/report_model.js",
  "report/report_render.js",
].forEach((rel) => {
  vm.runInNewContext(fs.readFileSync(path.join(root, "static/js", rel), "utf8"), sandbox);
});

const input = { year: 1990, month: 5, day: 15, hour: 10, minute: 30, gender: "male" };
const data = {
  bazi: {
    day_master: "Canh",
    year_pillar: { stem: "Canh", branch: "Ngọ", ten_god: "Tỷ Kiên" },
    month_pillar: { stem: "Tân", branch: "Tỵ", ten_god: "Kiếp Tài" },
    day_pillar: { stem: "Canh", branch: "Thìn", ten_god: "Nhật Chủ" },
    hour_pillar: { stem: "Tân", branch: "Tỵ", ten_god: "Kiếp Tài" },
  },
  pattern: { than_vuong_nhuoc: "Thân vượng", dung_than: "Thủy", cach_cuc: "chinh_an" },
  score: {
    overall_score: 72,
    strength_score: 68,
    wuxing_score: 61,
    strengths: ["Ấn hỗ trợ"],
    recommendations: ["Ưu tiên Thủy · Kim."],
  },
  interpretation: {
    confidence: 0.8,
    sections: [
      {
        id: "five_elements",
        body: "Ngũ hành nghiêng Kim · Thổ; Thủy cần được nuôi dưỡng.",
      },
      {
        id: "ten_gods",
        body: "Tỷ Kiên và Kiếp Tài xuất hiện rõ trên trụ.",
      },
    ],
  },
};

const model = sandbox.window.BteReportModel.build(data, { input });
const html = sandbox.window.BteReportRender.tiers.charts(model);

function page(theme) {
  return `<!doctype html><html lang="vi" data-theme="${theme}"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Sprint 03 Metrics ${theme}</title>
<style>${css}
body{padding:1.25rem;background:var(--bg);color:var(--ink);}
.panel{max-width:1100px;margin:0 auto;}
.preview-banner{margin:0 0 1rem;color:var(--muted);font-size:.9rem;}
</style></head><body>
<div class="panel">
<p class="preview-banner">BTE UI Sprint 03 — Metrics & Visual Analytics · theme=${theme}</p>
<h1>Kết quả phân tích</h1>
<div class="rpt-main">${html}</div>
</div></body></html>`;
}

const assert = [];
if (!html.includes("MetricsWorkspace")) assert.push("workspace");
if (!html.includes("SummaryMetricGrid")) assert.push("metrics");
if (!html.includes("StrengthGauge")) assert.push("gauge");
if (!html.includes("ElementDistribution")) assert.push("elements");
if (!html.includes("TenGodDistribution")) assert.push("gods");
const order = [
  html.indexOf("SummaryMetricGrid"),
  html.indexOf("StrengthGauge"),
  html.indexOf("ElementDistribution"),
  html.indexOf("TenGodDistribution"),
];
for (let i = 1; i < order.length; i++) {
  if (order[i] < order[i - 1]) assert.push("order");
}
if (html.includes("Đại Vận") || html.includes("Lưu Niên")) assert.push("luck_invented");
[
  "report.chart_metrics_title",
  "report.chart_gauge_desc",
  "report.chart_workspace_hint",
].forEach((k) => {
  if (html.includes(k)) assert.push("raw:" + k);
});
if (html.includes("null") || html.includes("undefined")) assert.push("nullish");
if (!(model.charts.insights && model.charts.insights.elements)) {
  assert.push("insight_elements");
}

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, "metrics_light.html"), page("light"), "utf8");
fs.writeFileSync(path.join(outDir, "metrics_dark.html"), page("dark"), "utf8");
fs.writeFileSync(
  path.join(outDir, "index.html"),
  `<!doctype html><meta charset="utf-8"><title>Sprint 03</title>
  <h1>UI Sprint 03 — Metrics</h1>
  <ul><li><a href="metrics_light.html">Light</a></li><li><a href="metrics_dark.html">Dark</a></li></ul>
  <pre>${JSON.stringify({ charts: model.charts, assert_failures: assert }, null, 2)}</pre>`,
  "utf8"
);

console.log("wrote", outDir);
console.log("assert_failures", assert);
console.log(pathToFileURL(path.join(outDir, "metrics_light.html")).href);
if (assert.length) process.exitCode = 1;
