async function postJSON(url, data) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include", // importante: manda/recebe cookies
    body: JSON.stringify(data),
  });

  const payload = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg = payload?.detail || payload?.non_field_errors?.[0] || "Erro";
    throw new Error(msg);
  }
  return payload;
}

// LOGIN
document.getElementById("login-form")?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("login-email").value;
  const senha = document.getElementById("login-senha").value;

  try {
    await postJSON("/api/auth/login/", { email, senha });
    window.location.href = "index.html";
  } catch (err) {
    alert(err.message);
  }
});

// CADASTRO
document.getElementById("cadastro-form")?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("cadastro-email").value;
  const nome = document.getElementById("cadastro-nome").value;
  const nascimento = document.getElementById("cadastro-nascimento").value || null;
  const cpf = document.getElementById("cadastro-cpf").value;
  const telefone = document.getElementById("cadastro-telefone").value;
  const senha = document.getElementById("cadastro-senha").value;
  const confirmar = document.getElementById("cadastro-confirmar").value;

  try {
    await postJSON("/api/auth/register/", { email, nome, nascimento, cpf, telefone, senha, confirmar });
    window.location.href = "index.html";
  } catch (err) {
    alert(err.message);
  }
});
