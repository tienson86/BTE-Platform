/**
 * UI Sprint 05 — Interpretation Document preview.
 * Run: node applications/customer_portal/tests/js/ui_sprint05_interpretation_preview_build.js
 */
const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");
const vm = require("vm");

const root = path.join(__dirname, "../..");
const outDir = path.join(
  root,
  "../../docs/reports/ui_sprint05_interpretation/preview"
);
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
  "report/interpretation_doc.js",
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
  bazi: { day_master: "Canh" },
  pattern: { dung_than: "Thủy", cach_cuc: "chinh_an" },
  score: { overall_score: 72, recommendations: ["Ưu tiên môi trường Thủy · Kim."] },
  interpretation: {
    confidence: 0.84,
    references: [{ label: "Tàng thư Ấn tinh", source: "classical" }],
    sections: [
      {
        id: "overview",
        body: "Lá số nghiêng về thân vượng với Ấn tinh hỗ trợ.\n\nNền tảng ổn định để đọc sâu các lĩnh vực đời sống.",
        callout: "Nền tảng ổn định — ưu tiên đọc Dụng thần Thủy.",
      },
      {
        id: "personality",
        body: "Tính cách thiên về kiên định, trọng chữ tín và có xu hướng tự chủ.",
      },
      {
        id: "career",
        body: "Hướng nghề Kim · Thủy phù hợp hơn môi trường Hỏa khắc.",
        citations: [{ label: "Thập thần Tỷ Kiên / Kiếp Tài trên trụ" }],
      },
      {
        id: "wealth",
        body: "Tài tinh cần bồi dưỡng qua môi trường hỗ trợ.",
      },
      {
        id: "marriage",
        body: "Quan hệ đôi lứa cần sự cân bằng và giao tiếp rõ ràng.",
      },
      {
        id: "health",
        body: "Chú ý nhịp nghỉ và cân bằng khí huyết theo ngũ hành.",
      },
      {
        id: "conclusion",
        body: "Giữ cân bằng Ngũ hành, ưu tiên dụng thần.\n\nHạn chế môi trường Hỏa quá mạnh.",
        callout: "Ưu tiên dụng thần Thủy trong quyết định gần.",
      },
      {
        id: "classical",
        body: "Cổ thư nhấn mạnh vai trò Ấn tinh trong cách cục Chính Ấn.",
        citations: [{ label: "Chính Ấn cách", book: "Tàng thư" }],
      },
    ],
  },
};

const model = sandbox.window.BteReportModel.build(data, { input });
const html = sandbox.window.BteReportRender.tiers.interpretation(model);

function page(theme) {
  return `<!doctype html><html lang="vi" data-theme="${theme}"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Sprint 05 Interpretation ${theme}</title>
<style>${css}
body{padding:1.25rem;background:var(--bg);color:var(--ink);}
.panel{max-width:980px;margin:0 auto;}
.preview-banner{margin:0 0 1rem;color:var(--muted);font-size:.9rem;}
.rpt-tier-head{margin-bottom:1rem;}
</style></head><body>
<div class="panel">
<p class="preview-banner">BTE UI Sprint 05 — Interpretation Document · theme=${theme}</p>
<h1>Kết quả phân tích</h1>
<div class="rpt-main">${html}</div>
</div>
<script>
${fs.readFileSync(path.join(root, "static/js/report/interpretation_doc.js"), "utf8")}
window.BteInterpretationDoc && BteInterpretationDoc.bind(document);
</script>
</body></html>`;
}

const assert = [];
if (!html.includes("InterpretationDocument")) assert.push("document");
if (!html.includes("TableOfContents")) assert.push("toc");
if (!html.includes("DocumentSection")) assert.push("section");
if (!html.includes("CalloutBox")) assert.push("callout");
if (html.includes('class="rpt-large-card"')) assert.push("uses_large_cards");
if (html.includes("null") || html.includes("undefined")) assert.push("nullish");
[
  "report.idoc_title",
  "report.toc",
  "report.ch_overview",
].forEach((k) => {
  if (html.includes(k)) assert.push("raw:" + k);
});
const doc = model.interpretation.document;
if (!doc || doc.chapters.length < 9) assert.push("chapter_count");
if (!doc.showToc) assert.push("show_toc");

const order = [
  "overview",
  "personality",
  "career",
  "wealth",
  "marriage",
  "health",
  "advice",
  "classical",
  "references",
];
order.forEach((id, i) => {
  if (!doc.chapters[i] || doc.chapters[i].id !== id) assert.push("order:" + id);
});

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, "interpretation_light.html"), page("light"), "utf8");
fs.writeFileSync(path.join(outDir, "interpretation_dark.html"), page("dark"), "utf8");
fs.writeFileSync(
  path.join(outDir, "index.html"),
  `<!doctype html><meta charset="utf-8"><title>Sprint 05</title>
  <h1>UI Sprint 05 — Interpretation Document</h1>
  <ul>
    <li><a href="interpretation_light.html">Light</a></li>
    <li><a href="interpretation_dark.html">Dark</a></li>
  </ul>
  <pre>${JSON.stringify(
    {
      chapters: doc.chapters.map((c) => ({ id: c.id, available: c.available })),
      assert_failures: assert,
    },
    null,
    2
  )}</pre>`,
  "utf8"
);

console.log("wrote", outDir);
console.log("assert_failures", assert);
console.log(pathToFileURL(path.join(outDir, "interpretation_light.html")).href);
if (assert.length) process.exitCode = 1;
