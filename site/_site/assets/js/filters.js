(function () {
  var bar = document.querySelector(".filter-bar");
  if (!bar) return;
  var btns = bar.querySelectorAll(".filter-btn");
  var entries = document.querySelectorAll("li.entry[data-topics]");
  var sections = document.querySelectorAll("main section.level2, main h2");
  function apply(key) {
    btns.forEach(function (b) { b.classList.toggle("active", (b.dataset.filter || "") === key); });
    entries.forEach(function (e) {
      e.hidden = key !== "" && (" " + e.dataset.topics + " ").indexOf(" " + key + " ") < 0;
    });
    // nascondi le sezioni rimaste vuote e rendi visibile il resto
    sections.forEach(function (sec) {
      var ul = sec.matches("section") ? sec.querySelector("ul.entries") : sec.nextElementSibling;
      if (!ul || !ul.matches || !ul.matches("ul.entries")) return;
      var any = ul.querySelector("li.entry:not([hidden])");
      sec.hidden = !any; ul.hidden = !any;
    });
    entries.forEach(function (e) { if (!e.hidden) e.classList.add("revealed"); });
    var url = new URL(location);
    if (key) url.searchParams.set("tema", key); else url.searchParams.delete("tema");
    history.replaceState(null, "", url);
  }
  bar.addEventListener("click", function (ev) {
    var b = ev.target.closest(".filter-btn");
    if (b) apply(b.dataset.filter || "");
  });
  var initial = new URL(location).searchParams.get("tema") || "";
  if (initial) apply(initial);
})();
