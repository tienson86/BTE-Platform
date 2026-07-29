(function () {
  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  function esc(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  const flash = document.getElementById("globalFlash");
  const view = document.getElementById("profileView");

  function renderFriendly(me) {
    var user = (me && me.user) || me || {};
    var username =
      user.username || user.name || user.full_name || BtePortal.getUser()?.username || "--";
    var role = user.role || user.roles || "--";
    if (Array.isArray(role)) role = role.join(", ");
    view.innerHTML =
      '<div class="bte-exec-grid">' +
      '<div class="bte-exec-kv"><span class="bte-exec-k">' +
      esc(t("profile.username")) +
      '</span><span class="bte-exec-v">' +
      esc(String(username)) +
      "</span></div>" +
      '<div class="bte-exec-kv"><span class="bte-exec-k">' +
      esc(t("profile.role")) +
      '</span><span class="bte-exec-v">' +
      esc(String(role)) +
      "</span></div></div>";
  }

  async function load() {
    if (!BtePortal.getToken()) {
      view.textContent = t("profile.not_signed_in");
      return;
    }
    try {
      const me = await BtePortal.get("/api/v1/auth/me");
      renderFriendly(me && me.data != null ? me.data : me);
    } catch (err) {
      BtePortal.showFlash(flash, err.message || t("common.request_failed"), "error");
      view.textContent = t("profile.not_signed_in");
    }
  }

  document.getElementById("btnMe").addEventListener("click", load);
  load();
})();
