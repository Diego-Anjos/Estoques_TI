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
const setorDestinoInput = document.getElementById('setor-destino');
const grupoSetorDestino = document.getElementById('grupo-setor-destino');
const setorOrigemInput = document.getElementById('setor-origem');
const grupoSetorOrigem = document.getElementById('grupo-setor-origem');
const filtroItem = document.getElementById('filtro-item');
const filtroTipo = document.getElementById('filtro-tipo');
const greeting = document.getElementById('user-greeting');

function normalizarTipoUi(tipo) {
  return String(tipo || '')
    .trim()
    .toUpperCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '');
}

function ehSaida(tipo) {
  const t = normalizarTipoUi(tipo);
  return t === 'SAIDA' || t === 'S' || t.startsWith('SAID');
}

function ehDevolucao(tipo) {
  const t = normalizarTipoUi(tipo);
  return t === 'DEVOLUCAO' || t === 'D' || t.startsWith('DEVOL');
}

function atualizarCamposSetor() {
  const saida = ehSaida(tipoSelect?.value);
  const devolucao = ehDevolucao(tipoSelect?.value);

  if (grupoSetorDestino) {
    if (saida) {
      grupoSetorDestino.classList.remove('hidden');
    } else {
      grupoSetorDestino.classList.add('hidden');
      if (setorDestinoInput) setorDestinoInput.value = '';
    }
  }

  if (grupoSetorOrigem) {
    if (devolucao) {
      grupoSetorOrigem.classList.remove('hidden');
    } else {
      grupoSetorOrigem.classList.add('hidden');
      if (setorOrigemInput) setorOrigemInput.value = '';
    }
  }
}

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
  if (t === 'DEVOLUCAO') return 'Devolução';
  return tipo || '—';
}

function classeTipoBadge(tipo) {
  const t = String(tipo || '').toUpperCase();
  if (t === 'ENTRADA') return 'entrada';
  if (t === 'SAIDA') return 'saida';
  if (t === 'DEVOLUCAO') return 'devolucao';
  return 'saida';
}

/** Texto da coluna Setor: destino (saída) ou origem (devolução). */
function textoSetorHistorico(mov) {
  const tipo = String(mov.tipo_movimentacao || '').toUpperCase();
  if (tipo === 'SAIDA' && mov.setor_destino) {
    return mov.setor_destino;
  }
  if (tipo === 'DEVOLUCAO' && mov.setor_origem) {
    return `De: ${mov.setor_origem}`;
  }
  return '—';
}

/** Query params esperados por GET /movimentacoes/ */
function filtrosAtuais() {
  const params = new URLSearchParams();
  const nome = (filtroItem?.value || '').trim();
  const tipo = (filtroTipo?.value || '').trim();

  if (nome) params.set('item', nome);
  if (tipo) params.set('tipo', tipo);

  return params;
}

function temFiltroAtivo() {
  return Boolean((filtroItem?.value || '').trim() || (filtroTipo?.value || '').trim());
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

function renderizarHistorico(lista = movimentacoesCache) {
  if (!tbody) return;

  if (!lista.length) {
    const mensagem = temFiltroAtivo()
      ? 'Nenhuma movimentação encontrada para os filtros aplicados.'
      : 'Nenhuma movimentação registrada. O saldo inicial informado no cadastro do item não gera movimentação — use o botão + para registrar uma entrada, saída ou devolução.';
    tbody.innerHTML = `
      <tr>
        <td colspan="6" style="text-align:center;padding:1.5rem;color:#6b7280;">
          ${mensagem}
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = lista
    .map((mov) => {
      const tipo = String(mov.tipo_movimentacao || '').toUpperCase();
      return `
        <tr>
          <td>${escapeHtml(formatarDataHora(mov.data_movimentacao))}</td>
          <td>${escapeHtml(mov.nome_item || '—')}</td>
          <td><span class="tipo-badge ${classeTipoBadge(tipo)}">${escapeHtml(labelTipo(tipo))}</span></td>
          <td>${escapeHtml(mov.quantidade)}</td>
          <td>${escapeHtml(textoSetorHistorico(mov))}</td>
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
  const query = filtrosAtuais().toString();

  try {
    const data = await api.get(`/movimentacoes/${query ? `?${query}` : ''}`);
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
  atualizarCamposSetor();
  modal?.classList.add('active');
  itemSelect?.focus();
}

function fecharModal() {
  modal?.classList.remove('active');
  form?.reset();
  atualizarCamposSetor();
}

async function salvarMovimentacao(event) {
  event.preventDefault();

  const idItem = Number(itemSelect?.value || 0);
  const tipo = (tipoSelect?.value || '').trim();
  const quantidade = Number(quantidadeInput?.value || 0);
  const observacao = (observacaoInput?.value || '').trim();
  const setorDestino = (setorDestinoInput?.value || '').trim();
  const setorOrigem = (setorOrigemInput?.value || '').trim();

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
    setor_destino: ehSaida(tipo) && setorDestino ? setorDestino : null,
    setor_origem: ehDevolucao(tipo) && setorOrigem ? setorOrigem : null,
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

  tipoSelect?.addEventListener('change', atualizarCamposSetor);

  document.getElementById('btn-buscar-estoque')?.addEventListener('click', async (e) => {
    e.preventDefault();
    await carregarMovimentacoes();
  });

  document.getElementById('btn-limpar-estoque')?.addEventListener('click', async (e) => {
    e.preventDefault();
    if (filtroItem) filtroItem.value = '';
    if (filtroTipo) filtroTipo.value = '';
    await carregarMovimentacoes();
  });

  filtroItem?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      carregarMovimentacoes();
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
Promise.all([carregarOpcoesItens(), carregarMovimentacoes()]);

export { carregarMovimentacoes, carregarOpcoesItens };
