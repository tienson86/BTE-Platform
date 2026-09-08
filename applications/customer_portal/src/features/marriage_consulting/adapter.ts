/**
 * Public DTO → customer view-model. Does not compute compatibility or invent score.
 */

import {
  CONFIDENCE_LABEL,
  CUSTOMER_ERROR,
  DOMAIN_TITLE,
  FORBIDDEN_ID_PATTERN,
  HERO_EYEBROW,
  LIMITATION_NOTE,
  OPTIONAL_DOMAINS,
  OVERALL_STATE_HEADLINE,
  OVERALL_STATE_LABEL,
  PRIORITY_LABEL,
  WARNING_NOTE,
} from "./labels";
import type {
  ActionCardVm,
  AssessmentCardVm,
  CungPhiVm,
  DomainCardVm,
  FinalOpinionVm,
  MarriageConsultationDto,
  MarriageEnvelope,
  MarriagePublicError,
  MarriageReportBlock,
  MarriageReportDto,
  MarriageReportSection,
  MarriageViewModel,
  MarriageWarning,
  MutualSupportVm,
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
  const comparisonSec = section(report, "comparison_a_to_b");
  const domainsSec = section(report, "domain_analysis");
  const timingSec = section(report, "timing");
  const actionsSec = section(report, "action_plan");
  const confidenceSec = section(report, "confidence_limitations");
  const conclusionSec = section(report, "conclusion");
  const appendixSec = section(report, "appendix");
  const cungSec = section(report, "cung_phi");
  const finalOpinion = finalOpinionFrom(conclusionSec);
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
    heroStateLabel: state ? `Nền tảng hiện ở trạng thái: ${OVERALL_STATE_LABEL[state] || "cần đọc kèm đánh giá chi tiết"}` : "",
    heroStrengths,
    heroRisks,
    confidenceLabel: CONFIDENCE_LABEL[consultation.confidence.level] || "Mang tính tham khảo",
    executiveSummary: executive?.blocks.find((item) => item.kind === "answer")?.body || executive?.blocks[0]?.body || executive?.summary || "",
    assessmentCards: assessmentCardsFrom(consultation, executive),
    strengths: highlightBodies(strengthsSec),
    risks: highlightBodies(risksSec),
    mutualSupport: mutualSupportFrom(comparisonSec),
    cungPhi: cungPhiFrom(cungSec),
    domains: groupDomains(domainsSec),
    unavailableNote: unavailableNote(warnings, domainsSec),
    timingSummary: timingBody(timingSec),
    actions: actionCards(actionsSec),
    limitations: customerLimitations(consultation.limitations || [], confidenceSec),
    confidenceBody: joinBodies(confidenceSec),
    conclusion: finalOpinion.overall,
    finalOpinion,
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

function assessmentCardsFrom(
  consultation: MarriageConsultationDto,
  executive: MarriageReportSection | undefined,
): AssessmentCardVm[] {
  const fromApi = consultation.assessment_cards || [];
  if (fromApi.length) {
    return fromApi.map((card) => ({
      questionId: card.question_id,
      question: card.question,
      answer: card.verdict || card.headline || card.answer,
      meaning: card.meaning || "",
      supportingFacts: card.supporting_facts || [],
      quickGuidance: card.quick_guidance || "",
      confidence: card.confidence,
      limitations: card.limitations || [],
      technicalExplanation: card.technical_explanation || "",
    }));
  }
  return cardsFromExecutive(executive);
}

function cardsFromExecutive(executive: MarriageReportSection | undefined): AssessmentCardVm[] {
  if (!executive) return [];
  const questions = executive.blocks.filter((item) => item.kind === "question");
  const cards: AssessmentCardVm[] = [];
  for (const question of questions) {
    const prefix = (question.block_id || "").replace(/-question$/, "");
    const answer = executive.blocks.find((item) => item.block_id === `${prefix}-answer`);
    const facts = executive.blocks.find((item) => item.block_id === `${prefix}-facts`);
    const confidence = executive.blocks.find((item) => item.block_id === `${prefix}-confidence`);
    const limitations = executive.blocks.find((item) => item.block_id === `${prefix}-limitations`);
    cards.push({
      questionId: prefix.toUpperCase(),
      question: question.body || question.title || "",
      answer: answer?.body || "",
      meaning: executive.blocks.find((item) => item.block_id === `${prefix}-meaning`)?.body || "",
      supportingFacts: (facts?.body || "")
        .split("\n")
        .map((line) => line.replace(/^•\s*/, "").trim())
        .filter(Boolean),
      quickGuidance: executive.blocks.find((item) => item.block_id === `${prefix}-guidance`)?.body || "",
      confidence: confidence?.body || "",
      limitations: (limitations?.body || "")
        .split("\n")
        .map((line) => line.replace(/^•\s*/, "").trim())
        .filter(Boolean),
      technicalExplanation:
        executive.blocks.find((item) => item.block_id === `${prefix}-technical`)?.body || "",
    });
  }
  return cards;
}

function mutualSupportFrom(sec: MarriageReportSection | undefined): MutualSupportVm | null {
  if (!sec) return null;
  const contributions = sec.blocks
    .filter((item) => item.kind === "highlight" && (item.body || item.title))
    .map((item) => ({
      title: item.title || "",
      body: item.body || "",
    }))
    .filter((item) => item.body && !FORBIDDEN_ID_PATTERN.test(item.body));
  const overall =
    sec.blocks.find((item) => item.kind === "summary" && item.block_id === "mutual-overall")?.body ||
    sec.blocks.find((item) => item.kind === "summary")?.body ||
    "";
  if (!contributions.length && !overall) return null;
  return {
    title: sec.title || "Bổ trợ lẫn nhau",
    contributions,
    overall,
  };
}

function cungPhiFrom(sec: MarriageReportSection | undefined): CungPhiVm | null {
  if (!sec) return null;
  const people = sec.blocks
    .filter((item) => item.kind === "reference")
    .map((item) => ({
      label: item.title || "",
      cung: item.body || "",
    }))
    .filter((item) => item.cung);
  const relation = sec.blocks.find((item) => item.block_id === "cung-relation")?.body || "";
  const meaning = sec.blocks.find((item) => item.block_id === "cung-meaning")?.body || "";
  const disclaimer = sec.blocks.find((item) => item.block_id === "cung-limit")?.body || "";
  if (!people.length && !relation) return null;
  return {
    title: sec.title || "Đánh giá Cung Phi",
    people,
    relation,
    meaning,
    disclaimer,
  };
}

function finalOpinionFrom(sec: MarriageReportSection | undefined): FinalOpinionVm {
  const overall =
    blockBody(sec, "conclusion-opinion") || sec?.summary || sec?.blocks[0]?.body || "";
  return {
    overall,
    strongestStrength: blockBody(sec, "conclusion-strength"),
    mainAttention: blockBody(sec, "conclusion-attention"),
    recommendation: blockBody(sec, "conclusion-recommendation"),
  };
}

function blockBody(sec: MarriageReportSection | undefined, blockId: string): string {
  if (!sec) return "";
  const block = sec.blocks.find((item) => item.block_id === blockId);
  return block?.body || "";
}

function customerLimitations(codes: string[], confidenceSec: MarriageReportSection | undefined): string[] {
  const seen = new Set<string>();
  const items: string[] = [];
  for (const code of codes) {
    const mapped = LIMITATION_NOTE[code];
    if (mapped) {
      if (seen.has(mapped)) continue;
      seen.add(mapped);
      items.push(mapped);
      continue;
    }
    if (!code || /^[a-z0-9_]+$/i.test(code)) continue;
    if (seen.has(code)) continue;
    seen.add(code);
    items.push(code);
  }
  for (const block of confidenceSec?.blocks || []) {
    if (block.kind !== "limitations" || !block.body) continue;
    if (seen.has(block.body)) continue;
    seen.add(block.body);
    items.push(block.body);
  }
  return items;
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
      return "Một số phần (tương tác, gia đình, con cái) chưa đủ dữ liệu nên không luận riêng.";
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
