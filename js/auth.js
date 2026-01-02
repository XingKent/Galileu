(() => {
  const API = {
    register: "/api/auth/register/",
    login: "/api/auth/login/",
    me: "/api/auth/me/",
    logout: "/api/auth/logout/",
  };

  function q(id) {
    return document.getElementById(id);
  }

  async function registerFromForm() {
    const senha = q("cadastro-senha")?.value;
    const confirmar = q("cadastro-confirmar")?.value;

    if (senha !== confirmar) throw new Error("As senhas não conferem.");

    const payload = {
      email: q("cadastro-email")?.value.trim(),
      nome: q("cadastro-nome")?.value.trim(),
      nascimento: q("cadastro-nascimento")?.value,
      cpf: q("cadastro-cpf")?.value.trim(),
      rg: q("cadastro-rg")?.value.trim(),
      telefone: q("cadastro-telefone")?.value.trim(),
      senha,
      confirmar,
    };

    return window.GalileuAPI.request(API.register, {
      method: "POST",
      body: payload,
    });
  }

  async function loginFromForm() {
    const payload = {
      email: q("login-email")?.value.trim(),
      senha: q("login-senha")?.value, // ✅ seu backend exige "senha"
    };

    return window.GalileuAPI.request(API.login, {
      method: "POST",
      body: payload,
    });
  }

  async function me() {
    return window.GalileuAPI.request(API.me, { method: "GET" });
  }

  async function logout() {
    // mesmo que o backend não limpe, você redireciona e pronto
    return window.GalileuAPI.request(API.logout, { method: "POST" });
  }

  async function requireAuth(redirect = "cadastrar.html") {
    try {
      return await me();
    } catch {
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
