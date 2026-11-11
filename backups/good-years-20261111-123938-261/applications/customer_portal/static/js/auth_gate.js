(function () {
  var PUBLIC_PATHS = { "/gioi-thieu-bte": true, "/thanh-vien-bte": true, "/": true, "/good-date": true, "/login": true, "/name-analysis": true, "/number-energy": true, "/membership": true, "/contact":true };

  function currentPath() {
    return window.location.pathname || "/";
  }

  function loginUrl() {
    return "/login?next=" + encodeURIComponent(currentPath() + (window.location.search || ""));
  }

  var walletOwner = null, walletGeneration = 0, walletTimer = null, walletLoading = false, walletRefreshPending = false;
  async function refreshHeaderWallet() {
    var badge = document.getElementById('headerLinhThach'), count = document.getElementById('headerLinhThachBalance');
    if (!badge || !count || !walletOwner || document.hidden) return;
    if (walletLoading) { walletRefreshPending = true; return; }
    var generation = walletGeneration;
    walletLoading = true;
    try {
      var result = await BtePortal.get('/api/v1/membership/wallet-balance');
      if (generation !== walletGeneration) return;
      if (!Number.isSafeInteger(result.balance)) throw new Error('Invalid balance');
      count.textContent = result.balance.toLocaleString('vi-VN');
      badge.setAttribute('aria-label', 'Số dư ' + count.textContent + ' Linh Thạch. Xem và đổi Linh Thạch');
      badge.title = 'Số dư ' + count.textContent + ' Linh Thạch — bấm để xem và đổi';
      badge.hidden = false;
    } catch (error) {
      if (generation !== walletGeneration) return;
      count.textContent = '—';
      badge.title = 'Chưa tải được số dư Linh Thạch. Bấm để kiểm tra';
      badge.setAttribute('aria-label', 'Chưa tải được số dư Linh Thạch');
      if (error.status === 401 || error.status === 403) updateHeaderWallet(null);
    } finally {
      if (generation === walletGeneration) {
        walletLoading = false;
        if (walletRefreshPending) { walletRefreshPending = false; void refreshHeaderWallet(); }
      }
    }
  }
  function updateHeaderWallet(user) {
    var badge = document.getElementById('headerLinhThach'), count = document.getElementById('headerLinhThachBalance');
    if (!badge || !count) return;
    var next = user ? user.user_id || user.username : null;
    if (next === walletOwner) { badge.hidden = !user; return; }
    walletGeneration += 1; walletOwner = next; walletLoading = false; walletRefreshPending = false;
    if (walletTimer) clearInterval(walletTimer);
    walletTimer = null; count.textContent = '—'; badge.hidden = !user;
    badge.setAttribute('aria-label', 'Số dư Linh Thạch');
    if (user) {
      void refreshHeaderWallet();
      walletTimer = setInterval(refreshHeaderWallet, 45000);
    }
  }
  window.addEventListener('bte:wallet-changed', refreshHeaderWallet);
  window.addEventListener('bte:session-cleared', function () { updateHeaderWallet(null); });
  window.addEventListener('focus', refreshHeaderWallet);
  document.addEventListener('visibilitychange', function () { if (!document.hidden) void refreshHeaderWallet(); });

  function updateNavigation(user) {
    updateHeaderWallet(user);
    var logout = document.getElementById("memberLogout");
    if (logout) logout.hidden = !user;
    var sidebar = document.getElementById("memberSidebar");
    var toggle = document.getElementById("btnNavToggle");
    if (sidebar) sidebar.hidden = !user;
    if (toggle) toggle.hidden = !user;
    document.body.dataset.memberNav = user ? "true" : "false";
    document.querySelectorAll("[data-admin-only]").forEach(function (link) { link.hidden = !user || user.role !== "ADMIN"; });
    document.querySelectorAll("[data-forum-only]").forEach(function(link){link.hidden=!user || !(user.role==="ADMIN" || user.member_access===true);});
    if(!user)document.querySelectorAll("[data-message-unread]").forEach(function(badge){badge.hidden=true;badge.textContent="";});
    var join = document.getElementById("memberJoinLink");
    if (join) join.textContent = user ? "Thành viên" : "Đăng ký thành viên";
    document.querySelectorAll("[data-nav-id]").forEach(function (link) {
      var href = link.getAttribute("href") || "";
      var feature = {"/analyze":"bazi", "/choose-date":"date_selection", "/marriage-consulting":"marriage",
        "/childbirth-consulting":"childbirth", "/naming-consulting":"naming",
        "/business-consulting":"business", "/tinh-van-han":"van_han", "/tinh-cac-nam-tot":"van_han"}[href];
      link.hidden = (!user && !PUBLIC_PATHS[href]) ||
        !!(user && Array.isArray(user.member_features) && feature && !user.member_features.includes(feature));
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
    var logout = document.getElementById("memberLogout");
    if (logout) logout.onclick = async function () {
      logout.disabled = true;
      try { await BtePortal.post("/api/v1/auth/logout", {}); } catch (_) {}
      BtePortal.clearSession();
      updateNavigation(null);
      window.location.assign("/login");
    };
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
      BtePortal.get("/api/v1/communications/summary").then(function(summary){
        document.querySelectorAll("[data-message-unread]").forEach(function(badge){var count=Number(summary.unread_messages)||0;badge.textContent=count>99?"99+":String(count);badge.hidden=count===0;badge.setAttribute("aria-label",count+" tin nhắn chưa đọc");});
      }).catch(function(){});
      if (path === "/admin-membership" && user.role !== "ADMIN") window.location.replace("/membership");
      else if (user.member_access === false && !PUBLIC_PATHS[path] && path !== "/profile" && path !== "/messages") window.location.replace("/membership");
    } catch (_) {
      BtePortal.clearSession();
      updateNavigation(null);
      if (!PUBLIC_PATHS[path]) window.location.replace(loginUrl());
    }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
