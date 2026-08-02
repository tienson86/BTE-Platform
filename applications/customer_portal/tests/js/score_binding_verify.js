/**
 * Sprint 2B / UI v2 — verify score presenter bindings (Node, no browser).
 */
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const scoreJs = fs.readFileSync(
  path.join(__dirname, "../../static/js/presenters/score.js"),
  "utf8"
);

const catalog = JSON.parse(
  fs.readFileSync(path.join(__dirname, "../../static/i18n/vi.json"), "utf8")
);

function deepGet(obj, key) {
  const parts = String(key).split(".");
  let node = obj;
  for (const p of parts) {
    if (node == null || typeof node !== "object" || !(p in node)) return undefined;
    node = node[p];
  }
  return node;
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

vm.runInNewContext(scoreJs, sandbox);
const render = sandbox.window.BtePresenters.score;

const score = {
  success: true,
  total_score: 55.25,
  strength_score: 45.0,
  pattern_score: 100.0,
  ten_god_score: 100.0,
  wuxing_score: 0.0,
  useful_god_score: 20.0,
  shensha_score: 100.0,
  luck_score: 0.0,
  grade: "D+",
  confidence: "medium",
  recommendation: "Nhiều điểm cần cải thiện",
  wuxing_series: [
    { label: "Mộc", value: 4.0 },
    { label: "Hỏa", value: 5.0 },
  ],
  ten_god_series: [{ label: "Thất Sát", value: 1.0 }],
};

const html = render(score, {
  data: {
    bazi: {
      year_pillar: { ten_god: "Thất Sát" },
      month_pillar: { ten_god: "Chính Tài" },
      day_pillar: { ten_god: "Tỷ Kiên" },
      hour_pillar: { ten_god: "Thiên Ấn" },
      shensha: ["Hoa Cái", "Thiên Ất"],
    },
    score,
  },
});

const checks = [
  ["overall grade D+", html.includes("D+")],
  ["overall out of 10", html.includes("/ 10")],
  ["strength category 45", html.includes(">45<") || html.includes(">45.0<")],
  ["pattern category 100", html.includes(">100<") || html.includes(">100.0<")],
  ["luck category 0", /Hậu Vận[\s\S]*?>0(\.0)?</.test(html)],
  ["recommendation shown", html.includes("Nhiều điểm cần cải thiện")],
  ["checklist present", html.includes("Hoa Cái")],
  ["checklist yes/no", html.includes("Có") && html.includes("Không")],
  ["executive section titles", html.includes("Điểm mạnh") && html.includes("Điểm yếu")],
  ["no overall_score alias needed", !html.includes("overall_score")],
];

let failed = 0;
for (const [name, ok] of checks) {
  console.log(ok ? "PASS" : "FAIL", name);
  if (!ok) failed += 1;
}

const out = path.join(
  __dirname,
  "../../../../docs/reports/_s2b_score_render.html"
);
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(
  out,
  `<!doctype html><meta charset="utf-8"><title>UI v2 Score Render</title>${html}`,
  "utf8"
);
console.log("wrote", out);
process.exit(failed ? 1 : 0);
