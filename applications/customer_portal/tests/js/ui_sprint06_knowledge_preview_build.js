/**
 * UI Sprint 06 — Knowledge & Evidence Workspace preview.
 * Run: node applications/customer_portal/tests/js/ui_sprint06_knowledge_preview_build.js
 */
const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");
const vm = require("vm");

const root = path.join(__dirname, "../..");
const outDir = path.join(
  root,
  "../../docs/reports/ui_sprint06_knowledge/preview"
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
  "report/knowledge_workspace.js",
  "report/report_model.js",
  "report/report_render.js",
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
  bazi: { day_master: "Canh" },
  pattern: {
    dung_than: "Thủy",
    cach_cuc: "Chính Ấn",
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
        passage: "1",
        quote: "Ấn tinh sinh thân, chủ học vấn và danh tiếng.",
      },
    ],
    confidence: 0.81,
    related_sections: [
      { type: "analysis", id: "pattern", label: "Cách cục" },
      { type: "interpretation", id: "classical", label: "Cổ thư" },
    ],
  },
  score: { overall_score: 72 },
  knowledge_expert: { status: "ready", message: "Knowledge layer sẵn sàng truy vết." },
  knowledge_blocks: [
    {
      id: "kb-useful",
      insight: "Ưu tiên dụng thần Thủy trong quyết định gần.",
      description: "Dụng thần được xác định từ cấu trúc ngũ hành và cách cục.",
      evidence: [
        {
          label: "Dụng thần = Thủy",
          reason: "Thủy sinh Kim và điều hòa Hỏa",
          condition: "Thân vượng cần tiết / sinh",
          source_type: "reasoning",
          reference: "overview.dung_than",
        },
      ],
      rules: [
        {
          name: "Dụng thần ưu tiên",
          category: "Useful God",
          priority: 2,
          description: "Khi thân vượng, dụng thần thiên về tiết khí hoặc tài quan cân bằng.",
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
    sections: [{ id: "overview", body: "Tóm tắt ngắn." }],
  },
};

const model = sandbox.window.BteReportModel.build(data, { input });
const html = sandbox.window.BteReportRender.tiers.knowledge(model);

function page(theme) {
  return `<!doctype html><html lang="vi" data-theme="${theme}"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Sprint 06 Knowledge ${theme}</title>
<style>${css}
body{padding:1.25rem;background:var(--bg);color:var(--ink);}
.panel{max-width:980px;margin:0 auto;}
.preview-banner{margin:0 0 1rem;color:var(--muted);font-size:.9rem;}
.rpt-tier-head{margin-bottom:1rem;}
.rpt-large-card{margin-top:1.5rem;}
</style></head><body>
<div class="panel">
<p class="preview-banner">BTE UI Sprint 06 — Knowledge & Evidence Workspace · theme=${theme}</p>
<h1>Kết quả phân tích</h1>
<div class="rpt-main" id="host">${html}</div>
</div>
<script>
${fs.readFileSync(path.join(root, "static/js/report/knowledge_workspace.js"), "utf8")}
window.__rptModel = ${JSON.stringify({ knowledge: model.knowledge })};
window.BteKnowledge && BteKnowledge.bind(document.getElementById("host"), window.__rptModel);
</script>
</body></html>`;
}

const assert = [];
if (!html.includes("KnowledgeWorkspace")) assert.push("workspace");
if (!html.includes("KnowledgeBlock")) assert.push("block");
if (!html.includes("EvidencePanel")) assert.push("evidence");
if (!html.includes("RuleReference")) assert.push("rule");
if (!html.includes("ClassicalReference")) assert.push("classical");
if (!html.includes("ConfidencePanel")) assert.push("confidence");
if (!html.includes("RelatedSectionLinks")) assert.push("related");
if (!html.includes("CitationToolbar")) assert.push("toolbar");
if (html.includes("EngineInternal") || /FPR\d{3,}/.test(html)) {
  assert.push("engine_leak");
}
[
  "report.kw_insight",
  "report.kw_evidence",
  "report.kw_workspace_hint",
].forEach((k) => {
  if (html.includes(k)) assert.push("raw:" + k);
});

const blocks = model.knowledge.blocks || [];
if (!blocks.length) assert.push("no_blocks");

const orderMarks = [
  "kw_insight",
  "EvidencePanel",
  "RuleReference",
  "KnowledgeReference",
  "ClassicalReference",
  "ConfidencePanel",
  "RelatedSectionLinks",
];
const firstBlock = html.indexOf("KnowledgeBlock");
orderMarks.forEach((mark, i) => {
  if (i === 0) return;
  const prev = orderMarks[i - 1];
  const a = html.indexOf(prev === "kw_insight" ? "report.kw_insight" : prev, firstBlock);
  /* titles are translated — check component markers */
});
const markers = [
  'data-component="EvidencePanel"',
  'data-component="RuleReference"',
  'data-component="KnowledgeReference"',
  'data-component="ClassicalReference"',
  'data-component="ConfidencePanel"',
  'data-component="RelatedSectionLinks"',
];
let cursor = firstBlock;
markers.forEach((m) => {
  const at = html.indexOf(m, cursor);
  if (at < 0 || at < cursor) assert.push("order:" + m);
  else cursor = at;
});

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, "knowledge_light.html"), page("light"), "utf8");
fs.writeFileSync(path.join(outDir, "knowledge_dark.html"), page("dark"), "utf8");
fs.writeFileSync(
  path.join(outDir, "index.html"),
  `<!doctype html><meta charset="utf-8"><title>Sprint 06</title>
  <h1>UI Sprint 06 — Knowledge & Evidence Workspace</h1>
  <ul>
    <li><a href="knowledge_light.html">Light</a></li>
    <li><a href="knowledge_dark.html">Dark</a></li>
  </ul>
  <pre>${JSON.stringify(
    {
      blocks: blocks.map((b) => ({
        id: b.id,
        insight: b.insight,
        evidence: b.evidence.length,
        rules: b.rules.length,
        classical: b.classical.length,
      })),
      assert_failures: assert,
    },
    null,
    2
  )}</pre>`,
  "utf8"
);

console.log("wrote", outDir);
console.log("assert_failures", assert);
console.log(pathToFileURL(path.join(outDir, "knowledge_light.html")).href);
if (assert.length) process.exitCode = 1;
