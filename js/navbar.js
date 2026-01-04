// Galileu/js/navbar.js
document.addEventListener("DOMContentLoaded", async () => {
  const btn = document.getElementById("btn-login-nav") || document.querySelector(".auth-buttons a.btn");

  if (!btn || !window.GalileuAuth) return;

  try {
    // se tiver sessão, vai dar 200 e trocar o botão
    await window.GalileuAuth.me();

    btn.innerHTML = `<span>MINHA EQUIPE</span>`;
    btn.href = "minha-equipe.html";
  } catch (e) {
    // não logado (401) -> deixa como está (LOGIN/CADASTRE-SE)
    // NÃO faz console.error aqui pra não poluir
  }
});
