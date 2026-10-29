(function () {
  var PUBLIC_PATHS = { "/": true, "/good-date": true, "/login": true, "/name-analysis": true, "/number-energy": true, "/membership": true, "/contact":true };

  function currentPath() {
    return window.location.pathname || "/";
  }

  function loginUrl() {
    return "/login?next=" + encodeURIComponent(currentPath() + (window.location.search || ""));
  }

  function updateNavigation(user) {
    var sidebar = document.getElementById("memberSidebar");
    var toggle = document.getElementById("btnNavToggle");
    if (sidebar) sidebar.hidden = !user;
    if (toggle) toggle.hidden = !user;
    document.body.dataset.memberNav = user ? "true" : "false";
    document.querySelectorAll("[data-admin-only]").forEach(function (link) { link.hidden = !user || user.role !== "ADMIN"; });
    var join = document.getElementById("memberJoinLink");
    if (join) join.textContent = user ? "Thành viên" : "Đăng ký thành viên";
    document.querySelectorAll("[data-nav-id]").forEach(function (link) {
      var href = link.getAttribute("href") || "";
      link.hidden = !user && !PUBLIC_PATHS[href];
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
    // Verify the session before revealing the member sidebar.
    updateNavigation(null);
    if (window.BtePortal) {
      BtePortal.get("/api/v1/membership/plan").then(function (plan) {
        var announcement = document.getElementById("siteAnnouncement");
        if (announcement) { announcement.textContent = plan.public_notice || ""; announcement.hidden = !plan.public_notice; }
      }).catch(function () {});
    }
    if (!token) {
      if (!PUBLIC_PATHS[path]) window.location.replace(loginUrl());
      return;
    }
    try {
      var user = await BtePortal.get("/api/v1/auth/me");
      BtePortal.setSession(token, user);
      updateNavigation(user);
      if (path === "/admin-membership" && user.role !== "ADMIN") window.location.replace("/membership");
      else if (user.member_access === false && !PUBLIC_PATHS[path] && path !== "/profile") window.location.replace("/membership");
    } catch (_) {
      BtePortal.clearSession();
      updateNavigation(null);
      if (!PUBLIC_PATHS[path]) window.location.replace(loginUrl());
    }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
