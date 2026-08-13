// Script específico para a página de Tipos de Item
class TiposItemManager {
    constructor() {
        this.tipos = JSON.parse(localStorage.getItem('tipos')) || [];
        this.tipoEditando = null;
        this.tipoExcluindo = null;
        this.usuarioLogado = 'Maria';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupModal();
        this.setupModalConfirmacao();
        this.initTheme();
        this.renderTipos();
        this.adicionarTiposExemplo();
    }

    setupEventListeners() {
        // Filtros
        const nomeInput = document.getElementById('nome-tipo-input');
        const categoriaSelect = document.getElementById('categoria-tipo-select');
        const btnBuscar = document.getElementById('btn-buscar-tipos');
        const btnLimpar = document.getElementById('btn-limpar-tipos');
        const btnFiltroAvancado = document.getElementById('btn-filtro-avancado-tipos');

        if (nomeInput) {
            nomeInput.addEventListener('input', () => this.aplicarFiltros());
        }
        if (categoriaSelect) {
            categoriaSelect.addEventListener('change', () => this.aplicarFiltros());
        }
        if (btnBuscar) {
            btnBuscar.addEventListener('click', (e) => {
                e.preventDefault();
                this.aplicarFiltros();
                this.showToast('Filtros aplicados!', 'success');
            });
        }
        if (btnLimpar) {
            btnLimpar.addEventListener('click', (e) => {
                e.preventDefault();
                this.limparFiltros();
            });
        }
        if (btnFiltroAvancado) {
            btnFiltroAvancado.addEventListener('click', (e) => {
                e.preventDefault();
                this.showToast('Filtro avançado em desenvolvimento', 'info');
            });
        }

        // Botão adicionar
        const btnAdicionar = document.getElementById('btn-adicionar-tipo');
        if (btnAdicionar) {
            btnAdicionar.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('Botão adicionar clicado');
                this.abrirModal();
            });
        }

        // Botão voltar ao dashboard
        const btnVoltar = document.getElementById('btn-voltar-dashboard-tipos');
        if (btnVoltar) {
            btnVoltar.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('Botão voltar clicado');
                window.location.href = '../tela1/paginainicial/index.html';
            });
        }

        // Botão logout no header
        const logoutBtn = document.getElementById('logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', (e) => {
                e.preventDefault();
                if (confirm('Deseja realmente sair do sistema?')) {
                    localStorage.removeItem('userSession');
                    window.location.href = '../tela2entrar/index.html';
                }
            });
        }

        // Setup dropdown do usuário
        this.setupDropdown();
    }

    setupModal() {
        const modal = document.getElementById('modal-tipo');
        const btnCancelar = document.getElementById('btn-cancelar-tipo');
        const closeBtn = document.getElementById('close-tipo');
        const form = document.getElementById('tipo-form');

        if (btnCancelar) {
            btnCancelar.addEventListener('click', () => this.fecharModal());
        }
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.fecharModal());
        }
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) this.fecharModal();
            });
        }
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.salvarTipo();
            });
        }
    }

    setupModalConfirmacao() {
        const modal = document.getElementById('modal-confirmacao-tipo');
        const btnCancelar = document.getElementById('btn-cancelar-exclusao-tipo');
        const btnConfirmar = document.getElementById('btn-confirmar-exclusao-tipo');

        if (btnCancelar) {
            btnCancelar.addEventListener('click', () => this.fecharModalConfirmacao());
        }
        if (btnConfirmar) {
            btnConfirmar.addEventListener('click', () => this.confirmarExclusao());
        }
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) this.fecharModalConfirmacao();
            });
        }
    }

    setupDropdown() {
        const themeToggle = document.getElementById('theme-toggle');
        const userDropdown = document.getElementById('user-dropdown');
        const userBtn = document.getElementById('user-btn');
        const sairBtn = document.getElementById('sair-btn');

        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }

        if (userBtn && userDropdown) {
            userBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                userDropdown.classList.toggle('active');
            });

            document.addEventListener('click', (e) => {
                if (!userDropdown.contains(e.target)) {
                    userDropdown.classList.remove('active');
                }
            });
        }

        if (sairBtn) {
            sairBtn.addEventListener('click', (e) => {
                e.preventDefault();
                if (confirm('Deseja realmente sair do sistema?')) {
                    // Limpar dados locais ao sair
                    localStorage.removeItem('userSession');
                    window.location.href = '../tela2entrar/index.html';
                }
            });
        }

        // Botão de voltar ao dashboard
        const btnVoltarDashboard = document.getElementById('btn-voltar-dashboard-tipos');
        if (btnVoltarDashboard) {
            btnVoltarDashboard.addEventListener('click', (e) => {
                e.preventDefault();
                window.location.href = '../tela1/paginainicial/index.html';
            });
        }
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
            themeIcon.textContent = '◐';
            localStorage.setItem('theme', 'light');
        } else {
            body.setAttribute('data-theme', 'dark');
            themeIcon.textContent = '◑';
            localStorage.setItem('theme', 'dark');
        }
    }

    renderTipos() {
        const tbody = document.getElementById('tipos-tbody');
        if (!tbody) return;

        if (this.tipos.length === 0) {
            this.adicionarTiposExemplo();
        }

        tbody.innerHTML = '';

        this.tipos.forEach(tipo => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="checkbox-col">
                    <input type="checkbox" class="tipo-checkbox" data-id="${tipo.id}">
                </td>
                <td class="id-col">${tipo.id}</td>
                <td class="name-col">${tipo.nome}</td>
                <td class="category-col">${this.getCategoriaText(tipo.categoria)}</td>
                <td class="description-col">${tipo.descricao || 'N/A'}</td>
                <td class="status-col">
                    <span class="status ${tipo.status.toLowerCase()}">${tipo.status}</span>
                </td>
                <td class="date-creation-col">${tipo.dataCriacao || 'N/A'}</td>
                <td class="created-by-col">${tipo.criadoPor || 'N/A'}</td>
                <td class="date-modification-col">${tipo.dataAlteracao || 'N/A'}</td>
                <td class="modified-by-col">${tipo.alteradoPor || 'N/A'}</td>
                <td class="actions-col">
                    <div class="actions">
                        <button class="btn-edit" onclick="tiposManager.abrirModal(${JSON.stringify(tipo).replace(/"/g, '&quot;')})" title="Editar">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="m18.5 2.5 a2.12 2.12 0 0 1 3 3l-9.5 9.5-4 1 1-4 9.5-9.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                        <button class="btn-delete" onclick="tiposManager.excluirTipo(${tipo.id})" title="Excluir">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6h14ZM10 11v6M14 11v6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                    </div>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    getCategoriaText(categoria) {
        const categoriaMap = {
            'material': 'Material',
            'equipamento': 'Equipamento',
            'consumivel': 'Consumível',
            'ferramenta': 'Ferramenta',
            'componente': 'Componente'
        };
        return categoriaMap[categoria] || categoria;
    }

    aplicarFiltros() {
        const nome = document.getElementById('nome-tipo-input')?.value.toLowerCase() || '';
        const categoria = document.getElementById('categoria-tipo-select')?.value || '';

        let tiposFiltrados = this.tipos;

        if (nome) {
            tiposFiltrados = tiposFiltrados.filter(tipo =>
                tipo.nome.toLowerCase().includes(nome)
            );
        }

        if (categoria) {
            tiposFiltrados = tiposFiltrados.filter(tipo =>
                tipo.categoria === categoria
            );
        }

        this.renderTiposFiltrados(tiposFiltrados);
    }

    renderTiposFiltrados(tipos) {
        const tbody = document.getElementById('tipos-tbody');
        if (!tbody) return;

        tbody.innerHTML = '';

        tipos.forEach(tipo => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="checkbox-col">
                    <input type="checkbox" class="tipo-checkbox" data-id="${tipo.id}">
                </td>
                <td class="id-col">${tipo.id}</td>
                <td class="name-col">${tipo.nome}</td>
                <td class="category-col">${this.getCategoriaText(tipo.categoria)}</td>
                <td class="description-col">${tipo.descricao || 'N/A'}</td>
                <td class="status-col">
                    <span class="status ${tipo.status.toLowerCase()}">${tipo.status}</span>
                </td>
                <td class="date-creation-col">${tipo.dataCriacao || 'N/A'}</td>
                <td class="created-by-col">${tipo.criadoPor || 'N/A'}</td>
                <td class="date-modification-col">${tipo.dataAlteracao || 'N/A'}</td>
                <td class="modified-by-col">${tipo.alteradoPor || 'N/A'}</td>
                <td class="actions-col">
                    <div class="actions">
                        <button class="btn-edit" onclick="tiposManager.abrirModal(${JSON.stringify(tipo).replace(/"/g, '&quot;')})" title="Editar">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="m18.5 2.5 a2.12 2.12 0 0 1 3 3l-9.5 9.5-4 1 1-4 9.5-9.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                        <button class="btn-delete" onclick="tiposManager.excluirTipo(${tipo.id})" title="Excluir">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6h14ZM10 11v6M14 11v6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                    </div>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    limparFiltros() {
        const nomeInput = document.getElementById('nome-tipo-input');
        const categoriaSelect = document.getElementById('categoria-tipo-select');

        if (nomeInput) nomeInput.value = '';
        if (categoriaSelect) categoriaSelect.value = '';

        this.renderTipos();
        this.showToast('Filtros limpos!', 'info');
    }

    abrirModal(tipo = null) {
        const modal = document.getElementById('modal-tipo');
        const modalTitle = document.getElementById('modal-tipo-title');
        const form = document.getElementById('tipo-form');
        
        this.tipoEditando = tipo;
        
        if (tipo) {
            modalTitle.textContent = 'Editar Tipo de Item';
            this.preencherForm(tipo);
        } else {
            modalTitle.textContent = 'Adicionar Tipo de Item';
            form.reset();
        }
        
        modal.classList.add('active');
    }

    fecharModal() {
        const modal = document.getElementById('modal-tipo');
        modal.classList.remove('active');
        this.tipoEditando = null;
    }

    preencherForm(tipo) {
        document.getElementById('nome-tipo').value = tipo.nome || '';
        document.getElementById('categoria-tipo').value = tipo.categoria || '';
        document.getElementById('descricao-tipo').value = tipo.descricao || '';
        document.getElementById('status-tipo').value = tipo.status || 'Ativo';
    }

    salvarTipo() {
        const nome = document.getElementById('nome-tipo').value;
        const categoria = document.getElementById('categoria-tipo').value;
        const descricao = document.getElementById('descricao-tipo').value;
        const status = document.getElementById('status-tipo').value;

        if (!nome.trim()) {
            this.showToast('O nome do tipo é obrigatório!', 'error');
            return;
        }

        if (!categoria) {
            this.showToast('A categoria é obrigatória!', 'error');
            return;
        }

        const agora = new Date().toLocaleString('pt-BR');
        
        let novoId;
        if (this.tipoEditando) {
            novoId = this.tipoEditando.id;
        } else {
            const maiorId = this.tipos.length > 0 ? Math.max(...this.tipos.map(t => t.id)) : 0;
            novoId = maiorId + 1;
        }

        const novoTipo = {
            id: novoId,
            nome: nome.trim(),
            categoria,
            descricao: descricao.trim(),
            status,
            dataCriacao: this.tipoEditando ? this.tipoEditando.dataCriacao : agora,
            criadoPor: this.tipoEditando ? this.tipoEditando.criadoPor : this.usuarioLogado,
            dataAlteracao: agora,
            alteradoPor: this.usuarioLogado
        };

        if (this.tipoEditando) {
            const index = this.tipos.findIndex(t => t.id === this.tipoEditando.id);
            this.tipos[index] = novoTipo;
            this.showToast('Tipo de item atualizado com sucesso!', 'success');
        } else {
            this.tipos.push(novoTipo);
            this.showToast('Tipo de item adicionado com sucesso!', 'success');
        }

        localStorage.setItem('tipos', JSON.stringify(this.tipos));
        this.renderTipos();
        this.fecharModal();
    }

    excluirTipo(id) {
        this.tipoExcluindo = id;
        const modal = document.getElementById('modal-confirmacao-tipo');
        modal.classList.add('active');
    }

    fecharModalConfirmacao() {
        const modal = document.getElementById('modal-confirmacao-tipo');
        modal.classList.remove('active');
        this.tipoExcluindo = null;
    }

    confirmarExclusao() {
        if (this.tipoExcluindo) {
            this.tipos = this.tipos.filter(t => t.id !== this.tipoExcluindo);
            localStorage.setItem('tipos', JSON.stringify(this.tipos));
            this.renderTipos();
            this.showToast('Tipo de item excluído com sucesso!', 'success');
        }
        this.fecharModalConfirmacao();
    }

    showToast(message, type = 'info') {
        let toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.className = 'toast-container';
            document.body.appendChild(toastContainer);
        }

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };

        toast.innerHTML = `
            <div class="toast-icon">${icons[type] || icons.info}</div>
            <div class="toast-content">
                <p>${message}</p>
            </div>
            <button class="toast-close">&times;</button>
        `;

        toastContainer.appendChild(toast);

        const closeBtn = toast.querySelector('.toast-close');
        closeBtn.addEventListener('click', () => {
            toast.remove();
        });

        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 5000);
    }

    adicionarTiposExemplo() {
        if (this.tipos.length > 0) return;

        const tiposExemplo = [
            {
                id: 1,
                nome: 'Material de Construção',
                categoria: 'material',
                descricao: 'Materiais diversos para construção civil',
                status: 'Ativo',
                dataCriacao: '15/01/2026, 08:00:00',
                criadoPor: 'Sistema',
                dataAlteracao: '15/01/2026, 08:00:00',
                alteradoPor: 'Sistema'
            },
            {
                id: 2,
                nome: 'Equipamento de Informática',
                categoria: 'equipamento',
                descricao: 'Equipamentos relacionados a informática',
                status: 'Ativo',
                dataCriacao: '18/01/2026, 10:30:00',
                criadoPor: 'Maria',
                dataAlteracao: '20/02/2026, 14:20:00',
                alteradoPor: 'Maria'
            },
            {
                id: 3,
                nome: 'Material de Escritório',
                categoria: 'consumivel',
                descricao: 'Materiais consumíveis de escritório',
                status: 'Ativo',
                dataCriacao: '22/01/2026, 16:45:00',
                criadoPor: 'Maria',
                dataAlteracao: '05/03/2026, 09:30:00',
                alteradoPor: 'Maria'
            },
            {
                id: 4,
                nome: 'Ferramentas Manuais',
                categoria: 'ferramenta',
                descricao: 'Ferramentas para uso manual',
                status: 'Ativo',
                dataCriacao: '25/01/2026, 11:15:00',
                criadoPor: 'Sistema',
                dataAlteracao: '25/01/2026, 11:15:00',
                alteradoPor: 'Sistema'
            },
            {
                id: 5,
                nome: 'Componente Eletrônico',
                categoria: 'componente',
                descricao: 'Componentes para equipamentos eletrônicos',
                status: 'Inativo',
                dataCriacao: '28/01/2026, 13:20:00',
                criadoPor: 'Maria',
                dataAlteracao: '10/03/2026, 16:45:00',
                alteradoPor: 'Maria'
            }
        ];

        this.tipos = tiposExemplo;
        localStorage.setItem('tipos', JSON.stringify(this.tipos));
    }
}

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    window.tiposManager = new TiposItemManager();
});