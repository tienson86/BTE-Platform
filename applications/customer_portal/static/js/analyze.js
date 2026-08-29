(function () {
  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  function pad2(value) {
    return String(value).padStart(2, "0");
  }

  function boot() {
    const flash = document.getElementById("globalFlash");
    const form = document.getElementById("analyzeForm");
    const btn = document.getElementById("btnAnalyze");
    const status = document.getElementById("analyzeStatus");
    const timeWarn = document.getElementById("analyzeTimeWarn");

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

    function selectedGender() {
      var checked = form.querySelector('input[name="gender"]:checked');
      return checked ? checked.value : "";
    }

    function parseBirthDate() {
      var raw = String((document.getElementById("birth_date") || {}).value || "").trim();
      var match = raw.match(/^(\d{4})-(\d{2})-(\d{2})$/);
      if (!match) return null;
      return {
        year: Number(match[1]),
        month: Number(match[2]),
        day: Number(match[3]),
      };
    }

    function parseBirthTime() {
      var raw = String((document.getElementById("birth_time") || {}).value || "").trim();
      if (!raw) return { hour: 0, minute: 0, missing: true };
      var match = raw.match(/^(\d{1,2}):(\d{2})/);
      if (!match) return { hour: 0, minute: 0, missing: true };
      return {
        hour: Number(match[1]),
        minute: Number(match[2]),
        missing: false,
      };
    }

    function prefillFromQuery() {
      var params;
      try {
        params = new URLSearchParams(window.location.search || "");
      } catch (_) {
        return;
      }
      if (params.get("reanalyze") !== "1") return;
      var nameEl = document.getElementById("full_name");
      var placeEl = document.getElementById("birth_place");
      var dateEl = document.getElementById("birth_date");
      var timeEl = document.getElementById("birth_time");
      var tzEl = document.getElementById("timezone");
      if (nameEl && params.has("full_name")) nameEl.value = params.get("full_name") || "";
      if (placeEl && params.has("birth_place")) placeEl.value = params.get("birth_place") || "";
      if (tzEl && params.has("timezone") && params.get("timezone")) tzEl.value = params.get("timezone");
      if (dateEl && params.has("year") && params.has("month") && params.has("day")) {
        dateEl.value = params.get("year") + "-" + pad2(params.get("month")) + "-" + pad2(params.get("day"));
      }
      if (timeEl && (params.has("hour") || params.has("minute"))) {
        timeEl.value = pad2(params.get("hour") || "0") + ":" + pad2(params.get("minute") || "0");
      }
      var gender = params.get("gender") || "";
      if (gender) {
        var radio = form.querySelector('input[name="gender"][value="' + gender + '"]');
        if (radio) radio.checked = true;
      }
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
      var err = document.getElementById("err_" + id.replace(/^gender_male$|^gender_female$/, "gender"));
      if (id === "gender") {
        form.querySelectorAll('input[name="gender"]').forEach(function (el) {
          el.setAttribute("aria-invalid", "true");
        });
        err = document.getElementById("err_gender");
      } else if (input) {
        input.setAttribute("aria-invalid", "true");
      }
      if (err) {
        err.hidden = false;
        err.textContent = message;
      }
    }

    function readInput() {
      var date = parseBirthDate();
      var time = parseBirthTime();
      var tzEl = document.getElementById("timezone");
      return {
        full_name: String((document.getElementById("full_name") || {}).value || "").trim() || null,
        birth_place: String((document.getElementById("birth_place") || {}).value || "").trim() || null,
        year: date ? date.year : NaN,
        month: date ? date.month : NaN,
        day: date ? date.day : NaN,
        hour: time.hour,
        minute: time.minute,
        time_missing: time.missing,
        gender: selectedGender() || null,
        timezone: (tzEl && tzEl.value) || "Asia/Ho_Chi_Minh",
      };
    }

    function validate(input) {
      clearFieldErrors();
      var first = "";
      if (!input.gender) {
        first = t("analyze.gender_required");
        setFieldError("gender", first);
      }
      if (!Number.isFinite(input.year) || !Number.isFinite(input.month) || !Number.isFinite(input.day)) {
        var dateMsg = t("analyze.date_required");
        setFieldError("birth_date", dateMsg);
        if (!first) first = dateMsg;
      }
      if (timeWarn) timeWarn.hidden = !input.time_missing;
      return first;
    }

    function setLoading(on, message) {
      btn.disabled = on;
      form.setAttribute("aria-busy", on ? "true" : "false");
      if (status) {
        status.hidden = !on;
        status.textContent = on ? message || t("analyze.analyzing") : "";
      }
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
        var text = t(steps[Math.min(index, steps.length - 1)]);
        btn.textContent = text;
        if (status) {
          status.hidden = false;
          status.textContent = text;
        }
        index += 1;
      }
      showStep();
      return setInterval(showStep, 900);
    }

    var analyzing = false;

    async function runAnalyze(event) {
      if (event) event.preventDefault();
      if (analyzing) return;
      const input = readInput();
      const invalid = validate(input);
      if (invalid) {
        BtePortal.showFlash(flash, invalid, "error");
        return;
      }

      analyzing = true;
      setLoading(true, t("analyze.analyzing"));
      var loadingTimer = startFriendlyLoading();
      var payload = {
        full_name: input.full_name,
        birth_place: input.birth_place,
        year: input.year,
        month: input.month,
        day: input.day,
        hour: input.hour,
        minute: input.minute,
        gender: input.gender,
        timezone: input.timezone,
      };

      try {
        const res = await BtePortal.post("/api/v1/analyze", payload);
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
        var saved = BtePortal.saveLastResult({
          input: payload,
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
        analyzing = false;
        clearInterval(loadingTimer);
        setLoading(false);
        const message = (err && err.message) || t("analyze.failed");
        BtePortal.showFlash(flash, message, "error");
      }
    }

    form.addEventListener("submit", runAnalyze);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
