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

  function refreshAuthUI() {
    const user = BteAdmin.getUser();
    if (userLabel) {
      userLabel.textContent = user
        ? user.username + " (" + (user.role || "") + ")"
        : "Not signed in";
    }
    if (loginBtn) loginBtn.style.display = BteAdmin.getToken() ? "none" : "inline-flex";
    if (logoutBtn) logoutBtn.style.display = BteAdmin.getToken() ? "inline-flex" : "none";
  }

  if (loginBtn) {
    loginBtn.addEventListener("click", async () => {
      const username = prompt("Username", "admin");
      if (!username) return;
      const password = prompt("Password", "admin123");
      if (password === null) return;
      try {
        const data = await BteAdmin.post("/api/v1/auth/login", {
          username,
          password,
        });
        BteAdmin.setSession(data.access_token, data.user || { username });
        BteAdmin.showFlash(flash, "Signed in as " + username, "success");
        refreshAuthUI();
        window.dispatchEvent(new Event("bte:auth"));
      } catch (err) {
        BteAdmin.showFlash(flash, err.message || "Login failed", "error");
      }
    });
  }

  if (logoutBtn) {
    logoutBtn.addEventListener("click", async () => {
      try {
        await BteAdmin.post("/api/v1/auth/logout", {});
      } catch (_) {
        /* ignore */
      }
      BteAdmin.clearSession();
      refreshAuthUI();
      BteAdmin.showFlash(flash, "Signed out", "success");
      window.dispatchEvent(new Event("bte:auth"));
    });
  }

  refreshAuthUI();
})();
