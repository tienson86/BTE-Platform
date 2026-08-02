/**
 * Unified inline SVG icons for Phase 2 report (presentation only).
 */
(function (global) {
  function svg(paths, cls) {
    return (
      '<svg class="rpt-icon' +
      (cls ? " " + cls : "") +
      '" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">' +
      paths +
      "</svg>"
    );
  }

  var Icons = {
    spark: function () {
      return svg('<path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1"/><circle cx="12" cy="12" r="3"/>');
    },
    pillar: function () {
      return svg('<rect x="8" y="3" width="8" height="18" rx="1"/><path d="M6 21h12M6 3h12"/>');
    },
    chart: function () {
      return svg('<path d="M4 19V5M4 19h16"/><path d="M8 16v-5M12 16V8M16 16v-3"/>');
    },
    analyze: function () {
      return svg('<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/><path d="M8 11h6M11 8v6"/>');
    },
    book: function () {
      return svg('<path d="M4 5a2 2 0 012-2h11v18H6a2 2 0 01-2-2V5z"/><path d="M17 3v18"/>');
    },
    knowledge: function () {
      return svg('<path d="M12 3l8 4v6c0 4.5-3.2 7.5-8 9-4.8-1.5-8-4.5-8-9V7l8-4z"/><path d="M9 12l2 2 4-4"/>');
    },
    dayMaster: function () {
      return svg('<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/>');
    },
    element: function () {
      return svg('<path d="M12 3c3 4 6 7 6 10a6 6 0 11-12 0c0-3 3-6 6-10z"/>');
    },
    god: function () {
      return svg('<path d="M12 3l2.2 5.5L20 9.2l-4.2 3.7L17.5 19 12 15.8 6.5 19l1.7-6.1L4 9.2l5.8-.7L12 3z"/>');
    },
    warn: function () {
      return svg('<path d="M12 4l9 16H3L12 4z"/><path d="M12 10v4M12 16h.01"/>');
    },
    chevron: function () {
      return svg('<path d="M6 9l6 6 6-6"/>');
    },
  };

  global.BteReportIcons = Icons;
})(typeof window !== "undefined" ? window : globalThis);
