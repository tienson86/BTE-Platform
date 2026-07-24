/**
 * BTE Web Admin — REST client (calls /backend proxy only).
 * No business logic; stores JWT in sessionStorage.
 */
(function (global) {
  const TOKEN_KEY = "bte_admin_token";
  const USER_KEY = "bte_admin_user";

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

  async function api(method, path, body, opts) {
    const headers = Object.assign(
      { Accept: "application/json" },
      (opts && opts.headers) || {}
    );
    const token = getToken();
    if (token) headers.Authorization = "Bearer " + token;
    if (body !== undefined && !(body instanceof FormData)) {
      headers["Content-Type"] = "application/json";
    }
    const res = await fetch("/backend" + path, {
      method,
      headers,
      body:
        body === undefined
          ? undefined
          : body instanceof FormData
            ? body
            : JSON.stringify(body),
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

  function qs(params) {
    const u = new URLSearchParams();
    Object.entries(params || {}).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== "") u.set(k, v);
    });
    const s = u.toString();
    return s ? "?" + s : "";
  }

  function showFlash(el, message, type) {
    if (!el) return;
    el.textContent = message;
    el.className = "flash show " + (type || "");
  }

  function fmt(v) {
    if (v === null || v === undefined || v === "") return "—";
    if (typeof v === "object") return JSON.stringify(v);
    return String(v);
  }

  global.BteAdmin = {
    getToken,
    setSession,
    clearSession,
    getUser,
    api,
    qs,
    showFlash,
    fmt,
    get: (path) => api("GET", path),
    post: (path, body) => api("POST", path, body),
    put: (path, body) => api("PUT", path, body),
    del: (path) => api("DELETE", path),
  };
})(window);
