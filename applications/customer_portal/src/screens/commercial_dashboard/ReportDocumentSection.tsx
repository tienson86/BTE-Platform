/**
 * Customer-facing Bát Tự report document.
 */

import type { ReactNode } from "react";
import type { BaziReportDocumentChapterView, BaziReportDocumentView } from "./types";

type ReportDocumentSectionProps = {
  readonly model: BaziReportDocumentView;
};

function ReportChapter({ chapter }: { readonly chapter: BaziReportDocumentChapterView }): ReactNode {
  return (
    <section className="bte-report-doc__chapter" data-report-chapter={chapter.id}>
      <h3 className="bte-report-doc__chapter-title">{chapter.title}</h3>
      {chapter.paragraphs.map((paragraph, index) => (
        <p key={`${chapter.id}-p-${index}`} className="bte-report-doc__paragraph">
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
  return (
    <section className="bte-report-doc" data-report-document="bazi-v1" aria-labelledby="bazi-report-document-title">
      <header className="bte-report-doc__header">
        <p className="bte-report-doc__eyebrow">Hồ sơ luận giải</p>
        <h2 id="bazi-report-document-title" className="bte-report-doc__title">
          {model.title}
        </h2>
        {model.subtitle ? <p className="bte-report-doc__subtitle">{model.subtitle}</p> : null}
      </header>
      <div className="bte-report-doc__body">
        {model.chapters.map((chapter) => (
          <ReportChapter key={chapter.id} chapter={chapter} />
        ))}
      </div>
    </section>
  );
}
