/**
 * Canonical Full Customer Report ViewModel.
 * Structured analytical truth + NarrativeResult + supporting sections.
 * Presentation only — no engine recalculation.
 */

import type { AnalysisDataDto, AnalyzeChartRequest, PillarDto } from "../models";
import {
  canonicalStrengthEvidence,
  canonicalStrengthLabel,
  formatCanonicalStrengthScore,
  readCanonicalStrengthScore,
} from "../adapters/canonicalStrength";
import { canonicalPatternEvidence } from "../adapters/canonicalPattern";
import {
  FIVE_ELEMENTS_SECTION_TITLE,
  formatFiveElementsProvenance,
} from "../adapters/canonicalFiveElements";
import {
  canonicalFavorableDisplay,
  canonicalUsefulDisplay,
  canonicalUsefulGodPayload,
  canonicalUnfavorableDisplay,
} from "../adapters/canonicalUsefulGod";
import {
  canonicalBalancingNeedLabel,
  canonicalClimateStateLabel,
  canonicalTemperatureEvidence,
} from "../adapters/canonicalTemperature";
import { shenShaEntriesFromAnalysis, type ShenShaEntryView } from "../adapters/canonicalShenSha";
import {
  asTenGodsPayload,
  hiddenLinesForPillar,
  stemDisplay,
} from "../adapters/tenGodsDisplay";
import {
  asNarrativeResult,
  careerFieldText,
  careerSelectionFromNarrative,
  hasUsableNarrativeResult,
  type NarrativeResultDto,
} from "../adapters/narrativeResultAdapter";
import {
  analyticalFiveElementCounts,
  analyticalHiddenTenGods,
  analyticalTenGods,
} from "../resultState/currentResult";

export const CANONICAL_NARRATIVE_SECTIONS = [
  { id: "executive_summary", title: "Tóm tắt điều hành", match: /executive|summary|tóm tắt/i },
  { id: "observation", title: "Quan sát", match: /observation|quan sát/i },
  { id: "reasoning", title: "Lý giải", match: /reasoning|explanation|lý giải/i },
  { id: "impact", title: "Tác động", match: /impact|ảnh hưởng|tác động/i },
  { id: "recommendation", title: "Khuyến nghị", match: /recommendation|suggestion|khuyến/i },
  { id: "warning", title: "Lưu ý", match: /warning|caution|cảnh báo|lưu ý/i },
  { id: "conclusion", title: "Kết luận", match: /conclusion|kết luận/i },
] as const;

export type FullReportPillar = {
  readonly key: "year" | "month" | "day" | "hour";
  readonly label: string;
  readonly stem: string;
  readonly branch: string;
  readonly napAm: string;
  readonly hiddenStems: string;
  readonly tenGod: string;
  readonly growthStage: string;
};

export type FullReportNarrativeSection = {
  readonly id: string;
  readonly title: string;
  readonly body: string;
  readonly present: boolean;
};

export type FullReportSupportingSection = {
  readonly id: string;
  readonly title: string;
  readonly body: string;
};

export type FullReportViewModel = {
  readonly analysisId: string;
  readonly customerName: string;
  readonly gender: string;
  readonly birthPlace: string;
  readonly timezone: string;
  readonly solarDate: string;
  readonly lunarDate: string;
  readonly birthTime: string;
  readonly dayMaster: string;
  readonly dayMasterElement: string;
  readonly yinYang: string;
  readonly strengthLabel: string;
  readonly strengthScore: string;
  readonly strengthEvidence: string;
  readonly pattern: string;
  readonly patternEvidence: string;
  readonly usefulGod: string;
  readonly hyThan: string;
  readonly kyThan: string;
  readonly fiveElements: ReadonlyArray<{ readonly name: string; readonly count: number }>;
  readonly tenGods: readonly string[];
  readonly hiddenTenGods: readonly string[];
  readonly tenGodsNote: string;
  readonly pillars: readonly FullReportPillar[];
  readonly shenSha: readonly ShenShaEntryView[];
  readonly luckStartAge: string;
  readonly luckCurrent: string;
  readonly luckCycles: ReadonlyArray<{
    readonly label: string;
    readonly years: string;
    readonly current: boolean;
  }>;
  readonly cungPhi: string;
  readonly menhQuai: string;
  readonly nhomTrach: string;
  readonly scoreLabel: string;
  readonly climateState: string;
  readonly balancingNeed: string;
  readonly climateEvidence: string;
  readonly narrative: readonly FullReportNarrativeSection[];
  readonly supporting: readonly FullReportSupportingSection[];
  readonly factsOnly: false;
};

export type BuildFullReportOptions = {
  readonly input?: AnalyzeChartRequest | Record<string, unknown> | null;
  readonly analysisId?: string | null;
};

const PILLAR_META: ReadonlyArray<{
  key: FullReportPillar["key"];
  label: string;
  field: keyof NonNullable<AnalysisDataDto["bazi"]>;
}> = [
  { key: "year", label: "Năm", field: "year_pillar" },
  { key: "month", label: "Tháng", field: "month_pillar" },
  { key: "day", label: "Ngày", field: "day_pillar" },
  { key: "hour", label: "Giờ", field: "hour_pillar" },
];

const STORAGE_ID_RE = /^(last-result|last_result|bte_last_result|bte_history|bte_view_result)$/i;

/**
 * Build the single customer report model from the current analysis payload.
 */
export function buildFullReportViewModel(
  data: AnalysisDataDto,
  options: BuildFullReportOptions = {},
): FullReportViewModel {
  const input = (options.input || {}) as Record<string, unknown>;
  const calendar = data.calendar || {};
  const bazi = data.bazi || {};
  const pattern = asRecord(data.pattern);
  const useful = canonicalUsefulGodPayload(data);
  const feng = asRecord(data.feng_shui);
  const score = data.score || {};
  const luck = data.luck;
  const narrative = asNarrativeResult(data.narrative_result);
  const counts = analyticalFiveElementCounts(data) || {
    Mộc: 0,
    Hỏa: 0,
    Thổ: 0,
    Kim: 0,
    Thủy: 0,
  };
  const current = luck?.current_cycle;
  const currentGan = text(current?.gan_zhi);
  const cycles = (luck?.cycles ?? []).map((cycle) => {
    const label = text(cycle.gan_zhi);
    const years =
      cycle.year_start != null && cycle.year_end != null
        ? `${cycle.year_start}–${cycle.year_end}`
        : "";
    return {
      label,
      years,
      current: Boolean(currentGan) && label === currentGan,
    };
  });

  return {
    analysisId: sanitizeAnalysisId(options.analysisId, data, input),
    customerName: text(data.customer?.full_name || input.full_name),
    gender: text(data.customer?.gender || input.gender),
    birthPlace: text(data.customer?.birth_place || input.birth_place),
    timezone: text(data.customer?.timezone || input.timezone, "Asia/Ho_Chi_Minh"),
    solarDate: solarFromInput(calendar.solar_date, input),
    lunarDate: text(calendar.lunar_date),
    birthTime: timeFromInput(input),
    dayMaster: text(bazi.day_master),
    dayMasterElement: text(bazi.day_master_element),
    yinYang: text(bazi.day_master_yin_yang),
    strengthLabel: canonicalStrengthLabel(data) || text(data.strength?.strength_level),
    strengthScore: (() => {
      const score = readCanonicalStrengthScore(data);
      return score == null ? "" : formatCanonicalStrengthScore(score);
    })(),
    strengthEvidence: canonicalStrengthEvidence(data),
    pattern: text(pattern.cach_cuc || pattern.pattern),
    patternEvidence: canonicalPatternEvidence(data),
    usefulGod: canonicalUsefulDisplay(useful, text(pattern.dung_than)),
    hyThan: canonicalFavorableDisplay(useful, text(pattern.hy_than)),
    kyThan: canonicalUnfavorableDisplay(useful, text(pattern.ky_than)),
    fiveElements: [
      { name: "Mộc", count: counts.Mộc },
      { name: "Hỏa", count: counts.Hỏa },
      { name: "Thổ", count: counts.Thổ },
      { name: "Kim", count: counts.Kim },
      { name: "Thủy", count: counts.Thủy },
    ],
    tenGods: analyticalTenGods(data),
    hiddenTenGods: analyticalHiddenTenGods(data),
    tenGodsNote:
      String(data.ten_gods?.note || data.ten_gods_result?.note || "").trim() ||
      "Xác định theo quan hệ Ngũ hành và âm dương với Nhật chủ.",
    pillars: PILLAR_META.map((meta) =>
      mapPillar(bazi[meta.field] as PillarDto | undefined, meta, data),
    ),
    shenSha: shenShaEntriesFromAnalysis(data),
    luckStartAge: luck?.start_age != null ? String(luck.start_age) : "",
    luckCurrent: current
      ? [text(current.gan_zhi), current.year_start != null ? `${current.year_start}–${current.year_end}` : ""]
          .filter(Boolean)
          .join(" ")
      : "",
    luckCycles: cycles,
    cungPhi: text(feng.cung_phi || calendar.cung_phi),
    menhQuai: text(feng.menh_quai || calendar.menh_quai),
    nhomTrach: text(feng.nhom_trach || calendar.nhom_trach),
    scoreLabel:
      score.total_score != null && score.grade
        ? `${score.total_score} / ${score.grade}`
        : text(score.grade),
    climateState: canonicalClimateStateLabel(data),
    balancingNeed: canonicalBalancingNeedLabel(data),
    climateEvidence: canonicalTemperatureEvidence(data),
    narrative: buildNarrativeSections(narrative),
    supporting: buildSupportingSections(narrative),
    factsOnly: false,
  };
}

/**
 * True when the model still has the seven narrative sections plus chart detail.
 */
export function isFullCustomerReport(model: FullReportViewModel): boolean {
  return (
    model.factsOnly === false &&
    model.pillars.length === 4 &&
    model.narrative.length === 7 &&
    model.fiveElements.length === 5
  );
}

/**
 * Print/export HTML — structured sections + NarrativeResult + supporting.
 * Never a facts-only dump. Never stale report HTML.
 */
export function renderFullReportHtml(model: FullReportViewModel): string {
  const title = model.customerName ? `Báo cáo Bát Tự — ${model.customerName}` : "Báo cáo Bát Tự";
  return `<!DOCTYPE html><html lang="vi"><head><meta charset="utf-8" /><title>${esc(title)}</title>${reportCss()}</head><body>
<article class="bte-full-report" data-report="canonical-full" data-analysis-id="${esc(model.analysisId)}" data-facts-only="false">
${coverSection(model)}
${section("Thông tin sinh", identityGrid(model))}
${section("Tứ trụ / Bát Tự", pillarTable(model.pillars))}
${section("Nhật chủ · Thân · Cách cục", overviewGrid(model))}
${section(FIVE_ELEMENTS_SECTION_TITLE, elementsList(model))}
${section("Thập thần", godsList(model))}
${section("Dụng thần · Hỷ · Kỵ", godsSupport(model))}
${section("Thần sát", shenShaBlock(model.shenSha))}
${section("Đại vận", luckBlock(model))}
${section("Phong thủy", fengBlock(model))}
${section("Điểm tổng", `<p class="bte-full-metric">${esc(model.scoreLabel || "—")}</p>`)}
${narrativeBlock(model)}
${supportingBlock(model)}
<footer class="bte-full-footer">Mã phân tích ${esc(model.analysisId)}</footer>
</article></body></html>`;
}

function mapPillar(
  pillar: PillarDto | undefined,
  meta: (typeof PILLAR_META)[number],
  data: AnalysisDataDto,
): FullReportPillar {
  const payload =
    asTenGodsPayload(data.ten_gods) ?? asTenGodsPayload(data.ten_gods_result);
  const hidden = hiddenLinesForPillar(payload, meta.key);
  return {
    key: meta.key,
    label: meta.label,
    stem: stemDisplay(text(pillar?.stem), text(pillar?.element)) || text(pillar?.stem),
    branch: text(pillar?.branch),
    napAm: text(pillar?.nap_am),
    hiddenStems: hidden.length
      ? hidden.join(" · ")
      : Array.isArray(pillar?.hidden_stems)
        ? pillar.hidden_stems.filter(Boolean).join(", ")
        : text(pillar?.hidden_stems as unknown as string),
    tenGod: text(pillar?.ten_god),
    growthStage: text(pillar?.truong_sinh),
  };
}

function buildNarrativeSections(
  narrative: NarrativeResultDto | null,
): FullReportNarrativeSection[] {
  const source = hasUsableNarrativeResult(narrative) ? narrative?.sections ?? [] : [];
  return CANONICAL_NARRATIVE_SECTIONS.map((def) => {
    const found = source.find((section) =>
      def.match.test(`${section.id ?? ""} ${section.intent ?? ""} ${section.title ?? ""}`),
    );
    const body = (found?.paragraphs ?? [])
      .map((paragraph) => text(paragraph.text))
      .filter(Boolean)
      .join("\n\n");
    return { id: def.id, title: def.title, body, present: Boolean(body) };
  });
}

function buildSupportingSections(
  narrative: NarrativeResultDto | null,
): FullReportSupportingSection[] {
  if (!hasUsableNarrativeResult(narrative) || !narrative) return [];
  const career = careerSelectionFromNarrative(narrative);
  const items: FullReportSupportingSection[] = [];
  const direction = careerFieldText(career, "career_direction");
  if (direction) {
    items.push({
      id: "career",
      title: "Định hướng nghề nghiệp (hỗ trợ)",
      body: direction,
    });
  }
  return items;
}

function sanitizeAnalysisId(
  raw: string | null | undefined,
  data: AnalysisDataDto,
  input: Record<string, unknown>,
): string {
  const fromOption = text(raw);
  if (fromOption && !STORAGE_ID_RE.test(fromOption)) return fromOption;
  const fromData = text(data.analysis_id || data.request_id);
  if (fromData && !STORAGE_ID_RE.test(fromData)) return fromData;
  return ["bte", input.year || 0, input.month || 0, input.day || 0, input.hour || 0, input.minute || 0]
    .map(String)
    .join("-");
}

function asRecord(value: unknown): Record<string, unknown> {
  return value && typeof value === "object" ? (value as Record<string, unknown>) : {};
}

function text(value: unknown, fallback = ""): string {
  if (value === null || value === undefined || value === "") return fallback;
  const next = String(value).trim();
  return next || fallback;
}

function listText(value: unknown): string {
  if (!Array.isArray(value)) return "";
  return value.map((item) => String(item).trim()).filter(Boolean).join(", ");
}

function solarFromInput(solar: unknown, input: Record<string, unknown>): string {
  if (text(solar)) return text(solar);
  const year = input.year;
  const month = input.month;
  const day = input.day;
  if (year && month && day) {
    return `${pad(Number(day))}/${pad(Number(month))}/${year}`;
  }
  return "";
}

function timeFromInput(input: Record<string, unknown>): string {
  if (input.hour == null) return "";
  return `${pad(Number(input.hour))}:${pad(Number(input.minute || 0))}`;
}

function pad(value: number): string {
  return String(Number.isFinite(value) ? value : 0).padStart(2, "0");
}

function esc(value: string): string {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function section(title: string, body: string): string {
  return `<section class="bte-full-section"><h2>${esc(title)}</h2>${body}</section>`;
}

function coverSection(model: FullReportViewModel): string {
  return `<header class="bte-full-cover">
    <p class="bte-full-kicker">Báo cáo tư vấn Bát Tự</p>
    <h1>${esc(model.customerName || "Khách hàng")}</h1>
    <p>${esc([model.solarDate, model.lunarDate ? `Âm lịch ${model.lunarDate}` : "", model.scoreLabel].filter(Boolean).join(" · "))}</p>
  </header>`;
}

function identityGrid(model: FullReportViewModel): string {
  return `<div class="bte-full-grid">
    ${kv("Dương lịch", model.solarDate)}
    ${kv("Âm lịch", model.lunarDate)}
    ${kv("Giờ sinh", model.birthTime)}
    ${kv("Giới tính", model.gender)}
    ${kv("Nơi sinh", model.birthPlace)}
    ${kv("Múi giờ", model.timezone)}
  </div>`;
}

function overviewGrid(model: FullReportViewModel): string {
  return `<div class="bte-full-grid">
    ${kv("Nhật chủ", [model.dayMaster, model.yinYang, model.dayMasterElement].filter(Boolean).join(" · "))}
    ${kv("Thân", model.strengthLabel)}
    ${kv("Điểm thân", model.strengthScore)}
    ${model.strengthEvidence ? kv("Căn cứ chính", model.strengthEvidence) : ""}
    ${kv("Cách cục", model.pattern)}
    ${model.patternEvidence ? kv("Căn cứ", model.patternEvidence) : ""}
    ${kv("Trạng thái khí hậu", model.climateState)}
    ${kv("Nhu cầu điều hòa", model.balancingNeed)}
    ${model.climateEvidence ? kv("Căn cứ khí hậu", model.climateEvidence) : ""}
  </div>`;
}

function pillarTable(pillars: readonly FullReportPillar[]): string {
  const cols = pillars.map((pillar) => `<th>${esc(pillar.label)}</th>`).join("");
  const row = (label: string, pick: (pillar: FullReportPillar) => string) =>
    `<tr><th scope="row">${esc(label)}</th>${pillars
      .map((pillar) => `<td>${esc(pick(pillar) || "—")}</td>`)
      .join("")}</tr>`;
  return `<div class="bte-full-table-wrap"><table class="bte-full-table">
    <thead><tr><th></th>${cols}</tr></thead>
    <tbody>
      ${row("Thiên can", (pillar) => pillar.stem)}
      ${row("Địa chi", (pillar) => pillar.branch)}
      ${row("Nạp âm", (pillar) => pillar.napAm)}
      ${row("Tàng can", (pillar) => pillar.hiddenStems)}
      ${row("Thập thần", (pillar) => pillar.tenGod)}
      ${row("Trường sinh", (pillar) => pillar.growthStage)}
    </tbody>
  </table></div>`;
}

function elementsList(model: FullReportViewModel): string {
  const total = model.fiveElements.reduce((sum, row) => sum + row.count, 0);
  const list = `<ul class="bte-full-elements">${model.fiveElements
    .map((row) => `<li><span>${esc(row.name)}</span><strong>${row.count}</strong></li>`)
    .join("")}</ul>`;
  return `${list}<p class="bte-full-note">${esc(formatFiveElementsProvenance(total))}</p>`;
}

function godsList(model: FullReportViewModel): string {
  const visible = model.tenGods.join(" · ");
  const hidden = model.hiddenTenGods.join(" · ");
  if (!visible && !hidden) return `<p class="bte-full-empty">Chưa có thập thần hiển thị.</p>`;
  return `<div>
    <p><strong>Lộ can</strong> ${esc(visible || "—")}</p>
    <p><strong>Tàng can</strong> ${esc(hidden || "—")}</p>
    <p class="bte-full-note">${esc(model.tenGodsNote)}</p>
  </div>`;
}

function godsSupport(model: FullReportViewModel): string {
  return `<div class="bte-full-grid">
    ${kv("Dụng thần", model.usefulGod)}
    ${kv("Hỷ thần", model.hyThan)}
    ${kv("Kỵ thần", model.kyThan)}
  </div>`;
}

function bulletList(items: readonly string[], empty: string): string {
  if (!items.length) return `<p class="bte-full-empty">${esc(empty)}</p>`;
  return `<ul>${items.map((item) => `<li>${esc(item)}</li>`).join("")}</ul>`;
}

function shenShaBlock(items: readonly ShenShaEntryView[]): string {
  if (!items.length) {
    return `<p class="bte-full-empty">Chưa có thần sát trên lá số này.</p>`;
  }
  return `<ul>${items
    .map((item) => {
      const evidence = item.evidence ? ` · Căn cứ: ${item.evidence}` : "";
      return `<li><strong>${esc(item.name)}</strong> — ${esc(item.presence)}${esc(evidence)}</li>`;
    })
    .join("")}</ul>`;
}

function luckBlock(model: FullReportViewModel): string {
  const head = `<p>Tuổi khởi Đại vận: <strong>${esc(model.luckStartAge || "—")}</strong>. Hiện tại: <strong>${esc(model.luckCurrent || "—")}</strong>.</p>`;
  if (!model.luckCycles.length) return head;
  return `${head}<ol class="bte-full-luck">${model.luckCycles
    .map(
      (cycle) =>
        `<li${cycle.current ? ' data-current="true"' : ""}>${esc(cycle.label)} ${esc(cycle.years)}${cycle.current ? " (hiện tại)" : ""}</li>`,
    )
    .join("")}</ol>`;
}

function fengBlock(model: FullReportViewModel): string {
  return `<div class="bte-full-grid">
    ${kv("Cung Phi", model.cungPhi)}
    ${kv("Mệnh Quái", model.menhQuai)}
    ${kv("Nhóm Trạch", model.nhomTrach)}
  </div>`;
}

function narrativeBlock(model: FullReportViewModel): string {
  return `<section class="bte-full-narrative" data-narrative="pack05">
    <h2>Luận giải</h2>
    ${model.narrative
      .map(
        (sectionItem) =>
          `<section class="bte-full-narrative__section" data-narrative-id="${esc(sectionItem.id)}">
            <h3>${esc(sectionItem.title)}</h3>
            <p>${esc(sectionItem.body || "—")}</p>
          </section>`,
      )
      .join("")}
  </section>`;
}

function supportingBlock(model: FullReportViewModel): string {
  if (!model.supporting.length) return "";
  return model.supporting
    .map((item) => section(item.title, `<p>${esc(item.body)}</p>`))
    .join("");
}

function kv(label: string, value: string): string {
  return `<div class="bte-full-kv"><span>${esc(label)}</span><strong>${esc(value || "—")}</strong></div>`;
}

function reportCss(): string {
  return `<style>
    body{font-family:"Segoe UI",system-ui,sans-serif;color:#1c2430;margin:0;background:#f7f5f2;}
    .bte-full-report{max-width:960px;margin:0 auto;padding:32px 24px 64px;}
    .bte-full-cover{margin-bottom:28px;}
    .bte-full-kicker{letter-spacing:.08em;text-transform:uppercase;font-size:12px;opacity:.7;}
    h1{font-size:28px;margin:4px 0 8px;}
    h2{font-size:18px;margin:0 0 12px;}
    h3{font-size:16px;margin:0 0 8px;}
    .bte-full-section,.bte-full-narrative{background:#fff;border:1px solid #d7e0ea;border-radius:14px;padding:16px 18px;margin:0 0 14px;}
    .bte-full-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;}
    .bte-full-kv{background:#f4f7f7;border-radius:10px;padding:10px 12px;}
    .bte-full-kv span{display:block;font-size:12px;opacity:.7;margin-bottom:4px;}
    .bte-full-table{width:100%;border-collapse:collapse;font-size:14px;}
    .bte-full-table th,.bte-full-table td{border:1px solid #d7e0ea;padding:8px;text-align:center;}
    .bte-full-table th[scope=row]{text-align:left;background:#f4f7f7;}
    .bte-full-elements{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;list-style:none;padding:0;margin:0;}
    .bte-full-elements li{background:#f4f7f7;border-radius:10px;padding:10px;text-align:center;}
    .bte-full-luck{columns:2;padding-left:18px;}
    .bte-full-luck li[data-current="true"]{font-weight:700;}
    .bte-full-narrative__section{margin:0 0 16px;}
    .bte-full-footer{margin-top:24px;font-size:12px;opacity:.65;}
    .bte-full-empty,.bte-full-metric{margin:0;}
    @media print{
      body{background:#fff;}
      .bte-full-cover,.bte-full-section,.bte-full-narrative{break-inside:avoid;page-break-inside:avoid;}
      .bte-full-narrative{page-break-before:always;}
    }
  </style>`;
}
