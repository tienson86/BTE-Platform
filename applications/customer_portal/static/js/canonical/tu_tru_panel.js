/**
 * Canonical Tứ Trụ panel — HTML renderer.
 * Presentation only. Callers supply Year/Month/Day/Hour labels.
 */
(function (global) {
  var TITLE = "TỨ TRỤ";
  var COLUMNS = ["Can Chi", "Nạp âm", "Cung Phi"];
  var ROWS = [
    { key: "year", label: "Năm" },
    { key: "month", label: "Tháng" },
    { key: "day", label: "Ngày" },
    { key: "hour", label: "Giờ" },
  ];
  var NAP_AM_TOKEN = { Mộc: "moc", Hỏa: "hoa", Thổ: "tho", Kim: "kim", Thủy: "thuy" };
  var CUNG_TOKEN = {
    Khảm: "thuy",
    Ly: "hoa",
    Chấn: "moc",
    Tốn: "moc",
    Càn: "kim",
    Khôn: "tho",
    Cấn: "tho",
    Đoài: "kim",
  };

  function esc(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function foldVi(value) {
    return String(value || "").trim().toLocaleLowerCase("vi");
  }

  function matchKnown(value, table) {
    var trimmed = String(value || "").trim();
    if (!trimmed) return null;
    if (table[trimmed]) return table[trimmed];
    var folded = foldVi(trimmed);
    var label;
    for (label in table) {
      if (Object.prototype.hasOwnProperty.call(table, label) && foldVi(label) === folded) {
        return table[label];
      }
    }
    return null;
  }

  function napAmToken(value) {
    var direct = matchKnown(value, NAP_AM_TOKEN);
    if (direct) return direct;
    var folded = foldVi(value);
    var label;
    for (label in NAP_AM_TOKEN) {
      if (Object.prototype.hasOwnProperty.call(NAP_AM_TOKEN, label) && folded.endsWith(foldVi(label))) {
        return NAP_AM_TOKEN[label];
      }
    }
    return null;
  }

  function cungToken(value) {
    return matchKnown(value, CUNG_TOKEN);
  }

  function badgeHtml(value, kind) {
    var label = String(value || "").trim();
    if (!label) return '<span class="bte-tu-tru__empty">—</span>';
    var token = kind === "nap-am" ? napAmToken(label) : cungToken(label);
    var tokenClass = token ? "bte-tu-tru__badge--" + token : "bte-tu-tru__badge--neutral";
    return (
      '<span class="bte-tu-tru__badge ' +
      tokenClass +
      '" data-kind="' +
      kind +
      '">' +
      esc(label) +
      "</span>"
    );
  }

  function pillarOf(data, key) {
    var pillar = (data && data[key]) || {};
    return {
      canChi: pillar.canChi || pillar.can_chi || "",
      napAm: pillar.napAm || pillar.nap_am || pillar.nayin || "",
      cungPhi: pillar.cungPhi || pillar.cung_phi || pillar.cung || "",
    };
  }

  /**
   * Return canonical Tứ Trụ markup for supplied pillar labels.
   */
  function html(data) {
    var head =
      '<th class="bte-tu-tru__corner" scope="col"><span class="bte-tu-tru__sr-only">Trụ</span></th>' +
      COLUMNS.map(function (column) {
        return "<th scope=\"col\">" + esc(column) + "</th>";
      }).join("");
    var body = ROWS.map(function (row) {
      var pillar = pillarOf(data, row.key);
      var canChi = String(pillar.canChi || "").trim() || "—";
      return (
        "<tr data-pillar=\"" +
        esc(row.key) +
        "\"><th scope=\"row\">" +
        esc(row.label) +
        '</th><td class="bte-tu-tru__can-chi">' +
        esc(canChi) +
        "</td><td>" +
        badgeHtml(pillar.napAm, "nap-am") +
        "</td><td>" +
        badgeHtml(pillar.cungPhi, "cung-phi") +
        "</td></tr>"
      );
    }).join("");
    return (
      '<section class="bte-tu-tru" data-canonical="tu-tru-panel" data-testid="tu-tru-panel" aria-labelledby="bte-tu-tru-title">' +
      '<h3 id="bte-tu-tru-title" class="bte-tu-tru__title">' +
      TITLE +
      "</h3>" +
      '<table class="bte-tu-tru__table"><thead><tr>' +
      head +
      "</tr></thead><tbody>" +
      body +
      "</tbody></table></section>"
    );
  }

  /**
   * Mount the panel into an existing element.
   */
  function mount(element, data) {
    if (!element) return;
    element.innerHTML = html(data);
  }

  global.BteTuTruPanel = {
    html: html,
    mount: mount,
  };
})(typeof window !== "undefined" ? window : globalThis);
