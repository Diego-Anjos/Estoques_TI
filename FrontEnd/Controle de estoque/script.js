class ControleEstoqueManager {
    constructor() {
        this.storageKey = 'controle_estoque_movimentos';
        this.movimentos = JSON.parse(localStorage.getItem(this.storageKey)) || [];
        this.movimentoEditando = null;
        this.init();
    }

    init() {
        this.setupDropdown();
        this.setupModal();
        this.setupBotoes();
        this.setupFiltros();
        this.initTheme();
        this.render();
    }

    setupDropdown() {
        const themeToggle = document.getElementById('theme-toggle');
        const userDropdown = document.getElementById('user-dropdown');
        const userBtn = document.getElementById('user-btn');
        const perfilBtn = document.getElementById('perfil-btn');
        const configBtn = document.getElementById('config-btn');
        const sairBtn = document.getElementById('sair-btn');
        const logoutBtn = document.getElementById('logout-btn');

        if (themeToggle) themeToggle.addEventListener('click', () => this.toggleTheme());
        if (userBtn && userDropdown) {
            userBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                userDropdown.classList.toggle('active');
            });
            document.addEventListener('click', (e) => {
                if (!userDropdown.contains(e.target)) userDropdown.classList.remove('active');
            });
        }
        if (perfilBtn) perfilBtn.addEventListener('click', (e) => {
            e.preventDefault();
            this.showToast('Funcionalidade de Perfil em desenvolvimento', 'info');
        });
        if (configBtn) configBtn.addEventListener('click', (e) => {
            e.preventDefault();
            this.showToast('Funcionalidade de Configuracoes em desenvolvimento', 'info');
        });
        if (sairBtn) sairBtn.addEventListener('click', (e) => {
            e.preventDefault();
            if (confirm('Deseja sair do sistema?')) window.location.href = '../tela2entrar/index.html';
        });
        if (logoutBtn) logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            if (confirm('Deseja realmente sair do sistema?')) window.location.href = '../tela2entrar/index.html';
        });
    }

    setupModal() {
        const modal = document.getElementById('modal-movimento');
        const form = document.getElementById('movimento-form');
        const close = document.getElementById('close-movimento');
        const cancelar = document.getElementById('btn-cancelar-movimento');

        if (close) close.addEventListener('click', () => this.fecharModal());
        if (cancelar) cancelar.addEventListener('click', () => this.fecharModal());
        if (modal) modal.addEventListener('click', (e) => {
            if (e.target === modal) this.fecharModal();
        });
        if (form) form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.salvarMovimento();
        });
    }

    setupBotoes() {
        const btnVoltar = document.getElementById('btn-voltar-dashboard-estoque');
        const btnAdicionar = document.getElementById('btn-adicionar-movimento');
        const btnBuscar = document.getElementById('btn-buscar-estoque');
        const btnLimpar = document.getElementById('btn-limpar-estoque');
        const btnFiltroAvancado = document.getElementById('btn-filtro-avancado-estoque');

        if (btnVoltar) btnVoltar.addEventListener('click', () => {
            window.location.href = '../tela1/paginainicial/index.html';
        });
        if (btnAdicionar) btnAdicionar.addEventListener('click', () => this.abrirModal());
        if (btnBuscar) btnBuscar.addEventListener('click', () => {
            this.aplicarFiltros();
            this.showToast('Filtros aplicados!', 'info');
        });
        if (btnLimpar) btnLimpar.addEventListener('click', () => this.limparFiltros());
        if (btnFiltroAvancado) btnFiltroAvancado.addEventListener('click', () => {
            this.showToast('Filtro avancado em desenvolvimento', 'info');
        });
    }

    setupFiltros() {
        const nomeInput = document.getElementById('filtro-item');
        const tipoSelect = document.getElementById('filtro-tipo');
        if (nomeInput) nomeInput.addEventListener('input', () => this.aplicarFiltros());
        if (tipoSelect) tipoSelect.addEventListener('change', () => this.aplicarFiltros());
    }

    abrirModal(movimento = null) {
        const modal = document.getElementById('modal-movimento');
        const title = document.getElementById('modal-movimento-title');
        const form = document.getElementById('movimento-form');
        this.movimentoEditando = movimento;

        if (movimento) {
            title.textContent = 'Editar Movimento';
            document.getElementById('item').value = movimento.item;
            document.getElementById('tipo').value = movimento.tipo;
            document.getElementById('quantidade').value = movimento.quantidade;
            document.getElementById('observacao').value = movimento.observacao || '';
        } else {
            title.textContent = 'Adicionar Movimento';
            form.reset();
        }
        modal.classList.add('active');
    }

    fecharModal() {
        document.getElementById('modal-movimento').classList.remove('active');
        this.movimentoEditando = null;
    }

    salvarMovimento() {
        const item = document.getElementById('item').value.trim();
        const tipo = document.getElementById('tipo').value;
        const quantidade = parseInt(document.getElementById('quantidade').value, 10);
        const observacao = document.getElementById('observacao').value.trim();

        if (!item || !tipo || !Number.isInteger(quantidade) || quantidade <= 0) {
            this.showToast('Preencha os campos corretamente.', 'warning');
            return;
        }

        const agora = new Date().toISOString();
        if (this.movimentoEditando) {
            const idx = this.movimentos.findIndex((m) => m.id === this.movimentoEditando.id);
            this.movimentos[idx] = { ...this.movimentoEditando, item, tipo, quantidade, observacao };
            this.showToast('Movimento atualizado com sucesso!', 'success');
        } else {
            this.movimentos.push({ id: crypto.randomUUID(), item, tipo, quantidade, observacao, data: agora });
            this.showToast('Movimento adicionado com sucesso!', 'success');
        }

        this.persistir();
        this.fecharModal();
        this.render();
    }

    persistir() {
        localStorage.setItem(this.storageKey, JSON.stringify(this.movimentos));
    }

    aplicarFiltros() {
        const nome = (document.getElementById('filtro-item')?.value || '').toLowerCase();
        const tipo = document.getElementById('filtro-tipo')?.value || '';
        let filtrados = [...this.movimentos];
        if (nome) filtrados = filtrados.filter((m) => m.item.toLowerCase().includes(nome));
        if (tipo) filtrados = filtrados.filter((m) => m.tipo === tipo);
        this.renderMovimentos(filtrados);
    }

    limparFiltros() {
        const nome = document.getElementById('filtro-item');
        const tipo = document.getElementById('filtro-tipo');
        if (nome) nome.value = '';
        if (tipo) tipo.value = '';
        this.render();
        this.showToast('Filtros limpos!', 'info');
    }

    calcularSaldos() {
        const saldos = {};
        this.movimentos.forEach((mov) => {
            if (!saldos[mov.item]) saldos[mov.item] = 0;
            saldos[mov.item] += mov.tipo === 'entrada' ? mov.quantidade : -mov.quantidade;
        });
        return saldos;
    }

    renderSaldo() {
        const saldoTabela = document.getElementById('saldo-tabela');
        const saldoVazio = document.getElementById('saldo-vazio');
        const saldoBody = document.getElementById('saldo-body');
        const saldos = this.calcularSaldos();
        const linhas = Object.entries(saldos).sort((a, b) => a[0].localeCompare(b[0]));

        saldoBody.innerHTML = '';
        if (linhas.length === 0) {
            saldoTabela.classList.add('hidden');
            saldoVazio.classList.remove('hidden');
            return;
        }

        saldoTabela.classList.remove('hidden');
        saldoVazio.classList.add('hidden');
        linhas.forEach(([item, saldo]) => {
            const row = document.createElement('tr');
            const cItem = document.createElement('td');
            const cSaldo = document.createElement('td');
            cItem.textContent = item;
            cSaldo.textContent = String(saldo);
            cSaldo.className = saldo >= 0 ? 'saldo-positivo' : 'saldo-negativo';
            row.appendChild(cItem);
            row.appendChild(cSaldo);
            saldoBody.appendChild(row);
        });
    }

    renderMovimentos(movimentos = null) {
        const tbody = document.getElementById('movimentos-tbody');
        const dados = movimentos || [...this.movimentos].sort((a, b) => new Date(b.data) - new Date(a.data));
        tbody.innerHTML = '';

        dados.forEach((mov) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${new Date(mov.data).toLocaleString('pt-BR')}</td>
                <td>${mov.item}</td>
                <td><span class="badge ${mov.tipo}">${mov.tipo === 'entrada' ? 'Entrada' : 'Saida'}</span></td>
                <td>${mov.quantidade}</td>
                <td>${mov.observacao || '-'}</td>
            `;
            tbody.appendChild(row);
        });
    }

    render() {
        this.renderSaldo();
        this.renderMovimentos();
    }

    initTheme() {
        const savedTheme = localStorage.getItem('theme');
        const body = document.body;
        const themeIcon = document.querySelector('.theme-icon');
        if (savedTheme === 'dark') {
            body.setAttribute('data-theme', 'dark');
            if (themeIcon) themeIcon.textContent = '◑';
        } else {
            body.removeAttribute('data-theme');
            if (themeIcon) themeIcon.textContent = '◐';
        }
    }

    toggleTheme() {
        const body = document.body;
        const themeIcon = document.querySelector('.theme-icon');
        if (body.getAttribute('data-theme') === 'dark') {
            body.removeAttribute('data-theme');
            if (themeIcon) themeIcon.textContent = '◐';
            localStorage.setItem('theme', 'light');
        } else {
            body.setAttribute('data-theme', 'dark');
            if (themeIcon) themeIcon.textContent = '◑';
            localStorage.setItem('theme', 'dark');
        }
    }

    showToast(message, type = 'info') {
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `<div>${icons[type] || icons.info}</div><div>${message}</div><button class="toast-close">&times;</button>`;
        container.appendChild(toast);
        toast.querySelector('.toast-close').addEventListener('click', () => toast.remove());
        setTimeout(() => toast.remove(), 4000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.controleEstoque = new ControleEstoqueManager();
});
