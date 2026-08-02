/**
 * Tier 3 — Metrics & Visual Analytics workspace (Blueprint V1.1).
 * Insight-first charts. Presentation only — no invented analytics.
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

  function unavailable(v) {
    return v === null || v === undefined || v === "" || v === MISSING;
  }

  function show(v) {
    return unavailable(v) ? MISSING : String(v);
  }

  function TooltipInfo(text) {
    if (!text) return "";
    return (
      '<button type="button" class="mx-tip" data-component="TooltipInfo" title="' +
      esc(text) +
      '" aria-label="' +
      esc(text) +
      '">i</button>'
    );
  }

  function panelShell(opts) {
    opts = opts || {};
    var empty = !!opts.empty;
    var insightHtml = opts.insight
      ? '<p class="mx-insight rpt-body">' + esc(opts.insight) + "</p>"
      : empty
        ? ""
        : '<p class="mx-insight rpt-caption">' +
          esc(t("report.chart_insight_none")) +
          "</p>";
    return (
      '<section class="mx-panel' +
      (empty ? " mx-panel-empty" : "") +
      '" data-component="' +
      esc(opts.component || "InsightPanel") +
      '" tabindex="0" aria-label="' +
      esc(opts.title || "") +
      '">' +
      '<header class="mx-panel-head">' +
      "<div>" +
      '<h3 class="rpt-subtitle">' +
      esc(opts.title) +
      "</h3>" +
      '<p class="rpt-caption mx-desc">' +
      esc(opts.description || "") +
      "</p></div>" +
      TooltipInfo(opts.tooltip) +
      "</header>" +
      insightHtml +
      '<div class="mx-panel-body mx-visual">' +
      (opts.body || "") +
      "</div>" +
      (opts.altText
        ? '<p class="mx-alt visually-hidden">' + esc(opts.altText) + "</p>"
        : "") +
      "</section>"
    );
  }

  function MetricCard(metric) {
    var missing = unavailable(metric.value);
    return (
      '<div class="mx-metric' +
      (missing ? " mx-metric-miss" : "") +
      '" data-component="MetricCard" role="group" aria-label="' +
      esc(metric.label) +
      '" title="' +
      esc(metric.label + ": " + show(metric.value)) +
      '">' +
      '<div class="rpt-caption">' +
      esc(metric.label) +
      "</div>" +
      '<div class="mx-metric-value">' +
      esc(show(metric.value)) +
      "</div>" +
      (metric.hint
        ? '<div class="rpt-caption">' + esc(metric.hint) + "</div>"
        : "") +
      "</div>"
    );
  }

  function SummaryMetricGrid(charts) {
    var metrics = [
      {
        label: t("report.than"),
        value: charts.than_label,
        hint: t("report.chart_metric_than_hint"),
      },
      {
        label: t("report.quality"),
        value: charts.quality,
        hint: t("report.chart_metric_quality_hint"),
      },
    ];
    if (charts.wuxing_score != null && Number.isFinite(Number(charts.wuxing_score))) {
      metrics.push({
        label: t("report.chart_metric_wuxing"),
        value: charts.wuxing_score,
        hint: t("report.chart_metric_wuxing_hint"),
      });
    }
    if (charts.strength_gauge != null && Number.isFinite(Number(charts.strength_gauge))) {
      metrics.push({
        label: t("report.chart_metric_strength_score"),
        value: Math.round(Number(charts.strength_gauge)),
        hint: t("report.chart_metric_strength_hint"),
      });
    }
    return (
      '<div class="mx-metrics" data-component="SummaryMetricGrid">' +
      '<div class="mx-metrics-head">' +
      '<h3 class="rpt-subtitle">' +
      esc(t("report.chart_metrics_title")) +
      "</h3>" +
      '<p class="rpt-caption">' +
      esc(t("report.chart_metrics_desc")) +
      "</p></div>" +
      '<div class="mx-metrics-grid">' +
      metrics.map(MetricCard).join("") +
      "</div></div>"
    );
  }

  function sourceLabel(key) {
    if (key === "score") return t("report.chart_source_score");
    if (key === "pillars") return t("report.chart_source_pillars");
    return t("report.unavailable");
  }

  function seriesAlt(items, title) {
    if (!items || !items.length) return title + ": " + t("report.unavailable");
    return (
      title +
      ": " +
      items
        .map(function (it) {
          return it.label + " " + it.value;
        })
        .join(", ")
    );
  }

  function StrengthGauge(charts) {
    var C = window.BteReportCharts || {};
    var gauge = charts.strength_gauge;
    var empty = gauge == null || !Number.isFinite(Number(gauge));
    var body;
    if (empty) {
      body =
        '<div class="rpt-chart-empty" data-component="ChartEmpty">' +
        '<div class="rpt-metric-value">' +
        esc(show(charts.than_label)) +
        '</div><p class="rpt-caption">' +
        esc(t("report.gauge_text_only")) +
        "</p></div>";
    } else {
      body = C.gauge
        ? C.gauge(gauge, t("report.than"), t("report.unavailable"))
        : "";
    }
    return panelShell({
      component: "StrengthGauge",
      title: t("report.chart_gauge"),
      description: t("report.chart_gauge_desc"),
      source: empty
        ? sourceLabel(unavailable(charts.than_label) ? "none" : "score")
        : t("report.chart_source_score"),
      tooltip: t("report.chart_gauge_tip"),
      insight: charts.insights && charts.insights.strength,
      empty: empty && unavailable(charts.than_label),
      body: body,
      altText: empty
        ? t("report.than") + ": " + show(charts.than_label)
        : t("report.chart_gauge") + ": " + Math.round(Number(gauge)),
    });
  }

  function ElementDistribution(charts) {
    var C = window.BteReportCharts || {};
    var series = charts.elements || [];
    var empty = !series.length;
    var body = empty
      ? '<div class="rpt-chart-empty">' +
        esc(t("report.unavailable")) +
        "</div>"
      : '<div class="mx-element-split">' +
        '<div class="mx-element-radar">' +
        (C.radar ? C.radar(series, t("report.unavailable")) : "") +
        "</div>" +
        '<div class="mx-element-bars">' +
        (C.bars ? C.bars(series, t("report.unavailable")) : "") +
        "</div></div>";
    return panelShell({
      component: "ElementDistribution",
      title: t("report.chart_elements"),
      description: t("report.chart_elements_desc"),
      source: sourceLabel(charts.elements_source),
      tooltip: t("report.chart_elements_tip"),
      insight: charts.insights && charts.insights.elements,
      empty: empty,
      body: body,
      altText: seriesAlt(series, t("report.chart_elements")),
    });
  }

  function TenGodDistribution(charts) {
    var C = window.BteReportCharts || {};
    var series = charts.ten_gods || [];
    var empty = !series.length;
    var body = empty
      ? '<div class="rpt-chart-empty">' +
        esc(t("report.unavailable")) +
        "</div>"
      : C.bars
        ? C.bars(series, t("report.unavailable"))
        : "";
    return panelShell({
      component: "TenGodDistribution",
      title: t("report.chart_gods"),
      description: t("report.chart_gods_desc"),
      source: sourceLabel(charts.ten_gods_source),
      tooltip: t("report.chart_gods_tip"),
      insight: charts.insights && charts.insights.ten_gods,
      empty: empty,
      body: body,
      altText: seriesAlt(series, t("report.chart_gods")),
    });
  }

  function MetricsWorkspace(model) {
    var charts = (model && model.charts) || {};
    var lead =
      (charts.insights &&
        (charts.insights.strength ||
          charts.insights.elements ||
          charts.insights.ten_gods)) ||
      t("report.chart_workspace_hint");
    return (
      '<div class="mx-workspace" data-component="MetricsWorkspace">' +
      '<p class="mx-lead rpt-body">' +
      esc(lead) +
      "</p>" +
      '<div class="mx-stack">' +
      StrengthGauge(charts) +
      ElementDistribution(charts) +
      TenGodDistribution(charts) +
      "</div></div>"
    );
  }

  global.BteMetrics = {
    render: MetricsWorkspace,
    components: {
      MetricsWorkspace: MetricsWorkspace,
      SummaryMetricGrid: SummaryMetricGrid,
      MetricCard: MetricCard,
      StrengthGauge: StrengthGauge,
      ElementDistribution: ElementDistribution,
      TenGodDistribution: TenGodDistribution,
      TooltipInfo: TooltipInfo,
    },
  };
})(typeof window !== "undefined" ? window : globalThis);
