(function () {
  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  const list = document.getElementById("historyList");
  const flash = document.getElementById("globalFlash");
  const summary = document.getElementById("historySummary");

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

  function birthDateLabel(input) {
    if (!input || typeof input !== "object") return "—";
    if (input.day == null || input.month == null || input.year == null) return "—";
    return pad(input.day) + "/" + pad(input.month) + "/" + String(input.year);
  }

  function birthTimeLabel(input) {
    if (!input || typeof input !== "object" || input.hour == null || input.hour === "") return "—";
    return pad(Number(input.hour) || 0) + ":" + pad(Number(input.minute) || 0);
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
      if (summary) summary.innerHTML = "";
      list.innerHTML = window.BteUI
        ? BteUI.emptyState(t("history.empty"), t("common.new_analyze"))
        : '<p class="muted">' + t("history.empty") + "</p>";
      return;
    }
    const archiveNumbers = items
      .map(function (item) { return Number(item.archive_number) || 0; })
      .filter(Boolean);
    const latestNumber = archiveNumbers.length ? Math.max.apply(null, archiveNumbers) : items.length;
    if (summary) {
      summary.innerHTML =
        '<div><strong>' + esc(items.length) + '</strong><span> hồ sơ đã lưu</span></div>' +
        '<div class="muted">Số lưu trữ: 001 - ' + esc(String(latestNumber).padStart(3, "0")) + '</div>';
    }
    const rows = items
      .map(function (item, idx) {
        const input = item.input || {};
        const name = input.full_name || t("history.unnamed");
        const when = formatWhen(item.created_at || item.saved_at);
        const analysisId = item.analysis_id || item.id || "";
        const legacy = versionNote(item);
        const corrupt = !item.data || typeof item.data !== "object";
        const archiveCode = item.archive_code || String(item.archive_number || items.length - idx).padStart(3, "0");
        return (
          '<tr data-history-idx="' +
          idx +
          '"' +
          (analysisId ? ' data-analysis-id="' + esc(analysisId) + '"' : "") +
          ">" +
          '<td class="history-record-number">' + esc(archiveCode) + "</td>" +
          '<td class="history-run-time">' + esc(when || "—") + "</td>" +
          '<td class="history-name"><strong>' + esc(name) + "</strong>" +
          (legacy ? " · " + esc(legacy) : "") +
          (corrupt ? " · " + esc(t("history.corrupt_badge")) : "") +
          "</td>" +
          '<td class="history-birth-date">' + esc(birthDateLabel(input)) + "</td>" +
          '<td class="history-birth-time">' + esc(birthTimeLabel(input)) + "</td>" +
          '<td class="history-analysis-id">' + esc(analysisId || "—") + "</td>" +
          '<td class="history-actions">' +
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
          '<button type="button" class="secondary history-delete" data-delete-idx="' +
          idx +
          '">Xóa</button>' +
          "</td></tr>"
        );
      })
      .join("");
    list.innerHTML =
      '<div class="history-table-wrap"><table class="history-table">' +
      '<thead><tr><th>STT</th><th>Thời gian</th><th>Họ và tên</th>' +
      '<th>Ngày tháng năm sinh</th><th>Giờ sinh</th><th>Mã phân tích</th><th>Thao tác</th></tr></thead>' +
      "<tbody>" + rows + "</tbody></table></div>";

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

    list.querySelectorAll("button[data-delete-idx]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        const item = items[Number(btn.getAttribute("data-delete-idx"))];
        const analysisId = item && (item.analysis_id || item.id);
        if (!analysisId) return;
        const archiveCode = item.archive_code || String(item.archive_number || "").padStart(3, "0");
        if (!window.confirm("Bạn có chắc muốn xóa hồ sơ " + archiveCode + "? Thao tác này không thể hoàn tác.")) {
          return;
        }
        if (!BtePortal.ResultStore.deleteHistory(analysisId)) return;
        BtePortal.showFlash(flash, "Đã xóa hồ sơ " + archiveCode + ".", "success");
        render();
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
