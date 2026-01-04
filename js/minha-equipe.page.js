function q(id) { return document.getElementById(id); }

document.addEventListener("DOMContentLoaded", async () => {
  if (!window.GalileuAuth || !window.GalileuAuth.me) {
    window.location.href = "cadastrar.html";
    return;
  }

  let me;
  try {
    me = await window.GalileuAuth.me();
  } catch (e) {
    window.location.href = "cadastrar.html";
    return;
  }

  q("me-email").textContent = me.email || "-";
  q("me-nome").textContent = me.nome || "-";
  q("me-nascimento").textContent = me.nascimento || "-";
  q("me-cpf").textContent = me.cpf || "-";

  const btnSair = q("btn-sair");
  if (btnSair) {
    btnSair.addEventListener("click", async () => {
      try { await window.GalileuAuth.logout(); } catch (_) {}
      window.location.href = "cadastrar.html";
    });
  }
});
