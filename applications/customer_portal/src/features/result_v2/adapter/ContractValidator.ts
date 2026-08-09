/**
 * UI Contract validation — presence only, no business logic.
 */

import type { DomainKey, HeroStatus } from "./PortalResultModel";
import { DOMAIN_ORDER } from "./PortalResultModel";
import type { PresentationIdentity, ReportPresentationEnvelope } from "./reportInput";
import { trimText } from "../formatters/text";

export type ValidationIssue = {
  code: string;
  field: string;
};

export const DOMAIN_KEYS: readonly DomainKey[] = DOMAIN_ORDER;

export function isDomainKey(value: string): value is DomainKey {
  return (DOMAIN_KEYS as readonly string[]).includes(value);
}

export function isHeroStatus(value: string): value is HeroStatus {
  return (
    value === "ready" ||
    value === "partial" ||
    value === "in_progress" ||
    value === "error"
  );
}

export function identityIsComplete(identity: PresentationIdentity | null | undefined): boolean {
  if (!identity) return false;
  return Boolean(
    trimText(identity.full_name) &&
      trimText(identity.headline) &&
      trimText(identity.one_line_summary) &&
      trimText(identity.consultation_status),
  );
}

export function validatePresentation(
  envelope: ReportPresentationEnvelope | null | undefined,
): ValidationIssue[] {
  const issues: ValidationIssue[] = [];
  if (!envelope) {
    issues.push({ code: "PRESENTATION_MISSING", field: "presentation" });
    return issues;
  }
  if (!identityIsComplete(envelope.identity ?? null)) {
    issues.push({ code: "HERO_INCOMPLETE", field: "report.identity" });
  }
  const bullets = envelope.summary?.bullets;
  const hasBullet =
    Array.isArray(bullets) && bullets.some((item) => Boolean(trimText(item)));
  if (!hasBullet) {
    issues.push({ code: "SUMMARY_EMPTY", field: "report.summary.bullets" });
  }
  return issues;
}

export function isUserSafeMessage(value: string): boolean {
  const lower = value.toLowerCase();
  if (lower.includes("traceback")) return false;
  if (lower.includes("exception")) return false;
  if (lower.includes("stack")) return false;
  if (lower.includes("pipeline")) return false;
  if (lower.includes("engine")) return false;
  return true;
}
