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

    function showBanner(msg) {
      var b = form.querySelector(".form-banner");
      if (!b) {
        b = document.createElement("p");
        b.className = "form-banner";
        b.style.cssText = "color:#d9480f;font-weight:600;margin:10px 0 0;text-align:center";
        var btnEl = form.querySelector('button[type="submit"]');
        if (btnEl && btnEl.parentNode) btnEl.parentNode.insertBefore(b, btnEl.nextSibling);
        else form.appendChild(b);
      }
      b.textContent = msg;
    }
    function fireLead() {
      try {
        if (typeof window.gtag === "function") {
          var svcEl = form.querySelector('[name="service"]');
          window.gtag("event", "generate_lead", {
            form_id: form.id || "lead",
            service: svcEl ? svcEl.value : "",
            page_path: window.location.pathname
          });
        }
      } catch (e) {}
    }

    function done() {
      form.querySelectorAll(".field, .btn, .form-note").forEach(function (el) { el.style.display = "none"; });
      var b = form.querySelector(".form-banner"); if (b) b.remove();
      if (success) success.style.display = "block";
    }

    // Tag each submission with the page it came from
    var sp = form.querySelector('input[name="source_page"]');
    if (sp && !sp.value) sp.value = (document.title || "") + " " + window.location.pathname;

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
      // DEMO MODE: no live backend wired. Show success without sending.
      if (form.getAttribute("action") === "#" || form.dataset.demo === "true") {
        e.preventDefault();
        done();
        return;
      }
      // LIVE: submit via AJAX (Formspree) so the visitor stays on the page.
      e.preventDefault();
      var btn = form.querySelector('button[type="submit"]');
      var orig = btn ? btn.innerHTML : "";
      if (btn) { btn.disabled = true; btn.innerHTML = "Sending…"; }
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (res) {
          if (res.ok) { fireLead(); done(); return; }
          return res.json().then(function (d) {
            var msg = (d && d.errors && d.errors.length)
              ? d.errors.map(function (x) { return x.message; }).join(", ")
              : "Sorry — something went wrong. Please call us instead.";
            showBanner(msg);
            if (btn) { btn.disabled = false; btn.innerHTML = orig; }
          });
        })
        .catch(function () {
          showBanner("Network error — please call us at the number above.");
          if (btn) { btn.disabled = false; btn.innerHTML = orig; }
        });
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
