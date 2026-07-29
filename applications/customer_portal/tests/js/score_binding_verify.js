/**
 * Sprint 2B — verify score presenter bindings (Node, no browser).
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

const html = render(score);
const checks = [
  ["total_score card", html.includes("55.25")],
  ["strength_score card", html.includes(">45<") || html.includes(">45.0<")],
  ["pattern_score card", html.includes(">100<") || html.includes(">100.0<")],
  ["useful_god 20", html.includes(">20<") || html.includes(">20.0<")],
  ["shensha 100 present", /Điểm Thần sát[\s\S]*?>100(\.0)?</.test(html)],
  ["wuxing_score label", html.includes("Điểm Ngũ hành")],
  ["wuxing numeric 0 as score card", /Điểm Ngũ hành[\s\S]*?<div class="bte-card-value">0(\.0)?<\/div>/.test(html)],
  ["not using series as score title alone", html.includes("Phân bố Ngũ hành")],
  ["confidence medium", html.includes("medium")],
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
  `<!doctype html><meta charset="utf-8"><title>Sprint 2B Score Render</title>${html}`,
  "utf8"
);
console.log("wrote", out);
process.exit(failed ? 1 : 0);
