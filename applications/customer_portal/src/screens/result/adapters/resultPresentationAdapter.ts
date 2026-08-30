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
  FIVE_ELEMENTS_DISCLAIMER,
  FIVE_ELEMENTS_TITLE,
} from "../../../adapters/canonicalFiveElements";
import {
  executiveFromNarrative,
  hasUsableNarrativeResult,
  paragraphByRole,
  primaryRecommendationFromNarrative,
  secondaryMilestoneFromNarrative,
  type NarrativeRecommendationDto,
} from "../../../adapters/narrativeResultAdapter";
import {
  MAX_PRIMARY_RECOMMENDATIONS,
  RECOMMENDATION_PRIORITY_LABEL,
  bindPlaceholder,
  formatPreviewField,
  priorityFromIndex,
  sortByRecommendationPriority,
  truncatePrimaryList,
} from "../presentation/previewBuilder";
import type { FullReportViewModel } from "../../../report/fullReportViewModel";
import type {
  InterpretationBlockViewModel,
  KnowledgeSectionViewModel,
  RecommendationItemViewModel,
  RecommendationPriority,
  ResultPageViewModel,
} from "../viewModels";

const CANONICAL_NARRATIVE_TITLES: ReadonlyArray<{ match: RegExp; title: string }> = [
  { match: /executive|summary|tóm tắt/i, title: "Tóm tắt điều hành" },
  { match: /observation|quan sát/i, title: "Quan sát" },
  { match: /reasoning|explanation|lý giải/i, title: "Lý giải" },
  { match: /impact|ảnh hưởng|tác động/i, title: "Tác động" },
  { match: /recommendation|suggestion|khuyến/i, title: "Khuyến nghị" },
  { match: /warning|caution|cảnh báo|lưu ý/i, title: "Lưu ý" },
  { match: /conclusion|kết luận/i, title: "Kết luận" },
];

function chartPillarLabel(title: string): string {
  if (/năm/i.test(title)) return "Năm";
  if (/tháng/i.test(title)) return "Tháng";
  if (/ngày|nhật/i.test(title)) return "Ngày";
  if (/giờ/i.test(title)) return "Giờ";
  return title.replace(/\s*\(.*\)\s*$/, "").trim() || title;
}

function mapResultChartPillars(
  source: CanonicalDesktopViewModel,
  fullReport?: FullReportViewModel | null,
): ResultPageViewModel["chart"]["pillars"] {
  const reportByLabel = new Map(
    (fullReport?.pillars ?? []).map((pillar) => [pillar.label, pillar]),
  );
  return source.s03.pillars.map((pillar) => {
    const label = chartPillarLabel(pillar.title);
    const report = reportByLabel.get(label);
    const tenGod =
      (pillar.tenGod || report?.tenGod || "").trim() ||
      (pillar.highlight ? "Nhật Chủ" : "");
    return {
      label,
      stem: pillar.stem.viet || report?.stem || "",
      stemElement: pillar.stem.element || "",
      branch: pillar.branch.viet || report?.branch || "",
      branchElement: pillar.branch.element || "",
      napAm: report?.napAm || "",
      hiddenStems: report?.hiddenStems || "",
      hiddenGods: (pillar.hiddenLines || []).filter(Boolean).join(" · "),
      tenGod,
      growthStage: report?.growthStage || "",
    };
  });
}

function isUsablePreviewText(text: string): boolean {
  const trimmed = text.trim();
  return Boolean(trimmed) && trimmed !== UNAVAILABLE_CONCLUSION;
}

function buildRecommendations(
  source: CanonicalDesktopViewModel,
): ResultPageViewModel["recommendations"] {
  const narrative = source.narrativeResult;
  const structuredPrimary = primaryRecommendationFromNarrative(narrative);
  const secondaryMilestone = secondaryMilestoneFromNarrative(narrative);

  if (structuredPrimary) {
    const what = formatPreviewField(structuredPrimary.what, "title");
    const why = formatPreviewField(structuredPrimary.why, "summary");
    const outcome = formatPreviewField(
      structuredPrimary.expected_outcome,
      "summary",
    );
    const howWhenDetail = adaptPreviewText(
      [
        structuredPrimary.how
          ? `Cách làm: ${commercialOrUnavailable(structuredPrimary.how)}`
          : "",
        structuredPrimary.when
          ? `Thời điểm: ${commercialOrUnavailable(structuredPrimary.when)}`
          : "",
      ]
        .filter(Boolean)
        .join(" "),
      "narrative",
    );
    const primaryItem: RecommendationItemViewModel = {
      id: "rec-primary-career",
      priority: "critical",
      priorityLabel:
        structuredPrimary.capability_label?.trim() || "Chiến lược nghề nghiệp",
      action: what,
      reason: why,
      benefit: outcome,
      detail: howWhenDetail,
      hasMore:
        what.hasMore ||
        why.hasMore ||
        outcome.hasMore ||
        howWhenDetail.hasMore ||
        Boolean(structuredPrimary.how || structuredPrimary.when),
    };
    const items: RecommendationItemViewModel[] = [primaryItem];
    if (secondaryMilestone?.summary || secondaryMilestone?.composed_text) {
      const summaryText = commercialOrUnavailable(
        secondaryMilestone.summary || secondaryMilestone.composed_text,
      );
      const summaryPreview = formatPreviewField(summaryText, "summary");
      items.push({
        id: "rec-secondary-promotion",
        priority: "medium",
        priorityLabel:
          secondaryMilestone.capability_label?.trim() ||
          "Cột mốc thăng tiến",
        action: formatPreviewField(
          secondaryMilestone.capability_label || "Sẵn sàng thăng tiến",
          "title",
        ),
        reason: summaryPreview,
        benefit: formatPreviewField(
          "Xem chi tiết trong phần mở rộng khi cần.",
          "summary",
        ),
        detail: summaryPreview,
        hasMore: summaryPreview.hasMore,
      });
    }
    return {
      title: "KHUYẾN NGHỊ",
      items,
      totalCount: items.length,
      hasMore: items.some((item) => item.hasMore),
      viewAllLabel: "Đọc toàn bộ tư vấn",
      visible: true,
      primaryCtaLabel: "Đọc toàn bộ tư vấn",
      secondaryCtaLabel: "Xem phân tích chi tiết",
    };
  }

  if (hasUsableNarrativeResult(narrative) && narrative) {
    const fromRoot = narrative.recommendations ?? [];
    const fromSections = (narrative.sections ?? []).flatMap(
      (section) => section.recommendations ?? [],
    );
    const rawItems: NarrativeRecommendationDto[] = [...fromRoot, ...fromSections];
    const draft: RecommendationItemViewModel[] = rawItems.map((item, index) => {
      const priority = _mapPriority(item.priority, index);
      const actionPreview = formatPreviewField(item.action, "title");
      const reasonPreview = formatPreviewField(item.reason, "summary");
      const benefitPreview = formatPreviewField(item.benefit, "summary");
      const detailPreview = adaptPreviewText(
        [
          `Hành động: ${bindPlaceholder(item.action)}`,
          `Lý do: ${bindPlaceholder(item.reason)}`,
          `Lợi ích kỳ vọng: ${bindPlaceholder(item.benefit)}`,
        ]
          .filter((part) => !part.endsWith(UNAVAILABLE_CONCLUSION))
          .join(" "),
        "narrative",
      );
      return {
        id: item.id ?? `rec-${index + 1}`,
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
      viewAllLabel: "Đọc toàn bộ tư vấn",
      visible: primary.items.length > 0,
      primaryCtaLabel: "Đọc toàn bộ tư vấn",
      secondaryCtaLabel: "Xem phân tích chi tiết",
    };
  }

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
    viewAllLabel: "Đọc toàn bộ tư vấn",
    visible: primary.items.length > 0,
    primaryCtaLabel: "Đọc toàn bộ tư vấn",
    secondaryCtaLabel: "Xem phân tích chi tiết",
  };
}

function _mapPriority(
  value: string | undefined,
  index: number,
): RecommendationPriority {
  const key = (value ?? "").toLowerCase();
  if (key === "critical" || key === "high" || key === "medium" || key === "low") {
    return key;
  }
  return priorityFromIndex(index);
}

function canonicalNarrativeTitle(section: { id?: string; intent?: string; title?: string }): string {
  const blob = `${section.id ?? ""} ${section.intent ?? ""} ${section.title ?? ""}`;
  return CANONICAL_NARRATIVE_TITLES.find((item) => item.match.test(blob))?.title || section.title || "Luận giải";
}

function buildInterpretation(
  source: CanonicalDesktopViewModel,
  fullReport?: FullReportViewModel | null,
): ResultPageViewModel["interpretation"] {
  if (fullReport && fullReport.narrative.length === 7) {
    const blocks = fullReport.narrative.map((section) => ({
      id: section.id,
      title: section.title,
      observation: formatPreviewField(section.body || UNAVAILABLE_CONCLUSION, "summary"),
      explanation: formatPreviewField(section.body || UNAVAILABLE_CONCLUSION, "description"),
      impact: formatPreviewField(section.body || UNAVAILABLE_CONCLUSION, "summary"),
      suggestion: formatPreviewField(section.body || UNAVAILABLE_CONCLUSION, "summary"),
      hasMore: Boolean(section.body),
    }));
    return {
      title: "LUẬN GIẢI",
      blocks,
      expandLabel: "Mở rộng luận giải",
      collapseLabel: "Thu gọn",
      visible: blocks.length > 0,
    };
  }
  const narrative = source.narrativeResult;
  if (hasUsableNarrativeResult(narrative) && narrative) {
    const sectionBlocks: InterpretationBlockViewModel[] = (narrative.sections ?? [])
      .map((section, index) => {
        const texts = (section.paragraphs ?? [])
          .map((paragraph) => commercialOrUnavailable(paragraph.text ?? ""))
          .filter(isUsablePreviewText);
        const observation = texts[0] ?? "";
        const explanation = texts[1] ?? texts[0] ?? "";
        const impact = texts.find((_, i) => i === 2) ?? texts[0] ?? "";
        const suggestion = texts[texts.length - 1] ?? "";
        return {
          id: section.id || `interp-${index + 1}`,
          title: canonicalNarrativeTitle(section),
          observation: formatPreviewField(observation, "summary"),
          explanation: formatPreviewField(explanation, "description"),
          impact: formatPreviewField(impact, "summary"),
          suggestion: formatPreviewField(suggestion, "summary"),
          hasMore: true,
        };
      })
      .filter((block) => isUsablePreviewText(block.observation.text));

    const blocks = (
      sectionBlocks.length > 0
        ? sectionBlocks
        : [
            {
              id: "interp-overview",
              title: "Executive Summary",
              observation: formatPreviewField(
                paragraphByRole(narrative, "observation") ||
                  commercialOrUnavailable(narrative.summary?.identity),
                "summary",
              ),
              explanation: formatPreviewField(paragraphByRole(narrative, "explanation"), "description"),
              impact: formatPreviewField(paragraphByRole(narrative, "impact"), "summary"),
              suggestion: formatPreviewField(
                paragraphByRole(narrative, "suggestion") ||
                  commercialOrUnavailable(narrative.summary?.priority_recommendation),
                "summary",
              ),
              hasMore: true,
            },
          ]
    ).map((block) => ({
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
      visible: blocks.length > 0,
    };
  }

  const limited = formatPreviewField(UNAVAILABLE_CONCLUSION, "summary");
  return {
    title: "LUẬN GIẢI",
    blocks: [
      {
        id: "interp-limited",
        title: "Luận giải",
        observation: limited,
        explanation: formatPreviewField(UNAVAILABLE_CONCLUSION, "description"),
        impact: limited,
        suggestion: limited,
        hasMore: false,
      },
    ],
    expandLabel: "Mở rộng luận giải",
    collapseLabel: "Thu gọn",
    visible: true,
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
    ...buildCommercialKnowledgeSections(source.commercialConsulting),
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
      reference: formatPreviewField("Phân bố Ngũ hành", "summary"),
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
        `Mã tham chiếu ${bindPlaceholder(source.s00.chartId.value, "—")} · ${bindPlaceholder(source.s00.version.value, "—")}.`,
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
    visible: sections.length > 0,
  };
}

function buildCommercialKnowledgeSections(
  consulting: CanonicalDesktopViewModel["commercialConsulting"],
): KnowledgeSectionViewModel[] {
  if (!consulting?.visible || consulting.sections.length === 0) {
    return [];
  }
  return consulting.sections.map((section, index) => {
    const meaning = section.meaning.filter(Boolean).join(" ");
    const recommendations = section.recommendations.filter(Boolean).join(" ");
    const detail = [meaning, recommendations].filter(Boolean).join(" ");
    return {
      id: `know-consulting-${section.domain || index}`,
      kind: "consulting" as const,
      title: section.title,
      definition: formatPreviewField(section.summary, "summary"),
      reference: formatPreviewField("Tư vấn thương mại", "summary"),
      detail: adaptPreviewText(detail, "narrative"),
      hasMore: Boolean(detail),
      defaultOpen: index === 0,
    };
  });
}

/**
 * Build full Result Page ViewModel (Sprint A zones + Sprint B content zones).
 * Product Polish V1 — consulting presentation mapping (existing data only).
 */
export function adaptResultPageViewModel(
  source: CanonicalDesktopViewModel,
  fullReport?: FullReportViewModel | null,
): ResultPageViewModel {
  const narrative = source.narrativeResult;
  const commercialExec = executiveFromNarrative(narrative);

  const executiveBody = adaptPreviewText(
    commercialOrUnavailable(
      commercialExec?.central_message || source.s08.executive.body,
    ),
    "narrative",
  );
  const pointSources = commercialExec?.supporting_points?.length
    ? [...commercialExec.supporting_points]
    : [
        ...source.s08.strengths.items.slice(0, 2),
        ...source.s08.warnings.items.slice(0, 2),
      ];
  const executivePoints = adaptPreviewList(
    pointSources
      .map((item) => commercialOrUnavailable(item))
      .filter(isUsablePreviewText)
      .slice(0, 4),
    4,
  );
  const conclusionText = commercialExec?.conclusion
    ? commercialOrUnavailable(commercialExec.conclusion)
    : "";
  const conclusion = isUsablePreviewText(conclusionText)
    ? adaptPreviewText(conclusionText, "summary")
    : null;

  const indicatorSource = source.s02.items;
  const preferred = ["Dụng thần", "Hỷ thần", "Kỵ thần"];
  const byLabel = new Map(indicatorSource.map((item) => [item.label, item]));
  const ordered = preferred
    .map((label) => byLabel.get(label))
    .filter((item): item is NonNullable<typeof item> => Boolean(item));
  const indicators = adaptPreviewList(
    ordered.map((item) => ({
      label: item.label,
      value: item.value,
      color: item.color,
    })),
    3,
  );
  const dungReason = source.s02.dungReason?.trim() || "";
  const patternValue =
    source.s01.conditions.rows.find((row) => row.label === "Cách cục")?.value?.trim() || "";
  const climateValue =
    source.s01.conditions.rows.find((row) => row.label === "Điều hậu")?.value?.trim() || "";

  const destinyItems = adaptPreviewList(
    source.s01.decisions.map((d) => ({
      question: d.question,
      answer: adaptPreviewText(commercialOrUnavailable(d.answer), "summary"),
    })),
    3,
  );
  const destinyVisible = destinyItems.items.some((item) =>
    isUsablePreviewText(item.answer.text),
  );

  const elementRows = adaptPreviewList(
    source.s04.rows.map((row) => ({
      name: row.name,
      element: row.element,
      pct: row.pct,
      count: "count" in row && typeof row.count === "number" ? row.count : null,
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
  const strengthVisible =
    Boolean(source.s05.level?.trim()) ||
    isUsablePreviewText(strengthInsight.text);

  const rankedGods = [...source.s06.gods];
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

  const luckCurrent = source.s01.conditions.rows.find((row) => row.label === "Đại vận");
  const luckStart = source.s01.conditions.rows.find((row) => row.label === "Tuổi khởi vận");
  const luckSequence = source.s01.conditions.rows.find((row) => row.label === "Lộ trình Đại vận");
  const luckParts = (luckSequence?.value ?? "")
    .split(/\s\|\s| · /)
    .map((part) => part.trim())
    .filter((part) => part && part !== UNAVAILABLE_CONCLUSION);
  const currentTokens = (luckCurrent?.value ?? "").trim().split(/\s+/);
  const currentGan =
    currentTokens.length >= 2 && !/^\d/.test(currentTokens[1] ?? "")
      ? `${currentTokens[0]} ${currentTokens[1]}`
      : (currentTokens[0] ?? "");
  const startAgeText =
    luckStart && isUsablePreviewText(luckStart.value) ? luckStart.value : "";
  const timelineSource = luckParts.map((part, index) => {
    const isCurrent = Boolean(currentGan) && part.startsWith(currentGan);
    return {
      label: isCurrent ? `Hiện tại · ${part}` : part,
      detail: adaptPreviewText(
        index === 0 && startAgeText
          ? `Tuổi khởi Đại vận: ${startAgeText}`
          : part,
        "summary",
      ),
    };
  });
  const stages = adaptPreviewList(timelineSource, 10);
  const timelineSummaryText =
    luckParts.length > 0
      ? [
          startAgeText ? `Tuổi khởi Đại vận: ${startAgeText}` : "",
          luckCurrent && isUsablePreviewText(luckCurrent.value)
            ? `Hiện tại: ${luckCurrent.value}`
            : "",
          `${luckParts.length} chu kỳ`,
        ]
          .filter(Boolean)
          .join(" · ")
      : UNAVAILABLE_CONCLUSION;
  const timelineSummary = adaptPreviewText(timelineSummaryText, "summary");
  const timelineVisible = stages.items.some((stage) =>
    isUsablePreviewText(stage.detail.text),
  );

  const recommendations = buildRecommendations(source);
  const interpretation = buildInterpretation(source, fullReport);
  const knowledge = buildKnowledge(source);

  const cungPhi =
    source.s09.quai.bullets
      .find((item) => item.toLowerCase().includes("cung"))
      ?.split(":")
      .slice(1)
      .join(":")
      .trim() || source.s09.quai.center;
  const nhomTrach =
    source.s09.quai.bullets
      .find((item) => item.toLowerCase().includes("nhóm") || item.toLowerCase().includes("trạch"))
      ?.split(":")
      .slice(1)
      .join(":")
      .trim() || "";
  const tamNguyen =
    source.s09.quai.bullets
      .find((item) => item.toLowerCase().includes("nguyên"))
      ?.split(":")
      .slice(1)
      .join(":")
      .trim() || "";
  const cuuVan =
    source.s09.quai.bullets
      .find((item) => item.toLowerCase().includes("vận"))
      ?.split(":")
      .slice(1)
      .join(":")
      .trim() || "";

  return {
    analysisId: fullReport?.analysisId || source.s00.chartId.value,
    chart: {
      title: "Tứ trụ – Bát Tự",
      pillars: mapResultChartPillars(source, fullReport),
      visible: source.s03.pillars.length > 0,
    },
    shenSha: {
      title: "THẦN SÁT",
      items:
        fullReport?.shenSha ??
        source.s07.items.map((item) => ({
          name: item.name,
          presence: item.presence,
          evidence: item.evidence,
        })),
      visible: Boolean(
        (fullReport?.shenSha.length ?? 0) > 0 || source.s07.items.length > 0,
      ),
    },
    context: {
      title: "BẠN LÀ AI",
      identityLabel: "Hồ sơ tư vấn",
      profileName: source.s00.profile.name,
      profileMeta: source.s00.profile.meta,
      birthDate: source.s00.birth.date,
      birthLunar: source.s00.birth.lunar,
      birthTime: source.s00.birth.time,
      chartId: source.s00.chartId.value,
      status: source.s00.status.value,
      analyzedAt: source.s00.analyzedAt.value,
      cungPhi,
      menhQuai: source.s09.quai.center,
      nhomTrach,
      tamNguyen,
      cuuVan,
    },
    executive: {
      title: "TÓM TẮT TƯ VẤN",
      headline: executiveBody,
      points: executivePoints,
      conclusion,
      hasMore:
        executiveBody.hasMore ||
        executivePoints.hasMore ||
        Boolean(conclusion?.hasMore),
      primaryCtaLabel: "Đọc toàn bộ tư vấn",
      secondaryCtaLabel: "Xem phân tích chi tiết",
    },
    indicators: {
      title: "Dụng thần · Hỷ · Kỵ",
      items: indicators,
      reasonLabel: "Căn cứ chọn Dụng",
      reason: dungReason,
      hasMore: indicators.hasMore,
      visible: indicators.items.length > 0 || Boolean(dungReason),
    },
    pattern: {
      title: "Cách cục",
      value: patternValue && patternValue !== UNAVAILABLE_CONCLUSION ? patternValue : "",
      visible: Boolean(patternValue && patternValue !== UNAVAILABLE_CONCLUSION),
    },
    climate: {
      title: "Điều hậu",
      value: climateValue && climateValue !== UNAVAILABLE_CONCLUSION ? climateValue : "",
      visible: Boolean(climateValue && climateValue !== UNAVAILABLE_CONCLUSION),
    },
    destiny: {
      title: "ĐỊNH HƯỚNG NGHỀ NGHIỆP",
      questionLabel: "Hướng nghề phù hợp?",
      items: destinyItems,
      cta: source.s01.cta,
      hasMore: destinyItems.hasMore || destinyItems.items.some((i) => i.answer.hasMore),
      visible: destinyVisible,
    },
    fiveElements: {
      title: FIVE_ELEMENTS_TITLE,
      rows: elementRows,
      summary: adaptPreviewText(FIVE_ELEMENTS_DISCLAIMER, "description"),
      hasMore: elementRows.hasMore,
      visible: elementRows.items.length > 0,
    },
    strength: {
      title: "Điểm thân",
      level: source.s05.level,
      score: source.s05.score,
      percent: source.s05.percent,
      insight: strengthInsight,
      factors: strengthFactors,
      cta: source.s05.cta,
      hasMore: strengthInsight.hasMore || strengthFactors.hasMore,
      visible: strengthVisible,
    },
    tenGods: {
      title: "Thập thần nổi bật",
      gods,
      othersLine: source.s06.note.startsWith("Các thần khác") ? source.s06.note : "",
      cta: source.s06.link,
      hasMore: gods.hasMore,
      visible: gods.items.length > 0,
    },
    radar: {
      title: "Phân bố Ngũ hành (biểu đồ)",
      axes: radarAxes,
      summary: radarSummary,
      hasMore: radarSummary.hasMore,
      visible: radarAxes.length > 0,
    },
    timeline: {
      title: "DÒNG THỜI GIAN VẬN",
      stages,
      summary: timelineSummary,
      hasMore: stages.hasMore || timelineSummary.hasMore,
      visible: timelineVisible,
    },
    recommendations,
    interpretation,
    knowledge,
  };
}
