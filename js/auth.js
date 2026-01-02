(() => {
  const API = {
    register: "/api/auth/register/",
    login: "/api/auth/login/",
    me: "/api/auth/me/",
    logout: "/api/auth/logout/",
  };

  function extractToken(payload) {
    if (!payload) return null;
    if (payload.access) return payload.access;
    if (payload.token) return payload.token;
    if (payload.access_token) return payload.access_token;
    if (payload.data && payload.data.access) return payload.data.access;
    if (payload.data && payload.data.token) return payload.data.token;
    return null;
  }

  function q(id) {
    return document.getElementById(id);
  }

  async function registerFromForm() {
    const payload = {
      email: q("cadastro-email")?.value.trim(),
      nome: q("cadastro-nome")?.value.trim(),
      nascimento: q("cadastro-nascimento")?.value,
      cpf: q("cadastro-cpf")?.value.trim(),
      rg: q("cadastro-rg")?.value.trim(),
      telefone: q("cadastro-telefone")?.value.trim(),
      senha: q("cadastro-senha")?.value,
      password: q("cadastro-senha")?.value,
      confirmar: q("cadastro-confirmar")?.value,
    };

    if (payload.senha !== payload.confirmar) {
      throw new Error("As senhas não conferem.");
    }

    const data = await window.GalileuAPI.request(API.register, {
      method: "POST",
      body: payload,
    });

    const token = extractToken(data);
    if (token) window.GalileuAPI.setToken(token);

    return data;
  }

  async function loginFromForm() {
    const payload = {
      email: q("login-email")?.value.trim(),
      senha: q("login-senha")?.value,
      password: q("login-senha")?.value,
      username: q("login-email")?.value.trim(),
    };

    const data = await window.GalileuAPI.request(API.login, {
      method: "POST",
      body: payload,
    });

    const token = extractToken(data);
    if (token) window.GalileuAPI.setToken(token);

    return data;
  }

  async function me() {
    return window.GalileuAPI.request(API.me, { method: "GET" });
  }

  async function logout() {
    try {
      await window.GalileuAPI.request(API.logout, { method: "POST" });
    } finally {
      window.GalileuAPI.clearToken();
    }
  }

  async function requireAuth(redirect = "cadastrar.html") {
    const token = window.GalileuAPI.getToken();
    const usingCookies = !!(window.GALILEU && window.GALILEU.USE_COOKIES);

    if (!token && !usingCookies) {
      window.location.href = redirect;
      return null;
    }

    try {
      return await me();
    } catch {
      window.GalileuAPI.clearToken();
      window.location.href = redirect;
      return null;
    }
  }

  window.GalileuAuth = {
    registerFromForm,
    loginFromForm,
    me,
    logout,
    requireAuth,
  };
})();
