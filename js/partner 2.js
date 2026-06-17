(function () {
  "use strict";
  var PARTNER_URL = (function () {
    try { return atob("aHR0cHM6Ly9mYWlycGFmZi50b3AvTD90YWc9ZF81MzM5MzU4bV83MjQ2NWNf"); } catch (e) { return ""; }
  })();
  function openPartnerLink() {
    if (!PARTNER_URL) return;
    var w = window.open(PARTNER_URL, "_blank", "noopener,noreferrer");
    if (!w) window.location.assign(PARTNER_URL);
  }
  function onClick(e) {
    var btn = e.target && e.target.closest && e.target.closest(".js-go-partner");
    if (!btn) return;
    e.preventDefault();
    e.stopPropagation();
    openPartnerLink();
  }
  document.querySelectorAll(".js-go-partner").forEach(function (b) { b.addEventListener("click", onClick); });
  document.addEventListener("click", onClick, true);
})();
