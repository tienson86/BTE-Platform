/**
 * Result Presentation Adapter — Sprint A + Sprint B (Phase 08).
 * Maps Canonical Desktop ViewModel → Result Page preview ViewModels.
 * No BaZi business logic — formatting, grouping, sorting, truncation only.
 */

import type { CanonicalDesktopViewModel } from "../../../adapters";
import {
  adaptPreviewList,
  adaptPreviewText,
} from "../../../presentation";
import {
  UNAVAILABLE_CONCLUSION,
  commercialOrUnavailable,
} from "../../../adapters/contentGuards";
import {
  MAX_PRIMARY_RECOMMENDATIONS,
  RECOMMENDATION_PRIORITY_LABEL,
  bindPlaceholder,
  formatPreviewField,
  priorityFromIndex,
  sortByRecommendationPriority,
  truncatePrimaryList,
} from "../presentation/previewBuilder";
import type {
  InterpretationBlockViewModel,
  KnowledgeSectionViewModel,
  RecommendationItemViewModel,
  ResultPageViewModel,
} from "../viewModels";

const TIMELINE_LABELS = ["Tiền vận", "Trung vận", "Hậu vận", "Định hướng"] as const;

function buildRecommendations(
  source: CanonicalDesktopViewModel,
): ResultPageViewModel["recommendations"] {
  const rawActions = source.s11.recommendations.items;
  const rawWarnings = source.s08.warnings.items;
  const rawBenefits = source.s08.strengths.items;

  const draft: RecommendationItemViewModel[] = rawActions.map((action, index) => {
    const priority = priorityFromIndex(index);
    const reasonSource =
      rawWarnings[index] ??
      source.s08.executive.body;
    const benefitSource =
      rawBenefits[index] ??
      source.s11.executive.body;
    const actionPreview = formatPreviewField(action, "title");
    const reasonPreview = formatPreviewField(reasonSource, "summary");
    const benefitPreview = formatPreviewField(benefitSource, "summary");
    const detailPreview = adaptPreviewText(
      [
        `Hành động: ${bindPlaceholder(action)}`,
        `Lý do: ${bindPlaceholder(reasonSource)}`,
        `Lợi ích kỳ vọng: ${bindPlaceholder(benefitSource)}`,
        "Chi tiết đầy đủ thuộc phần mở rộng — không thay đổi kết luận phân tích.",
      ].join(" "),
      "narrative",
    );

    return {
      id: `rec-${index + 1}`,
      priority,
      priorityLabel: RECOMMENDATION_PRIORITY_LABEL[priority],
      action: actionPreview,
      reason: reasonPreview,
      benefit: benefitPreview,
      detail: detailPreview,
      hasMore:
        actionPreview.hasMore ||
        reasonPreview.hasMore ||
        benefitPreview.hasMore ||
        detailPreview.hasMore,
    };
  });

  const sorted = sortByRecommendationPriority(draft);
  const primary = truncatePrimaryList(sorted, MAX_PRIMARY_RECOMMENDATIONS);

  return {
    title: "KHUYẾN NGHỊ",
    items: primary.items,
    totalCount: primary.totalCount,
    hasMore: primary.hasMore || primary.items.some((item) => item.hasMore),
    viewAllLabel: "Xem tất cả khuyến nghị →",
  };
}

function buildInterpretation(
  source: CanonicalDesktopViewModel,
): ResultPageViewModel["interpretation"] {
  const overviewObs = commercialOrUnavailable(source.s08.executive.body);
  const overviewImpact = commercialOrUnavailable(
    source.s08.strengths.items.filter((i) => i !== UNAVAILABLE_CONCLUSION).slice(0, 2).join("; "),
  );
  const overviewSuggestion = commercialOrUnavailable(
    source.s08.actions.items[0] ?? source.s01.cta,
  );
  const cautionObs = commercialOrUnavailable(
    source.s08.warnings.items.filter((i) => i !== UNAVAILABLE_CONCLUSION).slice(0, 2).join("; "),
  );
  const cautionExplanation = commercialOrUnavailable(
    source.s05.insight.replace(/\n/g, " "),
  );
  const cautionImpact = commercialOrUnavailable(
    source.s11.attention.items.filter((i) => i !== UNAVAILABLE_CONCLUSION).slice(0, 2).join("; "),
  );
  const cautionSuggestion = commercialOrUnavailable(
    source.s08.actions.items[1] ?? source.s11.recommendations.items[1],
  );
  const directionObs = commercialOrUnavailable(source.s01.decisions[0]?.answer);
  const directionExplanation = commercialOrUnavailable(source.s01.decisions[1]?.answer);
  const directionImpact = commercialOrUnavailable(source.s01.decisions[2]?.answer);
  const directionSuggestion = commercialOrUnavailable(
    source.s08.actions.items.filter((i) => i !== UNAVAILABLE_CONCLUSION).slice(0, 3).join("; "),
  );

  const blocks: InterpretationBlockViewModel[] = [
    {
      id: "interp-overview",
      title: "Tổng quan mệnh cục",
      observation: formatPreviewField(overviewObs, "summary"),
      explanation: formatPreviewField(
        `Nhật chủ ${bindPlaceholder(source.s01.dayMaster.value, "—")} · ${commercialOrUnavailable(source.s04.summary)}`,
        "description",
      ),
      impact: formatPreviewField(overviewImpact, "summary"),
      suggestion: formatPreviewField(overviewSuggestion, "summary"),
      hasMore: true,
    },
    {
      id: "interp-caution",
      title: "Điểm cần lưu ý",
      observation: formatPreviewField(cautionObs, "summary"),
      explanation: formatPreviewField(cautionExplanation, "description"),
      impact: formatPreviewField(cautionImpact, "summary"),
      suggestion: formatPreviewField(cautionSuggestion, "summary"),
      hasMore: true,
    },
    {
      id: "interp-direction",
      title: "Định hướng hành động",
      observation: formatPreviewField(directionObs, "summary"),
      explanation: formatPreviewField(directionExplanation, "description"),
      impact: formatPreviewField(directionImpact, "summary"),
      suggestion: formatPreviewField(directionSuggestion, "summary"),
      hasMore: true,
    },
  ].map((block) => ({
    ...block,
    hasMore:
      block.observation.hasMore ||
      block.explanation.hasMore ||
      block.impact.hasMore ||
      block.suggestion.hasMore,
  }));

  return {
    title: "LUẬN GIẢI",
    blocks,
    expandLabel: "Mở rộng luận giải",
    collapseLabel: "Thu gọn",
  };
}

function buildKnowledge(
  source: CanonicalDesktopViewModel,
): ResultPageViewModel["knowledge"] {
  const dayMaster = bindPlaceholder(source.s01.dayMaster.value, "—");
  const usefulGod = bindPlaceholder(
    source.s02.items.find((i) => i.label === "Dụng thần")?.value,
    "—",
  );
  const pattern = bindPlaceholder(
    source.s02.items.find((i) => i.label === "Thế cục")?.value,
    "—",
  );

  const sections: KnowledgeSectionViewModel[] = [
    {
      id: "know-terminology",
      kind: "terminology",
      title: "Thuật ngữ",
      definition: formatPreviewField(
        `Nhật chủ: ${dayMaster}. Dụng thần: ${usefulGod}. Thế cục: ${pattern}.`,
        "summary",
      ),
      reference: formatPreviewField("Thuật ngữ Bát Tự trong lá số hiện tại", "summary"),
      detail: adaptPreviewText(
        commercialOrUnavailable(
          `Nhật chủ ${dayMaster}; Dụng thần ${usefulGod}; Thế cục ${pattern}.`,
        ),
        "narrative",
      ),
      hasMore: true,
      defaultOpen: true,
    },
    {
      id: "know-references",
      kind: "references",
      title: "Tài liệu tham chiếu",
      definition: formatPreviewField(
        commercialOrUnavailable(source.s04.summary),
        "summary",
      ),
      reference: formatPreviewField("Ngũ hành · Thập thần · Khuyến nghị", "summary"),
      detail: adaptPreviewText(
        commercialOrUnavailable(
          [
            ...source.s08.strengths.items.slice(0, 2),
            ...source.s08.warnings.items.slice(0, 2),
          ]
            .filter((item) => item !== UNAVAILABLE_CONCLUSION)
            .join("; "),
        ),
        "narrative",
      ),
      hasMore: true,
      defaultOpen: false,
    },
    {
      id: "know-theory",
      kind: "theory",
      title: "Lý thuyết truyền thống",
      definition: formatPreviewField(
        commercialOrUnavailable(source.s04.summary),
        "summary",
      ),
      reference: formatPreviewField("Cân bằng Ngũ hành", "summary"),
      detail: adaptPreviewText(
        commercialOrUnavailable(source.s05.insight),
        "narrative",
      ),
      hasMore: true,
      defaultOpen: false,
    },
    {
      id: "know-appendix",
      kind: "appendix",
      title: "Phụ lục",
      definition: formatPreviewField(
        `Mã lá số ${bindPlaceholder(source.s00.chartId.value, "—")} · ${bindPlaceholder(source.s00.version.value, "—")}.`,
        "summary",
      ),
      reference: formatPreviewField("Metadata báo cáo", "summary"),
      detail: adaptPreviewText(
        commercialOrUnavailable(source.footer),
        "narrative",
      ),
      hasMore: true,
      defaultOpen: false,
    },
  ];

  return {
    title: "KIẾN THỨC",
    sections,
  };
}

/**
 * Build full Result Page ViewModel (Sprint A zones + Sprint B content zones).
 */
export function adaptResultPageViewModel(
  source: CanonicalDesktopViewModel,
): ResultPageViewModel {
  const executiveBody = adaptPreviewText(
    commercialOrUnavailable(source.s08.executive.body),
    "narrative",
  );
  const executivePoints = adaptPreviewList(
    [
      ...source.s08.strengths.items.slice(0, 2),
      ...source.s08.warnings.items.slice(0, 2),
    ].map((item) => commercialOrUnavailable(item)),
    4,
  );

  const indicators = adaptPreviewList(
    source.s02.items.map((item) => ({
      label: item.label,
      value: item.value,
      color: item.color,
    })),
    6,
  );

  const destinyItems = adaptPreviewList(
    source.s01.decisions.map((d) => ({
      question: d.question,
      answer: adaptPreviewText(commercialOrUnavailable(d.answer), "summary"),
    })),
    3,
  );

  const elementRows = adaptPreviewList(
    source.s04.rows.map((row) => ({
      name: row.name,
      element: row.element,
      pct: row.pct,
      status: row.status,
    })),
    5,
  );

  const strengthInsight = adaptPreviewText(
    commercialOrUnavailable(source.s05.insight.replace(/\n/g, " ")),
    "summary",
  );
  const strengthFactors = adaptPreviewList(
    source.s05.factors.map((f) => ({
      ...f,
      text: commercialOrUnavailable(f.text),
    })),
    4,
  );

  const rankedGods = [...source.s06.gods].sort(
    (a, b) => Number.parseFloat(b.score) - Number.parseFloat(a.score),
  );
  const gods = adaptPreviewList(
    rankedGods.map((g) => ({ name: g.name, score: g.score, color: g.color })),
    5,
  );

  const radarAxes = source.s04.rows.map((row) => ({
    name: row.name,
    pct: row.pct,
    element: row.element,
  }));
  const radarSummary = adaptPreviewText(
    commercialOrUnavailable(source.s04.summary),
    "summary",
  );

  const timelineSource = [
    {
      label: TIMELINE_LABELS[0],
      detail: adaptPreviewText(UNAVAILABLE_CONCLUSION, "summary"),
    },
    {
      label: TIMELINE_LABELS[1],
      detail: adaptPreviewText(
        commercialOrUnavailable(source.s08.strengths.items[0] ?? ""),
        "summary",
      ),
    },
    {
      label: TIMELINE_LABELS[2],
      detail: adaptPreviewText(
        commercialOrUnavailable(source.s08.warnings.items[0] ?? ""),
        "summary",
      ),
    },
    {
      label: TIMELINE_LABELS[3],
      detail: adaptPreviewText(
        commercialOrUnavailable(source.s08.actions.items[0] ?? source.s01.cta),
        "summary",
      ),
    },
  ];
  const stages = adaptPreviewList(timelineSource, 4);
  const timelineSummary = adaptPreviewText(UNAVAILABLE_CONCLUSION, "summary");

  return {
    context: {
      title: source.s00.title,
      profileName: source.s00.profile.name,
      profileMeta: source.s00.profile.meta,
      birthDate: source.s00.birth.date,
      birthLunar: source.s00.birth.lunar,
      birthTime: source.s00.birth.time,
      chartId: source.s00.chartId.value,
      status: source.s00.status.value,
      analyzedAt: source.s00.analyzedAt.value,
    },
    executive: {
      title: "TÓM TẮT ĐIỀU HÀNH",
      headline: executiveBody,
      points: executivePoints,
      hasMore: executiveBody.hasMore || executivePoints.hasMore,
    },
    indicators: {
      title: "CHỈ SỐ CỐT LÕI",
      items: indicators,
      hasMore: indicators.hasMore,
    },
    destiny: {
      title: "ĐỊNH HƯỚNG MỆNH VẬN",
      items: destinyItems,
      cta: source.s01.cta,
      hasMore: destinyItems.hasMore || destinyItems.items.some((i) => i.answer.hasMore),
    },
    fiveElements: {
      title: "NGŨ HÀNH",
      rows: elementRows,
      summary: adaptPreviewText(source.s04.summary, "summary"),
      hasMore: elementRows.hasMore,
    },
    strength: {
      title: source.s05.title,
      level: source.s05.level,
      score: source.s05.score,
      percent: source.s05.percent,
      insight: strengthInsight,
      factors: strengthFactors,
      cta: source.s05.cta,
      hasMore: strengthInsight.hasMore || strengthFactors.hasMore,
    },
    tenGods: {
      title: "THẬP THẦN",
      gods,
      cta: source.s06.link,
      hasMore: gods.hasMore,
    },
    radar: {
      title: "BIỂU ĐỒ RADAR NGŨ HÀNH",
      axes: radarAxes,
      summary: radarSummary,
      hasMore: radarSummary.hasMore,
    },
    timeline: {
      title: "DÒNG THỜI GIAN VẬN",
      stages,
      summary: timelineSummary,
      hasMore: stages.hasMore || timelineSummary.hasMore,
    },
    recommendations: buildRecommendations(source),
    interpretation: buildInterpretation(source),
    knowledge: buildKnowledge(source),
  };
}
