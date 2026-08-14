/**
 * Toggle do menu lateral (sidebar) + overlay mobile.
 *
 * Uso:
 *   import { initSidebar } from '../../../shared/js/sidebar.js';
 *   initSidebar();
 *
 * Esperado no DOM (opcional — só ativa se existir):
 *   #menu-toggle / .menu-toggle  → botão hambúrguer
 *   #app-sidebar / .app-sidebar  → aside
 *   #sidebar-overlay             → overlay (criado automaticamente se faltar)
 */
const OPEN_CLASS = 'sidebar-open';
const BODY_CLASS = 'has-sidebar-open';

function ensureOverlay() {
  let overlay = document.getElementById('sidebar-overlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.id = 'sidebar-overlay';
    overlay.className = 'sidebar-overlay';
    overlay.setAttribute('aria-hidden', 'true');
    document.body.appendChild(overlay);
  }
  return overlay;
}

function setOpen(open, { sidebar, toggle, overlay } = {}) {
  const side = sidebar || document.getElementById('app-sidebar') || document.querySelector('.app-sidebar');
  const btn = toggle || document.getElementById('menu-toggle') || document.querySelector('.menu-toggle');
  const layer = overlay || document.getElementById('sidebar-overlay');

  if (!side) return;

  side.classList.toggle(OPEN_CLASS, open);
  document.body.classList.toggle(BODY_CLASS, open);

  if (btn) {
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    btn.classList.toggle('is-active', open);
  }
  if (layer) {
    layer.classList.toggle('is-visible', open);
    layer.setAttribute('aria-hidden', open ? 'false' : 'true');
  }
}

/**
 * Inicializa o hamburger / sidebar. Seguro chamar em páginas sem sidebar.
 * @returns {{ open: Function, close: Function, toggle: Function } | null}
 */
export function initSidebar() {
  const sidebar = document.getElementById('app-sidebar') || document.querySelector('.app-sidebar');
  const toggle = document.getElementById('menu-toggle') || document.querySelector('.menu-toggle');

  if (!sidebar || !toggle) {
    return null;
  }

  const overlay = ensureOverlay();

  const api = {
    open: () => setOpen(true, { sidebar, toggle, overlay }),
    close: () => setOpen(false, { sidebar, toggle, overlay }),
    toggle: () => {
      const isOpen = sidebar.classList.contains(OPEN_CLASS);
      setOpen(!isOpen, { sidebar, toggle, overlay });
    },
  };

  toggle.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    api.toggle();
  });

  overlay.addEventListener('click', () => api.close());

  sidebar.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      if (window.matchMedia('(max-width: 767px)').matches) {
        api.close();
      }
    });
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') api.close();
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth >= 768) {
      api.close();
    }
  });

  // Estado inicial: fechado no mobile
  if (window.matchMedia('(max-width: 767px)').matches) {
    api.close();
  }

  return api;
}

export default initSidebar;
