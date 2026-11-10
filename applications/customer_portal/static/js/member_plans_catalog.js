(function () {
  const host = document.querySelector(".bte-plan-grid");
  if (!host) return;
  const state = document.getElementById("memberPlansState");
  const money = value => Number(value).toLocaleString("vi-VN") + " VNĐ";
  BtePortal.get("/api/v1/membership/plan").then(plan => {
    plan.tiers.forEach(tier => {
      const card = host.querySelector('[data-tier="' + tier.tier + '"]');
      if (!card) return;
      card.querySelector("[data-tier-title]").textContent = tier.title;
      card.querySelector("[data-tier-price]").textContent = money(tier.amount_vnd);
      card.querySelector("[data-tier-duration]").textContent = tier.validity_days ? "Thời hạn " + tier.validity_days + " ngày" : "Đang cập nhật thời hạn";
      const chartEnabled = tier.enabled_features.includes("bazi");
      card.querySelector("[data-tier-chart]").textContent = chartEnabled ?
        (tier.feature_limits.bazi === null ? "Không giới hạn lá số Bát Tự" : tier.feature_limits.bazi + " lá số Bát Tự") : "Chưa mở lá số Bát Tự trong gói";
      const rights = card.querySelector("[data-tier-rights]"); rights.replaceChildren();
      Object.entries(plan.features).forEach(([feature, label]) => {
        if (feature === "bazi") return;
        const item = document.createElement("li");
        item.textContent = label + " — " + (tier.enabled_features.includes(feature) ?
          (tier.feature_limits[feature] === null ? "không giới hạn" : tier.feature_limits[feature] + " lượt") : "chưa mở");
        rights.append(item);
      });
      const link = card.querySelector("[data-tier-register]");
      if (!tier.enabled || !plan.ready) {
        link.removeAttribute("href"); link.setAttribute("aria-disabled", "true");
        link.textContent = "Tạm ngừng đăng ký";
      }
    });
  }).catch(() => { state.textContent = "Chưa tải được biểu phí hiện tại. Vui lòng tải lại trang trước khi đăng ký."; });
})();
