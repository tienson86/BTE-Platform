/**
 * UI Sprint 04 — Explainable Analysis preview.
 * Run: node applications/customer_portal/tests/js/ui_sprint04_analysis_preview_build.js
 */
const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");
const vm = require("vm");

const root = path.join(__dirname, "../..");
const outDir = path.join(root, "../../docs/reports/ui_sprint04_analysis/preview");
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

const sandbox = {
  window: {},
  BteI18n: {
    t(key, vars) {
      let text = deepGet(catalog, key);
      if (typeof text !== "string") return key;
      if (!vars) return text;
      return text.replace(/\{(\w+)\}/g, (_, n) =>
        vars[n] != null ? String(vars[n]) : `{${n}}`
      );
    },
  },
};
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
  "report/analysis.js",
  "report/report_model.js",
  "report/report_render.js",
].forEach((rel) => {
  vm.runInNewContext(
    fs.readFileSync(path.join(root, "static/js", rel), "utf8"),
    sandbox
  );
});

const input = { year: 1990, month: 5, day: 15, hour: 10, minute: 30, gender: "male" };
const data = {
  bazi: {
    day_master: "Canh",
    year_pillar: { stem: "Canh", branch: "Ngọ", ten_god: "Tỷ Kiên" },
    month_pillar: { stem: "Tân", branch: "Tỵ", ten_god: "Kiếp Tài" },
    day_pillar: { stem: "Canh", branch: "Thìn", ten_god: "Nhật Chủ" },
    hour_pillar: { stem: "Tân", branch: "Tỵ", ten_god: "Kiếp Tài" },
    shensha: [{ name: "Hoa Cái" }],
  },
  pattern: {
    than_vuong_nhuoc: "Thân vượng",
    dung_than: "Thủy",
    hy_than: "Mộc",
    ky_than: "Hỏa",
    cach_cuc: "chinh_an",
    hop: "Thân Tỵ hợp",
    rules: [
      {
        display_name: "Chính Ấn cách",
        priority: 1,
        reason: "Ấn tinh lộ can tháng/ngày.",
      },
    ],
    evidence: [{ label: "Can tháng Tân · Chi Tỵ", reference: "pattern.payload" }],
    confidence: 0.78,
  },
  score: { overall_score: 72, strength_score: 68 },
  interpretation: {
    confidence: 0.82,
    sections: [
      {
        id: "five_elements",
        body: "Kim · Thổ chiếm ưu thế trên trụ.",
      },
      { id: "pattern", body: "Cách cục nghiêng Chính Ấn." },
    ],
  },
  knowledge_expert: {
    status: "ready",
    citation: "Tàng thư Ấn tinh",
  },
};

const model = sandbox.window.BteReportModel.build(data, { input });
const html = sandbox.window.BteReportRender.tiers.analysis(model);

function page(theme) {
  return `<!doctype html><html lang="vi" data-theme="${theme}"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Sprint 04 Analysis ${theme}</title>
<style>${css}
body{padding:1.25rem;background:var(--bg);color:var(--ink);}
.panel{max-width:960px;margin:0 auto;}
.preview-banner{margin:0 0 1rem;color:var(--muted);font-size:.9rem;}
</style></head><body>
<div class="panel">
<p class="preview-banner">BTE UI Sprint 04 — Explainable Analysis · theme=${theme}</p>
<h1>Kết quả phân tích</h1>
<div class="rpt-main">${html}</div>
</div>
<script>
${fs.readFileSync(path.join(root, "static/js/report/analysis.js"), "utf8")}
document.querySelectorAll && window.BteAnalysis && BteAnalysis.bind(document);
</script>
</body></html>`;
}

const assert = [];
if (!html.includes("AnalysisWorkspace")) assert.push("workspace");
if (!html.includes("AnalysisBlock")) assert.push("block");
if (!html.includes("RulePanel")) assert.push("rules");
if (!html.includes("EvidencePanel")) assert.push("evidence");
if (!html.includes("ConfidenceIndicator")) assert.push("confidence");
if (!html.includes("KnowledgeReference")) assert.push("knowledge");
const orderKeys = [
  "an_conclusion",
  "an_summary",
  "an_factors",
  "an_rules",
  "an_evidence",
  "an_confidence",
];
/* Structure order inside first block via Vietnamese labels */
const labels = [
  catalog.report.an_conclusion,
  catalog.report.an_summary,
  catalog.report.an_factors,
  catalog.report.an_rules,
  catalog.report.an_evidence,
  catalog.report.an_confidence,
];
let prev = -1;
labels.forEach((lab) => {
  const idx = html.indexOf(lab);
  if (idx < 0) assert.push("missing:" + lab);
  else if (idx < prev) assert.push("order:" + lab);
  if (idx >= 0) prev = idx;
});
if (html.includes("null") || html.includes("undefined")) assert.push("nullish");
[
  "report.an_conclusion",
  "report.an_workspace_hint",
].forEach((k) => {
  if (html.includes(k)) assert.push("raw:" + k);
});
if (!(model.analysis.blocks && model.analysis.blocks.length >= 10)) {
  assert.push("blocks_count");
}

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, "analysis_light.html"), page("light"), "utf8");
fs.writeFileSync(path.join(outDir, "analysis_dark.html"), page("dark"), "utf8");
fs.writeFileSync(
  path.join(outDir, "index.html"),
  `<!doctype html><meta charset="utf-8"><title>Sprint 04</title>
  <h1>UI Sprint 04 — Analysis</h1>
  <ul><li><a href="analysis_light.html">Light</a></li><li><a href="analysis_dark.html">Dark</a></li></ul>
  <pre>${JSON.stringify(
    { block_ids: model.analysis.blocks.map((b) => b.id), assert_failures: assert },
    null,
    2
  )}</pre>`,
  "utf8"
);

console.log("wrote", outDir);
console.log("assert_failures", assert);
console.log(pathToFileURL(path.join(outDir, "analysis_light.html")).href);
if (assert.length) process.exitCode = 1;
