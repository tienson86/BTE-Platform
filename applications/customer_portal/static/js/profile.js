(function () {
  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  const flash = document.getElementById("globalFlash");
  const view = document.getElementById("profileView");

  async function load() {
    if (!BtePortal.getToken()) {
      view.textContent = t("profile.not_signed_in");
      return;
    }
    try {
      const me = await BtePortal.get("/api/v1/auth/me");
      view.textContent = BtePortal.fmt(me);
    } catch (err) {
      BtePortal.showFlash(flash, err.message, "error");
      view.textContent = err.message;
    }
  }

  document.getElementById("btnMe").addEventListener("click", load);
  load();
})();
