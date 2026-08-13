/**
 * Toast de notificação do sistema.
 *
 * Uso:
 *   import { showNotification } from '../../../shared/js/notify.js';
 *   showNotification('Mensagem', 'success'); // success | error | warning | info
 *   showNotification('Mensagem', 'error', { duration: 5000 });
 */

const ICONS = {
  success: `
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
      <path d="M8 12.5l2.5 2.5L16 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>`,
  error: `
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
      <path d="M15 9l-6 6M9 9l6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    </svg>`,
  warning: `
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="M12 3l9 16H3L12 3z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
      <path d="M12 10v4M12 17h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    </svg>`,
  info: `
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
      <path d="M12 11v5M12 8h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    </svg>`,
};

const TITLES = {
  success: 'Sucesso',
  error: 'Erro',
  warning: 'Atenção',
  info: 'Informação',
};

function ensureContainer() {
  let container = document.getElementById('notify-root');
  if (!container) {
    container = document.createElement('div');
    container.id = 'notify-root';
    container.className = 'notify-root';
    container.setAttribute('aria-live', 'polite');
    container.setAttribute('aria-relevant', 'additions');
    document.body.appendChild(container);
  }
  return container;
}

function dismissToast(toast) {
  if (!toast || toast.classList.contains('is-leaving')) return;
  toast.classList.add('is-leaving');
  const remove = () => toast.remove();
  toast.addEventListener('animationend', remove, { once: true });
  // Fallback se animationend não disparar
  setTimeout(remove, 350);
}

/**
 * Exibe um toast moderno no canto superior direito.
 * @param {string} message - Texto da notificação
 * @param {'success'|'error'|'warning'|'info'} [type='info']
 * @param {{ duration?: number }} [options]
 * @returns {HTMLElement} elemento do toast
 */
export function showNotification(message, type = 'info', options = {}) {
  const kind = ICONS[type] ? type : 'info';
  const duration = options.duration ?? (kind === 'error' ? 5000 : 3500);
  const container = ensureContainer();

  const toast = document.createElement('div');
  toast.className = `notify-toast notify-${kind}`;
  toast.setAttribute('role', kind === 'error' ? 'alert' : 'status');

  toast.innerHTML = `
    <div class="notify-icon">${ICONS[kind]}</div>
    <div class="notify-body">
      <strong class="notify-title">${TITLES[kind]}</strong>
      <p class="notify-message"></p>
    </div>
    <button type="button" class="notify-close" aria-label="Fechar notificação">×</button>
    <div class="notify-progress" style="animation-duration:${duration}ms"></div>
  `;

  toast.querySelector('.notify-message').textContent = String(message ?? '');

  const closeBtn = toast.querySelector('.notify-close');
  closeBtn.addEventListener('click', () => dismissToast(toast));

  container.appendChild(toast);

  // Força reflow para animação de entrada
  void toast.offsetWidth;
  toast.classList.add('is-visible');

  if (duration > 0) {
    const timer = setTimeout(() => dismissToast(toast), duration);
    toast.addEventListener('mouseenter', () => clearTimeout(timer), { once: true });
  }

  return toast;
}

export default showNotification;
