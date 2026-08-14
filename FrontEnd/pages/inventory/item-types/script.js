import { api } from '../../../shared/js/api.js';
import { getSession, isAuthenticated, clearSession } from '../../../shared/js/auth.js';
import { showNotification } from '../../../shared/js/notify.js';
import { showConfirmModal } from '../../../shared/js/confirmModal.js';

const LOGIN_URL = '../../auth/login/index.html';
const DASHBOARD_URL = '../../auth/dashboard/paginainicial/index.html';

if (!isAuthenticated()) {
  window.location.replace(LOGIN_URL);
  throw new Error('Sessão não encontrada');
}

const sessao = getSession();
let tiposCache = [];
let tipoEditandoId = null;

const tbody = document.getElementById('tipos-tbody');
const modal = document.getElementById('modal-tipo');
const form = document.getElementById('tipo-form');
const modalTitle = document.getElementById('modal-tipo-title');
const tipoIdInput = document.getElementById('tipo-id');
const nomeInput = document.getElementById('nome-tipo');
const descricaoInput = document.getElementById('descricao-tipo');
const statusSelect = document.getElementById('status-tipo');
const filtroNome = document.getElementById('nome-tipo-input');
const filtroCategoria = document.getElementById('categoria-tipo-select');
const filtroStatus = document.getElementById('status-tipo-filtro');
const greeting = document.getElementById('user-greeting');

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function formatarData(valor) {
  if (!valor) return '—';
  const date = new Date(valor);
  if (Number.isNaN(date.getTime())) return '—';
  return date.toLocaleDateString('pt-BR');
}

function statusClass(status) {
  const normalized = String(status || 'Ativo').toLowerCase();
  return normalized.includes('inativ') ? 'inativo' : 'ativo';
}

function atualizarFiltroCategorias() {
  if (!filtroCategoria) return;

  const selecionado = filtroCategoria.value;
  const nomes = [...new Set(
    tiposCache
      .map((tipo) => String(tipo.nome || '').trim())
      .filter(Boolean)
  )].sort((a, b) => a.localeCompare(b, 'pt-BR'));

  filtroCategoria.innerHTML = '<option value="">Todas as categorias</option>';
  nomes.forEach((nome) => {
    const option = document.createElement('option');
    option.value = nome;
    option.textContent = nome;
    filtroCategoria.appendChild(option);
  });

  if (selecionado && nomes.includes(selecionado)) {
    filtroCategoria.value = selecionado;
  }
}

function tiposFiltrados() {
  const nome = (filtroNome?.value || '').trim().toLowerCase();
  const categoria = (filtroCategoria?.value || '').trim().toLowerCase();

  return tiposCache.filter((tipo) => {
    const nomeTipo = String(tipo.nome || '').toLowerCase();
    const okNome = !nome || nomeTipo.includes(nome);
    const okCategoria = !categoria || nomeTipo === categoria;
    return okNome && okCategoria;
  });
}

function toggleFiltroAvancado() {
  const btn = document.getElementById('btn-filtro-avancado-tipos');
  const panel = document.getElementById('filtro-avancado-tipos-panel');
  if (!panel) return;

  const abrir = panel.hasAttribute('hidden');
  if (abrir) {
    panel.removeAttribute('hidden');
    btn?.classList.add('open');
    btn?.setAttribute('aria-expanded', 'true');
  } else {
    panel.setAttribute('hidden', '');
    btn?.classList.remove('open');
    btn?.setAttribute('aria-expanded', 'false');
  }
}

function renderizarTabela(lista = tiposFiltrados()) {
  if (!tbody) return;

  if (!lista.length) {
    tbody.innerHTML = `
      <tr>
        <td colspan="7" style="text-align:center;padding:1.5rem;color:#6b7280;">
          Nenhum tipo de item encontrado.
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = lista
    .map((tipo) => {
      const status = tipo.status || 'Ativo';
      return `
        <tr data-id="${tipo.id_tipo_item}">
          <td class="id-col">${escapeHtml(tipo.id_tipo_item)}</td>
          <td class="name-col">${escapeHtml(tipo.nome)}</td>
          <td class="description-col">${escapeHtml(tipo.descricao || '—')}</td>
          <td class="status-col">
            <span class="status ${statusClass(status)}">${escapeHtml(status)}</span>
          </td>
          <td class="date-creation-col">${escapeHtml(formatarData(tipo.data_criacao))}</td>
          <td class="created-by-col">${escapeHtml(tipo.nome_criado_por || '—')}</td>
          <td class="actions-col">
            <div class="action-buttons">
              <button type="button" class="btn-edit" data-action="edit" data-id="${tipo.id_tipo_item}" title="Editar">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
              <button type="button" class="btn-delete" data-action="delete" data-id="${tipo.id_tipo_item}" title="Inativar">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <polyline points="3,6 5,6 21,6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
            </div>
          </td>
        </tr>
      `;
    })
    .join('');
}

async function carregarTipos() {
  try {
    const status = filtroStatus?.value || 'ativos';
    const data = await api.get(`/tipos-item/?status=${encodeURIComponent(status)}`);
    tiposCache = Array.isArray(data) ? data : [];
    atualizarFiltroCategorias();
    renderizarTabela();
  } catch (error) {
    showNotification(error.message || 'Não foi possível carregar os tipos.', 'error');
    tiposCache = [];
    atualizarFiltroCategorias();
    renderizarTabela([]);
  }
}

function abrirModal(tipo = null) {
  tipoEditandoId = tipo?.id_tipo_item ?? null;
  if (tipoIdInput) tipoIdInput.value = tipoEditandoId ?? '';

  if (modalTitle) {
    modalTitle.textContent = tipo ? 'Editar Tipo de Item' : 'Adicionar Tipo de Item';
  }

  if (nomeInput) nomeInput.value = tipo?.nome || '';
  if (descricaoInput) descricaoInput.value = tipo?.descricao || '';
  if (statusSelect) statusSelect.value = tipo?.status || 'Ativo';

  modal?.classList.add('active');
  nomeInput?.focus();
}

function fecharModal() {
  modal?.classList.remove('active');
  tipoEditandoId = null;
  form?.reset();
  if (tipoIdInput) tipoIdInput.value = '';
  if (statusSelect) statusSelect.value = 'Ativo';
}

async function salvarTipo(event) {
  event.preventDefault();

  const nome = (nomeInput?.value || '').trim();
  const descricao = (descricaoInput?.value || '').trim();
  const status = statusSelect?.value || 'Ativo';

  if (nome.length < 2) {
    showNotification('Informe um nome com pelo menos 2 caracteres.', 'warning');
    return;
  }

  const payload = {
    nome,
    descricao: descricao || null,
    status,
  };

  try {
    if (tipoEditandoId) {
      await api.put(`/tipos-item/${tipoEditandoId}`, payload);
      showNotification('Tipo atualizado com sucesso!', 'success');
    } else {
      await api.post('/tipos-item/', payload);
      showNotification('Tipo cadastrado com sucesso!', 'success');
    }
    fecharModal();
    await carregarTipos();
  } catch (error) {
    showNotification(error.message || 'Não foi possível salvar o tipo.', 'error');
  }
}

function confirmarExclusao(id) {
  const tipo = tiposCache.find((item) => Number(item.id_tipo_item) === Number(id));
  const nome = tipo?.nome ? `"${tipo.nome}"` : 'este tipo';

  showConfirmModal(
    'Inativar tipo de item',
    `Tem certeza que deseja inativar ${nome}? Ele deixará de aparecer na listagem padrão, mas poderá ser reativado depois.`,
    async () => {
      try {
        await api.delete(`/tipos-item/${id}`);
        showNotification('Tipo inativado com sucesso!', 'success');
        await carregarTipos();
      } catch (error) {
        showNotification(error.message || 'Não foi possível inativar o tipo.', 'error');
      }
    },
    { confirmText: 'Sim, inativar', cancelText: 'Cancelar', danger: true }
  );
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

function setupEventListeners() {
  if (greeting && sessao?.nome) {
    greeting.textContent = `Olá, ${sessao.nome}`;
  }

  document.getElementById('btn-adicionar-tipo')?.addEventListener('click', (e) => {
    e.preventDefault();
    abrirModal();
  });

  document.getElementById('btn-voltar-dashboard-tipos')?.addEventListener('click', (e) => {
    e.preventDefault();
    window.location.href = DASHBOARD_URL;
  });

  document.getElementById('btn-cancelar-tipo')?.addEventListener('click', fecharModal);
  document.getElementById('close-tipo')?.addEventListener('click', fecharModal);

  modal?.addEventListener('click', (e) => {
    if (e.target === modal) fecharModal();
  });

  form?.addEventListener('submit', salvarTipo);

  document.getElementById('btn-buscar-tipos')?.addEventListener('click', (e) => {
    e.preventDefault();
    renderizarTabela();
  });

  document.getElementById('btn-limpar-tipos')?.addEventListener('click', (e) => {
    e.preventDefault();
    if (filtroNome) filtroNome.value = '';
    if (filtroCategoria) filtroCategoria.value = '';
    if (filtroStatus) filtroStatus.value = 'ativos';
    carregarTipos();
  });

  document.getElementById('btn-filtro-avancado-tipos')?.addEventListener('click', (e) => {
    e.preventDefault();
    toggleFiltroAvancado();
  });

  filtroStatus?.addEventListener('change', () => {
    carregarTipos();
  });

  tbody?.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;

    const id = Number(btn.dataset.id);
    if (!id) return;

    if (btn.dataset.action === 'edit') {
      const tipo = tiposCache.find((item) => Number(item.id_tipo_item) === id);
      if (tipo) abrirModal(tipo);
      return;
    }

    if (btn.dataset.action === 'delete') {
      confirmarExclusao(id);
    }
  });

  document.getElementById('theme-toggle')?.addEventListener('click', (e) => {
    e.preventDefault();
    toggleTheme();
  });

  const userDropdown = document.getElementById('user-dropdown');
  const userBtn = document.getElementById('user-btn');

  userBtn?.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    userDropdown?.classList.toggle('active');
  });

  document.addEventListener('click', (e) => {
    if (userDropdown && !userDropdown.contains(e.target)) {
      userDropdown.classList.remove('active');
    }
  });

  const logout = (e) => {
    e.preventDefault();
    showConfirmModal('Sair do sistema', 'Deseja realmente sair?', () => {
      clearSession();
      window.location.href = LOGIN_URL;
    }, { confirmText: 'Sair', cancelText: 'Cancelar', danger: true });
  };

  document.getElementById('logout-btn')?.addEventListener('click', logout);
  document.getElementById('sair-btn')?.addEventListener('click', logout);
}

setupEventListeners();
initTheme();
carregarTipos();

export { carregarTipos };
