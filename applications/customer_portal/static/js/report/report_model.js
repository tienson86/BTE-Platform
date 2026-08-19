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

  /** Prefer score series; else display-only pillar counts (Binding Index). */
  function elementSeries(score, pillars, summaryWuxing) {
    var fromScore = namedSeries(score, [
      "wuxing_series",
      "element_series",
      "five_elements",
      "ngu_hanh",
      "wuxing",
      "element_scores",
      "wuxing_scores",
    ]);
    if (fromScore && fromScore.length) {
      return { series: fromScore, source: "score" };
    }
    if (
      Array.isArray(summaryWuxing) &&
      summaryWuxing.length &&
      summaryWuxing[0] &&
      summaryWuxing[0].label !== "Ngũ hành"
    ) {
      return { series: summaryWuxing, source: "score" };
    }
    var counts = elementCountsFromPillars(pillars);
    var has = counts.some(function (x) {
      return Number(x.value) > 0;
    });
    return {
      series: has ? counts : [],
      source: has ? "pillars" : "none",
    };
  }

  function namedSeries(obj, keys) {
    if (!obj || typeof obj !== "object") return null;
    for (var i = 0; i < keys.length; i++) {
      var v = obj[keys[i]];
      if (!v) continue;
      if (Array.isArray(v) && v.length) {
        var mapped = v
          .map(function (it) {
            if (it == null) return null;
            if (typeof it === "number") return null;
            if (typeof it === "string") return null;
            var label = it.label || it.name || it.element || it.key;
            var value = it.value != null ? it.value : it.score != null ? it.score : it.count;
            if (label == null || value == null || !Number.isFinite(Number(value))) {
              return null;
            }
            return { label: String(label), value: Number(value) };
          })
          .filter(Boolean);
        if (mapped.length) return mapped;
      }
      if (typeof v === "object" && !Array.isArray(v)) {
        var fromObj = Object.keys(v)
          .map(function (k) {
            var num = Number(v[k]);
            if (!Number.isFinite(num)) return null;
            return { label: k, value: num };
          })
          .filter(Boolean);
        if (fromObj.length) return fromObj;
      }
    }
    return null;
  }

  function chartInsightText(interpretation, idHints) {
    var sections = (interpretation && interpretation.sections) || [];
    if (!Array.isArray(sections)) return null;
    for (var i = 0; i < sections.length; i++) {
      var sec = sections[i];
      if (!sec) continue;
      var id = String(sec.id || sec.section || sec.name || "").toLowerCase();
      var hit = idHints.some(function (h) {
        return id.indexOf(h) !== -1;
      });
      if (!hit) continue;
      var body =
        sec.body || sec.text || sec.content || sec.summary || sec.description || "";
      if (Array.isArray(body)) body = body.join(" ");
      body = String(body || "").trim();
      if (!body) continue;
      var first = body.split(/[.!?。…]\s+|\n+/)[0].trim();
      return first || null;
    }
    return null;
  }

  function asList(raw) {
    if (!raw) return [];
    if (Array.isArray(raw)) return raw;
    if (typeof raw === "object") return [raw];
    if (typeof raw === "string" && raw.trim()) return [raw.trim()];
    return [];
  }

  /** Display-safe rule rows — never invent; prefer title over raw id. */
  function extractRules(containers) {
    var out = [];
    (containers || []).forEach(function (obj) {
      if (!obj || typeof obj !== "object") return;
      var lists = []
        .concat(asList(obj.rules))
        .concat(asList(obj.applied_rules))
        .concat(asList(obj.rule_trace))
        .concat(asList(obj.priority_rules));
      lists.forEach(function (r) {
        if (r == null) return;
        if (typeof r === "string") {
          out.push({
            name: r,
            id: null,
            priority: null,
            reason: null,
          });
          return;
        }
        if (typeof r !== "object") return;
        var name =
          r.display_name ||
          r.name ||
          r.title ||
          r.rule_name ||
          r.label ||
          null;
        var id = r.rule_id || r.id || r.code || null;
        /* Consumer: prefer name; hide bare internal ids */
        if (!name && id) name = null;
        if (!name && !r.reason && r.priority == null) return;
        out.push({
          name: name,
          id: name ? id : null,
          priority: r.priority != null ? r.priority : r.rank != null ? r.rank : null,
          reason: r.reason || r.explanation || r.why || r.description || null,
        });
      });
    });
    return out;
  }

  function extractEvidence(containers) {
    var out = [];
    (containers || []).forEach(function (obj) {
      if (!obj || typeof obj !== "object") return;
      asList(obj.evidence)
        .concat(asList(obj.evidences))
        .concat(asList(obj.proofs))
        .concat(asList(obj.citations))
        .forEach(function (e) {
          if (e == null) return;
          if (typeof e === "string") {
            out.push({ label: e, reference: null });
            return;
          }
          if (typeof e !== "object") return;
          var label =
            e.label || e.text || e.summary || e.body || e.name || e.title || null;
          if (!label) return;
          out.push({
            label: String(label),
            reference: e.reference || e.source || e.citation || null,
          });
        });
    });
    return out;
  }

  function pickConfidence(containers) {
    for (var i = 0; i < (containers || []).length; i++) {
      var obj = containers[i];
      if (!obj || typeof obj !== "object") continue;
      if (obj.confidence != null && obj.confidence !== "") return obj.confidence;
      if (obj.confidence_score != null) return obj.confidence_score;
    }
    return null;
  }

  function knowledgeRef(knowledge) {
    if (!knowledge || typeof knowledge !== "object") return null;
    var citation =
      knowledge.citation ||
      knowledge.reference ||
      knowledge.knowledge_reference ||
      knowledge.title ||
      null;
    var link =
      knowledge.link ||
      knowledge.url ||
      knowledge.href ||
      null;
    if (!citation && !link && knowledge.status == null) return null;
    return {
      citation: citation ? String(citation) : null,
      link: link ? String(link) : "#tier-knowledge",
      status: knowledge.status != null ? String(knowledge.status) : null,
    };
  }

  function seriesFactors(series) {
    return (series || [])
      .filter(function (x) {
        return x && Number(x.value) > 0;
      })
      .map(function (x) {
        return x.label + ": " + x.value;
      });
  }

  function makeBlock(opts) {
    var conclusion = opts.conclusion;
    var hasConclusion = conclusion != null && conclusion !== "" && conclusion !== MISSING;
    var factors = opts.factors || [];
    var rules = opts.rules || [];
    var evidence = opts.evidence || [];
    var status = "unavailable";
    if (hasConclusion) {
      status =
        factors.length || rules.length || evidence.length || opts.summary
          ? "available"
          : "partial";
    }
    return {
      id: opts.id,
      titleKey: opts.titleKey,
      status: status,
      conclusion: hasConclusion ? String(conclusion) : null,
      summary: opts.summary || null,
      factors: factors,
      rules: rules,
      evidence: evidence,
      confidence: opts.confidence != null ? opts.confidence : null,
      knowledge: opts.knowledge || null,
      open: !!opts.open,
    };
  }

  function buildAnalysisBlocks(ctx) {
    var overview = ctx.overview || {};
    var pattern = ctx.pattern || {};
    var score = ctx.score || {};
    var interpretation = ctx.interpretation || {};
    var knowledge = ctx.knowledge;
    var relations = ctx.relations || {};
    var baseContainers = [pattern, score, ctx.payload];
    var kRef = knowledgeRef(knowledge);
    var interpConf = interpretation.confidence;

    function scoped(extra) {
      return baseContainers.concat(extra || []);
    }

    var blocks = [];

    var elFactors = seriesFactors(ctx.elements);
    blocks.push(
      makeBlock({
        id: "elements",
        titleKey: "report.an_elements",
        open: true,
        conclusion: elFactors.length ? elFactors.join(" · ") : null,
        summary: chartInsightText(interpretation, [
          "five_element",
          "ngu_hanh",
          "wuxing",
          "element",
        ]),
        factors: elFactors,
        rules: extractRules(scoped([pattern.ngu_hanh, pattern.elements, score.wuxing])),
        evidence: extractEvidence(scoped([pattern.ngu_hanh, pattern.elements])),
        confidence: pickConfidence(scoped([pattern.ngu_hanh])),
        knowledge: kRef,
      })
    );

    var godFactors = seriesFactors(ctx.tenGods);
    blocks.push(
      makeBlock({
        id: "ten_gods",
        titleKey: "report.an_gods",
        open: true,
        conclusion: godFactors.length ? godFactors.join(" · ") : null,
        summary: chartInsightText(interpretation, [
          "ten_god",
          "thap_than",
          "shi_shen",
        ]),
        factors: godFactors,
        rules: extractRules(scoped([pattern.thap_than, score.ten_gods])),
        evidence: extractEvidence(scoped([pattern.thap_than])),
        confidence: pickConfidence(scoped([pattern.thap_than])),
        knowledge: kRef,
      })
    );

    var cach =
      overview.cach_cuc && overview.cach_cuc !== MISSING
        ? overview.cach_cuc
        : present(pick(pattern, ["cach_cuc", "pattern_name", "ge_ju", "main_pattern"]));
    var tong =
      overview.tong_cach && overview.tong_cach !== MISSING
        ? overview.tong_cach
        : present(pick(pattern, ["tong_cach", "follow_pattern"]));
    var patternConclusion =
      cach !== MISSING
        ? tong !== MISSING
          ? cach + " · " + tong
          : cach
        : null;
    blocks.push(
      makeBlock({
        id: "pattern",
        titleKey: "report.an_pattern",
        open: true,
        conclusion: patternConclusion,
        summary: chartInsightText(interpretation, ["pattern", "cach", "ge_ju"]),
        factors: [cach !== MISSING ? cach : null, tong !== MISSING ? tong : null].filter(
          Boolean
        ),
        rules: extractRules(scoped([pattern])),
        evidence: extractEvidence(scoped([pattern])),
        confidence: pickConfidence(scoped([pattern])),
        knowledge: kRef,
      })
    );

    var than = overview.than_strength || overview.than;
    blocks.push(
      makeBlock({
        id: "than",
        titleKey: "report.an_than",
        open: true,
        conclusion: than && than !== MISSING ? than : null,
        summary: chartInsightText(interpretation, ["strength", "than", "body"]),
        factors: than && than !== MISSING ? [than] : [],
        rules: extractRules(scoped([pattern.than, pattern.strength])),
        evidence: extractEvidence(scoped([pattern.than])),
        confidence: pickConfidence(scoped([pattern.than, score])),
        knowledge: kRef,
      })
    );

    [
      {
        id: "dung",
        titleKey: "report.an_dung",
        value: overview.dung_than,
        hints: ["useful", "dung", "yong"],
        open: false,
      },
      {
        id: "hy",
        titleKey: "report.an_hy",
        value: overview.hy_than,
        hints: ["favor", "hy", "xi"],
        open: false,
      },
      {
        id: "ky",
        titleKey: "report.an_ky",
        value: overview.ky_than,
        hints: ["unfavor", "ky", "ji", "avoid"],
        open: false,
      },
    ].forEach(function (spec) {
      var v = spec.value && spec.value !== MISSING ? spec.value : null;
      blocks.push(
        makeBlock({
          id: spec.id,
          titleKey: spec.titleKey,
          open: spec.open,
          conclusion: v,
          summary: chartInsightText(interpretation, spec.hints),
          factors: v ? [v] : [],
          rules: extractRules(scoped([pattern.useful_god, pattern.dung_than])),
          evidence: extractEvidence(scoped([pattern.useful_god])),
          confidence: pickConfidence(scoped([pattern.useful_god])),
          knowledge: kRef,
        })
      );
    });

    [
      { id: "hop", titleKey: "report.rel_hop", keys: ["hop", "he", "combinations"] },
      { id: "xung", titleKey: "report.rel_xung", keys: ["xung", "chong", "conflicts"] },
      { id: "hinh", titleKey: "report.rel_hinh", keys: ["hinh"] },
      { id: "hai", titleKey: "report.rel_hai", keys: ["hai"] },
      { id: "pha", titleKey: "report.rel_pha", keys: ["pha"] },
    ].forEach(function (rel) {
      var raw = null;
      for (var i = 0; i < rel.keys.length; i++) {
        if (relations[rel.keys[i]] != null && relations[rel.keys[i]] !== "") {
          raw = relations[rel.keys[i]];
          break;
        }
      }
      var text =
        raw == null
          ? null
          : typeof raw === "string" || typeof raw === "number"
            ? String(raw)
            : Array.isArray(raw)
              ? raw
                  .map(function (x) {
                    if (x == null) return null;
                    if (typeof x === "string" || typeof x === "number") return String(x);
                    return x.label || x.name || x.title || null;
                  })
                  .filter(Boolean)
                  .join(" · ") || null
              : raw.label || raw.name || raw.title || raw.summary || null;
      blocks.push(
        makeBlock({
          id: rel.id,
          titleKey: rel.titleKey,
          open: false,
          conclusion: text,
          summary: null,
          factors: text ? [text] : [],
          rules: extractRules(scoped([])),
          evidence: extractEvidence(scoped([])),
          confidence: null,
          knowledge: kRef,
        })
      );
    });

    var shensha = (ctx.shensha || [])
      .map(function (s) {
        if (s == null) return null;
        if (typeof s === "string") return s;
        return s.name || s.label || s.title || null;
      })
      .filter(Boolean);
    blocks.push(
      makeBlock({
        id: "shensha",
        titleKey: "report.an_shensha",
        open: false,
        conclusion: shensha.length ? shensha.join(" · ") : null,
        summary: chartInsightText(interpretation, ["shen", "than_sat"]),
        factors: shensha,
        rules: extractRules(scoped([pattern.shensha, ctx.payload && ctx.payload.bazi])),
        evidence: extractEvidence(scoped([pattern.shensha])),
        confidence: pickConfidence(scoped([pattern.shensha])),
        knowledge: kRef,
      })
    );

    var priorityRules = extractRules([
      pattern,
      score,
      knowledge,
      ctx.payload && ctx.payload.priority_rules,
    ]);
    var priorityText = null;
    if (knowledge && typeof knowledge === "object") {
      if (knowledge.status != null) priorityText = String(knowledge.status);
      else if (knowledge.message) priorityText = String(knowledge.message);
    }
    if (!priorityText && priorityRules.length) {
      priorityText = priorityRules
        .map(function (r) {
          return r.name || r.reason;
        })
        .filter(Boolean)
        .join(" · ");
    }
    var statusFactors = [];
    if (knowledge && typeof knowledge === "object") {
      Object.keys(knowledge).forEach(function (k) {
        /* Hide engine-ish keys */
        if (/engine|class|module|traceback/i.test(k)) return;
        var val = knowledge[k];
        if (val == null || typeof val === "object") return;
        statusFactors.push(k + ": " + String(val));
      });
    }
    blocks.push(
      makeBlock({
        id: "priority_knowledge",
        titleKey: "report.an_priority_knowledge",
        open: false,
        conclusion: priorityText,
        summary: null,
        factors: statusFactors,
        rules: priorityRules,
        evidence: extractEvidence([knowledge, score]),
        confidence: pickConfidence([knowledge, { confidence: interpConf }]),
        knowledge: kRef || (knowledge ? { citation: null, link: "#tier-knowledge", status: null } : null),
      })
    );

    return blocks;
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

  function strengthClassLabel(payload, overview) {
    var labels = {
      strong: "Thân vượng",
      weak: "Thân nhược",
      balanced: "Thân cân bằng",
    };
    var strength = payload && payload.strength && typeof payload.strength === "object"
      ? payload.strength
      : {};
    var level = String(strength.strength_level || strength.level || "")
      .trim()
      .toLowerCase();
    if (labels[level]) return labels[level];
    return present(overview && (overview.than_strength || overview.than));
  }

  function strengthGaugeValue(_overview, _score, payload) {
    var strength = payload && payload.strength && typeof payload.strength === "object"
      ? payload.strength
      : {};
    var raw = pick(strength, ["strength_score"]);
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

  /** Addendum A.2 / Localization L — display-only quality caption. */
  function qualityVerdict(score, interpretation) {
    var grade = pick(score || {}, ["grade", "quality", "quality_grade"]);
    if (grade != null) {
      var gradeNum = Number(grade);
      if (Number.isFinite(gradeNum)) {
        return qualityBandFromScore(gradeNum);
      }
      return {
        mode: "grade",
        available: true,
        caption: t("report.quality_verdict.grade", { grade: String(grade) }),
        band: null,
      };
    }
    var total = pick(score || {}, ["total_score", "overall_score", "score"]);
    if (total != null && Number.isFinite(Number(total))) {
      return qualityBandFromScore(Number(total));
    }
    var conf = interpretation && interpretation.confidence;
    if (conf != null && conf !== "") {
      return {
        mode: "confidence",
        available: true,
        caption: t("report.quality_verdict.confidence_only", {
          value: String(conf),
        }),
        band: null,
      };
    }
    return { mode: "unavailable", available: false, caption: null, band: null };
  }

  function qualityBandFromScore(score) {
    var band = "mid";
    if (score >= 70) band = "high";
    else if (score < 40) band = "low";
    return {
      mode: "band",
      available: true,
      caption: t("report.quality_verdict." + band),
      band: band,
    };
  }

  /** Addendum A.3 — first recommendation only; never invent. */
  function firstRecommendation(score, interpretation) {
    var fromScore = extractList(score || {}, [
      "recommendations",
      "recommendation",
    ]);
    if (fromScore.length) return fromScore[0];

    var chapters = interpChapters(interpretation);
    var prefer = ["advice", "highlights"];
    for (var p = 0; p < prefer.length; p++) {
      for (var i = 0; i < chapters.length; i++) {
        if (
          chapters[i].id === prefer[p] &&
          chapters[i].available &&
          chapters[i].body
        ) {
          var first = String(chapters[i].body)
            .split(/[.!?。…]\s+|\n+/)
            .map(function (s) {
              return s.trim();
            })
            .filter(Boolean)[0];
          if (first) return first;
        }
      }
    }
    return null;
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

  function splitTokens(raw) {
    if (raw === null || raw === undefined || raw === "" || raw === MISSING) {
      return [];
    }
    if (Array.isArray(raw)) {
      return raw
        .map(function (x) {
          if (x == null || x === "") return null;
          if (typeof x === "object") {
            return x.name || x.label || x.stem || x.text || null;
          }
          return String(x).trim();
        })
        .filter(function (x) {
          return x && x !== MISSING;
        });
    }
    return String(raw)
      .split(/[,;/|、]+/)
      .map(function (s) {
        return s.trim();
      })
      .filter(function (s) {
        return s && s !== MISSING;
      });
  }

  function pillarColumns(pillars) {
    var labels = [
      t("executive.col_year"),
      t("executive.col_month"),
      t("executive.col_day"),
      t("executive.col_hour"),
    ];
    var roleKeys = ["year", "month", "day", "hour"];
    return PILLAR_KEYS.map(function (_k, i) {
      var hiddenRaw = pillars.tang_can && pillars.tang_can[i];
      var tenGodRaw = pillars.thap_than && pillars.thap_than[i];
      var tenGodList = splitTokens(tenGodRaw);
      var isDay = i === 2;
      return {
        id: PILLAR_KEYS[i],
        label: labels[i],
        role_key: roleKeys[i],
        isDay: isDay,
        stem: present(pillars.stems && pillars.stems[i]),
        branch: present(pillars.branches && pillars.branches[i]),
        hidden: present(hiddenRaw),
        hidden_list: splitTokens(hiddenRaw),
        ten_god: present(tenGodRaw),
        ten_god_list: tenGodList,
        chang_sheng: present(pillars.truong_sinh && pillars.truong_sinh[i]),
        nap_am: present(pillars.nap_am && pillars.nap_am[i]),
        /* Thập thần = quan hệ với Nhật Chủ khi payload có; không suy diễn thêm. */
        relation_to_day_master: isDay
          ? t("bazi.day_master")
          : tenGodList.length
            ? tenGodList.join(" · ")
            : MISSING,
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
      {
        id: "overview",
        titleKey: "report.ch_overview",
        number: 1,
        chapterIds: ["overview", "summary", "tong_quan", "highlights"],
      },
      {
        id: "personality",
        titleKey: "report.ch_personality",
        number: 2,
        chapterIds: ["personality", "tinh_cach", "bazi", "five_elements", "ten_gods"],
      },
      {
        id: "career",
        titleKey: "report.ch_career",
        number: 3,
        chapterIds: ["career", "su_nghiep"],
      },
      {
        id: "wealth",
        titleKey: "report.ch_wealth",
        number: 4,
        chapterIds: ["wealth", "tai_van"],
      },
      {
        id: "marriage",
        titleKey: "report.ch_marriage",
        number: 5,
        chapterIds: ["marriage", "hon_nhan"],
      },
      {
        id: "health",
        titleKey: "report.ch_health",
        number: 6,
        chapterIds: ["health", "suc_khoe"],
      },
      {
        id: "advice",
        titleKey: "report.ch_advice",
        number: 7,
        chapterIds: [
          "conclusion",
          "recommendations",
          "advice",
          "useful_god",
          "ket_luan",
        ],
      },
      {
        id: "classical",
        titleKey: "report.ch_classical",
        number: 8,
        chapterIds: [
          "classical",
          "co_thu",
          "cot_thu",
          "cang_thu",
          "books",
          "bibliography",
        ],
      },
      {
        id: "references",
        titleKey: "report.ch_references",
        number: 9,
        chapterIds: ["references", "citations", "reference", "sources"],
      },
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
          callout: sec.callout || sec.insight || sec.caution || null,
          citations: asList(sec.citations)
            .concat(asList(sec.references))
            .concat(asList(sec.evidence)),
          knowledge: sec.knowledge_reference || sec.knowledge || null,
        };
      });
    }

    function firstSentence(text) {
      if (!text) return null;
      var s = String(text)
        .split(/[.!?。…]\s+|\n+/)
        .map(function (x) {
          return x.trim();
        })
        .filter(Boolean)[0];
      return s || null;
    }

    function normalizeCitations(rawList) {
      return (rawList || [])
        .map(function (c) {
          if (c == null) return null;
          if (typeof c === "string") return { label: c, reference: null };
          if (typeof c !== "object") return null;
          var label =
            c.label ||
            c.text ||
            c.title ||
            c.name ||
            c.citation ||
            c.reference ||
            null;
          if (!label) return null;
          return {
            label: String(label),
            reference: c.source || c.book || c.reference || null,
          };
        })
        .filter(Boolean);
    }

    var chapters = map.map(function (ch) {
      var hit = null;
      for (var i = 0; i < ch.chapterIds.length; i++) {
        if (byId[ch.chapterIds[i]] && byId[ch.chapterIds[i]].body) {
          hit = byId[ch.chapterIds[i]];
          break;
        }
      }
      if (!hit && ch.id === "references") {
        for (var j = 0; j < ch.chapterIds.length; j++) {
          if (byId[ch.chapterIds[j]]) {
            hit = byId[ch.chapterIds[j]];
            break;
          }
        }
      }
      var body = hit && hit.body ? hit.body : "";
      var citations = normalizeCitations(hit && hit.citations);
      var callout = hit && hit.callout ? String(hit.callout) : null;
      if (!callout && ch.id === "advice" && body) {
        callout = firstSentence(body);
      }
      var available = !!body || (ch.id === "references" && citations.length > 0);
      return {
        id: ch.id,
        number: ch.number,
        titleKey: ch.titleKey,
        anchor: "interp-" + ch.id,
        body: body,
        summary: firstSentence(body),
        callout: callout,
        citations: citations,
        knowledge: hit && hit.knowledge ? String(hit.knowledge) : null,
        available: available,
      };
    });

    var docRefs = normalizeCitations(
      asList(interpretation && interpretation.references).concat(
        asList(interpretation && interpretation.citations)
      )
    );
    var refChapter = null;
    for (var r = 0; r < chapters.length; r++) {
      if (chapters[r].id === "references") {
        refChapter = chapters[r];
        break;
      }
    }
    if (refChapter && docRefs.length) {
      refChapter.citations = refChapter.citations.concat(docRefs);
      refChapter.available = true;
    }

    return chapters;
  }

  function buildInterpretationDocument(interpretation) {
    var chapters = interpChapters(interpretation);
    var overview = null;
    for (var i = 0; i < chapters.length; i++) {
      if (chapters[i].id === "overview") {
        overview = chapters[i];
        break;
      }
    }
    var availableCount = chapters.filter(function (c) {
      return c.available;
    }).length;
    return {
      chapters: chapters,
      executive: {
        available: !!(overview && overview.available),
        summary: overview && overview.summary ? overview.summary : null,
        callout: overview && overview.callout ? overview.callout : null,
        body: overview && overview.body ? overview.body : null,
      },
      toc: chapters.map(function (c) {
        return {
          id: c.id,
          anchor: c.anchor,
          number: c.number,
          titleKey: c.titleKey,
          available: c.available,
        };
      }),
      showToc: availableCount >= 2 || chapters.length >= 2,
    };
  }

  function buildKnowledgeWorkspace(payload, analysisBlocks, interpChapters) {
    var blocks = [];
    var ke =
      payload.knowledge_expert && typeof payload.knowledge_expert === "object"
        ? payload.knowledge_expert
        : null;
    var pattern =
      payload.pattern && typeof payload.pattern === "object" ? payload.pattern : {};
    var knowledgeRoot =
      payload.knowledge && typeof payload.knowledge === "object"
        ? payload.knowledge
        : {};

    function mapSourceType(raw) {
      var s = String(raw || "unknown").toLowerCase();
      if (s.indexOf("rule") !== -1) return "rule";
      if (s.indexOf("classic") !== -1 || s.indexOf("book") !== -1 || s === "co_thu") {
        return "classical";
      }
      if (s.indexOf("reason") !== -1) return "reasoning";
      if (s.indexOf("status") !== -1) return "status";
      return "unknown";
    }

    function mapEvidence(list) {
      return asList(list)
        .map(function (e) {
          if (e == null) return null;
          if (typeof e === "string") {
            return {
              label: e,
              reason: null,
              condition: null,
              source_type: "unknown",
              reference: null,
            };
          }
          if (typeof e !== "object") return null;
          var label =
            e.label || e.text || e.claim || e.summary || e.body || e.name || null;
          if (!label) return null;
          return {
            label: String(label),
            reason: e.reason || e.why || null,
            condition: e.condition || e.when || null,
            source_type: mapSourceType(e.source_type || e.type),
            reference: e.reference || e.source || e.citation || null,
          };
        })
        .filter(Boolean);
    }

    function mapRules(list) {
      return asList(list)
        .map(function (r) {
          if (r == null) return null;
          if (typeof r === "string") {
            return {
              name: r,
              category: null,
              priority: null,
              description: null,
            };
          }
          if (typeof r !== "object") return null;
          var name =
            r.display_name || r.name || r.title || r.rule_name || r.label || null;
          /* Hide bare internal ids */
          if (!name) return null;
          if (/engine|traceback|classname/i.test(String(name))) return null;
          return {
            name: String(name),
            category: r.category || r.group || r.family || null,
            priority: r.priority != null ? r.priority : r.rank != null ? r.rank : null,
            description: r.description || r.reason || r.explanation || null,
          };
        })
        .filter(Boolean);
    }

    function mapClassical(list) {
      return asList(list)
        .map(function (c) {
          if (c == null) return null;
          if (typeof c === "string") {
            return {
              book: c,
              chapter: null,
              section: null,
              passage: null,
              quote: null,
            };
          }
          if (typeof c !== "object") return null;
          var book =
            c.book || c.title || c.name || c.work || c.classical || c.label || null;
          if (!book && !c.quote && !c.excerpt) return null;
          return {
            book: book ? String(book) : null,
            chapter: c.chapter || c.thien || null,
            section: c.section || c.chuong || null,
            passage: c.passage || c.doan || null,
            quote: c.quote || c.excerpt || c.text || null,
          };
        })
        .filter(Boolean);
    }

    function mapRelated(raw) {
      return asList(raw)
        .map(function (x) {
          if (!x || typeof x !== "object") return null;
          var type = String(x.type || x.kind || "").toLowerCase();
          var id = x.id || x.section_id || x.block_id || null;
          if (!id) return null;
          if (type === "analysis" || type === "tier-analysis") {
            return {
              type: "analysis",
              id: String(id),
              label: x.label || x.title || String(id),
              href: "#analysis-" + id,
            };
          }
          if (
            type === "interpretation" ||
            type === "interp" ||
            type === "tier-interpretation"
          ) {
            return {
              type: "interpretation",
              id: String(id),
              label: x.label || x.title || String(id),
              href: "#interp-" + id,
            };
          }
          return null;
        })
        .filter(Boolean);
    }

    function pushBlock(raw, idx) {
      if (!raw || typeof raw !== "object") return;
      var insight =
        raw.insight ||
        raw.conclusion ||
        raw.summary ||
        raw.title ||
        raw.label ||
        null;
      var evidence = mapEvidence(
        raw.evidence || raw.evidences || raw.proofs || raw.claims
      );
      var rules = mapRules(raw.rules || raw.applied_rules || raw.rule_trace);
      var classical = mapClassical(
        raw.classical ||
          raw.classical_references ||
          raw.citations ||
          raw.bibliography
      );
      var knowledgeRef =
        raw.knowledge ||
        raw.knowledge_reference ||
        raw.knowledge_ref ||
        raw.reference ||
        null;
      if (knowledgeRef && typeof knowledgeRef === "object") {
        knowledgeRef =
          knowledgeRef.title ||
          knowledgeRef.label ||
          knowledgeRef.name ||
          null;
      }
      var confidence =
        raw.confidence != null
          ? raw.confidence
          : raw.confidence_score != null
            ? raw.confidence_score
            : null;
      var related = mapRelated(
        raw.related ||
          raw.related_sections ||
          raw.related_analysis ||
          raw.related_interpretation
      );
      if (
        !insight &&
        !evidence.length &&
        !rules.length &&
        !classical.length &&
        !knowledgeRef &&
        confidence == null
      ) {
        return;
      }
      blocks.push({
        id: String(raw.id || raw.key || "kb-" + idx),
        insight: insight ? String(insight) : null,
        summary: raw.description ? String(raw.description) : null,
        evidence: evidence,
        rules: rules,
        knowledge_ref: knowledgeRef ? String(knowledgeRef) : null,
        classical: classical,
        confidence: confidence,
        related: related,
        open: idx < 2,
      });
    }

    var collections = []
      .concat(asList(payload.knowledge_blocks))
      .concat(asList(knowledgeRoot.blocks))
      .concat(asList(knowledgeRoot.insights))
      .concat(asList(ke && ke.blocks))
      .concat(asList(ke && ke.insights))
      .concat(asList(ke && ke.evidence_trace))
      .concat(asList(payload.evidence_trace))
      .concat(asList(payload.traceability));

    collections.forEach(function (item, idx) {
      pushBlock(item, idx);
    });

    /* Honest pattern/score trace block when explicit rules/evidence exist */
    var patternRules = mapRules(pattern.rules || pattern.applied_rules);
    var patternEvidence = mapEvidence(pattern.evidence || pattern.evidences);
    var patternClassical = mapClassical(
      pattern.classical || pattern.citations || payload.classical_references
    );
    if (patternRules.length || patternEvidence.length || patternClassical.length) {
      var insight =
        pattern.cach_cuc ||
        pattern.pattern_name ||
        pattern.insight ||
        null;
      blocks.push({
        id: "pattern-trace",
        insight: insight ? String(insight) : null,
        summary: pattern.summary ? String(pattern.summary) : null,
        evidence: patternEvidence,
        rules: patternRules,
        knowledge_ref: null,
        classical: patternClassical,
        confidence: pattern.confidence != null ? pattern.confidence : null,
        related: mapRelated(pattern.related_sections),
        open: blocks.length === 0,
      });
    }

    /* Status-only knowledge_expert as last resort status block */
    if (!blocks.length && ke) {
      var statusFactors = [];
      Object.keys(ke).forEach(function (k) {
        if (/engine|class|module|traceback/i.test(k)) return;
        var val = ke[k];
        if (val == null || typeof val === "object") return;
        statusFactors.push(k + ": " + String(val));
      });
      blocks.push({
        id: "knowledge-status",
        insight: ke.status != null ? String(ke.status) : null,
        summary: ke.message ? String(ke.message) : null,
        evidence: statusFactors.map(function (s) {
          return {
            label: s,
            reason: null,
            condition: null,
            source_type: "status",
            reference: null,
          };
        }),
        rules: mapRules(ke.rules),
        knowledge_ref: ke.citation || ke.reference || null,
        classical: mapClassical(ke.classical || ke.citations),
        confidence: ke.confidence != null ? ke.confidence : null,
        related: mapRelated(ke.related_sections),
        open: true,
      });
    }

    var filters = {
      source_types: ["rule", "classical", "reasoning", "status", "unknown"],
    };

    return {
      blocks: blocks,
      status: ke,
      filters: filters,
      hasExpert: true,
    };
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
    var elementPack = elementSeries(score, pillars, summary && summary.wuxing);
    var elements = elementPack.series;
    var tenGodsFromScore = namedSeries(score, [
      "ten_god_series",
      "ten_gods",
      "thap_than",
      "ten_god_scores",
      "shi_shen",
    ]);
    var tenGods = tenGodSeries(
      pillars,
      tenGodsFromScore || (summary && summary.ten_gods) || []
    );
    var tenGodSource =
      tenGodsFromScore && tenGodsFromScore.length
        ? "score"
        : tenGods.length
          ? "pillars"
          : "none";
    var gauge = strengthGaugeValue(overview, score, payload);
    var relations = relationsUnavailable(payload);
    var knowledge = payload.knowledge_expert || null;
    var quality = qualityLabel(score, interpretation);
    var thanLabel = strengthClassLabel(payload, overview);
    var wuxingScalar = pick(score, ["wuxing_score"]);
    if (wuxingScalar == null && summary && summary.wuxing && summary.wuxing.length === 1) {
      wuxingScalar = summary.wuxing[0].value;
    }

    var analysisBlocks = buildAnalysisBlocks({
      elements: elements,
      tenGods: tenGods,
      overview: overview,
      relations: relations,
      shensha: (summary && summary.shensha) || [],
      knowledge: knowledge,
      pattern: payload.pattern || null,
      score: score,
      interpretation: interpretation,
      payload: payload,
    });
    var interpretationDocument = buildInterpretationDocument(interpretation);
    var knowledgeWorkspace = buildKnowledgeWorkspace(
      payload,
      analysisBlocks,
      interpretationDocument.chapters
    );

    return {
      input: input,
      summary: summary,
      executive: {
        day_master: present(dm.stem),
        element: present(dm.element),
        yin_yang: present(dm.yin_yang),
        than: thanLabel,
        strengths: strengths,
        weaknesses: weaknesses,
        dung_than: present(overview.dung_than),
        hy_than: present(overview.hy_than),
        ky_than: present(overview.ky_than),
        cach_cuc: present(overview.cach_cuc),
        quality: quality,
        quality_verdict: qualityVerdict(score, interpretation),
        first_recommendation: firstRecommendation(score, interpretation),
        sentence: summarySentence(dm, overview),
      },
      pillars: pillarColumns(pillars),
      charts: {
        elements: elements,
        elements_source: elementPack.source,
        ten_gods: tenGods,
        ten_gods_source: tenGodSource,
        strength_gauge: gauge,
        than_label: thanLabel,
        quality: quality,
        wuxing_score:
          wuxingScalar != null && Number.isFinite(Number(wuxingScalar))
            ? Number(wuxingScalar)
            : null,
        insights: {
          elements: chartInsightText(interpretation, [
            "five_element",
            "ngu_hanh",
            "wuxing",
            "element",
          ]),
          strength: chartInsightText(interpretation, [
            "strength",
            "than",
            "body",
          ]),
          ten_gods: chartInsightText(interpretation, [
            "ten_god",
            "thap_than",
            "shi_shen",
          ]),
        },
      },
      analysis: {
        elements: elements,
        ten_gods: tenGods,
        shensha: (summary && summary.shensha) || [],
        overview: overview,
        relations: relations,
        knowledge_status: knowledge,
        pattern: payload.pattern || null,
        blocks: analysisBlocks,
      },
      interpretation: {
        confidence:
          interpretation.confidence != null
            ? present(interpretation.confidence)
            : MISSING,
        document: interpretationDocument,
        chapters: interpretationDocument.chapters,
      },
      knowledge: {
        status: knowledge,
        narrative: payload.narrative || payload.report || null,
        validation_hint: payload.knowledge_expert || null,
        blocks: knowledgeWorkspace.blocks,
        filters: knowledgeWorkspace.filters,
        hasExpert: knowledgeWorkspace.hasExpert,
      },
      raw: payload,
    };
  }

  global.BteReportModel = {
    build: buildReportModel,
    MISSING: MISSING,
  };
})(typeof window !== "undefined" ? window : globalThis);
