/* LAPP Muller relaunch concept: progressive enhancement only.
   Every page works without JavaScript; scripts add menu behaviour and form help. */
(function () {
  "use strict";

  /* ---------- mobile menu ---------- */
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
      var label = toggle.querySelector("span:last-child");
      if (label) label.textContent = open ? "Close" : "Menu";
    });
  }

  /* ---------- mega menus (one open at a time) ---------- */
  var triggers = Array.prototype.slice.call(document.querySelectorAll(".nav-trigger"));
  triggers.forEach(function (btn) {
    var panel = document.getElementById(btn.getAttribute("aria-controls"));
    if (!panel) return;
    function setOpen(open) {
      btn.setAttribute("aria-expanded", String(open));
      panel.classList.toggle("open", open);
    }
    btn._setOpen = setOpen;
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var willOpen = btn.getAttribute("aria-expanded") !== "true";
      triggers.forEach(function (o) { if (o !== btn && o._setOpen) o._setOpen(false); });
      setOpen(willOpen);
    });
    document.addEventListener("click", function (e) {
      if (!panel.contains(e.target)) setOpen(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && btn.getAttribute("aria-expanded") === "true") {
        setOpen(false);
        btn.focus();
      }
    });
  });

  /* ---------- stage slider (manual, no autoplay) ---------- */
  var stage = document.querySelector(".stage");
  if (stage) {
    var slides = Array.prototype.slice.call(stage.querySelectorAll(".slide"));
    var dots = Array.prototype.slice.call(stage.querySelectorAll(".dot"));
    var idx = 0;
    function go(i) {
      idx = (i + slides.length) % slides.length;
      slides.forEach(function (s, n) { s.hidden = n !== idx; });
      dots.forEach(function (d, n) {
        if (n === idx) d.setAttribute("aria-current", "true"); else d.removeAttribute("aria-current");
      });
    }
    stage.querySelector(".stage-prev").addEventListener("click", function () { go(idx - 1); });
    stage.querySelector(".stage-next").addEventListener("click", function () { go(idx + 1); });
    dots.forEach(function (d, n) { d.addEventListener("click", function () { go(n); }); });
  }

  /* ---------- tabs ---------- */
  document.querySelectorAll("[data-tabs]").forEach(function (box) {
    var tabs = Array.prototype.slice.call(box.querySelectorAll('[role="tab"]'));
    function select(tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute("aria-selected", String(on));
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
      });
      if (focus) tab.focus();
    }
    tabs.forEach(function (t, n) {
      t.addEventListener("click", function () { select(t); });
      t.addEventListener("keydown", function (e) {
        if (e.key === "ArrowRight") select(tabs[(n + 1) % tabs.length], true);
        if (e.key === "ArrowLeft") select(tabs[(n - 1 + tabs.length) % tabs.length], true);
      });
    });
  });

  /* ---------- field validation ---------- */
  function validate(field) {
    var ok = field.checkValidity();
    field.setAttribute("aria-invalid", ok ? "false" : "true");
    return ok;
  }
  function validateScope(scope) {
    var fields = scope.querySelectorAll("input[required], select[required], textarea[required], input[type=email]");
    var first = null;
    fields.forEach(function (f) {
      if (!validate(f) && !first) first = f;
    });
    // radio groups marked required via data attribute
    scope.querySelectorAll("[data-required-group]").forEach(function (group) {
      var checked = group.querySelector("input:checked");
      var err = group.querySelector(".error");
      if (err) err.style.display = checked ? "none" : "block";
      if (!group.dataset.bound) {
        group.dataset.bound = "1";
        group.addEventListener("change", function () { if (err) err.style.display = "none"; });
      }
      if (!checked && !first) first = group.querySelector("input");
    });
    if (first) first.focus();
    return !first;
  }
  document.querySelectorAll(".form input, .form select, .form textarea").forEach(function (f) {
    f.addEventListener("blur", function () {
      if (f.value !== "" || f.getAttribute("aria-invalid") === "true") validate(f);
    });
    // clear an error as soon as the input becomes valid, so the layout settles before the next click
    f.addEventListener("input", function () {
      if (f.getAttribute("aria-invalid") === "true") validate(f);
    });
  });

  /* ---------- summary helper ---------- */
  function summarise(form) {
    var lines = [];
    var data = new FormData(form);
    data.forEach(function (value, key) {
      if (value instanceof File) { if (value.name) lines.push(key + ": " + value.name); return; }
      if (String(value).trim() !== "") lines.push(key + ": " + value);
    });
    return lines.join("\n");
  }
  function showResult(form, title, text) {
    var box = form.parentNode.querySelector(".form-result");
    if (!box) return;
    box.hidden = false;
    box.querySelector("h2").textContent = title;
    box.querySelector("pre").textContent = text;
    form.hidden = true;
    box.setAttribute("tabindex", "-1");
    box.focus();
  }

  /* ---------- multi-step project request ---------- */
  var rfq = document.getElementById("rfq");
  if (rfq) {
    var steps = Array.prototype.slice.call(rfq.querySelectorAll(".form-step"));
    var markers = Array.prototype.slice.call(document.querySelectorAll(".stepper li"));
    var current = 0;
    function show(i, noFocus) {
      steps.forEach(function (s, n) { s.hidden = n !== i; });
      markers.forEach(function (m, n) {
        m.classList.toggle("done", n < i);
        if (n === i) m.setAttribute("aria-current", "step"); else m.removeAttribute("aria-current");
      });
      current = i;
      var heading = steps[i].querySelector("legend");
      if (heading && !noFocus) { heading.setAttribute("tabindex", "-1"); heading.focus(); }
    }
    rfq.addEventListener("click", function (e) {
      var t = e.target.closest("[data-step]");
      if (!t) return;
      e.preventDefault();
      var dir = t.getAttribute("data-step");
      if (dir === "next" && validateScope(steps[current])) show(current + 1);
      if (dir === "back") show(current - 1);
    });
    rfq.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!validateScope(steps[current])) return;
      showResult(rfq, "Your request is ready", summarise(rfq));
    });
    show(0, true);
    // Pre-select industry from ?industry=slug
    var param = new URLSearchParams(window.location.search).get("industry");
    if (param) {
      var radio = rfq.querySelector('input[name="industry"][value="' + param.replace(/[^a-z-]/g, "") + '"]');
      if (radio) radio.checked = true;
    }
  }

  /* ---------- simple contact form ---------- */
  var contact = document.getElementById("contact-form");
  if (contact) {
    contact.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!validateScope(contact)) return;
      showResult(contact, "Your message is ready", summarise(contact));
    });
  }

  /* ---------- cookie settings placeholder ---------- */
  document.querySelectorAll("[data-cookie-settings]").forEach(function (b) {
    b.addEventListener("click", function () {
      b.textContent = "Cookie settings: connect consent tool";
    });
  });
})();
