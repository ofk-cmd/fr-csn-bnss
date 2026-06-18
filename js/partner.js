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

    var tab = window.open(PARTNER_URL, "_blank", "noopener,noreferrer");
    if (tab) {
      try {
        tab.opener = null;
        tab.focus();
      } catch (e) {}
      return;
    }

    var link = document.createElement("a");
    link.href = PARTNER_URL;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.style.display = "none";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
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
})();
