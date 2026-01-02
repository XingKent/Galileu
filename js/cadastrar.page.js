(() => {
  function ensureMsgBox() {
    let box = document.getElementById("auth-msg");
    if (!box) {
      box = document.createElement("div");
      box.id = "auth-msg";
      box.style.margin = "12px 0";
      box.style.padding = "10px 12px";
      box.style.borderRadius = "10px";
      box.style.display = "none";
      box.style.fontFamily = "Poppins, Arial, sans-serif";
      box.style.fontSize = "14px";
      const anchor = document.querySelector("main") || document.body;
      anchor.prepend(box);
    }
    return box;
  }

  function showMsg(text, type = "info") {
    const box = ensureMsgBox();
    box.textContent = text;
    box.style.display = "block";

    if (type === "success") {
      box.style.background = "#e7f8ee";
      box.style.border = "1px solid #b8efd0";
      box.style.color = "#0f5132";
    } else if (type === "error") {
      box.style.background = "#fdecec";
      box.style.border = "1px solid #f5c2c7";
      box.style.color = "#842029";
    } else {
      box.style.background = "#eef3ff";
      box.style.border = "1px solid #cfe0ff";
      box.style.color = "#1f2a44";
    }
  }

  function wire() {
    const loginForm = document.getElementById("login-form");
    const cadastroForm = document.getElementById("cadastro-form");

    if (loginForm) {
      loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        try {
          showMsg("Entrando...", "info");
          await window.GalileuAuth.loginFromForm();
          showMsg("Login OK! Indo pro dashboard...", "success");
          window.location.href = "dashboard.html";
        } catch (err) {
          showMsg(err.message || "Falha no login.", "error");
        }
      });
    }

    if (cadastroForm) {
      cadastroForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        try {
          showMsg("Criando conta...", "info");
          await window.GalileuAuth.registerFromForm();
          showMsg("Conta criada! Indo pro dashboard...", "success");
          window.location.href = "dashboard.html";
        } catch (err) {
          showMsg(err.message || "Falha no cadastro.", "error");
        }
      });
    }
  }

  document.addEventListener("DOMContentLoaded", wire);
})();
