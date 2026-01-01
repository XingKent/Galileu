// Galileu/js/auth.js

const API = {
  register: "/api/auth/register/",
  login: "/api/auth/login/",
  me: "/api/auth/me/",
  logout: "/api/auth/logout/"
};

async function apiRequest(url, method, bodyObj) {
  const res = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    credentials: "include", // <- ESSENCIAL: manda/recebe cookies HttpOnly
    body: bodyObj ? JSON.stringify(bodyObj) : undefined
  });

  let data = null;
  try { data = await res.json(); } catch (_) {}

  if (!res.ok) {
    const msg = (data && (data.detail || data.message)) || `Erro HTTP ${res.status}`;
    throw new Error(msg);
  }

  return data;
}

function q(id) { return document.getElementById(id); }

async function handleRegisterSubmit(e) {
  e.preventDefault();

  const payload = {
    email: q("cadastro-email").value.trim(),
    nome: q("cadastro-nome").value.trim(),
    nascimento: q("cadastro-nascimento").value,
    cpf: q("cadastro-cpf").value.trim(),
    telefone: q("cadastro-telefone").value.trim(),
    senha: q("cadastro-senha").value,
    confirmar: q("cadastro-confirmar").value
  };

  await apiRequest(API.register, "POST", payload);

  // Se registrou, já vem cookie. Redireciona ou só avisa.
  alert("Conta criada e login efetuado.");
  window.location.href = "index.html";
}

async function handleLoginSubmit(e) {
  e.preventDefault();

  const payload = {
    email: q("login-email").value.trim(),
    senha: q("login-senha").value
  };

  await apiRequest(API.login, "POST", payload);

  alert("Login efetuado.");
  window.location.href = "index.html";
}

function wireCadastroPage() {
  const loginForm = q("login-form");
  const cadastroForm = q("cadastro-form");

  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      try { await handleLoginSubmit(e); }
      catch (err) { alert(err.message); }
    });
  }

  if (cadastroForm) {
    cadastroForm.addEventListener("submit", async (e) => {
      try { await handleRegisterSubmit(e); }
      catch (err) { alert(err.message); }
    });
  }
}

// auto-wire só na página que tem esses forms
document.addEventListener("DOMContentLoaded", wireCadastroPage);

// expõe helpers pra outras páginas (logout/protected)
window.GalileuAuth = {
  me: () => apiRequest(API.me, "GET"),
  logout: () => apiRequest(API.logout, "POST")
};
