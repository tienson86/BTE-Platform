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

  /** Vietnamese civil date: dd/mm/yyyy */
  function formatDmy(year, month, day) {
    const y = present(year);
    const m = pad2(month);
    const d = pad2(day);
    if (y === MISSING || m === null || d === null) {
      if (y === MISSING && m === null && d === null) return MISSING;
      return [d === null ? MISSING : d, m === null ? MISSING : m, y].join("/");
    }
    return d + "/" + m + "/" + y;
  }

  function formatSolar(cal) {
    if (cal && cal.solar_date) {
      const datePart = present(cal.solar_date);
      const hour = cal.solar_hour;
      const minute = cal.solar_minute;
      const hh = pad2(hour);
      const mm = pad2(minute);
      if (hh !== null || mm !== null) {
        const time =
          (hh === null ? MISSING : hh) + ":" + (mm === null ? MISSING : mm);
        if (datePart === MISSING) return time;
        return datePart + "\n" + time;
      }
      return datePart;
    }
    const solar = cal && typeof cal.solar === "object" ? cal.solar : null;
    const year = (solar && solar.year) ?? (cal && cal.solar_year);
    const month = (solar && solar.month) ?? (cal && cal.solar_month);
    const day = (solar && solar.day) ?? (cal && cal.solar_day);
    const datePart = formatDmy(year, month, day);

    const hour = cal && cal.solar_hour;
    const minute = cal && cal.solar_minute;
    const hh = pad2(hour);
    const mm = pad2(minute);
    if (hh !== null || mm !== null) {
      const time =
        (hh === null ? MISSING : hh) + ":" + (mm === null ? MISSING : mm);
      if (datePart === MISSING) return time;
      return datePart + "\n" + time;
    }
    return datePart;
  }

  function formatLunar(cal) {
    if (cal && cal.lunar_date) return present(cal.lunar_date);
    const lunar = cal && typeof cal.lunar === "object" ? cal.lunar : null;
    if (!lunar) {
      const ly = cal && cal.lunar_year;
      const lm = cal && cal.lunar_month;
      const ld = cal && cal.lunar_day;
      if (ly == null && lm == null && ld == null) return MISSING;
      return formatDmy(ly, lm, ld);
    }
    const d = pad2(lunar.day != null ? lunar.day : cal.lunar_day);
    const m = pad2(lunar.month != null ? lunar.month : cal.lunar_month);
    const canChi =
      lunar.year_can_chi ||
      lunar.can_chi ||
      lunar.year_name ||
      null;
    if (d !== null && m !== null && canChi) {
      return d + "/" + m + "/" + String(canChi).replace(/\s+/g, " ").trim();
    }
    const year = lunar.year != null ? lunar.year : cal.lunar_year;
    return formatDmy(year, lunar.month != null ? lunar.month : cal.lunar_month, lunar.day);
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

  function formatCanChi(cal) {
    if (!cal || typeof cal !== "object") return MISSING;
    var pieces = [];
    [
      ["Năm", cal.year_can_chi],
      ["Tháng", cal.month_can_chi],
      ["Ngày", cal.day_can_chi],
      ["Giờ", cal.hour_can_chi],
    ].forEach(function (item) {
      if (item[1]) pieces.push(item[0] + ": " + String(item[1]).trim());
    });
    return pieces.length ? pieces.join("\n") : MISSING;
  }

  function formatField(cal, keys) {
    if (!cal || typeof cal !== "object") return MISSING;
    for (var i = 0; i < keys.length; i++) {
      var value = cal[keys[i]];
      if (value !== null && value !== undefined && value !== "") return present(value);
    }
    return MISSING;
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

      // Julian Day is technical — hidden from customer Portal.
      return (
        '<section class="bte-calendar" aria-label="' + esc(t("calendar.title")) + '">' +
        '<header class="bte-calendar-head">' +
        "<h2>" + esc(t("calendar.title")) + "</h2>" +
        '<p class="bte-calendar-sub">' + esc(t("calendar.subtitle")) + "</p>" +
        "</header>" +
        '<div class="bte-card-grid">' +
        card(t("calendar.solar"), formatSolar(cal), t("calendar.hint_solar")) +
        card(t("calendar.lunar"), formatLunar(cal), t("calendar.hint_lunar")) +
        card(t("calendar.can_chi"), formatCanChi(cal)) +
        card(t("calendar.solar_term"), formatSolarTerm(cal), t("calendar.hint_term")) +
        card(t("chart.cung_phi"), formatField(cal, ["cung_phi", "gua_name"])) +
        card(t("chart.menh_quai"), formatField(cal, ["menh_quai", "gua_name"])) +
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
        card(t("calendar.can_chi"), MISSING) +
        card(t("calendar.solar_term"), MISSING) +
        card(t("chart.cung_phi"), MISSING) +
        card(t("chart.menh_quai"), MISSING) +
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
