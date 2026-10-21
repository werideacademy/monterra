// Monterra — interazioni minime

(function () {
  const root = document.documentElement;
  const header = document.querySelector(".site-header");
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.getElementById("nav");

  // Header trasparente sopra l'hero, solido dopo lo scroll
  const onScroll = () => header.classList.toggle("is-solid", window.scrollY > 40);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  // Menu mobile
  const closeMenu = () => {
    document.body.classList.remove("nav-open");
    toggle.setAttribute("aria-expanded", "false");
  };
  toggle.addEventListener("click", () => {
    const open = document.body.classList.toggle("nav-open");
    toggle.setAttribute("aria-expanded", String(open));
  });
  nav.querySelectorAll("a").forEach((a) => a.addEventListener("click", closeMenu));
  document.addEventListener("keydown", (e) => e.key === "Escape" && closeMenu());

  // Comparsa degli elementi allo scroll
  const items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => entries.forEach((en) => {
        if (en.isIntersecting) {
          en.target.classList.add("is-visible");
          io.unobserve(en.target);
        }
      }),
      { rootMargin: "0px 0px -10% 0px", threshold: 0.08 }
    );
    items.forEach((el) => io.observe(el));
  } else {
    root.classList.add("no-js");
  }

  document.getElementById("year").textContent = new Date().getFullYear();
})();

// Logo e "Torna su": ritorno all'inizio della home
document.querySelectorAll('.brand, a[href="#top"]').forEach((a) =>
  a.addEventListener("click", (e) => {
    e.preventDefault();
    document.body.classList.remove("nav-open");
    window.scrollTo({ top: 0, behavior: "smooth" });
    history.replaceState(null, "", location.pathname);
  })
);
