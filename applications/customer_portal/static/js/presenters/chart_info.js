/**
 * Chart / customer information presenter (presentation metadata only).
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

  function pad2(n) {
    var num = Number(n);
    if (!Number.isFinite(num)) return null;
    return String(Math.trunc(num)).padStart(2, "0");
  }

  function formatYmd(year, month, day) {
    var y = show(year);
    var m = pad2(month);
    var d = pad2(day);
    if (y === MISSING && m === null && d === null) return MISSING;
    return [y === MISSING ? MISSING : y, m === null ? MISSING : m, d === null ? MISSING : d].join(
      "-"
    );
  }

  function genderLabel(raw) {
    if (raw == null || raw === "") return MISSING;
    var key = String(raw).toLowerCase();
    if (key === "male" || key === "nam" || key === "m") return t("analyze.gender_male");
    if (key === "female" || key === "nu" || key === "nữ" || key === "f") {
      return t("analyze.gender_female");
    }
    return show(raw);
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

  /**
   * Resolve customer + birth display fields from analyze payload + input.
   * @returns {{full_name,gender,birth_date,birth_time,birth_place,timezone}}
   */
  function resolveChartInfo(data, input) {
    var payload = data && typeof data === "object" ? data : {};
    var inp = input || {};
    var customer =
      (payload.customer && typeof payload.customer === "object" && payload.customer) ||
      {};
    var cal = (payload.calendar && typeof payload.calendar === "object" && payload.calendar) || {};
    var solar = cal.solar && typeof cal.solar === "object" ? cal.solar : null;

    var fullName = pick(customer, ["full_name", "name", "ho_ten"]) ||
      pick(inp, ["full_name", "name", "ho_ten", "hoten", "customer_name"]);

    var birthPlace =
      pick(customer, ["birth_place", "noi_sinh", "place_of_birth", "birthplace"]) ||
      pick(inp, ["birth_place", "noi_sinh", "place_of_birth", "birthplace"]);

    var genderRaw =
      pick(customer, ["gender", "gioi_tinh", "sex"]) ||
      pick(inp, ["gender", "gioi_tinh", "sex"]);

    var birthDate = formatYmd(
      (solar && solar.year) ?? cal.solar_year ?? inp.year,
      (solar && solar.month) ?? cal.solar_month ?? inp.month,
      (solar && solar.day) ?? cal.solar_day ?? inp.day
    );

    var lunar = cal.lunar && typeof cal.lunar === "object" ? cal.lunar : null;
    var lunarDate = lunar
      ? formatYmd(lunar.year, lunar.month, lunar.day)
      : MISSING;

    var hh = pad2(cal.solar_hour != null ? cal.solar_hour : inp.hour);
    var mm = pad2(cal.solar_minute != null ? cal.solar_minute : inp.minute);
    var birthTime =
      hh === null && mm === null
        ? MISSING
        : (hh === null ? MISSING : hh) + ":" + (mm === null ? MISSING : mm);

    var timezone =
      pick(customer, ["timezone", "tz"]) ||
      pick(cal, ["timezone", "tz", "time_zone"]) ||
      pick(inp, ["timezone", "tz", "time_zone"]);

    return {
      full_name: show(fullName),
      gender: genderLabel(genderRaw),
      gender_raw: genderRaw,
      birth_date: birthDate,
      lunar_date: lunarDate,
      birth_time: birthTime,
      birth_place: show(birthPlace),
      timezone: show(timezone),
    };
  }

  /**
   * Resolve Bát Trạch fields when API provides them — never compute.
   */
  function resolveBatTrach(data) {
    var payload = data && typeof data === "object" ? data : {};
    // Prefer engine output (feng_shui) over client metadata echoes.
    var sources = [
      payload.feng_shui,
      payload.bat_trach,
      payload.batrach,
      payload.bazi && payload.bazi.bat_trach,
      payload.customer &&
        payload.customer.metadata &&
        (payload.customer.metadata.bat_trach || payload.customer.metadata.batrach),
    ];
    var src = null;
    for (var i = 0; i < sources.length; i++) {
      if (sources[i] && typeof sources[i] === "object") {
        src = sources[i];
        break;
      }
    }
    src = src || {};

    var cungPhi = pick(src, [
      "cung_phi",
      "cungPhi",
      "gua_name",
      "flying_star",
      "phi_cung",
    ]);
    var menhQuai = pick(src, [
      "menh_quai",
      "menhQuai",
      "ming_gua",
      "gua_name",
      "gua",
      "quai",
    ]);
    var nhom =
      pick(src, [
        "nhom_trach",
        "nhomTrach",
        "group",
        "trach_group",
        "east_west",
        "dong_tay_trach",
      ]) || null;

    // Normalize known group codes to display labels when already textual.
    var nhomLabel = nhom;
    if (nhom != null) {
      var key = String(nhom).toLowerCase().replace(/\s+/g, "_");
      if (
        key === "dong" ||
        key === "dong_tu_trach" ||
        key === "east" ||
        key === "east_four" ||
        key === "east_group"
      ) {
        nhomLabel = t("chart.bat_trach_east");
      } else if (
        key === "tay" ||
        key === "tay_tu_trach" ||
        key === "west" ||
        key === "west_four" ||
        key === "west_group"
      ) {
        nhomLabel = t("chart.bat_trach_west");
      }
    }

    return {
      cung_phi: show(cungPhi),
      menh_quai: show(menhQuai),
      nhom_trach: show(nhomLabel),
    };
  }

  /**
   * @param {object|null|undefined} data
   * @param {{ input?: object, titleKey?: string }} [options]
   * @returns {string}
   */
  function renderChartInfo(data, options) {
    var opts = options || {};
    var info = resolveChartInfo(data, opts.input || {});
    var title = t(opts.titleKey || "chart.info_title");
    var showLunar = opts.includeLunar !== false;
    return (
      '<section class="bte-chart-info bte-exec-section" aria-label="' +
      esc(title) +
      '">' +
      "<h3>" +
      esc(title) +
      "</h3>" +
      '<div class="bte-exec-grid">' +
      kv(t("chart.full_name"), info.full_name) +
      kv(t("chart.gender"), info.gender) +
      kv(t("chart.birth_date"), info.birth_date) +
      (showLunar ? kv(t("chart.lunar_date"), info.lunar_date) : "") +
      kv(t("chart.birth_time"), info.birth_time) +
      kv(t("chart.birth_place"), info.birth_place) +
      kv(t("chart.timezone"), info.timezone) +
      "</div></section>"
    );
  }

  /**
   * @param {object|null|undefined} data
   * @returns {string}
   */
  function renderBatTrach(data) {
    var bt = resolveBatTrach(data);
    var title = t("chart.feng_shui_title");
    return (
      '<section class="bte-bat-trach bte-exec-section" aria-label="' +
      esc(title) +
      '">' +
      "<h3>" +
      esc(title) +
      "</h3>" +
      '<div class="bte-cung-phi-hero">' +
      '<div class="bte-exec-k">' +
      esc(t("chart.cung_phi")) +
      "</div>" +
      '<div class="bte-cung-phi-name">' +
      esc(show(bt.cung_phi !== MISSING ? bt.cung_phi : bt.menh_quai)) +
      "</div>" +
      '<div class="bte-cung-phi-group">' +
      esc(show(bt.nhom_trach)) +
      "</div>" +
      "</div>" +
      '<div class="bte-exec-grid">' +
      kv(t("chart.cung_phi"), bt.cung_phi) +
      kv(t("chart.menh_quai"), bt.menh_quai) +
      kv(t("chart.nhom_trach"), bt.nhom_trach) +
      "</div></section>"
    );
  }

  /**
   * Combined card block for Result header (no lunar — matches "Thông tin lá số").
   */
  function renderChartHeader(data, options) {
    var opts = options || {};
    return (
      '<div class="bte-chart-header">' +
      renderChartInfo(data, {
        input: opts.input || {},
        titleKey: opts.titleKey || "chart.info_title",
        includeLunar: false,
      }) +
      renderBatTrach(data) +
      "</div>"
    );
  }

  global.BtePresenters = global.BtePresenters || {};
  global.BtePresenters.chartInfo = renderChartInfo;
  global.BtePresenters.batTrach = renderBatTrach;
  global.BtePresenters.chartHeader = renderChartHeader;
  global.BtePresenters.resolveChartInfo = resolveChartInfo;
  global.BtePresenters.resolveBatTrach = resolveBatTrach;
})(window);
