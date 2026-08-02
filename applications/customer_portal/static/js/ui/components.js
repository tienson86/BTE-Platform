/**
 * Presentational UI helpers — no business logic.
 */
(function (global) {
  function esc(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function metricCard(label, value, hint) {
    return (
      '<article class="bte-card ui-metric">' +
      '<div class="ui-metric-label">' +
      esc(label) +
      "</div>" +
      '<div class="ui-metric-value">' +
      esc(value) +
      "</div>" +
      (hint
        ? '<div class="muted" style="font-size:var(--text-sm)">' + esc(hint) + "</div>"
        : "") +
      "</article>"
    );
  }

  function sectionCard(opts) {
    opts = opts || {};
    var id = opts.id || "";
    var title = opts.title || "";
    var description = opts.description || "";
    var badge = opts.badge || "";
    var body = opts.body || "";
    var collapsed = opts.collapsed ? "true" : "false";
    return (
      '<section class="ui-section" data-collapsed="' +
      collapsed +
      '"' +
      (id ? ' id="' + esc(id) + '"' : "") +
      ">" +
      '<div class="ui-section-head">' +
      '<div class="ui-section-title"><strong>' +
      esc(title) +
      "</strong>" +
      (description ? "<span>" + esc(description) + "</span>" : "") +
      "</div>" +
      '<div style="display:flex;gap:0.5rem;align-items:center">' +
      (badge ? '<span class="ui-badge ui-badge-primary">' + esc(badge) + "</span>" : "") +
      '<button type="button" class="ui-section-toggle secondary" data-ui-collapse aria-expanded="' +
      (collapsed === "true" ? "false" : "true") +
      '">▾</button>' +
      "</div></div>" +
      '<div class="ui-section-body">' +
      body +
      "</div></section>"
    );
  }

  function emptyState(title, hint) {
    return (
      '<div class="ui-empty"><strong>' +
      esc(title) +
      "</strong><div>" +
      esc(hint || "") +
      "</div></div>"
    );
  }

  function errorPanel(message, details, requestId) {
    return (
      '<div class="ui-error" role="alert">' +
      "<strong>" +
      esc(message || "Error") +
      "</strong>" +
      (requestId
        ? '<div style="margin-top:0.5rem;font-size:var(--text-sm)">Request ID: <code>' +
          esc(requestId) +
          "</code></div>"
        : "") +
      (details
        ? "<details><summary>Technical details</summary><pre class=\"pre\">" +
          esc(details) +
          "</pre></details>"
        : "") +
      "</div>"
    );
  }

  function statusBadge(text, tone) {
    var cls = "ui-badge";
    if (tone === "success") cls += " ui-badge-success";
    else if (tone === "warning") cls += " ui-badge-warning";
    else if (tone === "danger") cls += " ui-badge-danger";
    else if (tone === "info") cls += " ui-badge-info";
    else cls += " ui-badge-primary";
    return '<span class="' + cls + '">' + esc(text) + "</span>";
  }

  function bindCollapsible(root) {
    if (!root) return;
    root.querySelectorAll("[data-ui-collapse]").forEach(function (btn) {
      if (btn.__bteBound) return;
      btn.__bteBound = true;
      btn.addEventListener("click", function () {
        var section = btn.closest(".ui-section");
        if (!section) return;
        var collapsed = section.getAttribute("data-collapsed") === "true";
        section.setAttribute("data-collapsed", collapsed ? "false" : "true");
        btn.setAttribute("aria-expanded", collapsed ? "true" : "false");
      });
    });
  }

  global.BteUI = {
    esc: esc,
    metricCard: metricCard,
    sectionCard: sectionCard,
    emptyState: emptyState,
    errorPanel: errorPanel,
    statusBadge: statusBadge,
    bindCollapsible: bindCollapsible,
  };
})(typeof window !== "undefined" ? window : globalThis);
