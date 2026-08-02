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
    var tabsHost = document.getElementById("stageTabs");

    if (!window.BtePortal) {
      if (meta) meta.textContent = t("common.api_client_failed_api_js");
      if (view) view.textContent = "";
      return;
    }

    var last = BtePortal.ResultStore.loadForView();
    if (!last || !last.data) {
      if (meta) meta.textContent = t("result.empty");
      if (view) {
        view.innerHTML = window.BteUI
          ? BteUI.emptyState(t("result.empty"), t("common.new_analyze"))
          : '<p class="muted">' + t("result.empty") + "</p>";
      }
      return;
    }

    var data = last.data;
    var input = last.input || {};
    var debugEnabled = !!(window.__BTE_DEBUG__);
    function debugLog(stage, payload) {
      if (!debugEnabled || !window.console) return;
      try {
        console.debug("[BTE Debug]", stage, payload);
      } catch (_) {}
    }

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
      };
    } catch (_) {}

    if (meta) {
      meta.textContent = formatBirthMeta(input);
      meta.classList.add("result-meta-friendly");
    }

    var presenters = window.BtePresenters || {};
    var modules =
      window.BteModules && typeof BteModules.listEnabled === "function"
        ? BteModules.listEnabled()
        : [
            { id: "basic", labelKey: "stages.basic" },
            { id: "calendar", labelKey: "stages.calendar" },
            { id: "bazi", labelKey: "stages.bazi" },
            { id: "score", labelKey: "stages.score" },
            { id: "interpretation", labelKey: "stages.interpretation" },
            { id: "discussion", labelKey: "stages.discussion" },
          ];

    var map = {
      basic: presenters.basicInfo,
      calendar: presenters.calendar,
      bazi: presenters.bazi,
      score: presenters.score,
      interpretation: presenters.interpretation,
      discussion: presenters.discussion,
    };

    if (tabsHost) {
      tabsHost.innerHTML = modules
        .map(function (mod, index) {
          return (
            '<button type="button" class="tab' +
            (index === 0 ? " active" : "") +
            '" role="tab" data-stage="' +
            mod.id +
            '" data-i18n="' +
            mod.labelKey +
            '">' +
            t(mod.labelKey) +
            "</button>"
          );
        })
        .join("");
      if (window.BteI18n) BteI18n.apply(tabsHost);
    }

    function show(stage) {
      document.querySelectorAll("#stageTabs .tab").forEach(function (tab) {
        var active = tab.getAttribute("data-stage") === stage;
        tab.classList.toggle("active", active);
        tab.setAttribute("aria-selected", active ? "true" : "false");
      });

      debugLog("ui_render_start", { stage: stage });

      if (map[stage]) {
        view.classList.remove("pre");
        view.classList.add("stage-view");
        var html = "";
        if (stage === "basic") {
          html = map[stage](data, { input: input });
        } else if (stage === "calendar") {
          html = map[stage](data.calendar, {
            timezone: input.timezone || null,
            data: data,
          });
        } else if (stage === "bazi") {
          html = map[stage](data.bazi, { data: data });
        } else if (stage === "score") {
          html = map[stage](data.score, { data: data, input: input });
        } else if (stage === "interpretation") {
          html = map[stage](data.interpretation, { data: data });
        } else if (stage === "discussion") {
          html = map[stage](data.narrative || data.report, {
            data: data,
            input: input,
          });
        } else {
          html = map[stage](data[stage]);
        }
        view.innerHTML = html;
        if (window.BteUI) BteUI.bindCollapsible(view);
        if (stage === "discussion" && presenters.bindNarrative) {
          presenters.bindNarrative(view);
        }
        if (stage === "discussion" && presenters.bindDiscussionExpert) {
          presenters.bindDiscussionExpert(view, { data: data, input: input });
        }
        return;
      }

      view.innerHTML =
        '<p class="muted">' + t("result.presenter_failed." + stage) + "</p>";
    }

    document.querySelectorAll("#stageTabs .tab").forEach(function (btn) {
      btn.addEventListener("click", function () {
        show(btn.getAttribute("data-stage"));
      });
    });
    show(modules[0] ? modules[0].id : "basic");
    BtePortal.showFlash(flash, t("result.showing_latest"), "success");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
