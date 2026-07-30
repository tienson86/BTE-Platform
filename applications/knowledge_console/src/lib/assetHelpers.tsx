import type { AssetStatus, AssetType } from "../api/types";

export const ASSET_TYPE_LABELS: Record<AssetType, string> = {
  rule: "Rule",
  sentence: "Sentence",
  phrase: "Phrase",
  terminology: "Terminology",
};

export function statusClass(status: AssetStatus): string {
  switch (status) {
    case "draft":
      return "bg-[var(--accent-soft)] text-[var(--accent)]";
    case "review":
      return "bg-[rgba(138,106,31,0.15)] text-[var(--warn)]";
    case "approved":
      return "bg-[rgba(31,122,92,0.15)] text-[var(--accent)]";
    case "released":
      return "bg-[rgba(31,122,92,0.22)] text-[var(--accent)]";
    case "rejected":
      return "bg-[rgba(155,59,47,0.15)] text-[var(--danger)]";
    default:
      return "bg-[var(--accent-soft)] text-[var(--muted)]";
  }
}

export function StatusBadge({ status }: { status: AssetStatus }) {
  return (
    <span
      className={`inline-flex rounded px-2 py-0.5 text-[11px] font-medium uppercase tracking-wide ${statusClass(status)}`}
    >
      {status}
    </span>
  );
}

export function emptyContent(type: AssetType): Record<string, unknown> {
  switch (type) {
    case "rule":
      return {
        rule_id: "",
        condition: "",
        action: "",
        priority: 50,
      };
    case "sentence":
      return {
        sentence_id: "",
        template: "",
        section_id: "",
        placeholders: [],
      };
    case "phrase":
      return {
        phrase_id: "",
        text: "",
        type: "general",
        tags: [],
      };
    case "terminology":
      return {
        term_id: "",
        display_name: "",
        domain: "",
        status: "active",
      };
  }
}
