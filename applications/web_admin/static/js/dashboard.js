async function loadDashboard() {
  const flash = document.getElementById("globalFlash");
  try {
    const [dash, stats, lic, users, applications] = await Promise.all([
      BteAdmin.get("/api/v1/admin/dashboard").catch(() => null),
      BteAdmin.get("/api/v1/admin/statistics").catch(() => null),
      BteAdmin.get("/api/v1/license/status").catch(() => null),
      BteAdmin.get("/api/v1/users"),
      BteAdmin.get("/api/v1/membership/admin/applications"),
    ]);

    const d = (dash && dash.data) || {};
    const s = (stats && stats.data) || {};
    const api = s.api || {};
    const L = (lic && lic.data) || {};
    document.getElementById("cAccounts").textContent = users.length;
    document.getElementById("cPending").textContent = applications.items.filter(item => item.membership.status === "pending").length;
    document.getElementById("cMembers").textContent = applications.items.filter(item => item.membership.status === "active" && item.user.member_access).length;

    document.getElementById("cCustomers").textContent = BteAdmin.fmt(d.customer_count);
    document.getElementById("cCases").textContent = BteAdmin.fmt(d.case_count);
    document.getElementById("cStorage").textContent = BteAdmin.fmt(d.storage_backend);
    document.getElementById("cApi").textContent = BteAdmin.fmt(d.api_version);
    document.getElementById("cEngine").textContent = BteAdmin.fmt(d.engine_version);
    document.getElementById("cRequests").textContent = BteAdmin.fmt(
      d.request_count ?? api.request_count
    );
    document.getElementById("cLatency").textContent = BteAdmin.fmt(
      api.average_response_time_ms ?? api.average_response_ms
    );

    const active = L.has_license && L.license ? L.license.edition : "Chưa kích hoạt";
    document.getElementById("cLicense").textContent = active;
  } catch (err) {
    BteAdmin.showFlash(flash, err.message || "Failed to load dashboard", "error");
  }
}

document.getElementById("refreshDash").addEventListener("click", loadDashboard);
window.addEventListener("bte:auth", loadDashboard);
loadDashboard();
