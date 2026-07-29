(function () {
  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  function pad2(n) {
    return String(Number(n) || 0).padStart(2, "0");
  }

  function genderLabel(raw) {
    if (raw == null || raw === "") return t("analyze.gender_unspecified");
    var key = String(raw).toLowerCase();
    if (key === "male" || key === "nam" || key === "m") return t("analyze.gender_male");
    if (key === "female" || key === "nu" || key === "nữ" || key === "f") {
      return t("analyze.gender_female");
    }
    return String(raw);
  }

  function formatBirthMeta(input) {
    var date =
      pad2(input.day) + "/" + pad2(input.month) + "/" + String(input.year || "");
    var time = pad2(input.hour ?? 0) + ":" + pad2(input.minute ?? 0);
    var datetime = date + " " + time;
    var line1 = t("result.birth_meta_line", {
      date_label: t("result.birth_date_label"),
      datetime: datetime,
    });
    var line2 = t("result.birth_meta_gender", {
      gender_label: t("result.gender_label"),
      gender: genderLabel(input.gender),
    });
    return line1 + "\n" + line2;
  }

  function boot() {
    var meta = document.getElementById("resultMeta");
    var view = document.getElementById("stageView");
    var flash = document.getElementById("globalFlash");

    if (!window.BtePortal) {
      if (meta) meta.textContent = t("common.api_client_failed_api_js");
      if (view) view.textContent = "";
      return;
    }

    // Analyze already persisted {input, data} in ResultStore before navigate.
    // Do NOT re-POST /analyze here — that breaks the workflow when API/proxy fails.
    var last = BtePortal.ResultStore.loadForView();
    if (!last || !last.data) {
      if (meta) meta.textContent = t("result.empty");
      if (view) view.innerHTML = '<p class="muted">' + t("result.empty") + "</p>";
      return;
    }

    var data = last.data;
    var input = last.input || {};
    // Debug mode: set window.__BTE_DEBUG__ = true in browser console to enable full pipeline trace.
    var debugEnabled = !!(window.__BTE_DEBUG__);
    function debugLog(stage, payload) {
      if (!debugEnabled || !window.console) return;
      try {
        console.debug("[BTE Debug]", stage, payload);
      } catch (_) { /* ignore */ }
    }

    // Always expose pipeline data under window.__BTE_TRACE__ for DevTools inspection.
    try {
      window.__BTE_TRACE__ = {
        store: last,
        data_keys: Object.keys(data || {}),
        pattern: data.pattern || null,
        score: data.score || null,
        interpretation: {
          section_count: (data.interpretation && data.interpretation.section_count) || 0,
          sections: (data.interpretation && data.interpretation.sections) || [],
          confidence: (data.interpretation && data.interpretation.confidence) || null,
        },
        calendar: data.calendar ? "present" : "missing",
        bazi: data.bazi ? "present" : "missing",
        report: data.narrative ? "present" : "missing",
      };
    } catch (_) { /* ignore */ }

    // Always log basic check (not gated by debug flag) so DevTools always shows pipeline summary.
    if (window.console && window.console.info) {
      try {
        console.info("[BTE Pipeline] stages=%o pattern_keys=%o score_total=%o interp_sections=%o | set window.__BTE_DEBUG__=true for full trace",
          Object.keys(data || {}),
          Object.keys(data.pattern || {}),
          data.score && data.score.total_score,
          data.interpretation && data.interpretation.section_count
        );
      } catch (_) { /* ignore */ }
    }
    debugLog("frontend_state_loaded", {
      has_calendar: !!data.calendar,
      has_bazi: !!data.bazi,
      has_pattern: !!data.pattern,
      has_score: !!data.score,
      has_interpretation: !!data.interpretation,
      interpretation_section_count:
        (data.interpretation && data.interpretation.section_count) || 0,
      pattern_keys: Object.keys(data.pattern || {}),
    });
    if (meta) {
      meta.textContent = formatBirthMeta(input);
      meta.classList.add("result-meta-friendly");
    }

    var chartHost = document.getElementById("chartInfoHost");
    if (chartHost && window.BtePresenters && BtePresenters.chartHeader) {
      chartHost.hidden = false;
      chartHost.innerHTML = BtePresenters.chartHeader(data, {
        input: input,
        titleKey: "chart.info_title",
      });
    }

    function show(stage) {
      document.querySelectorAll(".tab").forEach(function (tab) {
        tab.classList.toggle("active", tab.getAttribute("data-stage") === stage);
      });
      var payload = data[stage];
      var presenters = window.BtePresenters || {};
      debugLog("ui_render_start", {
        stage: stage,
        payload_keys: payload && typeof payload === "object" ? Object.keys(payload) : [],
      });

      var map = {
        calendar: presenters.calendar,
        bazi: presenters.bazi,
        pattern: presenters.pattern,
        score: presenters.score,
        interpretation: presenters.interpretation,
        narrative: presenters.narrative,
      };

      if (map[stage]) {
        view.classList.remove("pre");
        view.classList.add("stage-view");
        if (stage === "calendar") {
          view.innerHTML = map[stage](payload, {
            timezone: input.timezone || null,
          });
        } else if (stage === "narrative") {
          var narrativeHtml = map[stage](payload);
          var execHtml =
            presenters.executive && data
              ? presenters.executive(data, {
                  input: input,
                  chartTitleKey: "executive.basic",
                  includeLunar: true,
                })
              : "";
          view.innerHTML =
            (execHtml || "") +
            (execHtml ? '<hr class="bte-exec-page-break" />' : "") +
            narrativeHtml;
        } else {
          view.innerHTML = map[stage](payload);
        }
        debugLog("ui_render_done", {
          stage: stage,
          rendered: true,
          html_length: (view.innerHTML || "").length,
        });
        if (stage === "narrative" && presenters.bindNarrative) {
          presenters.bindNarrative(view);
        }
        return;
      }

      if (
        stage === "calendar" ||
        stage === "bazi" ||
        stage === "pattern" ||
        stage === "score" ||
        stage === "interpretation" ||
        stage === "narrative"
      ) {
        view.classList.remove("pre");
        view.classList.add("stage-view");
        view.innerHTML =
          '<p class="muted">' + t("result.presenter_failed." + stage) + "</p>";
        debugLog("ui_render_done", {
          stage: stage,
          rendered: false,
          reason: "missing_presenter",
        });
        return;
      }

      view.classList.remove("pre");
      view.classList.add("stage-view");
      view.innerHTML = '<p class="muted">' + t("result.no_stage_data") + "</p>";
      debugLog("ui_render_done", {
        stage: stage,
        rendered: false,
        reason: "missing_stage_data",
      });
    }

    document.querySelectorAll(".tab").forEach(function (btn) {
      btn.addEventListener("click", function () {
        show(btn.getAttribute("data-stage"));
      });
    });
    show("calendar");
    BtePortal.showFlash(flash, t("result.showing_latest"), "success");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
