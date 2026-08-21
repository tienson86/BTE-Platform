(function () {
  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  function boot() {
    const flash = document.getElementById("globalFlash");
    const form = document.getElementById("analyzeForm");
    const btn = document.getElementById("btnAnalyze");
    const loading = document.getElementById("analyzeLoading");

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

    function prefillFromQuery() {
      var params;
      try {
        params = new URLSearchParams(window.location.search || "");
      } catch (_) {
        return;
      }
      if (params.get("reanalyze") !== "1") return;
      ["full_name", "birth_place", "year", "month", "day", "hour", "minute", "gender", "timezone"].forEach(
        function (id) {
          var el = document.getElementById(id);
          if (!el || !params.has(id)) return;
          el.value = params.get(id) || "";
        },
      );
    }
    prefillFromQuery();

    function clearFieldErrors() {
      form.querySelectorAll(".field-error").forEach(function (el) {
        el.hidden = true;
        el.textContent = "";
      });
      form.querySelectorAll("[aria-invalid]").forEach(function (el) {
        el.removeAttribute("aria-invalid");
      });
    }

    function setFieldError(id, message) {
      var input = document.getElementById(id);
      var err = document.getElementById("err_" + id);
      if (input) input.setAttribute("aria-invalid", "true");
      if (err) {
        err.hidden = false;
        err.textContent = message;
      }
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
      clearFieldErrors();
      var first = "";
      if (!input.full_name) {
        first = t("analyze.full_name_required");
        setFieldError("full_name", first);
      }
      if (!input.birth_place) {
        var placeMsg = t("analyze.birth_place_required");
        setFieldError("birth_place", placeMsg);
        if (!first) first = placeMsg;
      }
      if (!Number.isFinite(input.year) || input.year < 1) {
        var yearMsg = t("analyze.year_required");
        if (!first) first = yearMsg;
      }
      if (!Number.isFinite(input.month) || input.month < 1 || input.month > 12) {
        var monthMsg = t("analyze.month_range");
        if (!first) first = monthMsg;
      }
      if (!Number.isFinite(input.day) || input.day < 1 || input.day > 31) {
        var dayMsg = t("analyze.day_range");
        if (!first) first = dayMsg;
      }
      return first;
    }

    function setLoading(on) {
      btn.disabled = on;
      if (loading) loading.hidden = !on;
      if (!on) btn.textContent = t("analyze.run");
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

      setLoading(true);
      var loadingTimer = startFriendlyLoading();

      try {
        const res = await BtePortal.post("/api/v1/analyze", input);
        const data = res && res.data != null ? res.data : res;
        if (!data || typeof data !== "object") {
          throw new Error(t("analyze.missing_payload"));
        }
        const analysisId =
          (data.analysis_id || data.request_id || (res && res.request_id) || "").toString().trim();
        if (analysisId && !data.analysis_id) {
          data.analysis_id = analysisId;
        }
        clearInterval(loadingTimer);
        btn.textContent = t("analyze.loading_done");
        BtePortal.showFlash(flash, t("analyze.loading_done"), "success");
        var saved = BtePortal.saveLastResult({
          input: input,
          data: data,
          analysis_id: analysisId || undefined,
        });
        if (!saved) {
          throw new Error(t("analyze.failed"));
        }
        var verify = BtePortal.ResultStore.load();
        if (!verify || !verify.data) {
          throw new Error(t("analyze.failed"));
        }
        window.location.assign("/result");
      } catch (err) {
        clearInterval(loadingTimer);
        setLoading(false);
        const message = (err && err.message) || t("analyze.failed");
        BtePortal.showFlash(flash, message, "error");
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
