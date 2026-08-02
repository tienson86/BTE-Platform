/**
 * UI Sprint 07 — Full Result Experience preview (integration polish).
 * Run: node applications/customer_portal/tests/js/ui_sprint07_result_preview_build.js
 */
const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");
const vm = require("vm");

const root = path.join(__dirname, "../..");
const outDir = path.join(
  root,
  "../../docs/reports/ui_production_readiness/preview"
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
  document: { readyState: "complete" },
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
  "report/knowledge_workspace.js",
  "report/report_model.js",
  "report/report_render.js",
  "ui/scroll_spy.js",
].forEach((rel) => {
  vm.runInNewContext(
    fs.readFileSync(path.join(root, "static/js", rel), "utf8"),
    sandbox
  );
});

const input = {
  year: 1990,
  month: 5,
  day: 15,
  hour: 10,
  minute: 30,
  gender: "male",
};

const data = {
  bazi: {
    day_master: "Canh",
    pillars: {
      year: { stem: "Canh", branch: "Ngọ", hidden: ["Giáp"], ten_god: "Kiếp Tài" },
      month: { stem: "Tân", branch: "Tỵ", hidden: ["Bính"], ten_god: "Chính Ấn" },
      day: { stem: "Canh", branch: "Thìn", hidden: ["Ất"], ten_god: "Nhật Chủ" },
      hour: { stem: "Ất", branch: "Tỵ", hidden: ["Canh"], ten_god: "Thương Quan" },
    },
  },
  pattern: {
    dung_than: "Thủy",
    hy_than: "Kim",
    ky_than: "Hỏa",
    cach_cuc: "Chính Ấn",
    than_strength: "Thân vượng",
    rules: [
      {
        display_name: "Ấn tinh sinh thân",
        category: "Cách cục",
        priority: 1,
        description: "Ấn tinh hiện rõ và sinh thân nhật chủ.",
      },
    ],
    evidence: [
      {
        label: "Tháng trụ thấy Ấn",
        reason: "Can tháng hỗ trợ nhật chủ",
        condition: "Thân vượng",
        source_type: "rule",
      },
    ],
    classical: [
      {
        book: "Tàng thư",
        chapter: "Ấn tinh",
        section: "Chính Ấn",
        quote: "Ấn tinh sinh thân, chủ học vấn.",
      },
    ],
    confidence: 0.81,
    related_sections: [
      { type: "analysis", id: "pattern", label: "Cách cục" },
      { type: "interpretation", id: "classical", label: "Cổ thư" },
    ],
  },
  score: {
    overall_score: 72,
    recommendations: ["Ưu tiên môi trường Thủy · Kim."],
    strengths: ["Ấn tinh vững", "Nhật chủ có gốc"],
    weaknesses: ["Hỏa quá mạnh có thể khắc Kim"],
    wuxing_series: [
      { label: "Mộc", value: 12 },
      { label: "Hỏa", value: 28 },
      { label: "Thổ", value: 18 },
      { label: "Kim", value: 22 },
      { label: "Thủy", value: 20 },
    ],
  },
  knowledge_expert: { status: "ready", message: "Knowledge layer sẵn sàng." },
  knowledge_blocks: [
    {
      id: "kb-useful",
      insight: "Ưu tiên dụng thần Thủy trong quyết định gần.",
      description: "Dụng thần từ cấu trúc ngũ hành và cách cục.",
      evidence: [
        {
          label: "Dụng thần = Thủy",
          reason: "Thủy sinh Kim và điều hòa Hỏa",
          condition: "Thân vượng cần tiết / sinh",
          source_type: "reasoning",
        },
      ],
      rules: [
        {
          name: "Dụng thần ưu tiên",
          category: "Useful God",
          priority: 2,
          description: "Thân vượng: dụng thần thiên về tiết khí hoặc tài quan cân bằng.",
        },
      ],
      knowledge_reference: "Knowledge base · Useful God matrix",
      classical: [
        {
          book: "Địch Thiên Tủy",
          chapter: "Dụng thần",
          section: "Thân vượng",
          quote: "Thân vượng dụng tiết, tài quan.",
        },
      ],
      confidence: "cao",
      related_sections: [
        { type: "analysis", id: "useful", label: "Dụng · Hỷ · Kỵ" },
        { type: "interpretation", id: "advice", label: "Khuyến nghị" },
      ],
    },
  ],
  interpretation: {
    confidence: 0.84,
    references: [{ label: "Tàng thư Ấn tinh", source: "classical" }],
    sections: [
      {
        id: "overview",
        body: "Lá số nghiêng về thân vượng với Ấn tinh hỗ trợ.\n\nNền tảng ổn định để đọc sâu.",
        callout: "Ưu tiên đọc Dụng thần Thủy trước.",
      },
      { id: "personality", body: "Tính cách kiên định, trọng chữ tín." },
      { id: "career", body: "Hướng nghề Kim · Thủy phù hợp hơn Hỏa khắc." },
      { id: "wealth", body: "Tài tinh cần bồi dưỡng qua môi trường hỗ trợ." },
      { id: "marriage", body: "Quan hệ cần cân bằng và giao tiếp rõ." },
      { id: "health", body: "Chú ý nhịp nghỉ theo ngũ hành." },
      {
        id: "conclusion",
        body: "Giữ cân bằng Ngũ hành, ưu tiên dụng thần.",
        callout: "Ưu tiên dụng thần Thủy trong quyết định gần.",
      },
      {
        id: "classical",
        body: "Cổ thư nhấn mạnh vai trò Ấn tinh trong Chính Ấn.",
        citations: [{ label: "Chính Ấn cách", book: "Tàng thư" }],
      },
    ],
  },
};

const model = sandbox.window.BteReportModel.build(data, { input });
const html = sandbox.window.BteReportRender.render(model);

const assert = [];
[
  "tier-executive",
  "tier-bazi",
  "tier-charts",
  "tier-analysis",
  "tier-interpretation",
  "tier-knowledge",
].forEach((id) => {
  if (!html.includes('id="' + id + '"')) assert.push("missing:" + id);
});
if (!html.includes("FourPillarsWorkspace") && !html.includes("fp-workspace")) {
  assert.push("pillars");
}
if (!html.includes("KnowledgeWorkspace")) assert.push("knowledge");
if (!html.includes("InterpretationDocument")) assert.push("interpretation");
if (html.includes("report.kw_evidence")) assert.push("raw:kw_evidence");
if (html.includes("report.collapse_section")) assert.push("raw:collapse");
if (/\bundefined\b/.test(html) || /\bnull\b/.test(html)) assert.push("nullish");

function page(theme) {
  return `<!doctype html><html lang="vi" data-theme="${theme}"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Sprint 07 Result ${theme}</title>
<style>${css}
body{padding:1.25rem;background:var(--bg);color:var(--ink);}
.panel{max-width:1280px;margin:0 auto;}
.preview-banner{margin:0 0 1rem;color:var(--muted);font-size:.9rem;}
</style></head><body>
<div class="panel result-report-page">
<p class="preview-banner">BTE UI Sprint 07 — Full Result Experience · theme=${theme}</p>
<h1>Kết quả phân tích</h1>
<div id="reportHost">${html}</div>
</div>
<script>
${fs.readFileSync(path.join(root, "static/js/report/pillars.js"), "utf8")}
${fs.readFileSync(path.join(root, "static/js/report/analysis.js"), "utf8")}
${fs.readFileSync(path.join(root, "static/js/report/interpretation_doc.js"), "utf8")}
${fs.readFileSync(path.join(root, "static/js/report/knowledge_workspace.js"), "utf8")}
${fs.readFileSync(path.join(root, "static/js/ui/scroll_spy.js"), "utf8")}
(function(){
  var host = document.getElementById("reportHost");
  var model = ${JSON.stringify({
    knowledge: model.knowledge,
    analysis: { blocks: (model.analysis && model.analysis.blocks) || [] },
  })};
  if (window.BtePillars) BtePillars.bind(host);
  if (window.BteAnalysis) BteAnalysis.bind(host);
  if (window.BteInterpretationDoc) BteInterpretationDoc.bind(host);
  if (window.BteKnowledge) BteKnowledge.bind(host, model);
  if (window.BteScrollSpy) BteScrollSpy.bind(host);
})();
</script>
</body></html>`;
}

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, "result_light.html"), page("light"), "utf8");
fs.writeFileSync(path.join(outDir, "result_dark.html"), page("dark"), "utf8");
fs.writeFileSync(
  path.join(outDir, "index.html"),
  `<!doctype html><meta charset="utf-8"><title>Sprint 07</title>
  <h1>UI Sprint 07 — Production Readiness Preview</h1>
  <ul>
    <li><a href="result_light.html">Full Result · Light</a></li>
    <li><a href="result_dark.html">Full Result · Dark</a></li>
  </ul>
  <pre>${JSON.stringify({ assert_failures: assert }, null, 2)}</pre>`,
  "utf8"
);

console.log("wrote", outDir);
console.log("assert_failures", assert);
console.log(pathToFileURL(path.join(outDir, "result_light.html")).href);
if (assert.length) process.exitCode = 1;
