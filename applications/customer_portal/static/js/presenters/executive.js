/**
 * Executive Summary presenter — "Tổng Quan Lá Số" (report page 1).
 * Renders Summary Builder model only. No Engine/API calls.
 */
(function (global) {
  var MISSING = "--";

  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  function esc(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function show(value) {
    if (value === null || value === undefined || value === "") return MISSING;
    return String(value);
  }

  function boolish(value) {
    if (value === "true") return t("common.yes");
    if (value === "false") return t("common.no");
    return show(value);
  }

  function kv(label, value) {
    return (
      '<div class="bte-exec-kv">' +
      '<span class="bte-exec-k">' +
      esc(label) +
      "</span>" +
      '<span class="bte-exec-v">' +
      esc(show(value)) +
      "</span>" +
      "</div>"
    );
  }

  function section(title, bodyHtml) {
    return (
      '<section class="bte-exec-section">' +
      "<h3>" +
      esc(title) +
      "</h3>" +
      bodyHtml +
      "</section>"
    );
  }

  function pillarTable(pillars) {
    var cols = [
      t("executive.col_year"),
      t("executive.col_month"),
      t("executive.col_day"),
      t("executive.col_hour"),
    ];
    var rows = [
      { label: t("bazi.stem"), values: pillars.stems },
      { label: t("bazi.branch"), values: pillars.branches },
      { label: t("bazi.nap_am"), values: pillars.nap_am },
      { label: t("bazi.hidden"), values: pillars.tang_can },
      { label: t("bazi.ten_god"), values: pillars.thap_than },
      { label: t("bazi.chang_sheng"), values: pillars.truong_sinh },
    ];
    var head =
      "<thead><tr><th></th>" +
      cols
        .map(function (c) {
          return "<th>" + esc(c) + "</th>";
        })
        .join("") +
      "</tr></thead>";
    var body =
      "<tbody>" +
      rows
        .map(function (row) {
          return (
            "<tr><th scope=\"row\">" +
            esc(row.label) +
            "</th>" +
            (row.values || [])
              .map(function (v) {
                return "<td>" + esc(show(v)) + "</td>";
              })
              .join("") +
            "</tr>"
          );
        })
        .join("") +
      "</tbody>";
    return '<div class="bte-exec-table-wrap"><table class="bte-exec-table">' + head + body + "</table></div>";
  }

  function barChart(items, emptyLabel) {
    if (!items || !items.length) {
      return '<p class="bte-exec-empty">' + esc(emptyLabel || MISSING) + "</p>";
    }
    var max = 0;
    items.forEach(function (item) {
      var n = Number(item.value);
      if (Number.isFinite(n) && Math.abs(n) > max) max = Math.abs(n);
    });
    if (max <= 0) max = 1;
    return (
      '<div class="bte-exec-bars">' +
      items
        .map(function (item) {
          var n = Number(item.value);
          var pct = Number.isFinite(n) ? Math.min(100, Math.round((Math.abs(n) / max) * 100)) : 0;
          return (
            '<div class="bte-exec-bar-row">' +
            '<span class="bte-exec-bar-label">' +
            esc(show(item.label)) +
            "</span>" +
            '<div class="bte-exec-bar-track"><div class="bte-exec-bar-fill" style="width:' +
            pct +
            '%"></div></div>' +
            '<span class="bte-exec-bar-value">' +
            esc(show(item.value)) +
            "</span>" +
            "</div>"
          );
        })
        .join("") +
      "</div>"
    );
  }

  function listBlock(items) {
    if (!items || !items.length) {
      return '<p class="bte-exec-empty">' + esc(MISSING) + "</p>";
    }
    return (
      '<ul class="bte-exec-list">' +
      items
        .map(function (item) {
          return "<li>" + esc(show(item)) + "</li>";
        })
        .join("") +
      "</ul>"
    );
  }

  function daiVanTable(rows) {
    if (!rows || !rows.length) {
      return '<p class="bte-exec-empty">' + esc(MISSING) + "</p>";
    }
    return (
      '<div class="bte-exec-table-wrap"><table class="bte-exec-table">' +
      "<thead><tr>" +
      "<th>" +
      esc(t("executive.dv_index")) +
      "</th><th>" +
      esc(t("executive.dv_label")) +
      "</th><th>" +
      esc(t("bazi.stem")) +
      "</th><th>" +
      esc(t("bazi.branch")) +
      "</th><th>" +
      esc(t("executive.dv_start")) +
      "</th><th>" +
      esc(t("executive.dv_end")) +
      "</th><th>" +
      esc(t("executive.dv_age")) +
      "</th></tr></thead><tbody>" +
      rows
        .map(function (row) {
          return (
            "<tr>" +
            "<td>" +
            esc(show(row.index)) +
            "</td><td>" +
            esc(show(row.label)) +
            "</td><td>" +
            esc(show(row.stem)) +
            "</td><td>" +
            esc(show(row.branch)) +
            "</td><td>" +
            esc(show(row.start)) +
            "</td><td>" +
            esc(show(row.end)) +
            "</td><td>" +
            esc(show(row.age)) +
            "</td></tr>"
          );
        })
        .join("") +
      "</tbody></table></div>"
    );
  }

  function canXuongBlock(cx) {
    return (
      '<div class="bte-exec-grid">' +
      kv(t("executive.cx_year"), cx.year) +
      kv(t("executive.cx_month"), cx.month) +
      kv(t("executive.cx_day"), cx.day) +
      kv(t("executive.cx_hour"), cx.hour) +
      kv(t("executive.cx_total"), cx.total) +
      "</div>" +
      '<div class="bte-exec-poem">' +
      '<div class="bte-exec-k">' +
      esc(t("executive.cx_poem")) +
      "</div>" +
      '<div class="bte-exec-poem-body">' +
      esc(show(cx.poem)) +
      "</div></div>"
    );
  }

  function highlightBlock(h) {
    var items = [
      { label: t("bazi.day_master"), value: h.day_master },
      { label: t("executive.than"), value: boolish(h.than) },
      { label: t("executive.cach_cuc"), value: h.cach_cuc },
      { label: t("executive.dung_than"), value: h.dung_than },
      { label: t("executive.hy_than"), value: h.hy_than },
      { label: t("executive.dieu_hau"), value: h.dieu_hau },
      { label: t("score.overall"), value: h.total_score },
      { label: t("executive.grade"), value: h.grade },
    ];
    return (
      '<div class="bte-exec-highlight">' +
      items
        .map(function (item) {
          return (
            '<article class="bte-exec-chip">' +
            '<div class="bte-exec-k">' +
            esc(item.label) +
            "</div>" +
            '<div class="bte-exec-chip-v">' +
            esc(show(item.value)) +
            "</div></article>"
          );
        })
        .join("") +
      "</div>"
    );
  }

  /**
   * @param {object|null|undefined} data - full analyze data
   * @param {{ input?: object }} [options]
   * @returns {string} HTML fragment (page 1)
   */
  function renderExecutive(data, options) {
    try {
      if (!window.BteSummaryBuilder) {
        return (
          '<section class="bte-exec"><p class="muted">' +
          esc(t("executive.builder_missing")) +
          "</p></section>"
        );
      }
      var opts = options || {};
      var model = BteSummaryBuilder.build(data, opts);
      var dm = model.day_master || {};
      var ov = model.overview || {};
      var chartTitleKey = opts.chartTitleKey || "chart.info_title";
      var includeLunar = opts.includeLunar !== false;

      var chartBlock = "";
      if (window.BtePresenters && typeof BtePresenters.chartInfo === "function") {
        chartBlock = BtePresenters.chartInfo(data, {
          input: opts.input || {},
          titleKey: chartTitleKey,
          includeLunar: includeLunar,
        });
      }

      var batBlock = "";
      if (window.BtePresenters && typeof BtePresenters.batTrach === "function") {
        batBlock = BtePresenters.batTrach(data);
      }

      return (
        '<section class="bte-exec" aria-label="' +
        esc(t("executive.title")) +
        '">' +
        '<header class="bte-exec-hero">' +
        '<p class="bte-exec-eyebrow">' +
        esc(t("executive.eyebrow")) +
        "</p>" +
        "<h2>" +
        esc(t("executive.title")) +
        "</h2>" +
        '<p class="bte-exec-sub">' +
        esc(t("executive.subtitle")) +
        "</p>" +
        "</header>" +
        chartBlock +
        batBlock +
        section(t("executive.pillars"), pillarTable(model.pillars || {})) +
        section(
          t("executive.day_master"),
          '<div class="bte-exec-grid">' +
            kv(t("bazi.day_master"), dm.stem) +
            kv(t("bazi.element"), dm.element) +
            kv(t("bazi.yin_yang"), dm.yin_yang) +
            "</div>"
        ) +
        section(
          t("executive.overview"),
          '<div class="bte-exec-grid">' +
            kv(t("executive.than"), boolish(ov.than)) +
            kv(t("executive.than_strength"), ov.than_strength) +
            kv(t("executive.cach_cuc"), ov.cach_cuc) +
            kv(t("executive.tong_cach"), ov.tong_cach) +
            kv(t("executive.dung_than"), ov.dung_than) +
            kv(t("executive.hy_than"), ov.hy_than) +
            kv(t("executive.ky_than"), ov.ky_than) +
            kv(t("executive.dieu_hau"), ov.dieu_hau) +
            "</div>"
        ) +
        section(t("executive.wuxing"), barChart(model.wuxing, MISSING)) +
        section(t("executive.ten_gods"), barChart(model.ten_gods, MISSING)) +
        section(t("executive.shensha"), listBlock(model.shensha)) +
        section(t("executive.dai_van"), daiVanTable(model.dai_van)) +
        section(t("executive.can_xuong"), canXuongBlock(model.can_xuong || {})) +
        section(t("executive.highlight"), highlightBlock(model.highlight || {})) +
        "</section>"
      );
    } catch (_) {
      return (
        '<section class="bte-exec"><p class="muted">' +
        esc(MISSING) +
        "</p></section>"
      );
    }
  }

  /**
   * Wrap page-1 executive + narrative/report body into a print-ready document.
   * @param {string} executiveHtml
   * @param {string} bodyHtml
   * @returns {string}
   */
  function composeReportDocument(executiveHtml, bodyHtml) {
    var css =
      "<style>" +
      "body{font-family:Segoe UI,Source Sans 3,system-ui,sans-serif;color:#1c2430;margin:0;padding:24px;background:#fff;}" +
      "@media (prefers-color-scheme:dark){body{color:#e8eef7;background:#0b1220;}}" +
      ".bte-exec{max-width:960px;margin:0 auto 2rem;}" +
      ".bte-exec-hero{margin-bottom:1.25rem;}" +
      ".bte-exec-eyebrow{text-transform:uppercase;letter-spacing:.08em;font-size:.75rem;opacity:.7;margin:0 0 .35rem;}" +
      ".bte-exec-hero h2{margin:0 0 .35rem;font-size:1.75rem;}" +
      ".bte-exec-sub{margin:0;opacity:.75;}" +
      ".bte-exec-section{border:1px solid #d7e0ea;border-radius:14px;padding:1rem 1.1rem;margin:0 0 1rem;background:rgba(255,255,255,.6);}" +
      "@media (prefers-color-scheme:dark){.bte-exec-section{border-color:#243247;background:rgba(22,32,51,.85);}}" +
      ".bte-exec-section h3{margin:0 0 .75rem;font-size:1.05rem;}" +
      ".bte-exec-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:.65rem;}" +
      ".bte-exec-kv,.bte-exec-chip{padding:.55rem .7rem;border-radius:10px;background:rgba(15,118,110,.06);}" +
      ".bte-exec-k{display:block;font-size:.75rem;opacity:.7;margin-bottom:.2rem;}" +
      ".bte-exec-v,.bte-exec-chip-v{font-weight:600;}" +
      ".bte-exec-highlight{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:.65rem;}" +
      ".bte-exec-chip{border:1px solid rgba(15,118,110,.25);}" +
      ".bte-exec-table-wrap{overflow:auto;}" +
      ".bte-exec-table{width:100%;border-collapse:collapse;font-size:.92rem;}" +
      ".bte-exec-table th,.bte-exec-table td{border:1px solid #d7e0ea;padding:.45rem .55rem;text-align:center;}" +
      ".bte-exec-table th[scope=row]{text-align:left;background:rgba(15,118,110,.06);}" +
      ".bte-exec-bars{display:grid;gap:.45rem;}" +
      ".bte-exec-bar-row{display:grid;grid-template-columns:7rem 1fr 3.5rem;gap:.5rem;align-items:center;}" +
      ".bte-exec-bar-track{height:.55rem;border-radius:999px;background:rgba(15,118,110,.12);overflow:hidden;}" +
      ".bte-exec-bar-fill{height:100%;background:linear-gradient(90deg,#0f766e,#0369a1);}" +
      ".bte-exec-list{margin:0;padding-left:1.1rem;}" +
      ".bte-exec-poem{margin-top:.75rem;}" +
      ".bte-exec-poem-body{white-space:pre-wrap;margin-top:.35rem;line-height:1.5;}" +
      ".bte-exec-empty{margin:0;opacity:.65;}" +
      ".bte-exec-page-break{page-break-after:always;break-after:page;height:0;margin:0;border:0;}" +
      ".bte-exec-narrative{max-width:960px;margin:0 auto;}" +
      "@media print{.bte-exec{page-break-after:always;}}" +
      "</style>";

    return (
      "<!DOCTYPE html><html><head><meta charset=\"utf-8\" /><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />" +
      "<title>" +
      esc(t("executive.title")) +
      "</title>" +
      css +
      "</head><body>" +
      (executiveHtml || "") +
      '<hr class="bte-exec-page-break" />' +
      '<div class="bte-exec-narrative">' +
      (bodyHtml || "") +
      "</div></body></html>"
    );
  }

  global.BtePresenters = global.BtePresenters || {};
  global.BtePresenters.executive = renderExecutive;
  global.BtePresenters.composeExecutiveReport = composeReportDocument;
})(window);
