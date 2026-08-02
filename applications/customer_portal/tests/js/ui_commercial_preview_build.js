/**
 * Build static HTML previews for UI Commercial Polish V1.
 * Run: node applications/customer_portal/tests/js/ui_commercial_preview_build.js
 */
const fs = require("fs");
const path = require("path");
const vm = require("vm");
const { pathToFileURL } = require("url");

const root = path.join(__dirname, "../..");
const outDir = path.join(root, "../../docs/reports/ui_commercial_preview");
const cssDir = path.join(root, "static/css");
const css = [
  "tokens.css",
  "base.css",
  "components.css",
  "layout.css",
  "pages.css",
  "domain.css",
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

vm.runInNewContext(
  fs.readFileSync(path.join(root, "static/js/ui/components.js"), "utf8"),
  sandbox
);

const presenters = [
  "chart_info.js",
  "summary_builder.js",
  "basic_info.js",
  "calendar.js",
  "bazi.js",
  "score.js",
  "interpretation.js",
  "narrative.js",
  "discussion.js",
];
for (const file of presenters) {
  vm.runInNewContext(
    fs.readFileSync(path.join(root, "static/js/presenters", file), "utf8"),
    sandbox
  );
}

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
  customer: {
    full_name: "Nguyễn Văn A",
    gender: "male",
    birth_place: "Hà Nội",
    timezone: "Asia/Ho_Chi_Minh",
  },
  calendar: {
    solar_date: "15/05/1990",
    solar_hour: 10,
    solar_minute: 30,
    lunar_date: "21/04 Canh Ngọ",
    timezone: "Asia/Ho_Chi_Minh",
  },
  bazi: {
    day_master: "Canh",
    day_master_element: "Kim",
    year_pillar: { stem: "Canh", branch: "Ngọ", ten_god: "Tỷ Kiên" },
    month_pillar: { stem: "Tân", branch: "Tỵ", ten_god: "Kiếp Tài" },
    day_pillar: { stem: "Canh", branch: "Thìn", ten_god: "Nhật Chủ" },
    hour_pillar: { stem: "Tân", branch: "Tỵ", ten_god: "Kiếp Tài" },
    ten_gods: ["Tỷ Kiên", "Kiếp Tài", "Chính Ấn"],
    shensha: [{ name: "Hoa Cái" }, { name: "Văn Xương" }],
  },
  pattern: {
    than_vuong_nhuoc: "Thân vượng",
    dung_than: "Thủy",
    hy_than: "Mộc",
  },
  score: {
    overall_score: 72,
    strength_score: 68,
    pattern_score: 70,
    wealth_score: 65,
    strengths: ["Nhật chủ vững", "Ấn tinh hỗ trợ"],
    weaknesses: ["Tài tinh yếu"],
    recommendations: ["Ưu tiên môi trường Thủy · Mộc"],
  },
  interpretation: {
    confidence: 0.82,
    section_count: 3,
    sections: [
      {
        id: "overview",
        title: "Tổng quan",
        body: "Lá số nghiêng về thân vượng, dụng thần thuộc Thủy.",
      },
      {
        id: "career",
        title: "Sự nghiệp",
        body: "Hướng nghề liên quan Kim · Thủy phù hợp hơn.",
      },
      {
        id: "conclusion",
        title: "Kết luận",
        body: "Cần giữ cân bằng Ngũ hành, tránh thiên lệch Hỏa.",
      },
    ],
  },
  narrative: {
    title: "Bản luận",
    sections: [
      {
        title: "Tóm tắt",
        body: "Đây là bản luận fallback khi Knowledge Expert chưa trả lời.",
      },
    ],
  },
  knowledge_expert: {
    alters_public_pipeline: false,
    alters_narrative: false,
  },
};

const P = sandbox.window.BtePresenters;
const tabs = [
  {
    id: "basic",
    label: catalog.stages.basic,
    html: P.basicInfo(data, { input }),
  },
  {
    id: "calendar",
    label: catalog.stages.calendar,
    html: P.calendar(data.calendar, { timezone: input.timezone, data }),
  },
  {
    id: "bazi",
    label: catalog.stages.bazi,
    html: P.bazi(data.bazi, { data }),
  },
  {
    id: "score",
    label: catalog.stages.score,
    html: P.score(data.score, { data, input }),
  },
  {
    id: "interpretation",
    label: catalog.stages.interpretation,
    html: P.interpretation(data.interpretation, { data }),
  },
  {
    id: "discussion",
    label: catalog.stages.discussion,
    html: P.discussion(data.narrative, { data, input }),
  },
];

fs.mkdirSync(outDir, { recursive: true });

function pageShell(title, body, activeId) {
  const tabButtons = tabs
    .map(
      (tab) =>
        `<button class="tab${tab.id === activeId ? " active" : ""}" type="button">${tab.label}</button>`
    )
    .join("");
  return `<!doctype html>
<html lang="vi" data-theme="light">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>${title}</title>
<style>${css}
body{padding:1.25rem;background:var(--bg);}
.panel{max-width:1200px;margin:0 auto;}
.stage-view{margin-top:1rem;}
.preview-banner{margin:0 0 0.75rem;color:var(--muted);font-size:0.9rem;}
</style>
</head>
<body>
<div class="panel">
  <p class="preview-banner">BTE Portal UI Commercial Polish V1 — preview (sample data)</p>
  <h1>Kết quả</h1>
  <p class="muted result-meta-friendly">Ngày sinh: 15/05/1990 10:30
Giới tính: Nam</p>
  <div class="tabs ui-tabs">${tabButtons}</div>
  <div class="stage-view">${body}</div>
</div>
</body>
</html>`;
}

const indexLinks = [];
for (const tab of tabs) {
  const file = `tab_${tab.id}.html`;
  fs.writeFileSync(
    path.join(outDir, file),
    pageShell(`UI Commercial — ${tab.label}`, tab.html, tab.id),
    "utf8"
  );
  indexLinks.push(`<li><a href="${file}">${tab.label}</a></li>`);
}

fs.writeFileSync(
  path.join(outDir, "index.html"),
  `<!doctype html><meta charset="utf-8"><title>UI Commercial Preview Index</title>
  <h1>BTE Portal UI Commercial Polish V1</h1>
  <p>Before snapshots: <a href="../ui_v2_preview/index.html">ui_v2_preview</a></p>
  <ol>${indexLinks.join("")}</ol>`,
  "utf8"
);

console.log("wrote", outDir);
for (const tab of tabs) {
  console.log(
    "-",
    tab.id,
    pathToFileURL(path.join(outDir, `tab_${tab.id}.html`)).href
  );
}
