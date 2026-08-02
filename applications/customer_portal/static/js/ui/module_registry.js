/**
 * Result stage module registry — presentation only, extensible for future modules.
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
      group: module.group || "core",
      enabled: module.enabled !== false,
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
      { id: "basic", labelKey: "stages.basic", order: 10, group: "core" },
      { id: "calendar", labelKey: "stages.calendar", order: 20, group: "core" },
      { id: "bazi", labelKey: "stages.bazi", order: 30, group: "core" },
      { id: "score", labelKey: "stages.score", order: 40, group: "analysis" },
      {
        id: "interpretation",
        labelKey: "stages.interpretation",
        order: 50,
        group: "analysis",
      },
      {
        id: "discussion",
        labelKey: "stages.discussion",
        order: 60,
        group: "knowledge",
      },
      // Future expansion stubs (disabled until data/modules exist)
      {
        id: "luck_cycle",
        labelKey: "stages.luck_cycle",
        order: 70,
        group: "luck",
        enabled: false,
      },
      {
        id: "shensha",
        labelKey: "stages.shensha",
        order: 80,
        group: "analysis",
        enabled: false,
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
