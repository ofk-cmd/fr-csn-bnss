(function () {
  "use strict";

  var toggle = document.querySelector(".nav-toggle");
  var mobileNav = document.querySelector(".nav-mobile");
  if (toggle && mobileNav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      mobileNav.classList.toggle("is-open", !open);
    });
    mobileNav.querySelectorAll('a[href^="#"]').forEach(function (link) {
      link.addEventListener("click", function () {
        toggle.setAttribute("aria-expanded", "false");
        mobileNav.classList.remove("is-open");
      });
    });
  }

  var faqItems = document.querySelectorAll(".faq-item");
  faqItems.forEach(function (item, index) {
    var btn = item.querySelector(".faq-item__question");
    if (!btn) return;

    if (index === 0) {
      item.classList.add("is-open");
      btn.setAttribute("aria-expanded", "true");
    } else {
      btn.setAttribute("aria-expanded", "false");
    }

    btn.addEventListener("click", function () {
      var isOpen = item.classList.contains("is-open");
      faqItems.forEach(function (other) {
        other.classList.remove("is-open");
        var otherBtn = other.querySelector(".faq-item__question");
        if (otherBtn) otherBtn.setAttribute("aria-expanded", "false");
      });
      if (!isOpen) {
        item.classList.add("is-open");
        btn.setAttribute("aria-expanded", "true");
      }
    });
  });

  var backTop = document.querySelector(".back-to-top");
  if (backTop) {
    window.addEventListener("scroll", function () {
      backTop.classList.toggle("is-visible", window.scrollY > 600);
    });
    backTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  var stickyCta = document.getElementById("sticky-cta");
  if (stickyCta) {
    var stickyKey = "casino_sticky_dismissed";
    var stickyDismissed = sessionStorage.getItem(stickyKey) === "1";

    function updateStickyVisibility() {
      if (stickyDismissed) {
        stickyCta.classList.add("is-hidden");
        document.body.classList.remove("has-sticky-cta");
        return;
      }
      var show = window.scrollY > 520;
      stickyCta.classList.toggle("is-hidden", !show);
      document.body.classList.toggle("has-sticky-cta", show);
    }

    updateStickyVisibility();
    window.addEventListener("scroll", updateStickyVisibility, { passive: true });

    var closeBtn = stickyCta.querySelector(".sticky-cta__close");
    function dismissSticky(event) {
      if (event) {
        event.preventDefault();
        event.stopPropagation();
      }
      stickyDismissed = true;
      stickyCta.classList.add("is-hidden");
      document.body.classList.remove("has-sticky-cta");
      try {
        sessionStorage.setItem(stickyKey, "1");
      } catch (e) {}
    }
    if (closeBtn) {
      closeBtn.addEventListener("click", dismissSticky);
      closeBtn.addEventListener("touchend", dismissSticky, { passive: false });
    }
  }

  document.querySelectorAll("[data-carousel]").forEach(function (root) {
    var slides = root.querySelectorAll(".promo-slide");
    if (!slides.length) return;
    var dots = root.querySelectorAll(".promo-carousel__dot");
    var prev = root.querySelector(".promo-carousel__nav--prev");
    var next = root.querySelector(".promo-carousel__nav--next");
    var index = 0;
    var timer;

    function show(i) {
      index = (i + slides.length) % slides.length;
      slides.forEach(function (s, n) {
        s.classList.toggle("is-active", n === index);
      });
      dots.forEach(function (d, n) {
        d.classList.toggle("is-active", n === index);
      });
    }

    function restart() {
      clearInterval(timer);
      timer = setInterval(function () {
        show(index + 1);
      }, 6000);
    }

    if (prev) prev.addEventListener("click", function () { show(index - 1); restart(); });
    if (next) next.addEventListener("click", function () { show(index + 1); restart(); });
    dots.forEach(function (dot) {
      dot.addEventListener("click", function () {
        var n = parseInt(dot.getAttribute("data-goto"), 10);
        if (!isNaN(n)) { show(n); restart(); }
      });
    });
    show(0);
    restart();
  });

  var promoCodeEl = document.getElementById("site-promo-code");
  var promoBadge = document.querySelector("[data-promo-badge]");
  if (promoCodeEl && promoBadge) {
    promoBadge.textContent = promoCodeEl.textContent.trim();
  }

  var pageLang = (document.documentElement.lang || "uz").toLowerCase().slice(0, 2);
  var copyI18n = {
    uz: { copied: "Nusxalandi!", prompt: "Promo kodni nusxalang:" },
    ru: { copied: "Скопировано!", prompt: "Скопируйте промокод:" },
    en: { copied: "Copied!", prompt: "Copy promo code:" }
  };
  var copyL = copyI18n[pageLang] || copyI18n.uz;

  var copyPromoBtns = document.querySelectorAll(".js-copy-promo");
  copyPromoBtns.forEach(function (btn) {
    var defaultLabel = btn.textContent.trim();
    if (pageLang === "ru" && defaultLabel === "Nusxalash") defaultLabel = "Копировать";
    if (pageLang === "en" && defaultLabel === "Nusxalash") defaultLabel = "Copy";
    btn.textContent = defaultLabel;
    btn.addEventListener("click", function (event) {
      event.preventDefault();
      event.stopPropagation();
      var targetId = btn.getAttribute("data-copy-target");
      var codeEl = targetId ? document.getElementById(targetId) : null;
      var code = codeEl ? codeEl.textContent.trim() : "";
      if (!code) return;

      function onCopied() {
        btn.classList.add("is-copied");
        btn.textContent = copyL.copied;
        window.setTimeout(function () {
          btn.classList.remove("is-copied");
          btn.textContent = defaultLabel;
        }, 1800);
      }

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(code).then(onCopied).catch(function () {
          window.prompt(copyL.prompt, code);
        });
      } else {
        window.prompt(copyL.prompt, code);
      }
    });
  });

})();
