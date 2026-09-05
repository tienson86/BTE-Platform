/**
 * Bind Pack 07 Narrative Composer compact into the existing interpretation card.
 * Copy only. Returns null when the compact is absent so UI-11 stays on the old path.
 */

import type { AnalysisDataDto } from "../../models";
import { INTERPRETATION_EMPTY, INTERPRETATION_TITLE } from "./cards";
import type {
  InterpretationView,
  Pack07NarrativeComposerView,
  Pack07NarrativeDomainView,
  Pack07NarrativeItemView,
} from "./types";

const TECHNICAL = /TR-P7-|E-DI-|mingju_result_id|_mc01|0x[0-9a-f]/i;

function text(value: unknown): string {
  if (typeof value !== "string") return "";
  const next = value.trim();
  if (!next || TECHNICAL.test(next)) return "";
  return next;
}

function asRecord(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)) return {};
  return value as Record<string, unknown>;
}

function asList(value: unknown): readonly Record<string, unknown>[] {
  if (!Array.isArray(value)) return [];
  return value.filter((item): item is Record<string, unknown> => Boolean(item) && typeof item === "object");
}

function item(value: Record<string, unknown>): Pack07NarrativeItemView | null {
  const summary = text(value.summary);
  const title = text(value.title);
  if (!summary && !title) return null;
  return {
    title,
    summary,
    domain: text(value.domain),
    priority: text(value.priority),
  };
}

function domain(value: Record<string, unknown>): Pack07NarrativeDomainView | null {
  const id = text(value.id);
  const title = text(value.title);
  if (!id && !title) return null;
  return {
    id,
    title,
    summary: text(value.summary),
    state: text(value.state),
    driver: text(value.driver),
    bottleneck: text(value.bottleneck),
    opportunity: text(value.opportunity),
    caution: text(value.caution),
    condition: text(value.condition),
  };
}

function labels(raw: Record<string, unknown>): Pack07NarrativeComposerView["labels"] {
  const fields = asRecord(raw.fields);
  return {
    executive: text(raw.executive) || "Tóm tắt",
    strengths: text(raw.strengths) || "Điểm mạnh",
    risks: text(raw.risks) || "Rủi ro",
    opportunities: text(raw.opportunities) || "Cơ hội",
    domains: text(raw.domains) || "Sáu trụ cột",
    luck: text(raw.luck) || "Vận hiện tại",
    actions: text(raw.actions) || "Việc ưu tiên",
    closing: text(raw.closing) || "Kết luận",
    fields: {
      state: text(fields.state) || "Hiện trạng",
      driver: text(fields.driver) || "Động lực",
      bottleneck: text(fields.bottleneck) || "Điểm nghẽn",
      opportunity: text(fields.opportunity) || "Cơ hội",
      caution: text(fields.caution) || "Lưu ý",
      condition: text(fields.condition) || "Điều kiện",
    },
  };
}

/**
 * Map published `data.detailed_narrative` onto InterpretationView. Null when missing.
 */
export function adaptPack07Narrative(
  data: AnalysisDataDto | null | undefined,
): InterpretationView | null {
  const block = asRecord(data?.detailed_narrative);
  if (!Object.keys(block).length) return null;
  const executive = text(block.executive);
  const closing = text(block.closing);
  const strengths = asList(block.strengths).map(item).filter((entry): entry is Pack07NarrativeItemView => entry != null);
  const risks = asList(block.risks).map(item).filter((entry): entry is Pack07NarrativeItemView => entry != null);
  const opportunities = asList(block.opportunities)
    .map(item)
    .filter((entry): entry is Pack07NarrativeItemView => entry != null);
  const domains = asList(block.domains)
    .map(domain)
    .filter((entry): entry is Pack07NarrativeDomainView => entry != null);
  const luck = asList(block.luck).map(item).filter((entry): entry is Pack07NarrativeItemView => entry != null);
  const actions = asList(block.actions).map(item).filter((entry): entry is Pack07NarrativeItemView => entry != null);
  if (!executive && !strengths.length && !closing && !domains.length) return null;
  const composer: Pack07NarrativeComposerView = {
    executive,
    strengths,
    risks,
    opportunities,
    domains,
    luck,
    actions,
    closing,
    labels: labels(asRecord(block.labels)),
  };
  return {
    title: text(block.title) || INTERPRETATION_TITLE,
    available: true,
    lead: executive,
    leadExtra: "",
    leadSource: "detailed_narrative.executive",
    zones: [],
    closing,
    closingSource: "detailed_narrative.closing",
    emptyMessage: INTERPRETATION_EMPTY,
    domainTitle: "",
    domains: [],
    composer,
  };
}
