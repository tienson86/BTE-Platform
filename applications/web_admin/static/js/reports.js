(function () {
  const flash = document.getElementById("globalFlash");
  let current = null;

  async function loadReport() {
    const id = document.getElementById("reportCaseId").value.trim();
    if (!id) return;
    try {
      const data = await BteAdmin.get("/api/v1/cases/" + id);
      current = data.data && data.data.case;
      const html =
        (current.narrative_result && current.narrative_result.html) ||
        (current.report_result && current.report_result.html) ||
        "<p>No HTML content</p>";
      const md =
        (current.narrative_result && current.narrative_result.markdown) ||
        (current.report_result && current.report_result.markdown) ||
        "";
      const frame = document.getElementById("htmlView");
      frame.style.display = "block";
      document.getElementById("mdView").style.display = "none";
      frame.srcdoc = html;
      document.getElementById("mdView").textContent = md;
      BteAdmin.showFlash(flash, "Report loaded", "success");
    } catch (err) {
      BteAdmin.showFlash(flash, err.message, "error");
    }
  }

  document.getElementById("btnLoadReport").addEventListener("click", loadReport);
  document.getElementById("btnShowHtml").addEventListener("click", () => {
    document.getElementById("htmlView").style.display = "block";
    document.getElementById("mdView").style.display = "none";
  });
  document.getElementById("btnShowMd").addEventListener("click", () => {
    document.getElementById("htmlView").style.display = "none";
    document.getElementById("mdView").style.display = "block";
  });
  document.getElementById("btnDownloadPdf").addEventListener("click", async () => {
    const id = document.getElementById("reportCaseId").value.trim();
    if (!id) return;
    try {
      const res = await fetch("/backend/api/v1/cases/" + id + "/export?format=html", {
        headers: {
          Authorization: BteAdmin.getToken()
            ? "Bearer " + BteAdmin.getToken()
            : undefined,
        },
      });
      const html = await res.text();
      if (!res.ok) throw new Error(html || res.statusText);
      const w = window.open("", "_blank");
      if (!w) throw new Error("Popup blocked");
      w.document.write(html);
      w.document.close();
      w.focus();
      w.print();
    } catch (err) {
      BteAdmin.showFlash(flash, err.message, "error");
    }
  });
})();
