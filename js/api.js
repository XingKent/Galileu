(() => {
  const TOKEN_KEY = "galileu_access_token";

  function apiBase() {
    const base = window.GALILEU && window.GALILEU.API_BASE;
    if (!base) throw new Error("API_BASE não configurado. Verifique o config.js");
    return base;
  }

  function useCookies() {
    return !!(window.GALILEU && window.GALILEU.USE_COOKIES);
  }

  function buildUrl(path) {
    if (/^https?:\/\//i.test(path)) return path;
    return `${apiBase()}${path}`;
  }

  function getToken() {
    return localStorage.getItem(TOKEN_KEY);
  }

  function setToken(token) {
    localStorage.setItem(TOKEN_KEY, token);
  }

  function clearToken() {
    localStorage.removeItem(TOKEN_KEY);
  }

  async function request(path, { method = "GET", body = null, headers = {} } = {}) {
    const url = buildUrl(path);

    const h = new Headers(headers);
    if (!h.has("Content-Type")) h.set("Content-Type", "application/json");

    const token = getToken();
    if (token) h.set("Authorization", `Bearer ${token}`);

    const opts = {
      method,
      headers: h,
      mode: "cors",
    };

    if (useCookies()) {
      opts.credentials = "include";
    }

    if (body !== null && body !== undefined) {
      opts.body = typeof body === "string" ? body : JSON.stringify(body);
    }

    const res = await fetch(url, opts);

    const text = await res.text();
    let data = null;
    try {
      data = text ? JSON.parse(text) : null;
    } catch {
      data = text || null;
    }

    if (!res.ok) {
      const msg =
        (data && typeof data === "object" && (data.detail || data.message)) ||
        (typeof data === "string" && data) ||
        `Erro HTTP ${res.status}`;
      throw new Error(msg);
    }

    return data;
  }

  window.GalileuAPI = {
    request,
    getToken,
    setToken,
    clearToken,
  };
})();
