/**
 * BTE Portal — Result Storage Service.
 *
 * Single owner of analyze-result persistence. Pages must never call
 * sessionStorage / localStorage for results directly.
 *
 * Keys are separated so that browsing never corrupts the analyze result:
 *   bte_last_result  — the result produced by the last Analyze run (current).
 *   bte_history      — append-only list of past runs.
 *   bte_view_result  — transient History pointer. Normal /result never reads it.
 *   loadForView()    — EXPLICIT LEGACY ONLY (`/result?legacy=1`).
 */
(function (global) {
  const LAST_KEY = "bte_last_result";
  const HISTORY_KEY = "bte_history";
  const VIEW_KEY = "bte_view_result";
  const CURRENT_ID_KEY = "bte_current_analysis_id";
  const VIEW_ID_KEY = "bte_view_analysis_id";
  const CALENDAR_RULE_VERSION = "G1-10C";
  // Pre-refactor keys — read-only, so existing browser sessions keep their data.
  const LEGACY_LAST_KEY = "bte_portal_last_result";
  const LEGACY_HISTORY_KEY = "bte_portal_history";
  const HISTORY_LIMIT = 30;
  let synthesizedIdSeq = 0;

  function sessionStore() {
    try {
      return global.sessionStorage || null;
    } catch (_) {
      return null;
    }
  }

  function localStore() {
    try {
      return global.localStorage || null;
    } catch (_) {
      return null;
    }
  }

  function writeRaw(key, raw, sessionOnly) {
    let wrote = false;
    const session = sessionStore();
    if (session) {
      try {
        session.setItem(key, raw);
        wrote = true;
      } catch (_) {
        /* quota */
      }
    }
    if (sessionOnly) return wrote;
    const local = localStore();
    if (local) {
      try {
        local.setItem(key, raw);
        wrote = true;
      } catch (_) {
        /* private mode / quota — sessionStorage is enough for same-tab Result */
      }
    }
    return wrote;
  }

  function removeRaw(keys) {
    const stores = [sessionStore(), localStore()];
    keys.forEach(function (key) {
      stores.forEach(function (store) {
        if (!store) return;
        try {
          store.removeItem(key);
        } catch (_) {
          /* ignore */
        }
      });
    });
  }

  function readRaw(keys) {
    const stores = [sessionStore(), localStore()];
    for (let i = 0; i < keys.length; i += 1) {
      for (let j = 0; j < stores.length; j += 1) {
        const store = stores[j];
        if (!store) continue;
        try {
          const raw = store.getItem(keys[i]);
          if (raw) return raw;
        } catch (_) {
          /* ignore */
        }
      }
    }
    return null;
  }

  function readValue(keys) {
    const raw = readRaw(keys);
    if (!raw) return null;
    try {
      return JSON.parse(raw);
    } catch (_) {
      return null;
    }
  }

  function encode(value) {
    try {
      return JSON.stringify(value);
    } catch (_) {
      return null;
    }
  }

  function normalizeResult(result) {
    if (!result || typeof result !== "object") return null;
    if (!result.data || typeof result.data !== "object") return null;
    const data = Object.assign({}, result.data);
    if (Object.prototype.hasOwnProperty.call(result.data, "narrative_result")) {
      data.narrative_result = result.data.narrative_result;
    }
    if (Object.prototype.hasOwnProperty.call(result.data, "narrative_v2_shadow")) {
      data.narrative_v2_shadow = result.data.narrative_v2_shadow;
    }
    const analysisId =
      result.analysis_id ||
      result.id ||
      data.analysis_id ||
      data.request_id;
    if (analysisId && !data.analysis_id) {
      data.analysis_id = String(analysisId);
    }
    return { input: result.input || {}, data: data };
  }

  function makeAnalysisId(entry) {
    const fromEntry = entry && (entry.analysis_id || entry.id);
    if (fromEntry) return String(fromEntry);
    const data = entry && entry.data;
    if (data && (data.analysis_id || data.request_id || data.case_id)) {
      return String(data.analysis_id || data.request_id || data.case_id);
    }
    const input = (entry && entry.input) || {};
    synthesizedIdSeq += 1;
    return ["bte", input.year || 0, input.month || 0, input.day || 0, input.hour || 0, input.minute || 0, Date.now(), synthesizedIdSeq].join("-");
  }

  function displayAnalysisId(entry) {
    const fromEntry = entry && (entry.analysis_id || entry.id);
    if (fromEntry) return String(fromEntry);
    const data = entry && entry.data;
    if (data && (data.analysis_id || data.request_id || data.case_id)) {
      return String(data.analysis_id || data.request_id || data.case_id);
    }
    const input = (entry && entry.input) || {};
    return ["bte", input.year || 0, input.month || 0, input.day || 0, input.hour || 0, input.minute || 0].join("-");
  }

  function writeCurrentAnalysisId(id) {
    if (!id) return;
    writeRaw(CURRENT_ID_KEY, encode(String(id)), false);
  }

  function readCurrentAnalysisId() {
    const value = readValue([CURRENT_ID_KEY]);
    return typeof value === "string" && value.trim() ? value : null;
  }

  /**
   * Last Analyze result plus the current-session analysis id.
   * Does not change load() JSON shape used by existing store tests.
   */
  function isIncompatibleCalendarRule(data) {
    const cal = data && data.calendar;
    if (!cal || typeof cal !== "object") return true;
    const version = cal.calendar_rule_version;
    if (!version || version !== CALENDAR_RULE_VERSION) return true;
    return false;
  }

  function loadCurrent() {
    const entry = load();
    if (!entry) return null;
    if (isIncompatibleCalendarRule(entry.data)) return null;
    return {
      input: entry.input || {},
      data: entry.data,
      analysis_id: readCurrentAnalysisId() || displayAnalysisId(entry),
      source: "current",
    };
  }

  function rowAnalysisId(row) {
    if (!row || typeof row !== "object") return "";
    return String(displayAnalysisId(row) || "").trim();
  }

  function historyRecordFromRow(row, analysisId) {
    if (!row || typeof row !== "object") return null;
    const id = String(analysisId || rowAnalysisId(row) || "").trim();
    if (!row.data || typeof row.data !== "object") {
      return {
        input: row.input || {},
        data: null,
        analysis_id: id || null,
        source: "history",
        corrupt: true,
      };
    }
    return {
      input: row.input || {},
      data: row.data,
      analysis_id: id,
      source: "history",
    };
  }

  function findHistoryById(expectedId) {
    const wanted = expectedId != null && String(expectedId).trim() ? String(expectedId).trim() : "";
    if (!wanted) return null;
    const view = peekView();
    if (view) {
      const viewId = readValue([VIEW_ID_KEY]) || view.analysis_id || view.id || displayAnalysisId(view);
      if (String(viewId) === wanted) {
        return historyRecordFromRow(
          {
            input: view.input || {},
            data: view.data,
            analysis_id: viewId,
          },
          wanted,
        );
      }
    }
    const list = loadHistory();
    for (let i = 0; i < list.length; i += 1) {
      const row = list[i];
      if (rowAnalysisId(row) === wanted) {
        return historyRecordFromRow(row, wanted);
      }
    }
    return null;
  }

  /**
   * Customer display payload.
   *
   * Default: fresh current analysis.
   * History: only when fromHistory is true AND expectedId matches a stored snapshot.
   * Explicit History never falls back to current.
   */
  function resolveForDisplay(fromHistory, expectedId) {
    const wanted = expectedId != null && String(expectedId).trim() ? String(expectedId).trim() : "";
    if (fromHistory && wanted) {
      return findHistoryById(wanted);
    }
    const current = loadCurrent();
    if (current) return current;
    return null;
  }

  function defaultSummary(entry) {
    const interp = entry.data && entry.data.interpretation;
    const summary = interp && (interp.summary || interp.interpretation_summary);
    if (summary) return summary;
    return global.BteI18n ? global.BteI18n.t("api.analyze_result") : "Analyze result";
  }

  function historyRow(entry, forcedId) {
    const analysisId = forcedId || makeAnalysisId(entry);
    const meta = (entry.data && entry.data.result_meta) || {};
    const source = (entry.data && entry.data.useful_god_source) || {};
    const narrative = (entry.data && entry.data.narrative_result) || {};
    const createdAt = meta.created_at || new Date().toISOString();
    return {
      id: analysisId,
      analysis_id: analysisId,
      request_id: (entry.data && entry.data.request_id) || meta.analysis_id || analysisId,
      saved_at: createdAt,
      created_at: createdAt,
      customer_contract: source.contract || meta.customer_contract || null,
      narrative_contract: narrative.contract || null,
      gate_core_freeze: meta.gate_core_freeze || null,
      month_pillar_standard: meta.month_pillar_standard || null,
      release_label: meta.release_label || null,
      input: entry.input || {},
      summary: defaultSummary(entry),
      data: entry.data,
    };
  }

  /**
   * Persist the result of an Analyze run and append it to history.
   *
   * @param {{input?: object, data: object}} result
   * @returns {boolean} true when the result was stored.
   */
  function save(result) {
    const entry = normalizeResult(result);
    if (!entry) return false;
    const raw = encode(entry);
    if (raw === null) return false;
    const wrote = writeRaw(LAST_KEY, raw, false);
    if (!wrote) return false;
    const declaredId =
      (result && (result.analysis_id || result.id)) ||
      (entry.data && (entry.data.analysis_id || entry.data.request_id || entry.data.case_id)) ||
      "";
    const analysisId = declaredId ? String(declaredId) : makeAnalysisId(entry);
    writeCurrentAnalysisId(analysisId);
    // Drop pre-refactor keys so stale pillars cannot shadow the new result.
    removeRaw([LEGACY_LAST_KEY]);
    // A fresh analyze always wins over whatever entry was being viewed.
    clearView();
    // History is best-effort — must not undo a successful last-result write.
    try {
      saveHistory(entry, analysisId);
    } catch (_) {
      /* ignore */
    }
    return true;
  }

  /**
   * Read the last Analyze result.
   *
   * Prefers current keys. Legacy keys remain a migration bridge only.
   *
   * @returns {{input: object, data: object}|null}
   */
  function load() {
    return readValue([LAST_KEY, LEGACY_LAST_KEY]);
  }

  /** Remove the last Analyze result from every storage backend. */
  function clear() {
    removeRaw([LAST_KEY, LEGACY_LAST_KEY]);
  }

  /** True when a history/report entry was selected for /result. */
  function peekView() {
    return readValue([VIEW_KEY]);
  }

  /**
   * Append an entry to history. Never touches the last Analyze result.
   * Same analysis_id is not prepended again (refresh/export-safe).
   * Existing snapshots are not mutated.
   *
   * @param {object} entry result shape ({input, data}) or a ready history row.
   * @param {string} [forcedId]
   * @returns {boolean} true when the entry was appended or already present.
   */
  function saveHistory(entry, forcedId) {
    let row = null;
    if (entry && typeof entry === "object" && entry.saved_at) {
      row = entry;
    } else {
      const normalized = normalizeResult(entry);
      if (normalized) row = historyRow(normalized, forcedId);
    }
    if (!row) return false;
    if (forcedId && !row.analysis_id) {
      row.analysis_id = String(forcedId);
      row.id = String(forcedId);
    }
    const list = loadHistory();
    const payloadId = String(
      (entry && entry.data && (entry.data.analysis_id || entry.data.request_id || entry.data.case_id)) ||
        (entry && !entry.saved_at && entry.analysis_id) ||
        "",
    ).trim();
    if (payloadId) {
      for (let i = 0; i < list.length; i += 1) {
        if (rowAnalysisId(list[i]) === payloadId) {
          return true;
        }
      }
    }
    list.unshift(row);
    const raw = encode(list.slice(0, HISTORY_LIMIT));
    if (raw === null) return false;
    return writeRaw(HISTORY_KEY, raw, false);
  }

  /**
   * Read the history list.
   *
   * @returns {Array<object>}
   */
  function loadHistory() {
    const list = readValue([HISTORY_KEY, LEGACY_HISTORY_KEY]);
    return Array.isArray(list) ? list : [];
  }

  /** Remove the history list from every storage backend. */
  function clearHistory() {
    removeRaw([HISTORY_KEY, LEGACY_HISTORY_KEY]);
  }

  /**
   * Mark an existing entry (history / report) as the one to show on Result.
   * Written to its own key so the last Analyze result stays intact.
   *
   * @param {{input?: object, data: object}} result
   * @returns {boolean} true when the selection was stored.
   */
  function selectForView(result) {
    const entry = normalizeResult(result);
    if (!entry) return false;
    const raw = encode(entry);
    if (raw === null) return false;
    const wrote = writeRaw(VIEW_KEY, raw, true);
    if (wrote) {
      const viewId = (result && (result.analysis_id || result.id)) || displayAnalysisId(entry);
      writeRaw(VIEW_ID_KEY, encode(String(viewId)), true);
    }
    return wrote;
  }

  /**
   * EXPLICIT LEGACY ONLY (`/result?legacy=1` + result.js).
   * Normal customer /result must use resolveForDisplay, never this path.
   *
   * @returns {{input: object, data: object}|null}
   */
  function loadForView() {
    return readValue([VIEW_KEY]) || load();
  }

  /** Drop the current view selection. */
  function clearView() {
    removeRaw([VIEW_KEY, VIEW_ID_KEY]);
  }

  /**
   * Diagnostic Narrative V2 Presentation envelope. Never overwrites Pack05.
   *
   * @returns {object|null}
   */
  function loadNarrativeV2Shadow() {
    const current = loadCurrent() || load();
    if (!current || !current.data || typeof current.data !== "object") return null;
    const shadow = current.data.narrative_v2_shadow;
    if (!shadow || typeof shadow !== "object") return null;
    return shadow;
  }

  global.BtePortal = global.BtePortal || {};
  global.BtePortal.ResultStore = {
    LAST_KEY: LAST_KEY,
    HISTORY_KEY: HISTORY_KEY,
    VIEW_KEY: VIEW_KEY,
    CURRENT_ID_KEY: CURRENT_ID_KEY,
    HISTORY_LIMIT: HISTORY_LIMIT,
    CALENDAR_RULE_VERSION: CALENDAR_RULE_VERSION,
    save: save,
    load: load,
    loadCurrent: loadCurrent,
    getCurrentAnalysisId: readCurrentAnalysisId,
    resolveForDisplay: resolveForDisplay,
    findHistoryById: findHistoryById,
    clear: clear,
    saveHistory: saveHistory,
    loadHistory: loadHistory,
    clearHistory: clearHistory,
    selectForView: selectForView,
    loadForView: loadForView,
    peekView: peekView,
    clearView: clearView,
    loadNarrativeV2Shadow: loadNarrativeV2Shadow,
  };
})(window);
