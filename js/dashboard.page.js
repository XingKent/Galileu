(() => {
  async function start() {
    const user = await window.GalileuGuards.protectPage({ redirect: "cadastrar.html" });
    if (!user) return;

    const box = document.getElementById("user-box");

    const email = user.email || user.user?.email || "—";
    const nome = user.nome || user.name || user.user?.nome || user.user?.name || "—";
    const role = user.role || user.tipo || user.user?.role || user.user?.tipo || "—";

    box.textContent = `Logado como: ${nome} | ${email} | role: ${role}`;

    document.getElementById("btn-logout").addEventListener("click", async () => {
      await window.GalileuAuth.logout();
      window.location.href = "cadastrar.html";
    });
  }

  document.addEventListener("DOMContentLoaded", start);
})();
