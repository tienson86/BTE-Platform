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
      if (!Number.isFinite(input.year) || input.year < 1) return t("analyze.year_required");
      if (!Number.isFinite(input.month) || input.month < 1 || input.month > 12) {
        return t("analyze.month_range");
      }
      if (!Number.isFinite(input.day) || input.day < 1 || input.day > 31) {
        return t("analyze.day_range");
      }
      return "";
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
      btn.textContent = t("analyze.analyzing");
      BtePortal.showFlash(flash, t("analyze.calling"), "success");

      try {
        const res = await BtePortal.post("/api/v1/analyze", input);
        const data = res && res.data != null ? res.data : res;
        if (!data || typeof data !== "object") {
          throw new Error(t("analyze.missing_payload"));
        }
        BtePortal.saveLastResult({ input: input, data: data });
        BtePortal.showFlash(flash, t("analyze.complete"), "success");
        window.location.assign("/result");
      } catch (err) {
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
