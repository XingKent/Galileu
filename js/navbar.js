document.addEventListener("DOMContentLoaded", () => {
    // Verifica se a função de auth existe e se o usuário está logado
    // Usa a função isLoggedIn que criamos no auth.js
    const isLogged = window.GalileuAuth && window.GalileuAuth.isLoggedIn();

    if (isLogged) {
        // Busca o botão de Login/Cadastro na Navbar
        // DICA: Adicione o ID="btn-login-nav" no seu HTML para facilitar
        const btnLogin = document.getElementById("btn-login-nav") || document.querySelector(".btn-laranja");

        if (btnLogin) {
            // Muda o texto e o link
            btnLogin.innerText = "Minha Equipe";
            btnLogin.href = "/minha-equipe.html";
            
            // Opcional: Muda a cor ou estilo se quiser
            // btnLogin.classList.add("btn-equipe");
        }
    }
});