(function () {
  const btn = document.getElementById("menuToggle");
  const sidebar = document.getElementById("sidebar");
  if (btn && sidebar) {
    btn.addEventListener("click", () => sidebar.classList.toggle("open"));
  }

  const loginBtn = document.getElementById("loginBtn");
  const logoutBtn = document.getElementById("logoutBtn");
  const userLabel = document.getElementById("userLabel");
  const flash = document.getElementById("globalFlash");

  const workspace = document.getElementById("adminWorkspace");
  const loginForm = document.getElementById("adminLoginForm");
  function refreshAuthUI(user) {
    if (userLabel) {
      userLabel.textContent = user
        ? user.username + " (" + (user.role || "") + ")"
        : "Chưa đăng nhập quản trị";
    }
    if (loginBtn) loginBtn.style.display = user ? "none" : "inline-flex";
    if (logoutBtn) logoutBtn.style.display = user ? "inline-flex" : "none";
    workspace.hidden = !user;
    if (user) loginForm.hidden = true;
  }

  async function showVerifiedSession() {
    try { refreshAuthUI(await BteAdmin.ready()); }
    catch (err) { refreshAuthUI(null); BteAdmin.showFlash(flash, err.message, "error"); }
  }
  if (loginBtn) {
    loginBtn.addEventListener("click", () => {
      if (BteAdmin.portalSession) {
        window.location.assign("/login?next=" + encodeURIComponent(location.pathname));
      } else { loginForm.hidden = false; loginForm.elements.username.focus(); }
    });
  }
  loginForm.addEventListener("submit", async event => {
      event.preventDefault();
      const button = loginForm.querySelector("button"); button.disabled = true;
      try {
        const data = await BteAdmin.post("/api/v1/auth/login", {
          username: loginForm.elements.username.value.trim(),
          password: loginForm.elements.password.value,
        });
        BteAdmin.setSession(data.access_token, data.user);
        await BteAdmin.verifySession();
        loginForm.elements.password.value = "";
        BteAdmin.showFlash(flash, "Đăng nhập quản trị thành công.", "success");
        await showVerifiedSession();
        window.dispatchEvent(new Event("bte:auth"));
        window.location.reload();
      } catch (err) {
        refreshAuthUI(null);
        BteAdmin.showFlash(flash, err.message || "Chưa đăng nhập được.", "error");
      }
      finally { button.disabled = false; }
  });

  if (logoutBtn) {
    logoutBtn.addEventListener("click", async () => {
      try {
        await BteAdmin.post("/api/v1/auth/logout", {});
      } catch (_) {
        /* ignore */
      }
      BteAdmin.clearSession();
      refreshAuthUI(null);
      BteAdmin.showFlash(flash, "Đã đăng xuất.", "success");
      window.dispatchEvent(new Event("bte:auth"));
    });
  }

  showVerifiedSession();
  const titles = {dashboard:"Tổng quan",accounts:"Quản lý tài khoản",memberships:"Thành viên & thanh toán","website-settings":"Cấu hình website",customers:"Khách hàng",cases:"Hồ sơ tư vấn",reports:"Báo cáo",licenses:"Bản quyền",statistics:"Thống kê",settings:"Thông tin hệ thống"};
  document.getElementById("pageTitle").textContent = titles[document.body.dataset.adminPage] || "Quản trị hệ thống";
})();
