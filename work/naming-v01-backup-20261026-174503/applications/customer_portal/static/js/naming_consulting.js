(function () {
  const form = document.getElementById("naming-form");
  if (!form) return;
  const fields = document.getElementById("nc-fields");
  const state = document.getElementById("nc-state");
  const result = document.getElementById("nc-result");
  const mode = document.getElementById("nc-mode");
  const currentField = document.getElementById("nc-current-field");
  const currentName = document.getElementById("nc-current-name");
  let busy = false;

  function updateMode() {
    const rename = mode.value === "rename";
    currentField.hidden = !rename;
    currentName.disabled = !rename;
    currentName.required = rename;
  }

  mode.addEventListener("change", updateMode);
  form.addEventListener("input", function () {
    result.hidden = true;
    result.replaceChildren();
    state.textContent = "";
  });
  updateMode();

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    if (busy || !form.reportValidity()) return;
    const values = new FormData(form);
    const payload = Object.fromEntries(values.entries());
    payload.count = Number(payload.count);
    payload.birth_time = payload.birth_time || null;
    payload.current_name = mode.value === "rename" ? payload.current_name : "";
    result.hidden = true;
    result.replaceChildren();
    state.textContent = "Đang đối chiếu dữ liệu Bát Tự và danh mục tên…";
    busy = true;
    fields.disabled = true;
    form.setAttribute("aria-busy", "true");
    try {
      const response = await fetch("/backend/api/v1/consulting/naming/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        signal: AbortSignal.timeout(120000),
      });
      const envelope = await response.json();
      if (!response.ok || envelope.status !== "SUCCESS" || !envelope.data) {
        const detail = envelope.detail;
        const message = typeof detail === "string" ? detail : Array.isArray(detail)
          ? detail.map(function (item) { return item.msg; }).join(" · ")
          : envelope.errors?.[0]?.message;
        throw new Error(message || "Chưa hoàn tất tư vấn. Vui lòng thử lại.");
      }
      renderResult(envelope.data);
      state.textContent = "Đã tìm được " + envelope.data.recommendations.length + " tên tham khảo.";
    } catch (error) {
      state.textContent = error.name === "TimeoutError"
        ? "Phân tích vượt thời gian chờ. Vui lòng thử lại."
        : error.message || "Chưa kết nối được dịch vụ tư vấn. Vui lòng thử lại.";
      state.focus();
    } finally {
      busy = false;
      fields.disabled = false;
      form.removeAttribute("aria-busy");
      updateMode();
    }
  });

  function node(tag, text, className) {
    const element = document.createElement(tag);
    if (text !== undefined) element.textContent = text;
    if (className) element.className = className;
    return element;
  }

  function list(items) {
    const element = node("ul");
    items.forEach(function (text) { element.append(node("li", text)); });
    return element;
  }

  function renderResult(data) {
    const signals = data.signals;
    const overview = node("section", undefined, "panel");
    overview.append(node("h2", data.quality === "preliminary" ? "Kết quả tham khảo sơ bộ" : "Cơ sở đối chiếu từ BTE"));
    if (data.current_name) overview.append(node("p", "Tên hiện tại: " + data.current_name));
    const signalGrid = node("div", undefined, "nc-signals");
    [
      ["Dụng thần", signals.useful_elements.join(", ") || "Chưa sử dụng / chưa có dữ liệu"],
      ["Hỷ thần", signals.favorable_elements.join(", ") || "Chưa sử dụng / chưa có dữ liệu"],
      ["Nạp Âm trụ năm BTE", signals.nap_am || "Chưa có dữ liệu"],
      ["Cung Phi", [signals.cung_phi, signals.cung_phi_element].filter(Boolean).join(" · ") || "Chưa có dữ liệu"],
    ].forEach(function (item) {
      const block = node("div");
      block.append(node("strong", item[0]), node("p", item[1]));
      signalGrid.append(block);
    });
    overview.append(signalGrid);
    if (signals.unfavorable_elements.length) overview.append(node("p", "Hành Kỵ thần tham khảo: " + signals.unfavorable_elements.join(", ")));
    const pillars = [
      ["Năm", "year"], ["Tháng", "month"], ["Ngày", "day"], ["Giờ", "hour"],
    ].map(function (item) { return item[0] + ": " + (signals.pillars[item[1]] || "Chưa biết"); });
    overview.append(node("p", pillars.join(" · "), "muted"));
    result.append(overview);
    if (data.warnings.length) {
      const warnings = node("aside", undefined, "panel nc-warnings");
      warnings.append(node("h3", "Lưu ý về dữ liệu"), list(data.warnings));
      result.append(warnings);
    }
    result.append(node("h2", "Tên gợi ý"));
    const names = node("div", undefined, "nc-names");
    data.recommendations.forEach(function (entry, index) {
      const card = node("article", undefined, "panel nc-name");
      card.append(
        node("h3", (index + 1) + ". " + entry.full_name),
        node("p", entry.fit_level, "nc-fit"),
        node("p", entry.meaning),
        node("p", "Hành quy ước: " + entry.element + ". " + entry.element_basis, "muted"),
        list(entry.reasons),
      );
      names.append(card);
    });
    const method = node("details", undefined, "panel");
    method.append(
      node("summary", "Cách đối chiếu và giới hạn"),
      node("p", data.method),
      node("p", data.catalog.element_convention),
      node("p", data.catalog.review_note),
      node("p", "Danh mục: " + data.catalog.version),
    );
    result.append(names, node("p", data.notice, "muted"), method);
    result.hidden = false;
  }
})();
