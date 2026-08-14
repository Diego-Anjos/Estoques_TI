/**
 * Tema global (claro/escuro) baseado em localStorage.
 *
 * Uso (módulo):
 *   import { applyTheme, initTheme, toggleTheme, isDarkTheme } from '../../shared/js/theme.js';
 *   initTheme();
 *
 * Preferência: localStorage key "theme" = "dark" | "light"
 * Aplica data-theme="dark" em <html> e <body>.
 */

export function isDarkTheme() {
  return localStorage.getItem('theme') === 'dark';
}

/**
 * @param {boolean} isDark
 */
export function applyTheme(isDark) {
  const html = document.documentElement;
  const body = document.body;
  const themeIcon = document.querySelector('.theme-icon');

  if (isDark) {
    html.setAttribute('data-theme', 'dark');
    if (body) body.setAttribute('data-theme', 'dark');
    html.classList.add('dark');
    if (body) body.classList.add('dark');
    if (themeIcon) themeIcon.textContent = '◑';
    localStorage.setItem('theme', 'dark');
  } else {
    html.removeAttribute('data-theme');
    if (body) body.removeAttribute('data-theme');
    html.classList.remove('dark');
    if (body) body.classList.remove('dark');
    if (themeIcon) themeIcon.textContent = '◐';
    localStorage.setItem('theme', 'light');
  }

  return isDark;
}

export function initTheme() {
  return applyTheme(isDarkTheme());
}

export function toggleTheme() {
  return applyTheme(!isDarkTheme());
}

/** Liga o botão #theme-toggle, se existir. */
export function bindThemeToggle(selector = '#theme-toggle') {
  const btn = document.querySelector(selector);
  if (!btn) return null;
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    toggleTheme();
  });
  return btn;
}

export default { applyTheme, initTheme, toggleTheme, isDarkTheme, bindThemeToggle };
