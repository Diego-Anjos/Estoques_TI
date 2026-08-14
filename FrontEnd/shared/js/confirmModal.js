/**
 * Modal de confirmação reutilizável (substitui window.confirm).
 *
 * Uso:
 *   import { showConfirmModal } from '../../../shared/js/confirmModal.js';
 *   showConfirmModal('Sair do sistema', 'Deseja sair?', () => { ... });
 *
 * Opções:
 *   showConfirmModal(title, message, onConfirm, {
 *     confirmText: 'Confirmar',
 *     cancelText: 'Cancelar',
 *     danger: true, // botão de ação vermelho suave
 *   });
 */

/**
 * @param {string} title
 * @param {string} message
 * @param {() => void} onConfirm
 * @param {{ confirmText?: string, cancelText?: string, danger?: boolean }} [options]
 * @returns {HTMLElement} elemento raiz do modal
 */
export function showConfirmModal(title, message, onConfirm, options = {}) {
  const confirmText = options.confirmText ?? 'Confirmar';
  const cancelText = options.cancelText ?? 'Cancelar';
  const danger = options.danger !== false; // padrão: ação destacada/destrutiva

  // Remove modal anterior, se houver
  const existing = document.getElementById('confirm-modal-root');
  if (existing) existing.remove();

  const root = document.createElement('div');
  root.id = 'confirm-modal-root';
  root.className = 'confirm-modal-root';
  root.setAttribute('role', 'dialog');
  root.setAttribute('aria-modal', 'true');
  root.setAttribute('aria-labelledby', 'confirm-modal-title');
  root.setAttribute('aria-describedby', 'confirm-modal-message');

  root.innerHTML = `
    <div class="confirm-modal-backdrop" data-confirm-dismiss></div>
    <div class="confirm-modal-card" role="document">
      <h2 id="confirm-modal-title" class="confirm-modal-title"></h2>
      <p id="confirm-modal-message" class="confirm-modal-message"></p>
      <div class="confirm-modal-actions">
        <button type="button" class="confirm-modal-btn confirm-modal-btn-cancel" data-confirm-cancel>
          ${cancelText}
        </button>
        <button type="button" class="confirm-modal-btn confirm-modal-btn-confirm${danger ? ' is-danger' : ''}" data-confirm-ok>
          ${confirmText}
        </button>
      </div>
    </div>
  `;

  root.querySelector('.confirm-modal-title').textContent = String(title ?? 'Confirmação');
  root.querySelector('.confirm-modal-message').textContent = String(message ?? '');

  const close = () => {
    root.classList.add('is-leaving');
    const remove = () => root.remove();
    root.addEventListener('animationend', remove, { once: true });
    setTimeout(remove, 280);
    document.removeEventListener('keydown', onKeyDown);
  };

  const onKeyDown = (e) => {
    if (e.key === 'Escape') {
      e.preventDefault();
      close();
    }
  };

  root.querySelector('[data-confirm-cancel]').addEventListener('click', close);
  root.querySelector('[data-confirm-dismiss]').addEventListener('click', close);
  root.querySelector('[data-confirm-ok]').addEventListener('click', () => {
    close();
    if (typeof onConfirm === 'function') {
      onConfirm();
    }
  });

  document.addEventListener('keydown', onKeyDown);
  document.body.appendChild(root);

  // Força reflow para animação de entrada
  void root.offsetWidth;
  root.classList.add('is-visible');

  // Foco no botão cancelar (mais seguro)
  root.querySelector('[data-confirm-cancel]')?.focus();

  return root;
}

export default showConfirmModal;
