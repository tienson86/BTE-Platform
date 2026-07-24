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
    const meta = document.getElementById("resultMeta");
    const view = document.getElementById("stageView");
    const flash = document.getElementById("globalFlash");

    if (!window.BtePortal) {
      if (meta) meta.textContent = t("common.api_client_failed_api_js");
      if (view) view.textContent = "";
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
    if (meta) {
      meta.textContent = formatBirthMeta(input);
      meta.classList.add("result-meta-friendly");
    }

    const chartHost = document.getElementById("chartInfoHost");
    if (chartHost && window.BtePresenters && BtePresenters.chartHeader) {
      chartHost.hidden = false;
      chartHost.innerHTML = BtePresenters.chartHeader(data, {
        input: input,
        titleKey: "chart.info_title",
      });
    }

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

      view.classList.remove("pre");
      view.classList.add("stage-view");
      view.innerHTML = '<p class="muted">' + t("result.no_stage_data") + "</p>";
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
