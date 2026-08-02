/**
 * Result report tier registry — Phase 2 scroll report (presentation only).
 */
(function (global) {
  var modules = [];

  function register(module) {
    if (!module || !module.id) return;
    var existing = modules.findIndex(function (m) {
      return m.id === module.id;
    });
    var row = {
      id: module.id,
      labelKey: module.labelKey || module.id,
      presenter: module.presenter || null,
      order: typeof module.order === "number" ? module.order : 100,
      group: module.group || "report",
      enabled: module.enabled !== false,
      anchor: module.anchor || ("tier-" + module.id),
    };
    if (existing >= 0) modules[existing] = row;
    else modules.push(row);
    modules.sort(function (a, b) {
      return a.order - b.order;
    });
  }

  function listEnabled() {
    return modules.filter(function (m) {
      return m.enabled;
    });
  }

  function get(id) {
    return modules.find(function (m) {
      return m.id === id;
    });
  }

  function registerDefaults() {
    [
      {
        id: "executive",
        labelKey: "report.tier.executive",
        order: 10,
        group: "report",
        anchor: "tier-executive",
      },
      {
        id: "bazi",
        labelKey: "report.tier.bazi",
        order: 20,
        group: "report",
        anchor: "tier-bazi",
      },
      {
        id: "charts",
        labelKey: "report.tier.charts",
        order: 30,
        group: "report",
        anchor: "tier-charts",
      },
      {
        id: "analysis",
        labelKey: "report.tier.analysis",
        order: 40,
        group: "report",
        anchor: "tier-analysis",
      },
      {
        id: "interpretation",
        labelKey: "report.tier.interpretation",
        order: 50,
        group: "report",
        anchor: "tier-interpretation",
      },
      {
        id: "knowledge",
        labelKey: "report.tier.knowledge",
        order: 60,
        group: "knowledge",
        anchor: "tier-knowledge",
      },
      {
        id: "luck_cycle",
        labelKey: "stages.luck_cycle",
        order: 70,
        group: "luck",
        enabled: false,
        anchor: "tier-luck",
      },
    ].forEach(register);
  }

  registerDefaults();

  global.BteModules = {
    register: register,
    listEnabled: listEnabled,
    get: get,
    all: function () {
      return modules.slice();
    },
  };
})(typeof window !== "undefined" ? window : globalThis);
