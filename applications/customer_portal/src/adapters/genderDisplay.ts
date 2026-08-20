/**
 * Customer-facing gender labels. Internal API remains male/female.
 */

const MALE_ALIASES = new Set(["male", "nam", "m", "1", "man", "boy"]);
const FEMALE_ALIASES = new Set(["female", "nu", "nữ", "f", "woman", "girl"]);

export function canonicalGender(raw: string | null | undefined): "male" | "female" | null {
  const key = (raw ?? "").trim().toLowerCase();
  if (!key) return null;
  if (MALE_ALIASES.has(key)) return "male";
  if (FEMALE_ALIASES.has(key)) return "female";
  return null;
}

export function genderDisplayLabel(raw: string | null | undefined): string {
  const canonical = canonicalGender(raw);
  if (canonical === "male") return "Nam";
  if (canonical === "female") return "Nữ";
  return "—";
}

export function customerGenderDisplay(
  customer?: { gender?: string | null; gender_label?: string | null } | null,
  fallback?: string | null,
): string {
  return genderDisplayLabel(customer?.gender_label || customer?.gender || fallback);
}
