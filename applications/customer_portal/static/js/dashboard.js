/**
 * Customer Portal Dashboard (Sprint 7) — presentation only.
 */
(function () {
  const MISSING = "--";

  function esc(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function present(value) {
    if (value === null || value === undefined || value === "") return MISSING;
    if (typeof value === "number" && Number.isNaN(value)) return MISSING;
    return String(value);
  }

  function boot() {
    if (!window.BtePortal) {
      const recent = document.getElementById("dashRecent");
      if (recent) recent.innerHTML = '<p class="muted">Portal API client failed to load.</p>';
      return;
    }

    const user = BtePortal.getUser();
    const greet = document.getElementById("dashGreeting");
    if (greet) {
      greet.textContent = user && user.username
        ? "Signed in as " + user.username
        : "Welcome to BTE Customer Portal";
    }

    renderRecentSkeletonDone();
    renderStatsFromLocal();
    probeSystemAndProduct();
  }

  function renderRecentSkeletonDone() {
    const host = document.getElementById("dashRecent");
    if (!host) return;
    const hist = (BtePortal.getHistory() || []).slice(0, 10);
    if (!hist.length) {
      host.innerHTML = '<p class="muted dash-empty">No recent charts</p>';
      return;
    }
    host.innerHTML = hist
      .map(function (item, idx) {
        const input = item.input || {};
        const label =
          [input.year, input.month, input.day].filter(function (v) {
            return v != null && v !== "";
          }).join("-") || item.id || "Chart";
        const when = item.saved_at ? String(item.saved_at) : MISSING;
        const summary = item.summary ? String(item.summary) : MISSING;
        return (
          '<article class="bte-card dash-recent-item">' +
          "<div>" +
          "<strong>" +
          esc(label) +
          '</strong><div class="muted">' +
          esc(when) +
          "</div>" +
          '<div class="dash-recent-summary">' +
          esc(summary) +
          "</div></div>" +
          '<button type="button" class="secondary" data-recent-idx="' +
          idx +
          '">Open</button>' +
          "</article>"
        );
      })
      .join("");

    host.querySelectorAll("[data-recent-idx]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        const idx = Number(btn.getAttribute("data-recent-idx"));
        const item = hist[idx];
        if (!item) return;
        const payload = { input: item.input || {}, data: item.data };
        try {
          const raw = JSON.stringify(payload);
          sessionStorage.setItem("bte_portal_last_result", raw);
          try {
            localStorage.setItem("bte_portal_last_result", raw);
          } catch (_) {}
        } catch (_) {}
        window.location.href = "/result";
      });
    });
  }

  function statCard(label, value) {
    return (
      '<article class="bte-card dash-stat">' +
      '<div class="bte-card-label">' +
      esc(label) +
      "</div>" +
      '<div class="bte-card-value">' +
      esc(present(value)) +
      "</div>" +
      "</article>"
    );
  }

  function renderStatsFromLocal() {
    const host = document.getElementById("dashStats");
    if (!host) return;
    const hist = BtePortal.getHistory() || [];
    const total = hist.length ? String(hist.length) : MISSING;
    const todayStr = new Date().toISOString().slice(0, 10);
    var todayCount = 0;
    hist.forEach(function (row) {
      var ts = row && (row.saved_at || row.created_at || row.timestamp);
      if (ts && String(ts).slice(0, 10) === todayStr) todayCount += 1;
    });
    const today = hist.length ? String(todayCount) : MISSING;
    var last = MISSING;
    if (hist.length) {
      var first = hist[0];
      last = present(first.saved_at || first.created_at || first.timestamp);
    }
    // Average score is not available from local history alone.
    host.innerHTML =
      statCard("Total Charts", total) +
      statCard("Charts Today", today) +
      statCard("Average Score", MISSING) +
      statCard("Last Analyze Time", last);
  }

  function statusRow(label, value, ok) {
    var tone = ok === true ? "strong" : ok === false ? "avoid" : "muted";
    return (
      '<div class="dash-status-row">' +
      "<span>" +
      esc(label) +
      "</span>" +
      '<span class="bte-badge bte-badge-' +
      tone +
      '">' +
      esc(present(value)) +
      "</span>" +
      "</div>"
    );
  }

  async function probeSystemAndProduct() {
    const systemHost = document.getElementById("dashSystem");
    const productHost = document.getElementById("dashProduct");
    const hero = document.getElementById("dashHeroMeta");

    var apiOk = null;
    var apiLabel = MISSING;
    var portalOk = null;
    var portalLabel = MISSING;
    var version = MISSING;
    var license = MISSING;
    var health = MISSING;

    try {
      const portal = await fetch("/healthz", { headers: { Accept: "application/json" } });
      if (portal.ok) {
        portalOk = true;
        portalLabel = "Running";
        const body = await portal.json();
        if (body && body.status) health = String(body.status);
      } else {
        portalOk = false;
        portalLabel = "Down";
      }
    } catch (_) {
      portalOk = false;
      portalLabel = "Down";
    }

    try {
      const api = await BtePortal.get("/api/v1/health");
      apiOk = true;
      apiLabel = "Running";
      const data = api && api.data ? api.data : api;
      if (data && data.version) version = String(data.version);
      else if (api && api.version) version = String(api.version);
      if (health === MISSING && data && data.status) health = String(data.status);
    } catch (_) {
      apiOk = false;
      apiLabel = "Down";
    }

    try {
      const lic = await BtePortal.get("/api/v1/license/status");
      const ld = lic && lic.data ? lic.data : lic;
      if (ld && (ld.status != null || ld.state != null || ld.valid != null)) {
        license = present(ld.status != null ? ld.status : ld.state != null ? ld.state : ld.valid);
      } else if (lic && lic.message) {
        license = present(lic.message);
      } else {
        license = "Available";
      }
    } catch (_) {
      license = MISSING;
    }

    if (version === MISSING) version = "1.0.0";

    if (systemHost) {
      systemHost.innerHTML =
        statusRow("API", apiLabel, apiOk) +
        statusRow("Portal", portalLabel, portalOk) +
        statusRow("Version", version, null) +
        statusRow("License", license, license !== MISSING) +
        statusRow("Health", health, health === "ok" || health === "healthy");
    }

    if (productHost) {
      productHost.innerHTML =
        '<div class="dash-product-name">BTE Platform</div>' +
        '<div class="dash-status-row"><span>Version</span><strong>' +
        esc(version) +
        "</strong></div>" +
        '<div class="dash-status-row"><span>Release</span><strong>v' +
        esc(version) +
        "</strong></div>" +
        '<div class="muted">Customer Portal presentation layer</div>';
    }

    if (hero) {
      hero.innerHTML =
        '<span class="bte-badge bte-badge-' +
        (apiOk ? "strong" : "avoid") +
        '">API ' +
        esc(apiLabel) +
        '</span><span class="bte-badge bte-badge-' +
        (portalOk ? "strong" : "avoid") +
        '">Portal ' +
        esc(portalLabel) +
        "</span>";
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
