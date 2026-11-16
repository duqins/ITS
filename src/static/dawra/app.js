// Feedback while a form is being sent, and no double sending.
// Every form that changes data (POST) marks its button as busy and ignores a second click,
// so an approval or a hold is never sent twice. Buttons that ask the AI also say so,
// because the answer can take a few seconds.
(function () {
  var AI_ACTIONS = /\/ai\/(assets\/\d+\/classify|requests\/\d+\/matches|report\/draft)\//;

  document.addEventListener("submit", function (event) {
    var form = event.target;
    if ((form.getAttribute("method") || "").toLowerCase() !== "post") return;
    if (form.dataset.sending) {
      event.preventDefault();
      return;
    }
    form.dataset.sending = "1";
    // The clicked button is not disabled: a disabled button would drop its name and value from the form.
    var button = event.submitter || form.querySelector("[type=submit]");
    if (!button) return;
    button.classList.add("is-busy");
    button.setAttribute("aria-busy", "true");
    if (AI_ACTIONS.test(form.action)) {
      button.dataset.label = button.innerHTML;
      button.innerHTML = 'Asking the AI<span class="thinking-dots" aria-hidden="true">' +
        "<span></span><span></span><span></span></span>";
    }
  });

  // Light and dark. The header button switches at once (the new theme spreads out in a circle from the
  // button where the browser supports it) and saves the choice to the account in the background.
  // On the Settings page, picking a theme previews it straight away; Save keeps it.
  var root = document.documentElement;

  function isDark() {
    var theme = root.dataset.theme;
    return theme === "dark" || (theme === "system" && matchMedia("(prefers-color-scheme: dark)").matches);
  }

  function lessMotion() {
    return root.dataset.motion === "reduced" || matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  function showTheme(theme, x, y) {
    var apply = function () { root.dataset.theme = theme; };
    if (!document.startViewTransition || lessMotion()) return apply();
    root.classList.add("theme-switching");
    var transition = document.startViewTransition(apply);
    transition.ready.then(function () {
      var radius = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
      root.animate(
        {clipPath: ["circle(0 at " + x + "px " + y + "px)", "circle(" + radius + "px at " + x + "px " + y + "px)"]},
        {duration: 560, easing: "cubic-bezier(.2,.7,.2,1)", pseudoElement: "::view-transition-new(root)"}
      );
    });
    transition.finished.then(function () { root.classList.remove("theme-switching"); });
  }

  // Runs before the busy-state handler above (capture), and stops it: this form never leaves the page.
  document.addEventListener("submit", function (event) {
    var form = event.target;
    if (!form.classList.contains("theme-toggle")) return;
    event.preventDefault();
    event.stopPropagation();
    var next = isDark() ? "light" : "dark";
    var box = form.querySelector("button").getBoundingClientRect();
    showTheme(next, box.left + box.width / 2, box.top + box.height / 2);
    var data = new FormData(form);
    data.set("theme", next);
    fetch(form.action, {method: "POST", body: data, credentials: "same-origin",
                        headers: {"X-Requested-With": "fetch"}});
  }, true);

  document.addEventListener("change", function (event) {
    var input = event.target;
    if (input.name !== "theme" || !input.closest(".settings")) return;
    var box = input.closest(".choice").getBoundingClientRect();
    showTheme(input.value, box.left + box.width / 2, box.top + box.height / 2);
  });

  // Numbers count up to their value when they come into view (home cards, AI scores).
  // The page already holds the true number, so without this script nothing is lost.
  function countUp(el) {
    var target = parseInt(el.dataset.count, 10);
    if (!(target > 0) || lessMotion()) return;
    var start = performance.now();
    var duration = Math.min(1200, 500 + target * 25);
    el.textContent = "0";
    requestAnimationFrame(function step(now) {
      var t = Math.min(1, (now - start) / duration);
      el.textContent = String(Math.round(target * (1 - Math.pow(1 - t, 3))));
      if (t < 1) requestAnimationFrame(step);
    });
  }

  if ("IntersectionObserver" in window) {
    var watcher = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        watcher.unobserve(entry.target);
        countUp(entry.target);
      });
    });
    document.querySelectorAll("[data-count]").forEach(function (el) { watcher.observe(el); });
  }

  // The browser's Back button can show the page exactly as it was left; make its buttons usable again.
  window.addEventListener("pageshow", function (event) {
    if (!event.persisted) return;
    document.querySelectorAll("form[data-sending]").forEach(function (form) {
      delete form.dataset.sending;
    });
    document.querySelectorAll(".is-busy").forEach(function (button) {
      button.classList.remove("is-busy");
      button.removeAttribute("aria-busy");
      if (button.dataset.label) button.innerHTML = button.dataset.label;
    });
  });
})();
