(function () {
  const api = window.BteAdmin || window.BtePortal;
  const form = document.getElementById("memberSettingsForm");
  if (!form) return;
  const state = document.getElementById("memberAdminState");
  const content = document.getElementById("memberAdminContent");
  const list = document.getElementById("memberApplications");
  const filter = document.getElementById("memberApplicationFilter");
  const view = form.closest("[data-admin-view]")?.dataset.adminView;
  if (view === "memberships") form.hidden = true;
  if (view === "website-settings") document.getElementById("memberApplicationsSection").hidden = true;
  const textKeys = ["title", "description", "public_notice", "public_base_url", "bank_name", "bank_account", "bank_holder", "payment_note"];
  const numberKeys = ["amount_vnd", "validity_days", "analysis_limit"];
  let applications = [], saving = false, settingsRevision = "", featureLabels = {};
  function node(tag, text) { const el = document.createElement(tag); if (text !== undefined) el.textContent = text; return el; }
  function line(label, value) { const el = node("p"); el.append(node("strong", label + ": "), document.createTextNode(String(value ?? "—"))); return el; }
  function tierInput(card, field, labelText, value, options = {}) {
    const label = node("label", labelText);
    const input = node("input");
    input.dataset.tierField = field;
    input.type = options.type || "number";
    input.value = value ?? "";
    if (options.type !== "text") { input.min = options.min ?? 0; input.max = options.max ?? 1000000; input.step = 1; }
    else { input.maxLength = 120; input.required = true; }
    label.append(input); card.append(label);
    return input;
  }
  function renderTiers(tiers) {
    const host = document.getElementById("memberTierSettings"); host.replaceChildren();
    tiers.forEach(tier => {
      const card = node("section"); card.className = "member-tier-card"; card.dataset.tier = tier.tier;
      card.append(node("h3", "Cấp " + tier.tier));
      const enabledLabel = node("label", "Mở đăng ký cấp này"); enabledLabel.className = "check";
      const enabled = node("input"); enabled.type = "checkbox"; enabled.checked = tier.enabled;
      enabled.dataset.tierField = "enabled"; enabledLabel.prepend(enabled); card.append(enabledLabel);
      tierInput(card, "title", "Tên cấp thành viên", tier.title, {type:"text"});
      tierInput(card, "amount_vnd", "Mức phí (VNĐ)", tier.amount_vnd, {min:1000,max:1000000000}).required = true;
      tierInput(card, "validity_days", "Thời hạn (ngày)", tier.validity_days, {min:1,max:3650});
      tierInput(card, "referral_reward", "Thưởng giới thiệu (Linh Thạch)", tier.referral_reward).required = true;
      card.append(node("h4", "Quyền sử dụng từng chức năng"));
      Object.entries(featureLabels).forEach(([feature, title]) => {
        const row = node("div"); row.className = "member-tier-feature"; row.dataset.feature = feature;
        const toggleLabel = node("label", title); toggleLabel.className = "check";
        const toggle = node("input"); toggle.type="checkbox"; toggle.checked=tier.enabled_features.includes(feature);
        toggle.setAttribute("aria-label", "Mở " + title + " cấp " + tier.tier);
        toggleLabel.prepend(toggle);
        const limitLabel = node("label", "Số lượt");
        const limit = node("input"); limit.type="number"; limit.min=0; limit.max=1000000; limit.step=1;
        limit.placeholder="Không giới hạn"; limit.value=tier.feature_limits[feature] ?? "";
        limit.setAttribute("aria-label", "Hạn mức " + title + " cấp " + tier.tier);
        limit.disabled=!toggle.checked; toggle.onchange=()=>{limit.disabled=!toggle.checked;};
        limitLabel.append(limit); row.append(toggleLabel,limitLabel); card.append(row);
      });
      host.append(card);
    });
  }
  function readTiers() {
    return Array.from(document.querySelectorAll("#memberTierSettings [data-tier]")).map(card => {
      const value = field => card.querySelector('[data-tier-field="' + field + '"]').value;
      const featureLimits = {}, enabledFeatures = [];
      card.querySelectorAll("[data-feature]").forEach(row => {
        const feature = row.dataset.feature, input = row.querySelector('input[type="number"]');
        featureLimits[feature] = input.value === "" ? null : Number(input.value);
        if (row.querySelector('input[type="checkbox"]').checked) enabledFeatures.push(feature);
      });
      return {tier:Number(card.dataset.tier),title:value("title"),amount_vnd:Number(value("amount_vnd")),
        validity_days:value("validity_days")==="" ? null : Number(value("validity_days")),
        referral_reward:Number(value("referral_reward")),enabled:card.querySelector('[data-tier-field="enabled"]').checked,
        feature_limits:featureLimits,enabled_features:enabledFeatures};
    });
  }
  function render() {
    list.replaceChildren();
    const rows = applications.filter(item => filter.value === "all" || item.membership.status === "pending");
    if (!rows.length) { list.append(node("p", "Chưa có đăng ký trong nhóm này.")); return; }
    rows.forEach(item => {
      const user = item.user, member = item.membership, plan = member.plan;
      const card = node("article"); card.className = "membership-application";
      card.append(node("h3", user.display_name + " (@" + user.username + ")"), line("Mã đăng ký nội bộ", member.reference),
        line("Nội dung chuyển khoản", item.transfer_content),
        line("Số điện thoại", user.phone || "Chưa bổ sung"),
        line("Mức phí đã thông báo", Number(plan.amount_vnd).toLocaleString("vi-VN") + " đ"),
        line("Thời hạn", plan.validity_days + " ngày"), line("Tài khoản nhận", plan.bank_name + " · " + plan.bank_account + " · " + plan.bank_holder),
        line("Thông báo từ khách", member.payment_reported_at ? "Khách đã báo chuyển khoản" : "Chưa báo chuyển khoản"),
        line("Ghi chú giao dịch", member.payment_note), line("Trạng thái", {pending:"Chờ xác nhận",active:"Đã kích hoạt",rejected:"Chưa chấp thuận",refunded:"Đã hoàn tiền"}[member.status] || member.status));
      if (member.source === "upgrade") card.append(line("Loại yêu cầu", "Nâng cấp từ cấp " + member.from_tier + " lên cấp " + member.tier));
      else if (member.tier) card.append(line("Cấp thành viên", member.tier));
      if (member.referrer_user_id) card.append(
        line("Mã giới thiệu", member.referral_code),
        line("Giá trước giảm", Number(member.original_amount_vnd).toLocaleString("vi-VN") + " đ"),
        line("Giảm giá", member.discount_percent + "%"),
        line("Thưởng khi duyệt", member.referral_reward + " Linh Thạch")
      );
      if (member.status === "active") {
        const refund = node("button", "Ghi nhận đã hoàn tiền và thu hồi quyền / thưởng");
        refund.type = "button"; refund.className = "secondary";
        if (member.source === "upgrade") refund.textContent = "Ghi nhận hoàn tiền và khôi phục gói trước";
        refund.onclick = async () => {
          const message = member.source === "upgrade" ? "Xác nhận đã hoàn tiền nâng cấp? BTE sẽ khôi phục gói trước." : "Xác nhận bạn đã xử lý hoàn tiền giao dịch này? BTE sẽ thu hồi quyền thành viên và thưởng giới thiệu tương ứng.";
          if (!window.confirm(message)) return;
          refund.disabled = true;
          try {
            await api.post("/api/v1/membership/admin/applications/" + encodeURIComponent(user.user_id) + "/review",
              {decision:"refund", expected_reference:member.reference, note:"Admin ghi nhận đã xử lý hoàn tiền."});
            await loadApplications(); state.textContent = "Đã ghi nhận hoàn tiền và thu hồi quyền, thưởng liên quan.";
          } catch (error) { state.textContent = error.message; refund.disabled = false; }
        };
        card.append(refund);
      }
      if (member.legacy_transfer_content) card.append(line("Nội dung chuyển khoản trước đây", member.legacy_transfer_content));
      if (member.status === "pending") {
        const confirmLabel = node("label"); confirmLabel.className = "check";
        const confirmed = node("input"); confirmed.type = "checkbox";
        confirmLabel.append(confirmed, document.createTextNode(" Tôi đã đối chiếu số tiền và nội dung chuyển khoản: " + item.transfer_content + (member.legacy_transfer_content ? " (hoặc nội dung trước đây: " + member.legacy_transfer_content + ")" : "")));
        const noteLabel = node("label", "Ghi chú phản hồi cho khách");
        const note = node("textarea"); note.maxLength = 500; noteLabel.append(note);
        const approve = node("button", member.source === "upgrade" ? "Xác nhận đã nhận tiền và nâng cấp" : "Xác nhận đã nhận tiền và mở quyền"); approve.type = "button";
        const reject = node("button", "Chưa chấp thuận"); reject.type = "button"; reject.className = "secondary";
        async function review(decision) {
          if (decision === "approve" && !confirmed.checked) { state.textContent = "Cần xác nhận đã đối chiếu khoản tiền trước khi mở quyền."; confirmed.focus(); return; }
          approve.disabled = reject.disabled = true;
          try {
            await api.post("/api/v1/membership/admin/applications/" + encodeURIComponent(user.user_id) + "/review", {decision, expected_reference: member.reference, note: note.value.trim()});
            await loadApplications(); state.textContent = decision === "approve" ? "Đã xác nhận và mở quyền xem, tải tài liệu cho thành viên." : "Đã cập nhật kết quả duyệt đăng ký.";
          } catch (error) { state.textContent = error.message; approve.disabled = reject.disabled = false; }
        }
        approve.onclick = () => review("approve"); reject.onclick = () => review("reject");
        card.append(confirmLabel, noteLabel, approve, reject);
      } else if (member.expires_at) card.append(line("Hiệu lực đến", new Date(member.expires_at).toLocaleString("vi-VN")));
      list.append(card);
    });
  }
  async function loadApplications() { applications = (await api.get("/api/v1/membership/admin/applications")).items; render(); }
  form.addEventListener("submit", async event => {
    event.preventDefault(); if (saving || !form.reportValidity()) return;
    const payload = {};
    textKeys.forEach(key => { payload[key] = form.elements[key].value.trim(); });
    numberKeys.forEach(key => { const value = form.elements[key].value; payload[key] = value === "" ? null : Number(value); });
    payload.registration_enabled = form.elements.registration_enabled.checked;
    payload.tiers = readTiers();
    const button = form.querySelector('button[type="submit"]'); saving = true; button.disabled = true;
    const controls = Array.from(form.querySelectorAll("input, textarea"));
    const previousDisabled = controls.map(input => input.disabled);
    controls.forEach(input => { input.disabled = true; });
    try {
      await api.api("PUT", "/api/v1/membership/admin/settings", payload, {headers: {"If-Match": settingsRevision}});
      const saved = await api.get("/api/v1/membership/admin/settings");
      settingsRevision = saved.revision;
      state.textContent = "Đã lưu ba cấp thành viên. Giá, thời hạn và quyền sử dụng mới áp dụng cho đăng ký tiếp theo.";
    } catch (error) { state.textContent = error.message; }
    finally { controls.forEach((input, index) => { input.disabled = previousDisabled[index]; }); saving = false; button.disabled = false; }
  });
  filter.onchange = render;
  document.getElementById("memberApplicationsRefresh").onclick = async event => {
    event.currentTarget.disabled = true;
    try { await loadApplications(); state.textContent = "Đã tải lại danh sách."; }
    catch (error) { state.textContent = error.message; }
    finally { document.getElementById("memberApplicationsRefresh").disabled = false; }
  };
  (async function boot() {
    try {
      const user = await api.get("/api/v1/auth/me");
      if (user.role !== "ADMIN") { state.textContent = "Trang này dành cho quản trị viên."; return; }
      const plan = await api.get("/api/v1/membership/admin/settings");
      settingsRevision = plan.revision; featureLabels = plan.features || {};
      renderTiers(plan.tiers || []);
      textKeys.concat(numberKeys).forEach(key => { form.elements[key].value = plan[key] ?? ""; });
      form.elements.registration_enabled.checked = plan.registration_enabled;
      if (view !== "website-settings") await loadApplications();
      content.hidden = false;
    } catch (error) { state.textContent = error.message || "Chưa tải được trang quản trị."; }
  })();
})();
