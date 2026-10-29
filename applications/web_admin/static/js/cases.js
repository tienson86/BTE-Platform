(function () {
  if (window.BteAdminArchive) {
    void BteAdminArchive.start();
    const form=document.getElementById("adminContactForm"), state=document.getElementById("adminContactState");
    form.addEventListener("submit",async event=>{
      event.preventDefault();if(!form.reportValidity())return;
      const button=form.querySelector("button");button.disabled=true;
      try{
        const fields=form.elements,payload={};["full_name","phone","subject","message","channel"].forEach(key=>payload[key]=fields[key].value.trim());
        const result=await BteAdmin.post("/api/v1/contacts",payload);state.textContent="Đã lưu liên hệ: "+result.id;form.reset();await BteAdminArchive.refresh();
      }catch(error){state.textContent=error.message;}finally{button.disabled=false;}
    });
    return;
  }
  const rows = document.getElementById("caseRows");
  const flash = document.getElementById("globalFlash");
  let selected = null;

  async function loadCases() {
    const q = BteAdmin.qs({
      customer_id: document.getElementById("filterCustomer").value,
    });
    try {
      const data = await BteAdmin.get("/api/v1/cases" + q);
      const list = (data.data && data.data.cases) || [];
      rows.innerHTML = list
        .map(
          (c) =>
            "<tr><td>" +
            c.case_id +
            "</td><td>" +
            BteAdmin.fmt(c.customer_id) +
            "</td><td>" +
            BteAdmin.fmt(c.created_at) +
            "</td><td>" +
            BteAdmin.fmt(c.engine_version) +
            '</td><td><button type="button" data-id="' +
            c.case_id +
            '">Open</button></td></tr>'
        )
        .join("");
      rows.querySelectorAll("button[data-id]").forEach((btn) => {
        btn.addEventListener("click", () => openCase(btn.getAttribute("data-id")));
      });
    } catch (err) {
      BteAdmin.showFlash(flash, err.message, "error");
    }
  }

  async function openCase(id) {
    try {
      const data = await BteAdmin.get("/api/v1/cases/" + id);
      selected = data.data && data.data.case;
      document.getElementById("caseDetail").style.display = "block";
      document.getElementById("caseBody").textContent = JSON.stringify(selected, null, 2);
    } catch (err) {
      BteAdmin.showFlash(flash, err.message, "error");
    }
  }

  async function exportCase(fmt) {
    if (!selected) return;
    try {
      const res = await fetch(
        "/backend/api/v1/cases/" + selected.case_id + "/export?format=" + fmt,
        {
          headers: {
            Authorization: BteAdmin.getToken()
              ? "Bearer " + BteAdmin.getToken()
              : undefined,
          },
        }
      );
      const text = await res.text();
      if (!res.ok) throw new Error(text || res.statusText);
      const blob = new Blob([text], {
        type:
          fmt === "html"
            ? "text/html"
            : fmt === "markdown"
              ? "text/markdown"
              : "application/json",
      });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = selected.case_id + "." + (fmt === "markdown" ? "md" : fmt);
      a.click();
    } catch (err) {
      BteAdmin.showFlash(flash, err.message, "error");
    }
  }

  document.getElementById("btnLoadCases").addEventListener("click", loadCases);
  document.getElementById("btnExportJson").addEventListener("click", () => exportCase("json"));
  document.getElementById("btnExportMd").addEventListener("click", () => exportCase("markdown"));
  document.getElementById("btnExportHtml").addEventListener("click", () => exportCase("html"));
  document.getElementById("btnDeleteCase").addEventListener("click", async () => {
    if (!selected || !confirm("Delete case?")) return;
    try {
      await BteAdmin.del("/api/v1/cases/" + selected.case_id);
      selected = null;
      document.getElementById("caseDetail").style.display = "none";
      BteAdmin.showFlash(flash, "Case deleted", "success");
      loadCases();
    } catch (err) {
      BteAdmin.showFlash(flash, err.message, "error");
    }
  });

  loadCases();
})();
