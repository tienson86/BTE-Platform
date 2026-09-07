(function () {
  const API = "/api/v1/consulting/marriage";
  const STATE_LABEL = {
    supportive: "Tương hợp tốt",
    balanced: "Cân bằng",
    mixed: "Hỗn hợp",
    pressured: "Có nhiều điểm cần lưu ý",
    critical: "Cần thận trọng",
    insufficient: "Chưa đủ dữ liệu",
  };
  const CONFIDENCE = {
    high: "Độ tin cậy cao",
    medium: "Khá tin cậy",
    reference_only: "Mang tính tham khảo",
  };
  const OPTIONAL = { interaction: true, family: true, children: true };

  function personFields(side, title) {
    const prefix = "person-" + side;
    return (
      '<section class="bte-card mc-person" data-person="' +
      side +
      '" data-testid="' +
      prefix +
      '-panel"><h2>' +
      title +
      "</h2>" +
      field(prefix + "-full-name", "Họ tên", "text") +
      '<fieldset class="ds-gender" data-testid="' +
      prefix +
      '-gender"><legend>Giới tính</legend>' +
      '<div class="ds-gender__options" role="radiogroup" aria-label="' +
      title +
      ' — giới tính">' +
      '<label><input type="radio" name="' +
      prefix +
      '-gender" value="male" /><span>Nam</span></label>' +
      '<label><input type="radio" name="' +
      prefix +
      '-gender" value="female" /><span>Nữ</span></label></div>' +
      '<span class="field-error" id="' +
      prefix +
      '-gender-error" hidden></span></fieldset>' +
      field(prefix + "-birth-date", "Ngày sinh dương lịch", "text", "DD/MM/YYYY") +
      field(prefix + "-birth-time", "Giờ sinh", "text", "HH:mm") +
      field(prefix + "-birth-place", "Nơi sinh", "text") +
      "</section>"
    );
  }

  function field(id, label, type, placeholder) {
    return (
      '<label for="' +
      id +
      '"><span>' +
      label +
      '</span><input id="' +
      id +
      '" name="' +
      id +
      '" type="' +
      type +
      '"' +
      (placeholder ? ' placeholder="' + placeholder + '"' : "") +
      " /></label>"
    );
  }

  function toIso(raw) {
    const match = String(raw || "").trim().match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
    if (!match) return null;
    return match[3] + "-" + match[2] + "-" + match[1];
  }

  function personBody(side) {
    const prefix = "person-" + side;
    const genderEl = document.querySelector('input[name="' + prefix + '-gender"]:checked');
    const date = toIso(document.getElementById(prefix + "-birth-date").value);
    if (!genderEl || !date) return null;
    const body = { gender: genderEl.value, birth_date: date };
    const name = document.getElementById(prefix + "-full-name").value.trim();
    const time = document.getElementById(prefix + "-birth-time").value.trim();
    const place = document.getElementById(prefix + "-birth-place").value.trim();
    if (name) body.full_name = name;
    if (time) body.birth_time = time;
    if (place) body.birth_place = { display_name: place };
    return body;
  }

  function section(report, id) {
    return (report.sections || []).find(function (item) {
      return item.section_id === id;
    });
  }

  function bodies(sec, kind) {
    if (!sec) return [];
    return (sec.blocks || [])
      .filter(function (item) {
        return (!kind || item.kind === kind) && item.visibility !== "expert";
      })
      .map(function (item) {
        return item.body || item.title || "";
      })
      .filter(Boolean);
  }

  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function renderResult(consultation, report, warnings) {
    const hero = section(report, "compatibility_hero");
    const exec = section(report, "executive_summary");
    const strengths = section(report, "strengths");
    const risks = section(report, "risks");
    const domains = section(report, "domain_analysis");
    const timing = section(report, "timing");
    const actions = section(report, "action_plan");
    const confidence = section(report, "confidence_limitations");
    const conclusion = section(report, "conclusion");
    const appendix = section(report, "appendix");
    const comparisonSpecs = [
      ["comparison_a_to_b", "A bổ trợ B"],
      ["comparison_b_to_a", "B bổ trợ A"],
      ["comparison_harmony", "Điểm hòa hợp"],
      ["comparison_conflict", "Điểm xung"],
      ["comparison_rescue", "Yếu tố cứu giải"],
    ];
    const comparisonHtml = comparisonSpecs
      .map(function (spec) {
        const sec = section(report, spec[0]);
        const items = bodies(sec, "highlight");
        if (!items.length) return "";
        return (
          '<article class="bte-card mc-comparison-card" data-testid="' +
          spec[0] +
          '"><h3>' +
          spec[1] +
          "</h3><ul>" +
          items
            .map(function (item) {
              return "<li>" + escapeHtml(item) + "</li>";
            })
            .join("") +
          "</ul></article>"
        );
      })
      .join("");
    const state = consultation.overall_state;
    const domainCards = {};
    (domains && domains.blocks ? domains.blocks : []).forEach(function (block) {
      if (!block.domain || block.visibility === "expert") return;
      if (!domainCards[block.domain]) domainCards[block.domain] = [];
      domainCards[block.domain].push(block);
    });
    const domainHtml = Object.keys(domainCards)
      .map(function (key) {
        const blocks = domainCards[key];
        const first = blocks[0];
        return (
          '<article class="bte-card mc-domain" data-domain="' +
          key +
          '" data-testid="domain-card"><h3>' +
          escapeHtml(first.title || key) +
          "</h3><p>" +
          escapeHtml(first.body || "") +
          "</p></article>"
        );
      })
      .join("");
    const actionHtml = bodies(actions, "recommendation")
      .map(function (text, index) {
        return (
          '<article class="bte-card mc-action" data-testid="action-card"><h3>Việc nên làm</h3><p>' +
          escapeHtml(actions.blocks[index].title || text) +
          "</p><p>" +
          escapeHtml(text) +
          "</p></article>"
        );
      })
      .join("");
    const warningHtml = (warnings || [])
      .map(function (item) {
        return '<p class="mc-limitation" data-testid="warning-note">' + escapeHtml(item.description || item.code) + "</p>";
      })
      .join("");
    const unavailable = (warnings || []).some(function (item) {
      return item.code === "DOMAIN_UNAVAILABLE" && OPTIONAL[item.affected_domain];
    });
    const timingHtml = timing
      ? '<section class="bte-card" data-testid="timing-section"><h2>Nhịp thời điểm</h2><p>' +
        escapeHtml(bodies(timing).join(" ")) +
        "</p></section>"
      : '<div data-testid="timing-omitted" hidden></div>';
    const cards = consultation.assessment_cards || [];
    const assessmentHtml = cards.length
      ? '<section class="mc-assessment" data-testid="marriage-assessment"><h2>Đánh giá hôn nhân</h2><div class="mc-assessment-grid">' +
        cards
          .map(function (card) {
            const facts = (card.supporting_facts || [])
              .map(function (item) {
                return "<li>" + escapeHtml(item) + "</li>";
              })
              .join("");
            const limits = (card.limitations || []).length
              ? '<p class="mc-limitation">' + escapeHtml((card.limitations || []).join("; ")) + "</p>"
              : "";
            return (
              '<article class="bte-card mc-assessment-card" data-testid="assessment-card-' +
              escapeHtml(card.question_id) +
              '"><p class="mc-assessment-card__question">' +
              escapeHtml(card.question) +
              '</p><p class="mc-assessment-card__answer">' +
              escapeHtml(card.answer) +
              '</p><details class="mc-assessment-card__more"><summary>Cơ sở và giới hạn</summary>' +
              '<ul class="mc-assessment-card__facts">' +
              facts +
              "</ul><p class=\"muted\">Độ tin cậy: " +
              escapeHtml(card.confidence) +
              "</p>" +
              limits +
              "</details></article>"
            );
          })
          .join("") +
        "</div></section>"
      : "";
    return (
      '<div class="mc-result" data-testid="marriage-result">' +
      '<section class="bte-card mc-identity" data-testid="couple-identity"><h2>Hồ sơ cặp đôi</h2>' +
      '<p data-testid="couple-names">' +
      escapeHtml((consultation.person_a && consultation.person_a.display_name) || "Người A") +
      " và " +
      escapeHtml((consultation.person_b && consultation.person_b.display_name) || "Người B") +
      "</p></section>" +
      assessmentHtml +
      '<section class="bte-card mc-hero" data-testid="compatibility-hero" data-semantic-only="true"' +
      (cards.length ? " hidden" : "") +
      ">" +
      '<p class="mc-hero__eyebrow">Tương hợp hôn nhân</p>' +
      '<h2 data-testid="hero-headline">' +
      escapeHtml(consultation.headline || (hero && hero.summary) || "") +
      "</h2>" +
      '<p data-testid="hero-state">Nền tảng hiện ở trạng thái: ' +
      escapeHtml(STATE_LABEL[state] || state || "") +
      "</p>" +
      '<p data-testid="hero-summary">' +
      escapeHtml(bodies(hero, "summary")[0] || bodies(hero, "decision_state")[0] || "") +
      "</p>" +
      '<p data-testid="hero-confidence">' +
      escapeHtml(CONFIDENCE[(consultation.confidence && consultation.confidence.level) || ""] || "") +
      "</p>" +
      '<p class="sr-only" data-testid="hero-score-absent">Điểm số tương hợp chưa khả dụng</p></section>' +
      '<section class="bte-card" data-testid="executive-summary"' +
      (cards.length ? " hidden" : "") +
      "><h2>Đánh giá hôn nhân</h2><p>" +
      escapeHtml((exec && exec.blocks && exec.blocks[0] && exec.blocks[0].body) || "") +
      "</p></section>" +
      '<details class="mc-details" data-testid="detailed-analysis"><summary>Phân tích chi tiết</summary>' +
      '<section class="bte-card" data-testid="key-strengths"><h2>Điểm hòa hợp nổi bật</h2><ul>' +
      bodies(strengths, "highlight")
        .map(function (item) {
          return "<li>" + escapeHtml(item) + "</li>";
        })
        .join("") +
      "</ul></section>" +
      '<section class="bte-card" data-testid="key-risks"><h2>Điểm xung đột cần lưu ý</h2><ul>' +
      bodies(risks, "highlight")
        .map(function (item) {
          return "<li>" + escapeHtml(item) + "</li>";
        })
        .join("") +
      "</ul></section>" +
      (comparisonHtml
        ? '<section class="mc-comparison" data-testid="comparison-board"><h2>So sánh hai chiều</h2><div class="mc-comparison-grid">' +
          comparisonHtml +
          "</div></section>"
        : "") +
      '<section class="mc-domains" data-testid="domain-analysis"><h2>Phân tích chi tiết theo miền</h2><div class="mc-domain-grid">' +
      domainHtml +
      "</div>" +
      (unavailable
        ? '<p class="mc-limitation" data-testid="unavailable-domains">Một số miền chưa đủ dữ liệu cấu trúc để luận riêng.</p>'
        : "") +
      "</section></details>" +
      timingHtml +
      '<section class="mc-actions" data-testid="action-plan"><h2>Kế hoạch hành động</h2><div class="mc-action-grid">' +
      actionHtml +
      "</div></section>" +
      '<section class="bte-card mc-confidence" data-testid="confidence-limitations"><h2>Độ tin cậy và giới hạn</h2>' +
      '<p data-testid="confidence-label">' +
      escapeHtml(CONFIDENCE[(consultation.confidence && consultation.confidence.level) || ""] || "") +
      "</p><p>" +
      escapeHtml(bodies(confidence).join(" ")) +
      "</p>" +
      warningHtml +
      "</section>" +
      '<section class="bte-card" data-testid="conclusion"><h2>Kết luận</h2><p>' +
      escapeHtml(bodies(conclusion)[0] || "") +
      "</p></section>" +
      '<section class="bte-card" data-testid="appendix"><h2>Phụ lục phương pháp</h2><p>' +
      escapeHtml(((appendix && appendix.blocks) || []).filter(function (item) { return item.visibility !== "expert"; }).map(function (item) { return item.body; }).join(" ")) +
      "</p></section>" +
      '<details class="bte-card mc-expert" data-testid="expert-mode"><summary>Xem chế độ chuyên gia</summary>' +
      '<p class="muted">Chế độ chuyên gia ẩn theo mặc định.</p></details>' +
      '<span data-testid="score-grade-guard" hidden>' +
      String(consultation.score) +
      "|" +
      String(consultation.grade) +
      "</span></div>"
    );
  }

  async function request(method, url, body) {
    const res = await fetch(url, {
      method: method,
      headers: body ? { "Content-Type": "application/json", Accept: "application/json" } : { Accept: "application/json" },
      body: body ? JSON.stringify(body) : undefined,
    });
    return res.json();
  }

  function boot() {
    const root = document.getElementById("marriage-consulting-root");
    if (!root) return;
    root.innerHTML =
      '<div class="ds-page mc-page" data-screen="marriage-consulting" data-layout="customer-dashboard">' +
      '<header class="mc-intro"><p class="muted" data-testid="consulting-family">Tư vấn → Tư vấn hôn nhân</p>' +
      '<h1 data-testid="marriage-title">Tư vấn hôn nhân</h1>' +
      "<p class=\"muted\">Phân tích cấu trúc tương hợp của hai người. Kết quả giúp hiểu nền tảng và việc nên làm, không phải lời phán tuyệt đối.</p></header>" +
      '<form class="mc-form" data-testid="marriage-form" novalidate>' +
      '<div class="mc-people" data-testid="people-layout">' +
      personFields("a", "Người A") +
      personFields("b", "Người B") +
      "</div><div class=\"mc-cta\"><button type=\"submit\" id=\"btnMarriageAnalyze\" data-testid=\"submit-marriage\">Phân tích hôn nhân</button></div></form>" +
      '<p class="muted" data-testid="empty-state">Nhập thông tin Người A và Người B rồi chọn Phân tích hôn nhân.</p>' +
      '<div id="mcStatus"></div></div>';

    const form = root.querySelector("[data-testid='marriage-form']");
    const status = document.getElementById("mcStatus");
    form.addEventListener("submit", async function (event) {
      event.preventDefault();
      const personA = personBody("a");
      const personB = personBody("b");
      if (!personA || !personB) {
        status.innerHTML = '<div class="bte-card mc-error" data-testid="error-state" role="alert"><p>Thiếu thông tin bắt buộc.</p></div>';
        return;
      }
      status.innerHTML = '<div class="bte-card mc-loading" data-testid="loading-state" role="status">Đang phân tích hôn nhân...</div>';
      const created = await request("POST", API, { person_a: personA, person_b: personB, options: { language: "vi", audience: "customer" } });
      if (!created.data || created.status !== "SUCCESS") {
        const message = (created.errors && created.errors[0] && created.errors[0].code === "VALIDATION_ERROR")
          ? "Thiếu thông tin bắt buộc."
          : "Không thể hoàn tất phân tích lúc này.";
        status.innerHTML = '<div class="bte-card mc-error" data-testid="error-state" role="alert"><p>' + message + "</p></div>";
        return;
      }
      form.hidden = true;
      const empty = root.querySelector("[data-testid='empty-state']");
      if (empty) empty.hidden = true;
      const reportEnv = await request("GET", API + "/" + created.data.consultation_id + "/report");
      status.innerHTML = renderResult(created.data, reportEnv.data, [].concat(created.warnings || [], reportEnv.warnings || []));
    });
  }

  boot();
})();
