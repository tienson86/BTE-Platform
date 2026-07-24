(function () {
  const flash = document.getElementById("globalFlash");
  const form = document.getElementById("analyzeForm");
  const btn = document.getElementById("btnAnalyze");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    btn.disabled = true;
    btn.textContent = "Analyzing…";
    const input = {
      year: Number(document.getElementById("year").value),
      month: Number(document.getElementById("month").value),
      day: Number(document.getElementById("day").value),
      hour: Number(document.getElementById("hour").value || 0),
      minute: Number(document.getElementById("minute").value || 0),
      gender: document.getElementById("gender").value || null,
      timezone: document.getElementById("timezone").value || "Asia/Ho_Chi_Minh",
    };
    try {
      const res = await BtePortal.post("/api/v1/analyze", input);
      BtePortal.saveLastResult({ input: input, data: res.data || res });
      BtePortal.showFlash(flash, "Analyze complete", "success");
      window.location.href = "/result";
    } catch (err) {
      BtePortal.showFlash(flash, err.message, "error");
      btn.disabled = false;
      btn.textContent = "Run analyze";
    }
  });
})();
