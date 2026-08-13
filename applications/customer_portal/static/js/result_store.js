/**
 * BTE Portal — Result Storage Service.
 *
 * Single owner of analyze-result persistence. Pages must never call
 * sessionStorage / localStorage for results directly.
 *
 * Keys are separated so that browsing never corrupts the analyze result:
 *   bte_last_result  — the result produced by the last Analyze run.
 *   bte_history      — append-only list of past runs.
 *   bte_view_result  — transient pointer used when opening an older entry.
 */
(function (global) {
  const LAST_KEY = "bte_last_result";
  const HISTORY_KEY = "bte_history";
  const VIEW_KEY = "bte_view_result";
  const CURRENT_ID_KEY = "bte_current_analysis_id";
  const VIEW_ID_KEY = "bte_view_analysis_id";
  // Pre-refactor keys — read-only, so existing browser sessions keep their data.
  const LEGACY_LAST_KEY = "bte_portal_last_result";
  const LEGACY_HISTORY_KEY = "bte_portal_history";
  const HISTORY_LIMIT = 30;

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
    return { input: result.input || {}, data: result.data };
  }

  function makeAnalysisId(entry) {
    const fromEntry = entry && (entry.analysis_id || entry.id);
    if (fromEntry) return String(fromEntry);
    const data = entry && entry.data;
    if (data && (data.analysis_id || data.request_id || data.case_id)) {
      return String(data.analysis_id || data.request_id || data.case_id);
    }
    const input = (entry && entry.input) || {};
    return ["bte", input.year || 0, input.month || 0, input.day || 0, input.hour || 0, input.minute || 0, Date.now()].join("-");
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
  function loadCurrent() {
    const entry = load();
    if (!entry) return null;
    return {
      input: entry.input || {},
      data: entry.data,
      analysis_id: readCurrentAnalysisId() || displayAnalysisId(entry),
      source: "current",
    };
  }

  /**
   * Customer display payload.
   *
   * Default: fresh current analysis.
   * fromHistory: explicit History / older report selection only.
   */
  function resolveForDisplay(fromHistory) {
    if (fromHistory) {
      const view = peekView();
      if (view && view.data) {
        return {
          input: view.input || {},
          data: view.data,
          analysis_id: readValue([VIEW_ID_KEY]) || view.analysis_id || view.id || displayAnalysisId(view),
          source: "history",
        };
      }
    }
    const current = loadCurrent();
    if (current) return current;
    const legacy = load();
    if (legacy && legacy.data) {
      return {
        input: legacy.input || {},
        data: legacy.data,
        analysis_id: readCurrentAnalysisId() || displayAnalysisId(legacy),
        source: "legacy",
      };
    }
    return null;
  }

  function defaultSummary(entry) {
    const interp = entry.data && entry.data.interpretation;
    const summary = interp && (interp.summary || interp.interpretation_summary);
    if (summary) return summary;
    return global.BteI18n ? global.BteI18n.t("api.analyze_result") : "Analyze result";
  }

  function historyRow(entry) {
    const analysisId = readCurrentAnalysisId() || makeAnalysisId(entry);
    return {
      id: analysisId,
      analysis_id: analysisId,
      saved_at: new Date().toISOString(),
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
    writeCurrentAnalysisId(makeAnalysisId(result) || makeAnalysisId(entry));
    // Drop pre-refactor keys so stale pillars cannot shadow the new result.
    removeRaw([LEGACY_LAST_KEY]);
    // A fresh analyze always wins over whatever entry was being viewed.
    clearView();
    // History is best-effort — must not undo a successful last-result write.
    try {
      saveHistory(entry);
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
   *
   * @param {object} entry result shape ({input, data}) or a ready history row.
   * @returns {boolean} true when the entry was appended.
   */
  function saveHistory(entry) {
    let row = null;
    if (entry && typeof entry === "object" && entry.saved_at) {
      row = entry;
    } else {
      const normalized = normalizeResult(entry);
      if (normalized) row = historyRow(normalized);
    }
    if (!row) return false;
    const list = loadHistory();
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
   * Read what the Result page should render: the selected entry when the user
   * opened an older one, otherwise the last Analyze result.
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

  global.BtePortal = global.BtePortal || {};
  global.BtePortal.ResultStore = {
    LAST_KEY: LAST_KEY,
    HISTORY_KEY: HISTORY_KEY,
    VIEW_KEY: VIEW_KEY,
    CURRENT_ID_KEY: CURRENT_ID_KEY,
    save: save,
    load: load,
    loadCurrent: loadCurrent,
    getCurrentAnalysisId: readCurrentAnalysisId,
    resolveForDisplay: resolveForDisplay,
    clear: clear,
    saveHistory: saveHistory,
    loadHistory: loadHistory,
    clearHistory: clearHistory,
    selectForView: selectForView,
    loadForView: loadForView,
    peekView: peekView,
    clearView: clearView,
  };
})(window);
