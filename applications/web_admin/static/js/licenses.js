(function () {
  const flash = document.getElementById("globalFlash");

  async function loadLicense() {
    try {
      const [status, features] = await Promise.all([
        BteAdmin.get("/api/v1/license/status"),
        BteAdmin.get("/api/v1/license/features"),
      ]);
      const s = status.data || {};
      const lic = s.license || {};
      document.getElementById("licEdition").textContent = BteAdmin.fmt(
        lic.edition || (features.data && features.data.edition)
      );
      document.getElementById("licStatus").textContent = BteAdmin.fmt(lic.status || "none");
      document.getElementById("licExpires").textContent = BteAdmin.fmt(lic.expires_at);
      document.getElementById("licMachine").textContent = BteAdmin.fmt(
        lic.machine_id || s.machine_id
      );
      const feats =
        (features.data && features.data.features) || lic.enabled_features || [];
      document.getElementById("licFeatures").innerHTML = feats
        .map((f) => '<span class="badge">' + f + "</span>")
        .join(" ");
      document.getElementById("licRaw").textContent = JSON.stringify(
        { status: s, features: features.data },
        null,
        2
      );
    } catch (err) {
      BteAdmin.showFlash(flash, err.message, "error");
    }
  }

  document.getElementById("btnRefreshLic").addEventListener("click", loadLicense);
  document.getElementById("btnActivate").addEventListener("click", async () => {
    try {
      await BteAdmin.post("/api/v1/license/activate", {
        license_key: document.getElementById("licenseKey").value.trim(),
      });
      BteAdmin.showFlash(flash, "License activated", "success");
      loadLicense();
    } catch (err) {
      BteAdmin.showFlash(flash, err.message, "error");
    }
  });

  loadLicense();
})();
