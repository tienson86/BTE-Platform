/**
 * App shell helpers — theme toggle, toast host (presentation only).
 */
(function (global) {
  var THEME_KEY = "bte_portal_theme";

  function preferredTheme() {
    try {
      var saved = localStorage.getItem(THEME_KEY);
      if (saved === "light" || saved === "dark") return saved;
    } catch (_) {}
    if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
      return "dark";
    }
    return "light";
  }

  function applyTheme(theme) {
    var value = theme === "dark" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", value);
    try {
      localStorage.setItem(THEME_KEY, value);
    } catch (_) {}
    var btn = document.getElementById("btnThemeToggle");
    if (btn) {
      btn.setAttribute("aria-pressed", value === "dark" ? "true" : "false");
      btn.textContent = value === "dark" ? "Light" : "Dark";
    }
  }

  function initThemeToggle() {
    applyTheme(preferredTheme());
    var btn = document.getElementById("btnThemeToggle");
    if (!btn || btn.__bteBound) return;
    btn.__bteBound = true;
    btn.addEventListener("click", function () {
      var current = document.documentElement.getAttribute("data-theme") || "light";
      applyTheme(current === "dark" ? "light" : "dark");
    });
  }

  function ensureToastHost() {
    var host = document.getElementById("uiToastHost");
    if (host) return host;
    host = document.createElement("div");
    host.id = "uiToastHost";
    host.className = "ui-toast-host";
    host.setAttribute("aria-live", "polite");
    document.body.appendChild(host);
    return host;
  }

  function toast(message, type) {
    var host = ensureToastHost();
    var el = document.createElement("div");
    el.className =
      "ui-alert" +
      (type === "success"
        ? " ui-alert-success"
        : type === "error"
          ? " ui-alert-danger"
          : type === "warn"
            ? " ui-alert-warning"
            : "");
    el.textContent = String(message || "");
    host.appendChild(el);
    setTimeout(function () {
      el.remove();
    }, 4200);
  }

  function boot() {
    initThemeToggle();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

  global.BteShell = {
    applyTheme: applyTheme,
    preferredTheme: preferredTheme,
    toast: toast,
  };
})(typeof window !== "undefined" ? window : globalThis);
