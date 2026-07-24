/**
 * Interpretation presentation layer (Sprint 5).
 * Renders interpretation JSON as readable cards — display only, no invented text.
 */
(function (global) {
  const MISSING = "--";

  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  /** Preferred section order (shown only when API provides data). */
  const KNOWN_SECTIONS = [
    {
      id: "overview",
      title: "Tổng quan",
      keys: ["summary", "tong_quan", "overview", "general", "tổng_quan"],
    },
    {
      id: "career",
      title: "Sự nghiệp",
      keys: ["career", "su_nghiep", "sự_nghiệp", "job", "work"],
    },
    {
      id: "wealth",
      title: "Tài vận",
      keys: ["wealth", "tai_van", "tài_vận", "finance", "money", "tai_chinh"],
    },
    {
      id: "marriage",
      title: "Hôn nhân",
      keys: [
        "marriage",
        "relationship",
        "hon_nhan",
        "hôn_nhân",
        "quan_he",
        "love",
      ],
    },
    {
      id: "health",
      title: "Sức khỏe",
      keys: ["health", "suc_khoe", "sức_khỏe", "body"],
    },
    {
      id: "luck",
      title: "Đại vận",
      keys: ["luck", "dai_van", "đại_vận", "major_luck", "da_yun"],
    },
    {
      id: "annual",
      title: "Lưu niên",
      keys: ["annual", "luu_nien", "lưu_niên", "yearly", "year_luck", "liu_nian"],
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

  const TITLE_ALIASES = {};
  KNOWN_SECTIONS.forEach(function (sec) {
    TITLE_ALIASES[sec.id] = sec.title;
    sec.keys.forEach(function (k) {
      TITLE_ALIASES[String(k).toLowerCase()] = sec.title;
    });
  });
  TITLE_ALIASES.warning = "Cảnh báo";
  TITLE_ALIASES.personality = "Tính cách";
  TITLE_ALIASES.useful_god = "Dụng thần";
  TITLE_ALIASES.pattern = "Cách cục";
  TITLE_ALIASES.conclusion = "Kết luận";

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

  function humanizeKey(key) {
    var lower = String(key || "").toLowerCase();
    if (TITLE_ALIASES[lower]) return TITLE_ALIASES[lower];
    return String(key)
      .replace(/[_-]+/g, " ")
      .replace(/\s+/g, " ")
      .trim()
      .replace(/^\w/, function (c) {
        return c.toUpperCase();
      });
  }

  function extractBadge(node) {
    if (!node || typeof node !== "object" || Array.isArray(node)) return null;
    var keys = ["badge", "tag", "status", "level", "severity", "grade", "label"];
    for (var i = 0; i < keys.length; i++) {
      var v = node[keys[i]];
      if (v != null && v !== "" && typeof v !== "object") return String(v);
    }
    return null;
  }

  function extractHighlight(node) {
    if (!node || typeof node !== "object" || Array.isArray(node)) return false;
    if (node.highlight === true || node.emphasized === true || node.important === true) {
      return true;
    }
    var level = String(node.level || node.severity || node.status || "").toLowerCase();
    return (
      level === "warning" ||
      level === "high" ||
      level === "critical" ||
      level === "danger" ||
      level === "alert"
    );
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
        var t =
          item.sentence ||
          item.text ||
          item.content ||
          item.body ||
          item.description ||
          item.summary ||
          null;
        if (t != null && t !== "") parts.push(String(t));
      }
    });
    return parts.length ? parts.join("\n\n") : MISSING;
  }

  /**
   * Normalize any API node into { title?, body, badge?, highlight? }.
   * Does not invent wording — only reads fields.
   */
  function normalizeNode(node, fallbackTitle) {
    if (node == null || node === "") {
      return null;
    }
    if (typeof node === "string" || typeof node === "number" || typeof node === "boolean") {
      return {
        title: fallbackTitle || null,
        body: present(node),
        badge: null,
        highlight: false,
      };
    }
    if (Array.isArray(node)) {
      var joined = joinSentences(node);
      if (isEmptyBody(joined)) return null;
      return {
        title: fallbackTitle || null,
        body: joined,
        badge: null,
        highlight: false,
      };
    }
    if (typeof node !== "object") return null;

    var title =
      node.title ||
      node.heading ||
      node.name ||
      node.section ||
      node.label ||
      fallbackTitle ||
      null;
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
                : node.sentence != null
                  ? node.sentence
                  : null;

    if (Array.isArray(body)) body = joinSentences(body);
    if (body == null && Array.isArray(node.sentences)) body = joinSentences(node.sentences);
    if (body == null && Array.isArray(node.paragraphs)) body = joinSentences(node.paragraphs);
    if (body == null && Array.isArray(node.rules)) body = joinSentences(node.rules);
    if (body != null && typeof body === "object") {
      body = present(body.sentence || body.text || body.content || MISSING);
    }
    if (body != null) body = present(body);

    // Plain object map of nested subsections → render as stacked paragraphs of values only.
    if (isEmptyBody(body)) {
      var nested = [];
      Object.keys(node).forEach(function (k) {
        if (
          k === "title" ||
          k === "heading" ||
          k === "name" ||
          k === "section" ||
          k === "label" ||
          k === "badge" ||
          k === "tag" ||
          k === "status" ||
          k === "level" ||
          k === "severity" ||
          k === "grade" ||
          k === "highlight" ||
          k === "emphasized" ||
          k === "important" ||
          k === "html"
        ) {
          return;
        }
        var child = normalizeNode(node[k], humanizeKey(k));
        if (child && !isEmptyBody(child.body)) {
          nested.push(
            (child.title ? child.title + ": " : "") + child.body
          );
        }
      });
      if (nested.length) body = nested.join("\n\n");
    }

    if (isEmptyBody(body)) return null;

    return {
      title: title ? String(title) : fallbackTitle || null,
      body: body,
      badge: extractBadge(node),
      highlight: extractHighlight(node),
    };
  }

  function pickKnown(data, keys) {
    for (var i = 0; i < keys.length; i++) {
      var key = keys[i];
      if (Object.prototype.hasOwnProperty.call(data, key) && data[key] != null && data[key] !== "") {
        return { key: key, value: data[key] };
      }
    }
    return null;
  }

  function collectSections(data) {
    var used = {};
    var out = [];

    function pushSection(id, title, value, fromKey) {
      var normalized = normalizeNode(value, title);
      if (!normalized) return;
      var keyMark = id || fromKey || title;
      if (used[keyMark]) return;
      used[keyMark] = true;
      if (fromKey) used[fromKey] = true;
      out.push({
        id: id || fromKey || "section",
        title: normalized.title || title,
        body: normalized.body,
        badge: normalized.badge,
        highlight: normalized.highlight,
      });
    }

    // 1) Preferred known sections from top-level keys
    KNOWN_SECTIONS.forEach(function (spec) {
      var found = pickKnown(data, spec.keys);
      if (!found) return;
      // summary used as Tổng quan
      pushSection(spec.id, spec.title, found.value, found.key);
    });

    // 2) data.sections as object or array
    if (data.sections && typeof data.sections === "object") {
      if (Array.isArray(data.sections)) {
        data.sections.forEach(function (item, idx) {
          var n = normalizeNode(item, t("interpretation.section_n", { n: idx + 1 }));
          if (!n) return;
          var id = String((item && (item.id || item.section || item.name)) || "sections_" + idx);
          if (used[id] || used[n.title]) return;
          pushSection(id, n.title || humanizeKey(id), item, id);
        });
      } else {
        Object.keys(data.sections).forEach(function (key) {
          if (used[key]) return;
          pushSection(key, humanizeKey(key), data.sections[key], key);
        });
      }
    }

    // 3) Other top-level content keys
    Object.keys(data).forEach(function (key) {
      var lower = String(key).toLowerCase();
      if (META_KEYS[lower] || used[key] || used[lower]) return;
      // skip pure numeric meta already covered
      if (/_count$/.test(lower)) return;
      var value = data[key];
      if (value == null || value === "") return;
      if (typeof value === "number" || typeof value === "boolean") return;
      pushSection(lower, humanizeKey(key), value, key);
    });

    return out;
  }

  function badgeHtml(text, tone) {
    if (!text) return "";
    return (
      '<span class="bte-badge bte-badge-' +
      esc(tone || "neutral") +
      '">' +
      esc(String(text)) +
      "</span>"
    );
  }

  function metaBar(data) {
    var bits = [];
    if (Object.prototype.hasOwnProperty.call(data, "confidence")) {
      bits.push(badgeHtml(t("interpretation.confidence", { value: present(data.confidence) }), "follow"));
    }
    if (Object.prototype.hasOwnProperty.call(data, "section_count")) {
      bits.push(badgeHtml(t("interpretation.sections", { value: present(data.section_count) }), "pattern"));
    }
    if (Object.prototype.hasOwnProperty.call(data, "sentence_count")) {
      bits.push(badgeHtml(t("interpretation.sentences", { value: present(data.sentence_count) }), "useful"));
    }
    if (Object.prototype.hasOwnProperty.call(data, "matched_rule_count")) {
      bits.push(badgeHtml(t("interpretation.matched", { value: present(data.matched_rule_count) }), "neutral"));
    }
    if (Object.prototype.hasOwnProperty.call(data, "resolved_rule_count")) {
      bits.push(badgeHtml(t("interpretation.resolved", { value: present(data.resolved_rule_count) }), "climate"));
    }
    if (!bits.length) return "";
    return '<div class="bte-interp-status">' + bits.join("") + "</div>";
  }

  function sectionCard(section) {
    var highlightClass = section.highlight ? " bte-interp-highlight" : "";
    var bodyHtml = esc(section.body).replace(/\n/g, "<br>");
    return (
      '<article class="bte-card bte-interp-card' +
      highlightClass +
      '" data-section="' +
      esc(section.id) +
      '">' +
      '<header class="bte-interp-head">' +
      "<h3>" +
      esc(section.title) +
      "</h3>" +
      (section.badge ? badgeHtml(section.badge, "pattern") : "") +
      "</header>" +
      '<div class="bte-interp-body">' +
      bodyHtml +
      "</div>" +
      "</article>"
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

      var sections = collectSections(data);
      var cards = sections.length
        ? sections.map(sectionCard).join("")
        : '<article class="bte-card bte-interp-card"><div class="bte-interp-body">' +
          esc(MISSING) +
          "</div></article>";

      return (
        '<section class="bte-interp" aria-label="' + esc(t("interpretation.title")) + '">' +
        '<header class="bte-calendar-head">' +
        "<h2>" + esc(t("interpretation.title")) + "</h2>" +
        '<p class="bte-calendar-sub">' + esc(t("interpretation.subtitle")) + "</p>" +
        "</header>" +
        metaBar(data) +
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
