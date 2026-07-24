(function () {
  const flash = document.getElementById("globalFlash");
  const last = BtePortal.getLastResult();
  const htmlView = document.getElementById("htmlView");
  const mdView = document.getElementById("mdView");

  if (!last || !last.data) {
    BtePortal.showFlash(flash, "No analyze result — run Analyze first", "error");
    htmlView.srcdoc = "<p>No report available.</p>";
    return;
  }

  const report = last.data.report || {};
  const narrative = last.data.narrative || {};
  const html = narrative.html || report.html || "<p>No HTML content</p>";
  const md = narrative.markdown || report.markdown || "";

  htmlView.srcdoc = html;
  mdView.textContent = md;

  document.getElementById("btnHtml").addEventListener("click", () => {
    htmlView.style.display = "block";
    mdView.style.display = "none";
  });
  document.getElementById("btnMd").addEventListener("click", () => {
    htmlView.style.display = "none";
    mdView.style.display = "block";
  });
  document.getElementById("btnPdf").addEventListener("click", () => {
    const w = window.open("", "_blank");
    if (!w) {
      BtePortal.showFlash(flash, "Popup blocked", "error");
      return;
    }
    w.document.write(html);
    w.document.close();
    w.focus();
    w.print();
  });
})();
