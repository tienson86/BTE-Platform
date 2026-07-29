(function () {
  const rows = document.getElementById("customerRows");
  const modal = document.getElementById("customerModal");
  const form = document.getElementById("customerForm");
  const flash = document.getElementById("globalFlash");

  function openModal(customer) {
    document.getElementById("modalTitle").textContent = customer
      ? "Edit customer"
      : "Add customer";
    document.getElementById("customerId").value = customer ? customer.customer_id : "";
    document.getElementById("full_name").value = customer ? customer.full_name || "" : "";
    document.getElementById("gender").value = customer ? customer.gender || "" : "";
    document.getElementById("birth_datetime").value = customer
      ? customer.birth_datetime || ""
      : "";
    document.getElementById("phone").value = customer ? customer.phone || "" : "";
    document.getElementById("email").value = customer ? customer.email || "" : "";
    document.getElementById("timezone").value =
      (customer && customer.timezone) || "Asia/Ho_Chi_Minh";
    document.getElementById("language").value = (customer && customer.language) || "vi";
    document.getElementById("tags").value = customer
      ? (customer.tags || []).join(", ")
      : "";
    document.getElementById("notes").value = customer ? customer.notes || "" : "";
    modal.classList.add("show");
  }

  function closeModal() {
    modal.classList.remove("show");
  }

  async function loadCustomers() {
    const q = BteAdmin.qs({
      name: document.getElementById("qName").value,
      phone: document.getElementById("qPhone").value,
      email: document.getElementById("qEmail").value,
      tag: document.getElementById("qTag").value,
    });
    try {
      const data = await BteAdmin.get("/api/v1/customers" + q);
      const list = (data.data && data.data.customers) || [];
      rows.innerHTML = list
        .map((c) => {
          return (
            "<tr>" +
            "<td>" +
            BteAdmin.fmt(c.full_name) +
            "</td>" +
            "<td>" +
            BteAdmin.fmt(c.gender) +
            "</td>" +
            "<td>" +
            BteAdmin.fmt(c.birth_datetime) +
            "</td>" +
            "<td>" +
            BteAdmin.fmt(c.phone) +
            "</td>" +
            "<td>" +
            BteAdmin.fmt(c.email) +
            "</td>" +
            "<td>" +
            BteAdmin.fmt((c.tags || []).join(", ")) +
            "</td>" +
            '<td class="toolbar">' +
            '<button type="button" data-edit="' +
            c.customer_id +
            '">Edit</button>' +
            '<button type="button" class="secondary" data-history="' +
            c.customer_id +
            '" data-name="' +
            encodeURIComponent(c.full_name || "") +
            '">History</button>' +
            '<button type="button" class="secondary" data-analyze="' +
            c.customer_id +
            '">Analyze</button>' +
            '<button type="button" class="danger" data-del="' +
            c.customer_id +
            '">Delete</button>' +
            "</td></tr>"
          );
        })
        .join("");

      rows.querySelectorAll("[data-edit]").forEach((btn) => {
        btn.addEventListener("click", () => {
          const c = list.find((x) => x.customer_id === btn.getAttribute("data-edit"));
          openModal(c);
        });
      });
      rows.querySelectorAll("[data-del]").forEach((btn) => {
        btn.addEventListener("click", async () => {
          if (!confirm("Delete this customer?")) return;
          try {
            await BteAdmin.del("/api/v1/customers/" + btn.getAttribute("data-del"));
            BteAdmin.showFlash(flash, "Customer deleted", "success");
            loadCustomers();
          } catch (err) {
            BteAdmin.showFlash(flash, err.message, "error");
          }
        });
      });
      rows.querySelectorAll("[data-history]").forEach((btn) => {
        btn.addEventListener("click", async () => {
          const id = btn.getAttribute("data-history");
          try {
            const hist = await BteAdmin.get("/api/v1/customers/" + id + "/history");
            document.getElementById("historyPanel").style.display = "block";
            document.getElementById("historyName").textContent = decodeURIComponent(
              btn.getAttribute("data-name") || id
            );
            document.getElementById("historyBody").textContent = JSON.stringify(
              hist.data || hist,
              null,
              2
            );
          } catch (err) {
            BteAdmin.showFlash(flash, err.message, "error");
          }
        });
      });
      rows.querySelectorAll("[data-analyze]").forEach((btn) => {
        btn.addEventListener("click", async () => {
          try {
            const res = await BteAdmin.post(
              "/api/v1/customers/" + btn.getAttribute("data-analyze") + "/analyze",
              {}
            );
            BteAdmin.showFlash(
              flash,
              "Analyze OK — case " + ((res.data && res.data.case && res.data.case.case_id) || ""),
              "success"
            );
          } catch (err) {
            BteAdmin.showFlash(flash, err.message, "error");
          }
        });
      });
    } catch (err) {
      BteAdmin.showFlash(flash, err.message, "error");
    }
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const id = document.getElementById("customerId").value;
    const payload = {
      full_name: document.getElementById("full_name").value,
      gender: document.getElementById("gender").value || null,
      birth_datetime: document.getElementById("birth_datetime").value || null,
      phone: document.getElementById("phone").value || null,
      email: document.getElementById("email").value || null,
      timezone: document.getElementById("timezone").value || "Asia/Ho_Chi_Minh",
      language: document.getElementById("language").value || "vi",
      notes: document.getElementById("notes").value || null,
      tags: document
        .getElementById("tags")
        .value.split(",")
        .map((t) => t.trim())
        .filter(Boolean),
    };
    try {
      if (id) {
        await BteAdmin.put("/api/v1/customers/" + id, payload);
        BteAdmin.showFlash(flash, "Customer updated", "success");
      } else {
        await BteAdmin.post("/api/v1/customers", payload);
        BteAdmin.showFlash(flash, "Customer created", "success");
      }
      closeModal();
      loadCustomers();
    } catch (err) {
      BteAdmin.showFlash(flash, err.message, "error");
    }
  });

  document.getElementById("btnCreate").addEventListener("click", () => openModal(null));
  document.getElementById("modalClose").addEventListener("click", closeModal);
  document.getElementById("btnSearch").addEventListener("click", loadCustomers);
  document.getElementById("btnReload").addEventListener("click", loadCustomers);
  loadCustomers();
})();
