/**
 * Interpretation presentation layer (Luận Giải).
 * All domain interpretations live here as ordered chapters.
 * Display only — no invented prose.
 */
(function (global) {
  const MISSING = "--";
  const INTERNAL_LINE =
    /\b(?:FPR|SPR|PAT|PSC|PPR|SER|SDR|CBR|PC)\d+\b|\bstatus\s*=|^[a-z0-9_]+$/i;
  const RAW_UNACCENTED = /^[A-Za-z][A-Za-z0-9 _\-/()]{4,}$/;

  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  /** Fixed chapter order for the BaZi report interpretation tab. */
  const CHAPTERS = [
    {
      id: "overview",
      titleKey: "interpretation.ch_overview",
      keys: ["summary", "tong_quan", "overview", "general", "tổng_quan"],
      sectionIds: ["summary", "overview", "tong_quan", "general"],
    },
    {
      id: "bazi",
      titleKey: "interpretation.ch_bazi",
      keys: ["bazi", "bat_tu", "four_pillars"],
      sectionIds: ["bazi", "bat_tu", "pillars", "four_pillars"],
    },
    {
      id: "five_elements",
      titleKey: "interpretation.ch_five_elements",
      keys: ["five_elements", "wuxing", "ngu_hanh", "elements"],
      sectionIds: ["five_elements", "wuxing", "ngu_hanh", "elements"],
    },
    {
      id: "ten_gods",
      titleKey: "interpretation.ch_ten_gods",
      keys: ["ten_gods", "thap_than", "shi_shen"],
      sectionIds: ["ten_gods", "thap_than", "shi_shen"],
    },
    {
      id: "shensha",
      titleKey: "interpretation.ch_shensha",
      keys: ["shensha", "than_sat", "shen_sha"],
      sectionIds: ["shensha", "than_sat", "shen_sha"],
    },
    {
      id: "useful_god",
      titleKey: "interpretation.ch_useful_god",
      keys: ["useful_god", "dung_than", "yong_shen"],
      sectionIds: ["useful_god", "dung_than", "yong_shen"],
    },
    {
      id: "structure",
      titleKey: "interpretation.ch_structure",
      keys: ["structure", "pattern", "cach_cuc", "ge_ju"],
      sectionIds: ["structure", "pattern", "cach_cuc", "ge_ju"],
    },
    {
      id: "career",
      titleKey: "interpretation.ch_career",
      keys: ["career", "su_nghiep", "sự_nghiệp", "job", "work"],
      sectionIds: ["career", "su_nghiep", "job", "work"],
    },
    {
      id: "wealth",
      titleKey: "interpretation.ch_wealth",
      keys: ["wealth", "tai_van", "tài_vận", "finance", "money"],
      sectionIds: ["wealth", "tai_van", "finance", "money"],
    },
    {
      id: "official",
      titleKey: "interpretation.ch_official",
      keys: ["official", "quan_van", "quan_loc", "office"],
      sectionIds: ["official", "quan_van", "quan_loc", "office"],
    },
    {
      id: "marriage",
      titleKey: "interpretation.ch_marriage",
      keys: ["marriage", "relationship", "hon_nhan", "hôn_nhân", "love"],
      sectionIds: ["marriage", "relationship", "hon_nhan", "love"],
    },
    {
      id: "children",
      titleKey: "interpretation.ch_children",
      keys: ["children", "con_cai", "tu_tuc", "offspring"],
      sectionIds: ["children", "con_cai", "tu_tuc", "offspring"],
    },
    {
      id: "parents",
      titleKey: "interpretation.ch_parents",
      keys: ["parents", "cha_me", "phu_mau"],
      sectionIds: ["parents", "cha_me", "phu_mau"],
    },
    {
      id: "siblings",
      titleKey: "interpretation.ch_siblings",
      keys: ["siblings", "anh_em", "huynh_de"],
      sectionIds: ["siblings", "anh_em", "huynh_de"],
    },
    {
      id: "luck_cycles",
      titleKey: "interpretation.ch_luck_cycles",
      keys: ["luck", "dai_van", "đại_vận", "major_luck", "da_yun", "luck_cycles"],
      sectionIds: ["luck", "dai_van", "major_luck", "da_yun", "luck_cycles"],
    },
    {
      id: "annual_luck",
      titleKey: "interpretation.ch_annual_luck",
      keys: ["annual", "luu_nien", "lưu_niên", "yearly", "year_luck", "liu_nian"],
      sectionIds: ["annual", "luu_nien", "yearly", "liu_nian"],
    },
    {
      id: "feng_shui",
      titleKey: "interpretation.ch_feng_shui",
      keys: ["feng_shui", "phong_thuy", "bat_trach", "fengshui"],
      sectionIds: ["feng_shui", "phong_thuy", "bat_trach", "fengshui"],
    },
    {
      id: "conclusion",
      titleKey: "interpretation.ch_conclusion",
      keys: ["conclusion", "ket_luan", "recommendation", "khuyen_nghi"],
      sectionIds: ["conclusion", "ket_luan", "recommendation", "khuyen_nghi"],
    },
  ];

  const META_KEYS = {
    summary: true,
    sentence_count: true,
    section_count: true,
    matched_rule_count: true,
    resolved_rule_count: true,
    confidence: true,
    success: true,
    error: true,
    sections: true,
    modules: true,
    metadata: true,
    request_id: true,
    pipeline: true,
  };

  function esc(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function present(value) {
    if (value === null || value === undefined || value === "") return MISSING;
    if (typeof value === "number" && Number.isNaN(value)) return MISSING;
    if (typeof value === "boolean") return value ? t("common.yes") : t("common.no");
    return String(value);
  }

  function isEmptyBody(text) {
    return !text || text === MISSING || String(text).trim() === "";
  }

  function cleanBodyText(text) {
    if (text == null || text === "") return "";
    var lines = String(text)
      .split(/\r?\n/)
      .map(function (line) {
        return String(line || "").trim();
      })
      .filter(function (line) {
        if (!line) return false;
        if (INTERNAL_LINE.test(line)) return false;
        if (RAW_UNACCENTED.test(line)) return false;
        return true;
      });
    return lines.join("\n");
  }

  function joinSentences(list) {
    var parts = [];
    list.forEach(function (item) {
      if (item == null || item === "") return;
      if (typeof item === "string" || typeof item === "number") {
        parts.push(String(item));
        return;
      }
      if (typeof item === "object") {
        var txt =
          item.sentence ||
          item.text ||
          item.content ||
          item.body ||
          item.description ||
          item.summary ||
          null;
        if (txt != null && txt !== "") parts.push(String(txt));
      }
    });
    return parts.length ? parts.join("\n\n") : "";
  }

  function normalizeNode(node) {
    if (node == null || node === "") return "";
    if (typeof node === "string" || typeof node === "number" || typeof node === "boolean") {
      return cleanBodyText(present(node));
    }
    if (Array.isArray(node)) return cleanBodyText(joinSentences(node));
    if (typeof node !== "object") return "";

    var body =
      node.body != null
        ? node.body
        : node.text != null
          ? node.text
          : node.content != null
            ? node.content
            : node.summary != null
              ? node.summary
              : node.description != null
                ? node.description
                : null;
    if (Array.isArray(body)) body = joinSentences(body);
    if (body == null && Array.isArray(node.sentences)) body = joinSentences(node.sentences);
    if (body == null && Array.isArray(node.paragraphs)) body = joinSentences(node.paragraphs);
    if (body != null && typeof body === "object") {
      body = present(body.sentence || body.text || body.content || "");
    }
    return cleanBodyText(body == null ? "" : String(body));
  }

  function buildSectionIndex(data) {
    var byId = {};
    var byTitle = {};
    var list = [];

    function add(id, title, body) {
      if (isEmptyBody(body)) return;
      var entry = {
        id: id || "section",
        title: title || id,
        body: body,
      };
      list.push(entry);
      if (id) byId[String(id).toLowerCase()] = entry;
      if (title) byTitle[String(title).toLowerCase()] = entry;
    }

    if (Array.isArray(data.sections)) {
      data.sections.forEach(function (item, idx) {
        if (!item) return;
        var id = String((item && (item.id || item.section || item.name)) || "sec_" + idx);
        var title = (item && (item.title || item.name || item.heading)) || id;
        add(id, title, normalizeNode(item));
      });
    } else if (data.sections && typeof data.sections === "object") {
      Object.keys(data.sections).forEach(function (key) {
        add(key, key, normalizeNode(data.sections[key]));
      });
    }

    Object.keys(data).forEach(function (key) {
      var lower = String(key).toLowerCase();
      if (META_KEYS[lower]) return;
      if (/_count$/.test(lower)) return;
      var value = data[key];
      if (value == null || value === "") return;
      if (typeof value === "number" || typeof value === "boolean") return;
      if (byId[lower]) return;
      add(key, key, normalizeNode(value));
    });

    return { list: list, byId: byId, byTitle: byTitle };
  }

  function findChapterBody(index, chapter) {
    var i;
    if (chapter.sectionIds) {
      for (i = 0; i < chapter.sectionIds.length; i++) {
        var id = String(chapter.sectionIds[i]).toLowerCase();
        if (index.byId[id] && !isEmptyBody(index.byId[id].body)) {
          return index.byId[id].body;
        }
      }
    }
    if (chapter.keys) {
      for (i = 0; i < chapter.keys.length; i++) {
        var key = String(chapter.keys[i]).toLowerCase();
        if (index.byId[key] && !isEmptyBody(index.byId[key].body)) {
          return index.byId[key].body;
        }
        if (index.byTitle[key] && !isEmptyBody(index.byTitle[key].body)) {
          return index.byTitle[key].body;
        }
      }
    }
    // Fuzzy title match against known Vietnamese titles.
    var want = t(chapter.titleKey).toLowerCase();
    if (index.byTitle[want] && !isEmptyBody(index.byTitle[want].body)) {
      return index.byTitle[want].body;
    }
    var titles = Object.keys(index.byTitle);
    for (i = 0; i < titles.length; i++) {
      if (titles[i].indexOf(want) >= 0 || want.indexOf(titles[i]) >= 0) {
        if (!isEmptyBody(index.byTitle[titles[i]].body)) {
          return index.byTitle[titles[i]].body;
        }
      }
    }
    return "";
  }

  function metaBar(data) {
    var bits = [];
    if (data && data.confidence != null && data.confidence !== "") {
      bits.push(
        '<span class="bte-badge bte-badge-follow">' +
          esc(t("interpretation.confidence", { value: String(data.confidence) })) +
          "</span>"
      );
    }
    if (data && data.section_count != null && data.section_count > 0) {
      bits.push(
        '<span class="bte-badge bte-badge-neutral">' +
          esc(t("interpretation.sections", { value: String(data.section_count) })) +
          "</span>"
      );
    }
    if (!bits.length) return "";
    return '<div class="bte-interp-meta">' + bits.join("") + "</div>";
  }

  function chapterCard(chapter, body, index) {
    var empty = isEmptyBody(body);
    var title =
      String(index + 1) + ". " + t(chapter.titleKey);
    var bodyHtml = empty
      ? window.BteUI
        ? BteUI.emptyState(t("interpretation.chapter_empty"), "")
        : '<p class="muted">' + esc(t("interpretation.chapter_empty")) + "</p>"
      : '<div class="bte-interp-body">' + esc(body).replace(/\n/g, "<br>") + "</div>";
    if (window.BteUI && typeof BteUI.sectionCard === "function") {
      return (
        '<div data-section="' +
        esc(chapter.id) +
        '" id="interp-' +
        esc(chapter.id) +
        '">' +
        BteUI.sectionCard({
          id: "section-" + chapter.id,
          title: title,
          description: empty ? t("interpretation.chapter_empty") : "",
          badge: empty ? "—" : "",
          body: bodyHtml,
          collapsed: empty || index > 2,
        }) +
        "</div>"
      );
    }
    return (
      '<article class="bte-card bte-interp-card' +
      (empty ? " bte-interp-empty" : "") +
      '" data-section="' +
      esc(chapter.id) +
      '" id="interp-' +
      esc(chapter.id) +
      '">' +
      '<header class="bte-interp-head">' +
      "<h3>" +
      '<span class="bte-interp-num">' +
      esc(String(index + 1)) +
      ".</span> " +
      esc(t(chapter.titleKey)) +
      "</h3>" +
      "</header>" +
      '<div class="bte-interp-body">' +
      bodyHtml +
      "</div>" +
      "</article>"
    );
  }

  function tocNav(chapters) {
    return (
      '<nav class="bte-card bte-interp-toc" aria-label="' +
      esc(t("interpretation.toc")) +
      '">' +
      "<h3>" +
      esc(t("interpretation.toc")) +
      "</h3>" +
      "<ol>" +
      chapters
        .map(function (ch, idx) {
          return (
            '<li><a href="#interp-' +
            esc(ch.id) +
            '">' +
            esc(String(idx + 1) + ". " + t(ch.titleKey)) +
            "</a></li>"
          );
        })
        .join("") +
      "</ol>" +
      "</nav>"
    );
  }

  /**
   * @param {object|null|undefined} interpretation
   * @returns {string} HTML
   */
  function renderInterpretation(interpretation) {
    try {
      var data =
        interpretation &&
        typeof interpretation === "object" &&
        !Array.isArray(interpretation)
          ? interpretation
          : {};

      var index = buildSectionIndex(data);
      var cards = CHAPTERS.map(function (ch, idx) {
        return chapterCard(ch, findChapterBody(index, ch), idx);
      }).join("");

      return (
        '<section class="bte-interp" aria-label="' +
        esc(t("interpretation.title")) +
        '">' +
        '<header class="bte-calendar-head">' +
        "<h2>" +
        esc(t("interpretation.title")) +
        "</h2>" +
        '<p class="bte-calendar-sub">' +
        esc(t("interpretation.subtitle")) +
        "</p>" +
        "</header>" +
        metaBar(data) +
        tocNav(CHAPTERS) +
        '<div class="bte-interp-stack">' +
        cards +
        "</div>" +
        "</section>"
      );
    } catch (_) {
      return (
        '<section class="bte-interp">' +
        '<article class="bte-card bte-interp-card"><div class="bte-interp-body">' +
        esc(MISSING) +
        "</div></article>" +
        "</section>"
      );
    }
  }

  global.BtePresenters = global.BtePresenters || {};
  global.BtePresenters.interpretation = renderInterpretation;
})(window);
