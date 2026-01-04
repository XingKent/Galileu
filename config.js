(() => {
  const isLocal =
    location.hostname === "localhost" || location.hostname === "127.0.0.1";

  const LOCAL_API_BASE = "http://localhost";
  const DEFAULT_PROD_API_BASE = "https://billy-polyester-silicon-fall.trycloudflare.com";

  const params = new URLSearchParams(location.search);
  const qsApi = params.get("api");

  function isValidHttpsUrl(u) {
    try {
      const url = new URL(u);
      return url.protocol === "https:";
    } catch {
      return false;
    }
  }

  if (qsApi && isValidHttpsUrl(qsApi)) {
    localStorage.setItem("GALILEU_API_BASE", qsApi);
  }

  const storedApi = localStorage.getItem("GALILEU_API_BASE");
  const PROD_API_BASE =
    (storedApi && isValidHttpsUrl(storedApi)) ? storedApi : DEFAULT_PROD_API_BASE;

  window.GALILEU = window.GALILEU || {};
  window.GALILEU.API_BASE = isLocal ? LOCAL_API_BASE : PROD_API_BASE;
  window.GALILEU.USE_COOKIES = true;

  window.GALILEU.setApiBase = (newApiBase) => {
    if (!isValidHttpsUrl(newApiBase)) throw new Error("API_BASE precisa ser uma URL https válida");
    localStorage.setItem("GALILEU_API_BASE", newApiBase);
    window.location.reload();
  };
})();
