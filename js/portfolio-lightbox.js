(function () {
  "use strict";

  var lightbox = document.getElementById("portfolio-lightbox");
  var triggers = document.querySelectorAll(".portfolio-case__image");

  if (!lightbox || !triggers.length) {
    return;
  }

  var preview = lightbox.querySelector("img");
  var closeButton = lightbox.querySelector(".portfolio-lightbox__close");
  var activeTrigger = null;

  function openLightbox(trigger) {
    var thumbnail = trigger.querySelector("img");

    activeTrigger = trigger;
    preview.src = trigger.href;
    preview.alt = thumbnail ? thumbnail.alt : "Project image";
    lightbox.hidden = false;
    document.body.classList.add("portfolio-lightbox-open");
    preview.focus();
  }

  function closeLightbox() {
    lightbox.hidden = true;
    document.body.classList.remove("portfolio-lightbox-open");
    preview.removeAttribute("src");

    if (activeTrigger) {
      activeTrigger.focus();
      activeTrigger = null;
    }
  }

  triggers.forEach(function (trigger) {
    trigger.addEventListener("click", function (event) {
      event.preventDefault();
      openLightbox(trigger);
    });
  });

  preview.addEventListener("click", closeLightbox);
  closeButton.addEventListener("click", closeLightbox);

  lightbox.addEventListener("click", function (event) {
    if (event.target === lightbox) {
      closeLightbox();
    }
  });

  document.addEventListener("keydown", function (event) {
    if (lightbox.hidden) {
      return;
    }

    if (event.key === "Escape") {
      closeLightbox();
    } else if ((event.key === "Enter" || event.key === " ") && event.target === preview) {
      event.preventDefault();
      closeLightbox();
    }
  });
})();
