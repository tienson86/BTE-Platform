(function () {
  const form = document.getElementById("name-analysis-form");
  if (!form) return;
  const fields = document.getElementById("na-fields");
  const state = document.getElementById("na-state");
  const result = document.getElementById("na-result");
  const fullName = document.getElementById("na-full-name");
  let busy = false;

  form.addEventListener("input", function () {
    fullName.setCustomValidity("");
    state.textContent = "";
    result.replaceChildren();
    result.hidden = true;
  });

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    if (busy) return;
    fullName.setCustomValidity(fullName.value.trim() ? "" : "Vui lòng nhập họ và tên hiện tại.");
    if (!form.reportValidity()) return;
    const payload = Object.fromEntries(new FormData(form));
    payload.full_name = fullName.value.trim();
    busy = true;
    fields.disabled = true;
    form.setAttribute("aria-busy", "true");
    result.hidden = true;
    result.replaceChildren();
    state.textContent = "Đang lập Bát Tự và đối chiếu hành tên…";
    try {
      const response = await fetch("/backend/api/v1/public/naming/analyze-current-birth", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload), signal: AbortSignal.timeout(120000),
      });
      const envelope = await response.json();
      if (!response.ok || envelope.status !== "SUCCESS" || !envelope.data) {
        const detail = envelope.detail;
        const message = typeof detail === "string" ? detail : Array.isArray(detail)
          ? detail.map(function (item) { return item.msg; }).join(" · ")
          : envelope.errors?.[0]?.message;
        throw new Error(message || "Chưa phân tích được tên. Vui lòng thử lại.");
      }
      renderResult(envelope.data);
      state.textContent = "Đã phân tích tên hiện tại của bạn.";
    } catch (error) {
      state.textContent = error.name === "TimeoutError"
        ? "Phân tích vượt thời gian chờ. Vui lòng thử lại."
        : error.message || "Chưa kết nối được dịch vụ phân tích tên.";
      state.focus();
    } finally {
      busy = false;
      fields.disabled = false;
      form.removeAttribute("aria-busy");
    }
  });

  function node(tag, text, className) {
    const element = document.createElement(tag);
    if (text !== undefined) element.textContent = text;
    if (className) element.className = className;
    return element;
  }

  function renderResult(data) {
    const reading = data.name_reading;
    if (data.basis !== "birth_chart" || !data.signals || !data.fit) {
      throw new Error("Dịch vụ chưa hỗ trợ phân tích theo ngày giờ sinh. Vui lòng cập nhật và khởi động lại BTE.");
    }
    const reference = data.signals;
    const verdict = node("section", undefined, "panel na-verdict");
    verdict.dataset.level = data.fit.level;
    verdict.append(node("h2", "Mức độ phù hợp của tên"), node("strong", data.fit.title), node("p", data.fit.reason));
    if (data.direction) verdict.append(node("p", data.direction));
    if (data.suggestions?.length) {
      const suggestions = node("ul");
      data.suggestions.forEach(function (item) {
        const line = node("li");
        line.append(node("strong", item.full_name + " · " + item.element),
          node("span", " — " + item.fit_level + ". " + item.meaning));
        if (item.cung_phi_relation?.relation !== "unresolved" && item.cung_phi_relation?.explanation) {
          line.append(node("p", item.cung_phi_relation.explanation, "muted"));
        }
        suggestions.append(line);
      });
      verdict.append(node("h3", "Tên gọi có thể cân nhắc"), suggestions);
    }
    const summary = node("section", undefined, "panel nc-name");
    summary.dataset.element = reading.element || "";
    summary.append(node("h2", data.full_name), node("p", reading.meaning));
    if (reading.main_part) {
      const structure = node("dl", undefined, "na-name-structure");
      [["Họ", reading.family_part], ["Tên đệm", reading.middle_part], ["Tên chính", reading.main_part]].forEach(function (item) {
        if (!item[1]) return;
        const cell = node("div"); cell.append(node("dt", item[0]), node("dd", item[1])); structure.append(cell);
      });
      summary.append(structure);
    }
    if (reading.element) {
      summary.append(node("p", "Hành tên gọi tham khảo: " + reading.element, "nc-fit"));
      summary.append(node("p", reading.element_basis, "muted"));
    }
    const parts = node("div", undefined, "na-parts");
    reading.parts.forEach(function (part) {
      const card = node("article", undefined, "panel nc-name");
      card.dataset.element = part.element || "";
      if (part.role) card.append(node("p", part.role, "na-caption"));
      card.append(node("h3", part.word), node("p", part.meaning));
      if (part.han_characters?.length) {
        const characterList = node("ul", undefined, "na-characters");
        part.han_characters.forEach(function (item) {
          const line = node("li");
          line.append(node("span", item.character, "na-han-character"), node("span", item.meaning));
          characterList.append(line);
        });
        card.append(node("p", "Chữ Hán có thể tham khảo", "na-caption"), characterList);
      }
      if (part.interpretation) card.append(node("p", part.interpretation, "na-prose"));
      if (part.element) card.append(node("p", "Hành tham khảo: " + part.element, "muted"));
      if (part.element_basis) card.append(node("p", part.element_basis, "muted"));
      parts.append(card);
    });
    const hanViet = node("section", undefined, "panel na-han-viet");
    hanViet.append(node("h2", "Luận nghĩa Hán–Việt"));
    if (reading.han_viet?.phrase) hanViet.append(node("h3", "Khi ghép thành tên “" + reading.han_viet.phrase + "”"));
    (reading.han_viet?.paragraphs || []).forEach(function (paragraph) {
      hanViet.append(node("p", paragraph, "na-prose"));
    });
    if (reading.han_viet?.note) hanViet.append(node("p", reading.han_viet.note, "muted"));
    hanViet.append(node("h3", "Ý nghĩa từng tiếng"), parts);
    if (reading.family_reading) {
      const family = node("details", undefined, "na-family");
      family.append(node("summary", "Họ “" + reading.family_reading.word + "” trong cấu trúc tên"));
      if (reading.family_reading.characters) family.append(node("p", "Chữ viết tham khảo: " + reading.family_reading.characters, "na-caption"));
      family.append(node("p", reading.family_reading.paragraph, "na-prose")); hanViet.append(family);
    }
    const rhythm = node("section", undefined, "panel na-rhythm");
    if (reading.rhythm) {
      rhythm.append(node("h2", "Âm điệu của họ tên"), node("p", reading.rhythm.paragraph, "na-prose"));
      const tones = node("div", undefined, "na-tones");
      reading.rhythm.tones.forEach(function (tone) {
        const badge = node("span", tone.word + " · " + tone.tone + " (" + tone.group.toLowerCase() + ")", "na-tone");
        badge.dataset.group = tone.group; tones.append(badge);
      });
      rhythm.append(tones);
    }
    const yearSection = node("section", undefined, "panel");
    yearSection.append(node("h2", "Bát Tự và đối chiếu ngũ hành"));
    const yearGrid = node("div", undefined, "na-grid");
    [
      ...[["Trụ năm", "year"], ["Trụ tháng", "month"], ["Trụ ngày", "day"], ["Trụ giờ", "hour"]].map(function ([label, key]) {
        return [label, reference.pillars[key]];
      }),
      ["Nạp Âm", reference.nap_am],
      ["Cung Phi", [reference.cung_phi, reference.cung_phi_element].filter(Boolean).join(" · ")],
    ].forEach(function (item) {
      const card = node("section");
      card.append(node("strong", item[0]), node("p", item[1] || "Chưa có dữ liệu"));
      yearGrid.append(card);
    });
    yearSection.append(yearGrid);
    const comparisons = node("div", undefined, "na-comparisons");
    data.factors.forEach(function (factor) {
      const card = node("section", undefined, "panel");
      card.append(node("h3", factor.label), node("strong", factor.elements.join(", ") || "Chưa xác định"), node("p", factor.explanation));
      comparisons.append(card);
    });
    const resolvedComparisons = data.comparisons.filter(function (comparison) { return comparison.relation !== "unresolved"; });
    resolvedComparisons.forEach(function (comparison) {
      const card = node("section", undefined, "panel");
      card.dataset.relation = comparison.relation;
      card.append(node("h3", comparison.label), node("strong", comparison.title), node("p", comparison.explanation));
      comparisons.append(card);
    });
    const notes = node("aside", undefined, "na-note");
    if (data.notes.length) {
      const notesList = node("ul");
      data.notes.forEach(function (text) { notesList.append(node("li", text)); });
      notes.append(notesList);
    }
    notes.hidden = !data.notes.length;
    result.append(summary, verdict, yearSection, comparisons, hanViet);
    if (reading.rhythm) result.append(rhythm);
    result.append(notes, node("p", data.notice, "muted"));
    result.hidden = false;
  }
})();
