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
    if (typeof value === "string") return value.trim();
    if (typeof value === "number" && Number.isFinite(value)) return String(value);
    return "";
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

  function numberValue(value) {
    if (typeof value === "number" && Number.isFinite(value)) return value;
    if (typeof value === "string" && value.trim() !== "" && Number.isFinite(Number(value))) {
      return Number(value);
    }
    return null;
  }

  function numericCount(value) {
    const direct = numberValue(value);
    if (direct != null) return direct;
    if (isRecord(value)) return numberValue(value.count);
    return null;
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
      fiveElements: adaptReportFiveElements(data),
      luck: adaptReportLuck(data),
    };
  }

  function adaptReportFiveElements(data) {
    const facts = isRecord(data && data.five_elements) ? data.five_elements : {};
    const counts = isRecord(facts.counts) ? facts.counts : {};
    const source = [
      { key: "wood", label: "Mộc" },
      { key: "fire", label: "Hỏa" },
      { key: "earth", label: "Thổ" },
      { key: "metal", label: "Kim" },
      { key: "water", label: "Thủy" },
    ];
    const items = source
      .map((item) => {
        const count = numericCount(counts[item.key]) ?? numericCount(facts[item.key]);
        return count == null ? null : { ...item, count };
      })
      .filter(Boolean);
    if (!items.length) return null;
    const maxCount = Math.max(1, ...items.map((item) => item.count));
    const minCount = Math.min(...items.map((item) => item.count));
    return {
      items,
      maxCount,
      dominantLabel: items.filter((item) => item.count === maxCount).map((item) => item.label).join(", "),
      weakLabel: items.filter((item) => item.count === minCount).map((item) => item.label).join(", "),
      methodNote: text(facts.method_note),
    };
  }

  function rangeText(start, end, suffix) {
    const from = numberValue(start);
    const to = numberValue(end);
    if (from == null || to == null) return "";
    return `${from}-${to}${suffix || ""}`;
  }

  function cycleKey(cycle) {
    if (!isRecord(cycle)) return "";
    return [text(cycle.gan_zhi), text(cycle.age_start), text(cycle.year_start)].join("|");
  }

  function luckAxis(data) {
    const contract = isRecord(data && data.bazi_analysis_result) ? data.bazi_analysis_result : {};
    const narrative = isRecord(contract.customer_narrative) ? contract.customer_narrative : {};
    const luckCycles = isRecord(narrative.luck_cycles) ? narrative.luck_cycles : {};
    const axis = isRecord(luckCycles.balance_axis) ? luckCycles.balance_axis : {};
    return {
      usefulElements: textList(axis.useful_elements),
      unfavorableElements: textList(axis.unfavorable_elements),
    };
  }

  function adaptReportLuck(data) {
    const luck = isRecord(data && data.luck) ? data.luck : {};
    const cyclesSource = arrayOf(luck.cycles).filter(isRecord);
    const current = isRecord(luck.current_cycle) ? luck.current_cycle : null;
    const currentKey = cycleKey(current);
    const currentGanZhi = text(current && current.gan_zhi);
    const cycles = cyclesSource
      .map((cycle) => {
        const ganZhi = text(cycle.gan_zhi);
        if (!ganZhi) return null;
        const elements = [text(cycle.stem_element), text(cycle.branch_element)].filter(Boolean).join(" / ");
        return {
          ganZhi,
          ageRange: rangeText(cycle.age_start, cycle.age_end, " tuổi"),
          yearRange: rangeText(cycle.year_start, cycle.year_end, ""),
          elements,
          isCurrent: cycleKey(cycle) === currentKey || Boolean(currentGanZhi && ganZhi === currentGanZhi),
        };
      })
      .filter(Boolean);
    if (!cycles.length && !current) return null;
    const axis = luckAxis(data);
    return {
      direction: text(luck.direction_label) || text(luck.direction),
      startAge: text(luck.start_age),
      currentLabel: currentGanZhi,
      usefulElements: axis.usefulElements,
      unfavorableElements: axis.unfavorableElements,
      cycles,
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

  function renderFiveElementsVisual(model) {
    if (!model || !model.items || !model.items.length) return null;
    const visual = document.createElement("aside");
    visual.className = "bte-report-doc__visual bte-report-doc__visual--elements";
    visual.setAttribute("aria-label", "Biểu đồ Ngũ hành");
    const head = document.createElement("header");
    head.className = "bte-report-doc__visual-head";
    const titleBox = document.createElement("div");
    appendText(titleBox, "p", "bte-report-doc__visual-kicker", "Biểu đồ Ngũ hành");
    appendText(titleBox, "h4", "bte-report-doc__visual-title", "Phân bố khí trong lá số");
    head.appendChild(titleBox);
    visual.appendChild(head);

    const chart = document.createElement("div");
    chart.className = "bte-report-doc__element-chart";
    model.items.forEach((item) => {
      const column = document.createElement("div");
      column.className = "bte-report-doc__element";
      column.setAttribute("data-element", item.key);
      appendText(column, "span", "bte-report-doc__element-label", item.label);
      const track = document.createElement("span");
      track.className = "bte-report-doc__element-track";
      track.setAttribute("aria-hidden", "true");
      const bar = document.createElement("span");
      bar.className = "bte-report-doc__element-bar";
      bar.style.height = `${Math.max(8, Math.round((item.count / model.maxCount) * 100))}%`;
      track.appendChild(bar);
      column.appendChild(track);
      appendText(column, "span", "bte-report-doc__element-count", String(item.count));
      chart.appendChild(column);
    });
    visual.appendChild(chart);

    const row = document.createElement("div");
    row.className = "bte-report-doc__insight-row";
    if (model.dominantLabel) appendText(row, "span", "bte-report-doc__insight-chip", `Nổi bật: ${model.dominantLabel}`);
    if (model.weakLabel) appendText(row, "span", "bte-report-doc__insight-chip", `Cần bồi: ${model.weakLabel}`);
    if (row.childNodes.length) visual.appendChild(row);
    if (model.methodNote) appendText(visual, "p", "bte-report-doc__visual-note", model.methodNote);
    return visual;
  }

  function cycleElementHits(cycle, elements) {
    return arrayOf(elements).filter((element) => cycle.elements && cycle.elements.includes(element)).join(", ");
  }

  function renderLuckVisual(model) {
    if (!model || !model.cycles || !model.cycles.length) return null;
    const visual = document.createElement("aside");
    visual.className = "bte-report-doc__visual bte-report-doc__visual--luck";
    visual.setAttribute("aria-label", "Timeline Đại vận");
    const head = document.createElement("header");
    head.className = "bte-report-doc__visual-head";
    const titleBox = document.createElement("div");
    appendText(titleBox, "p", "bte-report-doc__visual-kicker", "Timeline Đại vận");
    appendText(titleBox, "h4", "bte-report-doc__visual-title", "Nhịp vận theo từng giai đoạn");
    head.appendChild(titleBox);
    visual.appendChild(head);

    const summary = document.createElement("div");
    summary.className = "bte-report-doc__luck-summary";
    if (model.direction) appendText(summary, "span", "", `Chiều vận: ${model.direction}`);
    if (model.startAge) appendText(summary, "span", "", `Khởi vận: ${model.startAge} tuổi`);
    if (model.currentLabel) appendText(summary, "span", "", `Hiện tại: ${model.currentLabel}`);
    if (summary.childNodes.length) visual.appendChild(summary);

    const list = document.createElement("ol");
    list.className = "bte-report-doc__luck-list";
    model.cycles.forEach((cycle, index) => {
      const item = document.createElement("li");
      item.className = "bte-report-doc__luck-cycle";
      if (cycle.isCurrent) item.setAttribute("data-current", "true");
      const top = document.createElement("div");
      top.className = "bte-report-doc__luck-top";
      appendText(top, "span", "bte-report-doc__luck-index", String(index + 1).padStart(2, "0"));
      const info = document.createElement("div");
      appendText(info, "strong", "", cycle.ganZhi);
      appendText(info, "span", "", [cycle.ageRange, cycle.yearRange].filter(Boolean).join(" · "));
      top.appendChild(info);
      item.appendChild(top);
      if (cycle.elements) appendText(item, "p", "bte-report-doc__luck-elements", cycle.elements);
      const points = document.createElement("div");
      points.className = "bte-report-doc__luck-points";
      const usefulHits = cycleElementHits(cycle, model.usefulElements);
      const cautionHits = cycleElementHits(cycle, model.unfavorableElements);
      const plus = document.createElement("p");
      appendText(plus, "span", "", "+");
      appendText(plus, "span", "", usefulHits ? `Chạm trục nên dùng: ${usefulHits}.` : "Có thể mở việc khi mục tiêu và nhịp hành động rõ.");
      points.appendChild(plus);
      const minus = document.createElement("p");
      appendText(minus, "span", "", "-");
      appendText(minus, "span", "", cautionHits ? `Cần tiết chế: ${cautionHits}.` : "Cần đọc cùng mệnh cục gốc trước quyết định lớn.");
      points.appendChild(minus);
      item.appendChild(points);
      list.appendChild(item);
    });
    visual.appendChild(list);
    return visual;
  }

  function renderChapterVisual(chapter, model) {
    if (chapter.id === "five_elements") return renderFiveElementsVisual(model.fiveElements);
    if (chapter.id === "luck_cycles") return renderLuckVisual(model.luck);
    return null;
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
      const visual = renderChapterVisual(chapter, model);
      if (visual) chapterNode.appendChild(visual);
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
      .bte-report-doc__visual {
        margin: var(--space-4, 18px) 0;
        padding: var(--space-4, 18px);
        border: 1px solid var(--cdash-border, #dfe3ea);
        border-radius: 8px;
        background: #fff7d6;
      }
      .bte-report-doc__visual-head {
        display: flex;
        flex-wrap: wrap;
        align-items: baseline;
        justify-content: space-between;
        gap: var(--space-2, 8px);
        margin-bottom: var(--space-3, 12px);
      }
      .bte-report-doc__visual-kicker {
        margin: 0;
        color: var(--cdash-muted, #5f6b7a);
        font-size: var(--font-size-metadata, 0.78rem);
        font-weight: 700;
        letter-spacing: var(--letter-spacing-metadata, 0.12em);
        text-transform: uppercase;
      }
      .bte-report-doc__visual-title {
        margin: 0;
        color: var(--cdash-text, #111827);
        font-family: var(--font-family-display, inherit);
        font-size: 1rem;
        font-weight: 700;
      }
      .bte-report-doc__element-chart {
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        align-items: end;
        gap: var(--space-3, 12px);
        min-height: 13rem;
        padding: var(--space-2, 8px) 0;
      }
      .bte-report-doc__element {
        display: grid;
        grid-template-rows: auto 1fr auto;
        gap: var(--space-2, 8px);
        min-width: 0;
        height: 100%;
        text-align: center;
      }
      .bte-report-doc__element-label,
      .bte-report-doc__element-count {
        color: #7f1d1d;
        font-weight: 700;
      }
      .bte-report-doc__element-track {
        display: flex;
        align-items: end;
        justify-content: center;
        min-height: 8.5rem;
      }
      .bte-report-doc__element-bar {
        width: min(68%, 3.75rem);
        min-height: 0.5rem;
        border-radius: 4px 4px 0 0;
        background: var(--element-color, #64748b);
      }
      .bte-report-doc__element[data-element="wood"] {
        --element-color: #4f8f5f;
      }
      .bte-report-doc__element[data-element="fire"] {
        --element-color: #cf573f;
      }
      .bte-report-doc__element[data-element="earth"] {
        --element-color: #bd9b4f;
      }
      .bte-report-doc__element[data-element="metal"] {
        --element-color: #92a0aa;
      }
      .bte-report-doc__element[data-element="water"] {
        --element-color: #437b9e;
      }
      .bte-report-doc__insight-row,
      .bte-report-doc__luck-summary {
        display: flex;
        flex-wrap: wrap;
        gap: var(--space-2, 8px);
        margin-top: var(--space-3, 12px);
      }
      .bte-report-doc__insight-chip,
      .bte-report-doc__luck-summary span {
        display: inline-flex;
        align-items: center;
        min-height: 1.75rem;
        padding: 4px 10px;
        border: 1px solid var(--cdash-border, #dfe3ea);
        border-radius: 999px;
        background: #ffffff;
        color: var(--cdash-text, #111827);
        font-size: var(--font-size-caption, 0.875rem);
        font-weight: 700;
      }
      .bte-report-doc__visual-note {
        margin: var(--space-3, 12px) 0 0;
        color: var(--cdash-muted, #5f6b7a);
        font-size: var(--font-size-caption, 0.875rem);
        line-height: 1.5;
      }
      .bte-report-doc__luck-list {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: var(--space-3, 12px);
        margin: var(--space-4, 18px) 0 0;
        padding: 0;
        list-style: none;
      }
      .bte-report-doc__luck-cycle {
        display: grid;
        gap: var(--space-2, 8px);
        padding: var(--space-3, 12px);
        border: 1px solid var(--cdash-border, #dfe3ea);
        border-radius: 8px;
        background: #ffffff;
      }
      .bte-report-doc__luck-cycle[data-current="true"] {
        border-color: #0f9f75;
        background: #eaf8f2;
      }
      .bte-report-doc__luck-top {
        display: grid;
        grid-template-columns: 2rem minmax(0, 1fr);
        gap: var(--space-2, 8px);
        align-items: start;
      }
      .bte-report-doc__luck-index {
        color: #0f9f75;
        font-family: var(--font-family-display, inherit);
        font-weight: 700;
        font-variant-numeric: tabular-nums;
      }
      .bte-report-doc__luck-top strong,
      .bte-report-doc__luck-top span {
        display: block;
      }
      .bte-report-doc__luck-top strong {
        color: var(--cdash-text, #111827);
        font-size: 1rem;
      }
      .bte-report-doc__luck-top span,
      .bte-report-doc__luck-elements {
        color: var(--cdash-muted, #5f6b7a);
        font-size: var(--font-size-caption, 0.875rem);
      }
      .bte-report-doc__luck-elements {
        margin: 0;
        font-weight: 700;
      }
      .bte-report-doc__luck-points {
        display: grid;
        gap: 6px;
      }
      .bte-report-doc__luck-points p {
        display: grid;
        grid-template-columns: 1.25rem minmax(0, 1fr);
        gap: 6px;
        margin: 0;
        color: var(--cdash-text, #111827);
        font-size: var(--font-size-caption, 0.875rem);
        line-height: 1.45;
      }
      .bte-report-doc__luck-points span:first-child {
        color: #0f9f75;
        font-weight: 800;
        text-align: center;
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
        .bte-report-doc__element-chart,
        .bte-report-doc__luck-list {
          grid-template-columns: 1fr;
        }
        .bte-report-doc__element-chart {
          min-height: 0;
        }
        .bte-report-doc__element {
          grid-template-columns: 3rem minmax(0, 1fr) 2rem;
          grid-template-rows: auto;
          align-items: center;
          text-align: left;
        }
        .bte-report-doc__element-track {
          align-items: center;
          justify-content: start;
          min-height: 0.75rem;
        }
        .bte-report-doc__element-bar {
          width: 100%;
          height: 0.75rem !important;
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
