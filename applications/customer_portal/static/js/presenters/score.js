/**
 * Score presentation — Executive Summary (Đánh Giá).
 * Display-only redesign; keeps existing score fields / calculations.
 */
(function (global) {
  const MISSING = "--";

  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  /** Category cards — bind existing scores where available; placeholders otherwise. */
  const CATEGORIES = [
    { id: "than", labelKey: "score.cat_than", keys: ["strength_score"] },
    { id: "pattern", labelKey: "score.cat_pattern", keys: ["pattern_score"] },
    { id: "wealth", labelKey: "score.cat_wealth", keys: ["wealth_score", "tai_van_score"] },
    { id: "official", labelKey: "score.cat_official", keys: ["official_score", "quan_van_score"] },
    { id: "fame", labelKey: "score.cat_fame", keys: ["fame_score", "danh_tieng_score"] },
    { id: "leadership", labelKey: "score.cat_leadership", keys: ["leadership_score", "lanh_dao_score"] },
    { id: "marriage", labelKey: "score.cat_marriage", keys: ["marriage_score", "hon_nhan_score"] },
    { id: "health", labelKey: "score.cat_health", keys: ["health_score", "suc_khoe_score"] },
    { id: "luck", labelKey: "score.cat_luck", keys: ["luck_score"] },
  ];

  const TEN_GOD_CATALOG = [
    "Chính Quan",
    "Thất Sát",
    "Chính Tài",
    "Thiên Tài",
    "Chính Ấn",
    "Thiên Ấn",
    "Thực Thần",
    "Thương Quan",
    "Tỷ Kiên",
    "Kiếp Tài",
  ];

  const SHENSHA_CATALOG = [
    "Hoa Cái",
    "Thiên Ất",
    "Văn Xương",
    "Quốc Ấn",
    "Dịch Mã",
    "Cô Thần",
    "Quả Tú",
    "Thiên Đức",
    "Nguyệt Đức",
    "Hồng Loan",
    "Đào Hoa",
  ];

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

  function hasField(data, key) {
    return (
      data &&
      typeof data === "object" &&
      Object.prototype.hasOwnProperty.call(data, key) &&
      data[key] !== null &&
      data[key] !== undefined
    );
  }

  function pick(data, keys) {
    if (!data || typeof data !== "object") return null;
    for (var i = 0; i < keys.length; i++) {
      if (hasField(data, keys[i])) return data[keys[i]];
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

  function formatOutOfTen(total) {
    var n = asNumber(total);
    if (n === null) return MISSING;
    // Existing total_score is typically 0–100; present as /10 without changing math.
    var outOfTen = n <= 10 ? n : Math.round((n / 10) * 10) / 10;
    return Number(outOfTen).toFixed(1) + " / 10";
  }

  function normalizeToken(text) {
    return String(text || "")
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/[^a-z0-9]+/g, " ")
      .trim();
  }

  function collectGods(bazi) {
    var map = {};
    if (!bazi || typeof bazi !== "object") return map;
    var pillars = [
      bazi.year_pillar,
      bazi.month_pillar,
      bazi.day_pillar,
      bazi.hour_pillar,
    ];
    pillars.forEach(function (p) {
      if (!p || typeof p !== "object") return;
      var g = p.ten_god || p.ten_gods || p.thap_than;
      if (g == null) return;
      String(g)
        .split(/[,;/|]+/)
        .forEach(function (part) {
          var token = normalizeToken(part);
          if (token) map[token] = true;
        });
    });
    if (Array.isArray(bazi.ten_gods)) {
      bazi.ten_gods.forEach(function (g) {
        var token = normalizeToken(g);
        if (token) map[token] = true;
      });
    }
    return map;
  }

  function collectShensha(bazi) {
    var map = {};
    var unknown = true;
    if (!bazi || typeof bazi !== "object") return { map: map, unknown: true };
    var raw = bazi.shensha || bazi.than_sat || bazi.shen_sha;
    if (raw == null) return { map: map, unknown: true };
    unknown = false;
    if (Array.isArray(raw)) {
      raw.forEach(function (item) {
        var text =
          typeof item === "object"
            ? item.name || item.label || item.title || ""
            : item;
        var token = normalizeToken(text);
        if (token) map[token] = true;
      });
      return { map: map, unknown: false };
    }
    if (typeof raw === "object") {
      Object.keys(raw).forEach(function (k) {
        if (raw[k]) map[normalizeToken(k)] = true;
      });
      return { map: map, unknown: false };
    }
    map[normalizeToken(raw)] = true;
    return { map: map, unknown: unknown };
  }

  function matchCatalog(name, map) {
    var target = normalizeToken(name);
    if (map[target]) return true;
    return Object.keys(map).some(function (key) {
      return key.indexOf(target) >= 0 || target.indexOf(key) >= 0;
    });
  }

  function sectionHead(title) {
    return '<h3 class="bte-section-title">' + esc(title) + "</h3>";
  }

  function overallBlock(data) {
    var grade = present(pick(data, ["grade"]) || MISSING);
    var total = pick(data, ["total_score"]);
    var outOfTen = formatOutOfTen(total);
    return (
      '<section class="bte-exec-overall bte-card">' +
      '<div class="bte-card-label">' +
      esc(t("score.overall_title")) +
      "</div>" +
      '<div class="bte-overall-grade">' +
      esc(grade) +
      "</div>" +
      '<div class="bte-overall-score">' +
      esc(outOfTen) +
      "</div>" +
      (hasField(data, "total_score")
        ? '<div class="bte-overall-raw muted">' +
          esc(t("score.raw_total", { value: present(total) })) +
          "</div>"
        : "") +
      "</section>"
    );
  }

  function categoryCards(data) {
    return (
      '<div class="bte-card-grid bte-score-category-grid">' +
      CATEGORIES.map(function (cat) {
        var raw = pick(data, cat.keys);
        var shown = present(raw);
        var n = asNumber(raw);
        var meter =
          n === null
            ? ""
            : '<div class="bte-score-meter" aria-hidden="true"><div class="bte-score-meter-fill" style="width:' +
              Math.max(0, Math.min(100, n > 10 && n <= 100 ? n : n <= 10 ? n * 10 : n)) +
              '%"></div></div>';
        return (
          '<article class="bte-card bte-score-summary">' +
          '<div class="bte-card-label">' +
          esc(t(cat.labelKey)) +
          "</div>" +
          '<div class="bte-card-value">' +
          esc(shown) +
          "</div>" +
          meter +
          "</article>"
        );
      }).join("") +
      "</div>"
    );
  }

  function summaryChecklist(gods, shensha) {
    var rows = [];
    TEN_GOD_CATALOG.forEach(function (name) {
      var ok = matchCatalog(name, gods);
      rows.push({ name: name, state: ok ? "yes" : "no" });
    });
    SHENSHA_CATALOG.forEach(function (name) {
      var state = "unknown";
      if (!shensha.unknown) {
        state = matchCatalog(name, shensha.map) ? "yes" : "no";
      }
      rows.push({ name: name, state: state });
    });
    return (
      '<ul class="bte-checklist bte-checklist-compact">' +
      rows
        .map(function (row) {
          var mark = row.state === "yes" ? "✓" : row.state === "no" ? "✗" : "?";
          var label =
            row.state === "yes"
              ? t("score.has_yes")
              : row.state === "no"
                ? t("score.has_no")
                : t("score.has_unknown");
          var tone =
            row.state === "yes" ? "pos" : row.state === "no" ? "neg" : "unk";
          return (
            '<li class="bte-check bte-check-' +
            tone +
            '">' +
            '<span class="bte-check-label">' +
            esc(row.name) +
            "</span>" +
            '<span class="bte-check-mark">' +
            mark +
            " " +
            esc(label) +
            "</span>" +
            "</li>"
          );
        })
        .join("") +
      "</ul>"
    );
  }

  function bulletList(items, emptyKey) {
    if (!items || !items.length) {
      return '<p class="muted">' + esc(t(emptyKey)) + "</p>";
    }
    return (
      "<ul class=\"bte-bullet-list\">" +
      items
        .map(function (item) {
          return "<li>" + esc(String(item)) + "</li>";
        })
        .join("") +
      "</ul>"
    );
  }

  function extractList(source, keys) {
    if (!source || typeof source !== "object") return [];
    for (var i = 0; i < keys.length; i++) {
      var val = source[keys[i]];
      if (Array.isArray(val) && val.length) {
        return val
          .map(function (v) {
            if (v == null) return null;
            if (typeof v === "string" || typeof v === "number") return String(v);
            if (typeof v === "object") {
              return v.text || v.body || v.content || v.summary || v.name || null;
            }
            return null;
          })
          .filter(Boolean);
      }
      if (typeof val === "string" && val.trim()) {
        return val
          .split(/\n+|;\s*|•\s*/)
          .map(function (s) {
            return s.trim();
          })
          .filter(Boolean);
      }
    }
    return [];
  }

  function extractFromInterpretation(interp, ids) {
    var out = [];
    if (!interp || typeof interp !== "object") return out;
    var sections = Array.isArray(interp.sections) ? interp.sections : [];
    sections.forEach(function (sec) {
      if (!sec || typeof sec !== "object") return;
      var id = String(sec.id || "").toLowerCase();
      var title = String(sec.title || "").toLowerCase();
      var hit = ids.some(function (want) {
        return id.indexOf(want) >= 0 || title.indexOf(want) >= 0;
      });
      if (!hit) return;
      var body = sec.body || sec.text || sec.content;
      if (!body) return;
      String(body)
        .split(/\n+|;\s*|•\s*|\d+\.\s+/)
        .map(function (s) {
          return s.trim();
        })
        .filter(function (s) {
          return s.length > 2;
        })
        .forEach(function (s) {
          out.push(s);
        });
    });
    return out;
  }

  /**
   * @param {object|null|undefined} score
   * @param {{ data?: object }} [options]
   * @returns {string} HTML
   */
  function renderScore(score, options) {
    try {
      var data =
        score && typeof score === "object" && !Array.isArray(score) ? score : {};
      var full = (options && options.data) || {};
      var bazi = full.bazi && typeof full.bazi === "object" ? full.bazi : {};
      var interp =
        full.interpretation && typeof full.interpretation === "object"
          ? full.interpretation
          : {};

      var gods = collectGods(bazi);
      var shensha = collectShensha(bazi);

      var strengths = extractList(data, ["strengths", "uu_diem", "pros"]);
      if (!strengths.length) {
        strengths = extractFromInterpretation(interp, ["strength", "ưu", "uu"]);
      }
      var weaknesses = extractList(data, [
        "weaknesses",
        "nhuoc_diem",
        "cons",
        "warnings",
      ]);
      if (!weaknesses.length) {
        weaknesses = extractFromInterpretation(interp, [
          "weakness",
          "nhược",
          "nhuoc",
          "warning",
        ]);
      }
      var recommendations = extractList(data, ["recommendations", "suggestions"]);
      if (!recommendations.length && data.recommendation) {
        recommendations = String(data.recommendation)
          .split(/\n+|;\s*/)
          .map(function (s) {
            return s.trim();
          })
          .filter(Boolean);
      }
      if (!recommendations.length) {
        recommendations = extractFromInterpretation(interp, [
          "recommend",
          "khuyến",
          "khuyen",
          "conclusion",
        ]);
      }

      return (
        '<section class="bte-score bte-exec-summary" aria-label="' +
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
        sectionHead(t("score.section_overall")) +
        overallBlock(data) +
        sectionHead(t("score.section_categories")) +
        categoryCards(data) +
        sectionHead(t("score.section_checklist")) +
        '<div class="bte-card bte-checklist-card">' +
        summaryChecklist(gods, shensha) +
        "</div>" +
        sectionHead(t("score.section_strengths")) +
        '<div class="bte-card">' +
        bulletList(strengths, "score.empty_strengths") +
        "</div>" +
        sectionHead(t("score.section_weaknesses")) +
        '<div class="bte-card">' +
        bulletList(weaknesses, "score.empty_weaknesses") +
        "</div>" +
        sectionHead(t("score.section_recommendations")) +
        '<div class="bte-card">' +
        bulletList(recommendations, "score.empty_recommendations") +
        "</div>" +
        "</section>"
      );
    } catch (_) {
      return (
        '<section class="bte-score">' +
        '<div class="bte-card"><div class="bte-card-value">' +
        esc(MISSING) +
        "</div></div>" +
        "</section>"
      );
    }
  }

  global.BtePresenters = global.BtePresenters || {};
  global.BtePresenters.score = renderScore;
})(window);
