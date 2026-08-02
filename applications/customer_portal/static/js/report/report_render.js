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
      '<div class="rpt-hero">' +
      '<div class="rpt-hero-main">' +
      '<p class="rpt-eyebrow">' +
      esc(t("report.executive_eyebrow")) +
      "</p>" +
      '<div class="rpt-hero-dm rpt-accent-day">' +
      icon("dayMaster") +
      '<div><div class="rpt-caption">' +
      esc(t("bazi.day_master")) +
      '</div><div class="rpt-hero-dm-value">' +
      esc(show(ex.day_master)) +
      '</div><div class="rpt-caption">' +
      esc(show(ex.element) + " · " + show(ex.yin_yang)) +
      "</div></div></div>" +
      '<p class="rpt-body rpt-hero-sentence">' +
      esc(ex.sentence) +
      "</p></div>" +
      '<div class="rpt-hero-grid">' +
      metric(t("report.than"), ex.than, "than") +
      metric(t("executive.dung_than"), ex.dung_than, "dung") +
      metric(t("executive.hy_than"), ex.hy_than, "hy") +
      metric(t("executive.ky_than"), ex.ky_than, "ky") +
      metric(t("executive.cach_cuc"), ex.cach_cuc, null) +
      metric(t("report.quality"), ex.quality, null) +
      "</div>" +
      '<div class="rpt-hero-sw">' +
      '<div class="rpt-hero-panel"><div class="rpt-subtitle">' +
      esc(t("report.strengths")) +
      "</div>" +
      listOrMissing(ex.strengths) +
      '</div><div class="rpt-hero-panel"><div class="rpt-subtitle">' +
      esc(t("report.weaknesses")) +
      "</div>" +
      listOrMissing(ex.weaknesses) +
      "</div></div></div>";
    return tierWrap("tier-executive", t("report.tier.executive"), "spark", body);
  }

  function renderPillars(model) {
    var cols = model.pillars || [];
    var body =
      '<div class="rpt-pillars">' +
      cols
        .map(function (col) {
          return (
            '<article class="rpt-pillar' +
            (col.isDay ? " rpt-pillar-day rpt-accent-day" : "") +
            '">' +
            '<div class="rpt-pillar-label">' +
            icon("pillar") +
            "<span>" +
            esc(col.label) +
            (col.isDay ? " · " + esc(t("bazi.day_master")) : "") +
            "</span></div>" +
            '<div class="rpt-pillar-stem">' +
            esc(show(col.stem)) +
            "</div>" +
            '<div class="rpt-pillar-branch">' +
            esc(show(col.branch)) +
            "</div>" +
            '<div class="rpt-pillar-rows">' +
            row(t("bazi.hidden"), col.hidden) +
            row(t("bazi.ten_god"), col.ten_god) +
            row(t("bazi.chang_sheng"), col.chang_sheng) +
            row(t("bazi.nap_am"), col.nap_am) +
            "</div></article>"
          );
        })
        .join("") +
      "</div>";
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
    var C = window.BteReportCharts || {};
    var charts = model.charts || {};
    var strengthLabel = show((model.executive && model.executive.than) || MISSING);
    var body =
      '<div class="rpt-charts-grid">' +
      '<div class="rpt-chart-card"><div class="rpt-subtitle">' +
      esc(t("report.chart_radar")) +
      "</div>" +
      (C.radar
        ? C.radar(charts.elements, t("report.unavailable"))
        : "") +
      '</div><div class="rpt-chart-card"><div class="rpt-subtitle">' +
      esc(t("report.chart_gauge")) +
      "</div>" +
      (charts.strength_gauge != null && C.gauge
        ? C.gauge(charts.strength_gauge, t("report.than"), t("report.unavailable"))
        : '<div class="rpt-chart-empty"><div class="rpt-metric-value">' +
          esc(strengthLabel) +
          '</div><p class="rpt-caption">' +
          esc(t("report.gauge_text_only")) +
          "</p></div>") +
      '</div><div class="rpt-chart-card"><div class="rpt-subtitle">' +
      esc(t("report.chart_elements")) +
      "</div>" +
      (C.bars ? C.bars(charts.elements, t("report.unavailable")) : "") +
      '</div><div class="rpt-chart-card"><div class="rpt-subtitle">' +
      esc(t("report.chart_gods")) +
      "</div>" +
      (C.bars ? C.bars(charts.ten_gods, t("report.unavailable")) : "") +
      "</div></div>";
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
    var a = model.analysis || {};
    var ov = a.overview || {};
    var C = window.BteReportCharts || {};
    var rel = formatRelation(a.relations || {});
    var knowledgeBody = a.knowledge_status
      ? '<pre class="rpt-pre">' +
        esc(JSON.stringify(a.knowledge_status, null, 2)) +
        "</pre>"
      : unavailable(t("report.knowledge_status"));

    var body =
      largeSection(
        "analysis-elements",
        t("report.an_elements"),
        C.bars
          ? C.bars(a.elements, t("report.unavailable"))
          : unavailable(t("report.an_elements")),
        { hint: t("report.an_elements_hint") }
      ) +
      largeSection(
        "analysis-gods",
        t("report.an_gods"),
        C.bars
          ? C.bars(a.ten_gods, t("report.unavailable"))
          : listOrMissing(
              (a.ten_gods || []).map(function (x) {
                return x.label + ": " + x.value;
              })
            ),
        { hint: t("report.an_gods_hint") }
      ) +
      largeSection(
        "analysis-pattern",
        t("report.an_pattern"),
        '<div class="rpt-hero-grid">' +
          metric(t("executive.cach_cuc"), ov.cach_cuc) +
          metric(t("executive.tong_cach"), ov.tong_cach) +
          metric(t("report.than"), ov.than_strength || ov.than, "than") +
          "</div>",
        { hint: t("report.an_pattern_hint") }
      ) +
      largeSection(
        "analysis-useful",
        t("report.an_useful"),
        '<div class="rpt-hero-grid">' +
          metric(t("executive.dung_than"), ov.dung_than, "dung") +
          metric(t("executive.hy_than"), ov.hy_than, "hy") +
          metric(t("executive.ky_than"), ov.ky_than, "ky") +
          metric(t("executive.dieu_hau"), ov.dieu_hau) +
          "</div>",
        { hint: t("report.an_useful_hint") }
      ) +
      largeSection(
        "analysis-relations",
        t("report.an_relations"),
        rel.html,
        { hint: t("report.an_relations_hint"), collapsed: true }
      ) +
      largeSection(
        "analysis-shensha",
        t("report.an_shensha"),
        a.shensha && a.shensha.length
          ? listOrMissing(a.shensha)
          : unavailable(t("report.an_shensha")),
        { collapsed: true }
      ) +
      largeSection(
        "analysis-knowledge",
        t("report.an_priority_knowledge"),
        knowledgeBody,
        { collapsed: true }
      );

    return tierWrap("tier-analysis", t("report.tier.analysis"), "analyze", body);
  }

  function renderInterpretation(model) {
    var chapters = (model.interpretation && model.interpretation.chapters) || [];
    var conf = model.interpretation && model.interpretation.confidence;
    var body =
      '<div class="rpt-interp-meta"><span class="rpt-caption">' +
      esc(t("interpretation.confidence", { value: show(conf) })) +
      "</span></div>" +
      chapters
        .map(function (ch) {
          var content = ch.available
            ? '<div class="rpt-body">' +
              esc(ch.body).replace(/\n/g, "<br>") +
              "</div>"
            : unavailable(t(ch.titleKey));
          return largeSection(
            "interp-" + ch.id,
            t(ch.titleKey),
            content,
            { collapsed: !ch.available }
          );
        })
        .join("");
    return tierWrap(
      "tier-interpretation",
      t("report.tier.interpretation"),
      "book",
      body
    );
  }

  function renderKnowledge(model) {
    var k = model.knowledge || {};
    var statusHtml = k.status
      ? '<div class="rpt-knowledge-status"><div class="rpt-subtitle">' +
        esc(t("report.knowledge_status")) +
        '</div><pre class="rpt-pre">' +
        esc(JSON.stringify(k.status, null, 2)) +
        "</pre></div>"
      : unavailable(t("report.knowledge_status"));

    var discussHtml = "";
    if (window.BtePresenters && typeof BtePresenters.discussion === "function") {
      discussHtml = BtePresenters.discussion(k.narrative, {
        data: model.raw,
        input: model.input,
      });
    } else {
      discussHtml = unavailable(t("report.tier.knowledge"));
    }

    var body =
      largeSection("knowledge-sources", t("report.knowledge_sources"), statusHtml) +
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
    if (window.BteUI && BteUI.bindCollapsible) BteUI.bindCollapsible(root);
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
