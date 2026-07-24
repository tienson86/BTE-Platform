(function () {
  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  const flash = document.getElementById("globalFlash");
  const status = document.getElementById("loginStatus");
  const user = BtePortal.getUser();
  status.textContent = user
    ? t("login.signed_in_as", {
        user: user.username,
        role: user.role || "",
      })
    : t("login.not_signed_in");

  document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
      const data = await BtePortal.post("/api/v1/auth/login", {
        username: document.getElementById("username").value,
        password: document.getElementById("password").value,
      });
      BtePortal.setSession(data.access_token, data.user || { username: data.user });
      BtePortal.showFlash(flash, t("login.success"), "success");
      status.textContent = t("login.signed_in_as", {
        user: data.user && data.user.username ? data.user.username : "",
        role: (data.user && data.user.role) || "",
      });
      setTimeout(() => (window.location.href = "/dashboard"), 400);
    } catch (err) {
      BtePortal.showFlash(flash, err.message, "error");
    }
  });

  document.getElementById("btnLogout").addEventListener("click", async () => {
    try {
      await BtePortal.post("/api/v1/auth/logout", {});
    } catch (_) {}
    BtePortal.clearSession();
    status.textContent = t("login.not_signed_in");
    BtePortal.showFlash(flash, t("login.signed_out"), "success");
  });
})();
