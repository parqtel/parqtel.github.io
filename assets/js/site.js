/* Parqtel site — minimal vanilla JS. No dependencies. */
(function () {
  "use strict";

  // --- Theme -----------------------------------------------------------
  var root = document.documentElement;
  var stored = null;
  try { stored = localStorage.getItem("parqtel-theme"); } catch (e) {}
  if (!stored) {
    stored = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  root.setAttribute("data-theme", stored);

  function setTheme(t) {
    root.setAttribute("data-theme", t);
    try { localStorage.setItem("parqtel-theme", t); } catch (e) {}
    var btn = document.querySelector("[data-theme-toggle]");
    if (btn) btn.setAttribute("aria-label", t === "dark" ? "Switch to light mode" : "Switch to dark mode");
  }
  document.addEventListener("click", function (e) {
    var t = e.target.closest("[data-theme-toggle]");
    if (t) setTheme(root.getAttribute("data-theme") === "dark" ? "light" : "dark");
  });

  // --- Mobile nav ------------------------------------------------------
  document.addEventListener("click", function (e) {
    var t = e.target.closest(".nav-toggle");
    if (t) {
      var links = document.getElementById("navLinks");
      if (links) links.classList.toggle("open");
    }
  });

  // --- Copy buttons ----------------------------------------------------
  document.addEventListener("click", function (e) {
    var btn = e.target.closest(".copy-btn");
    if (!btn) return;
    var block = btn.closest(".codeblock");
    var code = block && block.querySelector("code, pre");
    var text = code ? code.innerText : "";
    if (navigator.clipboard && text) {
      navigator.clipboard.writeText(text).then(function () {
        btn.textContent = "Copied";
        btn.classList.add("ok");
        setTimeout(function () { btn.textContent = "Copy"; btn.classList.remove("ok"); }, 1400);
      });
    }
  });

  // --- Active nav / sidebar link (scrollspy) ---------------------------
  function markActive() {
    var links = Array.prototype.slice.call(document.querySelectorAll(".nav-links a, .sidebar a"));
    if (!links.length) return;
    var id = location.pathname.split("/").pop() || "index.html";
    links.forEach(function (a) {
      var href = a.getAttribute("href");
      if (href && href.indexOf(id) !== -1 && href.indexOf("#") === -1) a.classList.add("active");
    });
    // In-page anchor highlight
    var headings = Array.prototype.slice.call(document.querySelectorAll("h2[id], h3[id]"));
    if (!headings.length) return;
    var pos = window.scrollY + 120;
    var current = headings[0].id;
    headings.forEach(function (h) { if (h.offsetTop <= pos) current = h.id; });
    document.querySelectorAll(".sidebar a[href*='#']").forEach(function (a) {
      a.classList.toggle("active", a.getAttribute("href").split("#")[1] === current);
    });
  }
  window.addEventListener("scroll", markActive, { passive: true });
  window.addEventListener("load", markActive);
  markActive();
})();
