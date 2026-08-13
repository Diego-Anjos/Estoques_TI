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

    if (senha !== confirmar) {
      showNotification('As senhas não coincidem.', 'warning');
      return;
    }

    btn.disabled = true;
    const labelOriginal = btn.textContent;
    btn.textContent = 'Cadastrando...';

    try {
      await api.post('/usuarios/', {
        nome,
        email,
        senha,
        ativo: 'S',
      });

      showNotification('Conta criada com sucesso! Redirecionando para o login...', 'success', {
        duration: 1800,
      });
      setTimeout(() => {
        window.location.href = '../login/index.html';
      }, 1400);
    } catch (error) {
      showNotification(error.message || 'Não foi possível criar a conta.', 'error');
      btn.disabled = false;
      btn.textContent = labelOriginal;
    }
  });
});
