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

    let succeeded = false;
    try {
      // JSON { email, senha } — alinhado com UsuarioLogin no FastAPI (não OAuth2 form)
      const data = await api.post('/usuarios/login', { email, senha }, { skipAuth: true });
      saveSession(data);
      succeeded = true;
      showNotification(`Bem-vindo(a), ${data.nome}!`, 'success', { duration: 1200 });
      setTimeout(() => {
        window.location.href = '../dashboard/paginainicial/index.html';
      }, 900);
    } catch (error) {
      if (error?.notified || error?.isNetworkError) {
        // api.js já notificou erro de rede
      } else if (error?.status === 401) {
        showNotification('Email ou senha incorretos.', 'error');
      } else {
        showNotification(error.message || 'Não foi possível fazer login.', 'error');
      }
    } finally {
      if (!succeeded) {
        btn.disabled = false;
        btn.textContent = labelOriginal;
      }
    }
  });
});
