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
  { id: "health", title: "Sức khỏe", cardTitle: "Luận sức khỏe", pattern: /sức khỏe/i },
  { id: "wealth", title: "Tài vận và kinh doanh", cardTitle: "Luận tài vận", pattern: /mệnh\/tài vận|tài vận/i },
  { id: "career", title: "Nghề nghiệp", cardTitle: "Luận nghề nghiệp", pattern: /quan vận\/nghề nghiệp|nghề nghiệp/i },
  { id: "marriage", title: "Hôn nhân và quan hệ", cardTitle: "Luận hôn nhân", pattern: /nhân duyên\/hôn nhân|hôn nhân/i },
  { id: "children", title: "Con cái và hậu vận", cardTitle: "Luận con cái/hậu vận", pattern: /con cái/i },
  { id: "parents", title: "Bố mẹ", cardTitle: "Luận về bố mẹ", pattern: /bố mẹ/i },
  { id: "siblings", title: "Anh em và người đồng hành", cardTitle: "Luận quan hệ đồng hành", pattern: /anh em/i },
  { id: "ancestry", title: "Tổ tiên và gốc phúc", cardTitle: "Luận gốc gia tộc", pattern: /tổ tiên/i },
  { id: "property", title: "Điền trạch và phong thủy", cardTitle: "Luận điền trạch", pattern: /điền trạch/i },
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
  const titleMatch = DOMAIN_GROUPS.find((group) => group.pattern.test(title));
  return titleMatch ?? DOMAIN_GROUPS.find((group) => group.pattern.test(body)) ?? DOMAIN_GROUPS[0];
}

function compactLegacyUsefulGod(title: string, body: string): { readonly title: string; readonly body: string } {
  if (!/^Dụng thần trọng tâm(?:\s+\d+)?$/i.test(title)) return { title, body };
  const markers = ["Trong tài vận", "Khi chọn nghề", "Khi đưa vào hôn nhân", "Với kế hoạch sinh con", "Khi hòa giải", "Khi xét cộng sự", "Vì vậy, phong thủy"];
  const marker = markers.map((value) => ({ value, index: body.indexOf(value) })).find((item) => item.index >= 0);
  if (!marker) return { title: "Dụng thần ứng dụng", body };
  const element = body.split("·", 1)[0].trim().split(/[.;]/, 1)[0].trim();
  const lead = element ? `Trục điều tiết của lá số là ${element}. ` : "";
  return { title: "Dụng thần ứng dụng", body: lead + body.slice(marker.index) };
}

function splitDomainParagraph(paragraph: string, index: number, activeGroup?: DomainGroup): DomainItem {
  const colonIndex = paragraph.indexOf(":");
  const title = colonIndex <= 0 ? inferDomainTitle(paragraph, index) : paragraph.slice(0, colonIndex).trim();
  const rawBody = colonIndex <= 0 ? paragraph : paragraph.slice(colonIndex + 1).trim();
  const compact = compactLegacyUsefulGod(title, rawBody);
  const explicitGroup = colonIndex > 0 ? DOMAIN_GROUPS.find((group) => group.pattern.test(title)) : undefined;
  return { title: compact.title, body: compact.body, group: explicitGroup ?? activeGroup ?? inferDomainGroup(title, rawBody) };
}

function parseDomainItems(paragraphs: readonly string[]): readonly DomainItem[] {
  const items: DomainItem[] = [];
  let activeGroup: DomainGroup | undefined;
  paragraphs.forEach((paragraph, index) => {
    const item = splitDomainParagraph(paragraph, index, activeGroup);
    activeGroup = item.group;
    if (item.body) items.push(item);
  });
  return items;
}

function groupDomainItems(items: readonly DomainItem[]): ReadonlyArray<{
  readonly group: DomainGroup;
  readonly items: readonly DomainItem[];
  readonly startIndex: number;
}> {
  let startIndex = 0;
  return DOMAIN_GROUPS
    .map((group) => ({
      group,
      items: items.filter((item) => item.group.id === group.id),
    }))
    .filter((entry) => entry.items.length)
    .map((entry) => {
      const numbered = { ...entry, startIndex };
      startIndex += entry.items.length;
      return numbered;
    });
}

function ReportLifeDomainsVisual({
  paragraphs,
}: {
  readonly paragraphs: readonly string[];
}): ReactNode {
  const items = parseDomainItems(paragraphs);
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
            {entry.items.map((item, index) => {
              const duplicateIndex = entry.items.slice(0, index).filter((candidate) => candidate.title === item.title).length + 1;
              const duplicateCount = entry.items.filter((candidate) => candidate.title === item.title).length;
              const displayTitle = duplicateCount > 1 && duplicateIndex > 1 ? `${item.title} ${duplicateIndex}` : item.title;
              return (
                <article key={`${entry.group.id}-${index}`} className="bte-report-doc__domain-card">
                  <span className="bte-report-doc__domain-index">{String(entry.startIndex + index + 1).padStart(2, "0")}</span>
                  <h6>{displayTitle}</h6>
                  <p>{item.body}</p>
                </article>
              );
            })}
          </div>
        </section>
      ))}
    </aside>
  );
}

const STRUCTURED_CHAPTER_IDS = new Set([
  "four_pillars",
  "day_master",
  "strength_structure_useful_god",
  "ten_gods",
  "shen_sha",
  "bone_weight",
  "palace_feng_shui",
  "synthesis",
  "recommendations",
]);

const STRUCTURED_CHAPTER_META: Record<string, { readonly kicker: string; readonly title: string; readonly cardTitle: string }> = {
  four_pillars: { kicker: "Khung tứ trụ", title: "Bốn trụ và vai trò từng cung", cardTitle: "Luận trụ" },
  day_master: { kicker: "Nhật chủ", title: "Khí chất cốt lõi của mệnh", cardTitle: "Luận Nhật chủ" },
  strength_structure_useful_god: { kicker: "Trục cân bằng", title: "Thân vượng, Mệnh cục và Dụng thần", cardTitle: "Luận trục" },
  ten_gods: { kicker: "Thập thần", title: "Vai trò đời sống qua từng tín hiệu", cardTitle: "Luận Thập thần" },
  shen_sha: { kicker: "Thần sát", title: "Tín hiệu bổ sung cần quan sát", cardTitle: "Luận Thần sát" },
  bone_weight: { kicker: "Cân xương", title: "Nền lượng và nhịp tích lũy", cardTitle: "Luận Cân xương" },
  palace_feng_shui: { kicker: "Cung Phi", title: "Nhóm trạch và phong thủy ứng dụng", cardTitle: "Luận Cung Phi" },
  synthesis: { kicker: "Tổng hợp", title: "Điểm mạnh, rủi ro và trọng tâm hành động", cardTitle: "Kết luận" },
  recommendations: { kicker: "Khuyến nghị", title: "Việc nên ưu tiên sau khi đọc lá số", cardTitle: "Khuyến nghị" },
};

const STRUCTURED_PREFIX_RULES: ReadonlyArray<readonly [RegExp, string]> = [
  [/^Trụ\s+Năm/i, "Trụ năm"],
  [/^Trụ\s+Tháng/i, "Trụ tháng"],
  [/^Trụ\s+Ngày/i, "Trụ ngày"],
  [/^Trụ\s+Giờ/i, "Trụ giờ"],
  [/^Nhật\s+chủ/i, "Nhật chủ"],
  [/^Thân\s+vượng|^Thân\s+nhược|^Thân\s+trung/i, "Thế thân"],
  [/^Mệnh\s+cục/i, "Mệnh cục"],
  [/^Dụng\s+thần/i, "Dụng thần"],
  [/^Hỷ\s+thần/i, "Hỷ thần"],
  [/^Kỵ\s+thần/i, "Kỵ thần"],
  [/^Cung\s+Phi|^Mệnh\s+quái/i, "Cung Phi/Mệnh quái"],
  [/^Đông\s+Tứ|^Tây\s+Tứ|^Nhóm\s+trạch/i, "Nhóm trạch"],
  [/^Điền\s+trạch/i, "Điền trạch"],
  [/^Phong\s+thủy/i, "Phong thủy ứng dụng"],
  [/^Tóm\s+tắt/i, "Tóm tắt"],
  [/^Điểm\s+mạnh/i, "Điểm mạnh"],
  [/^Rủi\s+ro/i, "Rủi ro"],
  [/^Hướng\s+đi/i, "Hướng đi"],
];

type StructuredItem = {
  readonly title: string;
  readonly body: string;
};

function shouldUseStructuredVisual(chapterId: string): boolean {
  return STRUCTURED_CHAPTER_IDS.has(chapterId);
}

function splitStructuredParagraph(chapterId: string, paragraph: string, index: number): StructuredItem {
  const value = paragraph.trim();
  const meta = STRUCTURED_CHAPTER_META[chapterId] ?? {
    kicker: "Luận giải",
    title: "Các ý chính cần đọc",
    cardTitle: "Luận điểm",
  };
  const prefix = STRUCTURED_PREFIX_RULES.find(([pattern]) => pattern.test(value));
  const colonIndex = value.indexOf(":");
  if (prefix) {
    const body = colonIndex > 0 ? value.slice(colonIndex + 1).trim() : value;
    return { title: prefix[1], body };
  }
  if (colonIndex > 0 && colonIndex < 62) {
    return {
      title: value.slice(0, colonIndex).trim(),
      body: value.slice(colonIndex + 1).trim(),
    };
  }
  return {
    title: `${meta.cardTitle} ${index + 1}`,
    body: value,
  };
}

function ReportStructuredChapterVisual({
  chapter,
}: {
  readonly chapter: BaziReportDocumentChapterView;
}): ReactNode {
  const meta = STRUCTURED_CHAPTER_META[chapter.id] ?? {
    kicker: "Luận giải",
    title: "Các ý chính cần đọc",
    cardTitle: "Luận điểm",
  };
  const items = chapter.paragraphs
    .map((paragraph, index) => splitStructuredParagraph(chapter.id, paragraph, index))
    .filter((item) => item.body);
  if (!items.length) return null;
  return (
    <aside className="bte-report-doc__visual bte-report-doc__visual--structured" aria-label={meta.title}>
      <header className="bte-report-doc__visual-head">
        <div>
          <p className="bte-report-doc__visual-kicker">{meta.kicker}</p>
          <h4 className="bte-report-doc__visual-title">{meta.title}</h4>
        </div>
      </header>
      <div className="bte-report-doc__structured-grid" data-structured-chapter={chapter.id}>
        {items.map((item, index) => (
          <article key={`${chapter.id}-${index}`} className="bte-report-doc__structured-card">
            <span className="bte-report-doc__structured-index">{String(index + 1).padStart(2, "0")}</span>
            <h6>{item.title}</h6>
            <p>{item.body}</p>
          </article>
        ))}
      </div>
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
  if (shouldUseStructuredVisual(chapter.id)) {
    return <ReportStructuredChapterVisual chapter={chapter} />;
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
  const visualConsumesParagraphs = chapter.id === "life_domains" || shouldUseStructuredVisual(chapter.id);

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
