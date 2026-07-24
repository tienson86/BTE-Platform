/**
 * Calendar presentation layer (Sprint 1).
 * Renders calendar JSON into cards — no business logic.
 */
(function (global) {
  const MISSING = "--";

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

  function present(value) {
    if (value === null || value === undefined || value === "") return MISSING;
    if (typeof value === "number" && Number.isNaN(value)) return MISSING;
    return String(value);
  }

  function pad2(n) {
    const num = Number(n);
    if (!Number.isFinite(num)) return null;
    return String(Math.trunc(num)).padStart(2, "0");
  }

  function formatYmd(year, month, day) {
    const y = present(year);
    const m = pad2(month);
    const d = pad2(day);
    if (y === MISSING || m === null || d === null) {
      if (y === MISSING && m === null && d === null) return MISSING;
      return [y, m === null ? MISSING : m, d === null ? MISSING : d].join("-");
    }
    return y + "-" + m + "-" + d;
  }

  function formatSolar(cal) {
    const solar = cal && typeof cal.solar === "object" ? cal.solar : null;
    const year = (solar && solar.year) ?? (cal && cal.solar_year);
    const month = (solar && solar.month) ?? (cal && cal.solar_month);
    const day = (solar && solar.day) ?? (cal && cal.solar_day);
    const datePart = formatYmd(year, month, day);

    const hour = cal && cal.solar_hour;
    const minute = cal && cal.solar_minute;
    const hh = pad2(hour);
    const mm = pad2(minute);
    if (hh !== null || mm !== null) {
      const time =
        (hh === null ? MISSING : hh) + ":" + (mm === null ? MISSING : mm);
      if (datePart === MISSING) return time;
      return datePart + " " + time;
    }
    return datePart;
  }

  function formatLunar(cal) {
    const lunar = cal && typeof cal.lunar === "object" ? cal.lunar : null;
    if (!lunar) return MISSING;
    return formatYmd(lunar.year, lunar.month, lunar.day);
  }

  function formatLeap(cal) {
    const lunar = cal && typeof cal.lunar === "object" ? cal.lunar : null;
    if (!lunar || lunar.leap === null || lunar.leap === undefined) return MISSING;
    if (lunar.leap === true) return t("common.yes");
    if (lunar.leap === false) return t("common.no");
    return present(lunar.leap);
  }

  function formatSolarTerm(cal) {
    const term = cal && cal.solar_term;
    if (term === null || term === undefined || term === "") return MISSING;
    if (typeof term === "string") return present(term);
    if (typeof term === "object") {
      if (term.name !== null && term.name !== undefined && term.name !== "") {
        return present(term.name);
      }
      return MISSING;
    }
    return present(term);
  }

  function formatJulian(cal) {
    if (!cal || cal.julian_day === null || cal.julian_day === undefined) {
      return MISSING;
    }
    return present(cal.julian_day);
  }

  function formatTimezone(cal, options) {
    const opts = options || {};
    const fromCal =
      (cal && (cal.timezone || cal.tz || cal.time_zone)) || null;
    const fromOpts = opts.timezone || opts.tz || null;
    return present(fromCal || fromOpts || null);
  }

  function card(label, value, hint) {
    const hintHtml = hint
      ? '<div class="bte-card-hint">' + esc(hint) + "</div>"
      : "";
    return (
      '<article class="bte-card">' +
      '<div class="bte-card-label">' +
      esc(label) +
      "</div>" +
      '<div class="bte-card-value">' +
      esc(value) +
      "</div>" +
      hintHtml +
      "</article>"
    );
  }

  /**
   * @param {object|null|undefined} calendar - calendar JSON from analyze result
   * @param {{ timezone?: string }} [options]
   * @returns {string} HTML
   */
  function renderCalendar(calendar, options) {
    try {
      const cal =
        calendar && typeof calendar === "object" && !Array.isArray(calendar)
          ? calendar
          : {};
      const leap = formatLeap(cal);
      const yes = t("common.yes");
      const no = t("common.no");
      const leapHint =
        leap === yes ? t("calendar.leap_yes_hint") : leap === no ? t("calendar.leap_no_hint") : "";

      return (
        '<section class="bte-calendar" aria-label="' + esc(t("calendar.title")) + '">' +
        '<header class="bte-calendar-head">' +
        "<h2>" + esc(t("calendar.title")) + "</h2>" +
        '<p class="bte-calendar-sub">' + esc(t("calendar.subtitle")) + "</p>" +
        "</header>" +
        '<div class="bte-card-grid">' +
        card(t("calendar.solar"), formatSolar(cal), t("calendar.hint_solar")) +
        card(t("calendar.lunar"), formatLunar(cal), t("calendar.hint_lunar")) +
        card(t("calendar.solar_term"), formatSolarTerm(cal), t("calendar.hint_term")) +
        card(t("calendar.julian"), formatJulian(cal), t("calendar.hint_jd")) +
        card(t("calendar.timezone"), formatTimezone(cal, options), t("calendar.hint_tz")) +
        card(t("calendar.leap_month"), leap, leapHint) +
        "</div>" +
        "</section>"
      );
    } catch (_) {
      return (
        '<section class="bte-calendar">' +
        '<div class="bte-card-grid">' +
        card(t("calendar.solar"), MISSING) +
        card(t("calendar.lunar"), MISSING) +
        card(t("calendar.solar_term"), MISSING) +
        card(t("calendar.julian"), MISSING) +
        card(t("calendar.timezone"), MISSING) +
        card(t("calendar.leap_month"), MISSING) +
        "</div>" +
        "</section>"
      );
    }
  }

  global.BtePresenters = global.BtePresenters || {};
  global.BtePresenters.calendar = renderCalendar;
})(window);
