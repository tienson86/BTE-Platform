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
    var host = document.getElementById("reportHost");
    var flash = document.getElementById("globalFlash");

    if (!window.BtePortal) {
      if (meta) meta.textContent = t("common.api_client_failed_api_js");
      if (host) host.textContent = "";
      return;
    }

    var last = BtePortal.ResultStore.loadForView();
    if (!last || !last.data) {
      if (meta) meta.textContent = t("result.empty");
      if (host) {
        host.innerHTML = window.BteUI
          ? BteUI.emptyState(t("result.empty"), t("common.new_analyze"))
          : '<p class="muted">' + t("result.empty") + "</p>";
      }
      return;
    }

    var data = last.data;
    var input = last.input || {};

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
        report_ia: "phase2_v1",
      };
    } catch (_) {}

    if (meta) {
      meta.textContent = formatBirthMeta(input);
      meta.classList.add("result-meta-friendly");
    }

    if (!window.BteReportModel || !window.BteReportRender) {
      if (host) {
        host.innerHTML =
          '<p class="muted">' + t("result.presenter_failed.basic") + "</p>";
      }
      return;
    }

    var model = BteReportModel.build(data, { input: input });
    host.classList.remove("rpt-skeleton");
    host.innerHTML = BteReportRender.render(model);
    BteReportRender.bind(host);

    if (window.BteScrollSpy) BteScrollSpy.bind(host);

    var presenters = window.BtePresenters || {};
    if (presenters.bindNarrative) presenters.bindNarrative(host);
    if (presenters.bindDiscussionExpert) {
      presenters.bindDiscussionExpert(host, { data: data, input: input });
    }

    BtePortal.showFlash(flash, t("result.showing_latest"), "success");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
