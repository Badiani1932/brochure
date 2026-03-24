/* ── Touch-device dropdown fix ──
   On tablets (no hover), the first tap opens the dropdown menu;
   the second tap on the same parent link navigates to the page.
   Tapping outside or on a sub-item closes the dropdown normally. */
(function () {
  if (window.matchMedia('(hover: hover)').matches) return;

  document.addEventListener('click', function (e) {
    var trigger = e.target.closest('.topbar__dropdown > a');
    if (trigger) {
      var dd = trigger.closest('.topbar__dropdown');
      if (!dd.classList.contains('is-open')) {
        e.preventDefault();
        document.querySelectorAll('.topbar__dropdown.is-open').forEach(function (o) {
          o.classList.remove('is-open');
        });
        dd.classList.add('is-open');
        return;
      }
    }
    if (!e.target.closest('.topbar__dropdown')) {
      document.querySelectorAll('.topbar__dropdown.is-open').forEach(function (dd) {
        dd.classList.remove('is-open');
      });
    }
  });
})();
