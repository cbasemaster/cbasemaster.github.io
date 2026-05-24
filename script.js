const year = document.querySelector("#year");
const navLinks = document.querySelectorAll(".nav-links a[href^='#']");
const metricFields = document.querySelectorAll("[data-metric]");

if (year) {
  year.textContent = new Date().getFullYear();
}

navLinks.forEach((link) => {
  link.addEventListener("click", () => {
    document.querySelector(".nav-links a.active")?.classList.remove("active");
    link.classList.add("active");
  });
});

async function refreshMetrics() {
  if (!metricFields.length) {
    return;
  }

  try {
    const response = await fetch("data/metrics.json", { cache: "no-store" });
    if (!response.ok) {
      return;
    }

    const metrics = await response.json();
    metricFields.forEach((field) => {
      const key = field.dataset.metric;
      if (key && metrics[key] !== undefined && metrics[key] !== null) {
        field.textContent = metrics[key];
      }
    });
  } catch (error) {
    // Static fallback values stay visible when metrics cannot be refreshed.
  }
}

refreshMetrics();
