(function () {
  const flash = document.getElementById("globalFlash");
  async function load() {
    try {
      const data = await BteAdmin.get("/api/v1/admin/statistics");
      document.getElementById("statsBody").textContent = JSON.stringify(
        data.data || data,
        null,
        2
      );
    } catch (err) {
      BteAdmin.showFlash(flash, err.message, "error");
      document.getElementById("statsBody").textContent = err.message;
    }
  }
  document.getElementById("btnStats").addEventListener("click", load);
  window.addEventListener("bte:auth", load);
  if (BteAdmin.getToken()) load();
})();
