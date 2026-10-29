(function () {
  const form = document.getElementById("memberRegisterForm");
  if (!form) return;
  const fields = document.getElementById("memberRegisterFields");
  const state = document.getElementById("membershipState");
  const account = document.getElementById("memberAccount");
  const usernameError = document.getElementById("memberUsernameError");
  const registerError = document.getElementById("memberRegisterError");
  let plan, busy = false;
  const money = value => Number(value).toLocaleString("vi-VN") + " đ";
  const date = value => value ? new Date(value).toLocaleDateString("vi-VN") : "—";
  function node(tag, text, className) {
    const el = document.createElement(tag);
    if (text !== undefined) el.textContent = text;
    if (className) el.className = className;
    return el;
  }
  function link(text, href) { const el = node("a", text); el.href = href; return el; }
  function row(label, value) { const el = node("p"); el.append(node("strong", label + ": "), document.createTextNode(String(value))); return el; }

  function renderAccount(data) {
    account.replaceChildren(); account.hidden = false; form.hidden = true;
    const user = data.user, membership = data.membership;
    const card = node("section", undefined, "panel");
    card.append(node("h2", "Tài khoản " + (user.display_name || user.username)));
    if (!membership) {
      card.append(node("p", "Tài khoản hiện tại giữ nguyên quyền sử dụng đã được cấp."), link("Mở xem lá số", "/analyze"), node("p"), link("Hồ sơ đã lưu và tải tài liệu", "/history"));
    } else {
      const labels = { pending: "Chờ xác nhận thanh toán", active: user.member_access ? "Thành viên đang hoạt động" : "Thành viên đã hết hạn", rejected: "Đăng ký chưa được chấp thuận" };
      card.append(node("p", labels[membership.status] || "Đang kiểm tra trạng thái", "membership-status"));
      card.append(row("Họ và Tên", user.display_name || user.username), row("Tên đăng nhập", user.username), row("Số điện thoại", user.phone || "Chưa bổ sung"));
      if (membership.status === "pending") {
        const paidPlan = membership.plan;
        card.append(node("h3", "Thông tin chuyển khoản"), row("Ngân hàng", paidPlan.bank_name), row("Số tài khoản", paidPlan.bank_account),
          row("Chủ tài khoản", paidPlan.bank_holder), row("Số tiền", money(paidPlan.amount_vnd)),
          row("Nội dung chuyển khoản", data.transfer_content), node("p", paidPlan.payment_note));
        card.append(node("p", "Thông tin trên được giữ theo lần đăng ký của bạn. Nếu được thông báo thay đổi tài khoản nhận tiền, hãy kiểm tra với quản trị viên trước khi chuyển."));
        if (data.transfer_instructions_updated) card.append(node("p", "Nội dung chuyển khoản đã được cập nhật theo họ tên và tên đăng nhập. Nếu bạn đã chuyển theo hướng dẫn trước đây, không cần chuyển lại; quản trị viên vẫn đối chiếu được giao dịch."));
        if (membership.payment_reported_at) card.append(node("p", "Đã gửi thông báo chuyển khoản. Quản trị viên sẽ đối chiếu giao dịch trước khi mở quyền."));
        const paymentForm = node("form"); paymentForm.id = "memberPaymentForm";
        const label = node("label", "Ghi chú giao dịch (nếu có)");
        const note = node("textarea"); note.name = "payment_note"; note.maxLength = 500; note.value = membership.payment_note || "";
        label.append(note);
        const button = node("button", membership.payment_reported_at ? "Cập nhật thông báo chuyển khoản" : "Tôi đã chuyển khoản"); button.type = "submit";
        paymentForm.append(label, button);
        paymentForm.addEventListener("submit", async event => {
          event.preventDefault(); button.disabled = true;
          try { renderAccount(await BtePortal.post("/api/v1/membership/payment-notice", {note: note.value})); state.textContent = "Đã gửi thông báo. Quyền thành viên được mở sau khi quản trị viên xác nhận."; }
          catch (error) { state.textContent = error.message; button.disabled = false; }
        });
        card.append(paymentForm);
      } else if (membership.status === "active") {
        card.append(row("Hiệu lực đến", date(membership.expires_at)));
        if (user.member_access) card.append(link("Bắt đầu xem lá số", "/analyze"), node("p"), link("Hồ sơ đã lưu và tải tài liệu", "/history"));
        else card.append(node("p", "Vui lòng liên hệ quản trị viên để được hướng dẫn gia hạn."));
      }
      if (membership.review_note) card.append(row("Ghi chú của quản trị viên", membership.review_note));
    }
    const refresh = node("button", "Kiểm tra lại trạng thái", "secondary"); refresh.type = "button";
    refresh.onclick = async () => { refresh.disabled = true; try { await loadAccount(); state.textContent = "Đã cập nhật trạng thái thành viên."; } catch (error) { state.textContent = error.message; refresh.disabled = false; } };
    card.append(node("p"), refresh); account.append(card);
    if (user.role === "ADMIN") account.append(link("Mở quản trị hệ thống", "/admin"));
  }

  async function loadAccount() {
    const data = await BtePortal.get("/api/v1/membership/me");
    BtePortal.setSession(BtePortal.getToken(), data.user); renderAccount(data);
  }
  form.addEventListener("submit", async event => {
    event.preventDefault(); if (busy || !plan?.ready) return;
    const input = form.elements;
    input.password_confirmation.setCustomValidity(input.password.value === input.password_confirmation.value ? "" : "Hai mật khẩu chưa giống nhau.");
    if (!form.reportValidity()) return;
    usernameError.hidden = registerError.hidden = true;
    input.username.removeAttribute("aria-invalid");
    busy = true; fields.disabled = true; state.textContent = "Đang tạo tài khoản…";
    let registered = false, duplicate = false;
    try {
      const username = input.username.value.trim(), password = input.password.value;
      await BtePortal.post("/api/v1/membership/register", {username, password, display_name: input.display_name.value.trim(), phone: input.phone.value.trim()});
      registered = true;
      input.password.value = ""; input.password_confirmation.value = "";
      const login = await BtePortal.post("/api/v1/auth/login", {username, password});
      BtePortal.setSession(login.access_token, login.user);
      window.location.assign("/membership");
    } catch (error) {
      state.textContent = "";
      duplicate = !registered && (error.payload?.code === "username_taken" || (error.status === 409 && /Tên đăng nhập/.test(error.message)));
      if (duplicate) {
        usernameError.textContent = "Tên đăng nhập đã có người dùng rồi. Bạn hãy chọn tên đăng nhập khác.";
        usernameError.hidden = false; input.username.setAttribute("aria-invalid", "true");
      } else {
        registerError.textContent = registered ? "Tài khoản đã được tạo. Vui lòng đăng nhập để tiếp tục." : error.message;
        registerError.hidden = false;
      }
    }
    finally {
      busy = false; fields.disabled = !plan.ready;
      if (duplicate) input.username.focus();
    }
  });
  form.addEventListener("input", event => {
    form.elements.password_confirmation.setCustomValidity("");
    registerError.hidden = true;
    if (event.target === form.elements.username) {
      usernameError.hidden = true; usernameError.textContent = "";
      form.elements.username.removeAttribute("aria-invalid");
    }
  });
  (async function boot() {
    try {
      plan = await BtePortal.get("/api/v1/membership/plan");
      document.getElementById("membershipTitle").textContent = plan.title;
      document.getElementById("membershipIntro").textContent = plan.description;
      document.getElementById("memberPrice").textContent = plan.amount_vnd && plan.validity_days ? money(plan.amount_vnd) + " / " + plan.validity_days + " ngày" : "Đang cập nhật biểu phí";
      document.getElementById("memberAllowance").textContent = plan.analysis_limit ? "Mỗi chức năng được tối đa " + plan.analysis_limit + " lượt tạo mới, tính riêng cho lá số, chọn ngày, hôn nhân, sinh con, đặt tên, hợp tác và vận hạn. Xem lại hoặc tải hồ sơ đã lưu không tính thêm lượt." : "Quyền xem và tải được mở sau khi xác nhận thanh toán.";
      if (BtePortal.getToken()) await loadAccount();
      else { form.hidden = false; fields.disabled = !plan.ready; if (!plan.ready) state.textContent = "Đăng ký trả phí sẽ mở sau khi biểu phí được cập nhật. Bạn vẫn dùng được các mục miễn phí."; }
    } catch (error) { state.textContent = error.message || "Chưa tải được thông tin thành viên. Vui lòng thử lại."; }
  })();
})();
