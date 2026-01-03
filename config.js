(() => {
  const isLocal =
    location.hostname === "localhost" || location.hostname === "127.0.0.1";

  const LOCAL_API_BASE = "http://localhost";
  const PROD_API_BASE = "https://revelation-deutschland-clearance-label.trycloudflare.com";

  const USE_COOKIES = true;

  window.GALILEU = window.GALILEU || {};
  window.GALILEU.API_BASE = isLocal ? LOCAL_API_BASE : PROD_API_BASE;
  window.GALILEU.USE_COOKIES = USE_COOKIES;
})();
