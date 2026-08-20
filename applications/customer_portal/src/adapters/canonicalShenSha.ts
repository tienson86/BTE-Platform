/**
 * Copy canonical ShenSha matches from API. Do not recalculate stars.
 */

import type { AnalysisDataDto, BaziDto, ShenShaMatchDto } from "../models/dto";

export type ShenShaEntryView = {
  readonly id: string;
  readonly name: string;
  readonly presence: string;
  readonly evidence: string;
};

function asString(value: unknown): string {
  return typeof value === "string" ? value : value == null ? "" : String(value);
}

export function readShenShaMatches(bazi: BaziDto | undefined): readonly ShenShaMatchDto[] {
  const matches = bazi?.shensha_matches ?? [];
  return matches.filter((item) => asString(item.canonical_name || item.name).trim());
}

export function shenShaEntriesFromAnalysis(data: AnalysisDataDto): readonly ShenShaEntryView[] {
  const matches = readShenShaMatches(data.bazi);
  if (matches.length > 0) {
    return matches.map((item, index) => {
      const name = asString(item.canonical_name || item.name).trim();
      return {
        id: asString(item.id) || `ss-${index + 1}`,
        name,
        presence: asString(item.presence_label).trim() || "Có",
        evidence: asString(item.evidence_text).trim(),
      };
    });
  }
  const names = (data.bazi?.shensha ?? []).map((item) => asString(item).trim()).filter(Boolean);
  return names.map((name, index) => ({
    id: `ss-${index + 1}`,
    name,
    presence: "Có",
    evidence: "",
  }));
}
