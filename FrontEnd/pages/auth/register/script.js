import { api } from '../../../shared/js/api.js';
import { showNotification } from '../../../shared/js/notify.js';

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('form-cadastro');
  const btn = document.getElementById('btn-cadastrar');
  const nomeInput = document.getElementById('nome-completo');
  const emailInput = document.getElementById('email-cadastro');
  const senhaInput = document.getElementById('senha-cadastro');
  const confirmarInput = document.getElementById('confirmar-senha');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const nome = nomeInput.value.trim();
    const email = emailInput.value.trim();
    const senha = senhaInput.value;
    const confirmar = confirmarInput.value;

    if (!nome || !email || !senha || !confirmar) {
      showNotification('Por favor, preencha todos os campos.', 'warning');
      return;
    }

    if (senha.length < 6) {
      showNotification('A senha deve ter pelo menos 6 caracteres.', 'warning');
      return;
    }

    if (senha !== confirmar) {
      showNotification('As senhas não coincidem.', 'warning');
      return;
    }

    btn.disabled = true;
    const labelOriginal = btn.textContent;
    btn.textContent = 'Cadastrando...';

    let succeeded = false;
    try {
      // Rota pública — não exige JWT (cadastro antes do primeiro login)
      await api.post(
        '/usuarios/registro',
        {
          nome,
          email,
          senha,
          ativo: 'S',
        },
        { skipAuth: true }
      );

      succeeded = true;
      showNotification('Conta criada com sucesso! Redirecionando para o login...', 'success', {
        duration: 1800,
      });
      setTimeout(() => {
        window.location.href = '../login/index.html';
      }, 1400);
    } catch (error) {
      if (error?.notified || error?.isNetworkError) {
        // api.js já notificou erro de rede
      } else {
        showNotification(error.message || 'Não foi possível criar a conta.', 'error');
      }
    } finally {
      if (!succeeded) {
        btn.disabled = false;
        btn.textContent = labelOriginal;
      }
    }
  });
});
