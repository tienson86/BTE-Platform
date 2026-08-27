/**
 * Vietnamese calendar-date helpers. Values are civil dates, not timestamps.
 */

export type ParsedDate = {
  year: number;
  month: number;
  day: number;
  iso: string;
  display: string;
};

export type ParsedMonth = {
  year: number;
  month: number;
  iso: string;
  display: string;
};

function isLeapYear(year: number): boolean {
  return (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0;
}

function daysInMonth(year: number, month: number): number {
  const lengths = [31, isLeapYear(year) ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  return lengths[month - 1] ?? 0;
}

export function formatVnDate(year: number, month: number, day: number): string {
  return `${String(day).padStart(2, "0")}/${String(month).padStart(2, "0")}/${String(year).padStart(4, "0")}`;
}

export function formatVnMonth(year: number, month: number): string {
  return `Tháng ${String(month).padStart(2, "0")}/${year}`;
}

export function maskVnDate(raw: string): string {
  const digits = raw.replace(/\D/g, "").slice(0, 8);
  if (digits.length <= 2) return digits;
  if (digits.length <= 4) return `${digits.slice(0, 2)}/${digits.slice(2)}`;
  return `${digits.slice(0, 2)}/${digits.slice(2, 4)}/${digits.slice(4)}`;
}

export function maskVnMonth(raw: string): string {
  const digits = raw.replace(/\D/g, "").slice(0, 6);
  if (digits.length <= 2) return digits;
  return `${digits.slice(0, 2)}/${digits.slice(2)}`;
}

export function parseVnDate(text: string): ParsedDate | null {
  const match = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec(text.trim());
  if (!match) return null;
  const day = Number(match[1]);
  const month = Number(match[2]);
  const year = Number(match[3]);
  if (month < 1 || month > 12) return null;
  if (day < 1 || day > daysInMonth(year, month)) return null;
  return {
    year,
    month,
    day,
    iso: `${String(year).padStart(4, "0")}-${String(month).padStart(2, "0")}-${String(day).padStart(2, "0")}`,
    display: formatVnDate(year, month, day),
  };
}

export function parseVnMonth(text: string): ParsedMonth | null {
  const trimmed = text.trim().replace(/^Tháng\s+/i, "");
  const compact = /^(\d{2})\/(\d{4})$/.exec(trimmed);
  if (compact) {
    const month = Number(compact[1]);
    const year = Number(compact[2]);
    if (month < 1 || month > 12 || year < 1) return null;
    return {
      year,
      month,
      iso: `${year}-${String(month).padStart(2, "0")}`,
      display: formatVnMonth(year, month),
    };
  }
  const iso = /^(\d{4})-(\d{2})$/.exec(trimmed);
  if (!iso) return null;
  const year = Number(iso[1]);
  const month = Number(iso[2]);
  if (month < 1 || month > 12) return null;
  return {
    year,
    month,
    iso: `${year}-${String(month).padStart(2, "0")}`,
    display: formatVnMonth(year, month),
  };
}
