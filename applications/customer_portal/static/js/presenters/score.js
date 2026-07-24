/**
 * Score presentation layer (Sprint 4).
 * Renders score JSON as a dashboard — display only, no extra scoring math.
 */
(function (global) {
  const MISSING = "--";

  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  const SUMMARY = [
    {
      id: "overall",
      labelKey: "score.overall",
      keys: ["total_score", "overall_score", "overall", "final_score", "score"],
      tone: "overall",
    },
    {
      id: "than",
      labelKey: "score.than",
      keys: ["strength_score", "than_score", "body_score", "strength"],
      tone: "strength",
    },
    {
      id: "pattern",
      labelKey: "score.pattern",
      keys: ["pattern_score", "cach_cuc_score", "pattern"],
      tone: "pattern",
    },
    {
      id: "interpretation",
      labelKey: "score.interpretation",
      keys: [
        "interpretation_score",
        "interp_score",
        "luan_giai_score",
        "interpretation",
      ],
      tone: "interp",
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

  function pick(data, keys) {
    if (!data || typeof data !== "object") return null;
    for (var i = 0; i < keys.length; i++) {
      var key = keys[i];
      if (Object.prototype.hasOwnProperty.call(data, key) && data[key] != null) {
        return data[key];
      }
    }
    return null;
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
   * Collect {label, value} rows from API structures only.
   * Returns null if no suitable series exists.
   */
  function extractNamedScores(source) {
    if (!source) return null;
    var rows = [];

    if (Array.isArray(source)) {
      source.forEach(function (item) {
        if (!item || typeof item !== "object") return;
        var label =
          item.element ||
          item.name ||
          item.label ||
          item.god ||
          item.ten_god ||
          item.id ||
          null;
        var value =
          item.score != null
            ? item.score
            : item.value != null
              ? item.value
              : item.weighted_score != null
                ? item.weighted_score
                : null;
        if (label != null && value != null) {
          rows.push({ label: String(label), value: value });
        }
      });
      return rows.length ? rows : null;
    }

    if (typeof source === "object") {
      var keys = Object.keys(source);
      keys.forEach(function (key) {
        var val = source[key];
        var num = asNumber(val);
        if (num !== null) {
          rows.push({ label: key, value: num });
        } else if (val && typeof val === "object" && asNumber(val.score) !== null) {
          rows.push({ label: key, value: val.score });
        }
      });
      return rows.length ? rows : null;
    }

    return null;
  }

  function findWuxingSeries(data) {
    var direct = pick(data, [
      "ngu_hanh",
      "wuxing",
      "five_elements",
      "elements",
      "element_scores",
      "wuxing_scores",
    ]);
    var fromDirect = extractNamedScores(direct);
    if (fromDirect) return fromDirect;

    var details = data.details && data.details.wuxing;
    if (details) {
      var fromDetails = extractNamedScores(details.details);
      if (fromDetails) return fromDetails;
      var fromMeta = extractNamedScores(details.metadata);
      if (fromMeta) return fromMeta;
      var fromRules = extractNamedScores(details.matched_rules);
      if (fromRules) return fromRules;
      if (details.score != null || details.weighted_score != null) {
        return [
          {
            label: details.dimension || "Ngũ hành",
            value: details.score != null ? details.score : details.weighted_score,
          },
        ];
      }
    }

    if (Object.prototype.hasOwnProperty.call(data, "wuxing_score")) {
      return [{ label: "Ngũ hành", value: data.wuxing_score }];
    }
    return null;
  }

  function findTenGodSeries(data) {
    var direct = pick(data, [
      "thap_than",
      "ten_gods",
      "ten_god_scores",
      "shi_shen",
      "gods",
    ]);
    var fromDirect = extractNamedScores(direct);
    if (fromDirect) return fromDirect;

    var details = data.details && data.details.ten_gods;
    if (details) {
      var fromDetails = extractNamedScores(details.details);
      if (fromDetails) return fromDetails;
      var fromMeta = extractNamedScores(details.metadata);
      if (fromMeta) return fromMeta;
      var fromRules = extractNamedScores(details.matched_rules);
      if (fromRules) return fromRules;
      if (details.score != null || details.weighted_score != null) {
        return [
          {
            label: details.dimension || "Thập thần",
            value: details.score != null ? details.score : details.weighted_score,
          },
        ];
      }
    }

    if (Object.prototype.hasOwnProperty.call(data, "ten_god_score")) {
      return [{ label: "Thập thần", value: data.ten_god_score }];
    }
    return null;
  }

  function findPriority(data) {
    var top = pick(data, ["priority", "priority_level", "rank_priority"]);
    if (top != null && top !== "") return present(top);
    var finalDetails =
      data.details &&
      data.details.final_score &&
      data.details.final_score.details;
    if (finalDetails && finalDetails.priority != null) {
      return present(finalDetails.priority);
    }
    return MISSING;
  }

  function findStrengthValue(data) {
    if (Object.prototype.hasOwnProperty.call(data, "strength_score")) {
      return data.strength_score;
    }
    var strength = data.details && data.details.strength;
    if (strength && strength.score != null) return strength.score;
    var picked = pick(data, ["strength", "than_score", "body_strength"]);
    return picked;
  }

  function gaugeHtml(value) {
    var shown = present(value);
    var n = asNumber(value);
    var width = barWidth(value);
    var needle = width === null ? 0 : width;
    // Map 0..100 score to ~-90..+90 degrees for needle — display only.
    var deg = -90 + (needle / 100) * 180;
    return (
      '<article class="bte-card bte-score-gauge-card">' +
      '<div class="bte-card-label">' + esc(t("score.strength")) + "</div>" +
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
    var confidence = present(pick(data, ["confidence"]) || MISSING);
    var recommendation = present(pick(data, ["recommendation"]) || MISSING);
    var priority = findPriority(data);
    return (
      '<div class="bte-score-status">' +
      badge(t("score.grade", { value: grade }), "pattern") +
      badge(t("score.confidence", { value: confidence }), "follow") +
      badge(t("score.priority", { value: priority }), priority === MISSING ? "muted" : "useful") +
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
          var raw = pick(data, item.keys);
          // Avoid treating nested module objects as the score value.
          if (raw && typeof raw === "object" && raw.score == null && asNumber(raw) === null) {
            raw = null;
          }
          return summaryCard(t(item.labelKey), raw, item.tone);
        }).join("") +
        "</div>";

      var wuxing = findWuxingSeries(data);
      var tenGods = findTenGodSeries(data);
      var strengthVal = findStrengthValue(data);
      var hasStrength = strengthVal !== null && strengthVal !== undefined;

      var extras =
        (wuxing ? sectionBars(t("score.wuxing"), wuxing, true) : "") +
        (tenGods ? sectionBars(t("score.ten_god"), tenGods, false) : "") +
        (hasStrength ? gaugeHtml(strengthVal) : "");

      return (
        '<section class="bte-score" aria-label="' + esc(t("score.title")) + '">' +
        '<header class="bte-calendar-head">' +
        "<h2>" + esc(t("score.title")) + "</h2>" +
        '<p class="bte-calendar-sub">' + esc(t("score.subtitle")) + "</p>" +
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
