(function () {
  var EMAIL = "tracynajjimngo01@gmail.com";

  // Preview build: hash routing between views (the deployed site uses real pages instead)
  var views = document.querySelectorAll(".view");
  function route() {
    var id = (location.hash || "#home").slice(1);
    var anchor = document.getElementById(id);
    if (anchor && !anchor.classList.contains("view")) { anchor.scrollIntoView({ behavior: "smooth" }); return; }
    var found = false;
    views.forEach(function (v) { var on = v.dataset.view === id; v.hidden = !on; if (on) { found = true; document.title = v.dataset.title; } });
    if (!found && views.length) { views.forEach(function (v, i) { v.hidden = i !== 0; }); id = "home"; }
    markNav(id === "home" ? "" : id.split("-")[0]);
    window.scrollTo(0, 0);
  }
  function markNav(section) {
    document.querySelectorAll("[data-nav]").forEach(function (a) {
      if (a.dataset.nav === section) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
    });
  }
  if (views.length) { window.addEventListener("hashchange", route); route(); }
  else { markNav((document.body.dataset.route || "").split("/")[0]); }

  // Work page filter
  document.addEventListener("click", function (ev) {
    var b = ev.target.closest && ev.target.closest(".chip-btn");
    if (!b) return;
    var f = b.dataset.filter, group = b.parentElement;
    group.querySelectorAll(".chip-btn").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
    var grid = group.parentElement.querySelector("#project-grid");
    grid.querySelectorAll(".pcard").forEach(function (card) {
      var match = (" " + card.dataset.cats + " ").indexOf(" " + f + " ") > -1;
      card.hidden = card.dataset.only ? (" " + card.dataset.only + " ").indexOf(" " + f + " ") === -1 : !(f === "all" || match);
    });
  });

  // Journey: glass orb timeline
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.querySelectorAll("[data-journey]").forEach(function (jx) {
    var DUR = 5200, tabs = [].slice.call(jx.querySelectorAll(".jx-tab")), panels = jx.querySelectorAll(".jx-panel");
    var reel = jx.querySelector(".jx-reel"), sub = jx.querySelector(".jx-sub"), ring = jx.querySelector(".jx-ring circle");
    var playBtn = jx.querySelector(".jx-play"), idx = 0, timer = null, visible = false, held = false, playing = !reduce;
    jx.style.setProperty("--jx-dur", DUR + "ms");
    function restartRing() { jx.classList.remove("running"); void jx.offsetWidth; if (playing && visible && !held) jx.classList.add("running"); }
    function show(i, focus) {
      idx = (i + tabs.length) % tabs.length;
      reel.style.setProperty("--n", idx);
      tabs.forEach(function (t, k) { var on = k === idx; t.setAttribute("aria-selected", on); t.tabIndex = on ? 0 : -1; });
      panels.forEach(function (p, k) { p.hidden = k !== idx; p.classList.remove("enter"); });
      if (!reduce) { void panels[idx].offsetWidth; panels[idx].classList.add("enter"); }
      sub.classList.add("fade"); setTimeout(function () { sub.textContent = tabs[idx].dataset.sub; sub.classList.remove("fade"); }, reduce ? 0 : 450);
      if (focus) tabs[idx].focus();
      schedule();
    }
    function schedule() {
      clearTimeout(timer); restartRing();
      if (playing && visible && !held) timer = setTimeout(function () { show(idx + 1); }, DUR);
    }
    tabs.forEach(function (t, k) {
      t.addEventListener("click", function () { show(k); });
      t.addEventListener("keydown", function (ev) {
        if (ev.key === "ArrowRight" || ev.key === "ArrowDown") { ev.preventDefault(); show(idx + 1, true); }
        if (ev.key === "ArrowLeft" || ev.key === "ArrowUp") { ev.preventDefault(); show(idx - 1, true); }
        if (ev.key === "Home") { ev.preventDefault(); show(0, true); }
        if (ev.key === "End") { ev.preventDefault(); show(tabs.length - 1, true); }
      });
    });
    function setPlaying(v) { playing = v; playBtn.dataset.playing = v; playBtn.setAttribute("aria-label", v ? "Pause the timeline" : "Play the timeline"); schedule(); }
    playBtn.addEventListener("click", function () { setPlaying(!playing); });
    setPlaying(playing);
    jx.addEventListener("mouseenter", function () { held = true; schedule(); });
    jx.addEventListener("mouseleave", function () { held = false; schedule(); });
    jx.addEventListener("focusin", function () { held = true; schedule(); });
    jx.addEventListener("focusout", function (ev) { if (!jx.contains(ev.relatedTarget)) { held = false; schedule(); } });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (en) { visible = en[0].isIntersecting; schedule(); }, { threshold: 0.35 }).observe(jx);
    } else { visible = true; schedule(); }
  });

  // Contact form: opens the visitor's email app with the message filled in
  document.addEventListener("submit", function (ev) {
    var f = ev.target;
    if (f.id !== "contact-form") return;
    ev.preventDefault();
    var status = f.querySelector("#cf-status");
    var bad = null;
    f.querySelectorAll("[required]").forEach(function (el) {
      var ok = el.value.trim() !== "" && (el.type !== "email" || /.+@.+\..+/.test(el.value));
      el.setAttribute("aria-invalid", ok ? "false" : "true");
      if (!ok && !bad) bad = el;
    });
    if (bad) { status.textContent = "Please fill in your name, a valid email and your message."; bad.focus(); return; }
    var v = function (n) { return f.elements[n].value.trim(); };
    var subject = "New project enquiry from " + v("name") + (v("company") ? " (" + v("company") + ")" : "");
    var body = v("message") + "\n\n" + v("name") + "\n" + v("email") + (v("company") ? "\n" + v("company") : "");
    var href = "mailto:" + EMAIL + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
    status.innerHTML = "Your email app should open with the message ready to send. If it doesn’t, email <a href=\"mailto:" + EMAIL + "\">" + EMAIL + "</a> directly.";
    window.location.href = href;
  });
})();
