/**
 * Pure SVG chart helpers for Phase 2 report (no npm).
 */
(function (global) {
  function esc(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function emptyChart(label) {
    return (
      '<div class="rpt-chart-empty"><span class="rpt-caption">' +
      esc(label || "--") +
      "</span></div>"
    );
  }

  /**
   * @param {{label:string,value:number}[]} items
   * @param {string} [emptyLabel]
   */
  function radar(items, emptyLabel) {
    if (!items || !items.length) return emptyChart(emptyLabel);
    var n = items.length;
    var cx = 100;
    var cy = 100;
    var r = 72;
    var max = 0;
    items.forEach(function (it) {
      var v = Math.abs(Number(it.value) || 0);
      if (v > max) max = v;
    });
    if (max <= 0) max = 1;

    function pt(i, scale) {
      var angle = (-Math.PI / 2) + (i * 2 * Math.PI) / n;
      return {
        x: cx + Math.cos(angle) * r * scale,
        y: cy + Math.sin(angle) * r * scale,
      };
    }

    var grid = [0.25, 0.5, 0.75, 1]
      .map(function (s) {
        var pts = [];
        for (var i = 0; i < n; i++) {
          var p = pt(i, s);
          pts.push(p.x.toFixed(1) + "," + p.y.toFixed(1));
        }
        return '<polygon class="rpt-radar-grid" points="' + pts.join(" ") + '"/>';
      })
      .join("");

    var dataPts = [];
    var labels = "";
    for (var i = 0; i < n; i++) {
      var scale = Math.min(1, Math.abs(Number(items[i].value) || 0) / max);
      var p = pt(i, scale);
      dataPts.push(p.x.toFixed(1) + "," + p.y.toFixed(1));
      var lp = pt(i, 1.18);
      labels +=
        '<text class="rpt-radar-label" x="' +
        lp.x.toFixed(1) +
        '" y="' +
        lp.y.toFixed(1) +
        '" text-anchor="middle" dominant-baseline="middle">' +
        esc(items[i].label) +
        "</text>";
    }

    return (
      '<div class="rpt-chart rpt-chart-radar">' +
      '<svg viewBox="0 0 200 200" role="img" aria-label="' +
      esc(
        items
          .map(function (it) {
            return it.label + " " + it.value;
          })
          .join(", ")
      ) +
      '" tabindex="0">' +
      grid +
      '<polygon class="rpt-radar-fill" points="' +
      dataPts.join(" ") +
      '"/>' +
      labels +
      "</svg></div>"
    );
  }

  /**
   * Gauge 0–100 for body strength / quality.
   * @param {number|null} value
   * @param {string} label
   * @param {string} [emptyLabel]
   */
  function gauge(value, label, emptyLabel) {
    var n = Number(value);
    if (!Number.isFinite(n)) return emptyChart(emptyLabel);
    n = Math.max(0, Math.min(100, n));
    var r = 54;
    var cx = 70;
    var cy = 68;
    var start = Math.PI;
    var end = 0;
    function polar(a) {
      return { x: cx + Math.cos(a) * r, y: cy + Math.sin(a) * r };
    }
    var a0 = start;
    var a1 = start + (end - start) * (n / 100);
    var p0 = polar(a0);
    var p1 = polar(a1);
    var large = n > 50 ? 1 : 0;
    var track =
      "M " +
      polar(start).x +
      " " +
      polar(start).y +
      " A " +
      r +
      " " +
      r +
      " 0 1 1 " +
      polar(end).x +
      " " +
      polar(end).y;
    var arc =
      "M " +
      p0.x +
      " " +
      p0.y +
      " A " +
      r +
      " " +
      r +
      " 0 " +
      large +
      " 1 " +
      p1.x +
      " " +
      p1.y;

    return (
      '<div class="rpt-chart rpt-chart-gauge">' +
      '<svg viewBox="0 0 140 90" role="img" aria-label="' +
      esc(label + " " + Math.round(n)) +
      '" tabindex="0">' +
      '<path class="rpt-gauge-track" d="' +
      track +
      '" fill="none" stroke-width="10" stroke-linecap="round"/>' +
      '<path class="rpt-gauge-value" d="' +
      arc +
      '" fill="none" stroke-width="10" stroke-linecap="round"/>' +
      '<text class="rpt-gauge-num" x="70" y="62" text-anchor="middle">' +
      esc(String(Math.round(n))) +
      "</text>" +
      '<text class="rpt-gauge-caption" x="70" y="78" text-anchor="middle">' +
      esc(label) +
      "</text>" +
      "</svg></div>"
    );
  }

  /**
   * Horizontal distribution bars.
   * @param {{label:string,value:number}[]} items
   */
  function bars(items, emptyLabel) {
    if (!items || !items.length) return emptyChart(emptyLabel);
    var max = 0;
    items.forEach(function (it) {
      var v = Math.abs(Number(it.value) || 0);
      if (v > max) max = v;
    });
    if (max <= 0) max = 1;
    return (
      '<div class="rpt-chart rpt-chart-bars" role="list" aria-label="' +
      esc(
        items
          .map(function (it) {
            return it.label + " " + it.value;
          })
          .join(", ")
      ) +
      '" tabindex="0">' +
      items
        .map(function (it) {
          var v = Math.abs(Number(it.value) || 0);
          var pct = Math.round((v / max) * 100);
          return (
            '<div class="rpt-bar-row" role="listitem" title="' +
            esc(it.label + ": " + it.value) +
            '">' +
            '<span class="rpt-caption">' +
            esc(it.label) +
            "</span>" +
            '<div class="rpt-bar-track"><div class="rpt-bar-fill" style="width:' +
            pct +
            '%"></div></div>' +
            '<span class="rpt-metric-sm">' +
            esc(String(it.value)) +
            "</span>" +
            "</div>"
          );
        })
        .join("") +
      "</div>"
    );
  }

  global.BteReportCharts = {
    radar: radar,
    gauge: gauge,
    bars: bars,
    empty: emptyChart,
  };
})(typeof window !== "undefined" ? window : globalThis);
