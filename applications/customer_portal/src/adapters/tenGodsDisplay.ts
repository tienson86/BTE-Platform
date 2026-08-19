/**
 * Presentation helpers for canonical Ten Gods payload.
 * Copies labels from API data. Does not recalculate Ten Gods.
 */

export type TenGodEntry = {
  readonly pillar?: string;
  readonly stem?: string;
  readonly hidden_stem?: string;
  readonly branch?: string;
  readonly element?: string;
  readonly ten_god?: string;
  readonly display?: string;
  readonly visibility?: string;
};

export type TenGodsPayload = {
  readonly visible?: readonly (string | TenGodEntry)[];
  readonly hidden?: readonly (string | TenGodEntry)[];
  readonly visible_labels?: readonly string[];
  readonly hidden_labels?: readonly string[];
  readonly visible_summary?: string;
  readonly hidden_summary?: string;
  readonly note?: string;
};

const TEN_GODS_NOTE = "Xác định theo quan hệ Ngũ hành và âm dương với Nhật chủ.";

const PILLAR_KEYS = ["year", "month", "day", "hour"] as const;

export function asTenGodsPayload(value: unknown): TenGodsPayload | null {
  if (!value || typeof value !== "object" || Array.isArray(value)) return null;
  const payload = value as TenGodsPayload;
  if (payload.visible == null && payload.hidden == null && payload.visible_labels == null) {
    return null;
  }
  return payload;
}

export function tenGodLabel(item: unknown): string {
  if (typeof item === "string") return item.trim();
  if (item && typeof item === "object" && "ten_god" in item) {
    return String((item as TenGodEntry).ten_god || "").trim();
  }
  return "";
}

export function visibleLabels(payload: TenGodsPayload | null | undefined): string[] {
  if (!payload) return [];
  if (Array.isArray(payload.visible_labels) && payload.visible_labels.length) {
    return payload.visible_labels.map(String).filter(Boolean);
  }
  return (payload.visible ?? []).map(tenGodLabel).filter(Boolean);
}

export function hiddenLabels(payload: TenGodsPayload | null | undefined): string[] {
  if (!payload) return [];
  if (Array.isArray(payload.hidden_labels) && payload.hidden_labels.length) {
    return unique(payload.hidden_labels.map(String).filter(Boolean));
  }
  return unique((payload.hidden ?? []).map(tenGodLabel).filter(Boolean));
}

export function visibleEntryForPillar(
  payload: TenGodsPayload | null | undefined,
  pillar: (typeof PILLAR_KEYS)[number],
): TenGodEntry | null {
  const visible = payload?.visible ?? [];
  for (const item of visible) {
    if (item && typeof item === "object" && item.pillar === pillar) return item;
  }
  return null;
}

export function hiddenEntries(
  payload: TenGodsPayload | null | undefined,
): TenGodEntry[] {
  if (!payload) return [];
  return (payload.hidden ?? []).filter(
    (item): item is TenGodEntry => Boolean(item) && typeof item === "object",
  );
}

export function hiddenLinesForPillar(
  payload: TenGodsPayload | null | undefined,
  pillar: (typeof PILLAR_KEYS)[number],
): string[] {
  return hiddenEntries(payload)
    .filter((item) => item.pillar === pillar)
    .map((item) => hiddenDisplay(item))
    .filter(Boolean);
}

export function hiddenDisplay(item: TenGodEntry): string {
  if (item.display) return item.display;
  return [item.hidden_stem || item.stem, item.element, item.ten_god]
    .map((part) => String(part || "").trim())
    .filter(Boolean)
    .join(" · ");
}

export function stemDisplay(stem: string, element?: string): string {
  const name = stem.trim();
  const el = (element || "").trim();
  if (name && el) return `${name} · ${el}`;
  return name;
}

export function tenGodsNote(payload: TenGodsPayload | null | undefined): string {
  return payload?.note?.trim() || TEN_GODS_NOTE;
}

function unique(values: string[]): string[] {
  return [...new Set(values)];
}
