(() => {
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

  async function request(path, { method = "GET", body = null, headers = {} } = {}) {
    const url = buildUrl(path);

    const h = new Headers(headers);
    if (!h.has("Content-Type")) h.set("Content-Type", "application/json");

    const opts = { method, headers: h, mode: "cors" };

    // ✅ essencial pra cookie/session
    if (useCookies()) opts.credentials = "include";

    if (body !== null && body !== undefined) {
      opts.body = typeof body === "string" ? body : JSON.stringify(body);
    }

    let res;
    try {
      res = await fetch(url, opts);
    } catch {
      throw new Error(`Falha de rede chamando API: ${url}. PROD_API_BASE está correto? A API está online (HTTPS)?`);
    }

    const text = await res.text();
    let data = null;
    try { data = text ? JSON.parse(text) : null; } catch { data = text || null; }

    if (!res.ok) {
      const msg =
        (data && typeof data === "object" && (data.detail || data.message)) ||
        (typeof data === "string" && data) ||
        `Erro HTTP ${res.status}`;
      throw new Error(`${msg} (URL: ${url})`);
    }

    return data;
  }

  window.GalileuAPI = { request };
})();
