/**
 * Customer-facing presentation helpers.
 * Does not recalculate Strength, Pattern, Temperature, Ten Gods, or ShenSha.
 */

import type { AnalysisDataDto, ShenShaMatchDto } from "../models";
import { canonicalStrengthEvidence } from "./canonicalStrength";
import { canonicalPatternEvidence, canonicalPatternLabel } from "./canonicalPattern";
import {
  canonicalBalancingNeedLabel,
  canonicalClimateStateLabel,
  canonicalTemperatureEvidence,
} from "./canonicalTemperature";
import {
  asTenGodsPayload,
  type TenGodEntry,
  type TenGodsPayload,
} from "./tenGodsDisplay";

export const PROMINENCE_VISIBLE = "Lộ rõ";
export const PROMINENCE_HIDDEN_STRONG = "Ẩn nổi bật";
export const PROMINENCE_HIDDEN = "Có ẩn";
export const PROMINENCE_ABSENT = "Không hiện";

export const SHENSHA_PROMINENT = "Nổi bật";

const FEATURED_LIMIT = 5;
const FEATURED_MIN = 3;
const HIDDEN_STRONG_COUNT = 3;
const HIDDEN_REPEAT_COUNT = 2;

const RULE_PHRASE_RE = /(?:^|\s|[·|,;])rule\s+[a-z][a-z0-9_]{1,40}/gi;
const INTERNAL_ID_RE =
  /\b(?:cli|com_san|pat|str|sea|tmp|flo|flw|ctl|sup|spc|cmb|root)_[a-z0-9_]+\b/gi;
const SCORE_SUFFIX_RE = /\s+[+\-]?\d+(?:\.\d+)?\s*$/;
const SEPARATOR_RE = /\s*[·|,;]\s*/;

const PILLAR_LABELS: Record<string, string> = {
  year: "Năm",
  month: "Tháng",
  day: "Ngày",
  hour: "Giờ",
};

const SEASON_LABELS: Record<string, string> = {
  spring: "Xuân",
  summer: "Hạ",
  autumn: "Thu",
  fall: "Thu",
  winter: "Đông",
};

const DAY_MASTER_LABELS = new Set(["nhật chủ", "nhat chu", "day_master"]);

export type TenGodProminenceItem = {
  readonly name: string;
  readonly klass: string;
  readonly evidence: string;
  readonly visibleCount: number;
  readonly hiddenCount: number;
  readonly totalCount: number;
  readonly pillarSpread: number;
};

export type TenGodsProminenceSummary = {
  readonly featured: readonly TenGodProminenceItem[];
  readonly others: readonly TenGodProminenceItem[];
  readonly othersLine: string;
  readonly all: readonly TenGodProminenceItem[];
};

/**
 * Remove internal rule tokens from customer-facing copy.
 */
export function stripInternalRuleIds(text: string): string {
  if (!text) return "";
  let cleaned = text.replace(RULE_PHRASE_RE, " ");
  cleaned = cleaned.replace(INTERNAL_ID_RE, " ");
  return collapseSeparators(cleaned);
}

/**
 * True when customer copy still contains an internal rule token.
 */
export function hasInternalRuleId(text: string): boolean {
  if (!text) return false;
  RULE_PHRASE_RE.lastIndex = 0;
  INTERNAL_ID_RE.lastIndex = 0;
  return RULE_PHRASE_RE.test(text) || INTERNAL_ID_RE.test(text);
}

/**
 * Natural-language Strength summary from canonical evidence. Not raw ±scores.
 */
export function strengthCustomerSummary(data: AnalysisDataDto): string {
  const evidence = canonicalStrengthEvidence(data);
  const parts = splitEvidence(evidence).map(stripScoreSuffix).filter(Boolean);
  if (!parts.length) return "";
  const monthBranch = monthBranchOf(data);
  const level = String(data.strength?.strength_level || "").toLowerCase();
  const weak = level === "weak" || Number(data.strength?.strength_score) < 0.4;
  const phrases: string[] = [];
  const used = new Set<number>();

  if (hasReason(parts, /vô căn/i)) {
    phrases.push("Vô căn");
    markUsed(parts, used, /vô căn/i);
  }

  const rest = hasReason(parts, /hưu khí theo tháng/i);
  const wang = hasReason(parts, /tướng địa theo tháng|vượng địa theo tháng/i);
  if (rest) {
    phrases.push(monthBranch ? `sinh tháng ${monthBranch}` : "Hưu khí theo tháng");
    markUsed(parts, used, /hưu khí theo tháng/i);
  } else if (wang) {
    phrases.push(
      monthBranch ? `Tướng địa theo tháng ${monthBranch}` : "Tướng địa theo tháng",
    );
    markUsed(parts, used, /tướng địa theo tháng|vượng địa theo tháng/i);
  }

  if (!hasReason(parts, /vô căn/i) && hasReason(parts, /căn khí|căn tàng/i)) {
    phrases.push("có căn khí");
    markUsed(parts, used, /căn khí|căn tàng/i);
  }

  const drainHeavy = hasReason(parts, /tiết khí nặng/i) || countReason(parts, /thực thương|thương quan|tiết khí/i) >= 2;
  if (hasReason(parts, /thực thương|thương quan|tiết khí/i)) {
    phrases.push(drainHeavy ? "Thực Thương tiết khí mạnh" : "Thực Thương tiết khí");
    markUsed(parts, used, /thực thương|thương quan|tiết khí/i);
  }

  if (hasReason(parts, /quan sát|thất sát|chính quan/i)) {
    phrases.push("Quan Sát gây áp lực");
    markUsed(parts, used, /quan sát|thất sát|chính quan/i);
  }

  const hasSupport = hasReason(parts, /ấn tinh|chính ấn|tỷ kiên|đồng hành|kiếp tài|trợ thân|trợ lực/i);
  if (hasSupport) {
    markUsed(parts, used, /ấn tinh|chính ấn|tỷ kiên|đồng hành|kiếp tài|trợ thân|trợ lực/i);
    phrases.push(weak ? "có sinh trợ nhưng không đủ cân lại" : "có sinh trợ");
  }

  if (hasReason(parts, /ấn mùa lạnh/i)) {
    phrases.push("Ấn mùa lạnh");
    markUsed(parts, used, /ấn mùa lạnh/i);
  }

  for (const [index, part] of parts.entries()) {
    if (used.has(index)) continue;
    phrases.push(part);
  }
  return phrases.join(" · ");
}

/**
 * Pattern evidence without internal rule IDs.
 */
export function patternCustomerEvidence(data: AnalysisDataDto): string {
  return stripInternalRuleIds(canonicalPatternEvidence(data));
}

/**
 * Pattern headline plus one short evidence line.
 */
export function patternCustomerLine(data: AnalysisDataDto): string {
  const label = canonicalPatternLabel(data);
  const evidence = patternCustomerEvidence(data);
  if (label && evidence) return `${label}. ${evidence}`;
  return label || evidence;
}

/**
 * Climate evidence as a short customer sentence. Not Overall Useful God.
 */
export function temperatureCustomerEvidence(data: AnalysisDataDto): string {
  const compact = stripInternalRuleIds(canonicalTemperatureEvidence(data));
  const branch = pickMonthToken(compact, /nguyệt lệnh\s+(\S+)/i) || monthBranchOf(data);
  const season =
    pickMonthToken(compact, /mùa\s+(\S+)/i) ||
    seasonLabelOf(data);
  const climate =
    pickMonthToken(compact, /khí hậu\s+(\S+)/i) || canonicalClimateStateLabel(data);
  if (branch && climate) {
    const climateBit = season
      ? `khí mùa ${season} thiên ${climate.toLowerCase()}`
      : `khí hậu ${climate.toLowerCase()}`;
    return `Sinh tháng ${branch}, ${climateBit}.`;
  }
  return dropDuplicateNeed(compact, canonicalBalancingNeedLabel(data));
}

/**
 * Điều hậu customer line: climate + balancing need + short evidence.
 */
export function temperatureCustomerLine(data: AnalysisDataDto): string {
  const climate = canonicalClimateStateLabel(data);
  const need = canonicalBalancingNeedLabel(data);
  const evidence = temperatureCustomerEvidence(data);
  const head = [climate, need].filter(Boolean).join(" · ");
  if (head && evidence) return `${head}. ${evidence}`;
  return head || evidence;
}

/**
 * Deterministic Ten Gods prominence from canonical visible + hidden entries.
 */
export function buildTenGodsProminence(
  payload: TenGodsPayload | null | undefined,
  dayMasterStem: string = "",
): TenGodsProminenceSummary {
  const visible = entriesOf(payload?.visible).filter(
    (item) => !isDayMasterVisible(item, dayMasterStem),
  );
  const hidden = entriesOf(payload?.hidden);
  const names = unique([
    ...visible.map((item) => tenGodName(item)),
    ...hidden.map((item) => tenGodName(item)),
  ]).filter((name) => name && !isDayMasterLabel(name));

  const all = names
    .map((name) => rankOneGod(name, visible, hidden))
    .sort(compareProminence);
  const featured = pickFeatured(all);
  const featuredNames = new Set(featured.map((item) => item.name));
  const others = all.filter((item) => !featuredNames.has(item.name));
  return {
    featured,
    others,
    othersLine: others.length ? `Các thần khác: ${others.map((item) => item.name).join(" · ")}` : "",
    all,
  };
}

/**
 * Prominence from an analysis payload. Keeps full canonical arrays untouched.
 */
export function tenGodsProminenceFromAnalysis(
  data: AnalysisDataDto,
): TenGodsProminenceSummary {
  const payload =
    asTenGodsPayload(data.ten_gods) ?? asTenGodsPayload(data.ten_gods_result);
  return buildTenGodsProminence(payload, String(data.bazi?.day_master || ""));
}

/**
 * Customer ShenSha line from canonical occurrences. Does not invent stars.
 */
export function formatShenShaCustomer(match: ShenShaMatchDto): {
  readonly id: string;
  readonly name: string;
  readonly presence: string;
  readonly evidence: string;
} {
  const name = String(match.canonical_name || match.name || "").trim();
  const pillars = unique(
    (match.occurrences ?? [])
      .map((item) => String(item.pillar || "").trim())
      .filter(Boolean),
  );
  const labels = pillars.map(pillarLabel).filter(Boolean);
  const prominent = labels.length >= 2;
  const location = labels.length
    ? `Có tại trụ ${labels.join(" · ")}`
    : stripInternalRuleIds(String(match.evidence_text || "").trim());
  return {
    id: String(match.id || name),
    name,
    presence: prominent ? SHENSHA_PROMINENT : "Có",
    evidence: location,
  };
}

function entriesOf(items: readonly (string | TenGodEntry)[] | undefined): TenGodEntry[] {
  if (!items) return [];
  return items
    .map((item) => (typeof item === "string" ? { ten_god: item } : item))
    .filter((item) => Boolean(item && tenGodName(item)));
}

function rankOneGod(
  name: string,
  visible: readonly TenGodEntry[],
  hidden: readonly TenGodEntry[],
): TenGodProminenceItem {
  const vis = visible.filter((item) => tenGodName(item) === name);
  const hid = hidden.filter((item) => tenGodName(item) === name);
  const pillars = unique([
    ...vis.map((item) => String(item.pillar || "")),
    ...hid.map((item) => String(item.pillar || "")),
  ]).filter(Boolean);
  const visibleCount = vis.length;
  const hiddenCount = hid.length;
  const klass = classifyProminence(visibleCount, hiddenCount, pillars.length);
  return {
    name,
    klass,
    evidence: prominenceEvidence(name, vis, hid, klass),
    visibleCount,
    hiddenCount,
    totalCount: visibleCount + hiddenCount,
    pillarSpread: pillars.length,
  };
}

function classifyProminence(
  visibleCount: number,
  hiddenCount: number,
  pillarSpread: number,
): string {
  if (visibleCount >= 1) return PROMINENCE_VISIBLE;
  if (
    hiddenCount >= HIDDEN_STRONG_COUNT ||
    (hiddenCount >= HIDDEN_REPEAT_COUNT && pillarSpread >= 2)
  ) {
    return PROMINENCE_HIDDEN_STRONG;
  }
  if (hiddenCount >= 1) return PROMINENCE_HIDDEN;
  return PROMINENCE_ABSENT;
}

function compareProminence(a: TenGodProminenceItem, b: TenGodProminenceItem): number {
  const score = (item: TenGodProminenceItem): number =>
    item.visibleCount * 100 +
    (item.klass === PROMINENCE_HIDDEN_STRONG ? 50 : 0) +
    item.hiddenCount * 10 +
    item.pillarSpread;
  return score(b) - score(a) || a.name.localeCompare(b.name, "vi");
}

function pickFeatured(all: readonly TenGodProminenceItem[]): TenGodProminenceItem[] {
  const primary = all.filter(
    (item) => item.klass === PROMINENCE_VISIBLE || item.klass === PROMINENCE_HIDDEN_STRONG,
  );
  const picked = [...primary.slice(0, FEATURED_LIMIT)];
  if (picked.length < FEATURED_MIN) {
    for (const item of all) {
      if (picked.length >= FEATURED_MIN) break;
      if (!picked.includes(item) && item.klass === PROMINENCE_HIDDEN) {
        picked.push(item);
      }
    }
  }
  return picked.slice(0, FEATURED_LIMIT);
}

function prominenceEvidence(
  name: string,
  visible: readonly TenGodEntry[],
  hidden: readonly TenGodEntry[],
  klass: string,
): string {
  if (klass === PROMINENCE_VISIBLE) {
    const stem = firstStem(visible);
    const where = visible.map((item) => `trụ ${pillarLabel(item.pillar)}`).filter((part) => !part.endsWith(" "));
    const uniqueWhere = unique(where);
    if (name === "Tỷ Kiên") {
      return stem ? `${stem} xuất hiện ngoài Nhật can` : "Xuất hiện ngoài Nhật can";
    }
    const visibleBit = stem
      ? `${stem} lộ ${uniqueWhere.join(" · ") || "trụ"}`
      : uniqueWhere.join(" · ");
    if (hidden.length) return `${visibleBit}, đồng thời có tàng`;
    return visibleBit;
  }
  const stem = firstStem(hidden);
  const branches = hidden.map((item) => String(item.branch || "").trim()).filter(Boolean);
  const uniqueBranches = unique(branches);
  if (stem && uniqueBranches.length === 1 && hidden.length >= 2) {
    return `${stem} xuất hiện tại ${hidden.length} chi ${uniqueBranches[0]}`;
  }
  const pillars = unique(hidden.map((item) => pillarLabel(item.pillar))).filter(Boolean);
  if (stem && pillars.length) {
    return hidden.length >= 2
      ? `${stem} xuất hiện lặp trong tàng can (${pillars.join(" · ")})`
      : `${stem} tàng trụ ${pillars[0]}`;
  }
  return hidden.length ? "Có tàng can" : "";
}

function isDayMasterVisible(item: TenGodEntry, dayMasterStem: string): boolean {
  if (String(item.pillar || "") === "day") return true;
  if (isDayMasterLabel(tenGodName(item))) return true;
  if (String(item.god_id || "") === "day_master") return true;
  if (dayMasterStem && String(item.stem || "") === dayMasterStem && item.pillar === "day") {
    return true;
  }
  return false;
}

function isDayMasterLabel(name: string): boolean {
  return DAY_MASTER_LABELS.has(name.trim().toLowerCase());
}

function tenGodName(item: TenGodEntry): string {
  return String(item.ten_god || item.display || "").trim();
}

function firstStem(items: readonly TenGodEntry[]): string {
  for (const item of items) {
    const stem = String(item.stem || item.hidden_stem || "").trim();
    if (stem) return stem;
  }
  return "";
}

function pillarLabel(pillar: string | undefined): string {
  const key = String(pillar || "").trim();
  return PILLAR_LABELS[key] || key;
}

function monthBranchOf(data: AnalysisDataDto): string {
  const pattern = data.pattern as { month_branch?: unknown } | undefined;
  const temperature = data.temperature as { month_branch?: unknown } | undefined;
  return String(
    pattern?.month_branch ||
      temperature?.month_branch ||
      data.bazi?.month_pillar?.branch ||
      "",
  ).trim();
}

function seasonLabelOf(data: AnalysisDataDto): string {
  const temperature = data.temperature as { season?: unknown; season_label?: unknown } | undefined;
  const labeled = String(temperature?.season_label || "").trim();
  if (labeled) return labeled;
  const season = String(temperature?.season || "").trim().toLowerCase();
  return SEASON_LABELS[season] || "";
}

function splitEvidence(text: string): string[] {
  return text
    .split(/\s·\s|[.;\n]+/)
    .map((part) => part.trim())
    .filter(Boolean);
}

function stripScoreSuffix(text: string): string {
  return text.replace(SCORE_SUFFIX_RE, "").trim();
}

function hasReason(parts: readonly string[], pattern: RegExp): boolean {
  return parts.some((part) => pattern.test(part));
}

function countReason(parts: readonly string[], pattern: RegExp): number {
  return parts.filter((part) => pattern.test(part)).length;
}

function markUsed(parts: readonly string[], used: Set<number>, pattern: RegExp): void {
  parts.forEach((part, index) => {
    if (pattern.test(part)) used.add(index);
  });
}

function pickMonthToken(text: string, pattern: RegExp): string {
  const match = text.match(pattern);
  return match?.[1] ? match[1].replace(/[.,;]+$/, "") : "";
}

function dropDuplicateNeed(text: string, need: string): string {
  if (!need) return text;
  return collapseSeparators(text.replace(need, " "));
}

function collapseSeparators(text: string): string {
  return text
    .split(SEPARATOR_RE)
    .map((part) => part.trim())
    .filter(Boolean)
    .join(" · ")
    .replace(/\s{2,}/g, " ")
    .trim();
}

function unique(values: readonly string[]): string[] {
  return [...new Set(values)];
}
