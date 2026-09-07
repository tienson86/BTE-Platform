/**
 * Public DTO → customer view-model. Does not compute compatibility or invent score.
 */

import {
  CONFIDENCE_LABEL,
  CUSTOMER_ERROR,
  DOMAIN_TITLE,
  FORBIDDEN_ID_PATTERN,
  HERO_EYEBROW,
  OPTIONAL_DOMAINS,
  OVERALL_STATE_HEADLINE,
  OVERALL_STATE_LABEL,
  PRIORITY_LABEL,
  WARNING_NOTE,
} from "./labels";
import type {
  ActionCardVm,
  ComparisonGroupVm,
  DomainCardVm,
  MarriageConsultationDto,
  MarriageEnvelope,
  MarriagePublicError,
  MarriageReportBlock,
  MarriageReportDto,
  MarriageReportSection,
  MarriageViewModel,
  MarriageWarning,
} from "./types";

const HERO_LABEL_MAX = 120;

export function customerErrorMessage(error: MarriagePublicError | undefined, fallback?: string): string {
  if (!error) {
    return fallback || CUSTOMER_ERROR.INTERNAL_ERROR;
  }
  const fromCode = CUSTOMER_ERROR[error.code];
  if (fromCode) return fromCode;
  const fromDetail = CUSTOMER_ERROR[error.message];
  if (fromDetail) return fromDetail;
  if (error.code === "VALIDATION_ERROR") return CUSTOMER_ERROR.VALIDATION_ERROR;
  return CUSTOMER_ERROR.INTERNAL_ERROR;
}

export function adaptMarriageView(
  consultation: MarriageConsultationDto,
  report: MarriageReportDto,
  warnings: MarriageWarning[],
  expertTrace?: Record<string, unknown> | null,
): MarriageViewModel {
  const identity = section(report, "identity");
  const hero = section(report, "compatibility_hero");
  const executive = section(report, "executive_summary");
  const strengthsSec = section(report, "strengths");
  const risksSec = section(report, "risks");
  const comparisonGroups = comparisonGroupsFrom(report);
  const domainsSec = section(report, "domain_analysis");
  const timingSec = section(report, "timing");
  const actionsSec = section(report, "action_plan");
  const confidenceSec = section(report, "confidence_limitations");
  const conclusionSec = section(report, "conclusion");
  const appendixSec = section(report, "appendix");
  const state = consultation.overall_state;
  const heroHighlights = (hero?.blocks || []).filter((item) => item.kind === "highlight");
  const heroStrengths = heroHighlights
    .filter((item) => (item.title || "").includes("hòa hợp") || (item.title || "").includes("hỗ trợ"))
    .map((item) => shortLabel(item.body || item.title || ""));
  const heroRisks = heroHighlights
    .filter((item) => (item.title || "").includes("xung") || (item.title || "").includes("lưu ý"))
    .map((item) => shortLabel(item.body || item.title || ""));
  return {
    consultationId: consultation.consultation_id,
    overallState: state,
    score: consultation.score ?? report.score ?? null,
    grade: consultation.grade ?? report.grade ?? null,
    identityTitle: identity?.summary || identity?.blocks[0]?.body || coupleFallback(consultation),
    personAName: consultation.person_a.display_name || "Người A",
    personBName: consultation.person_b.display_name || "Người B",
    heroEyebrow: HERO_EYEBROW,
    heroHeadline:
      firstText(hero, "headline") ||
      consultation.headline ||
      (state ? OVERALL_STATE_HEADLINE[state] : "") ||
      "",
    heroSummary: firstText(hero, "summary") || firstText(hero, "decision_state") || "",
    heroStateLabel: state ? `Nền tảng hiện ở trạng thái: ${OVERALL_STATE_LABEL[state] || state}` : "",
    heroStrengths,
    heroRisks,
    confidenceLabel: CONFIDENCE_LABEL[consultation.confidence.level] || consultation.confidence.level,
    executiveSummary: executive?.blocks[0]?.body || executive?.summary || "",
    strengths: highlightBodies(strengthsSec),
    risks: highlightBodies(risksSec),
    comparisonGroups,
    domains: groupDomains(domainsSec),
    unavailableNote: unavailableNote(warnings, domainsSec),
    timingSummary: timingBody(timingSec),
    actions: actionCards(actionsSec),
    limitations: consultation.limitations || [],
    confidenceBody: joinBodies(confidenceSec),
    conclusion: conclusionSec?.blocks[0]?.body || conclusionSec?.summary || "",
    appendix: customerAppendix(appendixSec),
    warnings,
    expertTrace: expertTrace ? stringifyExpert(expertTrace) : null,
  };
}

export function warningNotes(warnings: MarriageWarning[]): string[] {
  const seen = new Set<string>();
  const notes: string[] = [];
  for (const item of warnings) {
    const text = WARNING_NOTE[item.code] || item.description || item.code;
    if (seen.has(text)) continue;
    seen.add(text);
    notes.push(text);
  }
  return notes;
}

function section(report: MarriageReportDto, id: string): MarriageReportSection | undefined {
  return report.sections.find((item) => item.section_id === id);
}

function firstText(sec: MarriageReportSection | undefined, kind: string): string {
  if (!sec) return "";
  const block = sec.blocks.find((item) => item.kind === kind);
  return block?.body || block?.title || sec.summary || "";
}

function comparisonGroupsFrom(report: MarriageReportDto): ComparisonGroupVm[] {
  const specs = [
    { id: "comparison_a_to_b", title: "A bổ trợ B" },
    { id: "comparison_b_to_a", title: "B bổ trợ A" },
    { id: "comparison_harmony", title: "Điểm hòa hợp" },
    { id: "comparison_conflict", title: "Điểm xung" },
    { id: "comparison_rescue", title: "Yếu tố cứu giải" },
  ];
  const groups: ComparisonGroupVm[] = [];
  for (const spec of specs) {
    const sec = section(report, spec.id);
    const items = highlightBodies(sec);
    if (!items.length) continue;
    groups.push({ id: spec.id, title: spec.title, items });
  }
  return groups;
}

function highlightBodies(sec: MarriageReportSection | undefined): string[] {
  if (!sec) return [];
  return sec.blocks
    .filter((item) => item.kind === "highlight" && (item.body || item.title))
    .map((item) => item.body || item.title || "")
    .filter((text) => !FORBIDDEN_ID_PATTERN.test(text));
}

function groupDomains(sec: MarriageReportSection | undefined): DomainCardVm[] {
  if (!sec) return [];
  const byDomain = new Map<string, MarriageReportBlock[]>();
  for (const block of sec.blocks) {
    if (block.visibility === "expert") continue;
    if (!block.domain) continue;
    const list = byDomain.get(block.domain) || [];
    list.push(block);
    byDomain.set(block.domain, list);
  }
  const cards: DomainCardVm[] = [];
  for (const [domain, blocks] of byDomain) {
    const summaryBlock = blocks.find((item) => item.kind === "domain_summary") || blocks[0];
    const explanation = blocks
      .map((item) => item.body)
      .filter((text): text is string => Boolean(text))
      .join(" ");
    cards.push({
      domain,
      title: summaryBlock?.title || DOMAIN_TITLE[domain] || domain,
      stateLabel: summaryBlock?.state ? OVERALL_STATE_LABEL[summaryBlock.state] || summaryBlock.state : "",
      summary: summaryBlock?.body || "",
      explanation,
      relatedActionKeys: blocks.flatMap((item) => item.source_recommendation_ids || []),
    });
  }
  return cards;
}

function unavailableNote(
  warnings: MarriageWarning[],
  domainsSec: MarriageReportSection | undefined,
): string | null {
  const optional = warnings.filter(
    (item) => item.code === "DOMAIN_UNAVAILABLE" && OPTIONAL_DOMAINS.includes(item.affected_domain as never),
  );
  if (!optional.length) {
    const hasOptionalCard = (domainsSec?.blocks || []).some(
      (item) => item.domain && OPTIONAL_DOMAINS.includes(item.domain as never) && item.visibility !== "expert",
    );
    if (!hasOptionalCard) {
      return "Một số miền (tương tác, gia đình, con cái) chưa đủ dữ liệu cấu trúc nên không luận riêng.";
    }
    return null;
  }
  return WARNING_NOTE.DOMAIN_UNAVAILABLE;
}

function timingBody(sec: MarriageReportSection | undefined): string | null {
  if (!sec) return null;
  const text = joinBodies(sec).trim();
  return text ? text : null;
}

function actionCards(sec: MarriageReportSection | undefined): ActionCardVm[] {
  if (!sec) return [];
  return sec.blocks
    .filter((item) => item.kind === "recommendation" && (item.title || item.body))
    .map((item, index) => parseAction(item, index));
}

function parseAction(block: MarriageReportBlock, index: number): ActionCardVm {
  const body = block.body || "";
  const whenMatch = body.match(/Khi nào:\s*([^.]+)/);
  const priorityKey = detectPriority(body);
  return {
    key: block.block_id || `action-${index}`,
    title: block.title || "Việc nên làm",
    what: block.title || body,
    objective: extractObjective(body),
    priorityLabel: priorityKey ? PRIORITY_LABEL[priorityKey] : "",
    priority: priorityKey || "",
    when: whenMatch?.[1]?.trim() || "",
    outcome: extractOutcome(body),
  };
}

function detectPriority(body: string): string {
  if (body.includes("Then chốt")) return "critical";
  if (body.includes("Ưu tiên cao")) return "high";
  if (body.includes("Ưu tiên vừa") || body.includes("Nên thực hiện")) return "medium";
  if (body.includes("Ưu tiên thấp") || body.includes("Tham khảo")) return "low";
  return "";
}

function extractObjective(body: string): string {
  const cleaned = body.replace(/^[^.]+\.\s*/, "");
  return cleaned.split("Khi nào:")[0]?.trim() || "";
}

function extractOutcome(body: string): string {
  const afterWhen = body.split("Khi nào:")[1];
  if (!afterWhen) return "";
  return afterWhen.replace(/^[^.]+\.\s*/, "").replace(/Mức thời điểm:.*$/, "").trim();
}

function joinBodies(sec: MarriageReportSection | undefined): string {
  if (!sec) return "";
  return sec.blocks
    .filter((item) => item.visibility !== "expert")
    .map((item) => item.body || item.title || "")
    .filter(Boolean)
    .join(" ");
}

function customerAppendix(sec: MarriageReportSection | undefined): string {
  if (!sec) return "";
  const customer = sec.blocks.find((item) => item.visibility !== "expert");
  return customer?.body || "";
}

function coupleFallback(consultation: MarriageConsultationDto): string {
  const a = consultation.person_a.display_name || "Người A";
  const b = consultation.person_b.display_name || "Người B";
  return `${a} và ${b}`;
}

function shortLabel(text: string): string {
  const trimmed = text.trim();
  if (trimmed.length <= HERO_LABEL_MAX) return trimmed;
  return `${trimmed.slice(0, HERO_LABEL_MAX).trim()}…`;
}

function stringifyExpert(trace: Record<string, unknown>): string {
  try {
    return JSON.stringify(trace, null, 2);
  } catch {
    return "";
  }
}

export function envelopeErrors(payload: MarriageEnvelope<unknown> | null): MarriagePublicError[] {
  return payload?.errors || [];
}
