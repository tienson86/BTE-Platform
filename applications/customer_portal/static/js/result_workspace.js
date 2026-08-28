/**
 * BZ-UI-02 Result Workspace V2 — canonical panel shells.
 * Preview fixture only when ?preview=1. No fetch, engine, or ResultStore.
 */
(function (global) {
  var EMPTY = "Chờ dữ liệu";
  var EMPTY_PILLAR = { canChi: "", napAm: "", cungPhi: "" };
  var PREVIEW_PILLARS = {
    year: { canChi: "Bính Ngọ", napAm: "Thủy", cungPhi: "Khảm" },
    month: { canChi: "Bính Thân", napAm: "Hỏa", cungPhi: "Khôn" },
    day: { canChi: "Đinh Sửu", napAm: "Thủy", cungPhi: "Chấn" },
    hour: { canChi: "Ất Tỵ", napAm: "Hỏa", cungPhi: "Khôn" },
  };
  var OVERVIEW = [
    { id: "strength", label: "Thân vượng", value: "Thân vượng" },
    { id: "useful-god", label: "Dụng thần", value: "Tỷ Kiên" },
    { id: "favorable-god", label: "Hỷ thần", value: "Thực Thần" },
    { id: "avoid-god", label: "Kỵ thần", value: "Thất Sát" },
  ];
  var ELEMENTS = [
    { id: "wood", name: "Mộc", pct: 22 },
    { id: "fire", name: "Hỏa", pct: 18 },
    { id: "earth", name: "Thổ", pct: 24 },
    { id: "metal", name: "Kim", pct: 16 },
    { id: "water", name: "Thủy", pct: 20 },
  ];
  var TEN_GODS = [
    ["Tỷ Kiên", 18],
    ["Kiếp Tài", 8],
    ["Thực Thần", 14],
    ["Thương Quan", 6],
    ["Thiên Tài", 10],
    ["Chính Tài", 12],
    ["Thất Sát / Thiên Quan", 7],
    ["Chính Quan", 9],
    ["Thiên Ấn", 11],
    ["Chính Ấn", 5],
  ];
  var SHEN_SHA = [
    ["Thiên Đức", "Có"],
    ["Nguyệt Đức", "Có"],
    ["Thiên Ất Quý Nhân", "Có"],
    ["Văn Xương", "Không"],
    ["Đào Hoa", "Có"],
    ["Hồng Loan", "Không"],
    ["Hoa Cái", "Có"],
    ["Dịch Mã", "Không"],
    ["Không Vong", "Có"],
  ];
  var BLOCKS = [
    ["observe", "Quan sát", "Khối Quan sát chờ luận giải."],
    ["reason", "Lý do", "Khối Lý do chờ luận giải."],
    ["impact", "Tác động", "Khối Tác động chờ luận giải."],
    ["advice", "Khuyến nghị", "Khối Khuyến nghị chờ luận giải."],
  ];
  var CHIPS = [
    ["career", "Công việc"],
    ["finance", "Tài chính"],
    ["relation", "Quan hệ"],
    ["health", "Sức khỏe"],
  ];

  function isPreview() {
    return /(?:^|[?&])preview=1(?:&|$)/.test(global.location.search);
  }

  function val(preview, text) {
    if (preview) return '<span class="bte-rw-value" data-preview="fixture">' + text + "</span>";
    return '<span class="bte-rw-empty" data-empty="true">' + EMPTY + "</span>";
  }

  function meter(preview, label, pct, tone) {
    var width = preview ? pct : 0;
    var toneAttr = tone ? ' data-tone="' + tone + '"' : "";
    return (
      '<div class="bte-rw-meter" role="meter" aria-label="' +
      label +
      '" data-empty="' +
      (preview ? "false" : "true") +
      '"' +
      toneAttr +
      '><div class="bte-rw-meter__fill" style="width:' +
      width +
      '%"></div></div>'
    );
  }

  function htmlOverview(preview) {
    var stats = OVERVIEW.map(function (slot) {
      return (
        '<li class="bte-rw-stat" data-slot="' +
        slot.id +
        '"><span class="bte-rw-label">' +
        slot.label +
        '</span><span class="bte-rw-primary">' +
        val(preview, slot.value) +
        "</span></li>"
      );
    }).join("");
    return (
      '<div class="bte-rw-panel" data-shell="overview"><ul class="bte-rw-stat-grid">' +
      stats +
      '</ul><div class="bte-rw-score" data-slot="overview-score"><div class="bte-rw-score__head"><span class="bte-rw-label">Điểm tổng quan</span><span class="bte-rw-primary">' +
      val(preview, "78 / 100") +
      "</span></div>" +
      meter(preview, "Điểm tổng quan", 78) +
      '</div><div class="bte-rw-inline" data-slot="overview-confidence"><span class="bte-rw-label">Độ tin cậy</span>' +
      (preview ? '<span class="bte-rw-badge">Cao</span>' : val(false)) +
      "</div></div>"
    );
  }

  function htmlFive(preview) {
    var cols = ELEMENTS.map(function (el) {
      var h = preview ? el.pct : 18;
      return (
        '<span class="bte-rw-chart__col bte-rw-chart__col--' +
        el.id +
        '" style="height:' +
        h +
        '%" title="' +
        el.name +
        '"></span>'
      );
    }).join("");
    var rows = ELEMENTS.map(function (el) {
      return (
        '<li class="bte-rw-row" data-slot="five-element" data-element="' +
        el.id +
        '"><span class="bte-rw-swatch bte-rw-swatch--' +
        el.id +
        '" aria-hidden="true"></span><span class="bte-rw-label">' +
        el.name +
        "</span>" +
        meter(preview, el.name + " tỷ lệ", el.pct, el.id) +
        '<span class="bte-rw-secondary">' +
        val(preview, el.pct + "%") +
        "</span></li>"
      );
    }).join("");
    return (
      '<div class="bte-rw-panel" data-shell="five-elements"><div class="bte-rw-chart" data-slot="five-elements-chart" aria-hidden="true">' +
      cols +
      '</div><ul class="bte-rw-list">' +
      rows +
      '</ul><p class="bte-rw-caption" data-slot="five-elements-note">' +
      val(preview, "Bản xem trước — chưa phải kết quả phân tích.") +
      "</p></div>"
    );
  }

  function htmlTen(preview) {
    var rows = TEN_GODS.map(function (item) {
      return (
        '<li class="bte-rw-row" data-slot="ten-god" data-god="' +
        item[0] +
        '"><span class="bte-rw-label">' +
        item[0] +
        "</span>" +
        meter(preview, item[0], item[1]) +
        '<span class="bte-rw-secondary">' +
        val(preview, String(item[1])) +
        "</span></li>"
      );
    }).join("");
    return '<div class="bte-rw-panel" data-shell="ten-gods"><ul class="bte-rw-list bte-rw-list--compact">' + rows + "</ul></div>";
  }

  function htmlDestiny(preview) {
    return (
      '<div class="bte-rw-panel" data-shell="destiny"><div class="bte-rw-stat" data-slot="destiny-pattern"><span class="bte-rw-label">Cách cục</span><p class="bte-rw-primary">' +
      val(preview, "Kiến Lộc dụng Thực") +
      '</p></div><div class="bte-rw-stat" data-slot="destiny-climate"><span class="bte-rw-label">Điều hậu</span><p class="bte-rw-secondary">' +
      val(preview, "Điều hậu Trung hòa") +
      '</p></div><p class="bte-rw-caption" data-slot="destiny-summary">' +
      val(preview, "Khung cấu trúc xem trước — không phải cách cục máy.") +
      '</p><div class="bte-rw-inline" data-slot="destiny-quality"><span class="bte-rw-label">Đánh giá</span>' +
      (preview ? '<span class="bte-rw-badge">Ổn</span>' : val(false)) +
      "</div></div>"
    );
  }

  function htmlShen(preview) {
    var rows = SHEN_SHA.map(function (item) {
      return (
        '<li class="bte-rw-row" data-slot="shen-sha-row" data-name="' +
        item[0] +
        '"><span class="bte-rw-mark" aria-hidden="true">✦</span><span class="bte-rw-label">' +
        item[0] +
        '</span><span class="bte-rw-secondary">' +
        val(preview, item[1]) +
        "</span></li>"
      );
    }).join("");
    return '<div class="bte-rw-panel" data-shell="shen-sha"><ul class="bte-rw-list bte-rw-list--compact">' + rows + "</ul></div>";
  }

  function htmlBone(preview) {
    var stars = "";
    var i;
    for (i = 0; i < 5; i += 1) stars += preview && i < 4 ? "★" : "☆";
    return (
      '<div class="bte-rw-panel" data-shell="bone-weight"><p class="bte-rw-primary bte-rw-primary--xl" data-slot="bone-amount">' +
      val(preview, "4 lượng 8 chỉ") +
      '</p><p class="bte-rw-stars" data-slot="bone-rating">' +
      stars +
      '</p><div class="bte-rw-stat" data-slot="bone-class"><span class="bte-rw-label">Phân loại</span><p class="bte-rw-secondary">' +
      val(preview, "Thượng cách") +
      '</p></div><p class="bte-rw-caption" data-slot="bone-preview">' +
      val(preview, "Đoạn xem trước — chưa tính cân xương.") +
      "</p></div>"
    );
  }

  function htmlLuck(preview) {
    return (
      '<div class="bte-rw-panel" data-shell="luck-cycles"><div class="bte-rw-stat" data-slot="luck-current"><span class="bte-rw-label">Đại vận hiện tại</span><p class="bte-rw-primary">' +
      val(preview, "Đại vận hiện tại") +
      '</p></div><dl class="bte-rw-meta-grid"><div data-slot="luck-age"><dt class="bte-rw-label">Tuổi</dt><dd class="bte-rw-secondary">' +
      val(preview, "32–41") +
      '</dd></div><div data-slot="luck-ganzhi"><dt class="bte-rw-label">Can Chi</dt><dd class="bte-rw-secondary">' +
      val(preview, "Nhâm Thân") +
      '</dd></div><div data-slot="luck-year"><dt class="bte-rw-label">Năm hiện tại</dt><dd class="bte-rw-secondary">' +
      val(preview, "2026") +
      '</dd></div></dl><ol class="bte-rw-timeline" data-slot="luck-timeline" aria-label="Mốc đại vận"><li class="bte-rw-timeline__node"><span class="bte-rw-caption">trước</span></li><li class="bte-rw-timeline__node bte-rw-timeline__node--now"><span class="bte-rw-caption">hiện tại</span></li><li class="bte-rw-timeline__node"><span class="bte-rw-caption">sau</span></li></ol><p class="bte-rw-caption" data-slot="luck-note">' +
      val(preview, "Mốc xem trước — không tính vận hạn.") +
      "</p></div>"
    );
  }

  function htmlInterp(preview) {
    var blocks = BLOCKS.map(function (block) {
      return (
        '<section class="bte-rw-block" data-slot="reason-block" data-block="' +
        block[0] +
        '"><h3 class="bte-rw-label">' +
        block[1] +
        '</h3><p class="bte-rw-caption">' +
        val(preview, block[2]) +
        "</p></section>"
      );
    }).join("");
    return '<div class="bte-rw-panel" data-shell="interpretation"><div class="bte-rw-blocks">' + blocks + "</div></div>";
  }

  function htmlConclusion(preview) {
    var chips = CHIPS.map(function (chip) {
      return (
        '<span class="bte-rw-chip" data-slot="action-chip" data-action="' +
        chip[0] +
        '">' +
        chip[1] +
        "</span>"
      );
    }).join("");
    return (
      '<div class="bte-rw-panel" data-shell="conclusion"><div class="bte-rw-stat" data-slot="conclusion-overall"><span class="bte-rw-label">Kết luận</span><p class="bte-rw-caption">' +
      val(preview, "Kết luận xem trước — chưa phải khuyến nghị thật.") +
      '</p></div><div data-slot="conclusion-actions"><span class="bte-rw-label">Ưu tiên hành động</span><div class="bte-rw-chips">' +
      chips +
      "</div></div></div>"
    );
  }

  function mountBodies(preview) {
    var map = {
      overview: htmlOverview,
      "five-elements": htmlFive,
      "ten-gods": htmlTen,
      destiny: htmlDestiny,
      "shen-sha": htmlShen,
      "bone-weight": htmlBone,
      "luck-cycles": htmlLuck,
      interpretation: htmlInterp,
      conclusion: htmlConclusion,
    };
    Object.keys(map).forEach(function (id) {
      var host = document.querySelector('[data-panel-body="' + id + '"]');
      if (host) host.innerHTML = map[id](preview);
    });
  }

  function mountTuTru(preview) {
    var slot = document.getElementById("rw-tu-tru-slot");
    var api = global.BteTuTruPanel;
    if (!slot || !api || typeof api.mount !== "function") return;
    api.mount(slot, preview ? PREVIEW_PILLARS : {
      year: EMPTY_PILLAR,
      month: EMPTY_PILLAR,
      day: EMPTY_PILLAR,
      hour: EMPTY_PILLAR,
    });
  }

  function wireSidebar() {
    var root = document.querySelector("[data-workspace='bazi-result-v2']");
    var toggle = document.querySelector("[data-rw-toggle='sidebar']");
    if (!root || !toggle) return;
    toggle.addEventListener("click", function () {
      var open = root.getAttribute("data-sidebar") === "open";
      if (open) root.removeAttribute("data-sidebar");
      else root.setAttribute("data-sidebar", "open");
    });
  }

  function boot() {
    var preview = isPreview();
    var root = document.querySelector("[data-workspace='bazi-result-v2']");
    if (root) {
      root.setAttribute("data-panels", "BZ-UI-02");
      root.setAttribute("data-preview", preview ? "fixture" : "off");
    }
    mountTuTru(preview);
    mountBodies(preview);
    wireSidebar();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})(typeof window !== "undefined" ? window : globalThis);
