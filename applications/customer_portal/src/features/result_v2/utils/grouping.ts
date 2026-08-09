/**
 * Group recommendations by declared domain field — formatting only.
 */

import type { DomainKey, RecommendationModel } from "../adapter/PortalResultModel";
import { DOMAIN_ORDER } from "../adapter/PortalResultModel";

export type RecommendationGroup = {
  domain: DomainKey;
  domainLabel: string;
  items: RecommendationModel[];
};

export function groupRecommendations(
  items: RecommendationModel[],
): RecommendationGroup[] {
  return DOMAIN_ORDER.map((domain) => {
    const grouped = items.filter((item) => item.domain === domain);
    const domainLabel = grouped[0]?.domain_label ?? "";
    return { domain, domainLabel, items: grouped };
  });
}

export function collectIdsByDomain(
  items: RecommendationModel[],
  domain: DomainKey,
): string[] {
  return items.filter((item) => item.domain === domain).map((item) => item.id);
}
