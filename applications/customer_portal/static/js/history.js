(function () {
  const list = document.getElementById("historyList");
  const flash = document.getElementById("globalFlash");

  function render() {
    const items = BtePortal.getHistory();
    if (!items.length) {
      list.innerHTML = '<p class="muted">No local history yet.</p>';
      return;
    }
    list.innerHTML = items
      .map((item, idx) => {
        const input = item.input || {};
        const label =
          [input.year, input.month, input.day].filter(Boolean).join("-") ||
          item.id;
        return (
          '<div class="list-item">' +
          "<div><strong>" +
          label +
          '</strong><div class="muted">' +
          (item.saved_at || "") +
          " · " +
          (item.summary || "") +
          "</div></div>" +
          '<button type="button" data-idx="' +
          idx +
          '">Open result</button>' +
          "</div>"
        );
      })
      .join("");

    list.querySelectorAll("button[data-idx]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const item = items[Number(btn.getAttribute("data-idx"))];
        BtePortal.saveLastResult({ input: item.input, data: item.data });
        // saveLastResult also prepends history — trim duplicate by rewriting without double push
        // Overwrite last only:
        sessionStorage.setItem(
          "bte_portal_last_result",
          JSON.stringify({ input: item.input, data: item.data })
        );
        window.location.href = "/result";
      });
    });
  }

  document.getElementById("btnClearHist").addEventListener("click", () => {
    sessionStorage.removeItem("bte_portal_history");
    BtePortal.showFlash(flash, "History cleared", "success");
    render();
  });

  render();
})();
