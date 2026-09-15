/**
 * Customer-facing Bát Tự report document.
 */

import type { ReactNode } from "react";
import type { BaziReportDocumentChapterView, BaziReportDocumentView } from "./types";

type ReportDocumentSectionProps = {
  readonly model: BaziReportDocumentView;
};

function ReportChapter({
  chapter,
  index,
}: {
  readonly chapter: BaziReportDocumentChapterView;
  readonly index: number;
}): ReactNode {
  const chapterNumber = String(index + 1).padStart(2, "0");
  const [leadParagraph, ...bodyParagraphs] = chapter.paragraphs;

  return (
    <section
      id={`bazi-report-${chapter.id}`}
      className="bte-report-doc__chapter"
      data-report-chapter={chapter.id}
    >
      <header className="bte-report-doc__chapter-head">
        <span className="bte-report-doc__chapter-number" aria-hidden="true">
          {chapterNumber}
        </span>
        <h3 className="bte-report-doc__chapter-title">{chapter.title}</h3>
      </header>
      {leadParagraph ? (
        <p className="bte-report-doc__lead">
          {leadParagraph}
        </p>
      ) : null}
      {bodyParagraphs.map((paragraph, paragraphIndex) => (
        <p key={`${chapter.id}-p-${paragraphIndex + 1}`} className="bte-report-doc__paragraph">
          {paragraph}
        </p>
      ))}
      {chapter.bullets.length ? (
        <ul className="bte-report-doc__bullets">
          {chapter.bullets.map((bullet, index) => (
            <li key={`${chapter.id}-b-${index}`}>{bullet}</li>
          ))}
        </ul>
      ) : null}
    </section>
  );
}

export function ReportDocumentSection({ model }: ReportDocumentSectionProps): ReactNode {
  const chapterCount = model.chapters.length;

  return (
    <section className="bte-report-doc" data-report-document="bazi-v1" aria-labelledby="bazi-report-document-title">
      <header className="bte-report-doc__header">
        <p className="bte-report-doc__eyebrow">Hồ sơ luận giải</p>
        <h2 id="bazi-report-document-title" className="bte-report-doc__title">
          {model.title}
        </h2>
        <div className="bte-report-doc__meta">
          {model.subtitle ? <p className="bte-report-doc__subtitle">{model.subtitle}</p> : null}
          <span className="bte-report-doc__count">{chapterCount} chương luận giải</span>
        </div>
      </header>
      <div className="bte-report-doc__layout">
        <nav className="bte-report-doc__toc" aria-label="Mục lục bản luận giải">
          <p className="bte-report-doc__toc-title">Mục lục</p>
          <ol className="bte-report-doc__toc-list">
            {model.chapters.map((chapter, index) => (
              <li key={chapter.id} className="bte-report-doc__toc-item">
                <a className="bte-report-doc__toc-link" href={`#bazi-report-${chapter.id}`}>
                  <span className="bte-report-doc__toc-index">{String(index + 1).padStart(2, "0")}</span>
                  <span>{chapter.title}</span>
                </a>
              </li>
            ))}
          </ol>
        </nav>
        <div className="bte-report-doc__body">
          {model.chapters.map((chapter, index) => (
            <ReportChapter key={chapter.id} chapter={chapter} index={index} />
          ))}
        </div>
      </div>
    </section>
  );
}
