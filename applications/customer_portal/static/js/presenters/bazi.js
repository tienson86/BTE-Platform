/**
 * Bazi presentation layer (Sprint 2).
 * Renders bazi JSON into pillar cards — no business logic / no Engine calls.
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

  /** Display-only: how flat hidden_stems are grouped per branch in API JSON. */
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
    { key: "year_pillar", label: "Năm", alt: ["year", "năm"] },
    { key: "month_pillar", label: "Tháng", alt: ["month", "tháng"] },
    { key: "day_pillar", label: "Ngày", alt: ["day", "ngày"] },
    { key: "hour_pillar", label: "Giờ", alt: ["hour", "giờ", "time_pillar"] },
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
    if (!flat) return pillars.map(function () {
      return [];
    });
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
    var stem = pillarStem(dayPillar);
    return stem;
  }

  function row(label, value, element) {
    var cls = element ? ' bte-el-' + elementClass(element) : "";
    return (
      '<div class="bte-bazi-row">' +
      '<span class="bte-bazi-row-label">' +
      esc(label) +
      "</span>" +
      '<span class="bte-bazi-row-value' +
      cls +
      '">' +
      esc(value) +
      "</span>" +
      "</div>"
    );
  }

  function summaryCard(label, value, element) {
    var elCls = element ? " bte-el-" + elementClass(element) : "";
    return (
      '<article class="bte-card bte-bazi-summary' +
      elCls +
      '">' +
      '<div class="bte-card-label">' +
      esc(label) +
      "</div>" +
      '<div class="bte-card-value">' +
      esc(value) +
      "</div>" +
      "</article>"
    );
  }

  function pillarCard(label, pillar, hidden, tenGod) {
    var stem = pillarStem(pillar);
    var branch = pillarBranch(pillar);
    var stemInfo = stemMeta(stem);
    var branchEl = BRANCH_ELEMENT[branch] || MISSING;
    var titlePair =
      stem === MISSING && branch === MISSING
        ? MISSING
        : (stem === MISSING ? MISSING : stem) +
          " · " +
          (branch === MISSING ? MISSING : branch);

    return (
      '<article class="bte-card bte-pillar-card bte-el-' +
      elementClass(stemInfo.element) +
      '">' +
      '<div class="bte-pillar-head">' +
      '<div class="bte-card-label">' +
      esc(label) +
      "</div>" +
      '<div class="bte-pillar-pair">' +
      esc(titlePair) +
      "</div>" +
      "</div>" +
      '<div class="bte-bazi-rows">' +
      row("Thiên Can", stem, stemInfo.element) +
      row("Địa Chi", branch, branchEl === MISSING ? null : branchEl) +
      row("Tàng Can", hiddenAt(pillar, hidden)) +
      row("Thập Thần", tenGod) +
      row("Trường Sinh", growthAt(pillar)) +
      row("Nạp Âm", nayinAt(pillar)) +
      "</div>" +
      "</article>"
    );
  }

  /**
   * @param {object|null|undefined} bazi
   * @returns {string} HTML
   */
  function renderBazi(bazi) {
    try {
      var data =
        bazi && typeof bazi === "object" && !Array.isArray(bazi) ? bazi : {};
      var pillarObjs = PILLARS.map(function (spec) {
        return pickPillar(data, spec);
      });
      var hiddenSlices = sliceHidden(data, pillarObjs);
      var dayPillar = pillarObjs[2];
      var dm = dayMaster(data, dayPillar);
      var dmMeta = stemMeta(dm);

      var summary =
        '<div class="bte-card-grid bte-bazi-summary-grid">' +
        summaryCard(t("bazi.day_master"), dm, dmMeta.element) +
        summaryCard(t("bazi.element"), dmMeta.element, dmMeta.element) +
        summaryCard(t("bazi.yin_yang"), dmMeta.yinYang) +
        "</div>";

      var pillarsHtml =
        '<div class="bte-pillar-grid">' +
        PILLARS.map(function (spec, index) {
          return pillarCard(
            spec.label,
            pillarObjs[index],
            hiddenSlices[index],
            tenGodAt(data, pillarObjs[index], index)
          );
        }).join("") +
        "</div>";

      return (
        '<section class="bte-bazi" aria-label="' + esc(t("bazi.title")) + '">' +
        '<header class="bte-calendar-head">' +
        "<h2>" + esc(t("bazi.title")) + "</h2>" +
        '<p class="bte-calendar-sub">' + esc(t("bazi.subtitle")) + "</p>" +
        "</header>" +
        summary +
        pillarsHtml +
        "</section>"
      );
    } catch (_) {
      return (
        '<section class="bte-bazi">' +
        '<div class="bte-card-grid">' +
        summaryCard(t("bazi.day_master"), MISSING) +
        summaryCard(t("bazi.element"), MISSING) +
        summaryCard(t("bazi.yin_yang"), MISSING) +
        "</div>" +
        '<div class="bte-pillar-grid">' +
        PILLARS.map(function (spec) {
          return pillarCard(spec.label, null, [], MISSING);
        }).join("") +
        "</div>" +
        "</section>"
      );
    }
  }

  global.BtePresenters = global.BtePresenters || {};
  global.BtePresenters.bazi = renderBazi;
})(window);
