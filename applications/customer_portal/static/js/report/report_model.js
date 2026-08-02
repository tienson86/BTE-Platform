/**
 * Phase 2 report view-model — presentation only.
 * Adapts BteSummaryBuilder + analyze payload; never invents engine facts.
 */
(function (global) {
  var MISSING = "--";
  var STEM_ELEMENT = {
    Giáp: "Mộc",
    Ất: "Mộc",
    Bính: "Hỏa",
    Đinh: "Hỏa",
    Mậu: "Thổ",
    Kỷ: "Thổ",
    Canh: "Kim",
    Tân: "Kim",
    Nhâm: "Thủy",
    Quý: "Thủy",
  };
  var BRANCH_ELEMENT = {
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
  var ELEMENT_ORDER = ["Mộc", "Hỏa", "Thổ", "Kim", "Thủy"];
  var PILLAR_KEYS = ["year", "month", "day", "hour"];

  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  function present(v) {
    if (v === null || v === undefined || v === "") return MISSING;
    if (typeof v === "number" && Number.isNaN(v)) return MISSING;
    return String(v);
  }

  function pick(obj, keys) {
    if (!obj || typeof obj !== "object") return null;
    for (var i = 0; i < keys.length; i++) {
      if (
        Object.prototype.hasOwnProperty.call(obj, keys[i]) &&
        obj[keys[i]] != null &&
        obj[keys[i]] !== ""
      ) {
        return obj[keys[i]];
      }
    }
    return null;
  }

  function extractList(data, keys) {
    if (!data || typeof data !== "object") return [];
    for (var i = 0; i < keys.length; i++) {
      var v = data[keys[i]];
      if (Array.isArray(v) && v.length) {
        return v
          .map(function (x) {
            if (x == null) return null;
            if (typeof x === "string" || typeof x === "number") return String(x);
            return x.text || x.body || x.summary || x.name || null;
          })
          .filter(Boolean);
      }
      if (typeof v === "string" && v.trim()) {
        return v.split(/\n+|;\s*/).map(function (s) {
          return s.trim();
        }).filter(Boolean);
      }
    }
    return [];
  }

  function elementCountsFromPillars(pillars) {
    var counts = { Mộc: 0, Hỏa: 0, Thổ: 0, Kim: 0, Thủy: 0 };
    var stems = (pillars && pillars.stems) || [];
    var branches = (pillars && pillars.branches) || [];
    stems.forEach(function (s) {
      var el = STEM_ELEMENT[s];
      if (el) counts[el] += 1;
    });
    branches.forEach(function (b) {
      var el = BRANCH_ELEMENT[b];
      if (el) counts[el] += 1;
    });
    return ELEMENT_ORDER.map(function (k) {
      return { label: k, value: counts[k] };
    });
  }

  function tenGodSeries(pillars, scoreModel) {
    if (scoreModel && scoreModel.length && scoreModel[0].label !== "Thập thần") {
      return scoreModel;
    }
    var counts = {};
    ((pillars && pillars.thap_than) || []).forEach(function (g) {
      if (!g || g === MISSING) return;
      String(g)
        .split(/[,;/|]+/)
        .forEach(function (part) {
          var token = part.trim();
          if (!token || token === MISSING) return;
          counts[token] = (counts[token] || 0) + 1;
        });
    });
    return Object.keys(counts).map(function (k) {
      return { label: k, value: counts[k] };
    });
  }

  function strengthGaugeValue(_overview, score) {
    var raw = pick(score || {}, [
      "strength_score",
      "body_strength_score",
      "than_score",
    ]);
    if (raw != null && Number.isFinite(Number(raw))) return Number(raw);
    return null;
  }

  function qualityLabel(score, interpretation) {
    var grade = pick(score || {}, ["grade", "quality", "quality_grade"]);
    if (grade != null) return present(grade);
    var total = pick(score || {}, ["total_score", "overall_score", "score"]);
    if (total != null && Number.isFinite(Number(total))) {
      return present(total);
    }
    var conf = interpretation && interpretation.confidence;
    if (conf != null) return present(conf);
    return MISSING;
  }

  function summarySentence(dm, overview) {
    var parts = [];
    if (dm && dm.stem && dm.stem !== MISSING) {
      parts.push(
        t("report.summary_dm", {
          stem: dm.stem,
          element: dm.element || MISSING,
        })
      );
    }
    if (overview && overview.cach_cuc && overview.cach_cuc !== MISSING) {
      parts.push(t("report.summary_pattern", { pattern: overview.cach_cuc }));
    }
    if (overview && overview.dung_than && overview.dung_than !== MISSING) {
      parts.push(t("report.summary_useful", { useful: overview.dung_than }));
    }
    if (!parts.length) return t("report.summary_fallback");
    return parts.join(" ");
  }

  function pillarColumns(pillars) {
    var labels = [
      t("executive.col_year"),
      t("executive.col_month"),
      t("executive.col_day"),
      t("executive.col_hour"),
    ];
    return PILLAR_KEYS.map(function (_k, i) {
      return {
        id: PILLAR_KEYS[i],
        label: labels[i],
        isDay: i === 2,
        stem: present(pillars.stems && pillars.stems[i]),
        branch: present(pillars.branches && pillars.branches[i]),
        hidden: present(pillars.tang_can && pillars.tang_can[i]),
        ten_god: present(pillars.thap_than && pillars.thap_than[i]),
        chang_sheng: present(pillars.truong_sinh && pillars.truong_sinh[i]),
        nap_am: present(pillars.nap_am && pillars.nap_am[i]),
      };
    });
  }

  function relationsUnavailable(data) {
    var pattern = data.pattern || {};
    var bazi = data.bazi || {};
    var keys = [
      "hop",
      "xung",
      "hinh",
      "hai",
      "pha",
      "combinations",
      "conflicts",
      "he",
      "chong",
    ];
    var found = {};
    keys.forEach(function (k) {
      var v = pick(pattern, [k]) || pick(bazi, [k]);
      if (v != null) found[k] = v;
    });
    return found;
  }

  function interpChapters(interpretation) {
    var map = [
      { id: "highlights", titleKey: "report.ch_highlights", chapterIds: ["overview", "summary", "tong_quan"] },
      { id: "career", titleKey: "report.ch_career", chapterIds: ["career", "su_nghiep"] },
      { id: "wealth", titleKey: "report.ch_wealth", chapterIds: ["wealth", "tai_van"] },
      { id: "marriage", titleKey: "report.ch_marriage", chapterIds: ["marriage", "hon_nhan"] },
      { id: "health", titleKey: "report.ch_health", chapterIds: ["health", "suc_khoe"] },
      { id: "personality", titleKey: "report.ch_personality", chapterIds: ["bazi", "personality", "five_elements", "ten_gods"] },
      { id: "advice", titleKey: "report.ch_advice", chapterIds: ["conclusion", "recommendations", "useful_god"] },
    ];

    var byId = {};
    var sections = (interpretation && interpretation.sections) || [];
    if (Array.isArray(sections)) {
      sections.forEach(function (sec, idx) {
        if (!sec) return;
        var id = String(sec.id || sec.section || sec.name || "sec_" + idx).toLowerCase();
        var body =
          sec.body || sec.text || sec.content || sec.summary || sec.description || "";
        if (Array.isArray(body)) body = body.join("\n\n");
        byId[id] = {
          title: sec.title || sec.name || id,
          body: body ? String(body) : "",
        };
      });
    }

    return map.map(function (ch) {
      var body = "";
      for (var i = 0; i < ch.chapterIds.length; i++) {
        var hit = byId[ch.chapterIds[i]];
        if (hit && hit.body) {
          body = hit.body;
          break;
        }
      }
      return {
        id: ch.id,
        titleKey: ch.titleKey,
        body: body,
        available: !!body,
      };
    });
  }

  function buildReportModel(data, options) {
    var payload = data && typeof data === "object" ? data : {};
    var input = (options && options.input) || {};
    var summary =
      window.BteSummaryBuilder && typeof window.BteSummaryBuilder.build === "function"
        ? window.BteSummaryBuilder.build(payload, { input: input })
        : null;

    var dm = (summary && summary.day_master) || {};
    var overview = (summary && summary.overview) || {};
    var pillars = (summary && summary.pillars) || {};
    var score = payload.score && typeof payload.score === "object" ? payload.score : {};
    var interpretation =
      payload.interpretation && typeof payload.interpretation === "object"
        ? payload.interpretation
        : {};

    var strengths = extractList(score, ["strengths", "uu_diem", "pros"]);
    var weaknesses = extractList(score, ["weaknesses", "nhuoc_diem", "cons", "warnings"]);
    var elements = elementCountsFromPillars(pillars);
    var tenGods = tenGodSeries(pillars, (summary && summary.ten_gods) || []);
    var gauge = strengthGaugeValue(overview, score);
    var relations = relationsUnavailable(payload);
    var knowledge = payload.knowledge_expert || null;

    return {
      input: input,
      summary: summary,
      executive: {
        day_master: present(dm.stem),
        element: present(dm.element),
        yin_yang: present(dm.yin_yang),
        than: present(overview.than_strength || overview.than),
        strengths: strengths,
        weaknesses: weaknesses,
        dung_than: present(overview.dung_than),
        hy_than: present(overview.hy_than),
        ky_than: present(overview.ky_than),
        cach_cuc: present(overview.cach_cuc),
        quality: qualityLabel(score, interpretation),
        sentence: summarySentence(dm, overview),
      },
      pillars: pillarColumns(pillars),
      charts: {
        elements: elements,
        ten_gods: tenGods,
        strength_gauge: gauge,
        wuxing_score: summary && summary.wuxing,
      },
      analysis: {
        elements: elements,
        ten_gods: tenGods,
        shensha: (summary && summary.shensha) || [],
        overview: overview,
        relations: relations,
        knowledge_status: knowledge,
        pattern: payload.pattern || null,
      },
      interpretation: {
        confidence: interpretation.confidence != null ? present(interpretation.confidence) : MISSING,
        chapters: interpChapters(interpretation),
      },
      knowledge: {
        status: knowledge,
        narrative: payload.narrative || payload.report || null,
        validation_hint: payload.knowledge_expert || null,
      },
      raw: payload,
    };
  }

  global.BteReportModel = {
    build: buildReportModel,
    MISSING: MISSING,
  };
})(typeof window !== "undefined" ? window : globalThis);
