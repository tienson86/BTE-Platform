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

const DOMAIN_TITLE_RULES: ReadonlyArray<readonly [RegExp, string]> = [
  [/thanh khoản|dòng tiền|tiền\/tài sản|tiền và tài sản/i, "Dòng tiền và thanh khoản"],
  [/quản trị tiền|quản trị tài sản|kiểm soát rủi ro|nguồn lực thành tài sản/i, "Quản trị tài sản"],
  [/kim gặp hỏa|áp lực cạnh tranh|doanh số|mục tiêu doanh số/i, "Áp lực cạnh tranh"],
  [/cung phi|đông tứ trạch|tây tứ trạch|hướng nhà|hướng bàn|phong thủy|không gian/i, "Phong thủy ứng dụng"],
  [/kinh doanh|tài vận|tài sản|nguồn tiền|giữ tài/i, "Tài vận và kinh doanh"],
  [/sức khỏe|hô hấp|phổi|xoang|xương khớp|giấc ngủ|tiêu hóa|tỳ vị|thận/i, "Sức khỏe"],
  [/nghề nghiệp|công việc|sự nghiệp|nghề|chuyên môn/i, "Nghề nghiệp"],
  [/hôn nhân|phối ngẫu|tình cảm|quan hệ gần|vợ|chồng/i, "Hôn nhân và quan hệ"],
  [/hợp tác|đối tác|cộng sự|làm ăn chung|phân vai/i, "Hợp tác làm ăn"],
  [/con cái|tử tức|hậu vận|trụ giờ|dự án dài hạn/i, "Con cái và hậu vận"],
  [/bố mẹ|cha mẹ|gia đình|gia đạo|trụ tháng/i, "Gia đạo và nền nâng đỡ"],
  [/anh em|bạn bè|đồng hành|cạnh tranh ngang vai/i, "Quan hệ đồng hành"],
  [/tổ tiên|gia tộc|phúc khí|trụ năm/i, "Gốc gia tộc"],
  [/học hỏi|mở rộng|kỹ năng|kế hoạch dài hơi/i, "Học tập và phát triển"],
  [/đại vận|vận hiện tại|nhịp vận|giai đoạn/i, "Nhịp vận"],
];

const DOMAIN_GROUPS = [
  { id: "career", title: "Nghề nghiệp", cardTitle: "Luận nghề nghiệp", pattern: /nghề nghiệp|công việc|sự nghiệp|nghề|chuyên môn|học hỏi|mở rộng|kỹ năng|kế hoạch dài hơi/i },
  { id: "wealth", title: "Tài vận và kinh doanh", cardTitle: "Luận tài vận", pattern: /tài vận|kinh doanh|dòng tiền|thanh khoản|quản trị tài sản|quản trị tiền|doanh số|cạnh tranh|tài sản|nguồn tiền|giữ tài/i },
  { id: "marriage", title: "Hôn nhân và quan hệ", cardTitle: "Luận hôn nhân", pattern: /hôn nhân|phối ngẫu|tình cảm|quan hệ gần|vợ|chồng|hồng loan|duyên|cảm xúc/i },
  { id: "children", title: "Con cái và hậu vận", cardTitle: "Luận con cái/hậu vận", pattern: /con cái|tử tức|hậu vận|trụ giờ|dự án dài hạn|sinh con/i },
  { id: "health", title: "Sức khỏe", cardTitle: "Luận sức khỏe", pattern: /sức khỏe|hô hấp|phổi|xoang|xương khớp|giấc ngủ|tiêu hóa|tỳ vị|thận|tim mạch|gan mật|căng thẳng/i },
  { id: "family", title: "Gia đạo và nền gốc", cardTitle: "Luận gia đạo", pattern: /bố mẹ|cha mẹ|gia đình|gia đạo|trụ tháng|anh em|bạn bè|đồng hành|tổ tiên|gia tộc|phúc khí|trụ năm|gốc phúc/i },
  { id: "property", title: "Điền trạch và phong thủy", cardTitle: "Luận điền trạch", pattern: /điền trạch|cung phi|mệnh quái|đông tứ trạch|tây tứ trạch|nhóm trạch|hướng nhà|hướng bàn|phong thủy|không gian|nhà đất|ánh sáng|màu sắc|vật liệu|độ thoáng|bếp|cửa|bàn làm việc|dụng thần|ngũ hành|hành nổi bật|hành còn yếu|hành còn thiếu/i },
  { id: "luck", title: "Đại vận và thời điểm", cardTitle: "Luận vận", pattern: /đại vận|vận hiện tại|nhịp vận|giai đoạn|lưu niên/i },
] as const;

type DomainGroup = (typeof DOMAIN_GROUPS)[number];
type DomainItem = {
  readonly title: string;
  readonly body: string;
  readonly group: DomainGroup;
};

function inferDomainTitle(paragraph: string, index: number): string {
  const normalized = paragraph.toLocaleLowerCase("vi-VN");
  const matched = DOMAIN_TITLE_RULES.find(([pattern]) => pattern.test(normalized));
  return matched ? matched[1] : `Góc nhìn ${index + 1}`;
}

function inferDomainGroup(title: string, body: string): DomainGroup {
  const value = `${title} ${body}`;
  return DOMAIN_GROUPS.find((group) => group.pattern.test(value)) ?? DOMAIN_GROUPS[0];
}

function splitDomainParagraph(paragraph: string, index: number): DomainItem {
  const colonIndex = paragraph.indexOf(":");
  const title = colonIndex <= 0 ? inferDomainTitle(paragraph, index) : paragraph.slice(0, colonIndex).trim();
  const body = colonIndex <= 0 ? paragraph : paragraph.slice(colonIndex + 1).trim();
  return { title, body, group: inferDomainGroup(title, body) };
}

function groupDomainItems(items: readonly DomainItem[]): ReadonlyArray<{
  readonly group: DomainGroup;
  readonly items: readonly DomainItem[];
}> {
  return DOMAIN_GROUPS
    .map((group) => ({
      group,
      items: items.filter((item) => item.group.id === group.id),
    }))
    .filter((entry) => entry.items.length);
}

function ReportLifeDomainsVisual({
  paragraphs,
}: {
  readonly paragraphs: readonly string[];
}): ReactNode {
  const items = paragraphs
    .map((paragraph, index) => splitDomainParagraph(paragraph, index))
    .filter((item) => item.body);
  const groups = groupDomainItems(items);
  if (!items.length) return null;
  return (
    <aside className="bte-report-doc__visual bte-report-doc__visual--domains" aria-label="Các mục đời sống">
      <header className="bte-report-doc__visual-head">
        <p className="bte-report-doc__visual-kicker">Ứng dụng đời sống</p>
        <h4 className="bte-report-doc__visual-title">Các mảng cần đọc từ lá số gốc</h4>
      </header>
      {groups.map((entry) => (
        <section key={entry.group.id} className="bte-report-doc__domain-group">
          <h5 className="bte-report-doc__domain-group-title">{entry.group.title}</h5>
          <div className="bte-report-doc__domain-grid">
            {entry.items.map((item, index) => (
              <article key={`${entry.group.id}-${index}`} className="bte-report-doc__domain-card">
                <span className="bte-report-doc__domain-index">{String(index + 1).padStart(2, "0")}</span>
                <h6>{`${entry.group.cardTitle} ${index + 1}`}</h6>
                <p className="bte-report-doc__domain-topic">{item.title}</p>
                <p>{item.body}</p>
              </article>
            ))}
          </div>
        </section>
      ))}
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
  if (chapter.id === "life_domains") {
    return <ReportLifeDomainsVisual paragraphs={chapter.paragraphs} />;
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
  const visualConsumesParagraphs = chapter.id === "life_domains";

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
      {!visualConsumesParagraphs && leadParagraph ? (
        <p className="bte-report-doc__lead">
          {leadParagraph}
        </p>
      ) : null}
      <ReportChapterVisual chapter={chapter} model={model} />
      {!visualConsumesParagraphs && bodyParagraphs.map((paragraph, paragraphIndex) => (
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
