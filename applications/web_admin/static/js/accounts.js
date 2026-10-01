(function () {
  const rows = document.getElementById("accountRows");
  const modal = document.getElementById("accountModal");
  const form = document.getElementById("accountForm");
  const flash = document.getElementById("globalFlash");
  let accounts = [];

  function openModal(account) {
    const editing = Boolean(account);
    document.getElementById("editingUsername").value = editing ? account.username : "";
    document.getElementById("username").value = editing ? account.username : "";
    document.getElementById("username").disabled = editing;
    document.getElementById("displayName").value = editing ? account.display_name || "" : "";
    document.getElementById("password").value = "";
    document.getElementById("password").required = !editing;
    document.getElementById("analysisLimit").value = editing ? account.analysis_limit : 50;
    document.getElementById("analysesUsed").value = editing ? account.analyses_used : 0;
    document.getElementById("isActive").checked = editing ? account.is_active : true;
    document.getElementById("usedLabel").style.display = editing ? "block" : "none";
    document.getElementById("activeLabel").style.display = editing ? "block" : "none";
    modal.classList.add("show");
  }

  async function load() {
    try {
      accounts = await BteAdmin.get("/api/v1/users");
      rows.innerHTML = accounts.map(function (u) {
        return "<tr><td><strong>" + BteAdmin.fmt(u.username) + "</strong></td><td>" + BteAdmin.fmt(u.display_name) +
          "</td><td>" + (u.is_active ? "Đang hoạt động" : "Đã khóa") + "</td><td>" + BteAdmin.fmt(u.analysis_limit) +
          "</td><td>" + u.analyses_used + "</td><td>" + BteAdmin.fmt(u.analyses_remaining) +
          '</td><td><button type="button" data-edit="' + u.username + '">Sửa</button></td></tr>';
      }).join("");
      rows.querySelectorAll("[data-edit]").forEach(function (button) {
        button.addEventListener("click", function () { openModal(accounts.find(function (u) { return u.username === button.dataset.edit; })); });
      });
    } catch (err) { BteAdmin.showFlash(flash, err.message, "error"); }
  }

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    const editing = document.getElementById("editingUsername").value;
    const payload = { display_name: document.getElementById("displayName").value, analysis_limit: Number(document.getElementById("analysisLimit").value) };
    const password = document.getElementById("password").value;
    if (password) payload.password = password;
    try {
      if (editing) {
        payload.analyses_used = Number(document.getElementById("analysesUsed").value);
        payload.is_active = document.getElementById("isActive").checked;
        await BteAdmin.api("PATCH", "/api/v1/users/" + encodeURIComponent(editing), payload);
      } else {
        payload.username = document.getElementById("username").value;
        payload.password = password;
        await BteAdmin.post("/api/v1/users", payload);
      }
      modal.classList.remove("show"); BteAdmin.showFlash(flash, "Đã lưu tài khoản", "success"); load();
    } catch (err) { BteAdmin.showFlash(flash, err.message, "error"); }
  });
  document.getElementById("btnCreate").addEventListener("click", function () { openModal(null); });
  document.getElementById("btnReload").addEventListener("click", load);
  document.getElementById("modalClose").addEventListener("click", function () { modal.classList.remove("show"); });
  load();
})();
