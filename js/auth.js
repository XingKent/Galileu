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

    // Faz o cadastro
    const response = await window.GalileuAPI.request(API.register, {
      method: "POST",
      body: payload,
    });

    // Opcional: Se cadastrou com sucesso, já manda pro login ou loga direto
    alert("Cadastro realizado com sucesso! Faça login.");
    window.location.href = "cadastrar.html"; // Recarrega para limpar ou vai pra login
    return response;
  }

  async function loginFromForm() {
    const payload = {
      email: q("login-email")?.value.trim(),
      senha: q("login-senha")?.value,
    };

    try {
      // 1. Tenta fazer o login no backend
      const data = await window.GalileuAPI.request(API.login, {
        method: "POST",
        body: payload,
      });

      // 2. SUCESSO! Salva a "bandeira" de logado no navegador
      localStorage.setItem('usuario_logado', 'true');

      // Se o backend devolver o nome do usuário no JSON, salva também pra usar na tela
      if (data && data.nome) {
        localStorage.setItem('user_name', data.nome);
      }

      // 3. Redireciona para a página da equipe (Dashboard)
      window.location.href = "/minha-equipe.html";
      
      return data;
    } catch (error) {
      // Se der erro (400/401), o request joga o erro pra cá
      console.error("Erro ao logar:", error);
      throw error; // Repassa o erro para o UI mostrar o alert
    }
  }

  async function me() {
    return window.GalileuAPI.request(API.me, { method: "GET" });
  }

  async function logout() {
    try {
      // Tenta avisar o backend
      await window.GalileuAPI.request(API.logout, { method: "POST" });
    } catch (e) {
      console.warn("Backend logout falhou, mas limpando localmente...");
    } finally {
      // Limpa os dados do navegador SEMPRE (mesmo se o backend der erro)
      localStorage.removeItem('usuario_logado');
      localStorage.removeItem('user_name');
      
      // Manda de volta pra Home ou Login
      window.location.href = "/index.html"; 
    }
  }

  // Função nova: Verifica rápido se está logado (para usar na Navbar)
  function isLoggedIn() {
    return localStorage.getItem('usuario_logado') === 'true';
  }

  async function requireAuth(redirect = "cadastrar.html") {
    // Primeiro checa rápido o localStorage (mais rápido pra UI)
    if (!isLoggedIn()) {
        window.location.href = redirect;
        return null;
    }

    // Depois confirma com o backend se a sessão ainda é válida
    try {
      return await me();
    } catch {
      // Se o backend disser que o cookie expirou, desloga
      logout(); 
      return null;
    }
  }

  window.GalileuAuth = {
    registerFromForm,
    loginFromForm,
    me,
    logout,
    requireAuth,
    isLoggedIn // Exportei essa pra você usar no navbar.js
  };
})();