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
      document.getElementById("licStatus").textContent = ({active:"Đang hiệu lực",issued:"Đã cấp",expired:"Đã hết hạn",revoked:"Đã thu hồi"})[lic.status] || "Chưa kích hoạt giấy phép";
      document.getElementById("licExpires").textContent = BteAdmin.fmt(lic.expires_at);
      document.getElementById("licMachine").textContent = BteAdmin.fmt(
        lic.machine_id || s.machine_id
      );
      const feats =
        (features.data && features.data.features) || lic.enabled_features || [];
      const featureList=document.getElementById("licFeatures");featureList.replaceChildren();
      feats.forEach(feature=>{const label=document.createElement("span");label.className="badge";label.textContent=({bazi:"Lá số Bát Tự",calendar:"Lịch",report:"Báo cáo"})[feature]||feature;featureList.append(label);});
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
      BteAdmin.showFlash(flash, "Đã kích hoạt giấy phép sử dụng.", "success");
      loadLicense();
    } catch (err) {
      BteAdmin.showFlash(flash, err.message, "error");
    }
  });

  loadLicense();
})();
