(() => {
  async function protectPage({ redirect = "cadastrar.html" } = {}) {
    return window.GalileuAuth.requireAuth(redirect);
  }

  window.GalileuGuards = {
    protectPage,
  };
})();
