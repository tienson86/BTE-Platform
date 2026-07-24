(function () {
  function boot() {
    const flash = document.getElementById("globalFlash");
    const form = document.getElementById("analyzeForm");
    const btn = document.getElementById("btnAnalyze");

    if (!window.BtePortal) {
      if (flash) {
        flash.textContent = "Portal API client failed to load (api.js).";
        flash.className = "flash show error";
      }
      return;
    }
    if (!form || !btn) {
      BtePortal.showFlash(flash, "Analyze form not found in page.", "error");
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
      if (!Number.isFinite(input.year) || input.year < 1) return "Year is required.";
      if (!Number.isFinite(input.month) || input.month < 1 || input.month > 12) {
        return "Month must be 1–12.";
      }
      if (!Number.isFinite(input.day) || input.day < 1 || input.day > 31) {
        return "Day must be 1–31.";
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
      btn.textContent = "Analyzing...";
      BtePortal.showFlash(flash, "Calling POST /backend/api/v1/analyze ...", "success");

      try {
        const res = await BtePortal.post("/api/v1/analyze", input);
        const data = res && res.data != null ? res.data : res;
        if (!data || typeof data !== "object") {
          throw new Error("Analyze response missing data payload.");
        }
        BtePortal.saveLastResult({ input: input, data: data });
        BtePortal.showFlash(flash, "Analyze complete — opening Result", "success");
        window.location.assign("/result");
      } catch (err) {
        const message = (err && err.message) || "Analyze failed";
        BtePortal.showFlash(flash, message, "error");
        btn.disabled = false;
        btn.textContent = "Run analyze";
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
