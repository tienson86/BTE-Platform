/**
 * Phase 2 report HTML renderers — 6 tiers (presentation only).
 */
(function (global) {
  var MISSING = "--";

  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  function esc(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function icon(name) {
    var I = window.BteReportIcons;
    if (!I || typeof I[name] !== "function") return "";
    return I[name]();
  }

  function show(v) {
    if (v === null || v === undefined || v === "") return MISSING;
    return String(v);
  }

  function listOrMissing(items) {
    if (!items || !items.length) {
      return '<p class="rpt-caption">' + esc(MISSING) + "</p>";
    }
    return (
      "<ul class=\"rpt-list\">" +
      items
        .map(function (x) {
          return "<li>" + esc(show(x)) + "</li>";
        })
        .join("") +
      "</ul>"
    );
  }

  function unavailable(title) {
    return (
      '<div class="rpt-unavailable">' +
      '<div class="rpt-subtitle">' +
      esc(title) +
      "</div>" +
      '<p class="rpt-caption">' +
      esc(t("report.unavailable")) +
      "</p></div>"
    );
  }

  function metric(label, value, accent) {
    return (
      '<div class="rpt-metric' +
      (accent ? " rpt-accent-" + accent : "") +
      '">' +
      '<div class="rpt-caption">' +
      esc(label) +
      "</div>" +
      '<div class="rpt-metric-value">' +
      esc(show(value)) +
      "</div></div>"
    );
  }

  function slotUnavailable(value) {
    return value === null || value === undefined || value === "" || value === MISSING;
  }

  function metricSlot(label, value, accent) {
    var missing = slotUnavailable(value);
    return (
      '<div class="rpt-metric' +
      (accent ? " rpt-accent-" + accent : "") +
      (missing ? " rpt-metric-unavailable" : "") +
      '" role="group" aria-label="' +
      esc(label) +
      '">' +
      '<div class="rpt-caption">' +
      esc(label) +
      "</div>" +
      '<div class="rpt-metric-value' +
      (missing ? " rpt-slot-unavailable" : "") +
      '">' +
      esc(missing ? t("report.unavailable") : String(value)) +
      "</div></div>"
    );
  }

  function renderDayMasterDisplay(ex) {
    var missing = slotUnavailable(ex.day_master);
    var metaParts = [];
    if (!slotUnavailable(ex.element)) metaParts.push(ex.element);
    if (!slotUnavailable(ex.yin_yang)) metaParts.push(ex.yin_yang);
    var meta =
      metaParts.length > 0
        ? metaParts.join(" · ")
        : missing
          ? ""
          : MISSING;
    return (
      '<div class="rpt-hero-dm rpt-accent-day" data-component="DayMasterDisplay">' +
      icon("dayMaster") +
      "<div>" +
      '<div class="rpt-caption">' +
      esc(t("bazi.day_master")) +
      "</div>" +
      (missing
        ? '<div class="rpt-hero-dm-value rpt-slot-unavailable" aria-live="polite">' +
          esc(t("report.unavailable")) +
          "</div>"
        : '<div class="rpt-hero-dm-value">' +
          esc(String(ex.day_master)) +
          "</div>") +
      (meta
        ? '<div class="rpt-caption">' + esc(meta) + "</div>"
        : "") +
      "</div></div>"
    );
  }

  function renderQualityVerdictCaption(ex) {
    var v = ex.quality_verdict || {};
    if (!v.available || !v.caption) {
      return (
        '<div class="rpt-quality-verdict rpt-unavailable" data-component="QualityVerdictCaption" role="status">' +
        '<p class="rpt-caption">' +
        esc(t("report.quality")) +
        "</p>" +
        '<p class="rpt-body">' +
        esc(t("report.unavailable")) +
        "</p></div>"
      );
    }
    return (
      '<div class="rpt-quality-verdict' +
      (v.band ? " rpt-quality-" + esc(v.band) : "") +
      '" data-component="QualityVerdictCaption" role="status">' +
      '<p class="rpt-caption">' +
      esc(t("report.quality")) +
      "</p>" +
      '<p class="rpt-quality-verdict-text">' +
      esc(v.caption) +
      "</p></div>"
    );
  }

  function renderFirstRecommendation(ex) {
    var text = ex.first_recommendation;
    if (!text) {
      return (
        '<aside class="rpt-first-rec rpt-unavailable" data-component="FirstRecommendation" aria-label="' +
        esc(t("report.first_recommendation")) +
        '">' +
        '<div class="rpt-subtitle">' +
        esc(t("report.first_recommendation")) +
        "</div>" +
        '<p class="rpt-caption">' +
        esc(t("report.unavailable")) +
        "</p></aside>"
      );
    }
    return (
      '<aside class="rpt-first-rec" data-component="FirstRecommendation" aria-label="' +
      esc(t("report.first_recommendation")) +
      '">' +
      '<div class="rpt-subtitle">' +
      esc(t("report.first_recommendation")) +
      "</div>" +
      '<p class="rpt-body">' +
      esc(String(text)) +
      "</p></aside>"
    );
  }

  function largeSection(id, title, body, opts) {
    opts = opts || {};
    var collapsed = opts.collapsed ? "true" : "false";
    return (
      '<section class="rpt-large-card" id="' +
      esc(id) +
      '" data-collapsed="' +
      collapsed +
      '">' +
      '<header class="rpt-large-head">' +
      '<div><h3 class="rpt-subtitle">' +
      esc(title) +
      "</h3>" +
      (opts.hint
        ? '<p class="rpt-caption">' + esc(opts.hint) + "</p>"
        : "") +
      "</div>" +
      '<button type="button" class="secondary rpt-collapse-btn" data-rpt-collapse aria-expanded="' +
      (collapsed === "true" ? "false" : "true") +
      '">' +
      icon("chevron") +
      "</button></header>" +
      '<div class="rpt-large-body">' +
      body +
      "</div></section>"
    );
  }

  function tierWrap(id, title, iconName, body) {
    return (
      '<section class="rpt-tier" id="' +
      esc(id) +
      '" data-tier="' +
      esc(id) +
      '">' +
      '<header class="rpt-tier-head">' +
      icon(iconName) +
      '<div><h2 class="rpt-title">' +
      esc(title) +
      '</h2><p class="rpt-caption">' +
      esc(t("report.tier_hint." + id.replace("tier-", ""))) +
      "</p></div></header>" +
      '<div class="rpt-tier-body">' +
      body +
      "</div></section>"
    );
  }

  function renderExecutive(model) {
    var ex = model.executive || {};
    var body =
      '<div class="rpt-hero" data-component="ExecutiveHero">' +
      '<div class="rpt-hero-main">' +
      '<p class="rpt-eyebrow">' +
      esc(t("report.executive_eyebrow")) +
      "</p>" +
      renderDayMasterDisplay(ex) +
      renderQualityVerdictCaption(ex) +
      '<p class="rpt-body rpt-hero-sentence">' +
      esc(ex.sentence || t("report.summary_fallback")) +
      "</p></div>" +
      '<div class="rpt-hero-grid" data-component="SummaryMetricRow">' +
      metricSlot(t("report.than"), ex.than, "than") +
      metricSlot(t("executive.dung_than"), ex.dung_than, "dung") +
      metricSlot(t("executive.hy_than"), ex.hy_than, "hy") +
      metricSlot(t("executive.ky_than"), ex.ky_than, "ky") +
      metricSlot(t("executive.cach_cuc"), ex.cach_cuc, null) +
      metricSlot(t("report.quality"), ex.quality, null) +
      "</div>" +
      '<div class="rpt-hero-sw" data-component="StrengthWeaknessPanel">' +
      '<div class="rpt-hero-panel"><div class="rpt-subtitle">' +
      esc(t("report.strengths")) +
      "</div>" +
      listOrMissing(ex.strengths) +
      '</div><div class="rpt-hero-panel"><div class="rpt-subtitle">' +
      esc(t("report.weaknesses")) +
      "</div>" +
      listOrMissing(ex.weaknesses) +
      "</div></div>" +
      renderFirstRecommendation(ex) +
      "</div>";
    return tierWrap("tier-executive", t("report.tier.executive"), "spark", body);
  }

  function renderPillars(model) {
    var cols = model.pillars || [];
    var body =
      window.BtePillars && typeof window.BtePillars.render === "function"
        ? window.BtePillars.render(cols)
        : '<p class="rpt-caption">' + esc(t("report.unavailable")) + "</p>";
    return tierWrap("tier-bazi", t("report.tier.bazi"), "pillar", body);
  }

  function row(label, value) {
    return (
      '<div class="rpt-pillar-row"><span class="rpt-caption">' +
      esc(label) +
      '</span><span class="rpt-body">' +
      esc(show(value)) +
      "</span></div>"
    );
  }

  function renderCharts(model) {
    var body =
      window.BteMetrics && typeof window.BteMetrics.render === "function"
        ? window.BteMetrics.render(model)
        : '<p class="rpt-caption">' + esc(t("report.unavailable")) + "</p>";
    return tierWrap("tier-charts", t("report.tier.charts"), "chart", body);
  }

  function formatRelation(relations) {
    var labels = [
      { key: "hop", title: t("report.rel_hop") },
      { key: "xung", title: t("report.rel_xung") },
      { key: "hinh", title: t("report.rel_hinh") },
      { key: "hai", title: t("report.rel_hai") },
      { key: "pha", title: t("report.rel_pha") },
    ];
    var any = false;
    var html = labels
      .map(function (row) {
        var v = relations && relations[row.key];
        if (v == null) {
          return (
            '<div class="rpt-rel-row"><strong>' +
            esc(row.title) +
            '</strong><span class="rpt-caption">' +
            esc(t("report.unavailable")) +
            "</span></div>"
          );
        }
        any = true;
        var text =
          typeof v === "object" ? JSON.stringify(v) : String(v);
        return (
          '<div class="rpt-rel-row"><strong>' +
          esc(row.title) +
          "</strong><span>" +
          esc(text) +
          "</span></div>"
        );
      })
      .join("");
    return { html: html, any: any };
  }

  function renderAnalysis(model) {
    var body =
      window.BteAnalysis && typeof window.BteAnalysis.render === "function"
        ? window.BteAnalysis.render(model)
        : '<p class="rpt-caption">' + esc(t("report.unavailable")) + "</p>";
    return tierWrap("tier-analysis", t("report.tier.analysis"), "analyze", body);
  }

  function renderInterpretation(model) {
    var body =
      window.BteInterpretationDoc &&
      typeof window.BteInterpretationDoc.render === "function"
        ? window.BteInterpretationDoc.render(model)
        : '<p class="rpt-caption">' + esc(t("report.unavailable")) + "</p>";
    return tierWrap(
      "tier-interpretation",
      t("report.tier.interpretation"),
      "book",
      body
    );
  }

  function renderKnowledge(model) {
    var k = model.knowledge || {};
    var workspaceHtml =
      window.BteKnowledge && typeof window.BteKnowledge.render === "function"
        ? window.BteKnowledge.render(model)
        : unavailable(t("report.tier.knowledge"));

    var discussHtml = "";
    if (window.BtePresenters && typeof window.BtePresenters.discussion === "function") {
      discussHtml = window.BtePresenters.discussion(k.narrative, {
        data: model.raw,
        input: model.input,
      });
    } else {
      discussHtml = unavailable(t("report.tier.knowledge"));
    }

    var body =
      workspaceHtml +
      largeSection(
        "knowledge-expert",
        t("report.knowledge_expert"),
        discussHtml,
        { hint: t("report.knowledge_expert_hint") }
      );

    return tierWrap("tier-knowledge", t("report.tier.knowledge"), "knowledge", body);
  }

  function renderRail() {
    var items = [
      { id: "tier-executive", key: "executive", icon: "spark" },
      { id: "tier-bazi", key: "bazi", icon: "pillar" },
      { id: "tier-charts", key: "charts", icon: "chart" },
      { id: "tier-analysis", key: "analysis", icon: "analyze" },
      { id: "tier-interpretation", key: "interpretation", icon: "book" },
      { id: "tier-knowledge", key: "knowledge", icon: "knowledge" },
    ];
    return (
      '<nav class="rpt-rail" aria-label="' +
      esc(t("report.nav_aria")) +
      '"><div class="rpt-rail-title">' +
      esc(t("report.nav_title")) +
      "</div><ol class=\"rpt-rail-list\">" +
      items
        .map(function (it, idx) {
          return (
            '<li><a class="rpt-rail-link' +
            (idx === 0 ? " is-active" : "") +
            '" href="#' +
            esc(it.id) +
            '" data-rpt-nav="' +
            esc(it.id) +
            '">' +
            icon(it.icon) +
            "<span>" +
            esc(t("report.tier." + it.key)) +
            "</span></a></li>"
          );
        })
        .join("") +
      "</ol></nav>"
    );
  }

  function renderReport(model) {
    return (
      '<div class="rpt-shell">' +
      renderRail() +
      '<div class="rpt-main">' +
      renderExecutive(model) +
      renderPillars(model) +
      renderCharts(model) +
      renderAnalysis(model) +
      renderInterpretation(model) +
      renderKnowledge(model) +
      "</div></div>"
    );
  }

  function bindReportInteractions(root) {
    if (!root) return;
    root.querySelectorAll("[data-rpt-collapse]").forEach(function (btn) {
      if (btn.__rptBound) return;
      btn.__rptBound = true;
      btn.addEventListener("click", function () {
        var card = btn.closest(".rpt-large-card");
        if (!card) return;
        var collapsed = card.getAttribute("data-collapsed") === "true";
        card.setAttribute("data-collapsed", collapsed ? "false" : "true");
        btn.setAttribute("aria-expanded", collapsed ? "true" : "false");
      });
    });
    if (window.BteUI && window.BteUI.bindCollapsible) window.BteUI.bindCollapsible(root);
    if (window.BtePillars && typeof window.BtePillars.bind === "function") {
      window.BtePillars.bind(root);
    }
    if (window.BteAnalysis && typeof window.BteAnalysis.bind === "function") {
      window.BteAnalysis.bind(root);
    }
    if (
      window.BteInterpretationDoc &&
      typeof window.BteInterpretationDoc.bind === "function"
    ) {
      window.BteInterpretationDoc.bind(root);
    }
    if (window.BteKnowledge && typeof window.BteKnowledge.bind === "function") {
      window.BteKnowledge.bind(root, root.__rptModel || null);
    }
  }

  global.BteReportRender = {
    render: renderReport,
    bind: bindReportInteractions,
    tiers: {
      executive: renderExecutive,
      bazi: renderPillars,
      charts: renderCharts,
      analysis: renderAnalysis,
      interpretation: renderInterpretation,
      knowledge: renderKnowledge,
    },
  };
})(typeof window !== "undefined" ? window : globalThis);
