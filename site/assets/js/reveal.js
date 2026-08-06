(function () {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var els = document.querySelectorAll(".featured-card, li.entry, .project, .updates .update, .timeline .exp-item");
  if (!("IntersectionObserver" in window) || !els.length) return;
  els.forEach(function (e) { e.classList.add("to-reveal"); });
  var io = new IntersectionObserver(function (list) {
    list.forEach(function (x) {
      if (x.isIntersecting) { x.target.classList.add("revealed"); io.unobserve(x.target); }
    });
  }, { rootMargin: "0px 0px -8% 0px" });
  els.forEach(function (e) { io.observe(e); });
})();
