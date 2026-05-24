const year = document.querySelector("#year");
const navLinks = document.querySelectorAll(".nav-links a[href^='#']");

if (year) {
  year.textContent = new Date().getFullYear();
}

navLinks.forEach((link) => {
  link.addEventListener("click", () => {
    document.querySelector(".nav-links a.active")?.classList.remove("active");
    link.classList.add("active");
  });
});
