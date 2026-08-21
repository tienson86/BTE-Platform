(function () {
  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  const list = document.getElementById("historyList");
  const flash = document.getElementById("globalFlash");

  function esc(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function pad(value) {
    return String(value).padStart(2, "0");
  }

  function birthLabel(input) {
    if (!input || typeof input !== "object") return "";
    const date = [input.year, input.month, input.day]
      .filter(function (part) {
        return part != null && part !== "";
      })
      .join("-");
    if (!date) return "";
    const hour = input.hour;
    const minute = input.minute;
    if (hour == null || hour === "") return date;
    return date + " " + pad(Number(hour) || 0) + ":" + pad(Number(minute) || 0);
  }

  function formatWhen(iso) {
    if (!iso) return "";
    const date = new Date(iso);
    if (Number.isNaN(date.getTime())) return String(iso);
    try {
      return date.toLocaleString("vi-VN");
    } catch (_) {
      return String(iso);
    }
  }

  function reanalyzeHref(input) {
    if (!input || typeof input !== "object") return "/analyze";
    const params = new URLSearchParams();
    params.set("reanalyze", "1");
    ["full_name", "birth_place", "year", "month", "day", "hour", "minute", "gender", "timezone"].forEach(
      function (key) {
        if (input[key] == null || String(input[key]).trim() === "") return;
        params.set(key, String(input[key]));
      },
    );
    return "/analyze?" + params.toString();
  }

  function versionNote(item) {
    if (item && item.customer_contract) return "";
    return t("history.legacy_badge");
  }

  function render() {
    const items = BtePortal.getHistory();
    if (!items.length) {
      list.innerHTML = window.BteUI
        ? BteUI.emptyState(t("history.empty"), t("common.new_analyze"))
        : '<p class="muted">' + t("history.empty") + "</p>";
      return;
    }
    list.innerHTML = items
      .map(function (item, idx) {
        const input = item.input || {};
        const name = input.full_name || t("history.unnamed");
        const birth = birthLabel(input);
        const when = formatWhen(item.created_at || item.saved_at);
        const analysisId = item.analysis_id || item.id || "";
        const legacy = versionNote(item);
        const corrupt = !item.data || typeof item.data !== "object";
        return (
          '<div class="list-item bte-card" data-history-idx="' +
          idx +
          '"' +
          (analysisId ? ' data-analysis-id="' + esc(analysisId) + '"' : "") +
          ">" +
          "<div>" +
          "<strong>" +
          esc(name) +
          "</strong>" +
          (birth ? '<div class="muted">' + esc(birth) + "</div>" : "") +
          '<div class="muted">' +
          esc(when) +
          (analysisId ? " · " + esc(analysisId) : "") +
          (legacy ? " · " + esc(legacy) : "") +
          (corrupt ? " · " + esc(t("history.corrupt_badge")) : "") +
          "</div></div>" +
          '<div class="history-actions">' +
          '<button type="button" class="secondary" data-open-idx="' +
          idx +
          '">' +
          t("history.open_result") +
          "</button>" +
          '<a class="btn secondary" href="' +
          esc(reanalyzeHref(input)) +
          '">' +
          t("history.reanalyze") +
          "</a>" +
          "</div></div>"
        );
      })
      .join("");

    list.querySelectorAll("button[data-open-idx]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        const item = items[Number(btn.getAttribute("data-open-idx"))];
        const analysisId = item && (item.analysis_id || item.id);
        if (!analysisId) return;
        BtePortal.ResultStore.selectForView({
          input: item.input || {},
          data: item.data,
          analysis_id: analysisId,
        });
        window.location.href =
          "/result?from=history&id=" + encodeURIComponent(String(analysisId));
      });
    });
  }

  document.getElementById("btnClearHist").addEventListener("click", function () {
    BtePortal.ResultStore.clearHistory();
    BtePortal.showFlash(flash, t("history.cleared"), "success");
    render();
  });

  render();
})();
