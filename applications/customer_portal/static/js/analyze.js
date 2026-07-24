(function () {
  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  function boot() {
    const flash = document.getElementById("globalFlash");
    const form = document.getElementById("analyzeForm");
    const btn = document.getElementById("btnAnalyze");

    if (!window.BtePortal) {
      if (flash) {
        flash.textContent = t("common.api_client_failed_api_js");
        flash.className = "flash show error";
      }
      return;
    }
    if (!form || !btn) {
      BtePortal.showFlash(flash, t("analyze.form_missing"), "error");
      return;
    }

    function readInput() {
      return {
        full_name: String(document.getElementById("full_name").value || "").trim(),
        birth_place: String(document.getElementById("birth_place").value || "").trim(),
        year: Number(document.getElementById("year").value),
        month: Number(document.getElementById("month").value),
        day: Number(document.getElementById("day").value),
        hour: Number(document.getElementById("hour").value || 0),
        minute: Number(document.getElementById("minute").value || 0),
        gender: document.getElementById("gender").value || null,
        timezone: document.getElementById("timezone").value || "Asia/Ho_Chi_Minh",
      };
    }

    function validate(input) {
      if (!input.full_name) return t("analyze.full_name_required");
      if (!input.birth_place) return t("analyze.birth_place_required");
      if (!Number.isFinite(input.year) || input.year < 1) return t("analyze.year_required");
      if (!Number.isFinite(input.month) || input.month < 1 || input.month > 12) {
        return t("analyze.month_range");
      }
      if (!Number.isFinite(input.day) || input.day < 1 || input.day > 31) {
        return t("analyze.day_range");
      }
      return "";
    }

    function startFriendlyLoading() {
      var steps = [
        "analyze.loading_chart",
        "analyze.loading_bazi",
        "analyze.loading_narrative",
      ];
      var index = 0;
      function showStep() {
        var key = steps[Math.min(index, steps.length - 1)];
        var text = t(key);
        btn.textContent = text;
        BtePortal.showFlash(flash, text, "success");
        index += 1;
      }
      showStep();
      return setInterval(showStep, 900);
    }

    async function runAnalyze(event) {
      if (event) event.preventDefault();
      const input = readInput();
      const invalid = validate(input);
      if (invalid) {
        BtePortal.showFlash(flash, invalid, "error");
        return;
      }

      btn.disabled = true;
      var loadingTimer = startFriendlyLoading();

      try {
        const res = await BtePortal.post("/api/v1/analyze", input);
        const data = res && res.data != null ? res.data : res;
        if (!data || typeof data !== "object") {
          throw new Error(t("analyze.missing_payload"));
        }
        clearInterval(loadingTimer);
        btn.textContent = t("analyze.loading_done");
        BtePortal.showFlash(flash, t("analyze.loading_done"), "success");
        BtePortal.saveLastResult({ input: input, data: data });
        window.location.assign("/result");
      } catch (err) {
        clearInterval(loadingTimer);
        const message = (err && err.message) || t("analyze.failed");
        BtePortal.showFlash(flash, message, "error");
        btn.disabled = false;
        btn.textContent = t("analyze.run");
      }
    }

    btn.addEventListener("click", runAnalyze);
    form.addEventListener("submit", runAnalyze);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
