/**
 * Tier 6 — Knowledge & Evidence Workspace (Blueprint V1.1).
 * Insight → Evidence → Applied Rule → Knowledge → Classical → Confidence → Related.
 * Presentation only — never invents evidence, rules, or citations.
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

  function miss(html) {
    return '<p class="rpt-caption kw-miss">' + esc(html || unavailableText()) + "</p>";
  }

  function sourceTypeLabel(type) {
    var key = "report.kw_source_" + String(type || "unknown");
    var label = t(key);
    return label === key ? String(type || "unknown") : label;
  }

  function CitationToolbar(block) {
    return (
      '<div class="kw-toolbar" data-component="CitationToolbar">' +
      '<button type="button" class="secondary kw-tool" data-kw-copy="citation" data-kw-id="' +
      esc(block.id) +
      '">' +
      esc(t("report.kw_copy_citation")) +
      "</button>" +
      '<button type="button" class="secondary kw-tool" data-kw-copy="rule" data-kw-id="' +
      esc(block.id) +
      '">' +
      esc(t("report.kw_copy_rule")) +
      "</button>" +
      "</div>"
    );
  }

  function EvidencePanel(evidence) {
    var items = Array.isArray(evidence) ? evidence : [];
    if (!items.length) {
      return (
        '<section class="kw-section" data-component="EvidencePanel">' +
        '<h4 class="kw-section-title">' +
        esc(t("report.kw_evidence")) +
        "</h4>" +
        miss() +
        "</section>"
      );
    }
    return (
      '<section class="kw-section" data-component="EvidencePanel">' +
      '<h4 class="kw-section-title">' +
      esc(t("report.kw_evidence")) +
      "</h4>" +
      '<ul class="kw-list">' +
      items
        .map(function (e) {
          var bits = [];
          if (e.reason) bits.push(t("report.kw_reason") + ": " + e.reason);
          if (e.condition) bits.push(t("report.kw_condition") + ": " + e.condition);
          if (e.reference) bits.push(String(e.reference));
          return (
            "<li>" +
            '<div class="kw-evidence-label">' +
            esc(e.label || unavailableText()) +
            "</div>" +
            '<div class="rpt-caption">' +
            esc(sourceTypeLabel(e.source_type)) +
            "</div>" +
            (bits.length
              ? '<div class="rpt-caption">' + esc(bits.join(" · ")) + "</div>"
              : "") +
            "</li>"
          );
        })
        .join("") +
      "</ul></section>"
    );
  }

  function RuleReference(rules) {
    var items = Array.isArray(rules) ? rules : [];
    if (!items.length) {
      return (
        '<section class="kw-section" data-component="RuleReference">' +
        '<h4 class="kw-section-title">' +
        esc(t("report.kw_rule")) +
        "</h4>" +
        miss() +
        "</section>"
      );
    }
    return (
      '<section class="kw-section" data-component="RuleReference">' +
      '<h4 class="kw-section-title">' +
      esc(t("report.kw_rule")) +
      "</h4>" +
      '<ul class="kw-list">' +
      items
        .map(function (r) {
          var meta = [];
          if (r.category) {
            meta.push(t("report.kw_rule_category") + ": " + r.category);
          }
          if (r.priority != null && r.priority !== "") {
            meta.push(t("report.kw_rule_priority") + ": " + r.priority);
          }
          return (
            "<li>" +
            "<strong>" +
            esc(r.name || unavailableText()) +
            "</strong>" +
            (meta.length
              ? '<div class="rpt-caption">' + esc(meta.join(" · ")) + "</div>"
              : "") +
            (r.description
              ? '<div class="kw-rule-desc">' + esc(String(r.description)) + "</div>"
              : "") +
            "</li>"
          );
        })
        .join("") +
      "</ul></section>"
    );
  }

  function KnowledgeReference(ref) {
    return (
      '<section class="kw-section" data-component="KnowledgeReference">' +
      '<h4 class="kw-section-title">' +
      esc(t("report.kw_knowledge_ref")) +
      "</h4>" +
      (ref
        ? '<p class="kw-body">' + esc(String(ref)) + "</p>"
        : miss()) +
      "</section>"
    );
  }

  function ClassicalReference(classical) {
    var items = Array.isArray(classical) ? classical : [];
    if (!items.length) {
      return (
        '<section class="kw-section" data-component="ClassicalReference">' +
        '<h4 class="kw-section-title">' +
        esc(t("report.kw_classical")) +
        "</h4>" +
        miss() +
        "</section>"
      );
    }
    return (
      '<section class="kw-section" data-component="ClassicalReference">' +
      '<h4 class="kw-section-title">' +
      esc(t("report.kw_classical")) +
      "</h4>" +
      '<ul class="kw-list">' +
      items
        .map(function (c) {
          var loc = [];
          if (c.chapter) loc.push(t("report.kw_thien") + ": " + c.chapter);
          if (c.section) loc.push(t("report.kw_chuong") + ": " + c.section);
          if (c.passage) loc.push(t("report.kw_doan") + ": " + c.passage);
          return (
            "<li>" +
            (c.book
              ? "<strong>" + esc(String(c.book)) + "</strong>"
              : '<span class="kw-miss">' + esc(unavailableText()) + "</span>") +
            (loc.length
              ? '<div class="rpt-caption">' + esc(loc.join(" · ")) + "</div>"
              : "") +
            (c.quote
              ? '<blockquote class="kw-quote">' + esc(String(c.quote)) + "</blockquote>"
              : "") +
            "</li>"
          );
        })
        .join("") +
      "</ul></section>"
    );
  }

  function ConfidencePanel(value) {
    return (
      '<section class="kw-section" data-component="ConfidencePanel">' +
      '<h4 class="kw-section-title">' +
      esc(t("report.kw_confidence")) +
      "</h4>" +
      (value != null && value !== ""
        ? '<p class="kw-body">' + esc(String(value)) + "</p>"
        : miss()) +
      "</section>"
    );
  }

  function RelatedSectionLinks(related) {
    var items = Array.isArray(related) ? related : [];
    if (!items.length) {
      return (
        '<section class="kw-section" data-component="RelatedSectionLinks">' +
        '<h4 class="kw-section-title">' +
        esc(t("report.kw_related")) +
        "</h4>" +
        miss() +
        "</section>"
      );
    }
    return (
      '<section class="kw-section" data-component="RelatedSectionLinks">' +
      '<h4 class="kw-section-title">' +
      esc(t("report.kw_related")) +
      "</h4>" +
      '<ul class="kw-related">' +
      items
        .map(function (r) {
          var kind =
            r.type === "analysis"
              ? t("report.kw_related_analysis")
              : t("report.kw_related_interp");
          return (
            "<li><a class=\"kw-related-link\" href=\"" +
            esc(r.href) +
            '">' +
            esc(kind + ": " + (r.label || r.id)) +
            "</a></li>"
          );
        })
        .join("") +
      "</ul></section>"
    );
  }

  function KnowledgeFooter() {
    return (
      '<footer class="kw-footer" data-component="KnowledgeFooter">' +
      '<p class="rpt-caption">' +
      esc(t("report.kw_footer")) +
      "</p></footer>"
    );
  }

  function KnowledgeBlock(block) {
    var open = !!block.open;
    var insight = block.insight
      ? esc(String(block.insight))
      : esc(unavailableText());
    return (
      '<article class="kw-block" data-component="KnowledgeBlock" data-kw-id="' +
      esc(block.id) +
      '" data-collapsed="' +
      (open ? "false" : "true") +
      '" data-kw-search="' +
      esc(
        [
          block.insight,
          block.summary,
          block.knowledge_ref,
          (block.evidence || [])
            .map(function (e) {
              return e.label;
            })
            .join(" "),
          (block.rules || [])
            .map(function (r) {
              return r.name;
            })
            .join(" "),
          (block.classical || [])
            .map(function (c) {
              return [c.book, c.quote].join(" ");
            })
            .join(" "),
        ]
          .filter(Boolean)
          .join(" ")
          .toLowerCase()
      ) +
      '">' +
      '<header class="kw-head">' +
      "<div>" +
      '<h3 class="rpt-subtitle">' +
      esc(t("report.kw_insight")) +
      "</h3>" +
      '<p class="kw-insight' +
      (block.insight ? "" : " kw-miss") +
      '">' +
      insight +
      "</p>" +
      (block.summary
        ? '<p class="rpt-caption kw-summary">' + esc(String(block.summary)) + "</p>"
        : "") +
      "</div>" +
      '<button type="button" class="secondary kw-toggle" data-kw-toggle aria-expanded="' +
      (open ? "true" : "false") +
      '">' +
      esc(open ? t("report.kw_collapse") : t("report.kw_expand")) +
      "</button></header>" +
      '<div class="kw-body-wrap">' +
      CitationToolbar(block) +
      EvidencePanel(block.evidence) +
      RuleReference(block.rules) +
      KnowledgeReference(block.knowledge_ref) +
      ClassicalReference(block.classical) +
      ConfidencePanel(block.confidence) +
      RelatedSectionLinks(block.related) +
      KnowledgeFooter() +
      "</div></article>"
    );
  }

  function KnowledgeWorkspace(model) {
    var k = (model && model.knowledge) || {};
    var blocks = Array.isArray(k.blocks) ? k.blocks : [];
    var emptyBlocks = !blocks.length
      ? '<div class="kw-empty">' + miss(t("report.kw_empty")) + "</div>"
      : "";

    return (
      '<div class="kw-workspace" data-component="KnowledgeWorkspace">' +
      '<p class="rpt-caption kw-hint">' +
      esc(t("report.kw_workspace_hint")) +
      "</p>" +
      '<div class="kw-controls" role="search">' +
      '<label class="kw-filter-label" for="kw-filter-input">' +
      esc(t("report.kw_filter")) +
      "</label>" +
      '<input id="kw-filter-input" class="kw-filter" type="search" data-kw-filter placeholder="' +
      esc(t("report.kw_filter_ph")) +
      '" autocomplete="off" />' +
      '<div class="kw-bulk">' +
      '<button type="button" class="secondary" data-kw-expand-all>' +
      esc(t("report.kw_expand_all")) +
      "</button>" +
      '<button type="button" class="secondary" data-kw-collapse-all>' +
      esc(t("report.kw_collapse_all")) +
      "</button></div></div>" +
      emptyBlocks +
      '<div class="kw-stack">' +
      blocks.map(KnowledgeBlock).join("") +
      "</div></div>"
    );
  }

  function blockPayload(root, id) {
    var model = root.__kwModel;
    if (!model || !model.knowledge || !Array.isArray(model.knowledge.blocks)) {
      return null;
    }
    return model.knowledge.blocks.filter(function (b) {
      return b.id === id;
    })[0];
  }

  function copyText(text) {
    if (!text) return;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).catch(function () {});
      return;
    }
    try {
      var ta = document.createElement("textarea");
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
    } catch (err) {
      /* presentation-only; ignore copy failures */
    }
  }

  function formatCitation(block) {
    if (!block) return "";
    var lines = [];
    if (block.insight) lines.push(block.insight);
    (block.classical || []).forEach(function (c) {
      var parts = [c.book, c.chapter, c.section, c.passage].filter(Boolean);
      if (parts.length) lines.push(parts.join(" · "));
      if (c.quote) lines.push('"' + c.quote + '"');
    });
    if (block.knowledge_ref) lines.push(String(block.knowledge_ref));
    return lines.join("\n");
  }

  function formatRules(block) {
    if (!block) return "";
    return (block.rules || [])
      .map(function (r) {
        var parts = [r.name];
        if (r.category) parts.push(r.category);
        if (r.priority != null) {
          parts.push(t("report.kw_rule_priority") + ": " + r.priority);
        }
        if (r.description) parts.push(r.description);
        return parts.filter(Boolean).join(" — ");
      })
      .join("\n");
  }

  function setCollapsed(blockEl, collapsed) {
    blockEl.setAttribute("data-collapsed", collapsed ? "true" : "false");
    var btn = blockEl.querySelector("[data-kw-toggle]");
    if (btn) {
      btn.setAttribute("aria-expanded", collapsed ? "false" : "true");
      btn.textContent = collapsed ? t("report.kw_expand") : t("report.kw_collapse");
    }
  }

  function bind(root, model) {
    if (!root) return;
    var workspace = root.querySelector('[data-component="KnowledgeWorkspace"]');
    if (!workspace) return;
    if (model) workspace.__kwModel = model;
    else if (root.__kwModel) workspace.__kwModel = root.__kwModel;

    workspace.querySelectorAll("[data-kw-toggle]").forEach(function (btn) {
      if (btn.__kwBound) return;
      btn.__kwBound = true;
      btn.addEventListener("click", function () {
        var block = btn.closest(".kw-block");
        if (!block) return;
        var collapsed = block.getAttribute("data-collapsed") === "true";
        setCollapsed(block, !collapsed);
      });
    });

    var filter = workspace.querySelector("[data-kw-filter]");
    if (filter && !filter.__kwBound) {
      filter.__kwBound = true;
      filter.addEventListener("input", function () {
        var q = String(filter.value || "")
          .trim()
          .toLowerCase();
        workspace.querySelectorAll(".kw-block").forEach(function (el) {
          var hay = el.getAttribute("data-kw-search") || "";
          var show = !q || hay.indexOf(q) !== -1;
          el.hidden = !show;
        });
      });
    }

    var expandAll = workspace.querySelector("[data-kw-expand-all]");
    if (expandAll && !expandAll.__kwBound) {
      expandAll.__kwBound = true;
      expandAll.addEventListener("click", function () {
        workspace.querySelectorAll(".kw-block").forEach(function (el) {
          setCollapsed(el, false);
        });
      });
    }

    var collapseAll = workspace.querySelector("[data-kw-collapse-all]");
    if (collapseAll && !collapseAll.__kwBound) {
      collapseAll.__kwBound = true;
      collapseAll.addEventListener("click", function () {
        workspace.querySelectorAll(".kw-block").forEach(function (el) {
          setCollapsed(el, true);
        });
      });
    }

    workspace.querySelectorAll("[data-kw-copy]").forEach(function (btn) {
      if (btn.__kwBound) return;
      btn.__kwBound = true;
      btn.addEventListener("click", function () {
        var id = btn.getAttribute("data-kw-id");
        var kind = btn.getAttribute("data-kw-copy");
        var block = blockPayload(workspace, id);
        if (kind === "citation") copyText(formatCitation(block));
        else if (kind === "rule") copyText(formatRules(block));
      });
    });

    workspace.querySelectorAll(".kw-related-link").forEach(function (link) {
      if (link.__kwBound) return;
      link.__kwBound = true;
      link.addEventListener("click", function (ev) {
        var href = link.getAttribute("href") || "";
        if (href.indexOf("#analysis-") === 0) {
          var axId = href.slice("#analysis-".length);
          var target =
            document.querySelector('.ax-block[data-ax-id="' + axId + '"]') ||
            document.getElementById("tier-analysis");
          if (target) {
            ev.preventDefault();
            target.scrollIntoView({ behavior: "smooth", block: "start" });
          }
        }
      });
    });
  }

  global.BteKnowledge = {
    render: KnowledgeWorkspace,
    bind: bind,
    components: {
      KnowledgeWorkspace: KnowledgeWorkspace,
      KnowledgeBlock: KnowledgeBlock,
      EvidencePanel: EvidencePanel,
      RuleReference: RuleReference,
      ClassicalReference: ClassicalReference,
      ConfidencePanel: ConfidencePanel,
      RelatedSectionLinks: RelatedSectionLinks,
      CitationToolbar: CitationToolbar,
      KnowledgeFooter: KnowledgeFooter,
      KnowledgeReference: KnowledgeReference,
    },
  };
})(typeof window !== "undefined" ? window : globalThis);
