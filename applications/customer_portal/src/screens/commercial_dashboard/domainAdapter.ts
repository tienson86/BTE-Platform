/**
 * Bind Domain Interpretation customer labels. Copy only; no composer.
 */

import type { AnalysisDataDto, DomainInterpretationSummaryDto, DomainSummaryDto } from "../../models";
import { DOMAIN_PILLARS_TITLE, DOMAIN_UNRESOLVED_COPY } from "./cards";
import type {
  DomainDimensionView,
  DomainPillarView,
  DomainSummaryView,
  InterpretationView,
  OverviewView,
} from "./types";

const TECHNICAL = /TR-P7-|E-DI-|mingju_result_id|_mc01/;

function text(value: unknown): string {
  if (typeof value !== "string") return "";
  return value.trim();
}

function clean(value: unknown): string {
  const next = text(value);
  if (!next || TECHNICAL.test(next)) return "";
  return next;
}

function asRecord(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)) return {};
  return value as Record<string, unknown>;
}

/**
 * Map published `data.domains` onto compact pillar views.
 */
export function adaptDomainInterpretation(
  data: AnalysisDataDto | null | undefined,
): { readonly title: string; readonly items: readonly DomainPillarView[] } {
  const block = (data?.domains ?? null) as DomainInterpretationSummaryDto | null;
  if (!block || typeof block !== "object") {
    return { title: "", items: [] };
  }
  const items = (block.items ?? [])
    .map((item) => pillar(item))
    .filter((item): item is DomainPillarView => item != null);
  if (!items.length) return { title: "", items: [] };
  return {
    title: clean(block.title) || DOMAIN_PILLARS_TITLE,
    items,
  };
}

/**
 * Overview chips: name + state only.
 */
export function adaptDomainSummary(
  data: AnalysisDataDto | null | undefined,
): { readonly title: string; readonly items: readonly DomainSummaryView[] } {
  const adapted = adaptDomainInterpretation(data);
  return {
    title: adapted.title,
    items: adapted.items.map((item) => ({
      id: item.id,
      title: item.title,
      stateLabel: item.stateLabel,
    })),
  };
}

export function attachOverviewDomains(
  overview: OverviewView,
  data: AnalysisDataDto | null | undefined,
): OverviewView {
  const domains = adaptDomainSummary(data);
  return {
    ...overview,
    domainTitle: domains.title,
    domains: domains.items,
  };
}

export function attachInterpretationDomains(
  interpretation: InterpretationView,
  data: AnalysisDataDto | null | undefined,
): InterpretationView {
  const domains = adaptDomainInterpretation(data);
  const available = interpretation.available || domains.items.length > 0;
  return {
    ...interpretation,
    domainTitle: domains.title,
    domains: domains.items,
    available,
  };
}

function pillar(raw: DomainSummaryDto): DomainPillarView | null {
  const id = clean(raw.id);
  const title = clean(raw.title);
  if (!id || !title) return null;
  const unresolved = Boolean(raw.unresolved);
  const summary = unresolved ? DOMAIN_UNRESOLVED_COPY : clean(raw.summary) || DOMAIN_UNRESOLVED_COPY;
  return {
    id,
    title,
    state: clean(raw.state),
    stateLabel: clean(raw.state_label),
    driver: unresolved ? "" : clean(raw.driver),
    support: unresolved ? "" : clean(raw.support),
    bottleneck: unresolved ? "" : clean(raw.bottleneck),
    opportunity: unresolved ? "" : clean(raw.opportunity),
    caution: unresolved ? "" : clean(raw.caution),
    condition: unresolved ? "" : clean(raw.condition),
    confidence: unresolved ? "" : clean(raw.confidence),
    summary,
    dimensions: dimensions(raw),
    unresolved,
  };
}

function dimensions(raw: DomainSummaryDto): readonly DomainDimensionView[] {
  const items: DomainDimensionView[] = [];
  for (const item of raw.dimensions ?? []) {
    const label = clean(asRecord(item).label);
    const value = clean(asRecord(item).value);
    if (!label || !value) continue;
    items.push({ label, value });
  }
  return items;
}
