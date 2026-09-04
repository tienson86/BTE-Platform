/**
 * Bind Life Consulting from published evidence + authored profiles.
 * Lookup only. Does not calculate astrology or rewrite Narrative.
 */

import {
  LIFE_CONSULTING_TITLE,
  LIFE_DOMAIN_ORDER,
  lifeDomainProfileFor,
} from "./lifeConsultingAssets";
import { collectLifeConsultingEvidence } from "./lifeConsultingEvidence";
import type { AnalysisDataDto, AnalyzeChartRequest } from "../../models";
import type { LifeConsultingView, LifeDomainView } from "./types";

export type AdaptLifeConsultingOptions = {
  readonly request?: AnalyzeChartRequest | null;
};

/**
 * Attach life-domain consulting when published evidence matches an authored profile.
 * Omits a domain when no profile matches. Does not invent astrology.
 */
export function adaptLifeConsulting(
  data: AnalysisDataDto | null | undefined,
  options?: AdaptLifeConsultingOptions,
): LifeConsultingView {
  const evidence = collectLifeConsultingEvidence(data, {
    genderHint: options?.request?.gender,
  });
  const domains: LifeDomainView[] = [];
  for (const domain of LIFE_DOMAIN_ORDER) {
    const profile = lifeDomainProfileFor(domain, evidence);
    if (!profile) continue;
    domains.push({
      id: profile.domain,
      title: profile.title,
      insight: profile.insight,
      tendency: profile.tendency,
      strength: profile.strength,
      opportunity: profile.opportunity,
      risk: profile.risk,
      recommendation: profile.recommendation,
    });
  }
  return {
    title: LIFE_CONSULTING_TITLE,
    available: domains.length > 0,
    domains,
  };
}
