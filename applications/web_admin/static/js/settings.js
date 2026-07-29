(function () {
  const flash = document.getElementById("globalFlash");
  async function load() {
    try {
      const [cfg, sys] = await Promise.all([
        BteAdmin.get("/api/v1/admin/config"),
        BteAdmin.get("/api/v1/admin/system").catch(() => null),
      ]);
      const c = (cfg && cfg.data) || {};
      document.getElementById("sStorage").textContent = BteAdmin.fmt(c.storage_backend);
      document.getElementById("sVersion").textContent = BteAdmin.fmt(c.api_version);
      document.getElementById("sPrefix").textContent = BteAdmin.fmt(c.api_prefix);
      document.getElementById("sTz").textContent = BteAdmin.fmt(c.default_timezone);
      document.getElementById("settingsRaw").textContent = JSON.stringify(
        { config: c, system: sys && sys.data },
        null,
        2
      );
    } catch (err) {
      BteAdmin.showFlash(flash, err.message, "error");
    }
  }
  document.getElementById("btnSettings").addEventListener("click", load);
  window.addEventListener("bte:auth", load);
  if (BteAdmin.getToken()) load();
})();
