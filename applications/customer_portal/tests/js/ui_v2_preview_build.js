/**
 * Build static HTML previews for EPIC 01 Result UI v2.0 screenshots.
 * Run: node applications/customer_portal/tests/js/ui_v2_preview_build.js
 */
const fs = require("fs");
const path = require("path");
const vm = require("vm");
const { pathToFileURL } = require("url");

const root = path.join(__dirname, "../..");
const outDir = path.join(root, "../../docs/reports/ui_v2_preview");
const css = fs.readFileSync(path.join(root, "static/css/portal.css"), "utf8");
const catalog = JSON.parse(
  fs.readFileSync(path.join(root, "static/i18n/vi.json"), "utf8")
);

function deepGet(obj, key) {
  return String(key)
    .split(".")
    .reduce((node, p) => (node && typeof node === "object" ? node[p] : undefined), obj);
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
    year_can_chi: "Canh Ngọ",
    month_can_chi: "Ất Tỵ",
    day_can_chi: "Bính Ngọ",
    hour_can_chi: "Quý Tỵ",
    solar_term: "Lập Hạ",
    timezone: "Asia/Ho_Chi_Minh",
    lunar: { leap: false, day: 21, month: 4, year_can_chi: "Canh Ngọ" },
  },
  feng_shui: {
    cung_phi: "Đoài",
    menh_quai: "Đoài",
    nhom_trach: "tay_tu_trach",
  },
  bazi: {
    day_master: "Bính",
    day_master_element: "Hỏa",
    day_master_yin_yang: "Dương",
    year_pillar: {
      stem: "Canh",
      branch: "Ngọ",
      hidden_stems: ["Đinh", "Kỷ"],
      ten_god: "Thất Sát",
      truong_sinh: "Đế Vượng",
      nap_am: "Lộ Bàng Thổ",
    },
    month_pillar: {
      stem: "Ất",
      branch: "Tỵ",
      hidden_stems: ["Bính", "Mậu", "Canh"],
      ten_god: "Thương Quan",
      truong_sinh: "Lâm Quan",
      nap_am: "Phúc Đăng Hỏa",
    },
    day_pillar: {
      stem: "Bính",
      branch: "Ngọ",
      hidden_stems: ["Đinh", "Kỷ"],
      ten_god: "Tỷ Kiên",
      truong_sinh: "Đế Vượng",
      nap_am: "Thiên Hà Thủy",
    },
    hour_pillar: {
      stem: "Quý",
      branch: "Tỵ",
      hidden_stems: ["Bính", "Mậu", "Canh"],
      ten_god: "Chính Ấn",
      truong_sinh: "Thai",
      nap_am: "Trường Lưu Thủy",
    },
    ten_gods: ["Thất Sát", "Thương Quan", "Tỷ Kiên", "Chính Ấn"],
    shensha: ["Hoa Cái", "Thiên Ất", "Văn Xương", "Quốc Ấn"],
  },
  pattern: {
    than_vuong_nhuoc: "Thân Vượng",
    dung_than: "Thủy",
    hy_than: "Kim",
    cach_cuc: "Thất Sát",
  },
  score: {
    total_score: 91,
    strength_score: 88,
    pattern_score: 92,
    luck_score: 75,
    grade: "A+",
    confidence: "high",
    recommendation: "Ưu tiên bổ Thủy · giữ cân bằng Hỏa",
    strengths: ["Nhật chủ sáng rõ", "Ấn tinh hỗ trợ"],
    weaknesses: ["Hỏa khí hơi thịnh", "Quan sát đại vận Kim Thủy"],
    wuxing_series: [
      { label: "Mộc", value: 2 },
      { label: "Hỏa", value: 7 },
      { label: "Thổ", value: 4 },
      { label: "Kim", value: 3 },
      { label: "Thủy", value: 1 },
    ],
  },
  interpretation: {
    confidence: 0.86,
    section_count: 6,
    sections: [
      { id: "overview", title: "Tổng quan", body: "Lá số thiên về Hỏa khí, Nhật chủ Bính rõ nét." },
      { id: "bazi", title: "Bát Tự", body: "Tứ trụ cân đối với Ấn tại giờ hỗ trợ học vấn." },
      { id: "five_elements", title: "Ngũ Hành", body: "Hỏa vượng · Thủy nhu cầu điều hòa." },
      { id: "ten_gods", title: "Thập Thần", body: "Thất Sát năm · Chính Ấn giờ." },
      { id: "career", title: "Sự nghiệp", body: "Hướng chuyên môn kỹ thuật hoặc quản trị." },
      { id: "conclusion", title: "Kết luận", body: "Giữ cân bằng ngũ hành, ưu tiên môi trường mát." },
    ],
  },
  narrative: {
    title: "Thảo luận AI",
    markdown:
      "## Kết luận ngắn\n\nDựa trên **Tứ trụ** Bính Ngọ và **Ngũ hành** Hỏa thịnh, kết hợp **Thập thần** Thất Sát/Chính Ấn cùng **Thần sát** Hoa Cái · Văn Xương, **Dụng thần** Thủy giúp điều hòa cục diện.",
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
body{padding:1.25rem;}
.panel{max-width:1100px;margin:0 auto;}
.stage-view{margin-top:1rem;}
.preview-banner{margin:0 0 0.75rem;color:var(--muted);font-size:0.9rem;}
</style>
</head>
<body>
<div class="panel">
  <p class="preview-banner">BTE Portal UI v2.0 — preview (sample data)</p>
  <h1>Kết quả</h1>
  <p class="muted result-meta-friendly">Ngày sinh: 15/05/1990 10:30
Giới tính: Nam</p>
  <div class="tabs">${tabButtons}</div>
  <div class="stage-view">${body}</div>
</div>
</body>
</html>`;
}

const indexLinks = [];
for (const tab of tabs) {
  const file = `tab_${tab.id}.html`;
  fs.writeFileSync(path.join(outDir, file), pageShell(`UI v2 — ${tab.label}`, tab.html, tab.id), "utf8");
  indexLinks.push(`<li><a href="${file}">${tab.label}</a></li>`);
}

fs.writeFileSync(
  path.join(outDir, "index.html"),
  `<!doctype html><meta charset="utf-8"><title>UI v2 Preview Index</title>
  <h1>BTE Portal UI v2.0 Previews</h1><ol>${indexLinks.join("")}</ol>`,
  "utf8"
);

console.log("wrote", outDir);
for (const tab of tabs) {
  console.log("-", tab.id, pathToFileURL(path.join(outDir, `tab_${tab.id}.html`)).href);
}
