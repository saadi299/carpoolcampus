document.addEventListener("DOMContentLoaded", function () {
  const toggleBtn = document.getElementById("mobile-menu-button");
  const menu = document.getElementById("mobile-menu");

  if (toggleBtn && menu) {
    toggleBtn.addEventListener("click", function () {
      const isExpanded = toggleBtn.getAttribute("aria-expanded") === "true";
      toggleBtn.setAttribute("aria-expanded", !isExpanded);
      menu.classList.toggle("hidden");
    });
  }
});
