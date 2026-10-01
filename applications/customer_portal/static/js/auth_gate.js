(function () {
  var PUBLIC_PATHS = { "/": true, "/good-date": true, "/login": true };

  function currentPath() {
    return window.location.pathname || "/";
  }

  function loginUrl() {
    return "/login?next=" + encodeURIComponent(currentPath() + (window.location.search || ""));
  }

  function updateNavigation(user) {
    document.querySelectorAll("[data-nav-id]").forEach(function (link) {
      var href = link.getAttribute("href") || "";
      if (!user && href !== "/good-date") link.hidden = true;
    });
    var profile = document.querySelector("a.app-user");
    if (profile) {
      profile.href = user ? "/profile" : "/login";
      profile.title = user ? (user.display_name || user.username || "Hồ sơ") : "Đăng nhập";
      var avatar = profile.querySelector(".app-user__avatar");
      if (avatar) avatar.textContent = user ? String(user.username || "U").charAt(0).toUpperCase() : "ĐN";
    }
  }

  async function boot() {
    var path = currentPath();
    var token = window.BtePortal && BtePortal.getToken ? BtePortal.getToken() : "";
    var cachedUser = window.BtePortal && BtePortal.getUser ? BtePortal.getUser() : null;
    updateNavigation(token ? cachedUser : null);
    if (!token) {
      if (!PUBLIC_PATHS[path]) window.location.replace(loginUrl());
      return;
    }
    try {
      var user = await BtePortal.get("/api/v1/auth/me");
      BtePortal.setSession(token, user);
      updateNavigation(user);
    } catch (_) {
      BtePortal.clearSession();
      updateNavigation(null);
      if (!PUBLIC_PATHS[path]) window.location.replace(loginUrl());
    }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
