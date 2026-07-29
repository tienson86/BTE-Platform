/**
 * Score presentation layer (Đánh Giá).
 * Renders score JSON as a dashboard — display only, no extra scoring math.
 *
 * Canonical API fields only (Sprint 2B):
 *   total_score, strength_score, pattern_score, wuxing_score,
 *   ten_god_score, useful_god_score, shensha_score, luck_score,
 *   confidence | confidence_score
 */
(function (global) {
  const MISSING = "--";

  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  /** Summary cards — one key per API field; no incorrect aliases. */
  const SUMMARY = [
    {
      id: "overall",
      labelKey: "score.overall",
      keys: ["total_score"],
      tone: "overall",
    },
    {
      id: "than",
      labelKey: "score.than",
      keys: ["strength_score"],
      tone: "strength",
    },
    {
      id: "pattern",
      labelKey: "score.pattern",
      keys: ["pattern_score"],
      tone: "pattern",
    },
    {
      id: "wuxing",
      labelKey: "score.wuxing_score",
      keys: ["wuxing_score"],
      tone: "wuxing",
    },
    {
      id: "ten_god",
      labelKey: "score.ten_god_score",
      keys: ["ten_god_score"],
      tone: "tengod",
    },
    {
      id: "useful_god",
      labelKey: "score.useful_god_score",
      keys: ["useful_god_score"],
      tone: "useful",
    },
    {
      id: "shensha",
      labelKey: "score.shensha_score",
      keys: ["shensha_score"],
      tone: "shensha",
    },
    {
      id: "luck",
      labelKey: "score.luck_score",
      keys: ["luck_score"],
      tone: "luck",
    },
  ];

  const ELEMENT_LABELS = {
    WOOD: "Mộc",
    FIRE: "Hỏa",
    EARTH: "Thổ",
    METAL: "Kim",
    WATER: "Thủy",
    Mộc: "Mộc",
    Hỏa: "Hỏa",
    Thổ: "Thổ",
    Kim: "Kim",
    Thủy: "Thủy",
    wood: "Mộc",
    fire: "Hỏa",
    earth: "Thổ",
    metal: "Kim",
    water: "Thủy",
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
    if (Array.isArray(value)) {
      var parts = value
        .map(function (v) {
          return present(v);
        })
        .filter(function (v) {
          return v !== MISSING;
        });
      return parts.length ? parts.join(", ") : MISSING;
    }
    if (typeof value === "object") {
      if (value.score != null) return present(value.score);
      if (value.value != null) return present(value.value);
      if (value.name != null) return present(value.name);
      if (value.label != null) return present(value.label);
      return MISSING;
    }
    return String(value);
  }

  /**
   * Read first present canonical key. Treats 0 as a valid score.
   */
  function pick(data, keys) {
    if (!data || typeof data !== "object") return null;
    for (var i = 0; i < keys.length; i++) {
      var key = keys[i];
      if (!Object.prototype.hasOwnProperty.call(data, key)) continue;
      var value = data[key];
      if (value === null || value === undefined) continue;
      return value;
    }
    return null;
  }

  function hasScoreField(data, key) {
    return (
      data &&
      typeof data === "object" &&
      Object.prototype.hasOwnProperty.call(data, key) &&
      data[key] !== null &&
      data[key] !== undefined
    );
  }

  function asNumber(value) {
    if (typeof value === "number" && !Number.isNaN(value)) return value;
    if (value && typeof value === "object" && typeof value.score === "number") {
      return value.score;
    }
    if (typeof value === "string" && value.trim() !== "" && !Number.isNaN(Number(value))) {
      return Number(value);
    }
    return null;
  }

  /** CSS width only — does not change displayed score text. */
  function barWidth(value) {
    var n = asNumber(value);
    if (n === null) return null;
    if (n < 0) return 0;
    if (n > 100) return 100;
    return n;
  }

  function elementClass(name) {
    var label = ELEMENT_LABELS[name] || name;
    var map = { Mộc: "wood", Hỏa: "fire", Thổ: "earth", Kim: "metal", Thủy: "water" };
    return map[label] || "unknown";
  }

  function badge(text, tone) {
    if (text === MISSING || text === null || text === undefined || text === "") {
      return '<span class="bte-badge bte-badge-muted">' + esc(MISSING) + "</span>";
    }
    return (
      '<span class="bte-badge bte-badge-' +
      esc(tone || "neutral") +
      '">' +
      esc(String(text)) +
      "</span>"
    );
  }

  function summaryCard(label, value, tone) {
    var shown = present(value);
    var width = barWidth(value);
    var meter =
      width === null
        ? ""
        : '<div class="bte-score-meter" aria-hidden="true">' +
          '<div class="bte-score-meter-fill" style="width:' +
          width +
          '%"></div></div>';
    return (
      '<article class="bte-card bte-score-summary bte-tone-' +
      esc(tone) +
      '">' +
      '<div class="bte-card-label">' +
      esc(label) +
      "</div>" +
      '<div class="bte-card-value">' +
      esc(shown) +
      "</div>" +
      meter +
      "</article>"
    );
  }

  function progressRow(label, value, elClass) {
    var shown = present(value);
    var width = barWidth(value);
    var fill =
      width === null
        ? ""
        : '<div class="bte-progress"><div class="bte-progress-fill" style="width:' +
          width +
          '%"></div></div>';
    return (
      '<div class="bte-progress-row' +
      (elClass ? " bte-el-" + esc(elClass) : "") +
      '">' +
      '<div class="bte-progress-meta">' +
      "<span>" +
      esc(label) +
      "</span>" +
      "<strong>" +
      esc(shown) +
      "</strong>" +
      "</div>" +
      fill +
      "</div>"
    );
  }

  /**
   * Element balance / count series for context only — never used as wuxing_score.
   */
  function findElementBalanceSeries(data) {
    var series = data && data.wuxing_series;
    if (!Array.isArray(series) || !series.length) return null;
    var rows = [];
    series.forEach(function (item) {
      if (!item || typeof item !== "object") return;
      var label = item.label || item.element || item.name || null;
      var value = item.value != null ? item.value : item.count;
      if (label != null && value != null) {
        rows.push({ label: String(label), value: value });
      }
    });
    return rows.length ? rows : null;
  }

  function findTenGodBalanceSeries(data) {
    var series = data && data.ten_god_series;
    if (!Array.isArray(series) || !series.length) return null;
    var rows = [];
    series.forEach(function (item) {
      if (!item || typeof item !== "object") return;
      var label = item.label || item.name || item.ten_god || item.god || null;
      var value = item.value != null ? item.value : item.count;
      if (label != null && value != null) {
        rows.push({ label: String(label), value: value });
      }
    });
    return rows.length ? rows : null;
  }

  function findStrengthValue(data) {
    if (hasScoreField(data, "strength_score")) return data.strength_score;
    return null;
  }

  function findConfidence(data) {
    // API emits string `confidence` (e.g. "medium"); accept numeric confidence_score too.
    if (hasScoreField(data, "confidence")) return data.confidence;
    if (hasScoreField(data, "confidence_score")) return data.confidence_score;
    return null;
  }

  function gaugeHtml(value) {
    var shown = present(value);
    var width = barWidth(value);
    var needle = width === null ? 0 : width;
    var deg = -90 + (needle / 100) * 180;
    return (
      '<article class="bte-card bte-score-gauge-card">' +
      '<div class="bte-card-label">' +
      esc(t("score.strength")) +
      "</div>" +
      '<div class="bte-gauge" role="img" aria-label="' +
      esc(t("score.strength_aria", { value: shown })) +
      '">' +
      '<div class="bte-gauge-arc"></div>' +
      '<div class="bte-gauge-needle" style="transform:rotate(' +
      deg +
      'deg)"></div>' +
      '<div class="bte-gauge-hub"></div>' +
      '<div class="bte-gauge-value">' +
      esc(shown) +
      "</div>" +
      "</div>" +
      "</article>"
    );
  }

  function sectionBars(title, rows, useElementColor) {
    if (!rows || !rows.length) return "";
    var body = rows
      .map(function (row) {
        var label = ELEMENT_LABELS[row.label] || row.label;
        var el = useElementColor ? elementClass(row.label) : null;
        return progressRow(label, row.value, el);
      })
      .join("");
    return (
      '<section class="bte-card bte-score-panel">' +
      "<h3>" +
      esc(title) +
      "</h3>" +
      '<div class="bte-progress-list">' +
      body +
      "</div>" +
      "</section>"
    );
  }

  function headerMeta(data) {
    var grade = present(pick(data, ["grade"]) || MISSING);
    var confidence = present(findConfidence(data) || MISSING);
    var recommendation = present(pick(data, ["recommendation"]) || MISSING);
    return (
      '<div class="bte-score-status">' +
      badge(t("score.grade", { value: grade }), "pattern") +
      badge(t("score.confidence", { value: confidence }), "follow") +
      (recommendation !== MISSING
        ? '<span class="bte-score-rec">' + esc(recommendation) + "</span>"
        : "") +
      "</div>"
    );
  }

  /**
   * @param {object|null|undefined} score
   * @returns {string} HTML
   */
  function renderScore(score) {
    try {
      var data =
        score && typeof score === "object" && !Array.isArray(score) ? score : {};

      var summary =
        '<div class="bte-card-grid bte-score-summary-grid">' +
        SUMMARY.map(function (item) {
          var raw = hasScoreField(data, item.keys[0]) ? data[item.keys[0]] : null;
          return summaryCard(t(item.labelKey), raw, item.tone);
        }).join("") +
        "</div>";

      var strengthVal = findStrengthValue(data);
      var hasStrength = strengthVal !== null && strengthVal !== undefined;
      // Balance charts are contextual counts — never substitute for *_score cards.
      var elementBalance = findElementBalanceSeries(data);
      var tenGodBalance = findTenGodBalanceSeries(data);

      var extras =
        (hasStrength ? gaugeHtml(strengthVal) : "") +
        (elementBalance
          ? sectionBars(t("score.element_balance"), elementBalance, true)
          : "") +
        (tenGodBalance
          ? sectionBars(t("score.ten_god_balance"), tenGodBalance, false)
          : "");

      return (
        '<section class="bte-score" aria-label="' +
        esc(t("score.title")) +
        '">' +
        '<header class="bte-calendar-head">' +
        "<h2>" +
        esc(t("score.title")) +
        "</h2>" +
        '<p class="bte-calendar-sub">' +
        esc(t("score.subtitle")) +
        "</p>" +
        "</header>" +
        headerMeta(data) +
        summary +
        '<div class="bte-score-extras">' +
        (extras ||
          '<p class="muted">' + esc(t("score.empty_extras")) + "</p>") +
        "</div>" +
        "</section>"
      );
    } catch (_) {
      return (
        '<section class="bte-score">' +
        '<div class="bte-card-grid bte-score-summary-grid">' +
        SUMMARY.map(function (item) {
          return summaryCard(t(item.labelKey), MISSING, item.tone);
        }).join("") +
        "</div>" +
        "</section>"
      );
    }
  }

  global.BtePresenters = global.BtePresenters || {};
  global.BtePresenters.score = renderScore;
})(window);
