/**
 * Build Phase 2 report IA static preview.
 * Run: node applications/customer_portal/tests/js/ui_phase2_preview_build.js
 */
const fs = require("fs");
const path = require("path");
const vm = require("vm");
const { pathToFileURL } = require("url");

const root = path.join(__dirname, "../..");
const outDir = path.join(root, "../../docs/reports/ui_phase2_report_ia/preview");
const cssDir = path.join(root, "static/css");
const css = [
  "tokens.css",
  "base.css",
  "components.css",
  "layout.css",
  "pages.css",
  "domain.css",
  "report.css",
]
  .map((name) => fs.readFileSync(path.join(cssDir, name), "utf8"))
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
      return text.replace(/\{(\w+)\}/g, (_, name) =>
        vars[name] != null ? String(vars[name]) : `{${name}}`
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
  "report/report_model.js",
  "report/report_render.js",
].forEach((rel) => {
  vm.runInNewContext(
    fs.readFileSync(path.join(root, "static/js", rel), "utf8"),
    sandbox
  );
});

const input = {
  full_name: "Nguyễn Văn A",
  gender: "male",
  year: 1990,
  month: 5,
  day: 15,
  hour: 10,
  minute: 30,
  birth_place: "Hà Nội",
  timezone: "Asia/Ho_Chi_Minh",
};

const data = {
  bazi: {
    day_master: "Canh",
    day_master_element: "Kim",
    year_pillar: { stem: "Canh", branch: "Ngọ", ten_god: "Tỷ Kiên", nap_am: "Lộ Bàng Thổ", truong_sinh: "Đế Vượng" },
    month_pillar: { stem: "Tân", branch: "Tỵ", ten_god: "Kiếp Tài", nap_am: "Lộ Bàng Thổ", truong_sinh: "Lâm Quan" },
    day_pillar: { stem: "Canh", branch: "Thìn", ten_god: "Nhật Chủ", nap_am: "Bạch Lạp Kim", truong_sinh: "Mộ" },
    hour_pillar: { stem: "Tân", branch: "Tỵ", ten_god: "Kiếp Tài", nap_am: "Lộ Bàng Thổ", truong_sinh: "Lâm Quan" },
    ten_gods: ["Tỷ Kiên", "Kiếp Tài", "Chính Ấn"],
    shensha: [{ name: "Hoa Cái" }, { name: "Văn Xương" }],
  },
  pattern: {
    than_vuong_nhuoc: "Thân vượng",
    dung_than: "Thủy",
    hy_than: "Mộc",
    ky_than: "Hỏa",
    cach_cuc: "chinh_an",
  },
  score: {
    overall_score: 72,
    strength_score: 68,
    strengths: ["Nhật chủ vững", "Ấn tinh hỗ trợ"],
    weaknesses: ["Tài tinh yếu"],
  },
  interpretation: {
    confidence: 0.82,
    section_count: 4,
    sections: [
      { id: "overview", title: "Tổng quan", body: "Lá số nghiêng về thân vượng, dụng thần thuộc Thủy." },
      { id: "career", title: "Sự nghiệp", body: "Hướng nghề Kim · Thủy phù hợp hơn." },
      { id: "wealth", title: "Tài vận", body: "Tài tinh cần bồi dưỡng qua môi trường hỗ trợ." },
      { id: "conclusion", title: "Kết luận", body: "Giữ cân bằng Ngũ hành, ưu tiên dụng thần." },
    ],
  },
  narrative: {
    sections: [{ title: "Tóm tắt", body: "Bản luận fallback cho Knowledge tier." }],
  },
  knowledge_expert: {
    alters_public_pipeline: false,
    alters_narrative: false,
    status: "ready",
  },
};

const model = sandbox.window.BteReportModel.build(data, { input });
const html = sandbox.window.BteReportRender.render(model);

fs.mkdirSync(outDir, { recursive: true });
const page = `<!doctype html>
<html lang="vi" data-theme="light">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Phase 2 Report IA Preview</title>
<style>${css}
body{padding:1.25rem;background:var(--bg);}
.panel{max-width:1280px;margin:0 auto;}
.preview-banner{margin:0 0 1rem;color:var(--muted);font-size:0.9rem;}
</style>
</head>
<body>
<div class="panel result-report-page">
  <p class="preview-banner">BTE Phase 2 — After (6-tier report IA, sample data)</p>
  <h1>Kết quả phân tích</h1>
  <p class="muted">Ngày sinh: 15/05/1990 10:30 · Giới tính: Nam</p>
  ${html}
</div>
</body>
</html>`;

fs.writeFileSync(path.join(outDir, "after_report.html"), page, "utf8");
fs.writeFileSync(
  path.join(outDir, "index.html"),
  `<!doctype html><meta charset="utf-8"><title>Phase 2 Preview</title>
  <h1>Phase 2 Report IA</h1>
  <ul>
    <li><a href="after_report.html">After — 6-tier report</a></li>
    <li><a href="../../ui_commercial_preview/index.html">Before — commercial tab UI</a></li>
    <li><a href="../../ui_v2_preview/index.html">Earlier — UI v2 tabs</a></li>
  </ul>`,
  "utf8"
);

console.log("wrote", outDir);
console.log(pathToFileURL(path.join(outDir, "after_report.html")).href);
