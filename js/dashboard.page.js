(() => {
  async function start() {
    const user = await window.GalileuAuth.requireAuth("cadastrar.html");
    if (!user) return;

    const box = document.getElementById("user-box");
    box.textContent = `Logado como: ${user.nome} | ${user.email}`;

    document.getElementById("btn-logout").addEventListener("click", async () => {
      await window.GalileuAuth.logout();
      window.location.href = "cadastrar.html";
    });
  }

  document.addEventListener("DOMContentLoaded", start);
})();
