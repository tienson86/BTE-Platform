(function () {
  function boot() {
    const meta = document.getElementById("resultMeta");
    const view = document.getElementById("stageView");
    const flash = document.getElementById("globalFlash");

    if (!window.BtePortal) {
      if (meta) meta.textContent = "Portal API client failed to load (api.js).";
      if (view) view.textContent = "{}";
      return;
    }

    const last = BtePortal.getLastResult();
    if (!last || !last.data) {
      meta.textContent = "No result yet — run Analyze first.";
      view.textContent = "{}";
      return;
    }

    const data = last.data;
    const input = last.input || {};
    meta.textContent =
      "Birth " +
      [input.year, input.month, input.day].join("-") +
      " " +
      String(input.hour ?? 0).padStart(2, "0") +
      ":" +
      String(input.minute ?? 0).padStart(2, "0") +
      " · pipeline: " +
      ((data.pipeline || []).join(" → ") || "analyze");

    function show(stage) {
      document.querySelectorAll(".tab").forEach((t) => {
        t.classList.toggle("active", t.getAttribute("data-stage") === stage);
      });
      const payload = data[stage];
      view.textContent =
        payload === undefined ? "No data for stage: " + stage : BtePortal.fmt(payload);
    }

    document.querySelectorAll(".tab").forEach((btn) => {
      btn.addEventListener("click", () => show(btn.getAttribute("data-stage")));
    });
    show("calendar");
    BtePortal.showFlash(flash, "Showing latest analyze result", "success");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
