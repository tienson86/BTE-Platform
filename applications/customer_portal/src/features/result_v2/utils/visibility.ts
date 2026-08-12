/**
 * Section visibility — PX-2 SECTION_VISIBILITY_RULES.
 * Hidden = not mounted. Never blank cards.
 */

import type {
  AppendixModel,
  ChartModel,
  ChromeModel,
  DomainMapModel,
  KnowledgeModel,
  NavModel,
  PageState,
  TechnicalModel,
  WarningModel,
} from "../adapter/PortalResultModel";
import { DOMAIN_ORDER } from "../adapter/PortalResultModel";

export function isReadingState(state: PageState): boolean {
  return (
    state === "ready" ||
    state === "partial_ready" ||
    state === "printing" ||
    state === "exporting"
  );
}

export function showWarnings(warnings: WarningModel[]): boolean {
  return warnings.length > 0;
}

export function showCharts(charts: ChartModel[]): boolean {
  return charts.length > 0;
}

export function showKnowledge(knowledge: KnowledgeModel[]): boolean {
  return knowledge.length > 0;
}

export function showAppendix(appendix: AppendixModel | null): boolean {
  if (!appendix) return false;
  return Boolean(appendix.scope || appendix.reread || appendix.limits);
}

export function showTechnical(technical: TechnicalModel): boolean {
  return technical.available;
}

/** Domain is mountable only when it has real availability/content. */
export function showDomain(domain: DomainMapModel[keyof DomainMapModel]): boolean {
  if (!domain.available) return false;
  return Boolean(
    domain.intro ||
      domain.analysis_preview ||
      domain.analysis_detail ||
      domain.recommendation_ids.length > 0,
  );
}

export function buildNavModel(
  chrome: ChromeModel,
  pageState: PageState,
  domains: DomainMapModel,
  warnings: WarningModel[],
  charts: ChartModel[],
  technical: TechnicalModel,
  knowledge: KnowledgeModel[],
  appendix: AppendixModel | null,
): NavModel {
  const reading = isReadingState(pageState);
  const items = [
    {
      target_ui_id: "Technical",
      label: chrome.section_technical,
      visible: reading && showTechnical(technical),
    },
    { target_ui_id: "Summary", label: chrome.section_summary, visible: reading },
    {
      target_ui_id: "Recommendation",
      label: chrome.section_recommendation,
      visible: reading,
    },
    {
      target_ui_id: "Warnings",
      label: chrome.section_warnings,
      visible: reading && showWarnings(warnings),
    },
    ...DOMAIN_ORDER.map((key) => ({
      target_ui_id: `Domain${key.charAt(0).toUpperCase()}${key.slice(1)}`,
      label: domains[key].title,
      visible: reading && showDomain(domains[key]),
    })).filter((item) => item.visible),
    {
      target_ui_id: "Charts",
      label: chrome.section_charts,
      visible: reading && showCharts(charts),
    },
    {
      target_ui_id: "Knowledge",
      label: chrome.section_knowledge,
      visible: reading && showKnowledge(knowledge),
    },
    {
      target_ui_id: "Appendix",
      label: chrome.section_appendix,
      visible: reading && showAppendix(appendix),
    },
  ];
  return { items };
}
