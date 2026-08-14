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
let locaisCache = [];
let localEditandoId = null;

const tbody = document.getElementById('locais-tbody');
const modal = document.getElementById('modal-local');
const form = document.getElementById('local-form');
const modalTitle = document.getElementById('modal-local-title');
const nomeInput = document.getElementById('nome-local');
const setorInput = document.getElementById('setor-local');
const descricaoInput = document.getElementById('descricao-local');
const statusSelect = document.getElementById('status-local');
const localIdInput = document.getElementById('local-id');
const filtroNome = document.getElementById('nome-input');
const filtroSetor = document.getElementById('setor-input');
const greeting = document.getElementById('user-greeting');

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function statusClass(status) {
  const normalized = String(status || 'Ativo').toLowerCase();
  if (normalized.includes('inativ')) return 'inativo';
  if (normalized.includes('manut')) return 'manutencao';
  return 'ativo';
}

function locaisFiltrados() {
  const nome = (filtroNome?.value || '').trim().toLowerCase();
  const setor = (filtroSetor?.value || '').trim().toLowerCase();

  return locaisCache.filter((local) => {
    const okNome = !nome || String(local.nome || '').toLowerCase().includes(nome);
    const okSetor = !setor || String(local.setor || '').toLowerCase().includes(setor);
    return okNome && okSetor;
  });
}

function renderizarTabela(lista = locaisFiltrados()) {
  if (!tbody) return;

  if (!lista.length) {
    tbody.innerHTML = `
      <tr>
        <td colspan="6" style="text-align:center;padding:1.5rem;color:#6b7280;">
          Nenhum local encontrado.
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = lista
    .map((local) => {
      const status = local.status || 'Ativo';
      return `
        <tr data-id="${local.id_local}">
          <td class="id-col">${escapeHtml(local.id_local)}</td>
          <td class="name-col">${escapeHtml(local.nome)}</td>
          <td class="setor-col">${escapeHtml(local.setor || '—')}</td>
          <td class="description-col">${escapeHtml(local.descricao || '—')}</td>
          <td class="status-col">
            <span class="status ${statusClass(status)}">${escapeHtml(status)}</span>
          </td>
          <td class="actions-col">
            <div class="action-buttons">
              <button type="button" class="btn-edit" data-action="edit" data-id="${local.id_local}" title="Editar">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
              <button type="button" class="btn-delete" data-action="delete" data-id="${local.id_local}" title="Excluir">
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

async function carregarLocais() {
  try {
    const data = await api.get('/locais/');
    locaisCache = Array.isArray(data) ? data : [];
    renderizarTabela();
  } catch (error) {
    showNotification(error.message || 'Não foi possível carregar os locais.', 'error');
    locaisCache = [];
    renderizarTabela([]);
  }
}

function abrirModal(local = null) {
  localEditandoId = local?.id_local ?? null;
  if (localIdInput) localIdInput.value = localEditandoId ?? '';

  if (modalTitle) {
    modalTitle.textContent = local ? 'Editar Local' : 'Adicionar Local';
  }

  if (nomeInput) nomeInput.value = local?.nome || '';
  if (setorInput) setorInput.value = local?.setor || '';
  if (descricaoInput) descricaoInput.value = local?.descricao || '';
  if (statusSelect) statusSelect.value = local?.status || 'Ativo';

  modal?.classList.add('active');
  nomeInput?.focus();
}

function fecharModal() {
  modal?.classList.remove('active');
  localEditandoId = null;
  form?.reset();
  if (localIdInput) localIdInput.value = '';
  if (statusSelect) statusSelect.value = 'Ativo';
}

async function salvarLocal(event) {
  event.preventDefault();

  const nome = (nomeInput?.value || '').trim();
  const setor = (setorInput?.value || '').trim();
  const descricao = (descricaoInput?.value || '').trim();
  const status = statusSelect?.value || 'Ativo';

  if (nome.length < 2) {
    showNotification('Informe um nome do local com pelo menos 2 caracteres.', 'warning');
    return;
  }

  const payload = {
    nome,
    setor: setor || null,
    descricao: descricao || null,
    status,
  };

  try {
    if (localEditandoId) {
      await api.put(`/locais/${localEditandoId}`, payload);
      showNotification('Local atualizado com sucesso!', 'success');
    } else {
      await api.post('/locais/', payload);
      showNotification('Local cadastrado com sucesso!', 'success');
    }
    fecharModal();
    await carregarLocais();
  } catch (error) {
    showNotification(error.message || 'Não foi possível salvar o local.', 'error');
  }
}

function confirmarExclusao(id) {
  const local = locaisCache.find((item) => Number(item.id_local) === Number(id));
  const nome = local?.nome ? `"${local.nome}"` : 'este local';

  showConfirmModal(
    'Excluir local',
    `Tem certeza que deseja excluir ${nome}? Esta ação não poderá ser desfeita.`,
    async () => {
      try {
        await api.delete(`/locais/${id}`);
        showNotification('Local excluído com sucesso!', 'success');
        await carregarLocais();
      } catch (error) {
        showNotification(error.message || 'Não foi possível excluir o local.', 'error');
      }
    },
    { confirmText: 'Sim, excluir', cancelText: 'Cancelar', danger: true }
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

  document.getElementById('btn-adicionar-local')?.addEventListener('click', (e) => {
    e.preventDefault();
    abrirModal();
  });

  document.getElementById('btn-voltar-dashboard')?.addEventListener('click', (e) => {
    e.preventDefault();
    window.location.href = DASHBOARD_URL;
  });

  document.getElementById('btn-cancelar-local')?.addEventListener('click', fecharModal);
  document.getElementById('close-local')?.addEventListener('click', fecharModal);

  modal?.addEventListener('click', (e) => {
    if (e.target === modal) fecharModal();
  });

  form?.addEventListener('submit', salvarLocal);

  document.getElementById('btn-buscar')?.addEventListener('click', (e) => {
    e.preventDefault();
    renderizarTabela();
  });

  document.getElementById('btn-limpar')?.addEventListener('click', (e) => {
    e.preventDefault();
    if (filtroNome) filtroNome.value = '';
    if (filtroSetor) filtroSetor.value = '';
    renderizarTabela();
  });

  filtroNome?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      renderizarTabela();
    }
  });

  filtroSetor?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      renderizarTabela();
    }
  });

  tbody?.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;

    const id = Number(btn.dataset.id);
    if (!id) return;

    if (btn.dataset.action === 'edit') {
      const local = locaisCache.find((item) => Number(item.id_local) === id);
      if (local) abrirModal(local);
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
carregarLocais();

export { carregarLocais };
