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
  const textKeys = ["title", "description", "public_notice", "bank_name", "bank_account", "bank_holder", "payment_note"];
  const numberKeys = ["amount_vnd", "validity_days", "analysis_limit"];
  let applications = [], saving = false;
  function node(tag, text) { const el = document.createElement(tag); if (text !== undefined) el.textContent = text; return el; }
  function line(label, value) { const el = node("p"); el.append(node("strong", label + ": "), document.createTextNode(String(value ?? "—"))); return el; }
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
        line("Ghi chú giao dịch", member.payment_note), line("Trạng thái", {pending:"Chờ xác nhận",active:"Đã kích hoạt",rejected:"Chưa chấp thuận"}[member.status] || member.status));
      if (member.legacy_transfer_content) card.append(line("Nội dung chuyển khoản trước đây", member.legacy_transfer_content));
      if (member.status === "pending") {
        const confirmLabel = node("label"); confirmLabel.className = "check";
        const confirmed = node("input"); confirmed.type = "checkbox";
        confirmLabel.append(confirmed, document.createTextNode(" Tôi đã đối chiếu số tiền và nội dung chuyển khoản: " + item.transfer_content + (member.legacy_transfer_content ? " (hoặc nội dung trước đây: " + member.legacy_transfer_content + ")" : "")));
        const noteLabel = node("label", "Ghi chú phản hồi cho khách");
        const note = node("textarea"); note.maxLength = 500; noteLabel.append(note);
        const approve = node("button", "Xác nhận đã nhận tiền và mở quyền"); approve.type = "button";
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
    const button = form.querySelector('button[type="submit"]'); saving = true; button.disabled = true;
    try {
      await api.api("PUT", "/api/v1/membership/admin/settings", payload);
      state.textContent = "Đã lưu cấu hình. Hạn mức áp dụng riêng cho từng chức năng ở các đăng ký tiếp theo.";
    } catch (error) { state.textContent = error.message; }
    finally { saving = false; button.disabled = false; }
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
      const plan = await api.get("/api/v1/membership/plan");
      textKeys.concat(numberKeys).forEach(key => { form.elements[key].value = plan[key] ?? ""; });
      form.elements.registration_enabled.checked = plan.registration_enabled;
      if (view !== "website-settings") await loadApplications();
      content.hidden = false;
    } catch (error) { state.textContent = error.message || "Chưa tải được trang quản trị."; }
  })();
})();
