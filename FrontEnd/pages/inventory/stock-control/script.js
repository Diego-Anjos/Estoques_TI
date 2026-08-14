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
let movimentacoesCache = [];
let itensCache = [];

const tbody = document.getElementById('movimentos-tbody');
const saldoBody = document.getElementById('saldo-body');
const saldoVazio = document.getElementById('saldo-vazio');
const saldoTabela = document.getElementById('saldo-tabela');
const modal = document.getElementById('modal-movimento');
const form = document.getElementById('movimento-form');
const itemSelect = document.getElementById('item-select');
const tipoSelect = document.getElementById('tipo');
const quantidadeInput = document.getElementById('quantidade');
const observacaoInput = document.getElementById('observacao');
const filtroItem = document.getElementById('filtro-item');
const filtroTipo = document.getElementById('filtro-tipo');
const greeting = document.getElementById('user-greeting');

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function formatarDataHora(valor) {
  if (!valor) return '—';
  const date = new Date(valor);
  if (Number.isNaN(date.getTime())) return '—';
  return date.toLocaleString('pt-BR');
}

function labelTipo(tipo) {
  const t = String(tipo || '').toUpperCase();
  if (t === 'ENTRADA') return 'Entrada';
  if (t === 'SAIDA') return 'Saída';
  return tipo || '—';
}

function movimentacoesFiltradas() {
  const nome = (filtroItem?.value || '').trim().toLowerCase();
  const tipo = (filtroTipo?.value || '').trim().toUpperCase();

  return movimentacoesCache.filter((mov) => {
    const okNome = !nome || String(mov.nome_item || '').toLowerCase().includes(nome);
    const okTipo = !tipo || String(mov.tipo_movimentacao || '').toUpperCase() === tipo;
    return okNome && okTipo;
  });
}

function renderizarSaldo() {
  if (!saldoBody || !saldoTabela || !saldoVazio) return;

  if (!itensCache.length) {
    saldoVazio.classList.remove('hidden');
    saldoVazio.textContent = 'Nenhum item registrado.';
    saldoTabela.classList.add('hidden');
    saldoBody.innerHTML = '';
    return;
  }

  saldoVazio.classList.add('hidden');
  saldoTabela.classList.remove('hidden');
  saldoBody.innerHTML = itensCache
    .map(
      (item) => `
      <tr>
        <td>${escapeHtml(item.nome)}</td>
        <td>${escapeHtml(item.unidade || 'UN')}</td>
        <td>${escapeHtml(item.quantidade ?? 0)}</td>
        <td>${escapeHtml(item.nome_local || '—')}</td>
      </tr>
    `
    )
    .join('');
}

function renderizarHistorico(lista = movimentacoesFiltradas()) {
  if (!tbody) return;

  if (!lista.length) {
    tbody.innerHTML = `
      <tr>
        <td colspan="5" style="text-align:center;padding:1.5rem;color:#6b7280;">
          Nenhuma movimentação encontrada.
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = lista
    .map((mov) => {
      const tipo = String(mov.tipo_movimentacao || '').toUpperCase();
      const tipoClass = tipo === 'ENTRADA' ? 'entrada' : 'saida';
      return `
        <tr>
          <td>${escapeHtml(formatarDataHora(mov.data_movimentacao))}</td>
          <td>${escapeHtml(mov.nome_item || '—')}</td>
          <td><span class="tipo-badge ${tipoClass}">${escapeHtml(labelTipo(tipo))}</span></td>
          <td>${escapeHtml(mov.quantidade)}</td>
          <td>${escapeHtml(mov.observacao || '—')}</td>
        </tr>
      `;
    })
    .join('');
}

async function carregarOpcoesItens() {
  if (!itemSelect) return;

  try {
    const itens = await api.get('/itens/');
    itensCache = Array.isArray(itens) ? itens : [];

    itemSelect.innerHTML = '<option value="">Selecione um item</option>';
    itensCache.forEach((item) => {
      const option = document.createElement('option');
      option.value = String(item.id_item);
      option.textContent = `${item.nome} (Estoque: ${item.quantidade ?? 0})`;
      itemSelect.appendChild(option);
    });

    renderizarSaldo();

    if (!itensCache.length) {
      showNotification('Cadastre itens antes de registrar movimentações.', 'warning');
    }
  } catch (error) {
    showNotification(error.message || 'Não foi possível carregar os itens.', 'error');
  }
}

async function carregarMovimentacoes() {
  try {
    const data = await api.get('/movimentacoes/');
    movimentacoesCache = Array.isArray(data) ? data : [];
    renderizarHistorico();
  } catch (error) {
    showNotification(error.message || 'Não foi possível carregar o histórico.', 'error');
    movimentacoesCache = [];
    renderizarHistorico([]);
  }
}

function abrirModal() {
  form?.reset();
  modal?.classList.add('active');
  itemSelect?.focus();
}

function fecharModal() {
  modal?.classList.remove('active');
  form?.reset();
}

async function salvarMovimentacao(event) {
  event.preventDefault();

  const idItem = Number(itemSelect?.value || 0);
  const tipo = (tipoSelect?.value || '').trim();
  const quantidade = Number(quantidadeInput?.value || 0);
  const observacao = (observacaoInput?.value || '').trim();

  if (!idItem) {
    showNotification('Selecione um item.', 'warning');
    return;
  }
  if (!tipo) {
    showNotification('Selecione o tipo de movimentação.', 'warning');
    return;
  }
  if (!quantidade || quantidade < 1) {
    showNotification('Informe uma quantidade válida (>= 1).', 'warning');
    return;
  }

  const payload = {
    id_item: idItem,
    tipo_movimentacao: tipo,
    quantidade,
    observacao: observacao || null,
    usuario_id: sessao?.id_usuario || null,
  };

  try {
    const result = await api.post('/movimentacoes/', payload);
    const qtdAtual = result?.quantidade_atual;
    const msg =
      qtdAtual != null
        ? `Movimentação registrada! Estoque atual: ${qtdAtual}.`
        : 'Movimentação registrada com sucesso!';
    showNotification(msg, 'success');
    fecharModal();
    await Promise.all([carregarMovimentacoes(), carregarOpcoesItens()]);
  } catch (error) {
    showNotification(error.message || 'Não foi possível registrar a movimentação.', 'error');
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

function setupEventListeners() {
  if (greeting && sessao?.nome) {
    greeting.textContent = `Olá, ${sessao.nome}`;
  }

  document.getElementById('btn-adicionar-movimento')?.addEventListener('click', async (e) => {
    e.preventDefault();
    await carregarOpcoesItens();
    abrirModal();
  });

  document.getElementById('btn-voltar-dashboard-estoque')?.addEventListener('click', (e) => {
    e.preventDefault();
    window.location.href = DASHBOARD_URL;
  });

  document.getElementById('btn-cancelar-movimento')?.addEventListener('click', fecharModal);
  document.getElementById('close-movimento')?.addEventListener('click', fecharModal);

  modal?.addEventListener('click', (e) => {
    if (e.target === modal) fecharModal();
  });

  form?.addEventListener('submit', salvarMovimentacao);

  document.getElementById('btn-buscar-estoque')?.addEventListener('click', (e) => {
    e.preventDefault();
    renderizarHistorico();
  });

  document.getElementById('btn-limpar-estoque')?.addEventListener('click', (e) => {
    e.preventDefault();
    if (filtroItem) filtroItem.value = '';
    if (filtroTipo) filtroTipo.value = '';
    renderizarHistorico();
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
Promise.all([carregarOpcoesItens(), carregarMovimentacoes()]);

export { carregarMovimentacoes, carregarOpcoesItens };
