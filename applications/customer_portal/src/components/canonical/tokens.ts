/**
 * Presentation token maps for Tứ Trụ badges.
 * Colors reuse the existing portal element badge palette.
 * This is display styling only — not identity calculation.
 */

const NAP_AM_TOKEN: Record<string, string> = {
  Mộc: "moc",
  Hỏa: "hoa",
  Thổ: "tho",
  Kim: "kim",
  Thủy: "thuy",
};

const CUNG_TOKEN: Record<string, string> = {
  Khảm: "thuy",
  Ly: "hoa",
  Chấn: "moc",
  Tốn: "moc",
  Càn: "kim",
  Khôn: "tho",
  Cấn: "tho",
  Đoài: "kim",
};

function foldVi(value: string): string {
  return value.trim().toLocaleLowerCase("vi");
}

function matchKnown(value: string, table: Record<string, string>): string | null {
  const trimmed = value.trim();
  if (!trimmed) return null;
  if (table[trimmed]) return table[trimmed];
  const folded = foldVi(trimmed);
  for (const [label, token] of Object.entries(table)) {
    if (foldVi(label) === folded) return token;
  }
  return null;
}

/**
 * Resolve a Nạp âm label to an existing element badge token.
 */
export function napAmBadgeToken(value: string): string | null {
  const direct = matchKnown(value, NAP_AM_TOKEN);
  if (direct) return direct;
  const folded = foldVi(value);
  for (const [label, token] of Object.entries(NAP_AM_TOKEN)) {
    if (folded.endsWith(foldVi(label))) return token;
  }
  return null;
}

/**
 * Resolve a Cung Phi label to the matching element badge token.
 */
export function cungPhiBadgeToken(value: string): string | null {
  return matchKnown(value, CUNG_TOKEN);
}
