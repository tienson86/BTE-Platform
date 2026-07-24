/**
 * Narrative presentation layer (Sprint 6).
 * Renders narrative JSON as a report — display only, no invented content.
 */
(function (global) {
  const MISSING = "--";

  function esc(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function present(value) {
    if (value === null || value === undefined || value === "") return MISSING;
    if (typeof value === "number" && Number.isNaN(value)) return MISSING;
    return String(value);
  }

  function slugify(text, index) {
    var base = String(text || "section")
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "");
    return "narr-" + (base || "section") + "-" + index;
  }

  function inlineMarkdown(text) {
    var s = esc(text);
    s = s.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    s = s.replace(/__(.+?)__/g, "<strong>$1</strong>");
    s = s.replace(/\*(.+?)\*/g, "<em>$1</em>");
    s = s.replace(/_(.+?)_/g, "<em>$1</em>");
    s = s.replace(/`([^`]+)`/g, "<code>$1</code>");
    return s;
  }

  function renderMarkdownBlocks(md) {
    var lines = String(md || "").replace(/\r\n/g, "\n").split("\n");
    var html = [];
    var i = 0;
    var listOpen = false;
    var quoteOpen = false;

    function closeList() {
      if (listOpen) {
        html.push("</ul>");
        listOpen = false;
      }
    }
    function closeQuote() {
      if (quoteOpen) {
        html.push("</blockquote>");
        quoteOpen = false;
      }
    }

    while (i < lines.length) {
      var trimmed = lines[i].trim();
      if (!trimmed) {
        closeList();
        closeQuote();
        i += 1;
        continue;
      }

      var subHead = /^(#{1,4})\s+(.+)$/.exec(trimmed);
      if (subHead) {
        closeList();
        closeQuote();
        var lvl = subHead[1].length;
        html.push(
          "<h" + lvl + ">" + inlineMarkdown(subHead[2].trim()) + "</h" + lvl + ">"
        );
        i += 1;
        continue;
      }

      var listItem = /^([-*]|\d+\.)\s+(.+)$/.exec(trimmed);
      if (listItem) {
        closeQuote();
        if (!listOpen) {
          html.push("<ul>");
          listOpen = true;
        }
        html.push("<li>" + inlineMarkdown(listItem[2]) + "</li>");
        i += 1;
        continue;
      }

      var quote = /^>\s?(.*)$/.exec(trimmed);
      if (quote) {
        closeList();
        if (!quoteOpen) {
          html.push('<blockquote class="bte-narr-quote">');
          quoteOpen = true;
        }
        html.push("<p>" + inlineMarkdown(quote[1]) + "</p>");
        i += 1;
        continue;
      }

      if (/^(\*\*\*|___|---)\s*$/.test(trimmed)) {
        closeList();
        closeQuote();
        html.push("<hr>");
        i += 1;
        continue;
      }

      closeList();
      closeQuote();
      var buf = [trimmed];
      i += 1;
      while (
        i < lines.length &&
        lines[i].trim() &&
        !/^(#{1,4})\s+/.test(lines[i].trim()) &&
        !/^([-*]|\d+\.)\s+/.test(lines[i].trim()) &&
        !/^>\s?/.test(lines[i].trim())
      ) {
        buf.push(lines[i].trim());
        i += 1;
      }
      var joined = buf.join(" ");
      var highlight = /\*\*[^*]+\*\*/.test(joined);
      html.push(
        '<p' +
          (highlight ? ' class="bte-narr-highlight"' : "") +
          ">" +
          inlineMarkdown(joined) +
          "</p>"
      );
    }

    closeList();
    closeQuote();
    return html.join("\n");
  }

  function renderMarkdownDocument(md) {
    var lines = String(md || "").replace(/\r\n/g, "\n").split("\n");
    var html = [];
    var i = 0;
    var sectionIndex = 0;

    while (i < lines.length) {
      var trimmed = lines[i].trim();
      if (!trimmed) {
        i += 1;
        continue;
      }

      var heading = /^(#{1,4})\s+(.+)$/.exec(trimmed);
      if (heading) {
        var level = heading[1].length;
        var title = heading[2].trim();
        if (level === 1) {
          html.push('<h1 class="bte-narr-title">' + inlineMarkdown(title) + "</h1>");
          i += 1;
          continue;
        }

        var id = slugify(title, sectionIndex++);
        i += 1;
        var bodyLines = [];
        while (i < lines.length) {
          var next = lines[i];
          var nh = /^(#{1,4})\s+/.exec(next.trim());
          if (nh && nh[1].length <= level) break;
          bodyLines.push(next);
          i += 1;
        }
        html.push(
          '<section class="bte-narr-section" data-narr-section="' +
            esc(id) +
            '">' +
            '<header class="bte-narr-section-head">' +
            "<h" +
            level +
            ' id="' +
            esc(id) +
            '">' +
            inlineMarkdown(title) +
            "</h" +
            level +
            ">" +
            '<button type="button" class="bte-narr-toggle secondary" data-narr-toggle="' +
            esc(id) +
            '" aria-expanded="true">Collapse</button>' +
            "</header>" +
            '<div class="bte-narr-section-body" data-narr-body="' +
            esc(id) +
            '">' +
            renderMarkdownBlocks(bodyLines.join("\n")) +
            "</div></section>"
        );
        continue;
      }

      var loose = [];
      while (i < lines.length) {
        var t2 = lines[i].trim();
        if (/^(#{1,4})\s+/.test(t2)) break;
        loose.push(lines[i]);
        i += 1;
      }
      html.push(renderMarkdownBlocks(loose.join("\n")));
    }

    return html.join("\n");
  }

  function extractMarkdownHeadings(md) {
    var headings = [];
    String(md || "")
      .split(/\r?\n/)
      .forEach(function (line) {
        var m = /^(#{2,4})\s+(.+)$/.exec(line.trim());
        if (m) headings.push({ level: m[1].length, title: m[2].trim() });
      });
    return headings;
  }

  function plainTextFromMarkdown(md) {
    return String(md || "")
      .replace(/^#{1,6}\s+/gm, "")
      .replace(/^\s*[-*]\s+/gm, "• ")
      .replace(/^>\s?/gm, "")
      .replace(/\*\*(.+?)\*\*/g, "$1")
      .replace(/\*(.+?)\*/g, "$1")
      .trim();
  }

  function sanitizeHtmlFragment(html) {
    try {
      var doc = new DOMParser().parseFromString(String(html || ""), "text/html");
      doc.querySelectorAll("script,style,iframe,object,embed,link").forEach(function (el) {
        el.remove();
      });
      doc.querySelectorAll("*").forEach(function (el) {
        Array.from(el.attributes).forEach(function (attr) {
          if (/^on/i.test(attr.name) || attr.name === "srcdoc") {
            el.removeAttribute(attr.name);
          }
        });
      });
      return doc.body ? doc.body.innerHTML : "";
    } catch (_) {
      return "<p>" + esc(String(html || MISSING)) + "</p>";
    }
  }

  function wrapHtmlSections(fragmentHtml) {
    try {
      var doc = new DOMParser().parseFromString(
        "<div id='root'>" + fragmentHtml + "</div>",
        "text/html"
      );
      var root = doc.getElementById("root");
      if (!root) return fragmentHtml;
      var children = Array.from(root.childNodes);
      var out = [];
      var sectionIndex = 0;
      var i = 0;
      while (i < children.length) {
        var node = children[i];
        if (node.nodeType === 1 && /^H[2-4]$/i.test(node.tagName)) {
          var title = node.textContent || "Section";
          var id = slugify(title, sectionIndex++);
          var bodyNodes = [];
          i += 1;
          while (i < children.length) {
            var n2 = children[i];
            if (n2.nodeType === 1 && /^H[2-4]$/i.test(n2.tagName)) break;
            bodyNodes.push(n2);
            i += 1;
          }
          var bodyWrap = doc.createElement("div");
          bodyNodes.forEach(function (bn) {
            bodyWrap.appendChild(bn.cloneNode(true));
          });
          out.push(
            '<section class="bte-narr-section" data-narr-section="' +
              esc(id) +
              '">' +
              '<header class="bte-narr-section-head">' +
              "<" +
              node.tagName.toLowerCase() +
              ' id="' +
              esc(id) +
              '">' +
              esc(title) +
              "</" +
              node.tagName.toLowerCase() +
              ">" +
              '<button type="button" class="bte-narr-toggle secondary" data-narr-toggle="' +
              esc(id) +
              '" aria-expanded="true">Collapse</button>' +
              "</header>" +
              '<div class="bte-narr-section-body" data-narr-body="' +
              esc(id) +
              '">' +
              bodyWrap.innerHTML +
              "</div></section>"
          );
          continue;
        }
        if (node.nodeType === 1) out.push(node.outerHTML);
        else if (node.nodeType === 3 && node.textContent.trim()) {
          out.push("<p>" + esc(node.textContent) + "</p>");
        }
        i += 1;
      }
      return out.join("\n") || fragmentHtml;
    } catch (_) {
      return fragmentHtml;
    }
  }

  function buildToc(headings) {
    if (!headings || headings.length < 2) return "";
    var items = headings
      .map(function (h, idx) {
        var id = slugify(h.title, idx);
        return (
          '<li class="bte-narr-toc-l' +
          esc(String(h.level)) +
          '"><a href="#' +
          esc(id) +
          '">' +
          esc(h.title) +
          "</a></li>"
        );
      })
      .join("");
    return (
      '<nav class="bte-card bte-narr-toc" aria-label="Muc luc">' +
      "<h3>Mục lục</h3>" +
      "<ol>" +
      items +
      "</ol>" +
      "</nav>"
    );
  }

  function toolbarHtml() {
    return (
      '<div class="bte-narr-toolbar no-print">' +
      '<button type="button" class="secondary" data-narr-action="copy">Copy</button>' +
      '<button type="button" class="secondary" data-narr-action="print">Print</button>' +
      '<button type="button" class="secondary" data-narr-action="collapse-all">Collapse all</button>' +
      '<button type="button" class="secondary" data-narr-action="expand-all">Expand all</button>' +
      "</div>"
    );
  }

  function metricsBar(metrics, tone) {
    var bits = [];
    if (tone) {
      bits.push(
        '<span class="bte-badge bte-badge-neutral">Tone ' +
          esc(present(tone)) +
          "</span>"
      );
    }
    if (metrics && typeof metrics === "object") {
      ["output_paragraphs", "transitions", "input_units"].forEach(function (key) {
        if (metrics[key] != null) {
          bits.push(
            '<span class="bte-badge bte-badge-pattern">' +
              esc(key.replace(/_/g, " ")) +
              " " +
              esc(present(metrics[key])) +
              "</span>"
          );
        }
      });
    }
    return bits.length ? '<div class="bte-narr-meta">' + bits.join("") + "</div>" : "";
  }

  function resolveSource(data) {
    if (typeof data === "string") {
      return { kind: "text", title: null, content: data, tone: null, metrics: null };
    }
    if (!data || typeof data !== "object") {
      return { kind: "empty", title: null, content: "", tone: null, metrics: null };
    }
    var title = data.title || data.heading || data.name || null;
    var tone = data.tone || null;
    var metrics = data.metrics || null;

    if (data.markdown != null && String(data.markdown).trim()) {
      return { kind: "markdown", title: title, content: String(data.markdown), tone: tone, metrics: metrics };
    }
    if (data.md != null && String(data.md).trim()) {
      return { kind: "markdown", title: title, content: String(data.md), tone: tone, metrics: metrics };
    }
    if (data.html != null && String(data.html).trim()) {
      return { kind: "html", title: title, content: String(data.html), tone: tone, metrics: metrics };
    }
    var text = data.text || data.content || data.body || data.narrative || data.report || null;
    if (text != null && String(text).trim()) {
      return { kind: "text", title: title, content: String(text), tone: tone, metrics: metrics };
    }
    return { kind: "empty", title: title, content: "", tone: tone, metrics: metrics };
  }

  function renderNarrative(narrative) {
    try {
      var source = resolveSource(narrative);
      var hasMdH1 =
        source.kind === "markdown" && /^#\s+/m.test(String(source.content || ""));
      var titleHtml =
        source.title && !hasMdH1
          ? '<h1 class="bte-narr-title">' + esc(source.title) + "</h1>"
          : "";
      var bodyHtml = "";
      var tocHtml = "";
      var copySource = "";

      if (source.kind === "markdown") {
        tocHtml = buildToc(extractMarkdownHeadings(source.content));
        bodyHtml = renderMarkdownDocument(source.content);
        copySource = plainTextFromMarkdown(source.content);
      } else if (source.kind === "html") {
        var sanitized = sanitizeHtmlFragment(source.content);
        bodyHtml = wrapHtmlSections(sanitized);
        try {
          var tmp = new DOMParser().parseFromString(
            "<div>" + sanitized + "</div>",
            "text/html"
          );
          tocHtml = buildToc(
            Array.from(tmp.querySelectorAll("h2,h3,h4")).map(function (el) {
              return {
                level: Number(el.tagName.substring(1)),
                title: el.textContent || "",
              };
            })
          );
          copySource = tmp.body ? tmp.body.textContent || "" : "";
        } catch (_) {
          copySource = "";
        }
      } else if (source.kind === "text") {
        bodyHtml =
          '<div class="bte-narr-section"><div class="bte-narr-section-body"><p>' +
          esc(source.content).replace(/\n{2,}/g, "</p><p>").replace(/\n/g, "<br>") +
          "</p></div></div>";
        copySource = source.content;
      } else {
        bodyHtml =
          '<div class="bte-card"><div class="bte-interp-body">' +
          esc(MISSING) +
          "</div></div>";
        copySource = MISSING;
      }

      return (
        '<section class="bte-narr" aria-label="Narrative">' +
        '<textarea class="bte-narr-copy-source" hidden readonly>' +
        esc(copySource) +
        "</textarea>" +
        '<header class="bte-calendar-head">' +
        "<h2>Narrative</h2>" +
        '<p class="bte-calendar-sub">Báo cáo hoàn chỉnh</p>' +
        "</header>" +
        toolbarHtml() +
        metricsBar(source.metrics, source.tone) +
        titleHtml +
        tocHtml +
        '<article class="bte-narr-report">' +
        bodyHtml +
        "</article>" +
        "</section>"
      );
    } catch (_) {
      return (
        '<section class="bte-narr"><div class="bte-card"><div class="bte-interp-body">' +
        esc(MISSING) +
        "</div></div></section>"
      );
    }
  }

  function setSectionExpanded(root, id, expanded) {
    var section = root.querySelector('[data-narr-section="' + id + '"]');
    var body = root.querySelector('[data-narr-body="' + id + '"]');
    var btn = root.querySelector('[data-narr-toggle="' + id + '"]');
    if (!section || !body || !btn) return;
    section.classList.toggle("is-collapsed", !expanded);
    body.hidden = !expanded;
    btn.setAttribute("aria-expanded", expanded ? "true" : "false");
    btn.textContent = expanded ? "Collapse" : "Expand";
  }

  function fallbackCopy(text) {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.left = "-9999px";
    document.body.appendChild(ta);
    ta.select();
    try {
      document.execCommand("copy");
    } catch (_) {
      /* ignore */
    }
    document.body.removeChild(ta);
  }

  function bindNarrative(root) {
    if (!root) return;
    var host = root.querySelector(".bte-narr") || root;

    host.addEventListener("click", function (event) {
      var target = event.target;
      if (!(target instanceof Element)) return;

      var toggle = target.closest("[data-narr-toggle]");
      if (toggle) {
        var id = toggle.getAttribute("data-narr-toggle");
        var expanded = toggle.getAttribute("aria-expanded") !== "false";
        setSectionExpanded(host, id, !expanded);
        return;
      }

      var actionBtn = target.closest("[data-narr-action]");
      if (!actionBtn) return;
      var action = actionBtn.getAttribute("data-narr-action");

      if (action === "print") {
        global.print();
        return;
      }

      if (action === "copy") {
        var sourceEl = host.querySelector(".bte-narr-copy-source");
        var text =
          (sourceEl && sourceEl.value) ||
          (host.querySelector(".bte-narr-report") || host).innerText ||
          "";
        var done = function () {
          actionBtn.textContent = "Copied";
          setTimeout(function () {
            actionBtn.textContent = "Copy";
          }, 1200);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done).catch(function () {
            fallbackCopy(text);
            done();
          });
        } else {
          fallbackCopy(text);
          done();
        }
        return;
      }

      if (action === "collapse-all") {
        host.querySelectorAll("[data-narr-toggle]").forEach(function (btn) {
          setSectionExpanded(host, btn.getAttribute("data-narr-toggle"), false);
        });
        return;
      }

      if (action === "expand-all") {
        host.querySelectorAll("[data-narr-toggle]").forEach(function (btn) {
          setSectionExpanded(host, btn.getAttribute("data-narr-toggle"), true);
        });
      }
    });
  }

  global.BtePresenters = global.BtePresenters || {};
  global.BtePresenters.narrative = renderNarrative;
  global.BtePresenters.bindNarrative = bindNarrative;
})(window);
