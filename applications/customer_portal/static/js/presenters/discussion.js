/**
 * Discussion presentation layer (AI Discussion).
 * Wraps narrative/report content with analysis context references.
 * Display only — no LLM calls from the portal.
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

  function pillarText(pillar) {
    if (!pillar || typeof pillar !== "object") return MISSING;
    var stem = pick(pillar, ["stem", "thien_can", "can"]);
    var branch = pick(pillar, ["branch", "dia_chi", "chi"]);
    if (stem == null && branch == null) return MISSING;
    return show(stem) + " " + show(branch);
  }

  function contextStrip(data) {
    var payload = data && typeof data === "object" ? data : {};
    var bazi = payload.bazi && typeof payload.bazi === "object" ? payload.bazi : {};
    var pattern =
      payload.pattern && typeof payload.pattern === "object" ? payload.pattern : {};
    var useful =
      payload.useful_god && typeof payload.useful_god === "object"
        ? payload.useful_god
        : {};

    var pillars = [
      { label: t("executive.col_year"), value: pillarText(bazi.year_pillar) },
      { label: t("executive.col_month"), value: pillarText(bazi.month_pillar) },
      { label: t("executive.col_day"), value: pillarText(bazi.day_pillar) },
      { label: t("executive.col_hour"), value: pillarText(bazi.hour_pillar) },
    ];

    var dayMaster = show(
      pick(bazi, ["day_master", "dayMaster", "nhat_chu"]) ||
        (bazi.day_pillar && pick(bazi.day_pillar, ["stem", "thien_can"]))
    );
    var element = show(
      pick(bazi, ["day_master_element", "dayMasterElement", "element"])
    );
    var tenGods = Array.isArray(bazi.ten_gods)
      ? bazi.ten_gods.filter(Boolean).join(", ")
      : [
          bazi.year_pillar && bazi.year_pillar.ten_god,
          bazi.month_pillar && bazi.month_pillar.ten_god,
          bazi.day_pillar && bazi.day_pillar.ten_god,
          bazi.hour_pillar && bazi.hour_pillar.ten_god,
        ]
          .filter(Boolean)
          .join(", ");
    var shensha = Array.isArray(bazi.shensha)
      ? bazi.shensha
          .map(function (s) {
            return typeof s === "object" ? s.name || s.label || "" : s;
          })
          .filter(Boolean)
          .join(", ")
      : show(pick(bazi, ["shensha", "than_sat"]));
    var usefulGod = show(
      pick(pattern, ["dung_than", "useful_god", "yong_shen"]) ||
        pick(useful, ["dung_than", "useful_god", "primary", "name", "element"])
    );

    function chip(label, value) {
      return (
        '<div class="bte-discuss-chip">' +
        '<span class="bte-discuss-chip-k">' +
        esc(label) +
        "</span>" +
        '<span class="bte-discuss-chip-v">' +
        esc(value || MISSING) +
        "</span>" +
        "</div>"
      );
    }

    return (
      '<section class="bte-card bte-discuss-context" aria-label="' +
      esc(t("discussion.context_title")) +
      '">' +
      "<h3>" +
      esc(t("discussion.context_title")) +
      "</h3>" +
      '<p class="muted">' +
      esc(t("discussion.context_hint")) +
      "</p>" +
      '<div class="bte-discuss-chips">' +
      pillars
        .map(function (p) {
          return chip(p.label, p.value);
        })
        .join("") +
      chip(t("discussion.ref_elements"), dayMaster + (element !== MISSING ? " · " + element : "")) +
      chip(t("discussion.ref_ten_gods"), tenGods || MISSING) +
      chip(t("discussion.ref_shensha"), shensha || MISSING) +
      chip(t("discussion.ref_useful_god"), usefulGod) +
      "</div>" +
      "</section>"
    );
  }

  /**
   * @param {object|null|undefined} narrative
   * @param {{ data?: object, input?: object }} [options]
   * @returns {string}
   */
  function renderDiscussion(narrative, options) {
    try {
      var full = (options && options.data) || {};
      var context = contextStrip(full);
      var body = "";
      if (window.BtePresenters && typeof BtePresenters.narrative === "function") {
        body = BtePresenters.narrative(narrative);
        // Retitle narrative shell for Discussion tab when possible.
        body = body
          .replace(
            /aria-label="[^"]*"/,
            'aria-label="' + esc(t("discussion.title")) + '"'
          )
          .replace(
            /<h2>[^<]*<\/h2>/,
            "<h2>" + esc(t("discussion.title")) + "</h2>"
          )
          .replace(
            /<p class="bte-calendar-sub">[^<]*<\/p>/,
            '<p class="bte-calendar-sub">' + esc(t("discussion.subtitle")) + "</p>"
          );
      } else {
        body =
          '<section class="bte-narr"><p class="muted">' +
          esc(t("discussion.empty")) +
          "</p></section>";
      }

      return (
        '<div class="bte-discussion">' +
        context +
        body +
        "</div>"
      );
    } catch (_) {
      return (
        '<div class="bte-discussion"><p class="muted">' +
        esc(MISSING) +
        "</p></div>"
      );
    }
  }

  global.BtePresenters = global.BtePresenters || {};
  global.BtePresenters.discussion = renderDiscussion;
})(window);
