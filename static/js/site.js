(function () {
  function bindDrawer(btnId, drawerId, backdropId, closeId) {
    const btn = document.getElementById(btnId);
    const drawer = document.getElementById(drawerId);
    const backdrop = document.getElementById(backdropId);
    const closeBtn = document.getElementById(closeId);

    if (!btn || !drawer || !backdrop || !closeBtn) return;

    function openDrawer() {
      drawer.classList.add("g1drawer--open");
      drawer.setAttribute("aria-hidden", "false");
      btn.setAttribute("aria-expanded", "true");
      backdrop.hidden = false;
    }

    function closeDrawer() {
      drawer.classList.remove("g1drawer--open");
      drawer.setAttribute("aria-hidden", "true");
      btn.setAttribute("aria-expanded", "false");
      backdrop.hidden = true;
    }

    btn.addEventListener("click", openDrawer);
    closeBtn.addEventListener("click", closeDrawer);
    backdrop.addEventListener("click", closeDrawer);

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeDrawer();
    });
  }

  // Drawer do sticky (home + notícia)
  bindDrawer("g1MenuBtnSticky", "g1drawerSticky", "g1BackdropSticky", "g1CloseBtnSticky");

  // Sticky bar (home + notícia): aparece ao rolar
  const g1Sticky = document.getElementById("g1barSticky");
  const topBanner = document.getElementById("top-banner");
  const mainMenu = document.getElementById("main-menu");

  if (g1Sticky) {
    g1Sticky.classList.remove("g1bar--show");
    g1Sticky.setAttribute("aria-hidden", "true");

    function onScroll() {
      // ponto de gatilho: depois de passar o banner + menu
      let trigger = 180;
      if (topBanner && mainMenu) {
        trigger = topBanner.offsetHeight + mainMenu.offsetHeight - 10;
      }

      if (window.scrollY > trigger) {
        g1Sticky.classList.add("g1bar--show");
        g1Sticky.setAttribute("aria-hidden", "false");
      } else {
        g1Sticky.classList.remove("g1bar--show");
        g1Sticky.setAttribute("aria-hidden", "true");
      }
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }
})();
