document.addEventListener("DOMContentLoaded", () => {
  // Ampliar las imágenes cuando se les hace clic
  const miniPhotos = document.querySelectorAll(".miniPhoto");
  const modal = document.getElementById("photoModal");
  const imgContainer = document.getElementById("imgContainer");
  const closeModal = document.getElementById("closeModal");

  miniPhotos.forEach((img) => {
    img.addEventListener("click", () => {
      const modalImg = document.createElement("img");
      modalImg.src = img.src.replace("320x240", "800x600");
      modalImg.alt = "Foto ampliada";
      imgContainer.innerHTML = "";
      imgContainer.appendChild(modalImg);
      modal.classList.add("active");
    });
  });

  // Cerramos la imagen cuando se presiona la X o se pierde el foco
  closeModal.addEventListener("click", () => modal.classList.remove("active"));
  window.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.classList.remove("active");
    }
  });
});
