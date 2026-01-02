(() => {
  const isLocal =
    location.hostname === "localhost" || location.hostname === "127.0.0.1";

  // AJUSTE se seu backend local roda em outra porta (ex: http://localhost:8000)
  const LOCAL_API_BASE = "http://localhost";

  // AJUSTE quando seu backend estiver online (Render/Railway/VPS)
  const PROD_API_BASE = "https://SEU_BACKEND_AQUI";

  // Se seu backend autentica por cookie HttpOnly, coloque true.
  // Se autentica por Bearer token (recomendado com Pages), coloque false.
  const USE_COOKIES = false;

  window.GALILEU = window.GALILEU || {};
  window.GALILEU.API_BASE = isLocal ? LOCAL_API_BASE : PROD_API_BASE;
  window.GALILEU.USE_COOKIES = USE_COOKIES;
})();
