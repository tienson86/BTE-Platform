/**
 * Summary Builder — Portal presentation only.
 * Aggregates analyze API payload into a layout model.
 * Does NOT invent, infer, or calculate business values.
 */
(function (global) {
  var MISSING = "--";

  var STEM_META = {
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

  var BRANCH_HIDDEN_COUNT = {
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

  var PILLAR_SPECS = [
    { key: "year_pillar", alt: ["year", "năm"] },
    { key: "month_pillar", alt: ["month", "tháng"] },
    { key: "day_pillar", alt: ["day", "ngày"] },
    { key: "hour_pillar", alt: ["hour", "giờ", "time_pillar"] },
  ];

  var PATTERN_FIELDS = [
    { id: "than", keys: ["than", "body", "day_master_body", "than_chu", "body_element"] },
    {
      id: "than_strength",
      keys: [
        "than_vuong_nhuoc",
        "strength",
        "strength_level",
        "body_strength",
        "vuong_nhuoc",
        "day_master_strength",
      ],
    },
    { id: "cach_cuc", keys: ["cach_cuc", "pattern", "pattern_name", "ju", "ge_ju", "main_pattern"] },
    { id: "tong_cach", keys: ["tong_cach", "follow_pattern", "cong_ge", "from_pattern", "follower"] },
    { id: "dung_than", keys: ["dung_than", "useful_god", "yong_shen", "yongshen"] },
    { id: "hy_than", keys: ["hy_than", "xi_shen", "favorable_god", "xi_shen_list", "xi"] },
    { id: "ky_than", keys: ["ky_than", "ji_shen", "unfavorable_god", "ji", "avoid_god"] },
    { id: "dieu_hau", keys: ["dieu_hau", "climate", "tiao_hou", "tiaohou", "season_adjust"] },
  ];

  var PATTERN_LABELS = {
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

  function present(value) {
    if (value === null || value === undefined || value === "") return MISSING;
    if (typeof value === "number" && Number.isNaN(value)) return MISSING;
    if (typeof value === "boolean") return value ? "true" : "false";
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
      if (value.name != null && value.name !== "") return formatLabel(value.name);
      if (value.label != null && value.label !== "") return present(value.label);
      if (value.value != null && value.value !== "") return present(value.value);
      if (value.score != null) return present(value.score);
      if (value.level != null && value.level !== "") return present(value.level);
      return MISSING;
    }
    return String(value);
  }

  function formatLabel(raw) {
    var text = present(raw);
    if (text === MISSING) return MISSING;
    var key = String(raw).trim().toLowerCase().replace(/\s+/g, "_");
    if (PATTERN_LABELS[key]) return PATTERN_LABELS[key];
    return text;
  }

  function pick(obj, keys) {
    if (!obj || typeof obj !== "object") return null;
    for (var i = 0; i < keys.length; i++) {
      if (Object.prototype.hasOwnProperty.call(obj, keys[i]) && obj[keys[i]] != null && obj[keys[i]] !== "") {
        return obj[keys[i]];
      }
    }
    return null;
  }

  function pad2(n) {
    var num = Number(n);
    if (!Number.isFinite(num)) return null;
    return String(Math.trunc(num)).padStart(2, "0");
  }

  function formatYmd(year, month, day) {
    var y = present(year);
    var m = pad2(month);
    var d = pad2(day);
    if (y === MISSING && m === null && d === null) return MISSING;
    return [y, m === null ? MISSING : m, d === null ? MISSING : d].join("-");
  }

  function stemMeta(stem) {
    if (!stem || stem === MISSING) return { element: MISSING, yinYang: MISSING };
    if (STEM_META[stem]) return STEM_META[stem];
    var key = Object.keys(STEM_META).find(function (k) {
      return k.toLowerCase() === String(stem).toLowerCase();
    });
    return key ? STEM_META[key] : { element: MISSING, yinYang: MISSING };
  }

  function pickPillar(bazi, spec) {
    if (!bazi || typeof bazi !== "object") return null;
    if (bazi[spec.key] && typeof bazi[spec.key] === "object") return bazi[spec.key];
    for (var i = 0; i < spec.alt.length; i++) {
      var alt = spec.alt[i];
      if (bazi[alt] && typeof bazi[alt] === "object") return bazi[alt];
    }
    var idx = PILLAR_SPECS.indexOf(spec);
    if (Array.isArray(bazi.pillars) && bazi.pillars[idx]) return bazi.pillars[idx];
    return null;
  }

  function pillarStem(pillar) {
    if (!pillar || typeof pillar !== "object") return MISSING;
    return present(pillar.stem || pillar.thien_can || pillar.heavenly_stem || pillar.can || null);
  }

  function pillarBranch(pillar) {
    if (!pillar || typeof pillar !== "object") return MISSING;
    return present(pillar.branch || pillar.dia_chi || pillar.earthly_branch || pillar.chi || null);
  }

  function pillarField(pillar, keys) {
    if (!pillar || typeof pillar !== "object") return null;
    for (var i = 0; i < keys.length; i++) {
      if (pillar[keys[i]] != null && pillar[keys[i]] !== "") return pillar[keys[i]];
    }
    return null;
  }

  function buildBasic(data, input) {
    var cal = (data && data.calendar) || {};
    var bazi = (data && data.bazi) || {};
    var customer = (data && data.customer) || {};
    var inp = input || {};
    var solar = cal.solar && typeof cal.solar === "object" ? cal.solar : null;
    var lunar = cal.lunar && typeof cal.lunar === "object" ? cal.lunar : null;

    var solarDate = formatYmd(
      (solar && solar.year) ?? cal.solar_year ?? inp.year,
      (solar && solar.month) ?? cal.solar_month ?? inp.month,
      (solar && solar.day) ?? cal.solar_day ?? inp.day
    );
    var lunarDate = lunar
      ? formatYmd(lunar.year, lunar.month, lunar.day)
      : MISSING;

    var hh = pad2(cal.solar_hour != null ? cal.solar_hour : inp.hour);
    var mm = pad2(cal.solar_minute != null ? cal.solar_minute : inp.minute);
    var birthTime =
      hh === null && mm === null
        ? MISSING
        : (hh === null ? MISSING : hh) + ":" + (mm === null ? MISSING : mm);

    var genderRaw =
      pick(customer, ["gender", "gioi_tinh", "sex"]) ||
      pick(inp, ["gender", "gioi_tinh", "sex"]) ||
      pick(bazi, ["gender", "gioi_tinh", "sex"]) ||
      null;

    return {
      name: present(
        pick(customer, ["full_name", "name", "ho_ten"]) ||
          pick(inp, ["full_name", "name", "ho_ten", "hoten", "customer_name"])
      ),
      birth_place: present(
        pick(customer, ["birth_place", "noi_sinh", "place_of_birth", "birthplace"]) ||
          pick(inp, ["birth_place", "noi_sinh", "place_of_birth", "birthplace"])
      ),
      gender: present(genderRaw),
      gender_raw: genderRaw,
      solar: solarDate,
      lunar: lunarDate,
      birth_time: birthTime,
      timezone: present(
        pick(customer, ["timezone", "tz"]) ||
          pick(cal, ["timezone", "tz", "time_zone"]) ||
          pick(inp, ["timezone", "tz", "time_zone"])
      ),
    };
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

  function buildPillars(bazi) {
    var pillars = PILLAR_SPECS.map(function (spec) {
      return pickPillar(bazi, spec);
    });
    var hidden = sliceHidden(bazi || {}, pillars);
    var stems = [];
    var branches = [];
    var napAm = [];
    var tangCan = [];
    var thapThan = [];
    var truongSinh = [];

    pillars.forEach(function (pillar, index) {
      stems.push(pillarStem(pillar));
      branches.push(pillarBranch(pillar));
      napAm.push(
        present(pillarField(pillar, ["nap_am", "nayin", "na_yin", "napam"]))
      );
      var fromPillar = pillarField(pillar, [
        "hidden_stems",
        "tang_can",
        "cang_gan",
        "hidden",
      ]);
      tangCan.push(fromPillar != null ? present(fromPillar) : present(hidden[index]));
      var tg = pillarField(pillar, ["ten_god", "ten_gods", "thap_than", "shi_shen"]);
      if (tg != null) thapThan.push(present(tg));
      else if (Array.isArray(bazi.ten_gods) && bazi.ten_gods[index] != null) {
        thapThan.push(present(bazi.ten_gods[index]));
      } else thapThan.push(MISSING);
      truongSinh.push(
        present(
          pillarField(pillar, [
            "truong_sinh",
            "growth",
            "chang_sheng",
            "stage",
            "twelve_stage",
          ])
        )
      );
    });

    return {
      stems: stems,
      branches: branches,
      nap_am: napAm,
      tang_can: tangCan,
      thap_than: thapThan,
      truong_sinh: truongSinh,
    };
  }

  function buildDayMaster(bazi, dayPillar) {
    var dm =
      pick(bazi, ["day_master", "dayMaster", "nhat_chu"]) || pillarStem(dayPillar);
    var meta = stemMeta(dm);
    var element =
      present(pick(bazi, ["day_master_element", "element", "ngu_hanh"])) !== MISSING
        ? present(pick(bazi, ["day_master_element", "element", "ngu_hanh"]))
        : meta.element;
    var yinYang =
      present(pick(bazi, ["day_master_yin_yang", "yin_yang", "am_duong"])) !== MISSING
        ? present(pick(bazi, ["day_master_yin_yang", "yin_yang", "am_duong"]))
        : meta.yinYang;
    return { stem: present(dm), element: element, yin_yang: yinYang };
  }

  function buildOverview(pattern) {
    var out = {};
    PATTERN_FIELDS.forEach(function (field) {
      out[field.id] = present(pick(pattern || {}, field.keys));
      if (field.id === "cach_cuc" && out[field.id] !== MISSING) {
        out[field.id] = formatLabel(out[field.id]);
      }
    });
    return out;
  }

  function extractNamedScores(source) {
    if (!source) return null;
    var rows = [];
    if (Array.isArray(source)) {
      source.forEach(function (item) {
        if (!item || typeof item !== "object") return;
        var label = item.label || item.name || item.key || item.element || item.god || item.id;
        var value = item.value != null ? item.value : item.score != null ? item.score : item.weight;
        if (label != null && value != null) rows.push({ label: String(label), value: value });
      });
      return rows.length ? rows : null;
    }
    if (typeof source === "object") {
      Object.keys(source).forEach(function (key) {
        var val = source[key];
        if (typeof val === "number") rows.push({ label: key, value: val });
        else if (val && typeof val === "object" && val.score != null) {
          rows.push({ label: key, value: val.score });
        }
      });
      return rows.length ? rows : null;
    }
    return null;
  }

  function buildSeries(score, keys, detailsKey, scalarKey, fallbackLabel) {
    var direct = pick(score || {}, keys);
    var fromDirect = extractNamedScores(direct);
    if (fromDirect) return fromDirect;
    var details = score && score.details && score.details[detailsKey];
    if (details) {
      var nested =
        extractNamedScores(details.details) ||
        extractNamedScores(details.metadata) ||
        extractNamedScores(details.matched_rules) ||
        extractNamedScores(details);
      if (nested) return nested;
      if (details.score != null || details.weighted_score != null) {
        return [
          {
            label: details.dimension || fallbackLabel,
            value: details.score != null ? details.score : details.weighted_score,
          },
        ];
      }
    }
    if (score && Object.prototype.hasOwnProperty.call(score, scalarKey)) {
      return [{ label: fallbackLabel, value: score[scalarKey] }];
    }
    return [];
  }

  function buildShensha(bazi) {
    var raw = pick(bazi || {}, [
      "shensha",
      "than_sat",
      "shen_sha",
      "spirits",
      "star_spirits",
    ]);
    if (!raw) return [];
    if (Array.isArray(raw)) {
      return raw
        .map(function (item) {
          return present(item);
        })
        .filter(function (v) {
          return v !== MISSING;
        });
    }
    if (typeof raw === "object") {
      return Object.keys(raw)
        .map(function (k) {
          var v = raw[k];
          if (v === true) return String(k);
          if (v == null || v === false || v === "") return null;
          return String(k) + ": " + present(v);
        })
        .filter(Boolean);
    }
    var one = present(raw);
    return one === MISSING ? [] : [one];
  }

  function buildDaiVan(data) {
    var sources = [
      pick(data || {}, ["dai_van", "major_luck", "da_yun", "luck_cycles"]),
      data && data.bazi && pick(data.bazi, ["dai_van", "major_luck", "da_yun", "luck"]),
      data &&
        data.interpretation &&
        pick(data.interpretation, ["dai_van", "major_luck", "da_yun", "luck"]),
    ];
    for (var i = 0; i < sources.length; i++) {
      var raw = sources[i];
      if (!raw) continue;
      if (Array.isArray(raw) && raw.length) {
        return raw.map(function (row, idx) {
          if (!row || typeof row !== "object") {
            return {
              index: idx + 1,
              label: present(row),
              stem: MISSING,
              branch: MISSING,
              start: MISSING,
              end: MISSING,
              age: MISSING,
            };
          }
          return {
            index: idx + 1,
            label: present(row.label || row.name || row.title || idx + 1),
            stem: present(row.stem || row.thien_can || row.can),
            branch: present(row.branch || row.dia_chi || row.chi),
            start: present(row.start || row.start_year || row.from || row.begin),
            end: present(row.end || row.end_year || row.to || row.finish),
            age: present(row.age || row.start_age || row.tuoi),
          };
        });
      }
      if (typeof raw === "string" || typeof raw === "number") {
        return [
          {
            index: 1,
            label: present(raw),
            stem: MISSING,
            branch: MISSING,
            start: MISSING,
            end: MISSING,
            age: MISSING,
          },
        ];
      }
    }
    return [];
  }

  function buildCanXuong(data) {
    var cx =
      pick(data || {}, ["can_xuong", "bone_weight", "canxuong", "weight_poem"]) ||
      (data && data.bazi && pick(data.bazi, ["can_xuong", "bone_weight", "canxuong"])) ||
      (data &&
        data.interpretation &&
        pick(data.interpretation, ["can_xuong", "bone_weight", "canxuong"])) ||
      {};
    if (typeof cx !== "object" || cx === null) {
      return {
        year: MISSING,
        month: MISSING,
        day: MISSING,
        hour: MISSING,
        total: MISSING,
        poem: MISSING,
      };
    }
    return {
      year: present(pick(cx, ["year", "nam", "year_weight", "luong_chi_nam"])),
      month: present(pick(cx, ["month", "thang", "month_weight", "luong_chi_thang"])),
      day: present(pick(cx, ["day", "ngay", "day_weight", "luong_chi_ngay"])),
      hour: present(pick(cx, ["hour", "gio", "hour_weight", "luong_chi_gio"])),
      total: present(pick(cx, ["total", "tong", "sum", "tong_luong_chi"])),
      poem: present(pick(cx, ["poem", "bai_tho", "verse", "text", "content"])),
    };
  }

  function buildHighlight(dayMaster, overview, score) {
    return {
      day_master: dayMaster.stem,
      than: overview.than,
      cach_cuc: overview.cach_cuc,
      dung_than: overview.dung_than,
      hy_than: overview.hy_than,
      dieu_hau: overview.dieu_hau,
      total_score: present(
        pick(score || {}, ["total_score", "overall_score", "overall", "final_score", "score"])
      ),
      grade: present(pick(score || {}, ["grade", "rank", "xep_loai", "classification"])),
    };
  }

  /**
   * @param {object|null|undefined} data - full analyze `data` payload
   * @param {{ input?: object }} [options]
   * @returns {object} layout model (display values only)
   */
  function buildSummary(data, options) {
    var payload = data && typeof data === "object" ? data : {};
    var input = (options && options.input) || {};
    var bazi = payload.bazi && typeof payload.bazi === "object" ? payload.bazi : {};
    var pattern =
      payload.pattern && typeof payload.pattern === "object" ? payload.pattern : {};
    var score = payload.score && typeof payload.score === "object" ? payload.score : {};
    var dayPillar = pickPillar(bazi, PILLAR_SPECS[2]);
    var dayMaster = buildDayMaster(bazi, dayPillar);
    var overview = buildOverview(pattern);

    return {
      basic: buildBasic(payload, input),
      pillars: buildPillars(bazi),
      day_master: dayMaster,
      overview: overview,
      wuxing: buildSeries(
        score,
        ["ngu_hanh", "wuxing", "five_elements", "elements", "element_scores", "wuxing_scores"],
        "wuxing",
        "wuxing_score",
        "Ngũ hành"
      ),
      ten_gods: buildSeries(
        score,
        ["thap_than", "ten_gods", "ten_god_scores", "shi_shen", "gods"],
        "ten_gods",
        "ten_god_score",
        "Thập thần"
      ),
      shensha: buildShensha(bazi),
      dai_van: buildDaiVan(payload),
      can_xuong: buildCanXuong(payload),
      highlight: buildHighlight(dayMaster, overview, score),
    };
  }

  global.BteSummaryBuilder = {
    build: buildSummary,
    MISSING: MISSING,
  };
})(window);
