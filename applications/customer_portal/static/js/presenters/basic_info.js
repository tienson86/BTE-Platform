/**
 * Basic information presentation (Result tab).
 * Name · Gender · Birth date/time/place · Time zone — no Feng Shui.
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

  function card(label, value) {
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

  /**
   * @param {object|null|undefined} data
   * @param {{ input?: object }} [options]
   * @returns {string}
   */
  function renderBasicInfo(data, options) {
    try {
      var info =
        window.BtePresenters && BtePresenters.resolveChartInfo
          ? BtePresenters.resolveChartInfo(data, (options && options.input) || {})
          : {
              full_name: MISSING,
              gender: MISSING,
              birth_date: MISSING,
              birth_time: MISSING,
              birth_place: MISSING,
              timezone: MISSING,
            };

      return (
        '<section class="bte-basic" aria-label="' +
        esc(t("basic.title")) +
        '">' +
        '<header class="bte-calendar-head">' +
        "<h2>" +
        esc(t("basic.title")) +
        "</h2>" +
        '<p class="bte-calendar-sub">' +
        esc(t("basic.subtitle")) +
        "</p>" +
        "</header>" +
        '<div class="bte-card-grid">' +
        card(t("chart.full_name"), info.full_name) +
        card(t("chart.gender"), info.gender) +
        card(t("chart.birth_date"), info.birth_date) +
        card(t("chart.birth_time"), info.birth_time) +
        card(t("chart.birth_place"), info.birth_place) +
        card(t("chart.timezone"), info.timezone) +
        "</div>" +
        "</section>"
      );
    } catch (_) {
      return (
        '<section class="bte-basic">' +
        '<div class="bte-card-grid">' +
        card(t("chart.full_name"), MISSING) +
        card(t("chart.gender"), MISSING) +
        card(t("chart.birth_date"), MISSING) +
        card(t("chart.birth_time"), MISSING) +
        card(t("chart.birth_place"), MISSING) +
        card(t("chart.timezone"), MISSING) +
        "</div>" +
        "</section>"
      );
    }
  }

  global.BtePresenters = global.BtePresenters || {};
  global.BtePresenters.basicInfo = renderBasicInfo;
})(window);
