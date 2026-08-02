/**
 * Sticky rail scroll-spy for Phase 2 report.
 */
(function (global) {
  function bindScrollSpy(root) {
    if (!root || !window.IntersectionObserver) return;
    var links = root.querySelectorAll("[data-rpt-nav]");
    var tiers = root.querySelectorAll(".rpt-tier[id]");
    if (!links.length || !tiers.length) return;

    var map = {};
    links.forEach(function (a) {
      map[a.getAttribute("data-rpt-nav")] = a;
    });

    function setActive(id) {
      links.forEach(function (a) {
        a.classList.toggle("is-active", a.getAttribute("data-rpt-nav") === id);
      });
    }

    var observer = new IntersectionObserver(
      function (entries) {
        var visible = entries
          .filter(function (e) {
            return e.isIntersecting;
          })
          .sort(function (a, b) {
            return b.intersectionRatio - a.intersectionRatio;
          });
        if (visible[0] && visible[0].target && visible[0].target.id) {
          setActive(visible[0].target.id);
        }
      },
      { root: null, rootMargin: "-20% 0px -55% 0px", threshold: [0.1, 0.25, 0.5] }
    );

    tiers.forEach(function (tier) {
      observer.observe(tier);
    });

    links.forEach(function (a) {
      a.addEventListener("click", function (ev) {
        var id = a.getAttribute("data-rpt-nav");
        var el = id && root.querySelector("#" + id);
        if (!el) return;
        ev.preventDefault();
        el.scrollIntoView({ behavior: "smooth", block: "start" });
        setActive(id);
      });
    });
  }

  global.BteScrollSpy = { bind: bindScrollSpy };
})(typeof window !== "undefined" ? window : globalThis);
