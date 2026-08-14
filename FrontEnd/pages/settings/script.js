import { api, apiDownload } from '../../shared/js/api.js';
import { getSession, isAuthenticated } from '../../shared/js/auth.js';
import { showNotification } from '../../shared/js/notify.js';
import { initSidebar } from '../../shared/js/sidebar.js';
import { applyTheme, initTheme, toggleTheme } from '../../shared/js/theme.js';

const LOGIN_URL = '../auth/login/index.html';

if (!isAuthenticated()) {
  window.location.replace(LOGIN_URL);
  throw new Error('Sessão não encontrada');
}

const sessao = getSession();
const greeting = document.getElementById('user-greeting');
const tabs = document.querySelectorAll('.settings-tab');
const panels = document.querySelectorAll('.settings-panel');
const darkToggle = document.getElementById('toggle-dark-mode');
const nomeEmpresaInput = document.getElementById('nome-empresa');
const estoqueMinimoInput = document.getElementById('estoque-minimo-global');

let configAtual = {
  nome_empresa: 'Controle de Estoque',
  modo_escuro: false,
  alerta_estoque_minimo: 5,
};

function syncDarkToggle() {
  if (darkToggle) darkToggle.checked = localStorage.getItem('theme') === 'dark';
}

function activateTab(tabId) {
  tabs.forEach((tab) => {
    const active = tab.dataset.tab === tabId;
    tab.classList.toggle('is-active', active);
    tab.setAttribute('aria-selected', active ? 'true' : 'false');
  });

  panels.forEach((panel) => {
    const active = panel.dataset.panel === tabId;
    panel.classList.toggle('is-active', active);
    if (active) panel.removeAttribute('hidden');
    else panel.setAttribute('hidden', '');
  });
}

async function carregarConfiguracoes() {
  try {
    const cfg = await api.get('/configuracoes/');
    configAtual = {
      nome_empresa: cfg.nome_empresa || 'Controle de Estoque',
      modo_escuro: Boolean(cfg.modo_escuro),
      alerta_estoque_minimo: Number(cfg.alerta_estoque_minimo ?? 5),
    };

    if (nomeEmpresaInput) nomeEmpresaInput.value = configAtual.nome_empresa;
    if (estoqueMinimoInput) estoqueMinimoInput.value = String(configAtual.alerta_estoque_minimo);

    applyTheme(configAtual.modo_escuro);
    syncDarkToggle();
  } catch (error) {
    showNotification(error.message || 'Não foi possível carregar as configurações.', 'error');
    initTheme();
    syncDarkToggle();
  }
}

async function salvarPreferenciasGerais() {
  const nome = (nomeEmpresaInput?.value || '').trim();
  if (nome.length < 2) {
    showNotification('Informe o nome da empresa (mín. 2 caracteres).', 'warning');
    return;
  }

  const modoEscuro = Boolean(darkToggle?.checked);
  applyTheme(modoEscuro);

  try {
    const atualizado = await api.put('/configuracoes/', {
      nome_empresa: nome,
      modo_escuro: modoEscuro,
      alerta_estoque_minimo: configAtual.alerta_estoque_minimo,
    });
    configAtual = {
      ...configAtual,
      nome_empresa: atualizado.nome_empresa,
      modo_escuro: Boolean(atualizado.modo_escuro),
      alerta_estoque_minimo: Number(atualizado.alerta_estoque_minimo ?? configAtual.alerta_estoque_minimo),
    };
    localStorage.setItem('theme', configAtual.modo_escuro ? 'dark' : 'light');
    showNotification('Preferências gerais salvas com sucesso!', 'success');
  } catch (error) {
    showNotification(error.message || 'Não foi possível salvar as preferências.', 'error');
  }
}

async function salvarRegraAlerta() {
  const valor = Number(estoqueMinimoInput?.value);
  if (Number.isNaN(valor) || valor < 0) {
    showNotification('Informe um estoque mínimo válido (>= 0).', 'warning');
    return;
  }

  try {
    const atualizado = await api.put('/configuracoes/', {
      nome_empresa: (nomeEmpresaInput?.value || configAtual.nome_empresa).trim(),
      modo_escuro: Boolean(darkToggle?.checked),
      alerta_estoque_minimo: valor,
    });
    configAtual.alerta_estoque_minimo = Number(atualizado.alerta_estoque_minimo);
    showNotification('Regra de alerta salva com sucesso!', 'success');
  } catch (error) {
    showNotification(error.message || 'Não foi possível salvar a regra.', 'error');
  }
}

async function exportarArquivo(path, fallbackName) {
  try {
    await apiDownload(path, fallbackName);
    showNotification('Download iniciado.', 'success');
  } catch (error) {
    showNotification(error.message || 'Falha ao exportar o arquivo.', 'error');
  }
}

function setupTabs() {
  tabs.forEach((tab) => {
    tab.addEventListener('click', () => activateTab(tab.dataset.tab));
  });
}

function setupActions() {
  document.getElementById('theme-toggle')?.addEventListener('click', (e) => {
    e.preventDefault();
    toggleTheme();
    syncDarkToggle();
  });

  darkToggle?.addEventListener('change', () => {
    applyTheme(Boolean(darkToggle.checked));
  });

  document.getElementById('btn-salvar-geral')?.addEventListener('click', salvarPreferenciasGerais);
  document.getElementById('btn-salvar-alerta')?.addEventListener('click', salvarRegraAlerta);

  document.getElementById('btn-export-inventario')?.addEventListener('click', () => {
    exportarArquivo('/exportar/itens', 'inventario.csv');
  });

  document.getElementById('btn-export-movimentacoes')?.addEventListener('click', () => {
    exportarArquivo('/exportar/movimentacoes', 'movimentacoes.csv');
  });
}

if (greeting && sessao?.nome) {
  greeting.textContent = `Olá, ${sessao.nome}`;
}

initSidebar();
initTheme();
syncDarkToggle();
setupTabs();
setupActions();
activateTab('geral');
carregarConfiguracoes();
