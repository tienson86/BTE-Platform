/**
 * BTE Portal i18n — loads catalogs from /static/i18n/{locale}.json.
 * Default locale: vi. Ready for en.json / zh.json without code changes.
 */
(function (global) {
  var DEFAULT_LOCALE = "vi";
  var STORAGE_KEY = "bte_portal_locale";

  function deepGet(obj, key) {
    if (!obj || !key) return undefined;
    var parts = String(key).split(".");
    var node = obj;
    for (var i = 0; i < parts.length; i++) {
      if (node == null || typeof node !== "object" || !(parts[i] in node)) {
        return undefined;
      }
      node = node[parts[i]];
    }
    return node;
  }

  function format(text, vars) {
    if (!vars) return text;
    return String(text).replace(/\{(\w+)\}/g, function (_, name) {
      return vars[name] != null ? String(vars[name]) : "{" + name + "}";
    });
  }

  function detectLocale() {
    try {
      var stored = localStorage.getItem(STORAGE_KEY);
      if (stored) return stored;
    } catch (_) {}
    var htmlLang = document.documentElement && document.documentElement.lang;
    if (htmlLang) return String(htmlLang).toLowerCase().slice(0, 2);
    return DEFAULT_LOCALE;
  }

  var BteI18n = {
    locale: DEFAULT_LOCALE,
    catalog: {},

    init: function (catalog, locale) {
      this.catalog = catalog && typeof catalog === "object" ? catalog : {};
      this.locale = locale || detectLocale() || DEFAULT_LOCALE;
      if (document.documentElement) {
        document.documentElement.lang = this.locale;
      }
      return this;
    },

    t: function (key, vars) {
      var value = deepGet(this.catalog, key);
      if (typeof value !== "string") return key;
      return format(value, vars);
    },

    /**
     * Apply data-i18n / data-i18n-* attributes under root (default: document).
     * Supported:
     *   data-i18n="key"              → textContent
     *   data-i18n-html="key"         → innerHTML (trusted catalog only)
     *   data-i18n-placeholder="key"  → placeholder
     *   data-i18n-aria-label="key"   → aria-label
     *   data-i18n-title="key"        → title
     *   data-i18n-value="key"        → value (inputs/buttons)
     */
    apply: function (root) {
      var scope = root || document;
      var self = this;

      scope.querySelectorAll("[data-i18n]").forEach(function (el) {
        var key = el.getAttribute("data-i18n");
        if (key) el.textContent = self.t(key);
      });
      scope.querySelectorAll("[data-i18n-html]").forEach(function (el) {
        var key = el.getAttribute("data-i18n-html");
        if (key) el.innerHTML = self.t(key);
      });
      scope.querySelectorAll("[data-i18n-placeholder]").forEach(function (el) {
        var key = el.getAttribute("data-i18n-placeholder");
        if (key) el.setAttribute("placeholder", self.t(key));
      });
      scope.querySelectorAll("[data-i18n-aria-label]").forEach(function (el) {
        var key = el.getAttribute("data-i18n-aria-label");
        if (key) el.setAttribute("aria-label", self.t(key));
      });
      scope.querySelectorAll("[data-i18n-title]").forEach(function (el) {
        var key = el.getAttribute("data-i18n-title");
        if (key) el.setAttribute("title", self.t(key));
      });
      scope.querySelectorAll("[data-i18n-value]").forEach(function (el) {
        var key = el.getAttribute("data-i18n-value");
        if (key) el.setAttribute("value", self.t(key));
      });
    },

    /**
     * Switch locale by fetching /static/i18n/{code}.json then re-applying DOM.
     * Add en.json / zh.json later — no caller code changes required.
     */
    setLocale: function (code) {
      var locale = String(code || DEFAULT_LOCALE).toLowerCase();
      var self = this;
      return fetch("/static/i18n/" + locale + ".json", {
        headers: { Accept: "application/json" },
      })
        .then(function (res) {
          if (!res.ok) throw new Error("Locale not found: " + locale);
          return res.json();
        })
        .then(function (catalog) {
          self.init(catalog, locale);
          try {
            localStorage.setItem(STORAGE_KEY, locale);
          } catch (_) {}
          self.apply(document);
          return locale;
        });
    },
  };

  var boot = global.__BTE_I18N__;
  var bootLocale = global.__BTE_I18N_LOCALE__ || detectLocale();
  BteI18n.init(boot || {}, bootLocale);

  function onReady(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  onReady(function () {
    BteI18n.apply(document);
  });

  global.BteI18n = BteI18n;
})(window);
