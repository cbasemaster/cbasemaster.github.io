const year = document.querySelector("#year");
const navLinks = document.querySelectorAll(".nav-links a[href^='#']");
const metricFields = document.querySelectorAll("[data-metric]");
const soundtrackToggle = document.querySelector("#soundtrack-toggle");
const soundtrackPlayer = document.querySelector("#soundtrack-player");

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

if (soundtrackToggle && soundtrackPlayer) {
  soundtrackToggle.addEventListener("click", () => {
    const isPlaying = soundtrackToggle.getAttribute("aria-pressed") === "true";
    const icon = soundtrackToggle.querySelector(".soundtrack-icon");

    if (isPlaying) {
      soundtrackPlayer.replaceChildren();
      soundtrackToggle.setAttribute("aria-pressed", "false");
      soundtrackToggle.setAttribute("aria-label", "Play site soundtrack");
      soundtrackToggle.setAttribute("title", "Play soundtrack");
      if (icon) {
        icon.textContent = "\u25b6";
      }
      return;
    }

    const player = document.createElement("iframe");
    player.src = "https://www.youtube-nocookie.com/embed/w3a_iTwQIi4?autoplay=1&loop=1&playlist=w3a_iTwQIi4&controls=0";
    player.title = "Radical Dreamers by Noriko Mitose";
    player.allow = "autoplay; encrypted-media";
    player.referrerPolicy = "strict-origin-when-cross-origin";
    soundtrackPlayer.replaceChildren(player);
    soundtrackToggle.setAttribute("aria-pressed", "true");
    soundtrackToggle.setAttribute("aria-label", "Stop site soundtrack");
    soundtrackToggle.setAttribute("title", "Stop soundtrack");
    if (icon) {
      icon.textContent = "\u25a0";
    }
  });
}
