/**
 * Runtime bridge for the Bát Tự customer report document.
 *
 * The source React view already renders this section, but the static result bundle
 * can be stale in local desktop runs. This bridge only reads the customer-safe
 * bazi_analysis_result.customer_narrative contract and mounts the report above
 * the technical dashboard when the current bundle has not rendered it yet.
 */
(function (global) {
  const DOCUMENT_SELECTOR = '[data-report-document="bazi-v1"]';
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
    appendText(header, "p", "bte-report-doc__subtitle", model.subtitle);
    section.appendChild(header);

    const body = document.createElement("div");
    body.className = "bte-report-doc__body";
    model.chapters.forEach((chapter) => {
      const chapterNode = document.createElement("section");
      chapterNode.className = "bte-report-doc__chapter";
      chapterNode.setAttribute("data-report-chapter", chapter.id);
      appendText(chapterNode, "h3", "bte-report-doc__chapter-title", chapter.title);
      chapter.paragraphs.forEach((paragraph) => {
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
    section.appendChild(body);
    return section;
  }

  function ensureStyles() {
    if (document.getElementById(STYLE_ID)) return;
    const style = document.createElement("style");
    style.id = STYLE_ID;
    style.textContent = `
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
        max-width: 920px;
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
        margin: var(--space-2, 8px) 0 0;
        color: var(--cdash-muted, #5f6b7a);
        font-size: var(--font-size-body, 1rem);
        line-height: var(--line-height-body, 1.55);
      }
      .bte-report-doc__body {
        display: grid;
        grid-template-columns: minmax(0, 1fr);
        gap: var(--space-5, 24px);
        max-width: 980px;
      }
      .bte-report-doc__chapter {
        min-width: 0;
        padding-top: var(--space-1, 4px);
      }
      .bte-report-doc__chapter + .bte-report-doc__chapter {
        padding-top: var(--space-5, 24px);
        border-top: 1px solid var(--cdash-border, #dfe3ea);
      }
      .bte-report-doc__chapter-title {
        margin: 0 0 var(--space-3, 12px);
        color: var(--cdash-text, #111827);
        font-family: var(--font-family-display, inherit);
        font-size: var(--font-size-subsection, 1.1rem);
        font-weight: var(--font-weight-semibold, 700);
        line-height: var(--line-height-heading, 1.25);
      }
      .bte-report-doc__paragraph {
        margin: 0 0 var(--space-3, 12px);
        color: var(--cdash-text, #111827);
        font-size: var(--font-size-body, 1rem);
        line-height: 1.72;
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
      }
    `;
    document.head.appendChild(style);
  }

  function mountReport() {
    pending = false;
    const root = document.querySelector(".bte-cdash");
    const grid = root && root.querySelector(".bte-cdash__grid");
    if (!root || !grid) return;

    const record = loadDisplayRecord();
    const data = record && record.data;
    const model = adaptReport(data);
    if (!model) return;

    const signature = String(
      (record && (record.analysis_id || record.id)) ||
        (data && (data.analysis_id || data.request_id || data.case_id)) ||
        model.title,
    );
    const existing = root.querySelector(DOCUMENT_SELECTOR);
    if (existing && existing.getAttribute("data-report-document-bridge") !== "true") {
      return;
    }
    if (existing && existing.getAttribute("data-analysis-id") === signature) {
      lastSignature = signature;
      return;
    }
    if (existing) existing.remove();
    ensureStyles();
    grid.parentNode.insertBefore(renderReport(model, signature), grid);
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
      const current = document.querySelector(DOCUMENT_SELECTOR);
      if (!current || current.getAttribute("data-analysis-id") !== lastSignature) {
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
