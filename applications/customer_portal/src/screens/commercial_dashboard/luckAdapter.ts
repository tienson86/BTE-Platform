/**
 * Bind Luck Card from canonical analysis. Copy published cycles only.
 */

import { stripInternalRuleIds } from "../../adapters/customerFacingPresentation";
import type {
  AnalysisDataDto,
  LuckActivationDto,
  LuckCycleDto,
  LuckDto,
  LuckInteractionDto,
} from "../../models";
import { LUCK_TITLE } from "./cards";
import type {
  LuckActivationItemView,
  LuckActivationView,
  LuckCycleView,
  LuckInteractionEdgeView,
  LuckInteractionView,
  LuckView,
} from "./types";

const TECHNICAL_TOKEN = /^[a-z][a-z0-9_]*$/;
const TRUSTED_DIRECTION = new Set(["Thuận", "Nghịch"]);
const CUSTOMER_TREND_KEYS = ["customer_summary", "trend"] as const;
const JSONISH = /^\s*[{\[]/;
const RUNTIME_LEAK =
  /dayun_runtime|runtime_metadata|attack_elements|support_elements|luck_strength|"evaluation"|hidden_stems|luck_stage|liunian_runtime/i;
const BLOCKED_TREND = /Lưu Niên|lưu nguyệt|cưới|phát tài|tai họa|bệnh tật|kiện tụng|Đại hung|đại cát|thăng chức|chia tay|sẽ bệnh|sẽ thành công/i;

function text(value: unknown): string {
  if (typeof value === "string") return value.trim();
  if (typeof value === "number" && Number.isFinite(value)) return String(value);
  return "";
}

function customerLabel(value: string): string {
  const next = text(value);
  if (!next || TECHNICAL_TOKEN.test(next)) return "";
  return next;
}

function customerSentence(value: unknown): string {
  if (typeof value !== "string") return "";
  const next = customerLabel(stripInternalRuleIds(value));
  if (!next || JSONISH.test(next) || RUNTIME_LEAK.test(next) || BLOCKED_TREND.test(next)) {
    return "";
  }
  return next;
}

function numeric(value: unknown): number | null {
  if (typeof value === "number" && Number.isFinite(value)) return value;
  if (typeof value === "string" && value.trim() && Number.isFinite(Number(value))) {
    return Number(value);
  }
  return null;
}

function yearRange(start: unknown, end: unknown): string {
  const from = numeric(start);
  const to = numeric(end);
  if (from == null || to == null) return "";
  return `${from}–${to}`;
}

function ageRange(start: unknown, end: unknown): string {
  const from = numeric(start);
  const to = numeric(end);
  if (from == null || to == null) return "";
  return `${from}–${to} tuổi`;
}

function copyCycle(cycle: LuckCycleDto | null | undefined, isCurrent: boolean): LuckCycleView | null {
  if (!cycle) return null;
  const ganZhi = customerLabel(text(cycle.gan_zhi));
  if (!ganZhi) return null;
  return {
    ganZhi,
    yearRange: yearRange(cycle.year_start, cycle.year_end),
    ageRange: ageRange(cycle.age_start, cycle.age_end),
    isCurrent,
  };
}

function copyDirection(luck: LuckDto): string {
  const label = customerLabel(text(luck.direction_label) || text(luck.direction));
  return TRUSTED_DIRECTION.has(label) ? label : "";
}

function copyStartAge(luck: LuckDto): string {
  const age = numeric(luck.start_age);
  if (age == null) return "";
  return `${age} tuổi`;
}

function copyTrend(luck: LuckDto): string {
  const row = luck as LuckDto & Record<string, unknown>;
  for (const key of CUSTOMER_TREND_KEYS) {
    const value = customerSentence(row[key]);
    if (value) return value;
  }
  return "";
}

function currentIndex(cycles: readonly LuckCycleDto[], current: LuckCycleDto | null): number {
  if (!current) return -1;
  const ganZhi = customerLabel(text(current.gan_zhi));
  if (ganZhi) {
    const byName = cycles.findIndex((cycle) => customerLabel(text(cycle.gan_zhi)) === ganZhi);
    if (byName >= 0) return byName;
  }
  if (current.index != null) {
    const byIndex = cycles.findIndex((cycle) => cycle.index === current.index);
    if (byIndex >= 0) return byIndex;
    if (current.index >= 0 && current.index < cycles.length) return current.index;
  }
  return -1;
}

/**
 * Copy canonical Đại Vận cycles into the Card view. Does not calculate vận.
 */
export function adaptLuckCard(data: AnalysisDataDto | null | undefined): LuckView {
  const luck = data?.luck;
  const published = luck?.cycles ?? [];
  const currentSource = luck?.current_cycle ?? null;
  const active = currentIndex(published, currentSource);
  const cycles = published
    .map((cycle, index) => copyCycle(cycle, index === active))
    .filter((cycle): cycle is LuckCycleView => Boolean(cycle));
  const current =
    (active >= 0 ? cycles[active] : null) || (active < 0 ? copyCycle(currentSource, true) : null);
  const next = active >= 0 && active + 1 < cycles.length ? cycles[active + 1] : null;
  return {
    title: LUCK_TITLE,
    available: cycles.length > 0 || Boolean(current),
    current,
    direction: luck ? copyDirection(luck) : "",
    startAge: luck ? copyStartAge(luck) : "",
    cycles,
    next,
    trend: luck ? copyTrend(luck) : "",
    activation: luck ? copyActivation(luck.activation) : null,
    interaction: luck ? copyInteraction(luck.interaction) : null,
  };
}

function copyActivation(raw: LuckActivationDto | null | undefined): LuckActivationView | null {
  if (!raw || !Array.isArray(raw.items) || raw.items.length === 0) return null;
  const items: LuckActivationItemView[] = [];
  for (const item of raw.items) {
    const id = text(item.id);
    const title = customerLabel(text(item.title));
    if (!id || !title) continue;
    const conditions = (item.conditions ?? [])
      .map((row) => customerSentence(row))
      .filter((row): row is string => Boolean(row));
    items.push({
      id,
      title,
      state: text(item.state),
      stateLabel: customerLabel(text(item.state_label) || text(item.state)),
      driver: customerLabel(text(item.driver)),
      marker: customerLabel(text(item.marker)),
      bottleneck: customerLabel(text(item.bottleneck)),
      conditions,
    });
  }
  if (!items.length) return null;
  return {
    title: customerLabel(text(raw.title)) || "Kích hoạt vận hiện tại",
    timeWindow: text(raw.time_window),
    ganZhi: customerLabel(text(raw.gan_zhi)),
    items,
  };
}

function copyInteraction(raw: LuckInteractionDto | null | undefined): LuckInteractionView | null {
  if (!raw) return null;
  const edges: LuckInteractionEdgeView[] = [];
  for (const item of raw.edges ?? []) {
    const source = customerLabel(text(item.source));
    const target = customerLabel(text(item.target));
    const type = customerLabel(text(item.type));
    if (!source || !target || !type) continue;
    edges.push({
      source,
      target,
      type,
      explanation: customerSentence(item.explanation),
      condition: customerSentence(item.condition),
    });
  }
  const situation = customerLabel(text(raw.situation));
  const driver = customerLabel(text(raw.driver));
  const bottleneck = customerLabel(text(raw.bottleneck));
  const opportunity = customerSentence(raw.opportunity);
  const risk = customerSentence(raw.risk);
  if (!situation && !driver && !bottleneck && !opportunity && !risk && !edges.length) {
    return null;
  }
  return {
    title: customerLabel(text(raw.title)) || "Tương tác vận hiện tại",
    situation,
    driver,
    bottleneck,
    opportunity,
    risk,
    edges,
  };
}
