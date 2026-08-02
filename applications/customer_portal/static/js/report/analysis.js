/**
 * Tier 4 — Explainable Analysis Workspace (Blueprint V1.1).
 * Conclusion → reason → rules → evidence → confidence → knowledge.
 * Presentation only — never invents analysis content.
 */
(function (global) {
  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  function esc(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function unavailableText() {
    return t("report.unavailable");
  }

  function StatusBadge(status) {
    var label =
      status === "available"
        ? t("report.an_status_available")
        : status === "partial"
          ? t("report.an_status_partial")
          : t("report.an_status_unavailable");
    return (
      '<span class="ax-badge ax-badge-' +
      esc(status || "unavailable") +
      '" data-component="StatusBadge">' +
      esc(label) +
      "</span>"
    );
  }

  function ConfidenceIndicator(value) {
    if (value == null || value === "") {
      return (
        '<div class="ax-row" data-component="ConfidenceIndicator">' +
        '<div class="ax-k">' +
        esc(t("report.an_confidence")) +
        '</div><div class="ax-v ax-miss">' +
        esc(unavailableText()) +
        "</div></div>"
      );
    }
    return (
      '<div class="ax-row" data-component="ConfidenceIndicator">' +
      '<div class="ax-k">' +
      esc(t("report.an_confidence")) +
      '</div><div class="ax-v">' +
      esc(String(value)) +
      "</div></div>"
    );
  }

  function RulePanel(rules) {
    var items = Array.isArray(rules) ? rules : [];
    if (!items.length) {
      return (
        '<div class="ax-section" data-component="RulePanel">' +
        '<div class="ax-section-title">' +
        esc(t("report.an_rules")) +
        '</div><p class="rpt-caption ax-miss">' +
        esc(unavailableText()) +
        "</p></div>"
      );
    }
    return (
      '<div class="ax-section" data-component="RulePanel">' +
      '<div class="ax-section-title">' +
      esc(t("report.an_rules")) +
      "</div><ul class=\"ax-list\">" +
      items
        .map(function (r) {
          var name = r.name || unavailableText();
          var meta = [];
          if (r.priority != null && r.priority !== "") {
            meta.push(t("report.an_rule_priority") + ": " + r.priority);
          }
          if (r.reason) meta.push(String(r.reason));
          return (
            "<li><strong>" +
            esc(name) +
            "</strong>" +
            (meta.length
              ? '<div class="rpt-caption">' + esc(meta.join(" — ")) + "</div>"
              : "") +
            "</li>"
          );
        })
        .join("") +
      "</ul></div>"
    );
  }

  function EvidencePanel(evidence) {
    var items = Array.isArray(evidence) ? evidence : [];
    if (!items.length) {
      return (
        '<div class="ax-section" data-component="EvidencePanel">' +
        '<div class="ax-section-title">' +
        esc(t("report.an_evidence")) +
        '</div><p class="rpt-caption ax-miss">' +
        esc(unavailableText()) +
        "</p></div>"
      );
    }
    return (
      '<div class="ax-section" data-component="EvidencePanel">' +
      '<div class="ax-section-title">' +
      esc(t("report.an_evidence")) +
      "</div><ul class=\"ax-list\">" +
      items
        .map(function (e) {
          return (
            "<li>" +
            esc(e.label || unavailableText()) +
            (e.reference
              ? '<div class="rpt-caption">' + esc(String(e.reference)) + "</div>"
              : "") +
            "</li>"
          );
        })
        .join("") +
      "</ul></div>"
    );
  }

  function KnowledgeReference(knowledge) {
    if (!knowledge) {
      return (
        '<div class="ax-footer" data-component="KnowledgeReference">' +
        '<span class="rpt-caption ax-miss">' +
        esc(t("report.an_knowledge") + ": " + unavailableText()) +
        "</span></div>"
      );
    }
    var link = knowledge.link || "#tier-knowledge";
    var cite = knowledge.citation || t("report.an_knowledge_open");
    return (
      '<div class="ax-footer" data-component="KnowledgeReference">' +
      '<a class="ax-knowledge-link" href="' +
      esc(link) +
      '">' +
      esc(cite) +
      "</a>" +
      (knowledge.status
        ? '<span class="rpt-caption"> · ' + esc(String(knowledge.status)) + "</span>"
        : "") +
      "</div>"
    );
  }

  function AnalysisHeader(block, title) {
    return (
      '<header class="ax-head" data-component="AnalysisHeader">' +
      "<div>" +
      '<h3 class="rpt-subtitle">' +
      esc(title) +
      "</h3>" +
      '<p class="rpt-caption">' +
      esc(t("report.an_block_hint")) +
      "</p></div>" +
      StatusBadge(block.status) +
      "</header>"
    );
  }

  function AnalysisFooter(block) {
    return KnowledgeReference(block.knowledge);
  }

  function AnalysisBlock(block) {
    var title = t(block.titleKey);
    var open = block.open ? "true" : "false";
    var conclusion = block.conclusion
      ? esc(block.conclusion)
      : esc(unavailableText());
    var summary = block.summary
      ? esc(block.summary)
      : esc(unavailableText());
    var factors = Array.isArray(block.factors) ? block.factors : [];
    var factorsHtml = factors.length
      ? "<ul class=\"ax-list\">" +
        factors
          .map(function (f) {
            return "<li>" + esc(String(f)) + "</li>";
          })
          .join("") +
        "</ul>"
      : '<p class="rpt-caption ax-miss">' + esc(unavailableText()) + "</p>";

    return (
      '<article class="ax-block" data-component="AnalysisBlock" data-ax-id="' +
      esc(block.id) +
      '" data-collapsed="' +
      (open === "true" ? "false" : "true") +
      '">' +
      AnalysisHeader(block, title) +
      '<div class="ax-conclusion">' +
      '<div class="ax-k">' +
      esc(t("report.an_conclusion")) +
      '</div><div class="ax-conclusion-value' +
      (block.conclusion ? "" : " ax-miss") +
      '">' +
      conclusion +
      "</div></div>" +
      '<button type="button" class="secondary ax-toggle" data-ax-toggle aria-expanded="' +
      open +
      '">' +
      esc(open === "true" ? t("report.an_collapse") : t("report.an_expand")) +
      "</button>" +
      '<div class="ax-body">' +
      '<div class="ax-section">' +
      '<div class="ax-section-title">' +
      esc(t("report.an_summary")) +
      '</div><p class="rpt-body' +
      (block.summary ? "" : " ax-miss") +
      '">' +
      summary +
      "</p></div>" +
      '<div class="ax-section">' +
      '<div class="ax-section-title">' +
      esc(t("report.an_factors")) +
      "</div>" +
      factorsHtml +
      "</div>" +
      RulePanel(block.rules) +
      EvidencePanel(block.evidence) +
      ConfidenceIndicator(block.confidence) +
      AnalysisFooter(block) +
      "</div></article>"
    );
  }

  function AnalysisWorkspace(model) {
    var blocks =
      (model && model.analysis && model.analysis.blocks) || [];
    if (!blocks.length) {
      return (
        '<div class="ax-workspace" data-component="AnalysisWorkspace">' +
        '<p class="rpt-caption">' +
        esc(unavailableText()) +
        "</p></div>"
      );
    }
    return (
      '<div class="ax-workspace" data-component="AnalysisWorkspace">' +
      '<p class="rpt-caption ax-hint">' +
      esc(t("report.an_workspace_hint")) +
      "</p>" +
      '<div class="ax-stack">' +
      blocks.map(AnalysisBlock).join("") +
      "</div></div>"
    );
  }

  function bind(root) {
    if (!root) return;
    root.querySelectorAll("[data-ax-toggle]").forEach(function (btn) {
      if (btn.__axBound) return;
      btn.__axBound = true;
      btn.addEventListener("click", function () {
        var block = btn.closest(".ax-block");
        if (!block) return;
        var collapsed = block.getAttribute("data-collapsed") === "true";
        var next = collapsed ? "false" : "true";
        block.setAttribute("data-collapsed", next);
        btn.setAttribute("aria-expanded", next === "false" ? "true" : "false");
        btn.textContent =
          next === "false" ? t("report.an_collapse") : t("report.an_expand");
      });
    });
  }

  global.BteAnalysis = {
    render: AnalysisWorkspace,
    bind: bind,
    components: {
      AnalysisWorkspace: AnalysisWorkspace,
      AnalysisBlock: AnalysisBlock,
      AnalysisHeader: AnalysisHeader,
      EvidencePanel: EvidencePanel,
      RulePanel: RulePanel,
      ConfidenceIndicator: ConfidenceIndicator,
      KnowledgeReference: KnowledgeReference,
      AnalysisFooter: AnalysisFooter,
    },
  };
})(typeof window !== "undefined" ? window : globalThis);
