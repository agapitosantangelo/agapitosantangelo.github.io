// Hero della homepage: il plot event-study si costruisce da solo all'apertura
// (~3s, una volta sola), poi la pagina scorre normalmente. Ogni gruppo SVG
// dichiara la propria finestra in data-step="inizio fine" (frazioni 0..1
// della timeline). Senza JS o con prefers-reduced-motion il grafico resta
// completo e statico.
(function () {
  var hero = document.querySelector("[data-hero-anim]");
  if (!hero) return;
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var els = [].slice.call(hero.querySelectorAll(".es-anim"));
  var svg = hero.querySelector(".es-hero-svg");
  if (!svg || !els.length) return;

  var DURATA = 3200; // ms per l'intera sequenza
  var RITARDO = 350; // respiro prima di partire

  function clamp01(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function ease(v) { return 1 - Math.pow(1 - v, 3); } // easeOutCubic
  function seg(p, a, b) { return ease(clamp01((p - a) / (b - a))); }

  function render(p) {
    els.forEach(function (g) {
      var s = (g.getAttribute("data-step") || "0 1").split(" ");
      var e = seg(p, +s[0], +s[1]);
      if (g.hasAttribute("data-draw")) {
        // la linea del trattamento si "disegna" dall'alto verso il basso
        g.style.opacity = e > 0 ? "1" : "0";
        g.style.clipPath = "inset(0 0 " + ((1 - e) * 100).toFixed(2) + "% 0)";
      } else {
        var rise = +(g.getAttribute("data-rise") || 14);
        g.style.opacity = e.toFixed(3);
        g.style.transform = "translateY(" + ((1 - e) * rise).toFixed(2) + "px)";
      }
    });
  }

  render(0);

  var partito = false;
  function play() {
    if (partito) return;
    partito = true;
    setTimeout(function () {
      var t0 = null;
      function tick(ts) {
        if (t0 === null) t0 = ts;
        var p = clamp01((ts - t0) / DURATA);
        render(p);
        if (p < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    }, RITARDO);
  }

  // parte quando il grafico entra in vista (in cima alla pagina: subito)
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (list) {
      list.forEach(function (x) {
        if (x.isIntersecting) { io.disconnect(); play(); }
      });
    }, { threshold: 0.15 });
    io.observe(svg);
  } else {
    play();
  }
})();
