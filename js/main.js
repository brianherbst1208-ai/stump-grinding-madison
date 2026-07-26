/* Madison Stump Grinding — site interactions */
(function () {
  "use strict";

  /* ---- Mobile nav toggle ---- */
  var nav = document.querySelector(".nav");
  var toggle = document.querySelector(".nav__toggle");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.innerHTML = open ? "&times;" : "&#9776;";
    });
  }

  /* ---- FAQ accordion (accessible) ---- */
  var faqItems = document.querySelectorAll(".faq__item");
  faqItems.forEach(function (item) {
    var btn = item.querySelector(".faq__q");
    var ans = item.querySelector(".faq__a");
    if (!btn || !ans) return;
    btn.setAttribute("aria-expanded", "false");
    btn.addEventListener("click", function () {
      var isOpen = item.classList.contains("open");
      if (isOpen) {
        item.classList.remove("open");
        ans.style.maxHeight = null;
        btn.setAttribute("aria-expanded", "false");
      } else {
        item.classList.add("open");
        ans.style.maxHeight = ans.scrollHeight + "px";
        btn.setAttribute("aria-expanded", "true");
      }
    });
  });
  // Recalculate open answer height on resize
  window.addEventListener("resize", function () {
    document.querySelectorAll(".faq__item.open .faq__a").forEach(function (a) {
      a.style.maxHeight = a.scrollHeight + "px";
    });
  });

  /* ---- Lead form validation ---- */
  document.querySelectorAll("form.leadform, form[data-lead]").forEach(function (form) {
    var success = form.querySelector(".form-success");

    function validateField(field) {
      var input = field.querySelector("input, select, textarea");
      if (!input || !input.hasAttribute("required")) return true;
      var val = (input.value || "").trim();
      var ok = val.length > 0;
      if (input.type === "tel") {
        var digits = val.replace(/\D/g, "");
        ok = digits.length >= 10;
      }
      if (input.tagName === "SELECT") ok = val.length > 0;
      field.classList.toggle("invalid", !ok);
      return ok;
    }

    form.querySelectorAll(".field").forEach(function (field) {
      var input = field.querySelector("input, select, textarea");
      if (input) {
        input.addEventListener("blur", function () { validateField(field); });
        input.addEventListener("input", function () {
          if (field.classList.contains("invalid")) validateField(field);
        });
      }
    });

    form.addEventListener("submit", function (e) {
      var allValid = true;
      form.querySelectorAll(".field").forEach(function (field) {
        if (!validateField(field)) allValid = false;
      });
      if (!allValid) {
        e.preventDefault();
        var firstBad = form.querySelector(".field.invalid input, .field.invalid select");
        if (firstBad) firstBad.focus();
        return;
      }
      // DEMO MODE: no live backend wired yet. Prevent default and show success.
      // To go live, set the form's action to your Formspree/Netlify endpoint
      // and remove the block below (see README.md).
      if (form.getAttribute("action") === "#" || form.dataset.demo === "true") {
        e.preventDefault();
        form.querySelectorAll(".field, .btn").forEach(function (el) { el.style.display = "none"; });
        if (success) { success.style.display = "block"; }
      }
    });
  });

  /* ---- Footer year ---- */
  var yr = document.getElementById("year");
  if (yr) yr.textContent = new Date().getFullYear();

  /* ---- Active nav link highlight ---- */
  var path = window.location.pathname.replace(/index\.html$/, "");
  document.querySelectorAll(".nav__links a").forEach(function (a) {
    var href = a.getAttribute("href");
    if (!href || href.charAt(0) === "#") return;
    var clean = href.replace(/index\.html$/, "");
    if (clean === path) a.classList.add("active");
  });
})();
