import { api } from '../../../shared/js/api.js';
import { saveSession } from '../../../shared/js/auth.js';
import { showNotification } from '../../../shared/js/notify.js';

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('form-login');
  const btn = document.getElementById('btn-entrar');
  const emailInput = document.getElementById('email-login');
  const senhaInput = document.getElementById('senha-login');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const email = emailInput.value.trim();
    const senha = senhaInput.value;

    if (!email || !senha) {
      showNotification('Por favor, preencha todos os campos.', 'warning');
      return;
    }

    btn.disabled = true;
    const labelOriginal = btn.textContent;
    btn.textContent = 'Entrando...';

    try {
      const data = await api.post('/usuarios/login', { email, senha });
      saveSession(data);
      showNotification(`Bem-vindo(a), ${data.nome}!`, 'success', { duration: 1200 });
      setTimeout(() => {
        window.location.href = '../dashboard/paginainicial/index.html';
      }, 900);
    } catch (error) {
      showNotification(error.message || 'Não foi possível fazer login.', 'error');
      btn.disabled = false;
      btn.textContent = labelOriginal;
    }
  });
});
