// Galileu/js/auth.js

(function () {
  function getApiBase() {
    const base = (window.GALILEU && window.GALILEU.API_BASE) ? String(window.GALILEU.API_BASE).trim() : "";
    if (!base) return "";
    return base.replace(/\/+$/, ""); // remove barra final
  }

  function buildUrl(path) {
    const base = getApiBase();
    if (!base) return path; // fallback (dev)
    return base + path;
  }

  async function request(path, method = "GET", bodyObj) {
    const url = buildUrl(path);

    const opts = {
      method,
      headers: { "Content-Type": "application/json" },
      credentials: "include", // ESSENCIAL p/ cookie HttpOnly
    };

    if (bodyObj !== undefined) {
      opts.body = JSON.stringify(bodyObj);
    }

    const res = await fetch(url, opts);

    let data = null;
    try { data = await res.json(); } catch (_) {}

    if (!res.ok) {
      // tenta pegar erro amigável
      let msg = `Erro HTTP ${res.status}`;

      if (data) {
        if (typeof data.detail === "string") msg = data.detail;
        else if (typeof data.message === "string") msg = data.message;
        else if (typeof data.error === "string") msg = data.error;
        else if (typeof data === "object") {
          // erros de serializer: {campo:["msg"]}
          const firstKey = Object.keys(data)[0];
          if (firstKey) {
            const val = data[firstKey];
            if (Array.isArray(val) && val.length) msg = `${firstKey}: ${val[0]}`;
            else if (typeof val === "string") msg = `${firstKey}: ${val}`;
          }
        }
      }

      const err = new Error(msg);
      err.status = res.status;
      err.data = data;
      throw err;
    }

    return data;
  }

  // -------------------------
  // Funções públicas
  // -------------------------
  async function register(payload) {
    return request("/api/auth/register/", "POST", payload);
  }

  async function login(email, senha) {
    return request("/api/auth/login/", "POST", { email, senha });
  }

  async function me() {
    return request("/api/auth/me/", "GET");
  }

  async function logout() {
    return request("/api/auth/logout/", "POST", {});
  }

  function isLoggedIn() {
    // checagem leve (não garante sessão)
    // a garantia MESMO é chamar me()
    return !!localStorage.getItem("GALILEU_LAST_LOGIN_OK");
  }

  // Marca login OK após me() funcionar uma vez
  async function ensureSessionAndMark() {
    const user = await me();
    localStorage.setItem("GALILEU_LAST_LOGIN_OK", "1");
    return user;
  }

  // expõe no window
  window.GalileuAuth = {
    request,
    register,
    login,
    me: ensureSessionAndMark,
    logout: async () => {
      try { await logout(); } finally {
        localStorage.removeItem("GALILEU_LAST_LOGIN_OK");
      }
    },
    isLoggedIn,
  };
})();
