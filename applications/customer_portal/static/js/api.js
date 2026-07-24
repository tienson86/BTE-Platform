(function (global) {
  const TOKEN_KEY = "bte_portal_token";
  const USER_KEY = "bte_portal_user";
  const LAST_KEY = "bte_portal_last_result";
  const HISTORY_KEY = "bte_portal_history";

  function getToken() {
    return sessionStorage.getItem(TOKEN_KEY) || "";
  }
  function setSession(token, user) {
    if (token) sessionStorage.setItem(TOKEN_KEY, token);
    if (user) sessionStorage.setItem(USER_KEY, JSON.stringify(user));
  }
  function clearSession() {
    sessionStorage.removeItem(TOKEN_KEY);
    sessionStorage.removeItem(USER_KEY);
  }
  function getUser() {
    try {
      return JSON.parse(sessionStorage.getItem(USER_KEY) || "null");
    } catch (_) {
      return null;
    }
  }

  async function api(method, path, body) {
    const headers = { Accept: "application/json" };
    const token = getToken();
    if (token) headers.Authorization = "Bearer " + token;
    if (body !== undefined) headers["Content-Type"] = "application/json";
    // Portal proxies Applications API under /backend/*
    const res = await fetch("/backend" + path, {
      method,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
    });
    const text = await res.text();
    let data = null;
    try {
      data = text ? JSON.parse(text) : null;
    } catch (_) {
      data = { raw: text };
    }
    if (!res.ok) {
      let detail =
        (data && (data.message || data.detail)) ||
        res.statusText ||
        (window.BteI18n ? BteI18n.t("common.request_failed") : "Request failed");
      if (typeof detail === "object") {
        try {
          detail = JSON.stringify(detail);
        } catch (_) {
          detail = String(detail);
        }
      }
      const err = new Error(detail);
      err.status = res.status;
      err.payload = data;
      throw err;
    }
    return data;
  }

  function persist(key, value) {
    const raw = JSON.stringify(value);
    sessionStorage.setItem(key, raw);
    try {
      localStorage.setItem(key, raw);
    } catch (_) {
      /* private mode / quota — sessionStorage is enough for same-tab Result */
    }
  }

  function readPersist(key) {
    try {
      const raw = sessionStorage.getItem(key) || localStorage.getItem(key);
      return raw ? JSON.parse(raw) : null;
    } catch (_) {
      return null;
    }
  }

  function saveLastResult(payload) {
    persist(LAST_KEY, payload);
    const hist = getHistory();
    const interp = payload.data && payload.data.interpretation;
    hist.unshift({
      id: "local-" + Date.now(),
      saved_at: new Date().toISOString(),
      input: payload.input || {},
      summary:
        (interp && (interp.summary || interp.interpretation_summary)) ||
        (window.BteI18n ? BteI18n.t("api.analyze_result") : "Analyze result"),
      data: payload.data,
    });
    persist(HISTORY_KEY, hist.slice(0, 30));
  }

  function getLastResult() {
    return readPersist(LAST_KEY);
  }

  function getHistory() {
    const hist = readPersist(HISTORY_KEY);
    return Array.isArray(hist) ? hist : [];
  }

  function showFlash(el, message, type) {
    if (!el) return;
    el.textContent = message;
    el.className = "flash show " + (type || "");
  }

  function fmt(v) {
    if (v === null || v === undefined || v === "") return "—";
    if (typeof v === "object") return JSON.stringify(v, null, 2);
    return String(v);
  }

  global.BtePortal = {
    getToken,
    setSession,
    clearSession,
    getUser,
    api,
    get: (p) => api("GET", p),
    post: (p, b) => api("POST", p, b),
    saveLastResult,
    getLastResult,
    getHistory,
    showFlash,
    fmt,
  };
})(window);
