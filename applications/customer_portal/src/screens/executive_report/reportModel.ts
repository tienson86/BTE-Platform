/**
 * Assemble executive report view models. Copy Presentation and canonical chart only.
 * Does not compose Narrative.
 */

import { canonicalStrengthLabel } from "../../adapters/canonicalStrength";
import {
  adaptNarrativeV2Presentation,
  type NarrativeV2PresentationView,
} from "../../adapters/narrativeV2PresentationAdapter";
import type { AnalysisDataDto, AnalyzeChartRequest } from "../../models";
import { adaptIdentityHeader } from "../commercial_dashboard/adapter";
import { adaptBaziCard } from "../commercial_dashboard/baziAdapter";
import { adaptFiveElementsCard } from "../commercial_dashboard/fiveElementsAdapter";
import { adaptLuckCard } from "../commercial_dashboard/luckAdapter";
import { adaptPatternCard } from "../commercial_dashboard/patternAdapter";
import { adaptShenShaCard } from "../commercial_dashboard/shenShaAdapter";
import { adaptTenGodsCard } from "../commercial_dashboard/tenGodsAdapter";
import type {
  BaziStructureView,
  FiveElementsView,
  IdentityHeaderView,
  LuckView,
  PatternView,
  ShenShaView,
  TenGodsView,
} from "../commercial_dashboard/types";
import {
  REPORT_ANALYSIS_TITLE,
  REPORT_FINDING_LABEL,
  REPORT_IDENTITY_LABEL,
  REPORT_PRODUCT_TITLE,
} from "./copy";
import { formatPublishedDate } from "./dateDisplay";

export type ReportFindingId = "headline" | "pattern" | "strength" | "priority" | "luck";

export type ReportFinding = {
  readonly id: ReportFindingId;
  readonly label: string;
  readonly value: string;
};

export type ReportCoverView = {
  readonly productTitle: string;
  readonly analysisTitle: string;
  readonly customerName: string;
  readonly birthLine: string;
  readonly analysisDate: string;
  readonly reportVersion: string;
};

export type ReportIdentityRow = {
  readonly label: string;
  readonly value: string;
};

export type ReportAppendixView = {
  readonly reportVersion: string;
  readonly presentationVersion: string;
  readonly analysisDate: string;
};

export type ExecutiveReportView = {
  readonly presentation: NarrativeV2PresentationView | null;
  readonly cover: ReportCoverView;
  readonly identityRows: readonly ReportIdentityRow[];
  readonly findings: readonly ReportFinding[];
  readonly bazi: BaziStructureView;
  readonly fiveElements: FiveElementsView;
  readonly tenGods: TenGodsView;
  readonly pattern: PatternView;
  readonly shenSha: ShenShaView;
  readonly luck: LuckView;
  readonly appendix: ReportAppendixView;
};

function joinPublished(parts: readonly string[]): string {
  return parts.filter((part) => part.trim()).join(" · ");
}

function pillarSummary(identity: IdentityHeaderView): string {
  const pillars = identity.pillars;
  return joinPublished([
    pillars.year.canChi,
    pillars.month.canChi,
    pillars.day.canChi,
    pillars.hour.canChi,
  ]);
}

function dayMasterLine(identity: IdentityHeaderView): string {
  return joinPublished([
    identity.dayMaster.stem,
    identity.dayMaster.yinYang,
    identity.dayMaster.element,
  ]);
}

function identityRows(identity: IdentityHeaderView): ReportIdentityRow[] {
  const person = identity.person;
  const rows: ReportIdentityRow[] = [];
  const fields: readonly [string, string][] = [
    [REPORT_IDENTITY_LABEL.name, person.fullName],
    [REPORT_IDENTITY_LABEL.gender, person.gender],
    [REPORT_IDENTITY_LABEL.birthDate, formatPublishedDate(person.solarBirth)],
    [REPORT_IDENTITY_LABEL.birthTime, person.birthTime],
    [REPORT_IDENTITY_LABEL.birthPlace, person.birthPlace],
    [REPORT_IDENTITY_LABEL.pillars, pillarSummary(identity)],
    [REPORT_IDENTITY_LABEL.dayMaster, dayMasterLine(identity)],
    [REPORT_IDENTITY_LABEL.cungPhi, identity.status.cungPhi],
  ];
  for (const [label, value] of fields) {
    if (value) rows.push({ label, value });
  }
  return rows;
}

function collectFindings(
  presentation: NarrativeV2PresentationView | null,
  pattern: PatternView,
  luck: LuckView,
  data: AnalysisDataDto | null | undefined,
): ReportFinding[] {
  const items: ReportFinding[] = [];
  const headline = presentation?.overview?.headline;
  if (headline) {
    items.push({ id: "headline", label: REPORT_FINDING_LABEL.headline, value: headline });
  }
  if (pattern.primary) {
    items.push({ id: "pattern", label: REPORT_FINDING_LABEL.pattern, value: pattern.primary });
  }
  const strength = canonicalStrengthLabel(data);
  if (strength) {
    items.push({ id: "strength", label: REPORT_FINDING_LABEL.strength, value: strength });
  }
  const priority = presentation?.action_plan?.top_priority?.title;
  if (priority) {
    items.push({ id: "priority", label: REPORT_FINDING_LABEL.priority, value: priority });
  }
  if (luck.current?.ganZhi) {
    items.push({
      id: "luck",
      label: REPORT_FINDING_LABEL.luck,
      value: joinPublished([luck.current.ganZhi, luck.current.yearRange]),
    });
  }
  return items;
}

function readPresentation(
  data: AnalysisDataDto | null | undefined,
): NarrativeV2PresentationView | null {
  const view = adaptNarrativeV2Presentation(data?.narrative_v2_shadow);
  return view.ok ? view : null;
}

/**
 * Bind the executive report from frozen Presentation plus canonical chart adapters.
 */
export function buildExecutiveReportView(
  data: AnalysisDataDto | null | undefined,
  request?: AnalyzeChartRequest | null,
): ExecutiveReportView {
  const presentation = readPresentation(data);
  const identity = adaptIdentityHeader(data, { request: request ?? null });
  const pattern = adaptPatternCard(data);
  const luck = adaptLuckCard(data);
  const analysisDate = formatPublishedDate(identity.status.analyzedAt);
  const reportVersion = identity.status.version;
  return {
    presentation,
    cover: {
      productTitle: REPORT_PRODUCT_TITLE,
      analysisTitle: REPORT_ANALYSIS_TITLE,
      customerName: identity.person.fullName,
      birthLine: joinPublished([
        formatPublishedDate(identity.person.solarBirth),
        identity.person.birthTime,
      ]),
      analysisDate,
      reportVersion,
    },
    identityRows: identityRows(identity),
    findings: collectFindings(presentation, pattern, luck, data),
    bazi: adaptBaziCard(data),
    fiveElements: adaptFiveElementsCard(data),
    tenGods: adaptTenGodsCard(data),
    pattern,
    shenSha: adaptShenShaCard(data),
    luck,
    appendix: {
      reportVersion,
      presentationVersion: presentation?.version ?? "",
      analysisDate,
    },
  };
}
