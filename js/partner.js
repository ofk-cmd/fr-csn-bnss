(function () {
  "use strict";

  var PARTNER_URL = "https://bobaffs.org/click?o=1603&a=189";
  var lastOpenAt = 0;

  function resolvePartnerButton(target) {
    if (!target || !target.closest) return null;
    return target.closest(".js-go-partner");
  }

  function openPartnerLink() {
    if (!PARTNER_URL || PARTNER_URL === "#") return;
    var now = Date.now();
    if (now - lastOpenAt < 400) return;
    lastOpenAt = now;
    var opened = window.open(PARTNER_URL, "_blank", "noopener,noreferrer");
    if (!opened) window.location.href = PARTNER_URL;
  }

  function onPartnerClick(event) {
    var btn = resolvePartnerButton(event.target);
    if (!btn) return;
    event.preventDefault();
    event.stopPropagation();
    if (typeof event.stopImmediatePropagation === "function") {
      event.stopImmediatePropagation();
    }
    openPartnerLink();
  }

  document.addEventListener("click", onPartnerClick, true);

  function bindButtons() {
    document.querySelectorAll(".js-go-partner").forEach(function (btn) {
      if (btn.dataset.partnerBound === "1") return;
      btn.dataset.partnerBound = "1";
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        openPartnerLink();
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bindButtons);
  } else {
    bindButtons();
  }
})();
