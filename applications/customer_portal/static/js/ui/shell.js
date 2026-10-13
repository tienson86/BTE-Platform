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

  function initNavDropdown() {
    document.querySelectorAll(".nav-dropdown").forEach(function (root) {
      var toggle = root.querySelector(".nav-dropdown__toggle");
      if (!toggle || toggle.__bteBound) return;
      toggle.__bteBound = true;
      toggle.addEventListener("click", function (event) {
        event.preventDefault();
        var open = root.getAttribute("data-open") === "true";
        root.setAttribute("data-open", open ? "false" : "true");
        toggle.setAttribute("aria-expanded", open ? "false" : "true");
      });
    });
    document.addEventListener("click", function (event) {
      document.querySelectorAll(".nav-dropdown").forEach(function (root) {
        if (!root.contains(event.target)) {
          root.setAttribute("data-open", "false");
          var toggle = root.querySelector(".nav-dropdown__toggle");
          if (toggle) toggle.setAttribute("aria-expanded", "false");
        }
      });
    });
  }

  function initCustomerNavToggle() {
    var header = document.getElementById("appHeader");
    var toggle = document.getElementById("btnNavToggle");
    if (!header || !toggle || toggle.__bteBound) return;
    toggle.__bteBound = true;
    toggle.addEventListener("click", function () {
      var open = header.getAttribute("data-nav-open") === "true";
      var next = open ? "false" : "true";
      header.setAttribute("data-nav-open", next);
      toggle.setAttribute("aria-expanded", next);
      toggle.setAttribute("aria-label", next === "true" ? "Đóng điều hướng" : "Mở điều hướng");
    });
  }

  function boot() {
    function showAccount(user) {
      user = user || {};
      document.querySelectorAll(".app-user").forEach(function (node) {
        var label = node.querySelector(".app-user__identity");
        if (!label) {
          label = document.createElement("span");
          label.className = "app-user__identity";
          label.style.cssText = "display:flex;flex-direction:column;font-size:13px;line-height:1.4;margin-left:8px;max-width:220px";
          node.appendChild(label);
        }
        label.replaceChildren();
        var avatar = node.querySelector(".app-user__avatar");
        if (avatar) avatar.remove();
        if (!user.username) {
          label.textContent = "Đăng Nhập";
          label.style.marginLeft = "0";
          node.href = "/login";
          node.setAttribute("aria-label", "Đăng Nhập");
          node.title = "Đăng Nhập";
          return;
        }
        var name = document.createElement("strong");
        name.textContent = user.display_name || user.full_name || user.username || "Chưa đăng nhập";
        var username = document.createElement("span");
        username.textContent = user.username ? "@" + user.username : "Đăng nhập để quản lý hồ sơ theo tài khoản";
        label.appendChild(name); label.appendChild(username);
        label.style.marginLeft = "0";
        node.href = "/profile";
        node.style.display = "flex";
        node.setAttribute("aria-label", "Tài khoản " + name.textContent + (user.username ? " (" + user.username + ")" : ""));
      });
    }
    if (global.BtePortal) {
      showAccount(global.BtePortal.getUser && global.BtePortal.getUser());
      if (global.BtePortal.getToken && global.BtePortal.getToken() && global.BtePortal.get) {
        global.BtePortal.get("/api/v1/auth/me").then(function (response) {
          showAccount(response.data || response);
        }).catch(function () {});
      }
    }
    initThemeToggle();
    initNavDropdown();
    initCustomerNavToggle();
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
