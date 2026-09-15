/**
 * Bát Tự report document adapter.
 * Reads only the customer-safe narrative contract from bazi_analysis_result.
 */

import type { AnalysisDataDto } from "../../models";
import type {
  BaziReportDocumentChapterView,
  BaziReportDocumentView,
  BaziReportElementChartItemView,
  BaziReportFiveElementsView,
  BaziReportLuckCycleView,
  BaziReportLuckView,
  FiveElementKey,
} from "./types";

const ELEMENT_ORDER: readonly { readonly key: FiveElementKey; readonly label: string }[] = [
  { key: "wood", label: "Mộc" },
  { key: "fire", label: "Hỏa" },
  { key: "earth", label: "Thổ" },
  { key: "metal", label: "Kim" },
  { key: "water", label: "Thủy" },
];

function asRecord(value: unknown): Record<string, unknown> | null {
  return value && typeof value === "object" && !Array.isArray(value)
    ? value as Record<string, unknown>
    : null;
}

function asArray(value: unknown): readonly unknown[] {
  return Array.isArray(value) ? value : [];
}

function toText(value: unknown): string {
  if (typeof value === "string") return value.trim();
  if (typeof value === "number" && Number.isFinite(value)) return String(value);
  return "";
}

function textList(value: unknown): readonly string[] {
  return asArray(value)
    .map(toText)
    .filter(Boolean);
}

function technicalLuckAxis(analysis?: AnalysisDataDto | null): {
  readonly usefulElements: readonly string[];
  readonly unfavorableElements: readonly string[];
} {
  const raw = analysis as unknown as Record<string, unknown> | null | undefined;
  const contract = asRecord(raw?.bazi_analysis_result);
  const narrative = asRecord(contract?.customer_narrative);
  const luckCycles = asRecord(narrative?.luck_cycles);
  const balanceAxis = asRecord(luckCycles?.balance_axis);
  return {
    usefulElements: textList(balanceAxis?.useful_elements),
    unfavorableElements: textList(balanceAxis?.unfavorable_elements),
  };
}

function toNumber(value: unknown): number | null {
  if (typeof value === "number" && Number.isFinite(value)) return value;
  if (typeof value === "string" && value.trim() !== "" && Number.isFinite(Number(value))) {
    return Number(value);
  }
  return null;
}

function numericCount(value: unknown): number | null {
  const direct = toNumber(value);
  if (direct != null) return direct;
  const record = asRecord(value);
  return record ? toNumber(record.count) : null;
}

function copyElementCount(facts: Record<string, unknown>, key: FiveElementKey): number | null {
  const counts = asRecord(facts.counts);
  const fromCounts = numericCount(counts?.[key]);
  if (fromCounts != null) return fromCounts;
  return numericCount(facts[key]);
}

function chapterFromRecord(value: unknown, index: number): BaziReportDocumentChapterView | null {
  const record = asRecord(value);
  if (!record) return null;
  const title = toText(record.title);
  const paragraphs = textList(record.paragraphs);
  const bullets = textList(record.bullets);
  if (!title || (!paragraphs.length && !bullets.length)) return null;
  return {
    id: toText(record.id) || `chapter-${index + 1}`,
    title,
    paragraphs,
    bullets,
  };
}

function chaptersFromMarkdown(markdown: string): readonly BaziReportDocumentChapterView[] {
  type DraftChapter = {
    id: string;
    title: string;
    paragraphs: string[];
    bullets: string[];
  };

  const chapters: DraftChapter[] = [];
  let current: DraftChapter | null = null;

  markdown
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean)
    .forEach((line) => {
      const heading = line.match(/^#{2,3}\s+(.+)$/);
      if (heading) {
        current = {
          id: `chapter-${chapters.length + 1}`,
          title: heading[1].trim(),
          paragraphs: [],
          bullets: [],
        };
        chapters.push(current);
        return;
      }

      if (!current || line.startsWith("# ")) return;
      const bullet = line.match(/^[-*]\s+(.+)$/);
      if (bullet) {
        current.bullets.push(bullet[1].trim());
        return;
      }
      current.paragraphs.push(line);
    });

  return chapters.filter((chapter) => chapter.paragraphs.length || chapter.bullets.length);
}

function adaptReportFiveElements(analysis?: AnalysisDataDto | null): BaziReportFiveElementsView | null {
  const facts = asRecord(analysis?.five_elements);
  if (!facts) return null;
  const items = ELEMENT_ORDER
    .map((element): BaziReportElementChartItemView | null => {
      const count = copyElementCount(facts, element.key);
      return count == null ? null : { ...element, count };
    })
    .filter((item): item is BaziReportElementChartItemView => Boolean(item));
  if (!items.length) return null;
  const maxCount = Math.max(...items.map((item) => item.count), 1);
  const minCount = Math.min(...items.map((item) => item.count));
  const dominant = items.filter((item) => item.count === maxCount).map((item) => item.label);
  const weak = items.filter((item) => item.count === minCount).map((item) => item.label);
  return {
    items,
    maxCount,
    dominantLabel: dominant.join(", "),
    weakLabel: weak.join(", "),
    methodNote: toText(facts.method_note),
  };
}

function yearRange(start: unknown, end: unknown): string {
  const from = toNumber(start);
  const to = toNumber(end);
  return from == null || to == null ? "" : `${from}-${to}`;
}

function ageRange(start: unknown, end: unknown): string {
  const from = toNumber(start);
  const to = toNumber(end);
  return from == null || to == null ? "" : `${from}-${to} tuổi`;
}

function cycleKey(cycle: Record<string, unknown> | null): string {
  if (!cycle) return "";
  return [
    toText(cycle.gan_zhi),
    toText(cycle.age_start),
    toText(cycle.year_start),
  ].join("|");
}

function adaptReportLuck(analysis?: AnalysisDataDto | null): BaziReportLuckView | null {
  const luck = asRecord(analysis?.luck);
  if (!luck) return null;
  const rawCycles = asArray(luck.cycles)
    .map(asRecord)
    .filter((cycle): cycle is Record<string, unknown> => Boolean(cycle));
  const current = asRecord(luck.current_cycle);
  const currentKey = cycleKey(current);
  const currentGanZhi = toText(current?.gan_zhi);
  const cycles = rawCycles
    .map((cycle): BaziReportLuckCycleView | null => {
      const ganZhi = toText(cycle.gan_zhi);
      if (!ganZhi) return null;
      const elements = [toText(cycle.stem_element), toText(cycle.branch_element)]
        .filter(Boolean)
        .join(" / ");
      const isCurrent =
        cycleKey(cycle) === currentKey ||
        Boolean(currentGanZhi && ganZhi === currentGanZhi);
      return {
        ganZhi,
        ageRange: ageRange(cycle.age_start, cycle.age_end),
        yearRange: yearRange(cycle.year_start, cycle.year_end),
        elements,
        isCurrent,
      };
    })
    .filter((cycle): cycle is BaziReportLuckCycleView => Boolean(cycle));
  if (!cycles.length && !current) return null;
  const axis = technicalLuckAxis(analysis);
  return {
    direction: toText(luck.direction_label) || toText(luck.direction),
    startAge: toText(luck.start_age),
    currentLabel: currentGanZhi,
    usefulElements: axis.usefulElements,
    unfavorableElements: axis.unfavorableElements,
    cycles,
  };
}

export function adaptBaziReportDocument(
  analysis?: AnalysisDataDto | null,
): BaziReportDocumentView | null {
  const contract = asRecord(analysis?.bazi_analysis_result);
  const narrative = asRecord(contract?.customer_narrative);
  if (!narrative) return null;

  const reportDocument = asRecord(narrative.report_document);
  const markdown = toText(reportDocument?.markdown);
  const chapters = asArray(narrative.report_chapters)
    .map(chapterFromRecord)
    .filter((chapter): chapter is BaziReportDocumentChapterView => Boolean(chapter));
  const resolvedChapters = chapters.length ? chapters : chaptersFromMarkdown(markdown);

  if (!resolvedChapters.length) return null;
  return {
    title: toText(reportDocument?.title) || "Bản luận giải lá số Bát Tự",
    subtitle: toText(reportDocument?.subtitle),
    chapters: resolvedChapters,
    fiveElements: adaptReportFiveElements(analysis),
    luck: adaptReportLuck(analysis),
  };
}
