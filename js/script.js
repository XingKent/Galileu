document.addEventListener("DOMContentLoaded", () => {
  if (document.body.id === "home") {
    const videos = document.querySelectorAll(".video-container video");
    let index = 0;

    function trocarVideo() {
      // Pausar todos
      videos.forEach(v => {
        v.pause();
        v.style.opacity = "0";
      });

      // Mostrar o atual
      let atual = videos[index];
      atual.currentTime = 0;
      atual.play();
      atual.style.opacity = "1";

      // Próximo índice
      index = (index + 1) % videos.length;
    }

    // Primeira execução
    trocarVideo();

    // Troca a cada 6s
    setInterval(trocarVideo, 6000);
  }
});
