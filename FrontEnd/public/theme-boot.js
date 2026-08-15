/**
 * Boot síncrono do tema (sem module) — incluir no <head> para evitar flash.
 * Lê localStorage.theme e aplica data-theme/dark imediatamente.
 */
(function applyThemeBoot() {
  try {
    var isDark = localStorage.getItem('theme') === 'dark';
    var html = document.documentElement;
    if (isDark) {
      html.setAttribute('data-theme', 'dark');
      html.classList.add('dark');
    } else {
      html.removeAttribute('data-theme');
      html.classList.remove('dark');
    }
    document.addEventListener('DOMContentLoaded', function () {
      var body = document.body;
      if (!body) return;
      if (isDark) {
        body.setAttribute('data-theme', 'dark');
        body.classList.add('dark');
      } else {
        body.removeAttribute('data-theme');
        body.classList.remove('dark');
      }
      var icon = document.querySelector('.theme-icon');
      if (icon) icon.textContent = isDark ? '◑' : '◐';
    });
  } catch (e) {
    /* ignore */
  }
})();
