import { api } from '../../shared/js/api.js';
import { getSession, isAuthenticated, clearSession, saveSession } from '../../shared/js/auth.js';
import { showNotification } from '../../shared/js/notify.js';
import { initSidebar } from '../../shared/js/sidebar.js';

const LOGIN_URL = '../auth/login/index.html';

if (!isAuthenticated()) {
  window.location.replace(LOGIN_URL);
  throw new Error('Sessão não encontrada');
}

const sessao = getSession();
const form = document.getElementById('profile-form');
const nomeInput = document.getElementById('nome');
const emailInput = document.getElementById('email');
const cargoInput = document.getElementById('cargo');
const senhaInput = document.getElementById('senha');
const confirmarSenhaInput = document.getElementById('confirmar-senha');
const btnSalvar = document.getElementById('btn-salvar');
const greeting = document.getElementById('user-greeting');
const themeToggle = document.getElementById('theme-toggle');

function fillFormFromSession() {
  if (!sessao?.id_usuario) {
    clearSession();
    window.location.replace(LOGIN_URL);
    return;
  }

  nomeInput.value = sessao.nome || '';
  emailInput.value = sessao.email || '';
  cargoInput.value = sessao.cargo || '';

  if (greeting) {
    greeting.textContent = `Olá, ${sessao.nome || 'Usuário'}`;
  }
}

function initTheme() {
  const savedTheme = localStorage.getItem('theme');
  const html = document.documentElement;
  const body = document.body;
  const themeIcon = document.querySelector('.theme-icon');

  if (savedTheme === 'dark') {
    body.setAttribute('data-theme', 'dark');
    html.setAttribute('data-theme', 'dark');
    if (themeIcon) themeIcon.textContent = '◑';
  } else {
    body.removeAttribute('data-theme');
    html.removeAttribute('data-theme');
    if (themeIcon) themeIcon.textContent = '◐';
  }
}

function toggleTheme() {
  const html = document.documentElement;
  const body = document.body;
  const themeIcon = document.querySelector('.theme-icon');

  if (body.getAttribute('data-theme') === 'dark') {
    body.removeAttribute('data-theme');
    html.removeAttribute('data-theme');
    if (themeIcon) themeIcon.textContent = '◐';
    localStorage.setItem('theme', 'light');
  } else {
    body.setAttribute('data-theme', 'dark');
    html.setAttribute('data-theme', 'dark');
    if (themeIcon) themeIcon.textContent = '◑';
    localStorage.setItem('theme', 'dark');
  }
}

function buildPayload() {
  const nome = nomeInput.value.trim();
  const email = emailInput.value.trim();
  const cargo = cargoInput.value.trim();
  const senha = senhaInput.value;
  const confirmar = confirmarSenhaInput.value;

  if (!nome || nome.length < 3) {
    throw new Error('Informe um nome com pelo menos 3 caracteres.');
  }
  if (!email) {
    throw new Error('Informe um e-mail válido.');
  }

  if (senha || confirmar) {
    if (senha.length < 6) {
      throw new Error('A nova senha deve ter pelo menos 6 caracteres.');
    }
    if (senha !== confirmar) {
      throw new Error('As senhas não coincidem.');
    }
  }

  const payload = { nome, email, cargo };

  if (senha) {
    payload.senha = senha;
  }

  return payload;
}

async function handleSubmit(event) {
  event.preventDefault();

  let payload;
  try {
    payload = buildPayload();
  } catch (validationError) {
    showNotification(validationError.message, 'warning');
    return;
  }

  btnSalvar.disabled = true;
  const labelOriginal = btnSalvar.textContent;
  btnSalvar.textContent = 'Salvando...';

  try {
    const atualizado = await api.put(`/usuarios/${sessao.id_usuario}`, payload);

    saveSession({
      id_usuario: atualizado.id_usuario,
      nome: atualizado.nome,
      email: atualizado.email,
      cargo: atualizado.cargo ?? '',
    });

    senhaInput.value = '';
    confirmarSenhaInput.value = '';
    if (greeting) greeting.textContent = `Olá, ${atualizado.nome}`;

    showNotification('Perfil atualizado com sucesso!', 'success');
  } catch (error) {
    showNotification(error.message || 'Não foi possível atualizar o perfil.', 'error');
  } finally {
    btnSalvar.disabled = false;
    btnSalvar.textContent = labelOriginal;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  fillFormFromSession();
  initTheme();
  initSidebar();

  form.addEventListener('submit', handleSubmit);

  if (themeToggle) {
    themeToggle.addEventListener('click', (e) => {
      e.preventDefault();
      toggleTheme();
    });
  }
});
