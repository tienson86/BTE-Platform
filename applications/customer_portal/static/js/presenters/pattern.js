/**
 * Pattern presentation layer (Sprint 3).
 * Renders pattern JSON as a dashboard — no business logic / no Engine calls.
 */
(function (global) {
  const MISSING = "--";

  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  /** Display labels for known pattern codes (presentation only). */
  const PATTERN_LABELS = {
    chinh_quan: "Chính Quan",
    thien_quan: "Thiên Quan",
    thien_tai: "Thiên Tài",
    chinh_tai: "Chính Tài",
    thien_an: "Thiên Ấn",
    chinh_an: "Chính Ấn",
    thien_thuong: "Thiên Thương",
    thuc_than: "Thực Thần",
    thuong_quan: "Thương Quan",
    thien_sat: "Thiên Sát",
    that_sat: "Thất Sát",
    kien_loc: "Kiến Lộc",
    duong_nhan: "Dương Nhẫn",
    ty_kien: "Tỷ Kiên",
    kiep_tai: "Kiếp Tài",
  };

  const FIELDS = [
    {
      id: "than",
      label: "Thân",
      keys: ["than", "body", "day_master_body", "than_chu", "body_element"],
      tone: "neutral",
      icon: "person",
    },
    {
      id: "than_strength",
      label: "Thân vượng/nhược",
      keys: [
        "than_vuong_nhuoc",
        "strength",
        "strength_level",
        "body_strength",
        "vuong_nhuoc",
        "day_master_strength",
      ],
      tone: "strength",
      icon: "gauge",
    },
    {
      id: "cach_cuc",
      label: "Cách cục",
      keys: ["cach_cuc", "pattern", "pattern_name", "ju", "ge_ju", "main_pattern"],
      tone: "pattern",
      icon: "hex",
    },
    {
      id: "tong_cach",
      label: "Tòng cách",
      keys: ["tong_cach", "follow_pattern", "cong_ge", "from_pattern", "follower"],
      tone: "follow",
      icon: "flow",
    },
    {
      id: "dung_than",
      label: "Dụng thần",
      keys: ["dung_than", "useful_god", "yong_shen", "yongshen"],
      tone: "useful",
      icon: "star",
    },
    {
      id: "hy_than",
      label: "Hỷ thần",
      keys: ["hy_than", "xi_shen", "favorable_god", "xi_shen_list", "xi"],
      tone: "favor",
      icon: "heart",
    },
    {
      id: "ky_than",
      label: "Kỵ thần",
      keys: ["ky_than", "ji_shen", "unfavorable_god", "ji", "avoid_god"],
      tone: "avoid",
      icon: "alert",
    },
    {
      id: "dieu_hau",
      label: "Điều hậu",
      keys: ["dieu_hau", "climate", "tiao_hou", "tiaohou", "season_adjust"],
      tone: "climate",
      icon: "sun",
    },
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
      if (value.name != null && value.name !== "") return formatPatternName(value.name);
      if (value.label != null && value.label !== "") return present(value.label);
      if (value.value != null && value.value !== "") return present(value.value);
      if (value.level != null && value.level !== "") return present(value.level);
      return MISSING;
    }
    return String(value);
  }

  function formatPatternName(raw) {
    var text = present(raw);
    if (text === MISSING) return MISSING;
    var key = String(raw).trim().toLowerCase().replace(/\s+/g, "_");
    if (PATTERN_LABELS[key]) return PATTERN_LABELS[key];
    if (PATTERN_LABELS[String(raw)]) return PATTERN_LABELS[String(raw)];
    if (/^[a-z0-9_]+$/i.test(String(raw))) {
      return String(raw)
        .split(/[_\s]+/)
        .filter(Boolean)
        .map(function (w) {
          return w.charAt(0).toUpperCase() + w.slice(1);
        })
        .join(" ");
    }
    return text;
  }

  function pick(data, keys) {
    if (!data || typeof data !== "object") return null;
    for (var i = 0; i < keys.length; i++) {
      var key = keys[i];
      if (data[key] != null && data[key] !== "") return data[key];
    }
    if (data.gods && typeof data.gods === "object") {
      for (var j = 0; j < keys.length; j++) {
        if (data.gods[keys[j]] != null && data.gods[keys[j]] !== "") {
          return data.gods[keys[j]];
        }
      }
    }
    if (data.useful && typeof data.useful === "object") {
      for (var k = 0; k < keys.length; k++) {
        if (data.useful[keys[k]] != null && data.useful[keys[k]] !== "") {
          return data.useful[keys[k]];
        }
      }
    }
    return null;
  }

  function strengthTone(value) {
    var s = String(value || "").toLowerCase();
    if (!s || s === MISSING.toLowerCase()) return "neutral";
    if (
      s.indexOf("vượng") >= 0 ||
      s.indexOf("vuong") >= 0 ||
      s.indexOf("strong") >= 0 ||
      s.indexOf("旺") >= 0
    ) {
      return "strong";
    }
    if (
      s.indexOf("nhược") >= 0 ||
      s.indexOf("nhuoc") >= 0 ||
      s.indexOf("weak") >= 0 ||
      s.indexOf("弱") >= 0
    ) {
      return "weak";
    }
    if (s.indexOf("hòa") >= 0 || s.indexOf("hoa") >= 0 || s.indexOf("balance") >= 0) {
      return "balanced";
    }
    return "neutral";
  }

  function iconSvg(kind) {
    var common =
      'class="bte-pattern-icon-svg" viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"';
    switch (kind) {
      case "person":
        return (
          "<svg " +
          common +
          '><circle cx="12" cy="8" r="3.2"/><path d="M5.5 19c1.8-3.2 4-4.8 6.5-4.8S16.7 15.8 18.5 19"/></svg>'
        );
      case "gauge":
        return (
          "<svg " +
          common +
          '><path d="M5 16a7 7 0 1 1 14 0"/><path d="M12 16l4-5"/></svg>'
        );
      case "hex":
        return (
          "<svg " +
          common +
          '><path d="M12 3l7 4v6l-7 4-7-4V7l7-4z"/></svg>'
        );
      case "flow":
        return (
          "<svg " +
          common +
          '><path d="M5 8h10a3 3 0 1 0 0-6"/><path d="M19 16H9a3 3 0 1 0 0 6"/><path d="M5 8l3 3-3 3"/><path d="M19 16l-3-3 3-3"/></svg>'
        );
      case "star":
        return (
          "<svg " +
          common +
          '><path d="M12 3.5l2.2 4.5 5 .7-3.6 3.5.9 5L12 15.8 7.5 17.2l.9-5L4.8 8.7l5-.7L12 3.5z"/></svg>'
        );
      case "heart":
        return (
          "<svg " +
          common +
          '><path d="M12 19s-6.5-4.1-8.2-7.2C2.3 9.4 3.6 6.8 6.3 6.5c1.6-.2 3 .6 3.7 1.8.7-1.2 2.1-2 3.7-1.8 2.7.3 4 2.9 2.5 5.3C18.5 14.9 12 19 12 19z"/></svg>'
        );
      case "alert":
        return (
          "<svg " +
          common +
          '><path d="M12 4l9 16H3L12 4z"/><path d="M12 10v4"/><path d="M12 17h.01"/></svg>'
        );
      case "sun":
        return (
          "<svg " +
          common +
          '><circle cx="12" cy="12" r="3.5"/><path d="M12 3v2.2M12 18.8V21M3 12h2.2M18.8 12H21M5.6 5.6l1.6 1.6M16.8 16.8l1.6 1.6M18.4 5.6l-1.6 1.6M7.2 16.8l-1.6 1.6"/></svg>'
        );
      default:
        return "<svg " + common + '><circle cx="12" cy="12" r="7"/></svg>';
    }
  }

  function badge(text, tone) {
    if (!text || text === MISSING) {
      return '<span class="bte-badge bte-badge-muted">' + esc(MISSING) + "</span>";
    }
    return (
      '<span class="bte-badge bte-badge-' +
      esc(tone || "neutral") +
      '">' +
      esc(text) +
      "</span>"
    );
  }

  function resolveValue(data, field) {
    var raw = pick(data, field.keys);
    if (field.id === "cach_cuc") {
      if (raw == null) raw = data.pattern;
      return formatPatternName(raw);
    }
    return present(raw);
  }

  function cardTone(field, value) {
    if (field.tone === "strength") return strengthTone(value);
    return field.tone || "neutral";
  }

  function dashCard(field) {
    return dashCardWith(field, MISSING, "neutral");
  }

  function dashCardWith(field, value, tone) {
    return (
      '<article class="bte-card bte-pattern-card bte-tone-' +
      esc(tone) +
      '">' +
      '<div class="bte-pattern-card-top">' +
      '<div class="bte-pattern-icon" aria-hidden="true">' +
      iconSvg(field.icon) +
      "</div>" +
      badge(toneLabel(tone, value), tone) +
      "</div>" +
      '<div class="bte-card-label">' +
      esc(field.label) +
      "</div>" +
      '<div class="bte-card-value">' +
      esc(value) +
      "</div>" +
      "</article>"
    );
  }

  function toneLabel(tone, value) {
    if (value === MISSING) return t("pattern.na");
    if (tone === "strong") return "Vượng";
    if (tone === "weak") return "Nhược";
    if (tone === "balanced") return "Hòa";
    if (tone === "useful") return "Dụng";
    if (tone === "favor") return "Hỷ";
    if (tone === "avoid") return "Kỵ";
    if (tone === "climate") return "Hậu";
    if (tone === "pattern") return "Cách";
    if (tone === "follow") return "Tòng";
    if (tone === "neutral") return "Thân";
    return t("pattern.info");
  }

  function statusBar(data) {
    var score =
      data.score != null && data.score !== "" ? present(data.score) : MISSING;
    var priority =
      data.priority != null && data.priority !== ""
        ? present(data.priority)
        : MISSING;
    var okDisplay =
      data.success === true
        ? t("pattern.status_ok")
        : data.success === false
          ? t("pattern.status_fail")
          : MISSING;
    return (
      '<div class="bte-pattern-status">' +
      '<span class="bte-badge bte-badge-' +
      (data.success === true ? "strong" : data.success === false ? "avoid" : "muted") +
      '">' +
      esc(okDisplay) +
      "</span>" +
      '<span class="bte-badge bte-badge-pattern">' +
      esc(t("pattern.score", { value: score })) +
      "</span>" +
      '<span class="bte-badge bte-badge-follow">' +
      esc(t("pattern.priority", { value: priority })) +
      "</span>" +
      "</div>"
    );
  }

  /**
   * @param {object|null|undefined} pattern
   * @returns {string} HTML
   */
  function renderPattern(pattern) {
    try {
      var data =
        pattern && typeof pattern === "object" && !Array.isArray(pattern)
          ? pattern
          : {};

      var cards = FIELDS.map(function (field) {
        var value = resolveValue(data, field);
        var tone = cardTone(field, value);
        return dashCardWith(field, value, tone);
      }).join("");

      return (
        '<section class="bte-pattern" aria-label="' + esc(t("pattern.title")) + '">' +
        '<header class="bte-calendar-head">' +
        "<h2>" + esc(t("pattern.title")) + "</h2>" +
        '<p class="bte-calendar-sub">Cách cục · Thân · Thần sát dụng</p>' +
        "</header>" +
        statusBar(data) +
        '<div class="bte-card-grid bte-pattern-grid">' +
        cards +
        "</div>" +
        "</section>"
      );
    } catch (_) {
      return (
        '<section class="bte-pattern">' +
        '<div class="bte-card-grid bte-pattern-grid">' +
        FIELDS.map(function (field) {
          return dashCard(field);
        }).join("") +
        "</div>" +
        "</section>"
      );
    }
  }

  global.BtePresenters = global.BtePresenters || {};
  global.BtePresenters.pattern = renderPattern;
})(window);
