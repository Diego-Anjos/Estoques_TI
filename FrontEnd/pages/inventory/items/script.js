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
let itensCache = [];
let itemEditandoId = null;

const tbody = document.getElementById('itens-tbody');
const modal = document.getElementById('modal-item');
const form = document.getElementById('item-form');
const modalTitle = document.getElementById('modal-item-title');
const itemIdInput = document.getElementById('item-id');
const nomeInput = document.getElementById('nome-item');
const tipoSelect = document.getElementById('tipo-item');
const descricaoInput = document.getElementById('descricao-item');
const quantidadeInput = document.getElementById('quantidade-item');
const unidadeSelect = document.getElementById('unidade-item');
const localSelect = document.getElementById('local-item');
const statusSelect = document.getElementById('status-item');
const filtroNome = document.getElementById('nome-item-input');
const filtroTipo = document.getElementById('tipo-item-select');
const filtroStatus = document.getElementById('status-item-select');
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
  return normalized.includes('inativ') ? 'inativo' : 'ativo';
}

function itensFiltrados() {
  const nome = (filtroNome?.value || '').trim().toLowerCase();
  const tipo = (filtroTipo?.value || '').trim().toLowerCase();
  const status = (filtroStatus?.value || '').trim().toLowerCase();

  return itensCache.filter((item) => {
    const okNome = !nome || String(item.nome || '').toLowerCase().includes(nome);
    const okTipo = !tipo || String(item.tipo || '').toLowerCase() === tipo;
    const okStatus = !status || String(item.status || '').toLowerCase() === status;
    return okNome && okTipo && okStatus;
  });
}

function renderizarTabela(lista = itensFiltrados()) {
  if (!tbody) return;

  if (!lista.length) {
    tbody.innerHTML = `
      <tr>
        <td colspan="9" style="text-align:center;padding:1.5rem;color:#6b7280;">
          Nenhum item encontrado.
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = lista
    .map((item) => {
      const status = item.status || 'Ativo';
      return `
        <tr data-id="${item.id_item}">
          <td class="id-col">${escapeHtml(item.id_item)}</td>
          <td class="name-col">${escapeHtml(item.nome)}</td>
          <td class="type-col">${escapeHtml(item.tipo || '—')}</td>
          <td class="description-col">${escapeHtml(item.descricao || '—')}</td>
          <td class="quantity-col">${escapeHtml(item.quantidade ?? 0)}</td>
          <td class="unit-col">${escapeHtml(item.unidade || 'UN')}</td>
          <td class="location-col">${escapeHtml(item.nome_local || '—')}</td>
          <td class="status-col">
            <span class="status ${statusClass(status)}">${escapeHtml(status)}</span>
          </td>
          <td class="actions-col">
            <div class="action-buttons">
              <button type="button" class="btn-edit" data-action="edit" data-id="${item.id_item}" title="Editar">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
              <button type="button" class="btn-delete" data-action="delete" data-id="${item.id_item}" title="Excluir">
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

async function carregarOpcoesLocais() {
  if (!localSelect) return;

  try {
    const locais = await api.get('/locais/');
    const lista = Array.isArray(locais) ? locais : [];

    localSelect.innerHTML = '<option value="">Selecione um local</option>';
    lista.forEach((local) => {
      const option = document.createElement('option');
      option.value = String(local.id_local);
      const setor = local.setor ? ` (${local.setor})` : '';
      option.textContent = `${local.nome}${setor}`;
      localSelect.appendChild(option);
    });

    if (!lista.length) {
      showNotification('Cadastre um local antes de adicionar itens.', 'warning');
    }
  } catch (error) {
    showNotification(error.message || 'Não foi possível carregar os locais.', 'error');
  }
}

async function carregarItens() {
  try {
    const data = await api.get('/itens/');
    itensCache = Array.isArray(data) ? data : [];
    renderizarTabela();
  } catch (error) {
    showNotification(error.message || 'Não foi possível carregar os itens.', 'error');
    itensCache = [];
    renderizarTabela([]);
  }
}

function abrirModal(item = null) {
  itemEditandoId = item?.id_item ?? null;
  if (itemIdInput) itemIdInput.value = itemEditandoId ?? '';

  if (modalTitle) {
    modalTitle.textContent = item ? 'Editar Item' : 'Adicionar Item';
  }

  if (nomeInput) nomeInput.value = item?.nome || '';
  if (tipoSelect) tipoSelect.value = item?.tipo || '';
  if (descricaoInput) descricaoInput.value = item?.descricao || '';
  if (quantidadeInput) quantidadeInput.value = item?.quantidade ?? 0;
  if (unidadeSelect) unidadeSelect.value = item?.unidade || '';
  if (localSelect) localSelect.value = item?.id_local != null ? String(item.id_local) : '';
  if (statusSelect) statusSelect.value = item?.status || 'Ativo';

  modal?.classList.add('active');
  nomeInput?.focus();
}

function fecharModal() {
  modal?.classList.remove('active');
  itemEditandoId = null;
  form?.reset();
  if (itemIdInput) itemIdInput.value = '';
  if (quantidadeInput) quantidadeInput.value = '0';
  if (statusSelect) statusSelect.value = 'Ativo';
}

async function salvarItem(event) {
  event.preventDefault();

  const nome = (nomeInput?.value || '').trim();
  const tipo = (tipoSelect?.value || '').trim();
  const descricao = (descricaoInput?.value || '').trim();
  const quantidade = Number(quantidadeInput?.value ?? 0);
  const unidade = (unidadeSelect?.value || '').trim();
  const idLocal = Number(localSelect?.value || 0);
  const status = statusSelect?.value || 'Ativo';

  if (nome.length < 2) {
    showNotification('Informe um nome com pelo menos 2 caracteres.', 'warning');
    return;
  }
  if (!tipo) {
    showNotification('Selecione um tipo.', 'warning');
    return;
  }
  if (!unidade) {
    showNotification('Selecione uma unidade.', 'warning');
    return;
  }
  if (!idLocal) {
    showNotification('Selecione um local.', 'warning');
    return;
  }
  if (Number.isNaN(quantidade) || quantidade < 0) {
    showNotification('Informe uma quantidade válida (>= 0).', 'warning');
    return;
  }

  const payload = {
    nome,
    tipo,
    descricao: descricao || null,
    quantidade,
    unidade,
    id_local: idLocal,
    status,
  };

  try {
    if (itemEditandoId) {
      await api.put(`/itens/${itemEditandoId}`, payload);
      showNotification('Item atualizado com sucesso!', 'success');
    } else {
      await api.post('/itens/', payload);
      showNotification('Item cadastrado com sucesso!', 'success');
    }
    fecharModal();
    await carregarItens();
  } catch (error) {
    showNotification(error.message || 'Não foi possível salvar o item.', 'error');
  }
}

function confirmarExclusao(id) {
  const item = itensCache.find((row) => Number(row.id_item) === Number(id));
  const nome = item?.nome ? `"${item.nome}"` : 'este item';

  showConfirmModal(
    'Excluir item',
    `Tem certeza que deseja excluir ${nome}? Esta ação não poderá ser desfeita.`,
    async () => {
      try {
        await api.delete(`/itens/${id}`);
        showNotification('Item excluído com sucesso!', 'success');
        await carregarItens();
      } catch (error) {
        showNotification(error.message || 'Não foi possível excluir o item.', 'error');
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

  document.getElementById('btn-adicionar-item')?.addEventListener('click', async (e) => {
    e.preventDefault();
    await carregarOpcoesLocais();
    abrirModal();
  });

  document.getElementById('btn-voltar-dashboard-itens')?.addEventListener('click', (e) => {
    e.preventDefault();
    window.location.href = DASHBOARD_URL;
  });

  document.getElementById('btn-cancelar-item')?.addEventListener('click', fecharModal);
  document.getElementById('close-item')?.addEventListener('click', fecharModal);

  modal?.addEventListener('click', (e) => {
    if (e.target === modal) fecharModal();
  });

  form?.addEventListener('submit', salvarItem);

  document.getElementById('btn-buscar-itens')?.addEventListener('click', (e) => {
    e.preventDefault();
    renderizarTabela();
  });

  document.getElementById('btn-limpar-itens')?.addEventListener('click', (e) => {
    e.preventDefault();
    if (filtroNome) filtroNome.value = '';
    if (filtroTipo) filtroTipo.value = '';
    if (filtroStatus) filtroStatus.value = '';
    renderizarTabela();
  });

  tbody?.addEventListener('click', async (e) => {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;

    const id = Number(btn.dataset.id);
    if (!id) return;

    if (btn.dataset.action === 'edit') {
      const item = itensCache.find((row) => Number(row.id_item) === id);
      if (!item) return;
      await carregarOpcoesLocais();
      abrirModal(item);
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
carregarOpcoesLocais();
carregarItens();

export { carregarItens, carregarOpcoesLocais };
