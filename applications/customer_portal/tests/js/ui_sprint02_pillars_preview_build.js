/**
 * UI Sprint 02 — Four Pillars Workspace preview.
 * Run: node applications/customer_portal/tests/js/ui_sprint02_pillars_preview_build.js
 */
const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");
const vm = require("vm");

const root = path.join(__dirname, "../..");
const outDir = path.join(root, "../../docs/reports/ui_sprint02_four_pillars/preview");
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
  "report/pillars.js",
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
};

const data = {
  bazi: {
    day_master: "Canh",
    day_master_element: "Kim",
    year_pillar: {
      stem: "Canh",
      branch: "Ngọ",
      ten_god: "Tỷ Kiên",
      nap_am: "Lộ Bàng Thổ",
      truong_sinh: "Đế Vượng",
      tang_can: "Đinh, Kỷ",
    },
    month_pillar: {
      stem: "Tân",
      branch: "Tỵ",
      ten_god: "Kiếp Tài",
      nap_am: "Lộ Bàng Thổ",
      truong_sinh: "Lâm Quan",
      tang_can: "Bính, Mậu, Canh",
    },
    day_pillar: {
      stem: "Canh",
      branch: "Thìn",
      ten_god: "Nhật Chủ",
      nap_am: "Bạch Lạp Kim",
      truong_sinh: "Mộ",
      tang_can: "Mậu, Ất, Quý",
    },
    hour_pillar: {
      stem: "Tân",
      branch: "Tỵ",
      ten_god: "Kiếp Tài",
      nap_am: "Lộ Bàng Thổ",
      truong_sinh: "Lâm Quan",
      tang_can: "Bính, Mậu, Canh",
    },
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
    strengths: ["Nhật chủ vững"],
    weaknesses: ["Tài tinh yếu"],
    recommendations: ["Ưu tiên môi trường Thủy · Kim."],
  },
  interpretation: { confidence: 0.82, sections: [] },
};

const model = sandbox.window.BteReportModel.build(data, { input });
const pillarsHtml = sandbox.window.BteReportRender.tiers.bazi(model);

function page(theme) {
  return `<!doctype html>
<html lang="vi" data-theme="${theme}">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Sprint 02 Pillars ${theme}</title>
<style>${css}
body{padding:1.25rem;background:var(--bg);color:var(--ink);}
.panel{max-width:1280px;margin:0 auto;}
.preview-banner{margin:0 0 1rem;color:var(--muted);font-size:0.9rem;}
</style>
</head>
<body>
<div class="panel result-report-page">
  <p class="preview-banner">BTE UI Sprint 02 — Four Pillars Workspace · theme=${theme}</p>
  <h1>Kết quả phân tích</h1>
  <p class="muted">Ngày sinh: 15/05/1990 10:30 · Giới tính: Nam</p>
  <div class="rpt-main">${pillarsHtml}</div>
</div>
</body>
</html>`;
}

const assert = [];
const day = (model.pillars || []).find((p) => p.isDay);
if (!day) assert.push("missing_day");
if (!pillarsHtml.includes('data-component="FourPillarsWorkspace"')) {
  assert.push("missing_workspace");
}
if (!pillarsHtml.includes("fp-col-day")) assert.push("day_not_highlighted");
if (!pillarsHtml.includes("fp-chip")) assert.push("hidden_chips");
if (!pillarsHtml.includes("fp-badge")) assert.push("ten_god_badge");
if (pillarsHtml.includes("<table")) assert.push("uses_table");
if (pillarsHtml.includes("null") || pillarsHtml.includes("undefined")) {
  assert.push("nullish");
}
if (
  pillarsHtml.includes("bazi.workspace_hint") ||
  pillarsHtml.includes("report.unavailable") === false &&
    pillarsHtml.includes("bazi.relation_to_day_master")
) {
  /* raw key check */
}
if (/bazi\.[a-z_]+/.test(pillarsHtml.replace(/bazi\./g, ""))) {
  // soft
}
[
  "bazi.workspace_hint",
  "bazi.pillar_meta",
  "bazi.relation_to_day_master",
  "bazi.role_day_master",
].forEach((k) => {
  if (pillarsHtml.includes(k)) assert.push("raw_key:" + k);
});

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, "pillars_light.html"), page("light"), "utf8");
fs.writeFileSync(path.join(outDir, "pillars_dark.html"), page("dark"), "utf8");
fs.writeFileSync(
  path.join(outDir, "index.html"),
  `<!doctype html><meta charset="utf-8"><title>Sprint 02</title>
  <h1>UI Sprint 02 — Four Pillars</h1>
  <ul>
    <li><a href="pillars_light.html">Desktop Light</a></li>
    <li><a href="pillars_dark.html">Desktop Dark</a></li>
  </ul>
  <pre>${JSON.stringify({ day, assert_failures: assert }, null, 2)}</pre>`,
  "utf8"
);

console.log("wrote", outDir);
console.log("assert_failures", assert);
console.log(pathToFileURL(path.join(outDir, "pillars_light.html")).href);
if (assert.length) process.exitCode = 1;
