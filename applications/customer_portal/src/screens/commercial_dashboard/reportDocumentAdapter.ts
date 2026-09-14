/**
 * Bát Tự report document adapter.
 * Reads only the customer-safe narrative contract from bazi_analysis_result.
 */

import type { AnalysisDataDto } from "../../models";
import type { BaziReportDocumentChapterView, BaziReportDocumentView } from "./types";

function asRecord(value: unknown): Record<string, unknown> | null {
  return value && typeof value === "object" && !Array.isArray(value)
    ? value as Record<string, unknown>
    : null;
}

function asArray(value: unknown): readonly unknown[] {
  return Array.isArray(value) ? value : [];
}

function toText(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

function textList(value: unknown): readonly string[] {
  return asArray(value)
    .map(toText)
    .filter(Boolean);
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
  };
}
