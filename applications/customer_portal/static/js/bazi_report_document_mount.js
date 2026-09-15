/**
 * Runtime bridge for the Bát Tự customer report document.
 *
 * The source React view already renders this section, but the static result bundle
 * can be stale in local desktop runs. This bridge only reads the customer-safe
 * bazi_analysis_result.customer_narrative contract and mounts the detailed report
 * after the chart tables when the current bundle has not rendered it yet.
 */
(function (global) {
  const DOCUMENT_SELECTOR = '[data-report-document="bazi-v1"], .bte-report-doc';
  const STYLE_ID = "bazi-report-document-bridge-style";
  let lastSignature = "";
  let pending = false;

  function isRecord(value) {
    return Boolean(value && typeof value === "object" && !Array.isArray(value));
  }

  function text(value) {
    return typeof value === "string" ? value.trim() : "";
  }

  function textList(value) {
    return Array.isArray(value) ? value.map(text).filter(Boolean) : [];
  }

  const PILLAR_KEYS = ["year", "month", "day", "hour"];
  const TAM_HOP_GROUPS = [
    ["Thân", "Tý", "Thìn"],
    ["Dần", "Ngọ", "Tuất"],
    ["Hợi", "Mão", "Mùi"],
    ["Tỵ", "Dậu", "Sửu"],
  ];
  const BRANCH_META = {
    "Tý": { element: "Thủy", yinYang: "Dương" },
    "Sửu": { element: "Thổ", yinYang: "Âm" },
    "Dần": { element: "Mộc", yinYang: "Dương" },
    "Mão": { element: "Mộc", yinYang: "Âm" },
    "Thìn": { element: "Thổ", yinYang: "Dương" },
    "Tỵ": { element: "Hỏa", yinYang: "Âm" },
    "Ngọ": { element: "Hỏa", yinYang: "Dương" },
    "Mùi": { element: "Thổ", yinYang: "Âm" },
    "Thân": { element: "Kim", yinYang: "Dương" },
    "Dậu": { element: "Kim", yinYang: "Âm" },
    "Tuất": { element: "Thổ", yinYang: "Dương" },
    "Hợi": { element: "Thủy", yinYang: "Âm" },
  };

  function arrayOf(value) {
    return Array.isArray(value) ? value : [];
  }

  function pillarKey(value) {
    const key = text(value).toLowerCase();
    if (key === "year" || key === "năm" || key === "nam") return "year";
    if (key === "month" || key === "tháng" || key === "thang") return "month";
    if (key === "day" || key === "ngày" || key === "ngay") return "day";
    if (key === "hour" || key === "giờ" || key === "gio") return "hour";
    return "";
  }

  function pillarOf(data, key) {
    const bazi = isRecord(data && data.bazi) ? data.bazi : {};
    return isRecord(bazi[`${key}_pillar`]) ? bazi[`${key}_pillar`] : {};
  }

  function tenGodPayload(data) {
    if (isRecord(data && data.ten_gods)) return data.ten_gods;
    if (isRecord(data && data.ten_gods_result)) return data.ten_gods_result;
    return {};
  }

  function visibleForPillar(data, key) {
    return arrayOf(tenGodPayload(data).visible).find((item) => isRecord(item) && item.pillar === key) || {};
  }

  function hiddenForPillar(data, key) {
    return arrayOf(tenGodPayload(data).hidden).filter((item) => isRecord(item) && item.pillar === key);
  }

  function hiddenLines(data, key) {
    const pillar = pillarOf(data, key);
    const stems = arrayOf(pillar.hidden_stems).map(text).filter(Boolean);
    const entries = hiddenForPillar(data, key);
    const source = stems.length
      ? stems.map((stem) => entries.find((item) => text(item.hidden_stem || item.stem) === stem) || { stem })
      : entries;
    return source
      .map((item) => {
        const stem = text(item.hidden_stem || item.stem);
        if (!stem) return "";
        const element = text(item.element);
        const tenGod = text(item.ten_god);
        return [element ? `${stem} (${element})` : stem, tenGod].filter(Boolean).join(" ");
      })
      .filter(Boolean);
  }

  function tamHopByPillar(data) {
    const result = { year: "", month: "", day: "", hour: "" };
    const pillars = PILLAR_KEYS.map((key) => ({ key, branch: text(pillarOf(data, key).branch) }));
    pillars.forEach((pillar) => {
      const group = TAM_HOP_GROUPS.find((item) => item.includes(pillar.branch));
      result[pillar.key] = group ? group.join(" - ") : "";
    });
    return result;
  }

  function elementToken(value) {
    if (value.includes("Mộc")) return "wood";
    if (value.includes("Hỏa")) return "fire";
    if (value.includes("Thổ")) return "earth";
    if (value.includes("Kim")) return "metal";
    if (value.includes("Thủy")) return "water";
    return "";
  }

  function metaHtml(value) {
    const label = text(value);
    if (!label) return "";
    const token = elementToken(label);
    return `<span class="bte-bazi__meta"${token ? ` data-element="${token}"` : ""}>${escapeHtml(label)}</span>`;
  }

  function valueMetaHtml(primary, secondary) {
    const label = text(primary);
    if (!label) return "—";
    return `<span class="bte-bazi__value">${escapeHtml(label)}</span>${metaHtml(secondary)}`;
  }

  function branchMetaLabel(branch) {
    const meta = BRANCH_META[text(branch)];
    return meta ? `${meta.element} · ${meta.yinYang}` : "";
  }

  function shenShaByPillar(data) {
    const result = { year: [], month: [], day: [], hour: [] };
    const bazi = isRecord(data && data.bazi) ? data.bazi : {};
    arrayOf(bazi.shensha_matches).forEach((match) => {
      if (!isRecord(match)) return;
      const name = text(match.canonical_name || match.name);
      if (!name) return;
      const keys = new Set();
      const direct = pillarKey(match.pillar);
      if (direct) keys.add(direct);
      arrayOf(match.occurrences).forEach((occurrence) => {
        const key = isRecord(occurrence) ? pillarKey(occurrence.pillar) : "";
        if (key) keys.add(key);
      });
      keys.forEach((key) => {
        if (!result[key].includes(name)) result[key].push(name);
      });
    });
    return result;
  }

  function linesHtml(items) {
    const lines = items.map(text).filter(Boolean);
    if (!lines.length) return "—";
    return `<ul class="bte-bazi__lines">${lines.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;
  }

  function escapeHtml(value) {
    return text(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function loadDisplayRecord() {
    const store = global.BtePortal && global.BtePortal.ResultStore;
    if (!store) return null;
    const params = new URLSearchParams(global.location.search || "");
    const historyId = params.get("from") === "history" ? text(params.get("id")) : "";
    if (historyId && typeof store.resolveForDisplay === "function") {
      return store.resolveForDisplay(true, historyId);
    }
    if (typeof store.loadCurrent === "function") {
      return store.loadCurrent();
    }
    if (typeof store.load === "function") {
      return store.load();
    }
    return null;
  }

  function chapterFromRecord(value, index) {
    if (!isRecord(value)) return null;
    const title = text(value.title);
    const paragraphs = textList(value.paragraphs);
    const bullets = textList(value.bullets);
    if (!title || (!paragraphs.length && !bullets.length)) return null;
    return {
      id: text(value.id) || `chapter-${index + 1}`,
      title,
      paragraphs,
      bullets,
    };
  }

  function chaptersFromMarkdown(markdown) {
    if (!markdown) return [];
    const chapters = [];
    let current = null;
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

  function adaptReport(data) {
    const contract = isRecord(data) ? data.bazi_analysis_result : null;
    const narrative = isRecord(contract) ? contract.customer_narrative : null;
    if (!isRecord(narrative)) return null;
    const reportDocument = isRecord(narrative.report_document) ? narrative.report_document : {};
    const markdown = text(reportDocument.markdown);
    const chapters = Array.isArray(narrative.report_chapters)
      ? narrative.report_chapters.map(chapterFromRecord).filter(Boolean)
      : [];
    const resolvedChapters = chapters.length ? chapters : chaptersFromMarkdown(markdown);
    if (!resolvedChapters.length) return null;
    return {
      title: text(reportDocument.title) || "Bản luận giải lá số Bát Tự",
      subtitle: text(reportDocument.subtitle),
      chapters: resolvedChapters,
    };
  }

  function appendText(parent, tag, className, value) {
    if (!value) return null;
    const node = document.createElement(tag);
    node.className = className;
    node.textContent = value;
    parent.appendChild(node);
    return node;
  }

  function renderReport(model, signature) {
    const section = document.createElement("section");
    section.className = "bte-report-doc";
    section.setAttribute("data-report-document", "bazi-v1");
    section.setAttribute("data-report-document-bridge", "true");
    section.setAttribute("data-analysis-id", signature);
    section.setAttribute("aria-labelledby", "bazi-report-document-title");

    const header = document.createElement("header");
    header.className = "bte-report-doc__header";
    appendText(header, "p", "bte-report-doc__eyebrow", "Hồ sơ luận giải");
    const title = appendText(header, "h2", "bte-report-doc__title", model.title);
    if (title) title.id = "bazi-report-document-title";
    const meta = document.createElement("div");
    meta.className = "bte-report-doc__meta";
    appendText(meta, "p", "bte-report-doc__subtitle", model.subtitle);
    appendText(meta, "span", "bte-report-doc__count", `${model.chapters.length} chương luận giải`);
    header.appendChild(meta);
    section.appendChild(header);

    const layout = document.createElement("div");
    layout.className = "bte-report-doc__layout";

    const toc = document.createElement("nav");
    toc.className = "bte-report-doc__toc";
    toc.setAttribute("aria-label", "Mục lục bản luận giải");
    appendText(toc, "p", "bte-report-doc__toc-title", "Mục lục");
    const tocList = document.createElement("ol");
    tocList.className = "bte-report-doc__toc-list";
    model.chapters.forEach((chapter, index) => {
      const item = document.createElement("li");
      item.className = "bte-report-doc__toc-item";
      const link = document.createElement("a");
      link.className = "bte-report-doc__toc-link";
      link.href = `#bazi-report-${chapter.id}`;
      appendText(link, "span", "bte-report-doc__toc-index", String(index + 1).padStart(2, "0"));
      appendText(link, "span", "", chapter.title);
      item.appendChild(link);
      tocList.appendChild(item);
    });
    toc.appendChild(tocList);
    layout.appendChild(toc);

    const body = document.createElement("div");
    body.className = "bte-report-doc__body";
    model.chapters.forEach((chapter, index) => {
      const chapterNode = document.createElement("section");
      chapterNode.className = "bte-report-doc__chapter";
      chapterNode.id = `bazi-report-${chapter.id}`;
      chapterNode.setAttribute("data-report-chapter", chapter.id);
      const chapterHead = document.createElement("header");
      chapterHead.className = "bte-report-doc__chapter-head";
      const number = appendText(chapterHead, "span", "bte-report-doc__chapter-number", String(index + 1).padStart(2, "0"));
      if (number) number.setAttribute("aria-hidden", "true");
      appendText(chapterHead, "h3", "bte-report-doc__chapter-title", chapter.title);
      chapterNode.appendChild(chapterHead);
      const lead = chapter.paragraphs[0];
      if (lead) appendText(chapterNode, "p", "bte-report-doc__lead", lead);
      chapter.paragraphs.slice(1).forEach((paragraph) => {
        appendText(chapterNode, "p", "bte-report-doc__paragraph", paragraph);
      });
      if (chapter.bullets.length) {
        const list = document.createElement("ul");
        list.className = "bte-report-doc__bullets";
        chapter.bullets.forEach((bullet) => appendText(list, "li", "", bullet));
        chapterNode.appendChild(list);
      }
      body.appendChild(chapterNode);
    });
    layout.appendChild(body);
    section.appendChild(layout);
    return section;
  }

  function renderBaziRow(label, field, values) {
    const row = document.createElement("tr");
    row.setAttribute("data-bazi-row", field);
    const head = document.createElement("th");
    head.scope = "row";
    head.textContent = label;
    row.appendChild(head);
    PILLAR_KEYS.forEach((key) => {
      const cell = document.createElement("td");
      cell.setAttribute("data-pillar", key);
      cell.setAttribute("data-bazi-field", field);
      cell.innerHTML = values[key] || "—";
      row.appendChild(cell);
    });
    return row;
  }

  function patchBaziTable(data) {
    const root = document.querySelector(".bte-cdash");
    const grid = root && root.querySelector(".bte-cdash__grid");
    const baziCard = grid && grid.querySelector('[data-card="bazi"]');
    const table = baziCard && baziCard.querySelector(".bte-bazi__table");
    const body = table && table.querySelector("tbody");
    if (!root || !grid || !baziCard || !table || !body) return;

    grid.querySelectorAll("[data-card]").forEach((card) => {
      if (card.getAttribute("data-card") !== "bazi") card.remove();
    });
    grid.querySelectorAll("[data-life-consulting]").forEach((section) => section.remove());
    baziCard.classList.add("bte-cdash__card--span-12");
    baziCard.setAttribute("data-span", "12");

    const branchRow = body.querySelector('[data-bazi-row="branch"]');
    if (branchRow) {
      PILLAR_KEYS.forEach((key) => {
        const cell = branchRow.querySelector(`[data-pillar="${key}"]`);
        const branch = text(pillarOf(data, key).branch) || text(cell && cell.querySelector(".bte-bazi__value") && cell.querySelector(".bte-bazi__value").textContent);
        if (cell && branch) cell.innerHTML = valueMetaHtml(branch, branchMetaLabel(branch));
      });
    }

    const hiddenRow = body.querySelector('[data-bazi-row="hidden"]');
    if (hiddenRow) {
      PILLAR_KEYS.forEach((key) => {
        const cell = hiddenRow.querySelector(`[data-pillar="${key}"]`);
        if (cell) cell.innerHTML = linesHtml(hiddenLines(data, key));
      });
    }

    body.querySelectorAll('[data-bazi-row="tam-hop"], [data-bazi-row="shen-sha"]').forEach((row) => row.remove());
    const tamHop = tamHopByPillar(data);
    const shenSha = shenShaByPillar(data);
    const tamHopValues = {};
    const shenShaValues = {};
    PILLAR_KEYS.forEach((key) => {
      tamHopValues[key] = tamHop[key] ? escapeHtml(tamHop[key]) : "—";
      shenShaValues[key] = linesHtml(shenSha[key]);
    });
    body.appendChild(renderBaziRow("Tam Hợp", "tam-hop", tamHopValues));
    body.appendChild(renderBaziRow("Thần Sát", "shen-sha", shenShaValues));
  }

  function reportDocuments() {
    return Array.from(new Set(Array.from(document.querySelectorAll(DOCUMENT_SELECTOR))));
  }

  function placeReportAfterGrid(node, grid, signature) {
    if (!node || !grid) return;
    if (node.previousElementSibling !== grid) {
      grid.insertAdjacentElement("afterend", node);
    }
    if (signature) node.setAttribute("data-analysis-id", signature);
  }

  function removeAllReports() {
    reportDocuments().forEach((node) => node.remove());
  }

  function ensureStyles() {
    if (document.getElementById(STYLE_ID)) return;
    const style = document.createElement("style");
    style.id = STYLE_ID;
    style.textContent = `
      .bte-cdash[data-finish="v2"] .bte-id {
        border-radius: 6px;
      }
      .bte-cdash[data-finish="v2"] .bte-id__tu-tru .bte-tu-tru__title {
        margin-bottom: var(--space-2, 8px);
        color: #dc2626;
        font-size: 0.875rem;
        font-weight: 700;
        letter-spacing: 0.08em;
      }
      .bte-cdash[data-finish="v2"] .bte-id__tu-tru .bte-tu-tru__table {
        border-collapse: collapse;
        border: 1px solid #111827;
        font-size: 0.8125rem;
      }
      .bte-cdash[data-finish="v2"] .bte-id__tu-tru .bte-tu-tru__table th,
      .bte-cdash[data-finish="v2"] .bte-id__tu-tru .bte-tu-tru__table td {
        padding: 5px 8px;
        border: 1px solid #111827;
        background: transparent;
      }
      .bte-cdash[data-finish="v2"] .bte-id__tu-tru .bte-tu-tru__can-chi {
        font-size: 0.9375rem;
        font-weight: 700;
        letter-spacing: 0.02em;
      }
      .bte-cdash[data-finish="v2"] .bte-cdash__card.bte-bazi {
        grid-column: 1 / -1 !important;
        padding: var(--space-5, 24px);
        border-radius: 6px;
        background: var(--surface-report-paper, #fffdf8);
      }
      .bte-cdash[data-finish="v2"] .bte-cdash__grid > [data-card]:not([data-card="bazi"]),
      .bte-cdash[data-finish="v2"] .bte-cdash__grid > [data-life-consulting] {
        display: none !important;
      }
      .bte-cdash[data-finish="v2"] .bte-cdash__page-header {
        order: 1 !important;
      }
      .bte-cdash[data-finish="v2"] .bte-id {
        order: 2 !important;
      }
      .bte-cdash[data-finish="v2"] .bte-cdash__grid {
        order: 3 !important;
      }
      .bte-cdash[data-finish="v2"] .bte-report-doc {
        order: 4 !important;
      }
      .bte-cdash[data-finish="v2"] .bte-bazi .bte-cdash__card-title {
        margin-bottom: var(--space-3, 12px);
        color: var(--cdash-muted, #5f6b7a);
        font-family: var(--font-family-display, inherit);
        font-size: 1.25rem;
        font-weight: 700;
        letter-spacing: 0.04em;
      }
      .bte-cdash[data-finish="v2"] .bte-bazi[data-viz="structure"] .bte-bazi__table,
      .bte-cdash[data-finish="v2"] .bte-bazi__table {
        border-collapse: collapse;
        border-spacing: 0;
        table-layout: fixed;
        border: 1.5px solid #111827;
        font-size: 0.875rem;
      }
      .bte-cdash[data-finish="v2"] .bte-bazi[data-viz="structure"] .bte-bazi__table th,
      .bte-cdash[data-finish="v2"] .bte-bazi[data-viz="structure"] .bte-bazi__table td,
      .bte-cdash[data-finish="v2"] .bte-bazi__table th,
      .bte-cdash[data-finish="v2"] .bte-bazi__table td {
        padding: 12px 10px;
        border: 1px solid #111827;
        vertical-align: middle;
      }
      .bte-cdash[data-finish="v2"] .bte-bazi[data-viz="structure"] .bte-bazi__table tbody tr + tr td {
        padding-top: 12px;
      }
      .bte-cdash[data-finish="v2"] .bte-bazi[data-viz="structure"] .bte-bazi__table tbody tr + tr td::before {
        content: none;
      }
      .bte-cdash[data-finish="v2"] .bte-bazi__table th[scope="row"] {
        width: 6.75rem;
        color: var(--cdash-muted, #5f6b7a);
        font-size: 0.8125rem;
        text-align: left;
      }
      .bte-cdash[data-finish="v2"] .bte-bazi__table thead th[data-pillar] {
        color: #111827;
        font-size: 0.9375rem;
        text-decoration: underline;
      }
      .bte-cdash[data-finish="v2"] .bte-bazi__table [data-day-master="true"] {
        background: #eaf8f2;
      }
      .bte-cdash[data-finish="v2"] .bte-bazi[data-viz="structure"] [data-bazi-row="stem"] .bte-bazi__value,
      .bte-cdash[data-finish="v2"] .bte-bazi[data-viz="structure"] [data-bazi-row="branch"] .bte-bazi__value,
      .bte-cdash[data-finish="v2"] .bte-bazi__value {
        font-size: 1.125rem;
        font-weight: 700;
        color: #111827;
      }
      .bte-cdash[data-finish="v2"] .bte-bazi__meta {
        color: var(--cdash-muted, #5f6b7a);
        font-size: 0.8125rem;
      }
      .bte-cdash[data-finish="v2"] .bte-bazi__meta[data-element="wood"] {
        color: #15803d;
      }
      .bte-cdash[data-finish="v2"] .bte-bazi__meta[data-element="fire"] {
        color: #dc2626;
      }
      .bte-cdash[data-finish="v2"] .bte-bazi__meta[data-element="earth"] {
        color: #b45309;
      }
      .bte-cdash[data-finish="v2"] .bte-bazi__meta[data-element="metal"] {
        color: #64748b;
      }
      .bte-cdash[data-finish="v2"] .bte-bazi__meta[data-element="water"] {
        color: #0284c7;
      }
      .bte-cdash[data-finish="v2"] .bte-bazi__hidden,
      .bte-cdash[data-finish="v2"] .bte-bazi__lines {
        display: grid;
        gap: 6px;
        margin: 0;
        padding: 0;
        list-style: none;
        white-space: normal;
      }
      .bte-cdash[data-finish="v2"] .bte-bazi__hidden li,
      .bte-cdash[data-finish="v2"] .bte-bazi__lines li {
        display: grid;
        gap: 2px;
      }
      .bte-cdash[data-finish="v2"] .bte-bazi__table [data-bazi-field="tam-hop"],
      .bte-cdash[data-finish="v2"] .bte-bazi__table [data-bazi-field="shen-sha"] {
        font-weight: 700;
      }
      .bte-report-doc {
        width: 100%;
        margin-top: var(--space-5, 24px);
        padding: var(--space-6, 28px);
        background: var(--surface-report-paper, #fffdf8);
        border: 1px solid var(--cdash-border, #dfe3ea);
        border-radius: var(--cdash-radius, 8px);
        box-shadow: var(--cdash-shadow, 0 12px 28px rgba(15, 23, 42, 0.08));
        box-sizing: border-box;
      }
      .bte-report-doc__header {
        max-width: 1040px;
        margin: 0 0 var(--space-5, 24px);
        padding-bottom: var(--space-4, 18px);
        border-bottom: 1px solid var(--cdash-border, #dfe3ea);
      }
      .bte-report-doc__eyebrow {
        margin: 0 0 var(--space-2, 8px);
        color: var(--cdash-muted, #5f6b7a);
        font-size: var(--font-size-metadata, 0.78rem);
        font-weight: var(--font-weight-medium, 700);
        letter-spacing: var(--letter-spacing-metadata, 0.12em);
        text-transform: uppercase;
      }
      .bte-report-doc__title {
        margin: 0;
        color: var(--cdash-text, #111827);
        font-family: var(--font-family-display, inherit);
        font-size: 1.5rem;
        font-weight: var(--font-weight-semibold, 700);
        line-height: var(--line-height-heading, 1.25);
      }
      .bte-report-doc__subtitle {
        margin: 0;
        color: var(--cdash-muted, #5f6b7a);
        font-size: var(--font-size-body, 1rem);
        line-height: var(--line-height-body, 1.55);
      }
      .bte-report-doc__meta {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: var(--space-2, 8px) var(--space-4, 18px);
        margin-top: var(--space-2, 8px);
      }
      .bte-report-doc__count {
        display: inline-flex;
        align-items: center;
        min-height: 1.625rem;
        padding: 2px 10px;
        border: 1px solid var(--cdash-border, #dfe3ea);
        border-radius: 999px;
        color: var(--cdash-muted, #5f6b7a);
        background: #f7fafc;
        font-size: var(--font-size-caption, 0.875rem);
        font-weight: 600;
        line-height: 1.2;
      }
      .bte-report-doc__layout {
        display: grid;
        grid-template-columns: minmax(190px, 0.26fr) minmax(0, 1fr);
        align-items: start;
        gap: var(--space-6, 28px);
        max-width: 1180px;
      }
      .bte-report-doc__toc {
        position: sticky;
        top: var(--space-4, 18px);
        min-width: 0;
        padding-right: var(--space-4, 18px);
        border-right: 1px solid var(--cdash-border, #dfe3ea);
      }
      .bte-report-doc__toc-title {
        margin: 0 0 var(--space-3, 12px);
        color: var(--cdash-muted, #5f6b7a);
        font-size: var(--font-size-metadata, 0.78rem);
        font-weight: 700;
        letter-spacing: var(--letter-spacing-metadata, 0.12em);
        text-transform: uppercase;
      }
      .bte-report-doc__toc-list {
        display: grid;
        gap: 2px;
        margin: 0;
        padding: 0;
        list-style: none;
      }
      .bte-report-doc__toc-link {
        display: grid;
        grid-template-columns: 2rem minmax(0, 1fr);
        gap: var(--space-2, 8px);
        align-items: baseline;
        min-height: 2rem;
        padding: 5px 0;
        color: var(--cdash-muted, #5f6b7a);
        font-size: var(--font-size-caption, 0.875rem);
        line-height: 1.25;
        text-decoration: none;
      }
      .bte-report-doc__toc-index {
        color: #94a3b8;
        font-variant-numeric: tabular-nums;
        font-weight: 700;
      }
      .bte-report-doc__body {
        display: grid;
        grid-template-columns: minmax(0, 1fr);
        gap: var(--space-6, 28px);
        max-width: 860px;
      }
      .bte-report-doc__chapter {
        min-width: 0;
        scroll-margin-top: var(--space-6, 28px);
      }
      .bte-report-doc__chapter + .bte-report-doc__chapter {
        padding-top: var(--space-6, 28px);
        border-top: 1px solid var(--cdash-border, #dfe3ea);
      }
      .bte-report-doc__chapter-head {
        display: grid;
        grid-template-columns: 2.75rem minmax(0, 1fr);
        gap: var(--space-3, 12px);
        align-items: baseline;
        margin-bottom: var(--space-3, 12px);
      }
      .bte-report-doc__chapter-number {
        color: var(--cdash-accent, #2563eb);
        font-family: var(--font-family-display, inherit);
        font-size: 1rem;
        font-weight: 700;
        font-variant-numeric: tabular-nums;
      }
      .bte-report-doc__chapter-title {
        margin: 0;
        color: var(--cdash-text, #111827);
        font-family: var(--font-family-display, inherit);
        font-size: 1.125rem;
        font-weight: var(--font-weight-semibold, 700);
        line-height: var(--line-height-heading, 1.25);
      }
      .bte-report-doc__lead {
        margin: 0 0 var(--space-3, 12px);
        color: var(--cdash-text, #111827);
        font-size: 1rem;
        font-weight: 600;
        line-height: 1.65;
      }
      .bte-report-doc__paragraph {
        margin: 0 0 var(--space-3, 12px);
        color: var(--cdash-text, #111827);
        font-size: 0.95rem;
        line-height: 1.68;
      }
      .bte-report-doc__bullets {
        display: grid;
        gap: var(--space-2, 8px);
        margin: var(--space-3, 12px) 0 0;
        padding-left: 1.1rem;
        color: var(--cdash-text, #111827);
        font-size: var(--font-size-body, 1rem);
        line-height: var(--line-height-body, 1.55);
      }
      @media (max-width: 767px) {
        .bte-report-doc {
          margin-top: var(--space-4, 18px);
          padding: var(--space-4, 18px);
        }
        .bte-report-doc__title {
          font-size: 1.25rem;
        }
        .bte-report-doc__layout {
          grid-template-columns: 1fr;
          gap: var(--space-5, 24px);
        }
        .bte-report-doc__toc {
          position: static;
          padding: 0 0 var(--space-4, 18px);
          border-right: 0;
          border-bottom: 1px solid var(--cdash-border, #dfe3ea);
        }
        .bte-report-doc__chapter-head {
          grid-template-columns: 2.25rem minmax(0, 1fr);
          gap: var(--space-2, 8px);
        }
        .bte-report-doc__paragraph,
        .bte-report-doc__lead {
          font-size: 0.9375rem;
        }
      }
    `;
    document.head.appendChild(style);
  }

  function mountReport() {
    pending = false;
    const root = document.querySelector(".bte-cdash");
    const grid = root && root.querySelector(".bte-cdash__grid");
    if (!root || !grid) return;
    ensureStyles();

    const record = loadDisplayRecord();
    const data = record && record.data;
    if (data) patchBaziTable(data);
    const model = adaptReport(data);
    if (!model) return;

    const signature = String(
      (record && (record.analysis_id || record.id)) ||
        (data && (data.analysis_id || data.request_id || data.case_id)) ||
        model.title,
    );
    removeAllReports();
    placeReportAfterGrid(renderReport(model, signature), grid, signature);
    lastSignature = signature;
  }

  function scheduleMount() {
    if (pending) return;
    pending = true;
    global.requestAnimationFrame
      ? global.requestAnimationFrame(mountReport)
      : global.setTimeout(mountReport, 0);
  }

  function start() {
    scheduleMount();
    const target = document.getElementById("canonical-desktop-root") || document.body;
    if (!target || typeof MutationObserver === "undefined") return;
    const observer = new MutationObserver(() => {
      const docs = reportDocuments();
      const current = docs.find((node) => node.getAttribute("data-report-document-bridge") === "true") || docs[0] || null;
      const root = document.querySelector(".bte-cdash");
      const grid = root && root.querySelector(".bte-cdash__grid");
      if (
        !current ||
        docs.length > 1 ||
        current.getAttribute("data-analysis-id") !== lastSignature ||
        (grid && current.previousElementSibling !== grid)
      ) {
        scheduleMount();
      }
    });
    observer.observe(target, { childList: true, subtree: true });
    global.setTimeout(scheduleMount, 250);
    global.setTimeout(scheduleMount, 1000);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start, { once: true });
  } else {
    start();
  }
})(window);
