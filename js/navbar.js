document.addEventListener("DOMContentLoaded", () => {
  (async () => {
    const btn =
      document.getElementById("btn-login-nav") ||
      document.querySelector(".auth-buttons a.btn") ||
      document.querySelector("a.btn-laranja");

    if (!btn) return;
    if (!window.GalileuAuth || !window.GalileuAuth.me) return;

    const setText = (text) => {
      const span = btn.querySelector("span");
      if (span) span.textContent = text;
      else btn.textContent = text;
    };

    try {
      await window.GalileuAuth.me(); // ✅ checa login pelo backend (cookie)
      setText("MINHA EQUIPE");
      btn.href = "minha-equipe.html";
    } catch (e) {
      setText("LOGIN / CADASTRE-SE");
      btn.href = "cadastrar.html";
    }
  })();
});
