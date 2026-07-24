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
      const err = new Error(
        (data && (data.message || data.detail)) || res.statusText || "Request failed"
      );
      err.status = res.status;
      err.payload = data;
      throw err;
    }
    return data;
  }

  function saveLastResult(payload) {
    sessionStorage.setItem(LAST_KEY, JSON.stringify(payload));
    const hist = getHistory();
    hist.unshift({
      id: "local-" + Date.now(),
      saved_at: new Date().toISOString(),
      input: payload.input || {},
      summary:
        (payload.data &&
          payload.data.interpretation &&
          payload.data.interpretation.summary) ||
        "Analyze result",
      data: payload.data,
    });
    sessionStorage.setItem(HISTORY_KEY, JSON.stringify(hist.slice(0, 30)));
  }

  function getLastResult() {
    try {
      return JSON.parse(sessionStorage.getItem(LAST_KEY) || "null");
    } catch (_) {
      return null;
    }
  }

  function getHistory() {
    try {
      return JSON.parse(sessionStorage.getItem(HISTORY_KEY) || "[]");
    } catch (_) {
      return [];
    }
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
