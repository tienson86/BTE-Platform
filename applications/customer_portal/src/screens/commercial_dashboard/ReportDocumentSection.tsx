/**
 * Customer-facing Bát Tự report document.
 */

import type { ReactNode } from "react";
import type {
  BaziReportDocumentChapterView,
  BaziReportDocumentView,
  BaziReportFiveElementsView,
  BaziReportLuckCycleView,
  BaziReportLuckView,
} from "./types";

type ReportDocumentSectionProps = {
  readonly model: BaziReportDocumentView;
};

function ReportFiveElementsVisual({ model }: { readonly model: BaziReportFiveElementsView }): ReactNode {
  return (
    <aside className="bte-report-doc__visual bte-report-doc__visual--elements" aria-label="Biểu đồ Ngũ hành">
      <header className="bte-report-doc__visual-head">
        <p className="bte-report-doc__visual-kicker">Biểu đồ Ngũ hành</p>
        <h4 className="bte-report-doc__visual-title">Phân bố khí trong lá số</h4>
      </header>
      <div className="bte-report-doc__element-chart">
        {model.items.map((item) => {
          const height = `${Math.max(8, Math.round((item.count / model.maxCount) * 100))}%`;
          return (
            <div key={item.key} className="bte-report-doc__element" data-element={item.key}>
              <span className="bte-report-doc__element-label">{item.label}</span>
              <span className="bte-report-doc__element-track" aria-hidden="true">
                <span className="bte-report-doc__element-bar" style={{ height }} />
              </span>
              <span className="bte-report-doc__element-count">{item.count}</span>
            </div>
          );
        })}
      </div>
      <div className="bte-report-doc__insight-row">
        {model.dominantLabel ? (
          <span className="bte-report-doc__insight-chip">Nổi bật: {model.dominantLabel}</span>
        ) : null}
        {model.weakLabel ? (
          <span className="bte-report-doc__insight-chip">Cần bồi: {model.weakLabel}</span>
        ) : null}
      </div>
      {model.methodNote ? <p className="bte-report-doc__visual-note">{model.methodNote}</p> : null}
    </aside>
  );
}

function cycleElementHits(cycle: BaziReportLuckCycleView, elements: readonly string[]): string {
  const hits = elements.filter((element) => cycle.elements.includes(element));
  return hits.join(", ");
}

function ReportLuckVisual({ model }: { readonly model: BaziReportLuckView }): ReactNode {
  return (
    <aside className="bte-report-doc__visual bte-report-doc__visual--luck" aria-label="Timeline Đại vận">
      <header className="bte-report-doc__visual-head">
        <p className="bte-report-doc__visual-kicker">Timeline Đại vận</p>
        <h4 className="bte-report-doc__visual-title">Nhịp vận theo từng giai đoạn</h4>
      </header>
      <div className="bte-report-doc__luck-summary">
        {model.direction ? <span>Chiều vận: {model.direction}</span> : null}
        {model.startAge ? <span>Khởi vận: {model.startAge} tuổi</span> : null}
        {model.currentLabel ? <span>Hiện tại: {model.currentLabel}</span> : null}
      </div>
      <ol className="bte-report-doc__luck-list">
        {model.cycles.map((cycle, index) => {
          const usefulHits = cycleElementHits(cycle, model.usefulElements);
          const cautionHits = cycleElementHits(cycle, model.unfavorableElements);
          return (
            <li
              key={`${cycle.ganZhi}-${cycle.ageRange}-${index}`}
              className="bte-report-doc__luck-cycle"
              data-current={cycle.isCurrent ? "true" : undefined}
            >
              <div className="bte-report-doc__luck-top">
                <span className="bte-report-doc__luck-index">{String(index + 1).padStart(2, "0")}</span>
                <div>
                  <strong>{cycle.ganZhi}</strong>
                  <span>{[cycle.ageRange, cycle.yearRange].filter(Boolean).join(" · ")}</span>
                </div>
              </div>
              {cycle.elements ? <p className="bte-report-doc__luck-elements">{cycle.elements}</p> : null}
              <div className="bte-report-doc__luck-points">
                <p>
                  <span>+</span>
                  {usefulHits ? `Chạm trục nên dùng: ${usefulHits}.` : "Có thể mở việc khi mục tiêu và nhịp hành động rõ."}
                </p>
                <p>
                  <span>-</span>
                  {cautionHits ? `Cần tiết chế: ${cautionHits}.` : "Cần đọc cùng mệnh cục gốc trước quyết định lớn."}
                </p>
              </div>
            </li>
          );
        })}
      </ol>
    </aside>
  );
}

function ReportChapterVisual({
  chapter,
  model,
}: {
  readonly chapter: BaziReportDocumentChapterView;
  readonly model: BaziReportDocumentView;
}): ReactNode {
  if (chapter.id === "five_elements" && model.fiveElements) {
    return <ReportFiveElementsVisual model={model.fiveElements} />;
  }
  if (chapter.id === "luck_cycles" && model.luck) {
    return <ReportLuckVisual model={model.luck} />;
  }
  return null;
}

function ReportChapter({
  chapter,
  index,
  model,
}: {
  readonly chapter: BaziReportDocumentChapterView;
  readonly index: number;
  readonly model: BaziReportDocumentView;
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
      <ReportChapterVisual chapter={chapter} model={model} />
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
            <ReportChapter key={chapter.id} chapter={chapter} index={index} model={model} />
          ))}
        </div>
      </div>
    </section>
  );
}
