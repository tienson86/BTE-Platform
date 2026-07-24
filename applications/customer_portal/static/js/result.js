(function () {
  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  function boot() {
    const meta = document.getElementById("resultMeta");
    const view = document.getElementById("stageView");
    const flash = document.getElementById("globalFlash");

    if (!window.BtePortal) {
      if (meta) meta.textContent = t("common.api_client_failed_api_js");
      if (view) view.textContent = "{}";
      return;
    }

    const last = BtePortal.getLastResult();
    if (!last || !last.data) {
      meta.textContent = t("result.empty");
      view.innerHTML = '<p class="muted">' + t("result.empty") + "</p>";
      return;
    }

    const data = last.data;
    const input = last.input || {};
    meta.textContent = t("result.birth_meta", {
      date: [input.year, input.month, input.day].join("-"),
      time:
        String(input.hour ?? 0).padStart(2, "0") +
        ":" +
        String(input.minute ?? 0).padStart(2, "0"),
      pipeline: (data.pipeline || []).join(" → ") || t("result.pipeline_fallback"),
    });

    function show(stage) {
      document.querySelectorAll(".tab").forEach((tab) => {
        tab.classList.toggle("active", tab.getAttribute("data-stage") === stage);
      });
      const payload = data[stage];
      const presenters = window.BtePresenters || {};

      const map = {
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
        } else {
          view.innerHTML = map[stage](payload);
        }
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
        return;
      }

      view.classList.add("pre");
      view.classList.remove("stage-view");
      view.textContent =
        payload === undefined
          ? t("result.no_stage_data", { stage: stage })
          : BtePortal.fmt(payload);
    }

    document.querySelectorAll(".tab").forEach((btn) => {
      btn.addEventListener("click", () => show(btn.getAttribute("data-stage")));
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
