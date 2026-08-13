(function () {
  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  const list = document.getElementById("historyList");
  const flash = document.getElementById("globalFlash");

  function render() {
    const items = BtePortal.getHistory();
    if (!items.length) {
      list.innerHTML = window.BteUI
        ? BteUI.emptyState(t("history.empty"), t("common.new_analyze"))
        : '<p class="muted">' + t("history.empty") + "</p>";
      return;
    }
    list.innerHTML = items
      .map((item, idx) => {
        const input = item.input || {};
        const label =
          [input.year, input.month, input.day].filter(Boolean).join("-") ||
          item.id;
        return (
          '<div class="list-item bte-card">' +
          "<div><strong>" +
          label +
          '</strong><div class="muted">' +
          (item.saved_at || "") +
          " · " +
          (item.summary || "") +
          "</div></div>" +
          '<button type="button" data-idx="' +
          idx +
          '">' +
          t("history.open_result") +
          "</button>" +
          "</div>"
        );
      })
      .join("");

    list.querySelectorAll("button[data-idx]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const item = items[Number(btn.getAttribute("data-idx"))];
        // Opening a past chart must not rewrite the last Analyze result.
        BtePortal.ResultStore.selectForView({
          input: item.input || {},
          data: item.data,
          analysis_id: item.analysis_id || item.id,
        });
        window.location.href = "/result?from=history";
      });
    });
  }

  document.getElementById("btnClearHist").addEventListener("click", () => {
    BtePortal.ResultStore.clearHistory();
    BtePortal.showFlash(flash, t("history.cleared"), "success");
    render();
  });

  render();
})();
