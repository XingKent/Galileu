(() => {
  const isLocal =
    location.hostname === "localhost" || location.hostname === "127.0.0.1";

  // Backend local via nginx na porta 80 (seu caso)
  const LOCAL_API_BASE = "http://localhost";

  // Quando subir o backend online, coloque aqui:
  const PROD_API_BASE = "https://SEU_BACKEND_AQUI";

  // ✅ VOCÊ ESTÁ EM COOKIE/SESSION
  const USE_COOKIES = true;

  window.GALILEU = window.GALILEU || {};
  window.GALILEU.API_BASE = isLocal ? LOCAL_API_BASE : PROD_API_BASE;
  window.GALILEU.USE_COOKIES = USE_COOKIES;
})();
