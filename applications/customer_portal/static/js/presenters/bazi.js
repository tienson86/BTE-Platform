/**
 * Bazi presentation layer — primary analysis page.
 * Sections: Summary · Four Pillars · Analysis · Ten Gods · ShenSha.
 * Pattern fields are displayed here (Cách Cục tab removed). Display only.
 */
(function (global) {
  const MISSING = "--";

  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  const STEM_META = {
    Giáp: { element: "Mộc", yinYang: "Dương" },
    Ất: { element: "Mộc", yinYang: "Âm" },
    Bính: { element: "Hỏa", yinYang: "Dương" },
    Đinh: { element: "Hỏa", yinYang: "Âm" },
    Mậu: { element: "Thổ", yinYang: "Dương" },
    Kỷ: { element: "Thổ", yinYang: "Âm" },
    Canh: { element: "Kim", yinYang: "Dương" },
    Tân: { element: "Kim", yinYang: "Âm" },
    Nhâm: { element: "Thủy", yinYang: "Dương" },
    Quý: { element: "Thủy", yinYang: "Âm" },
  };

  const BRANCH_ELEMENT = {
    Tý: "Thủy",
    Sửu: "Thổ",
    Dần: "Mộc",
    Mão: "Mộc",
    Thìn: "Thổ",
    Tỵ: "Hỏa",
    Ngọ: "Hỏa",
    Mùi: "Thổ",
    Thân: "Kim",
    Dậu: "Kim",
    Tuất: "Thổ",
    Hợi: "Thủy",
  };

  const BRANCH_HIDDEN_COUNT = {
    Tý: 1,
    Sửu: 3,
    Dần: 3,
    Mão: 1,
    Thìn: 3,
    Tỵ: 3,
    Ngọ: 2,
    Mùi: 3,
    Thân: 3,
    Dậu: 1,
    Tuất: 3,
    Hợi: 2,
  };

  const PILLARS = [
    { key: "year_pillar", labelKey: "bazi.pillar_year", alt: ["year", "năm"] },
    { key: "month_pillar", labelKey: "bazi.pillar_month", alt: ["month", "tháng"] },
    { key: "day_pillar", labelKey: "bazi.pillar_day", alt: ["day", "ngày"] },
    { key: "hour_pillar", labelKey: "bazi.pillar_hour", alt: ["hour", "giờ", "time_pillar"] },
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
    "Quý Nhân",
    "Kiếp Sát",
  ];

  const ELEMENT_ORDER = [
    { key: "Mộc", en: "Wood", cls: "wood" },
    { key: "Hỏa", en: "Fire", cls: "fire" },
    { key: "Thổ", en: "Earth", cls: "earth" },
    { key: "Kim", en: "Metal", cls: "metal" },
    { key: "Thủy", en: "Water", cls: "water" },
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
    if (Array.isArray(value)) {
      const parts = value
        .map(function (v) {
          return present(v);
        })
        .filter(function (v) {
          return v !== MISSING;
        });
      return parts.length ? parts.join(", ") : MISSING;
    }
    if (typeof value === "object") {
      if (value.name != null && value.name !== "") return present(value.name);
      if (value.label != null && value.label !== "") return present(value.label);
      if (value.stem != null || value.branch != null) {
        return [present(value.stem), present(value.branch)]
          .filter(function (v) {
            return v !== MISSING;
          })
          .join(" ") || MISSING;
      }
      return MISSING;
    }
    return String(value);
  }

  function stemMeta(stem) {
    if (!stem || stem === MISSING) return { element: MISSING, yinYang: MISSING };
    if (STEM_META[stem]) return STEM_META[stem];
    const key = Object.keys(STEM_META).find(function (k) {
      return k.toLowerCase() === String(stem).toLowerCase();
    });
    return key ? STEM_META[key] : { element: MISSING, yinYang: MISSING };
  }

  function elementClass(element) {
    const map = {
      Mộc: "wood",
      Hỏa: "fire",
      Thổ: "earth",
      Kim: "metal",
      Thủy: "water",
      Wood: "wood",
      Fire: "fire",
      Earth: "earth",
      Metal: "metal",
      Water: "water",
    };
    return map[element] || "unknown";
  }

  function pickPillar(bazi, spec) {
    if (!bazi || typeof bazi !== "object") return null;
    if (bazi[spec.key] && typeof bazi[spec.key] === "object") return bazi[spec.key];
    for (var i = 0; i < spec.alt.length; i++) {
      var alt = spec.alt[i];
      if (bazi[alt] && typeof bazi[alt] === "object") return bazi[alt];
    }
    if (Array.isArray(bazi.pillars) && bazi.pillars[PILLARS.indexOf(spec)]) {
      return bazi.pillars[PILLARS.indexOf(spec)];
    }
    return null;
  }

  function pillarStem(pillar) {
    if (!pillar || typeof pillar !== "object") return MISSING;
    return present(
      pillar.stem ||
        pillar.thien_can ||
        pillar.heavenly_stem ||
        pillar.can ||
        null
    );
  }

  function pillarBranch(pillar) {
    if (!pillar || typeof pillar !== "object") return MISSING;
    return present(
      pillar.branch ||
        pillar.dia_chi ||
        pillar.earthly_branch ||
        pillar.chi ||
        null
    );
  }

  function pillarField(pillar, keys) {
    if (!pillar || typeof pillar !== "object") return null;
    for (var i = 0; i < keys.length; i++) {
      if (pillar[keys[i]] != null && pillar[keys[i]] !== "") return pillar[keys[i]];
    }
    return null;
  }

  function sliceHidden(bazi, pillars) {
    var flat = Array.isArray(bazi.hidden_stems) ? bazi.hidden_stems : null;
    if (!flat) {
      return pillars.map(function () {
        return [];
      });
    }
    var offset = 0;
    return pillars.map(function (p) {
      var branch = pillarBranch(p);
      var count = BRANCH_HIDDEN_COUNT[branch];
      if (!count) {
        var chunk = flat.slice(offset);
        offset = flat.length;
        return chunk;
      }
      var slice = flat.slice(offset, offset + count);
      offset += count;
      return slice;
    });
  }

  function tenGodAt(bazi, pillar, index) {
    var fromPillar = pillarField(pillar, [
      "ten_god",
      "ten_gods",
      "thap_than",
      "shi_shen",
    ]);
    if (fromPillar != null) return present(fromPillar);
    if (Array.isArray(bazi.ten_gods) && bazi.ten_gods[index] != null) {
      return present(bazi.ten_gods[index]);
    }
    return MISSING;
  }

  function growthAt(pillar) {
    return present(
      pillarField(pillar, [
        "truong_sinh",
        "growth",
        "chang_sheng",
        "stage",
        "twelve_stage",
      ])
    );
  }

  function nayinAt(pillar) {
    return present(
      pillarField(pillar, ["nap_am", "nayin", "na_yin", "napam"])
    );
  }

  function hiddenAt(pillar, sliced) {
    var fromPillar = pillarField(pillar, [
      "hidden_stems",
      "tang_can",
      "cang_gan",
      "hidden",
    ]);
    if (fromPillar != null) return present(fromPillar);
    return present(sliced);
  }

  function dayMaster(bazi, dayPillar) {
    var dm =
      bazi.day_master ||
      bazi.dayMaster ||
      bazi.nhat_chu ||
      null;
    if (dm != null && dm !== "") return present(dm);
    return pillarStem(dayPillar);
  }

  function dayMasterElement(bazi, dm) {
    var fromApi =
      bazi.day_master_element || bazi.dayMasterElement || bazi.element || null;
    if (fromApi != null && fromApi !== "") return present(fromApi);
    return stemMeta(dm).element;
  }

  function dayMasterYinYang(bazi, dm) {
    var fromApi =
      bazi.day_master_yin_yang || bazi.dayMasterYinYang || bazi.yin_yang || null;
    if (fromApi != null && fromApi !== "") return present(fromApi);
    return stemMeta(dm).yinYang;
  }

  function pickFrom(obj, keys) {
    if (!obj || typeof obj !== "object") return null;
    for (var i = 0; i < keys.length; i++) {
      if (obj[keys[i]] != null && obj[keys[i]] !== "") return obj[keys[i]];
    }
    return null;
  }

  function formatWithElement(name, element) {
    if (!name || name === MISSING) return MISSING;
    if (!element || element === MISSING) return name;
    return name + " (" + element + ")";
  }

  function elBadge(text, element) {
    var cls = element && element !== MISSING ? " bte-el-" + elementClass(element) : "";
    return (
      '<span class="bte-el-badge' +
      cls +
      '">' +
      esc(text) +
      "</span>"
    );
  }

  function row(label, valueHtml) {
    return (
      '<div class="bte-bazi-row">' +
      '<span class="bte-bazi-row-label">' +
      esc(label) +
      "</span>" +
      '<span class="bte-bazi-row-value">' +
      valueHtml +
      "</span>" +
      "</div>"
    );
  }

  function summaryCard(label, valueHtml, element) {
    var elCls = element && element !== MISSING ? " bte-el-" + elementClass(element) : "";
    return (
      '<article class="bte-card bte-bazi-summary' +
      elCls +
      '">' +
      '<div class="bte-card-label">' +
      esc(label) +
      "</div>" +
      '<div class="bte-card-value">' +
      valueHtml +
      "</div>" +
      "</article>"
    );
  }

  function sectionHead(title) {
    return '<h3 class="bte-section-title">' + esc(title) + "</h3>";
  }

  function resolveCanXuong(fullData) {
    var cx = null;
    if (window.BteSummaryBuilder && typeof window.BteSummaryBuilder.build === "function") {
      try {
        var model = window.BteSummaryBuilder.build(fullData || {}, {});
        cx = model && model.can_xuong;
      } catch (_) {
        cx = null;
      }
    }
    if (!cx) return { total: MISSING, poem: MISSING, stars: MISSING, grade: MISSING };
    var total = cx.total || MISSING;
    var poem = cx.poem || MISSING;
    // Optional display fields when API provides them.
    var stars = present(pickFrom(cx, ["stars", "rating", "sao", "star_rating"]));
    var grade = present(pickFrom(cx, ["grade", "cach", "level", "rank", "hang"]));
    return { total: total, poem: poem, stars: stars, grade: grade };
  }

  function canXuongHtml(cx) {
    if (cx.total === MISSING && cx.poem === MISSING && cx.stars === MISSING && cx.grade === MISSING) {
      return esc(MISSING);
    }
    var parts = [];
    if (cx.total !== MISSING) parts.push('<div class="bte-cx-total">' + esc(cx.total) + "</div>");
    if (cx.stars !== MISSING) parts.push('<div class="bte-cx-stars">' + esc(cx.stars) + "</div>");
    if (cx.grade !== MISSING) parts.push('<div class="bte-cx-grade">' + esc(cx.grade) + "</div>");
    if (cx.poem !== MISSING) parts.push('<div class="bte-cx-poem">' + esc(cx.poem) + "</div>");
    return parts.join("") || esc(MISSING);
  }

  function pillarCard(label, pillar, hidden, tenGod) {
    var stem = pillarStem(pillar);
    var branch = pillarBranch(pillar);
    var stemInfo = stemMeta(stem);
    var branchEl = BRANCH_ELEMENT[branch] || MISSING;
    var stemDisplay = formatWithElement(stem, stemInfo.element);
    var branchDisplay = formatWithElement(branch, branchEl);

    return (
      '<article class="bte-card bte-pillar-card bte-el-' +
      elementClass(stemInfo.element) +
      '">' +
      '<div class="bte-pillar-head">' +
      '<div class="bte-card-label">' +
      esc(label) +
      "</div>" +
      '<div class="bte-pillar-pair">' +
      esc(
        stem === MISSING && branch === MISSING
          ? MISSING
          : (stem === MISSING ? MISSING : stem) +
              " · " +
              (branch === MISSING ? MISSING : branch)
      ) +
      "</div>" +
      "</div>" +
      '<div class="bte-bazi-rows">' +
      row(t("bazi.stem"), elBadge(stemDisplay, stemInfo.element)) +
      row(
        t("bazi.branch"),
        elBadge(branchDisplay, branchEl === MISSING ? null : branchEl)
      ) +
      row(t("bazi.hidden"), esc(hiddenAt(pillar, hidden))) +
      row(t("bazi.ten_god"), esc(tenGod)) +
      row(t("bazi.chang_sheng"), esc(growthAt(pillar))) +
      row(t("bazi.nap_am"), esc(nayinAt(pillar))) +
      "</div>" +
      "</article>"
    );
  }

  function analysisCard(label, value) {
    return (
      '<article class="bte-card">' +
      '<div class="bte-card-label">' +
      esc(label) +
      "</div>" +
      '<div class="bte-card-value">' +
      esc(value == null || value === "" ? MISSING : String(value)) +
      "</div>" +
      "</article>"
    );
  }

  function normalizeElementLabel(label) {
    var map = {
      WOOD: "Mộc",
      FIRE: "Hỏa",
      EARTH: "Thổ",
      METAL: "Kim",
      WATER: "Thủy",
      wood: "Mộc",
      fire: "Hỏa",
      earth: "Thổ",
      metal: "Kim",
      water: "Thủy",
      Mộc: "Mộc",
      Hỏa: "Hỏa",
      Thổ: "Thổ",
      Kim: "Kim",
      Thủy: "Thủy",
      Wood: "Mộc",
      Fire: "Hỏa",
      Earth: "Thổ",
      Metal: "Kim",
      Water: "Thủy",
    };
    return map[label] || label;
  }

  function collectElementCounts(bazi, score) {
    var counts = { Mộc: 0, Hỏa: 0, Thổ: 0, Kim: 0, Thủy: 0 };
    var series = score && Array.isArray(score.wuxing_series) ? score.wuxing_series : null;
    if (series && series.length) {
      series.forEach(function (item) {
        if (!item || typeof item !== "object") return;
        var label = normalizeElementLabel(item.label || item.element || item.name || "");
        var value = item.value != null ? item.value : item.count;
        if (counts[label] != null && value != null && !Number.isNaN(Number(value))) {
          counts[label] = Number(value);
        }
      });
      return counts;
    }
    // Fallback: count stem + branch elements from pillars (display only).
    PILLARS.forEach(function (spec) {
      var pillar = pickPillar(bazi, spec);
      var stem = pillarStem(pillar);
      var branch = pillarBranch(pillar);
      var se = stemMeta(stem).element;
      var be = BRANCH_ELEMENT[branch];
      if (counts[se] != null) counts[se] += 1;
      if (counts[be] != null) counts[be] += 1;
    });
    return counts;
  }

  function elementBarsHtml(counts) {
    var max = 1;
    ELEMENT_ORDER.forEach(function (el) {
      if (counts[el.key] > max) max = counts[el.key];
    });
    return (
      '<div class="bte-el-bars">' +
      ELEMENT_ORDER.map(function (el) {
        var n = counts[el.key] || 0;
        var blocks = "";
        for (var i = 0; i < Math.max(0, Math.round(n)); i++) {
          blocks += "■";
        }
        if (!blocks) blocks = "·";
        var pct = Math.round((n / max) * 100);
        return (
          '<div class="bte-el-bar-row bte-el-' +
          el.cls +
          '">' +
          '<span class="bte-el-bar-label">' +
          esc(el.en) +
          "</span>" +
          '<span class="bte-el-bar-blocks" aria-hidden="true">' +
          esc(blocks) +
          "</span>" +
          '<div class="bte-el-bar-track"><div class="bte-el-bar-fill" style="width:' +
          pct +
          '%"></div></div>' +
          '<span class="bte-el-bar-value">' +
          esc(String(n)) +
          "</span>" +
          "</div>"
        );
      }).join("") +
      "</div>"
    );
  }

  function normalizeToken(text) {
    return String(text || "")
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/[^a-z0-9]+/g, " ")
      .trim();
  }

  function collectPresentGods(bazi, pillarObjs) {
    var present = {};
    pillarObjs.forEach(function (pillar, index) {
      var god = tenGodAt(bazi, pillar, index);
      if (god && god !== MISSING) {
        String(god)
          .split(/[,;/|]+/)
          .forEach(function (part) {
            var token = normalizeToken(part);
            if (token) present[token] = true;
          });
      }
    });
    if (Array.isArray(bazi.ten_gods)) {
      bazi.ten_gods.forEach(function (g) {
        var token = normalizeToken(g);
        if (token) present[token] = true;
      });
    }
    return present;
  }

  function collectPresentShensha(bazi) {
    var present = {};
    var unknown = false;
    var raw = pickFrom(bazi, ["shensha", "than_sat", "shen_sha", "spirits"]);
    if (raw == null) {
      return { present: present, unknown: true };
    }
    if (Array.isArray(raw)) {
      if (!raw.length) return { present: present, unknown: false };
      raw.forEach(function (item) {
        var text = presentLabel(item);
        if (text === MISSING) return;
        present[normalizeToken(text)] = true;
      });
      return { present: present, unknown: false };
    }
    if (typeof raw === "object") {
      Object.keys(raw).forEach(function (k) {
        var v = raw[k];
        if (v === true || (v != null && v !== false && v !== "")) {
          present[normalizeToken(k)] = true;
          if (typeof v === "string") present[normalizeToken(v)] = true;
        }
      });
      return { present: present, unknown: false };
    }
    var one = presentLabel(raw);
    if (one !== MISSING) present[normalizeToken(one)] = true;
    return { present: present, unknown: false };
  }

  function presentLabel(item) {
    if (item == null || item === "") return MISSING;
    if (typeof item === "string" || typeof item === "number") return String(item);
    if (typeof item === "object") {
      return present(item.name || item.label || item.title || item.id || null);
    }
    return MISSING;
  }

  function matchCatalog(catalogName, presentMap) {
    var target = normalizeToken(catalogName);
    if (presentMap[target]) return true;
    return Object.keys(presentMap).some(function (key) {
      return key.indexOf(target) >= 0 || target.indexOf(key) >= 0;
    });
  }

  function checklistHtml(items, presentMap, unknownAll) {
    return (
      '<ul class="bte-checklist">' +
      items
        .map(function (name) {
          var state = "absent";
          var mark = "✗";
          var tone = "neg";
          if (unknownAll) {
            state = "unknown";
            mark = "?";
            tone = "unk";
          } else if (matchCatalog(name, presentMap)) {
            state = "present";
            mark = "✓";
            tone = "pos";
          }
          return (
            '<li class="bte-check bte-check-' +
            tone +
            '" data-state="' +
            state +
            '">' +
            '<span class="bte-check-mark" aria-hidden="true">' +
            mark +
            "</span>" +
            '<span class="bte-check-label">' +
            esc(name) +
            "</span>" +
            "</li>"
          );
        })
        .join("") +
      "</ul>"
    );
  }

  function wrapSection(title, body, opts) {
    opts = opts || {};
    if (window.BteUI && typeof BteUI.sectionCard === "function") {
      return BteUI.sectionCard({
        title: title,
        description: opts.description || "",
        badge: opts.badge || "",
        body: body,
        collapsed: !!opts.collapsed,
      });
    }
    return sectionHead(title) + body;
  }

  /**
   * @param {object|null|undefined} bazi
   * @param {{ data?: object }} [options]
   * @returns {string} HTML
   */
  function renderBazi(bazi, options) {
    try {
      var data =
        bazi && typeof bazi === "object" && !Array.isArray(bazi) ? bazi : {};
      var full = (options && options.data) || {};
      var pattern =
        full.pattern && typeof full.pattern === "object" ? full.pattern : {};
      var score = full.score && typeof full.score === "object" ? full.score : {};
      var useful =
        full.useful_god && typeof full.useful_god === "object"
          ? full.useful_god
          : {};

      var pillarObjs = PILLARS.map(function (spec) {
        return pickPillar(data, spec);
      });
      var hiddenSlices = sliceHidden(data, pillarObjs);
      var dayPillar = pillarObjs[2];
      var dm = dayMaster(data, dayPillar);
      var dmEl = dayMasterElement(data, dm);
      var dmYy = dayMasterYinYang(data, dm);
      var cx = resolveCanXuong(full);

      var summaryBody =
        '<div class="bte-card-grid bte-bazi-summary-grid">' +
        summaryCard(t("bazi.day_master"), esc(dm), dmEl) +
        summaryCard(t("bazi.element"), esc(dmEl), dmEl) +
        summaryCard(t("bazi.yin_yang"), esc(dmYy)) +
        summaryCard(t("bazi.can_xuong"), canXuongHtml(cx)) +
        "</div>";

      var pillarsBody =
        '<div class="bte-pillar-grid">' +
        PILLARS.map(function (spec, index) {
          return pillarCard(
            t(spec.labelKey),
            pillarObjs[index],
            hiddenSlices[index],
            tenGodAt(data, pillarObjs[index], index)
          );
        }).join("") +
        "</div>";

      var strength = present(
        pickFrom(pattern, [
          "than_vuong_nhuoc",
          "strength",
          "strength_level",
          "body_strength",
          "vuong_nhuoc",
          "day_master_strength",
        ]) ||
          pickFrom(full.strength || {}, ["level", "label", "value", "status"])
      );
      var dungThan = present(
        pickFrom(pattern, ["dung_than", "useful_god", "yong_shen", "yongshen"]) ||
          pickFrom(useful, ["dung_than", "useful_god", "primary", "name", "element"])
      );
      var hyThan = present(
        pickFrom(pattern, ["hy_than", "xi_shen", "favorable_god", "xi"]) ||
          pickFrom(useful, ["hy_than", "xi_shen", "favorable"])
      );
      var elementCounts = collectElementCounts(data, score);

      var analysisBody =
        '<div class="bte-card-grid bte-bazi-analysis-grid">' +
        analysisCard(t("bazi.than_strength"), strength) +
        '<article class="bte-card bte-el-dist-card">' +
        '<div class="bte-card-label">' +
        esc(t("bazi.element_dist")) +
        "</div>" +
        elementBarsHtml(elementCounts) +
        "</article>" +
        analysisCard(t("bazi.dung_than"), dungThan) +
        analysisCard(t("bazi.hy_than"), hyThan) +
        "</div>";

      var godsPresent = collectPresentGods(data, pillarObjs);
      var shenshaState = collectPresentShensha(data);

      var tenGodsBody =
        '<div class="bte-checklist-card">' +
        checklistHtml(TEN_GOD_CATALOG, godsPresent, false) +
        "</div>";

      var shenshaBody =
        '<div class="bte-checklist-card">' +
        checklistHtml(SHENSHA_CATALOG, shenshaState.present, shenshaState.unknown) +
        "</div>";

      return (
        '<section class="bte-bazi" aria-label="' +
        esc(t("bazi.title")) +
        '">' +
        '<header class="bte-calendar-head">' +
        "<h2>" +
        esc(t("bazi.title")) +
        "</h2>" +
        '<p class="bte-calendar-sub">' +
        esc(t("bazi.subtitle")) +
        "</p>" +
        "</header>" +
        wrapSection(t("bazi.section_summary"), summaryBody) +
        wrapSection(t("bazi.section_pillars"), pillarsBody) +
        wrapSection(t("bazi.section_analysis"), analysisBody) +
        wrapSection(t("bazi.section_ten_gods"), tenGodsBody, { collapsed: true }) +
        wrapSection(t("bazi.section_shensha"), shenshaBody, { collapsed: true }) +
        "</section>"
      );
    } catch (_) {
      return (
        '<section class="bte-bazi">' +
        '<div class="bte-card-grid">' +
        summaryCard(t("bazi.day_master"), esc(MISSING)) +
        summaryCard(t("bazi.element"), esc(MISSING)) +
        summaryCard(t("bazi.yin_yang"), esc(MISSING)) +
        summaryCard(t("bazi.can_xuong"), esc(MISSING)) +
        "</div>" +
        "</section>"
      );
    }
  }

  global.BtePresenters = global.BtePresenters || {};
  global.BtePresenters.bazi = renderBazi;
})(window);
