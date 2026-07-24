/**
 * Report Center (Sprint 8) — presentation only.
 * Renders available report/narrative payloads from local analyze history.
 */
(function () {
  const MISSING = "--";
  const flash = document.getElementById("globalFlash");

  function t(key, vars) {
    return window.BteI18n ? BteI18n.t(key, vars) : key;
  }

  /** @type {Array<object>} */
  let allReports = [];
  /** @type {object|null} */
  let selected = null;
  let viewFormat = "html";

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
    return String(value);
  }

  function formatStatus(status) {
    if (status === "ready") return t("reports.status_ready");
    if (status === "empty") return t("reports.status_empty");
    if (status === "unknown") return t("reports.status_unknown");
    return present(status);
  }

  function composeHtmlDocument(report) {
    var body = report && report.html ? String(report.html) : "";
    var execHtml = "";
    if (
      report &&
      report.data &&
      window.BtePresenters &&
      typeof BtePresenters.executive === "function"
    ) {
      execHtml = BtePresenters.executive(report.data, {
        input: report.input || {},
        chartTitleKey: "chart.info_title",
        includeLunar: false,
      });
    }
    if (window.BtePresenters && typeof BtePresenters.composeExecutiveReport === "function") {
      return BtePresenters.composeExecutiveReport(execHtml, body);
    }
    return (
      "<!DOCTYPE html><html><head><meta charset=\"utf-8\" /></head><body>" +
      execHtml +
      body +
      "</body></html>"
    );
  }

  function composeMarkdownDocument(report) {
    var execTitle = t("executive.title");
    var md = report && report.markdown ? String(report.markdown) : "";
    // Page 1 marker only — detailed executive stays in HTML preview/print.
    return "# " + execTitle + "\n\n---\n\n" + md;
  }

  function boot() {
    if (!window.BtePortal) {
      setEmpty(t("common.api_client_failed"));
      return;
    }
    showSkeleton();
    // Local history only — avoid probing missing list APIs (404 console noise).
    buildLocalReports();
    bindControls();
    refreshList();
    if (allReports.length) selectReport(allReports[0].id);
    else setEmpty(t("reports.empty"));
  }

  function showSkeleton() {
    const list = document.getElementById("reportList");
    if (list) {
      list.innerHTML =
        '<div class="bte-card skeleton-card"></div>' +
        '<div class="bte-card skeleton-card"></div>' +
        '<div class="bte-card skeleton-card"></div>';
    }
  }

  function normalizeReport(raw, fallbackId) {
    if (!raw || typeof raw !== "object") return null;
    const report = raw.report || {};
    const narrative = raw.narrative || {};
    const input = raw.input || {};
    const html = narrative.html || report.html || raw.html || "";
    const markdown = narrative.markdown || report.markdown || raw.markdown || "";
    const pdf =
      raw.pdf ||
      raw.pdf_url ||
      report.pdf ||
      report.pdf_url ||
      narrative.pdf ||
      narrative.pdf_url ||
      null;
    const chartDate = [input.year, input.month, input.day].filter(Boolean).join("-");
    const title =
      raw.title ||
      narrative.title ||
      report.title ||
      (chartDate ? t("reports.chart_title", { date: chartDate }) : null) ||
      t("reports.default_title");
    const created =
      raw.created_at || raw.saved_at || raw.created || raw.timestamp || null;
    const type =
      raw.type ||
      (narrative.html || narrative.markdown
        ? "narrative"
        : report.html || report.markdown
          ? "report"
          : html
            ? "html"
            : markdown
              ? "markdown"
              : "unknown");
    const status = raw.status || (html || markdown || pdf ? "ready" : "empty");
    const id = String(raw.id || fallbackId || "report-" + Date.now());

    return {
      id: id,
      name: title,
      created_at: created,
      type: type,
      status: status,
      has_html: Boolean(html && String(html).trim()),
      has_markdown: Boolean(markdown && String(markdown).trim()),
      has_pdf: Boolean(pdf),
      html: html || "",
      markdown: markdown || "",
      pdf: pdf,
      summary: raw.summary || MISSING,
      source: raw.source || "local",
      input: input,
      data: raw.data || null,
    };
  }

  function buildLocalReports() {
    const seen = {};
    const items = [];

    const hist = BtePortal.getHistory() || [];
    hist.forEach(function (item, idx) {
      const data = item.data || {};
      const entry = normalizeReport(
        {
          id: item.id || "local-" + idx,
          saved_at: item.saved_at,
          input: item.input,
          summary: item.summary,
          report: data.report,
          narrative: data.narrative,
          data: data,
          source: "history",
        },
        "hist-" + idx
      );
      if (!entry) return;
      if (!entry.has_html && !entry.has_markdown && !entry.has_pdf) return;
      if (seen[entry.id]) return;
      seen[entry.id] = true;
      items.push(entry);
    });

    const last = BtePortal.getLastResult();
    if (last && last.data) {
      const entry = normalizeReport(
        {
          id: "last-result",
          saved_at: new Date().toISOString(),
          input: last.input,
          report: last.data.report,
          narrative: last.data.narrative,
          data: last.data,
          source: "last",
          summary: t("reports.latest_summary"),
        },
        "last-result"
      );
      if (entry && (entry.has_html || entry.has_markdown || entry.has_pdf)) {
        if (!seen[entry.id]) {
          items.unshift(entry);
          seen[entry.id] = true;
        }
      }
    }

    allReports = items;
  }

  function bindControls() {
    const search = document.getElementById("reportSearch");
    const filter = document.getElementById("reportFilter");
    const sort = document.getElementById("reportSort");
    if (search) search.addEventListener("input", refreshList);
    if (filter) filter.addEventListener("change", refreshList);
    if (sort) sort.addEventListener("change", refreshList);

    document.querySelectorAll("#formatTabs [data-format]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (btn.disabled) return;
        viewFormat = btn.getAttribute("data-format") || "html";
        document.querySelectorAll("#formatTabs .tab").forEach(function (t) {
          t.classList.toggle("active", t === btn);
        });
        renderPreview();
      });
    });

    const actions = document.getElementById("previewActions");
    if (actions) {
      actions.addEventListener("click", function (event) {
        const btn = event.target.closest("[data-action]");
        if (!btn || !selected) return;
        const action = btn.getAttribute("data-action");
        if (action === "open") openReport(selected);
        if (action === "print") printReport(selected);
        if (action === "copy") copyReport(selected);
        if (action === "download") downloadReport(selected);
        if (action === "share") {
          BtePortal.showFlash(flash, t("reports.share_placeholder"), "success");
        }
      });
    }
  }

  function filteredSorted() {
    const q = (document.getElementById("reportSearch") || {}).value || "";
    const filter = (document.getElementById("reportFilter") || {}).value || "all";
    const sort = (document.getElementById("reportSort") || {}).value || "date_desc";
    const query = String(q).trim().toLowerCase();

    let rows = allReports.slice();
    if (query) {
      rows = rows.filter(function (r) {
        return (
          String(r.name || "").toLowerCase().indexOf(query) >= 0 ||
          String(r.type || "").toLowerCase().indexOf(query) >= 0 ||
          String(r.summary || "").toLowerCase().indexOf(query) >= 0 ||
          String(r.status || "").toLowerCase().indexOf(query) >= 0
        );
      });
    }
    if (filter !== "all") {
      rows = rows.filter(function (r) {
        if (filter === "html") return r.has_html;
        if (filter === "markdown") return r.has_markdown;
        if (filter === "pdf") return r.has_pdf;
        return String(r.type).toLowerCase() === filter;
      });
    }

    rows.sort(function (a, b) {
      if (sort === "name_asc") return String(a.name).localeCompare(String(b.name));
      if (sort === "name_desc") return String(b.name).localeCompare(String(a.name));
      const da = Date.parse(a.created_at || "") || 0;
      const db = Date.parse(b.created_at || "") || 0;
      if (sort === "date_asc") return da - db;
      return db - da;
    });
    return rows;
  }

  function refreshList() {
    const rows = filteredSorted();
    const count = document.getElementById("reportCount");
    if (count) count.textContent = t("reports.count", { n: rows.length });

    const list = document.getElementById("reportList");
    const tbody = document.getElementById("reportTableBody");

    if (!rows.length) {
      if (list) {
        list.innerHTML =
          '<p class="muted dash-empty">' + esc(t("reports.empty")) + "</p>";
      }
      if (tbody) {
        tbody.innerHTML =
          '<tr><td colspan="4" class="muted">' + esc(t("reports.empty")) + "</td></tr>";
      }
      return;
    }

    if (list) {
      list.innerHTML = rows
        .map(function (r) {
          const active = selected && selected.id === r.id ? " is-active" : "";
          return (
            '<article class="bte-card reports-item' +
            active +
            '" data-report-id="' +
            esc(r.id) +
            '">' +
            "<div>" +
            "<strong>" +
            esc(r.name) +
            '</strong><div class="muted">' +
            esc(present(r.created_at)) +
            " · " +
            esc(present(r.type)) +
            "</div>" +
            '<div class="reports-item-flags">' +
            flag(t("common.html"), r.has_html) +
            flag(t("common.markdown"), r.has_markdown) +
            flag(t("common.pdf"), r.has_pdf) +
            '<span class="bte-badge bte-badge-' +
            (r.status === "ready" ? "strong" : "muted") +
            '">' +
            esc(formatStatus(r.status)) +
            "</span></div></div></article>"
          );
        })
        .join("");

      list.querySelectorAll("[data-report-id]").forEach(function (el) {
        el.addEventListener("click", function () {
          selectReport(el.getAttribute("data-report-id"));
        });
      });
    }

    if (tbody) {
      tbody.innerHTML = rows
        .map(function (r) {
          const active = selected && selected.id === r.id ? " is-active" : "";
          return (
            '<tr class="reports-row' +
            active +
            '" data-report-id="' +
            esc(r.id) +
            '">' +
            "<td>" +
            esc(r.name) +
            "</td>" +
            "<td>" +
            esc(present(r.created_at)) +
            "</td>" +
            "<td>" +
            esc(present(r.type)) +
            "</td>" +
            "<td>" +
            esc(formatStatus(r.status)) +
            "</td></tr>"
          );
        })
        .join("");
      tbody.querySelectorAll("[data-report-id]").forEach(function (el) {
        el.addEventListener("click", function () {
          selectReport(el.getAttribute("data-report-id"));
        });
      });
    }
  }

  function flag(label, on) {
    return (
      '<span class="bte-badge bte-badge-' +
      (on ? "pattern" : "muted") +
      '">' +
      esc(label) +
      (on ? "" : ": " + MISSING) +
      "</span>"
    );
  }

  function selectReport(id) {
    selected = allReports.find(function (r) {
      return r.id === id;
    }) || null;
    refreshList();
    renderPreview();
  }

  function setEmpty(message) {
    const empty = document.getElementById("previewEmpty");
    const html = document.getElementById("previewHtml");
    const md = document.getElementById("previewMd");
    const pdf = document.getElementById("previewPdf");
    const actions = document.getElementById("previewActions");
    const tabs = document.getElementById("formatTabs");
    const title = document.getElementById("previewTitle");
    if (title) title.textContent = t("common.preview");
    if (actions) actions.hidden = true;
    if (tabs) tabs.hidden = true;
    if (html) html.hidden = true;
    if (md) md.hidden = true;
    if (pdf) pdf.hidden = true;
    if (empty) {
      empty.hidden = false;
      empty.textContent = message || t("reports.empty");
    }
  }

  function renderPreview() {
    if (!selected) {
      setEmpty(t("reports.empty"));
      return;
    }

    const empty = document.getElementById("previewEmpty");
    const htmlView = document.getElementById("previewHtml");
    const mdView = document.getElementById("previewMd");
    const pdfView = document.getElementById("previewPdf");
    const actions = document.getElementById("previewActions");
    const tabs = document.getElementById("formatTabs");
    const title = document.getElementById("previewTitle");
    const tabPdf = document.getElementById("tabPdf");

    if (title) title.textContent = selected.name || t("common.preview");
    if (actions) actions.hidden = false;
    if (tabs) tabs.hidden = false;
    if (tabPdf) tabPdf.disabled = !selected.has_pdf;

    if (!selected.has_html && !selected.has_markdown && !selected.has_pdf) {
      setEmpty(t("reports.empty"));
      return;
    }

    let format = viewFormat;
    if (format === "html" && !selected.has_html) {
      format = selected.has_markdown ? "markdown" : selected.has_pdf ? "pdf" : "html";
    }
    if (format === "markdown" && !selected.has_markdown) {
      format = selected.has_html ? "html" : selected.has_pdf ? "pdf" : "markdown";
    }
    if (format === "pdf" && !selected.has_pdf) {
      format = selected.has_html ? "html" : "markdown";
    }
    viewFormat = format;
    document.querySelectorAll("#formatTabs .tab").forEach(function (t) {
      t.classList.toggle("active", t.getAttribute("data-format") === format);
    });

    if (empty) empty.hidden = true;
    if (htmlView) {
      htmlView.hidden = format !== "html";
      if (format === "html") {
        htmlView.srcdoc = selected.has_html || (selected.data && window.BtePresenters)
          ? composeHtmlDocument(selected)
          : "<p>" + esc(t("reports.empty")) + "</p>";
      }
    }
    if (mdView) {
      mdView.hidden = format !== "markdown";
      if (format === "markdown") {
        mdView.textContent = selected.has_markdown
          ? composeMarkdownDocument(selected)
          : MISSING;
      }
    }
    if (pdfView) {
      pdfView.hidden = format !== "pdf";
      if (format === "pdf") {
        if (selected.has_pdf && typeof selected.pdf === "string" && /^https?:/i.test(selected.pdf)) {
          pdfView.innerHTML =
            '<p><a href="' +
            esc(selected.pdf) +
            '" target="_blank" rel="noopener">' +
            esc(t("reports.open_pdf")) +
            "</a></p>";
        } else if (selected.has_pdf) {
          pdfView.textContent = t("reports.pdf_ref", { ref: present(selected.pdf) });
        } else {
          pdfView.textContent = t("reports.pdf_unavailable");
        }
      }
    }
  }

  function openReport(report) {
    if (report.data) {
      try {
        const raw = JSON.stringify({ input: report.input || {}, data: report.data });
        sessionStorage.setItem("bte_portal_last_result", raw);
        try {
          localStorage.setItem("bte_portal_last_result", raw);
        } catch (_) {}
      } catch (_) {}
      window.location.href = "/result";
      return;
    }
    if (report.has_html || report.data) {
      const w = window.open("", "_blank");
      if (!w) {
        BtePortal.showFlash(flash, t("reports.popup_blocked"), "error");
        return;
      }
      w.document.write(composeHtmlDocument(report));
      w.document.close();
      return;
    }
    BtePortal.showFlash(flash, t("reports.nothing_to_open"), "error");
  }

  function printReport(report) {
    const html = composeHtmlDocument(report);
    const w = window.open("", "_blank");
    if (!w) {
      BtePortal.showFlash(flash, t("reports.popup_blocked"), "error");
      return;
    }
    w.document.write(html);
    w.document.close();
    w.focus();
    w.print();
  }

  function copyReport(report) {
    const text =
      (viewFormat === "markdown" && report.markdown) ||
      report.markdown ||
      stripHtml(report.html) ||
      MISSING;
    const done = function () {
      BtePortal.showFlash(flash, t("reports.copied"), "success");
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
  }

  function stripHtml(html) {
    try {
      const doc = new DOMParser().parseFromString(String(html || ""), "text/html");
      return (doc.body && doc.body.textContent) || "";
    } catch (_) {
      return String(html || "");
    }
  }

  function fallbackCopy(text) {
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.left = "-9999px";
    document.body.appendChild(ta);
    ta.select();
    try {
      document.execCommand("copy");
    } catch (_) {}
    document.body.removeChild(ta);
  }

  function downloadReport(report) {
    // PDF only if API already provided a URL/reference — never generate PDF.
    if (viewFormat === "pdf" || (!report.has_html && !report.has_markdown && report.has_pdf)) {
      if (typeof report.pdf === "string" && /^https?:/i.test(report.pdf)) {
        window.open(report.pdf, "_blank", "noopener");
        return;
      }
      BtePortal.showFlash(flash, t("reports.pdf_download_unavailable"), "error");
      return;
    }

    if (viewFormat === "markdown" && report.has_markdown) {
      triggerDownload(
        safeFilename(report.name) + ".md",
        composeMarkdownDocument(report),
        "text/markdown;charset=utf-8"
      );
      return;
    }

    if (report.has_html) {
      triggerDownload(
        safeFilename(report.name) + ".html",
        composeHtmlDocument(report),
        "text/html;charset=utf-8"
      );
      return;
    }

    if (report.has_markdown) {
      triggerDownload(
        safeFilename(report.name) + ".md",
        composeMarkdownDocument(report),
        "text/markdown;charset=utf-8"
      );
      return;
    }

    BtePortal.showFlash(flash, t("reports.nothing_to_download"), "error");
  }

  function safeFilename(name) {
    return String(name || "bte-report")
      .replace(/[^\w\-]+/g, "_")
      .slice(0, 80);
  }

  function triggerDownload(filename, content, mime) {
    const blob = new Blob([content], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
