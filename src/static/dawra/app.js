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
