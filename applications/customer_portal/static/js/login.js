(function () {
  const flash = document.getElementById("globalFlash");
  const status = document.getElementById("loginStatus");
  const user = BtePortal.getUser();
  status.textContent = user
    ? "Signed in as " + user.username + " (" + (user.role || "") + ")"
    : "Not signed in";

  document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
      const data = await BtePortal.post("/api/v1/auth/login", {
        username: document.getElementById("username").value,
        password: document.getElementById("password").value,
      });
      BtePortal.setSession(data.access_token, data.user || { username: data.user });
      BtePortal.showFlash(flash, "Login successful", "success");
      status.textContent =
        "Signed in as " + (data.user && data.user.username ? data.user.username : "");
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
    status.textContent = "Not signed in";
    BtePortal.showFlash(flash, "Signed out", "success");
  });
})();
