(function () {
  const form = document.querySelector("[data-testid='childbirth-form']");
  const state = document.querySelector("[data-testid='childbirth-state']");
  const result = document.querySelector("[data-testid='childbirth-result']");
  const apiUrl = window.__BTE_CHILDBIRTH_API__ || "/backend/api/v1/consulting/childbirth/analyze";
  const apiBase = apiUrl.replace(/\/analyze\/?$/, "");
  const history = document.querySelector("[data-testid='childbirth-history']");
  const historyError = document.querySelector("[data-testid='childbirth-history-error']");
  let activeProfile = null;
  let busy = false;

  if (!form || !state || !result) return;

  void loadHistory();

  const currentYear = new Date().getFullYear();
  const startYear = form.querySelector("#cb-start-year");
  if (startYear && !startYear.value) {
    startYear.value = String(currentYear);
    startYear.min = String(currentYear);
  }

  form.querySelectorAll("#cb-father-date, #cb-mother-date").forEach((input) => {
    input.addEventListener("input", () => {
      const digits = input.value.replace(/\D/g, "").slice(0, 8);
      input.value = [digits.slice(0, 2), digits.slice(2, 4), digits.slice(4)]
        .filter(Boolean).join("/");
      input.removeAttribute("aria-invalid");
      document.getElementById(`${input.id}-error`).hidden = true;
    });
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (busy) return;
    activeProfile = null;
    result.hidden = true;
    result.innerHTML = "";
    state.textContent = "";

    const body = buildPayload(form);
    if (!body) {
      form.querySelector('[aria-invalid="true"]')?.focus();
      return;
    }

    state.textContent = "Đang phân tích năm sinh con...";
    setBusy(true);
    try {
      const data = await request(apiUrl, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
      state.textContent = "";
      renderResult(data);
    } catch (error) {
      state.innerHTML = `<p class="field-error">${escapeHtml(error.message || "Không thể hoàn tất tư vấn.")}</p>`;
    } finally {
      setBusy(false);
    }
  });

  result.addEventListener("click", async (event) => {
    const button = event.target.closest("[data-cb-action]");
    if (!button || busy || !activeProfile?.consultation_id) return;
    const action = button.dataset.cbAction;
    if (action === "save" && activeProfile.saved_at) return;
    setBusy(true);
    const message = result.querySelector(".cb-action-state");
    message.classList.remove("mc-export-error");
    message.textContent = action === "save" ? "Đang lưu hồ sơ..." : `Đang tạo ${action.toUpperCase()}...`;
    try {
      const url = `${apiBase}/${encodeURIComponent(activeProfile.consultation_id)}`;
      if (action === "save") {
        const saved = await request(`${url}/save`, { method: "POST" });
        activeProfile.saved_at = saved.saved_at;
        button.querySelector("span").textContent = "Đã lưu hồ sơ";
        message.textContent = "Đã lưu hồ sơ sinh con.";
        await loadHistory();
      } else {
        await downloadExport(`${url}/export/${action}`, action);
        message.textContent = `Đã tải báo cáo ${action.toUpperCase()}.`;
      }
    } catch (error) {
      message.classList.add("mc-export-error");
      message.textContent = error.message || "Không thể hoàn tất thao tác. Vui lòng thử lại.";
    } finally {
      setBusy(false);
    }
  });

  history?.addEventListener("click", async (event) => {
    const button = event.target.closest("[data-cb-profile]");
    if (!button || busy) return;
    setBusy(true);
    historyError.hidden = true;
    try {
      const data = await request(`${apiBase}/${encodeURIComponent(button.dataset.cbProfile)}`);
      restoreForm(data.input);
      state.textContent = "";
      renderResult(data);
      result.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (error) {
      historyError.textContent = error.message || "Không mở được hồ sơ. Vui lòng thử lại.";
      historyError.hidden = false;
    } finally {
      setBusy(false);
    }
  });

  function setBusy(value) {
    busy = value;
    form.querySelector("[data-testid='submit-childbirth']").disabled = value;
    result.querySelectorAll("[data-cb-action]").forEach((button) => {
      button.disabled = value || (button.dataset.cbAction === "save" && Boolean(activeProfile?.saved_at));
    });
    history?.querySelectorAll("button").forEach((button) => { button.disabled = value; });
  }

  async function request(url, options = {}) {
    const response = await fetch(url, { ...options, signal: AbortSignal.timeout(120000) });
    const envelope = await response.json();
    if (!response.ok || envelope.status !== "SUCCESS" || !envelope.data) {
      throw new Error(envelope.errors?.[0]?.message || "Không thể hoàn tất thao tác. Vui lòng thử lại.");
    }
    return envelope.data;
  }

  async function loadHistory() {
    if (!history) return;
    historyError.hidden = true;
    try {
      const data = await request(`${apiBase}/history`);
      history.innerHTML = data.items.map((item) => `
        <article class="bte-card mc-history__item">
          <div>
            <h3>${escapeHtml(item.display_identity)}</h3>
            <p class="muted">${escapeHtml(item.headline)}</p>
            <p class="muted">Đã lưu ${escapeHtml(new Date(item.saved_at).toLocaleString("vi-VN", { timeZone: "Asia/Ho_Chi_Minh" }))}</p>
          </div>
          <button type="button" class="secondary" data-cb-profile="${escapeHtml(item.consultation_id)}" ${busy ? "disabled" : ""}>Mở hồ sơ</button>
        </article>
      `).join("") || '<p class="muted">Chưa có hồ sơ sinh con đã lưu.</p>';
    } catch (error) {
      historyError.textContent = "Không tải được danh sách hồ sơ. Vui lòng tải lại trang.";
      historyError.hidden = false;
    }
  }

  function restoreForm(inputs) {
    if (!inputs) return;
    for (const role of ["father", "mother"]) {
      const person = inputs[role];
      const [year, month, day] = person.birth_date.split("-");
      form.querySelector(`#cb-${role}-name`).value = person.full_name || "";
      form.querySelector(`#cb-${role}-date`).value = `${day}/${month}/${year}`;
      form.querySelector(`#cb-${role}-time`).value = person.birth_time || "";
      form.querySelector(`#cb-${role}-place`).value = person.birth_place?.display_name || "";
      form.querySelector(`#cb-${role}-date`).removeAttribute("aria-invalid");
      document.getElementById(`cb-${role}-date-error`).hidden = true;
    }
    form.querySelector("#cb-start-year").value = inputs.options.start_year;
    form.querySelector("#cb-years-ahead").value = inputs.options.years_ahead;
  }

  async function downloadExport(url, format) {
    const mediaType = format === "pdf" ? "application/pdf" : "application/vnd.openxmlformats-officedocument.wordprocessingml.document";
    const response = await fetch(url, { headers: { Accept: mediaType }, signal: AbortSignal.timeout(120000) });
    if (!response.ok || !response.headers.get("Content-Type")?.includes(mediaType)) {
      throw new Error(`Không tạo được báo cáo ${format.toUpperCase()}. Vui lòng thử lại.`);
    }
    const disposition = response.headers.get("Content-Disposition");
    const encoded = disposition?.match(/filename\*=UTF-8''([^;]+)/i)?.[1];
    const plain = disposition?.match(/filename="?([^";]+)"?/i)?.[1];
    const filename = encoded ? decodeURIComponent(encoded.replace(/^"|"$/g, "")) : plain || `BTE_TuVanSinhCon.${format}`;
    const objectUrl = URL.createObjectURL(await response.blob());
    const link = document.createElement("a");
    link.href = objectUrl;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(objectUrl), 1000);
  }

  function buildPayload(root) {
    const fatherDate = birthDate("#cb-father-date");
    const motherDate = birthDate("#cb-mother-date");
    if (!fatherDate || !motherDate) return null;
    return {
      father: {
        gender: "male",
        full_name: value("#cb-father-name") || null,
        birth_date: fatherDate,
        birth_time: value("#cb-father-time") || null,
        birth_place: value("#cb-father-place") || null,
        timezone: "Asia/Ho_Chi_Minh",
      },
      mother: {
        gender: "female",
        full_name: value("#cb-mother-name") || null,
        birth_date: motherDate,
        birth_time: value("#cb-mother-time") || null,
        birth_place: value("#cb-mother-place") || null,
        timezone: "Asia/Ho_Chi_Minh",
      },
      options: {
        start_year: numberValue("#cb-start-year"),
        years_ahead: numberValue("#cb-years-ahead") || 12,
      },
    };

    function value(selector) {
      return root.querySelector(selector)?.value.trim() || "";
    }

    function numberValue(selector) {
      const raw = value(selector);
      return raw ? Number(raw) : null;
    }

    function birthDate(selector) {
      const input = root.querySelector(selector);
      const iso = parseBirthDate(input.value.trim());
      const error = document.getElementById(`${input.id}-error`);
      error.hidden = Boolean(iso);
      error.textContent = iso ? "" : "Vui lòng nhập ngày sinh hợp lệ theo DD/MM/YYYY.";
      if (iso) input.removeAttribute("aria-invalid");
      else input.setAttribute("aria-invalid", "true");
      return iso;
    }
  }

  function parseBirthDate(raw) {
    const match = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec(raw);
    if (!match) return null;
    const [, day, month, year] = match;
    const parsed = new Date(Number(year), Number(month) - 1, Number(day));
    if (parsed.getFullYear() !== Number(year) ||
        parsed.getMonth() !== Number(month) - 1 ||
        parsed.getDate() !== Number(day)) return null;
    return `${year}-${month}-${day}`;
  }

  function renderResult(data) {
    activeProfile = data;
    const top = data.recommendations || [];
    const parents = data.parents || {};
    result.innerHTML = `
      <div class="mc-result-toolbar">
        <span class="muted">${escapeHtml([data.input?.father?.full_name || "Người bố", data.input?.mother?.full_name || "Người mẹ"].join(" / "))}</span>
        <div class="mc-result-toolbar__exports" aria-label="Lưu và tải báo cáo sinh con">
          <button type="button" class="secondary" data-cb-action="save">${actionIcon("folder")}<span>${data.saved_at ? "Đã lưu hồ sơ" : "Lưu hồ sơ"}</span></button>
          <button type="button" class="secondary" data-cb-action="pdf">${actionIcon("export")}<span>Xuất PDF</span></button>
          <button type="button" class="secondary" data-cb-action="docx">${actionIcon("export")}<span>Xuất DOCX</span></button>
        </div>
      </div>
      <p class="cb-action-state" role="status" aria-live="polite"></p>
      <section class="bte-card cb-summary">
        <div>
          <h2>${escapeHtml(data.summary?.headline || "Kết quả tư vấn sinh con")}</h2>
          ${data.summary?.note ? `<p class="muted">${escapeHtml(data.summary.note)}</p>` : ""}
          <p class="muted">${escapeHtml(data.eligibility?.rule || "")}</p>
        </div>
        <div>
          <span class="cb-pill">Từ ${escapeHtml(String(data.start_year))}</span>
          <span class="cb-pill">${escapeHtml(String(data.years_ahead))} năm</span>
        </div>
      </section>
      <section class="cb-parent-grid">
        ${parentCard("Bố", parents.father)}
        ${parentCard("Mẹ", parents.mother)}
      </section>
      <section class="cb-year-grid">
        ${top.map(yearCard).join("") || emptyState(data)}
      </section>
    `;
    result.hidden = false;
    setBusy(busy);
  }

  function actionIcon(name) {
    const paths = name === "folder"
      ? '<path d="M3 8h6l2 2h10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8z"/>'
      : '<path d="M12 15V5M8 9l4-4 4 4"/><path d="M5 19h14"/>';
    return `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${paths}</svg>`;
  }

  function parentCard(title, parent) {
    if (!parent) return "";
    return `
      <article class="bte-card">
        <h2>${title}</h2>
        <p><strong>Nhật chủ:</strong> ${escapeHtml(parent.day_master || "--")} (${escapeHtml(parent.day_master_element || "--")})</p>
        <p><strong>Mệnh cục:</strong> ${escapeHtml(parent.pattern || "--")}</p>
        <p><strong>Dụng/Hỷ:</strong> ${escapeHtml([...(parent.useful_elements || []), ...(parent.favorable_elements || [])].join(", ") || "--")}</p>
        <p><strong>Thần sát:</strong> ${escapeHtml((parent.shen_sha || []).join(", ") || "--")}</p>
        <p><strong>Thập thần:</strong> ${escapeHtml((parent.ten_gods || []).join(", ") || "--")}</p>
        <p><strong>Cung phi:</strong> ${escapeHtml(parent.cung_phi || "--")} · ${escapeHtml(parent.trach_group || "--")}</p>
      </article>
    `;
  }

  function yearCard(item) {
    const genderLabel = {
      boy: "Ưu tiên con trai",
      girl: "Ưu tiên con gái",
      either: "Trai/gái đều xét được",
    }[item.recommended_child_gender] || "Trai/gái đều xét được";
    return `
      <article class="bte-card cb-year">
        <div>
          <h3>${escapeHtml(String(item.year))} · ${escapeHtml(item.can_chi)}</h3>
          <div class="cb-year__meta">
            <span class="cb-pill" data-level="${escapeHtml(item.level)}">${escapeHtml(levelLabel(item.level))}</span>
            <span class="cb-pill">${escapeHtml(genderLabel)}</span>
            <span class="cb-pill">${escapeHtml(item.primary_element)} / ${escapeHtml(item.branch_element)}</span>
          </div>
        </div>
        <p><strong>Điểm phù hợp:</strong> ${escapeHtml(String(item.score))}/100 · bố ${escapeHtml(String(item.father_age))} tuổi, mẹ ${escapeHtml(String(item.mother_age))} tuổi.</p>
        <p><strong>Bé trai:</strong> ${escapeHtml(item.boy?.cung_phi || "--")} · ${escapeHtml(item.boy?.trach_group || "--")}</p>
        <p><strong>Bé gái:</strong> ${escapeHtml(item.girl?.cung_phi || "--")} · ${escapeHtml(item.girl?.trach_group || "--")}</p>
        <ul class="cb-list">${(item.reasons || []).map((text) => `<li>${escapeHtml(text)}</li>`).join("")}</ul>
        ${(item.cautions || []).length ? `<p class="cb-caution"><strong>Lưu ý:</strong> ${escapeHtml(item.cautions.join(" "))}</p>` : ""}
      </article>
    `;
  }

  function emptyState(data) {
    const items = data.eligibility?.ineligible_years || [];
    return `
      <article class="bte-card">
        <h2>Chưa có năm phù hợp trong khoảng đang xét</h2>
        <p class="muted">${items.length ? escapeHtml(items[0].reason) : "Hãy mở rộng số năm tiếp theo để hệ thống xét thêm."}</p>
      </article>
    `;
  }

  function levelLabel(level) {
    return {
      very_suitable: "Rất phù hợp",
      suitable: "Phù hợp",
      consider: "Có thể cân nhắc",
      sensitive: "Cần thận trọng",
    }[level] || "Có thể cân nhắc";
  }

  function escapeHtml(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }
})();
