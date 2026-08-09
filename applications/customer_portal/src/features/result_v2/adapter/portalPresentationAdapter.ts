/**
 * bte.portal.presentation_adapter.v2
 * Canonical Report → PortalResultModel. Formatting only.
 */

import {
  RESULT_UI_CONTRACT_ID,
  RESULT_UI_CONTRACT_VERSION,
  type AppendixModel,
  type ChartModel,
  type ChartTable,
  type DomainKey,
  type DomainMapModel,
  type DomainModel,
  type HeroModel,
  type HeroStatus,
  type KnowledgeModel,
  type PageState,
  type PortalResultModel,
  type RecommendationModel,
  type TechnicalModel,
  type WarningModel,
  type WarningSeverity,
} from "./PortalResultModel";
import type {
  AdapterOptions,
  CanonicalReportInput,
  PresentationChart,
  PresentationRecommendation,
  PresentationWarning,
  ReportPresentationEnvelope,
} from "./reportInput";
import {
  identityIsComplete,
  isDomainKey,
  isHeroStatus,
  isUserSafeMessage,
} from "./ContractValidator";
import { buildChrome, domainLabel, statusLabel, t } from "../formatters/labels";
import { parseOptionalNumber } from "../formatters/number";
import { requiredText, stringifyMetaValue, trimText } from "../formatters/text";
import { formatTechnicalDate } from "../formatters/date";
import { clampSummaryBullets } from "../utils/clamp";
import { collectIdsByDomain } from "../utils/grouping";
import { compareNullablePriority } from "../utils/sorting";
import { buildNavModel } from "../utils/visibility";
import { DOMAIN_ORDER } from "./PortalResultModel";

function emptyTechnical(): TechnicalModel {
  return {
    collapsed: true,
    calendar: null,
    pillars: null,
    timezone: null,
    schema: null,
    ids: null,
    metadata: null,
    available: false,
  };
}

function emptyDomains(): DomainMapModel {
  return {
    career: emptyDomain("career"),
    wealth: emptyDomain("wealth"),
    relationship: emptyDomain("relationship"),
    health: emptyDomain("health"),
    luck: emptyDomain("luck"),
  };
}

function emptyDomain(key: DomainKey): DomainModel {
  return {
    key,
    title: domainLabel(key),
    available: false,
    intro: null,
    recommendation_ids: [],
    analysis_preview: null,
    analysis_detail: null,
    analysis_expanded: false,
  };
}

function shellModel(
  state: PageState,
  errorCode: string | null,
  errorMessage: string | null,
): PortalResultModel {
  const chrome = buildChrome();
  const domains = emptyDomains();
  const technical = emptyTechnical();
  return {
    contract_id: RESULT_UI_CONTRACT_ID,
    contract_version: RESULT_UI_CONTRACT_VERSION,
    page: {
      state,
      partial: state === "partial_ready",
      error_code: errorCode,
      error_message: errorMessage,
    },
    hero: null,
    summary: null,
    recommendations: [],
    warnings: [],
    domains,
    charts: [],
    technical,
    knowledge: [],
    appendix: null,
    cta: {
      primary_label: t("i18n.cta.primary"),
      primary_enabled: false,
      secondary_label: t("i18n.cta.secondary"),
      secondary_enabled: false,
    },
    nav: buildNavModel(chrome, state, domains, [], [], technical, [], null),
    chrome,
  };
}

function mapHeroStatus(value: unknown): HeroStatus {
  const text = trimText(value);
  if (text && isHeroStatus(text)) return text;
  return "ready";
}

function mapSeverity(value: unknown): WarningSeverity {
  return trimText(value) === "critical" ? "critical" : "attention";
}

function mapRecommendation(
  item: PresentationRecommendation,
  index: number,
): RecommendationModel | null {
  const domainRaw = trimText(item.domain);
  if (!domainRaw || !isDomainKey(domainRaw)) return null;
  const title = trimText(item.title);
  const reason = trimText(item.reason);
  const expected = trimText(item.expected_result);
  const action = trimText(item.action);
  if (!title || !reason || !expected || !action) return null;
  const id = trimText(item.id) ?? `rec-${domainRaw}-${index}`;
  return {
    id,
    domain: domainRaw,
    domain_label: domainLabel(domainRaw),
    title,
    reason,
    expected_result: expected,
    action,
    detail: trimText(item.detail),
    expanded: false,
    priority: parseOptionalNumber(item.priority),
  };
}

function mapWarning(item: PresentationWarning): WarningModel | null {
  const title = trimText(item.title);
  const body = trimText(item.body);
  if (!title || !body) return null;
  return {
    title,
    body,
    mitigation: trimText(item.mitigation),
    severity: mapSeverity(item.severity),
    expanded: false,
  };
}

function mapChart(item: PresentationChart): ChartModel | null {
  const title = trimText(item.title);
  const caption = trimText(item.caption);
  const assetRef = trimText(item.asset_ref);
  if (!title || !caption || !assetRef) return null;
  let table: ChartTable | null = null;
  if (item.table && Array.isArray(item.table.headers) && Array.isArray(item.table.rows)) {
    table = {
      headers: item.table.headers.map((header) => requiredText(header)),
      rows: item.table.rows.map((row) => row.map((cell) => requiredText(cell))),
    };
  }
  return {
    title,
    caption,
    asset_ref: assetRef,
    table,
    table_expanded: false,
  };
}

function mapKnowledge(item: PresentationKnowledgeLike): KnowledgeModel | null {
  const title = trimText(item.title);
  const teaser = trimText(item.teaser);
  if (!title || !teaser) return null;
  return {
    title,
    teaser,
    body: trimText(item.body),
    expanded: false,
  };
}

type PresentationKnowledgeLike = { title?: string | null; teaser?: string | null; body?: string | null };

function mapAppendix(envelope: ReportPresentationEnvelope): AppendixModel | null {
  const scope = trimText(envelope.appendix?.scope);
  const reread = trimText(envelope.appendix?.reread);
  const limits = trimText(envelope.appendix?.limits);
  if (!scope && !reread && !limits) return null;
  return { scope, reread, limits };
}

function mapTechnical(
  envelope: ReportPresentationEnvelope,
  input: CanonicalReportInput,
): TechnicalModel {
  const src = envelope.technical;
  const artifact = input.canonical_report_artifact;
  const calendar = trimText(src?.calendar);
  const pillars = trimText(src?.pillars);
  const timezone = trimText(src?.timezone);
  const schema =
    trimText(src?.schema) ?? trimText(input.report_pipeline_version);
  const ids = trimText(src?.ids) ?? trimText(artifact?.artifact_id);
  const metadata: Record<string, string> = {};
  const sourceMeta = src?.metadata ?? artifact?.metadata;
  if (sourceMeta && typeof sourceMeta === "object") {
    for (const [key, value] of Object.entries(sourceMeta)) {
      const formatted = stringifyMetaValue(value) ?? formatTechnicalDate(value);
      if (formatted) metadata[key] = formatted;
    }
  }
  const metaKeys = Object.keys(metadata);
  const available = Boolean(
    calendar || pillars || timezone || schema || ids || metaKeys.length > 0,
  );
  return {
    collapsed: true,
    calendar,
    pillars,
    timezone,
    schema,
    ids,
    metadata: metaKeys.length > 0 ? metadata : null,
    available,
  };
}

function mapDomains(
  envelope: ReportPresentationEnvelope,
  recommendations: RecommendationModel[],
): DomainMapModel {
  const result = emptyDomains();
  for (const key of DOMAIN_ORDER) {
    const src = envelope.domains?.[key];
    const intro = trimText(src?.intro);
    const preview = trimText(src?.analysis_preview);
    const detail = trimText(src?.analysis_detail);
    const declaredIds = Array.isArray(src?.recommendation_ids)
      ? src.recommendation_ids.map((id) => trimText(id)).filter((id): id is string => Boolean(id))
      : [];
    const recIds = declaredIds.length > 0 ? declaredIds : collectIdsByDomain(recommendations, key);
    const available =
      src?.available === true ||
      Boolean(intro || preview || detail || recIds.length > 0);
    result[key] = {
      key,
      title: domainLabel(key),
      available,
      intro,
      recommendation_ids: recIds,
      analysis_preview: preview,
      analysis_detail: detail,
      analysis_expanded: false,
    };
  }
  return result;
}

function derivePageState(args: {
  options: AdapterOptions;
  input: CanonicalReportInput | null;
  envelopeMissing: boolean;
  heroOk: boolean;
  summaryOk: boolean;
  recs: RecommendationModel[];
  domains: DomainMapModel;
}): { state: PageState; errorCode: string | null; errorMessage: string | null } {
  if (args.options.offline) {
    return { state: "offline", errorCode: null, errorMessage: null };
  }
  if (args.options.loading) {
    return { state: "loading", errorCode: null, errorMessage: null };
  }
  if (!args.input) {
    return {
      state: "error",
      errorCode: "RESULT_NULL",
      errorMessage: t("i18n.error.page"),
    };
  }
  if (args.envelopeMissing) {
    if (args.input.success === false) {
      return {
        state: "error",
        errorCode: "REPORT_FAILED",
        errorMessage: userSafeError(args.input),
      };
    }
    return { state: "empty", errorCode: null, errorMessage: null };
  }
  if (!args.heroOk) {
    return {
      state: "error",
      errorCode: "HERO_INCOMPLETE",
      errorMessage: t("i18n.error.page"),
    };
  }
  if (!args.summaryOk) {
    return {
      state: "error",
      errorCode: "SUMMARY_EMPTY",
      errorMessage: t("i18n.error.page"),
    };
  }
  const allDomains = DOMAIN_ORDER.every((key) => args.domains[key].available);
  const recsOk = args.recs.length > 0;
  let state: PageState = recsOk && allDomains ? "ready" : "partial_ready";
  if (args.options.printing) state = "printing";
  if (args.options.exporting) state = "exporting";
  return { state, errorCode: null, errorMessage: null };
}

function userSafeError(input: CanonicalReportInput): string {
  const first = input.errors?.find((item) => trimText(item) && isUserSafeMessage(String(item)));
  if (first) return requiredText(first);
  return t("i18n.error.page");
}

function ctaEnabled(pageState: PageState, flag: boolean): boolean {
  if (
    pageState === "loading" ||
    pageState === "error" ||
    pageState === "empty" ||
    pageState === "offline" ||
    pageState === "printing" ||
    pageState === "exporting"
  ) {
    return false;
  }
  return flag;
}

/**
 * Map Canonical Report input to PortalResultModel.
 */
export function adaptPortalResult(
  input: CanonicalReportInput | null,
  options: AdapterOptions = {},
): PortalResultModel {
  if (options.loading) return shellModel("loading", null, null);
  if (options.offline) return shellModel("offline", null, null);
  if (!input) return shellModel("error", "RESULT_NULL", t("i18n.error.page"));

  const envelope = input.presentation ?? null;
  const envelopeMissing = envelope === null;
  const chrome = buildChrome();

  const heroOk = identityIsComplete(envelope?.identity ?? null);
  const bullets = clampSummaryBullets(envelope?.summary?.bullets ?? []);
  const summaryOk = bullets.length > 0;

  const recommendations = (envelope?.recommendations ?? [])
    .map((item, index) => mapRecommendation(item, index))
    .filter((item): item is RecommendationModel => item !== null)
    .sort((a, b) => compareNullablePriority(a.priority, b.priority));

  const warnings = (envelope?.warnings ?? [])
    .map((item) => mapWarning(item))
    .filter((item): item is WarningModel => item !== null);

  const charts = (envelope?.charts ?? [])
    .map((item) => mapChart(item))
    .filter((item): item is ChartModel => item !== null);

  const knowledge = (envelope?.knowledge ?? [])
    .map((item) => mapKnowledge(item))
    .filter((item): item is KnowledgeModel => item !== null);

  const appendix = envelope ? mapAppendix(envelope) : null;
  const technical = envelope ? mapTechnical(envelope, input) : emptyTechnical();
  const domains = envelope ? mapDomains(envelope, recommendations) : emptyDomains();

  const derived = derivePageState({
    options,
    input,
    envelopeMissing,
    heroOk,
    summaryOk,
    recs: recommendations,
    domains,
  });

  let hero: HeroModel | null = null;
  let summary = null;
  if (heroOk && envelope?.identity) {
    const status = mapHeroStatus(envelope.identity.consultation_status);
    hero = {
      name: requiredText(envelope.identity.full_name),
      headline: requiredText(envelope.identity.headline),
      one_line_summary: requiredText(envelope.identity.one_line_summary),
      status,
      status_label: statusLabel(status),
    };
  }
  if (summaryOk) {
    summary = { title: chrome.section_summary, bullets };
  }

  if (derived.state === "error" || derived.state === "empty") {
    hero = null;
    summary = null;
  }

  const primaryEnabled = ctaEnabled(
    derived.state,
    envelope?.cta?.primary?.enabled === true,
  );
  const secondaryOn = envelope?.cta?.secondary?.enabled === true;
  const secondaryEnabled = ctaEnabled(derived.state, secondaryOn);

  const readingStates: PageState[] = ["ready", "partial_ready", "printing", "exporting"];
  const showCtaSecondary =
    readingStates.includes(derived.state) && secondaryOn;

  const model: PortalResultModel = {
    contract_id: RESULT_UI_CONTRACT_ID,
    contract_version: RESULT_UI_CONTRACT_VERSION,
    page: {
      state: derived.state,
      partial: derived.state === "partial_ready",
      error_code: derived.errorCode,
      error_message: derived.errorMessage,
    },
    hero: readingStates.includes(derived.state) ? hero : null,
    summary: readingStates.includes(derived.state) ? summary : null,
    recommendations: readingStates.includes(derived.state) ? recommendations : [],
    warnings: readingStates.includes(derived.state) ? warnings : [],
    domains: readingStates.includes(derived.state) ? domains : emptyDomains(),
    charts: readingStates.includes(derived.state) ? charts : [],
    technical: readingStates.includes(derived.state) ? technical : emptyTechnical(),
    knowledge: readingStates.includes(derived.state) ? knowledge : [],
    appendix: readingStates.includes(derived.state) ? appendix : null,
    cta: {
      primary_label: t("i18n.cta.primary"),
      primary_enabled: primaryEnabled,
      secondary_label: showCtaSecondary ? t("i18n.cta.secondary") : null,
      secondary_enabled: secondaryEnabled,
    },
    nav: buildNavModel(
      chrome,
      derived.state,
      readingStates.includes(derived.state) ? domains : emptyDomains(),
      readingStates.includes(derived.state) ? warnings : [],
      readingStates.includes(derived.state) ? charts : [],
      readingStates.includes(derived.state) ? technical : emptyTechnical(),
      readingStates.includes(derived.state) ? knowledge : [],
      readingStates.includes(derived.state) ? appendix : null,
    ),
    chrome,
  };

  return model;
}
