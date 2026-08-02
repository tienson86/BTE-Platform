/**
 * Discussion + Knowledge Expert presentation.
 * 3-pane UX consumes existing POST /api/v1/discussion; narrative is fallback only.
 */
(function (global) {
  var MISSING = "--";

  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  function esc(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function show(value) {
    if (value === null || value === undefined || value === "") return MISSING;
    return String(value);
  }

  function pick(obj, keys) {
    if (!obj || typeof obj !== "object") return null;
    for (var i = 0; i < keys.length; i++) {
      if (
        Object.prototype.hasOwnProperty.call(obj, keys[i]) &&
        obj[keys[i]] != null &&
        obj[keys[i]] !== ""
      ) {
        return obj[keys[i]];
      }
    }
    return null;
  }

  function pillarText(pillar) {
    if (!pillar || typeof pillar !== "object") return MISSING;
    var stem = pick(pillar, ["stem", "thien_can", "can"]);
    var branch = pick(pillar, ["branch", "dia_chi", "chi"]);
    if (stem == null && branch == null) return MISSING;
    return show(stem) + " " + show(branch);
  }

  function contextStrip(data) {
    var payload = data && typeof data === "object" ? data : {};
    var bazi = payload.bazi && typeof payload.bazi === "object" ? payload.bazi : {};
    var pattern =
      payload.pattern && typeof payload.pattern === "object" ? payload.pattern : {};
    var useful =
      payload.useful_god && typeof payload.useful_god === "object"
        ? payload.useful_god
        : {};

    var pillars = [
      { label: t("executive.col_year"), value: pillarText(bazi.year_pillar) },
      { label: t("executive.col_month"), value: pillarText(bazi.month_pillar) },
      { label: t("executive.col_day"), value: pillarText(bazi.day_pillar) },
      { label: t("executive.col_hour"), value: pillarText(bazi.hour_pillar) },
    ];

    var dayMaster = show(
      pick(bazi, ["day_master", "dayMaster", "nhat_chu"]) ||
        (bazi.day_pillar && pick(bazi.day_pillar, ["stem", "thien_can"]))
    );
    var element = show(
      pick(bazi, ["day_master_element", "dayMasterElement", "element"])
    );
    var tenGods = Array.isArray(bazi.ten_gods)
      ? bazi.ten_gods.filter(Boolean).join(", ")
      : [
          bazi.year_pillar && bazi.year_pillar.ten_god,
          bazi.month_pillar && bazi.month_pillar.ten_god,
          bazi.day_pillar && bazi.day_pillar.ten_god,
          bazi.hour_pillar && bazi.hour_pillar.ten_god,
        ]
          .filter(Boolean)
          .join(", ");
    var shensha = Array.isArray(bazi.shensha)
      ? bazi.shensha
          .map(function (s) {
            return typeof s === "object" ? s.name || s.label || "" : s;
          })
          .filter(Boolean)
          .join(", ")
      : show(pick(bazi, ["shensha", "than_sat"]));
    var usefulGod = show(
      pick(pattern, ["dung_than", "useful_god", "yong_shen"]) ||
        pick(useful, ["dung_than", "useful_god", "primary", "name", "element"])
    );

    function chip(label, value) {
      return (
        '<div class="bte-discuss-chip">' +
        '<span class="bte-discuss-chip-k">' +
        esc(label) +
        "</span>" +
        '<span class="bte-discuss-chip-v">' +
        esc(value || MISSING) +
        "</span>" +
        "</div>"
      );
    }

    return (
      '<section class="bte-card bte-discuss-context" aria-label="' +
      esc(t("discussion.context_title")) +
      '">' +
      "<h3>" +
      esc(t("discussion.context_title")) +
      "</h3>" +
      '<p class="muted">' +
      esc(t("discussion.context_hint")) +
      "</p>" +
      '<div class="bte-discuss-chips">' +
      pillars
        .map(function (p) {
          return chip(p.label, p.value);
        })
        .join("") +
      chip(
        t("discussion.ref_elements"),
        dayMaster + (element !== MISSING ? " · " + element : "")
      ) +
      chip(t("discussion.ref_ten_gods"), tenGods || MISSING) +
      chip(t("discussion.ref_shensha"), shensha || MISSING) +
      chip(t("discussion.ref_useful_god"), usefulGod) +
      "</div>" +
      "</section>"
    );
  }

  function narrativeFallback(narrative) {
    var body = "";
    if (window.BtePresenters && typeof window.BtePresenters.narrative === "function") {
      body = window.BtePresenters.narrative(narrative);
      body = body
        .replace(
          /aria-label="[^"]*"/,
          'aria-label="' + esc(t("discussion.narrative_fallback")) + '"'
        )
        .replace(
          /<h2>[^<]*<\/h2>/,
          "<h2>" + esc(t("discussion.narrative_fallback")) + "</h2>"
        );
    } else {
      body =
        '<p class="muted">' +
        esc(t("discussion.empty")) +
        "</p>";
    }
    return (
      '<details class="bte-expert-fallback">' +
      "<summary>" +
      esc(t("discussion.narrative_fallback")) +
      "</summary>" +
      body +
      "</details>"
    );
  }

  function expertShell() {
    return (
      '<div class="bte-expert" data-expert-root>' +
      '<aside class="bte-expert-pane" data-pane="conversation">' +
      '<div class="bte-expert-pane-head">' +
      esc(t("discussion.pane_conversation")) +
      "</div>" +
      '<div class="bte-expert-pane-body" data-expert-thread></div>' +
      '<form class="bte-expert-composer" data-expert-form>' +
      '<input type="text" data-expert-input autocomplete="off" placeholder="' +
      esc(t("discussion.ask_placeholder")) +
      '" aria-label="' +
      esc(t("discussion.ask_placeholder")) +
      '" />' +
      '<button type="submit">' +
      esc(t("discussion.ask_send")) +
      "</button>" +
      "</form>" +
      "</aside>" +
      '<section class="bte-expert-pane" data-pane="answer">' +
      '<div class="bte-expert-pane-head">' +
      esc(t("discussion.pane_answer")) +
      "</div>" +
      '<div class="bte-expert-pane-body" data-expert-answer>' +
      '<p class="muted">' +
      esc(t("discussion.ask_hint")) +
      "</p>" +
      "</div>" +
      "</section>" +
      '<aside class="bte-expert-pane" data-pane="sources">' +
      '<div class="bte-expert-pane-head">' +
      esc(t("discussion.pane_sources")) +
      "</div>" +
      '<div class="bte-expert-pane-body" data-expert-sources>' +
      '<p class="muted">' +
      esc(t("discussion.sources_empty")) +
      "</p>" +
      "</div>" +
      "</aside>" +
      "</div>"
    );
  }

  /**
   * @param {object|null|undefined} narrative
   * @param {{ data?: object, input?: object }} [options]
   * @returns {string}
   */
  function renderDiscussion(narrative, options) {
    try {
      var full = (options && options.data) || {};
      return (
        '<div class="bte-discussion">' +
        '<header class="bte-calendar-head">' +
        "<h2>" +
        esc(t("discussion.expert_title")) +
        "</h2>" +
        '<p class="bte-calendar-sub">' +
        esc(t("discussion.subtitle")) +
        "</p>" +
        "</header>" +
        contextStrip(full) +
        expertShell() +
        narrativeFallback(narrative) +
        "</div>"
      );
    } catch (_) {
      return (
        '<div class="bte-discussion"><p class="muted">' +
        esc(MISSING) +
        "</p></div>"
      );
    }
  }

  function formatAnswer(text) {
    return esc(text || "").replace(/\n/g, "<br>");
  }

  function renderSources(payload) {
    var discussion = payload && payload.discussion;
    var summary = payload && payload.summary;
    var validation = payload && payload.validation;
    var parts = [];

    if (discussion && discussion.confidence != null) {
      var conf =
        typeof discussion.confidence === "number"
          ? discussion.confidence.toFixed(2)
          : String(discussion.confidence);
      parts.push(
        "<div><strong>" +
          esc(t("discussion.confidence")) +
          ":</strong> " +
          esc(conf) +
          "</div>"
      );
      if (window.BteUI) {
        var tone =
          discussion.grounded === false
            ? "warning"
            : discussion.refused
              ? "danger"
              : "success";
        parts.push(
          BteUI.statusBadge(
            discussion.refused
              ? "Refused"
              : discussion.grounded
                ? "Grounded"
                : "Ungrounded",
            tone
          )
        );
      }
    }

    if (summary && typeof summary === "object") {
      parts.push(
        '<ul class="bte-expert-meta">' +
          "<li>Evidence: " +
          esc(show(summary.evidence_count)) +
          "</li>" +
          "<li>Knowledge: " +
          esc(show(summary.knowledge_count)) +
          "</li>" +
          "<li>Validation: " +
          esc(
            summary.validation_passed === true
              ? "passed"
              : summary.validation_passed === false
                ? "failed"
                : MISSING
          ) +
          "</li>" +
          "</ul>"
      );
      if (Array.isArray(summary.reasoning_conclusions) && summary.reasoning_conclusions.length) {
        parts.push(
          "<div><strong>" +
            esc(t("discussion.related")) +
            "</strong><ul>" +
            summary.reasoning_conclusions
              .slice(0, 6)
              .map(function (c) {
                return "<li>" + esc(String(c)) + "</li>";
              })
              .join("") +
            "</ul></div>"
        );
      }
    }

    if (validation && validation.issues && validation.issues.length) {
      parts.push(
        "<details><summary>Validation notes</summary><ul>" +
          validation.issues
            .slice(0, 8)
            .map(function (issue) {
              return (
                "<li>" +
                esc(
                  typeof issue === "string"
                    ? issue
                    : issue.message || JSON.stringify(issue)
                ) +
                "</li>"
              );
            })
            .join("") +
          "</ul></details>"
      );
    }

    if (!parts.length) {
      return '<p class="muted">' + esc(t("discussion.sources_empty")) + "</p>";
    }
    return parts.join("");
  }

  function bindDiscussionExpert(root, options) {
    if (!root) return;
    var host = root.querySelector("[data-expert-root]");
    if (!host) return;

    var thread = host.querySelector("[data-expert-thread]");
    var answerEl = host.querySelector("[data-expert-answer]");
    var sourcesEl = host.querySelector("[data-expert-sources]");
    var form = host.querySelector("[data-expert-form]");
    var input = host.querySelector("[data-expert-input]");
    var birth = (options && options.input) || {};
    var busy = false;

    function appendMsg(role, text) {
      if (!thread) return;
      var div = document.createElement("div");
      div.className = "bte-expert-msg " + role;
      div.innerHTML = formatAnswer(text);
      thread.appendChild(div);
      thread.scrollTop = thread.scrollHeight;
    }

    function showError(err) {
      var message =
        (err && err.message) || t("discussion.expert_unavailable");
      var requestId =
        (err && err.payload && err.payload.request_id) ||
        (err && err.request_id) ||
        "";
      var details = "";
      try {
        if (err && err.payload) details = JSON.stringify(err.payload, null, 2);
      } catch (_) {}
      if (answerEl) {
        answerEl.innerHTML = window.BteUI
          ? BteUI.errorPanel(message, details, requestId) +
            '<p class="muted" style="margin-top:0.75rem">' +
            esc(t("discussion.expert_unavailable")) +
            "</p>"
          : '<p class="muted">' + esc(message) + "</p>";
        var retry = document.createElement("button");
        retry.type = "button";
        retry.className = "secondary";
        retry.textContent = "Retry";
        retry.addEventListener("click", function () {
          if (input && input.value) form.dispatchEvent(new Event("submit"));
        });
        answerEl.appendChild(retry);
      }
    }

    async function ask(question) {
      if (!window.BtePortal || typeof BtePortal.post !== "function") {
        showError(new Error(t("common.api_client_failed")));
        return;
      }
      busy = true;
      if (answerEl) {
        answerEl.innerHTML =
          '<div class="skeleton-line"></div><div class="skeleton-line"></div>';
      }
      try {
        var body = {
          year: Number(birth.year),
          month: Number(birth.month),
          day: Number(birth.day),
          hour: Number(birth.hour || 0),
          minute: Number(birth.minute || 0),
          gender: birth.gender || null,
          timezone: birth.timezone || "Asia/Ho_Chi_Minh",
          full_name: birth.full_name || null,
          birth_place: birth.birth_place || null,
          question: question,
          show_citations: false,
        };
        var res = await BtePortal.post("/api/v1/discussion", body);
        var data = res && res.data != null ? res.data : res;
        var discussion = data && data.discussion;
        var answerText =
          (discussion && discussion.answer) ||
          (data && data.message) ||
          t("discussion.empty");
        appendMsg("assistant", answerText);
        if (answerEl) {
          answerEl.innerHTML =
            '<div class="bte-expert-answer-body">' +
            formatAnswer(answerText) +
            "</div>";
        }
        if (sourcesEl) sourcesEl.innerHTML = renderSources(data);
        if (window.BteShell && typeof BteShell.toast === "function") {
          BteShell.toast(t("discussion.expert_title"), "success");
        }
      } catch (err) {
        showError(err);
      } finally {
        busy = false;
      }
    }

    if (form) {
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        if (busy) return;
        var q = input ? String(input.value || "").trim() : "";
        if (!q) return;
        appendMsg("user", q);
        if (input) input.value = "";
        ask(q);
      });
    }
  }

  global.BtePresenters = global.BtePresenters || {};
  global.BtePresenters.discussion = renderDiscussion;
  global.BtePresenters.bindDiscussionExpert = bindDiscussionExpert;
})(window);
