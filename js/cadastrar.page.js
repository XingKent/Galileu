(function () {
  function el(id) { return document.getElementById(id); }

  function showMsg(msg) {
    const box = el("auth-alert");
    if (!box) { alert(msg); return; }
    box.textContent = msg;
    box.classList.add("show");
  }

  function clearMsg() {
    const box = el("auth-alert");
    if (!box) return;
    box.textContent = "";
    box.classList.remove("show");
  }

  function disable(btn, state) {
    if (!btn) return;
    btn.disabled = state;
    btn.style.opacity = state ? "0.7" : "1";
    btn.style.cursor = state ? "not-allowed" : "pointer";
  }

  function ensureApiBase() {
    const base = (window.GALILEU?.API_BASE || "").trim();
    if (!base) {
      throw new Error(
        "API_BASE não definido. Abra a página com ?api=https://SEU_TUNEL.trycloudflare.com (uma vez) para salvar."
      );
    }
  }

  async function alreadyLoggedRedirect() {
    try {
      ensureApiBase();
      await window.GalileuAuth.me();
      window.location.href = "minha-equipe.html";
    } catch (_) {
      // não logado, continua
    }
  }

  async function onLoginSubmit(e) {
    e.preventDefault();
    clearMsg();

    const email = (el("login-email")?.value || "").trim();
    const senha = (el("login-senha")?.value || "");

    const btn = el("login-btn");
    disable(btn, true);

    try {
      ensureApiBase();
      showMsg("Entrando...");

      await window.GalileuAuth.login(email, senha);

      // garante que cookie veio e sessão está válida
      await window.GalileuAuth.me();

      showMsg("Login OK! Indo para Minha Equipe...");
      window.location.href = "minha-equipe.html";
    } catch (err) {
      showMsg("Erro no login: " + (err?.message || "Erro desconhecido"));
    } finally {
      disable(btn, false);
    }
  }

  async function onRegisterSubmit(e) {
    e.preventDefault();
    clearMsg();

    const payload = {
      email: (el("cadastro-email")?.value || "").trim(),
      nome: (el("cadastro-nome")?.value || "").trim(),
      nascimento: el("cadastro-nascimento")?.value || "",
      cpf: (el("cadastro-cpf")?.value || "").trim(),
      telefone: (el("cadastro-telefone")?.value || "").trim(),
      senha: el("cadastro-senha")?.value || "",
      confirmar: el("cadastro-confirmar")?.value || "",
    };

    const btn = el("cadastro-btn");
    disable(btn, true);

    try {
      ensureApiBase();
      showMsg("Criando conta...");

      await window.GalileuAuth.register(payload);

      // depois do register, já deve estar logado (cookie)
      await window.GalileuAuth.me();

      showMsg("Cadastro OK! Indo para Minha Equipe...");
      window.location.href = "minha-equipe.html";
    } catch (err) {
      showMsg("Erro no cadastro: " + (err?.message || "Erro desconhecido"));
    } finally {
      disable(btn, false);
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    const loginForm = el("login-form");
    const cadastroForm = el("cadastro-form");

    if (loginForm) loginForm.addEventListener("submit", onLoginSubmit);
    if (cadastroForm) cadastroForm.addEventListener("submit", onRegisterSubmit);

    // se já estiver logado, joga pra Minha Equipe
    alreadyLoggedRedirect();
  });
})();
