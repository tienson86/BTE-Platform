(function () {
  const flash = document.getElementById("globalFlash");
  const view = document.getElementById("profileView");

  async function load() {
    if (!BtePortal.getToken()) {
      view.textContent = "Not signed in.";
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
