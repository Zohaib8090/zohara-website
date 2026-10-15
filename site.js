/* Zohara OS website: the scroll rail, appear-on-scroll, the theme switch and the phone menu.
   The page is complete without this file (everything is plain HTML); this only adds motion. No libraries, no network. */
(function () {
  "use strict";
  var root = document.documentElement;
  root.classList.add("js");
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ── theme: dark by default, light when the system asks or the person chose it (remembered only if storage works) ──
  var KEY = "zohara-theme";
  try { var saved = localStorage.getItem(KEY); if (saved === "light" || saved === "dark") root.setAttribute("data-theme", saved); } catch (e) {}
  var themeBtn = document.getElementById("theme");
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      var current = root.getAttribute("data-theme") ||
        (window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark");
      var next = current === "light" ? "dark" : "light";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem(KEY, next); } catch (e) {}
    });
  }

  // ── phone menu ──
  var menuBtn = document.getElementById("menu");
  var nav = document.getElementById("nav");
  if (menuBtn && nav) {
    menuBtn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.addEventListener("click", function (e) { if (e.target.tagName === "A") nav.classList.remove("open"); });
  }

  // ── appear on scroll ──
  var items = document.querySelectorAll(".rv");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("in"); });
  }

  // ── the rail ──
  // A ruler on the right edge, a line that grows as you scroll with its percent, and one label per section. Labels sit where
  // their section starts; the further a label is from where you are, the more it turns away and fades, so the one you are at
  // swings into view along a curve. Wide screens only (the CSS hides the rail below 1240px).
  var sections = Array.prototype.slice.call(document.querySelectorAll("[data-rail]"));
  if (!sections.length) return;
  var rail = document.createElement("nav");
  rail.className = "rail";
  rail.setAttribute("aria-label", "Page sections");
  rail.innerHTML = '<div class="rail-ticks" aria-hidden="true"></div><div class="rail-line" aria-hidden="true"></div><div class="rail-pct" aria-hidden="true">0%</div>';
  var line = rail.querySelector(".rail-line");
  var pct = rail.querySelector(".rail-pct");
  var labels = sections.map(function (s, i) {
    var a = document.createElement("a");
    a.className = "rail-label";
    a.href = "#" + s.id;
    a.innerHTML = "<b>" + String(i + 1).padStart(2, "0") + "</b>" + s.getAttribute("data-rail");
    rail.appendChild(a);
    return a;
  });
  document.body.appendChild(rail);

  // Label positions: sections are spread along the rail in proportion to where they start, but never closer than a minimum gap
  // and never beyond the end (the last sections are shorter than the screen, so the page cannot scroll to their start).
  var tops = [];      // where each section starts, in page pixels
  var fracs = [];     // where each label sits on the rail, 0..1
  var probeShare = 0.35; // "where we are" is a line this far down the screen
  function measure() {
    tops = sections.map(function (s) { return s.getBoundingClientRect().top + window.scrollY; });
    var last = Math.max(1, tops[tops.length - 1] - tops[0]);
    fracs = tops.map(function (t) { return ((t - tops[0]) / last) * 0.92; });
    var minGap = 0.075;
    for (var i = 1; i < fracs.length; i++) if (fracs[i] - fracs[i - 1] < minGap) fracs[i] = fracs[i - 1] + minGap;
    var over = fracs[fracs.length - 1] - 0.96;
    if (over > 0) fracs = fracs.map(function (f, i) { return f - over * (i / Math.max(1, fracs.length - 1)); });
    var h = rail.clientHeight;
    labels.forEach(function (l, i) { l.style.top = (fracs[i] * h - 13) + "px"; });
  }
  // Where the current spot of the page lies on the rail: between the labels of the sections around it.
  function railPos() {
    var at = window.scrollY + window.innerHeight * probeShare;
    var endAt = root.scrollHeight - window.innerHeight * (1 - probeShare);
    if (at <= tops[0]) return 0;
    for (var i = 0; i < tops.length; i++) {
      var nextTop = i + 1 < tops.length ? tops[i + 1] : Math.max(endAt, tops[i] + 1);
      var nextFrac = i + 1 < tops.length ? fracs[i + 1] : 1;
      if (at < nextTop || i === tops.length - 1) {
        var t = Math.min(1, Math.max(0, (at - tops[i]) / Math.max(1, nextTop - tops[i])));
        return fracs[i] + (nextFrac - fracs[i]) * t;
      }
    }
    return 1;
  }

  var ticking = false;
  function update() {
    ticking = false;
    var max = Math.max(1, root.scrollHeight - window.innerHeight);
    var real = Math.min(1, Math.max(0, window.scrollY / max));
    var pos = railPos();
    var h = rail.clientHeight;
    line.style.height = (pos * h) + "px";
    pct.style.top = (pos * h) + "px";
    pct.textContent = Math.round(real * 100) + "%";
    var active = 0;
    for (var k = 0; k < fracs.length; k++) if (fracs[k] <= pos + 0.0001) active = k;
    labels.forEach(function (l, i) {
      l.classList.toggle("on", i === active);
      if (reduce) return;
      var d = (fracs[i] - pos) / 0.16;                      // about 1 = the next label away
      var c = Math.max(-2, Math.min(2, d));
      var rot = c * 34;                                     // degrees: the further, the more it turns away
      var shift = c * c * 14;                               // pixels: swings out along a curve
      var op = Math.max(0, 1 - Math.abs(c) * 0.5);          // gone two labels away
      l.style.transform = "translateX(" + (-shift) + "px) rotate(" + rot + "deg)";
      l.style.opacity = i === active ? "1" : String(op);
      l.style.pointerEvents = op < 0.15 ? "none" : "auto";
    });
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", function () { measure(); update(); });
  window.addEventListener("load", function () { measure(); update(); });
  measure(); update();
})();
