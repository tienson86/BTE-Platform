/**
 * Tier 5 — Interpretation Document Experience (Blueprint V1.1).
 * Professional reading document — not a dashboard of cards.
 * Presentation only; never invents interpretation prose.
 */
(function (global) {
  var MISSING = "--";

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

  function unavailable() {
    return t("report.unavailable");
  }

  function paragraphs(text) {
    return String(text || "")
      .split(/\n{2,}/)
      .map(function (p) {
        return p.trim();
      })
      .filter(Boolean)
      .map(function (p) {
        return (
          '<p class="idoc-p">' +
          esc(p).replace(/\n/g, "<br>") +
          "</p>"
        );
      })
      .join("");
  }

  function DocumentHeader(interp) {
    var conf = interp && interp.confidence;
    var confHtml =
      conf != null && conf !== "" && conf !== MISSING
        ? '<p class="idoc-confidence rpt-caption">' +
          esc(t("interpretation.confidence", { value: String(conf) })) +
          "</p>"
        : "";
    return (
      '<header class="idoc-header" data-component="DocumentHeader">' +
      '<p class="idoc-eyebrow">' +
      esc(t("report.idoc_eyebrow")) +
      "</p>" +
      '<h2 class="idoc-doc-title">' +
      esc(t("report.idoc_title")) +
      "</h2>" +
      '<p class="idoc-lead rpt-caption">' +
      esc(t("report.idoc_lead")) +
      "</p>" +
      confHtml +
      "</header>"
    );
  }

  function ReadingProgress() {
    return (
      '<div class="idoc-progress" data-component="ReadingProgress" aria-hidden="true">' +
      '<div class="idoc-progress-bar" data-idoc-progress style="width:0%"></div></div>'
    );
  }

  function TableOfContents(toc, show) {
    if (!show || !toc || toc.length < 2) return "";
    return (
      '<nav class="idoc-toc" data-component="TableOfContents" aria-label="' +
      esc(t("report.toc")) +
      '">' +
      '<div class="idoc-toc-title">' +
      esc(t("report.toc")) +
      "</div><ol class=\"idoc-toc-list\">" +
      toc
        .map(function (item, idx) {
          return (
            '<li><a class="idoc-toc-link' +
            (idx === 0 ? " is-active" : "") +
            '" href="#' +
            esc(item.anchor) +
            '" data-idoc-toc="' +
            esc(item.anchor) +
            '"><span class="idoc-toc-num">' +
            esc(String(item.number)) +
            ".</span> " +
            esc(t(item.titleKey)) +
            (item.available
              ? ""
              : ' <span class="idoc-toc-miss">·</span>') +
            "</a></li>"
          );
        })
        .join("") +
      "</ol></nav>"
    );
  }

  function CalloutBox(text, kind) {
    if (!text) return "";
    return (
      '<aside class="idoc-callout idoc-callout-' +
      esc(kind || "insight") +
      '" data-component="CalloutBox" role="note">' +
      '<div class="idoc-callout-label">' +
      esc(
        kind === "caution"
          ? t("report.callout_caution")
          : t("report.callout_insight")
      ) +
      '</div><p class="idoc-callout-body">' +
      esc(text) +
      "</p></aside>"
    );
  }

  function CitationBlock(citations) {
    var items = Array.isArray(citations) ? citations : [];
    if (!items.length) return "";
    return (
      '<div class="idoc-citations" data-component="CitationBlock">' +
      '<div class="idoc-subhead">' +
      esc(t("report.idoc_citations")) +
      "</div><ul>" +
      items
        .map(function (c) {
          return (
            "<li>" +
            esc(c.label) +
            (c.reference
              ? '<span class="rpt-caption"> — ' + esc(c.reference) + "</span>"
              : "") +
            "</li>"
          );
        })
        .join("") +
      "</ul></div>"
    );
  }

  function ReferenceList(chapter) {
    var html = CitationBlock(chapter.citations);
    if (chapter.knowledge) {
      html +=
        '<p class="idoc-knowledge"><a href="#tier-knowledge">' +
        esc(String(chapter.knowledge)) +
        "</a></p>";
    }
    if (!html && chapter.id === "references" && !chapter.available) {
      html =
        '<p class="idoc-empty rpt-caption">' +
        esc(unavailable()) +
        ' · <a href="#tier-knowledge">' +
        esc(t("report.an_knowledge_open")) +
        "</a></p>";
    }
    return html
      ? '<div class="idoc-refs" data-component="ReferenceList">' + html + "</div>"
      : "";
  }

  function SectionHeading(chapter) {
    return (
      '<header class="idoc-section-head" data-component="SectionHeading">' +
      '<p class="idoc-section-num">' +
      esc(t("report.idoc_chapter", { n: String(chapter.number) })) +
      "</p>" +
      '<h2 class="idoc-h2" id="' +
      esc(chapter.anchor) +
      '-title">' +
      esc(t(chapter.titleKey)) +
      "</h2></header>"
    );
  }

  function SectionSummary(summary) {
    if (!summary) return "";
    return (
      '<p class="idoc-section-summary" data-component="SectionSummary">' +
      esc(summary) +
      "</p>"
    );
  }

  function DocumentSection(chapter) {
    var bodyHtml = chapter.available && chapter.body
      ? paragraphs(chapter.body)
      : '<p class="idoc-empty rpt-caption">' + esc(unavailable()) + "</p>";
    var calloutKind = chapter.id === "advice" ? "caution" : "insight";
    return (
      '<section class="idoc-section" data-component="DocumentSection" id="' +
      esc(chapter.anchor) +
      '" data-idoc-section="' +
      esc(chapter.anchor) +
      '" aria-labelledby="' +
      esc(chapter.anchor) +
      '-title">' +
      SectionHeading(chapter) +
      SectionSummary(chapter.summary) +
      '<div class="idoc-section-body">' +
      bodyHtml +
      "</div>" +
      CalloutBox(chapter.callout, calloutKind) +
      ReferenceList(chapter) +
      "</section>"
    );
  }

  function ExecutiveSummary(exec) {
    if (!exec || !exec.available) {
      return (
        '<section class="idoc-exec" data-component="ExecutiveSummary">' +
        '<h2 class="idoc-h2">' +
        esc(t("report.idoc_exec_summary")) +
        '</h2><p class="idoc-empty rpt-caption">' +
        esc(unavailable()) +
        "</p></section>"
      );
    }
    return (
      '<section class="idoc-exec" data-component="ExecutiveSummary" id="interp-exec">' +
      '<h2 class="idoc-h2">' +
      esc(t("report.idoc_exec_summary")) +
      "</h2>" +
      (exec.summary
        ? '<p class="idoc-section-summary">' + esc(exec.summary) + "</p>"
        : "") +
      (exec.body ? paragraphs(exec.body) : "") +
      CalloutBox(exec.callout, "insight") +
      "</section>"
    );
  }

  function DocumentFooter() {
    return (
      '<footer class="idoc-footer" data-component="DocumentFooter">' +
      '<p class="rpt-caption">' +
      esc(t("report.idoc_footer")) +
      ' <a href="#tier-knowledge">' +
      esc(t("report.an_knowledge_open")) +
      "</a></p></footer>"
    );
  }

  function InterpretationDocument(model) {
    var interp = (model && model.interpretation) || {};
    var doc = interp.document || {
      chapters: interp.chapters || [],
      executive: { available: false },
      toc: [],
      showToc: false,
    };
    return (
      '<article class="idoc" data-component="InterpretationDocument">' +
      ReadingProgress() +
      DocumentHeader(interp) +
      TableOfContents(doc.toc, doc.showToc) +
      ExecutiveSummary(doc.executive) +
      '<div class="idoc-chapters">' +
      (doc.chapters || []).map(DocumentSection).join("") +
      "</div>" +
      DocumentFooter() +
      "</article>"
    );
  }

  function bind(root) {
    if (!root) return;
    var doc = root.querySelector(".idoc");
    if (!doc) return;

    var links = doc.querySelectorAll("[data-idoc-toc]");
    var sections = doc.querySelectorAll("[data-idoc-section]");
    var bar = doc.querySelector("[data-idoc-progress]");

    function setActive(id) {
      links.forEach(function (a) {
        a.classList.toggle("is-active", a.getAttribute("data-idoc-toc") === id);
      });
    }

    links.forEach(function (a) {
      if (a.__idocBound) return;
      a.__idocBound = true;
      a.addEventListener("click", function (ev) {
        var id = a.getAttribute("data-idoc-toc");
        var el = id && doc.querySelector("#" + id);
        if (!el) return;
        ev.preventDefault();
        el.scrollIntoView({ behavior: "smooth", block: "start" });
        setActive(id);
      });
    });

    if (window.IntersectionObserver && sections.length) {
      var observer = new IntersectionObserver(
        function (entries) {
          var visible = entries
            .filter(function (e) {
              return e.isIntersecting;
            })
            .sort(function (a, b) {
              return b.intersectionRatio - a.intersectionRatio;
            });
          if (visible[0] && visible[0].target) {
            setActive(visible[0].target.id);
          }
        },
        { root: null, rootMargin: "-25% 0px -55% 0px", threshold: [0.1, 0.25, 0.5] }
      );
      sections.forEach(function (sec) {
        observer.observe(sec);
      });
    }

    if (bar) {
      var onScroll = function () {
        var rect = doc.getBoundingClientRect();
        var total = doc.offsetHeight - window.innerHeight;
        var scrolled = Math.min(
          1,
          Math.max(0, (0 - rect.top) / (total > 0 ? total : 1))
        );
        bar.style.width = Math.round(scrolled * 100) + "%";
      };
      if (!doc.__idocScrollBound) {
        doc.__idocScrollBound = true;
        window.addEventListener("scroll", onScroll, { passive: true });
        onScroll();
      }
    }
  }

  global.BteInterpretationDoc = {
    render: InterpretationDocument,
    bind: bind,
    components: {
      InterpretationDocument: InterpretationDocument,
      DocumentHeader: DocumentHeader,
      TableOfContents: TableOfContents,
      DocumentSection: DocumentSection,
      SectionHeading: SectionHeading,
      SectionSummary: SectionSummary,
      CalloutBox: CalloutBox,
      CitationBlock: CitationBlock,
      ReferenceList: ReferenceList,
      ReadingProgress: ReadingProgress,
      DocumentFooter: DocumentFooter,
    },
  };
})(typeof window !== "undefined" ? window : globalThis);
