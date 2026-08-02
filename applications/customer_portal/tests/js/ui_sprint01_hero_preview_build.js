/**
 * UI Sprint 01 — Executive Hero preview (Tier 1 only focus).
 * Run: node applications/customer_portal/tests/js/ui_sprint01_hero_preview_build.js
 */
const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");
const vm = require("vm");

const root = path.join(__dirname, "../..");
const outDir = path.join(root, "../../docs/reports/ui_sprint01_executive_hero/preview");
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
    },
    month_pillar: {
      stem: "Tân",
      branch: "Tỵ",
      ten_god: "Kiếp Tài",
      nap_am: "Lộ Bàng Thổ",
      truong_sinh: "Lâm Quan",
    },
    day_pillar: {
      stem: "Canh",
      branch: "Thìn",
      ten_god: "Nhật Chủ",
      nap_am: "Bạch Lạp Kim",
      truong_sinh: "Mộ",
    },
    hour_pillar: {
      stem: "Tân",
      branch: "Tỵ",
      ten_god: "Kiếp Tài",
      nap_am: "Lộ Bàng Thổ",
      truong_sinh: "Lâm Quan",
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
    strength_score: 68,
    strengths: ["Nhật chủ vững", "Ấn tinh hỗ trợ"],
    weaknesses: ["Tài tinh yếu"],
    recommendations: ["Ưu tiên môi trường Thủy · Kim để nuôi dụng thần."],
  },
  interpretation: {
    confidence: 0.82,
    sections: [
      {
        id: "conclusion",
        title: "Kết luận",
        body: "Giữ cân bằng Ngũ hành, ưu tiên dụng thần.",
      },
    ],
  },
};

const model = sandbox.window.BteReportModel.build(data, { input });
const heroOnly = sandbox.window.BteReportRender.tiers.executive(model);

function page(theme, bodyInner, title) {
  return `<!doctype html>
<html lang="vi" data-theme="${theme}">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>${title}</title>
<style>${css}
body{padding:1.25rem;background:var(--bg);color:var(--ink);}
.panel{max-width:1100px;margin:0 auto;}
.preview-banner{margin:0 0 1rem;color:var(--muted);font-size:0.9rem;}
.rpt-shell{grid-template-columns:200px minmax(0,1fr);}
.hero-isolate .rpt-rail,
.hero-isolate #tier-bazi,
.hero-isolate #tier-charts,
.hero-isolate #tier-analysis,
.hero-isolate #tier-interpretation,
.hero-isolate #tier-knowledge{display:none !important;}
.hero-isolate .rpt-shell{grid-template-columns:1fr;}
</style>
</head>
<body>
<div class="panel result-report-page hero-isolate">
  <p class="preview-banner">BTE UI Sprint 01 — Executive Hero (Tier 1) · theme=${theme}</p>
  <h1>Kết quả phân tích</h1>
  <p class="muted">Ngày sinh: 15/05/1990 10:30 · Giới tính: Nam</p>
  <div class="rpt-shell"><div class="rpt-main">${bodyInner}</div></div>
</div>
</body>
</html>`;
}

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(
  path.join(outDir, "hero_light.html"),
  page("light", heroOnly, "Sprint 01 Hero Light"),
  "utf8"
);
fs.writeFileSync(
  path.join(outDir, "hero_dark.html"),
  page("dark", heroOnly, "Sprint 01 Hero Dark"),
  "utf8"
);

const assert = [];
const ex = model.executive;
if (ex.day_master !== "Canh") assert.push("day_master");
if (!ex.quality_verdict || !ex.quality_verdict.available) assert.push("quality_verdict");
if (ex.quality_verdict && ex.quality_verdict.band !== "high") assert.push("quality_band_high");
if (!ex.first_recommendation) assert.push("first_recommendation");
if (/Ưu tiên môi trường/.test(ex.first_recommendation) === false) {
  assert.push("first_recommendation_from_score");
}
if (heroOnly.includes("null") || heroOnly.includes("undefined")) assert.push("nullish_literal");
if (
  heroOnly.includes("report.quality_verdict") ||
  heroOnly.includes("report.first_recommendation")
) {
  assert.push("raw_i18n_key");
}

fs.writeFileSync(
  path.join(outDir, "index.html"),
  `<!doctype html><meta charset="utf-8"><title>Sprint 01 Hero</title>
  <h1>UI Sprint 01 — Executive Hero</h1>
  <ul>
    <li><a href="hero_light.html">Hero Desktop Light</a></li>
    <li><a href="hero_dark.html">Hero Dark Mode</a></li>
  </ul>
  <pre>${JSON.stringify({ executive: ex, assert_failures: assert }, null, 2)}</pre>`,
  "utf8"
);

console.log("wrote", outDir);
console.log("assert_failures", assert);
console.log(pathToFileURL(path.join(outDir, "hero_light.html")).href);
if (assert.length) process.exitCode = 1;
