class CadastroItensManager {
    constructor() {
        this.itens = JSON.parse(localStorage.getItem('itens')) || [];
        this.tipos = JSON.parse(localStorage.getItem('tipos')) || [];
        this.locais = JSON.parse(localStorage.getItem('locais')) || [];
        this.itemEditando = null;
        this.itemExcluindo = null;
        this.usuarioLogado = 'Administrador';
        this.init();
    }

    init() {
        this.setupDropdown();
        this.setupModalItem();
        this.setupFormItem();
        this.setupModalConfirmacaoItem();
        this.setupFiltrosItens();
        this.setupBotoesItens();
        this.initTheme();
        this.renderItens();
        
        // Adicionar dados de exemplo se não existirem
        if (this.itens.length === 0) {
            this.adicionarItensExemplo();
        }
    }

    setupDropdown() {
        const themeToggle = document.getElementById('theme-toggle');
        const userDropdown = document.getElementById('user-dropdown');
        const userBtn = document.getElementById('user-btn');
        const perfilBtn = document.getElementById('perfil-btn');
        const configBtn = document.getElementById('config-btn');
        const sairBtn = document.getElementById('sair-btn');

        if (themeToggle) {
            themeToggle.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggleTheme();
            });
        }

        // Controle do dropdown do perfil
        if (userBtn && userDropdown) {
            userBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                userDropdown.classList.toggle('active');
            });

            // Fechar dropdown ao clicar fora
            document.addEventListener('click', (e) => {
                if (!userDropdown.contains(e.target)) {
                    userDropdown.classList.remove('active');
                }
            });
        }

        // Funcionalidades dos itens do menu
        if (perfilBtn) {
            perfilBtn.addEventListener('click', (e) => {
                e.preventDefault();
                userDropdown.classList.remove('active');
                this.showToast('Funcionalidade de Perfil em desenvolvimento', 'info');
            });
        }

        if (configBtn) {
            configBtn.addEventListener('click', (e) => {
                e.preventDefault();
                userDropdown.classList.remove('active');
                this.showToast('Funcionalidade de Configurações em desenvolvimento', 'info');
            });
        }

        if (sairBtn) {
            sairBtn.addEventListener('click', (e) => {
                e.preventDefault();
                userDropdown.classList.remove('active');
                const opcoes = confirm('Deseja sair do sistema?');
                if (opcoes) {
                    window.location.href = '../tela2entrar/index.html';
                }
            });
        }
    }

    initTheme() {
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

    toggleTheme() {
        const html = document.documentElement;
        const body = document.body;
        const themeIcon = document.querySelector('.theme-icon');
        
        if (body.getAttribute('data-theme') === 'dark') {
            body.removeAttribute('data-theme');
            html.removeAttribute('data-theme');
            themeIcon.textContent = '◐';
            localStorage.setItem('theme', 'light');
        } else {
            body.setAttribute('data-theme', 'dark');
            html.setAttribute('data-theme', 'dark');
            themeIcon.textContent = '◑';
            localStorage.setItem('theme', 'dark');
        }
    }

    showToast(message, type = 'info') {
        // Criar container se não existir
        let toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.className = 'toast-container';
            document.body.appendChild(toastContainer);
        }

        // Criar toast
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

        // Adicionar ao container
        toastContainer.appendChild(toast);

        // Configurar fechamento
        const closeBtn = toast.querySelector('.toast-close');
        closeBtn.addEventListener('click', () => {
            toast.remove();
        });

        // Auto-remover após 5 segundos
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 5000);
    }

    setupBotoesItens() {
        const btnVoltar = document.getElementById('btn-voltar-dashboard-itens');
        const btnAdicionar = document.getElementById('btn-adicionar-item');
        const btnBuscar = document.getElementById('btn-buscar-itens');
        const btnLimpar = document.getElementById('btn-limpar-itens');
        const btnFiltroAvancado = document.getElementById('btn-filtro-avancado-itens');
        
        if (btnVoltar) {
            btnVoltar.addEventListener('click', () => {
                window.location.href = '../tela1/paginainicial/index.html';
            });
        }
        
        if (btnAdicionar) {
            btnAdicionar.addEventListener('click', () => this.abrirModalItem());
        }

        if (btnBuscar) {
            btnBuscar.addEventListener('click', () => {
                this.aplicarFiltrosItens();
                this.showToast('Filtros aplicados!', 'info');
            });
        }

        if (btnLimpar) {
            btnLimpar.addEventListener('click', () => this.limparFiltrosItens());
        }

        if (btnFiltroAvancado) {
            btnFiltroAvancado.addEventListener('click', () => this.toggleFiltroAvancadoItens());
        }
    }

    setupFiltrosItens() {
        const nomeInput = document.getElementById('nome-item-input');
        const tipoSelect = document.getElementById('tipo-item-select');
        const statusSelect = document.getElementById('status-item-select');

        // Event listeners para filtros em tempo real
        if (nomeInput) {
            nomeInput.addEventListener('input', () => this.aplicarFiltrosItens());
        }
        if (tipoSelect) {
            tipoSelect.addEventListener('change', () => this.aplicarFiltrosItens());
        }
        if (statusSelect) {
            statusSelect.addEventListener('change', () => this.aplicarFiltrosItens());
        }
    }

    setupModalItem() {
        const modal = document.getElementById('modal-item');
        const btnCancelar = document.getElementById('btn-cancelar-item');
        const closeBtn = document.getElementById('close-item');

        if (btnCancelar) {
            btnCancelar.addEventListener('click', () => this.fecharModalItem());
        }
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.fecharModalItem());
        }
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) this.fecharModalItem();
            });
        }
    }

    setupFormItem() {
        const form = document.getElementById('item-form');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.salvarItem();
            });
        }
    }

    setupModalConfirmacaoItem() {
        const modal = document.getElementById('modal-confirmacao-item');
        const btnCancelar = document.getElementById('btn-cancelar-exclusao-item');
        const btnConfirmar = document.getElementById('btn-confirmar-exclusao-item');

        if (btnCancelar) {
            btnCancelar.addEventListener('click', () => this.fecharModalConfirmacaoItem());
        }
        if (btnConfirmar) {
            btnConfirmar.addEventListener('click', () => this.confirmarExclusaoItem());
        }
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) this.fecharModalConfirmacaoItem();
            });
        }
    }

    abrirModalItem(item = null) {
        const modal = document.getElementById('modal-item');
        const modalTitle = document.getElementById('modal-item-title');
        const form = document.getElementById('item-form');
        
        this.itemEditando = item;
        
        if (item) {
            modalTitle.textContent = 'Editar Item';
            this.preencherFormItem(item);
        } else {
            modalTitle.textContent = 'Adicionar Item';
            form.reset();
        }
        
        modal.classList.add('active');
    }

    fecharModalItem() {
        const modal = document.getElementById('modal-item');
        modal.classList.remove('active');
        this.itemEditando = null;
    }

    preencherFormItem(item) {
        document.getElementById('nome-item').value = item.nome || '';
        document.getElementById('tipo-item').value = item.tipoId || '';
        document.getElementById('descricao-item').value = item.descricao || '';
        document.getElementById('quantidade-item').value = item.quantidade || '0';
        document.getElementById('unidade-item').value = item.unidade || '';
        document.getElementById('local-item').value = item.localId || '';
        document.getElementById('status-item').value = item.status || 'Ativo';
    }

    salvarItem() {
        const nome = document.getElementById('nome-item').value.trim();
        const tipoId = document.getElementById('tipo-item').value;
        const descricao = document.getElementById('descricao-item').value.trim();
        const quantidade = parseInt(document.getElementById('quantidade-item').value) || 0;
        const unidade = document.getElementById('unidade-item').value;
        const localId = document.getElementById('local-item').value;
        const status = document.getElementById('status-item').value;

        // Validar campos obrigatórios
        if (!nome) {
            this.showToast('O nome do item é obrigatório!', 'warning');
            return;
        }

        if (!tipoId) {
            this.showToast('O tipo é obrigatório!', 'warning');
            return;
        }

        if (!unidade) {
            this.showToast('A unidade é obrigatória!', 'warning');
            return;
        }

        if (!localId) {
            this.showToast('O local é obrigatório!', 'warning');
            return;
        }

        const agora = new Date().toLocaleString('pt-BR');

        // Calcular próximo ID sequencial
        let novoId;
        if (this.itemEditando) {
            novoId = this.itemEditando.id;
        } else {
            const maiorId = this.itens.length > 0 ? Math.max(...this.itens.map(i => i.id)) : 0;
            novoId = maiorId + 1;
        }

        const novoItem = {
            id: novoId,
            nome,
            tipoId: parseInt(tipoId),
            tipoNome: this.getTipoNome(tipoId),
            descricao,
            quantidade,
            unidade,
            localId: parseInt(localId),
            localNome: this.getLocalNome(localId),
            status,
            dataCriacao: this.itemEditando ? this.itemEditando.dataCriacao : agora,
            criadoPor: this.itemEditando ? this.itemEditando.criadoPor : this.usuarioLogado,
            dataAlteracao: agora,
            alteradoPor: this.usuarioLogado
        };

        if (this.itemEditando) {
            const index = this.itens.findIndex(i => i.id === this.itemEditando.id);
            this.itens[index] = novoItem;
            this.showToast('Item atualizado com sucesso!', 'success');
        } else {
            this.itens.push(novoItem);
            this.showToast('Item adicionado com sucesso!', 'success');
        }

        localStorage.setItem('itens', JSON.stringify(this.itens));
        this.renderItens();
        this.fecharModalItem();
    }

    excluirItem(id) {
        this.itemExcluindo = id;
        const modal = document.getElementById('modal-confirmacao-item');
        modal.classList.add('active');
    }

    fecharModalConfirmacaoItem() {
        const modal = document.getElementById('modal-confirmacao-item');
        modal.classList.remove('active');
        this.itemExcluindo = null;
    }

    confirmarExclusaoItem() {
        if (this.itemExcluindo) {
            this.itens = this.itens.filter(i => i.id !== this.itemExcluindo);
            localStorage.setItem('itens', JSON.stringify(this.itens));
            this.renderItens();
            this.showToast('Item excluído com sucesso!', 'success');
        }
        this.fecharModalConfirmacaoItem();
    }

    getTipoNome(tipoId) {
        const tipoMap = {
            '1': 'Material de Construção',
            '2': 'Equipamento de Informática',
            '3': 'Material de Escritório',
            '4': 'Ferramentas Manuais',
            '5': 'Componente Eletrônico'
        };
        return tipoMap[tipoId] || 'Desconhecido';
    }

    getLocalNome(localId) {
        const localMap = {
            '1': 'Depósito Central',
            '2': 'Armazém Norte',
            '3': 'Galpão Sul'
        };
        return localMap[localId] || 'Desconhecido';
    }

    renderItens() {
        const tbody = document.getElementById('itens-tbody');
        if (!tbody) return;

        tbody.innerHTML = '';

        this.itens.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="checkbox-col">
                    <input type="checkbox" class="item-checkbox" data-id="${item.id}">
                </td>
                <td class="id-col">${item.id}</td>
                <td class="name-col">${item.nome}</td>
                <td class="type-col">${item.tipoNome}</td>
                <td class="description-col">${item.descricao || 'N/A'}</td>
                <td class="quantity-col">${item.quantidade}</td>
                <td class="unit-col">${item.unidade}</td>
                <td class="location-col">${item.localNome}</td>
                <td class="status-col">
                    <span class="status ${item.status.toLowerCase()}">${item.status}</span>
                </td>
                <td class="date-creation-col">${item.dataCriacao || 'N/A'}</td>
                <td class="created-by-col">${item.criadoPor || 'N/A'}</td>
                <td class="actions-col">
                    <div class="actions">
                        <button class="btn-edit" onclick="cadastroItens.abrirModalItem(${JSON.stringify(item).replace(/"/g, '&quot;')})" title="Editar">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="m18.5 2.5 a2.12 2.12 0 0 1 3 3l-9.5 9.5-4 1 1-4 9.5-9.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                        <button class="btn-delete" onclick="cadastroItens.excluirItem(${item.id})" title="Excluir">
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

    aplicarFiltrosItens() {
        const nome = document.getElementById('nome-item-input')?.value.toLowerCase() || '';
        const tipo = document.getElementById('tipo-item-select')?.value || '';
        const status = document.getElementById('status-item-select')?.value || '';

        let itensFiltrados = this.itens;

        if (nome) {
            itensFiltrados = itensFiltrados.filter(item =>
                item.nome.toLowerCase().includes(nome)
            );
        }

        if (tipo) {
            itensFiltrados = itensFiltrados.filter(item =>
                item.tipoId === parseInt(tipo)
            );
        }

        if (status) {
            itensFiltrados = itensFiltrados.filter(item =>
                item.status === status
            );
        }

        this.renderItensFiltrados(itensFiltrados);
    }

    renderItensFiltrados(itens) {
        const tbody = document.getElementById('itens-tbody');
        if (!tbody) return;

        tbody.innerHTML = '';

        itens.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="checkbox-col">
                    <input type="checkbox" class="item-checkbox" data-id="${item.id}">
                </td>
                <td class="id-col">${item.id}</td>
                <td class="name-col">${item.nome}</td>
                <td class="type-col">${item.tipoNome}</td>
                <td class="description-col">${item.descricao || 'N/A'}</td>
                <td class="quantity-col">${item.quantidade}</td>
                <td class="unit-col">${item.unidade}</td>
                <td class="location-col">${item.localNome}</td>
                <td class="status-col">
                    <span class="status ${item.status.toLowerCase()}">${item.status}</span>
                </td>
                <td class="date-creation-col">${item.dataCriacao || 'N/A'}</td>
                <td class="created-by-col">${item.criadoPor || 'N/A'}</td>
                <td class="actions-col">
                    <div class="actions">
                        <button class="btn-edit" onclick="cadastroItens.abrirModalItem(${JSON.stringify(item).replace(/"/g, '&quot;')})" title="Editar">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="m18.5 2.5 a2.12 2.12 0 0 1 3 3l-9.5 9.5-4 1 1-4 9.5-9.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                        <button class="btn-delete" onclick="cadastroItens.excluirItem(${item.id})" title="Excluir">
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

    limparFiltrosItens() {
        const nomeInput = document.getElementById('nome-item-input');
        const tipoSelect = document.getElementById('tipo-item-select');
        const statusSelect = document.getElementById('status-item-select');

        if (nomeInput) nomeInput.value = '';
        if (tipoSelect) tipoSelect.value = '';
        if (statusSelect) statusSelect.value = '';

        this.renderItens();
        this.showToast('Filtros limpos!', 'info');
    }

    toggleFiltroAvancadoItens() {
        this.showToast('Filtro avançado de itens em desenvolvimento', 'info');
    }

    adicionarItensExemplo() {
        const itensExemplo = [
            {
                id: 1,
                nome: 'Martelo de Unha 500g',
                tipoId: 4,
                tipoNome: 'Ferramentas Manuais',
                descricao: 'Martelo de unha profissional com cabo de madeira',
                quantidade: 15,
                unidade: 'UN',
                localId: 1,
                localNome: 'Depósito Central',
                status: 'Ativo',
                dataCriacao: '20/01/2026, 08:00:00',
                criadoPor: 'Sistema',
                dataAlteracao: '20/01/2026, 08:00:00',
                alteradoPor: 'Sistema'
            },
            {
                id: 2,
                nome: 'Mouse Óptico USB',
                tipoId: 2,
                tipoNome: 'Equipamento de Informática',
                descricao: 'Mouse óptico com conexão USB 2.0',
                quantidade: 25,
                unidade: 'UN',
                localId: 2,
                localNome: 'Armazém Norte',
                status: 'Ativo',
                dataCriacao: '22/01/2026, 10:30:00',
                criadoPor: 'Administrador',
                dataAlteracao: '25/02/2026, 14:20:00',
                alteradoPor: 'Maria'
            },
            {
                id: 3,
                nome: 'Papel A4 Branco',
                tipoId: 3,
                tipoNome: 'Material de Escritório',
                descricao: 'Resma de papel A4 75g com 500 folhas',
                quantidade: 50,
                unidade: 'PCT',
                localId: 1,
                localNome: 'Depósito Central',
                status: 'Ativo',
                dataCriacao: '15/02/2026, 16:45:00',
                criadoPor: 'Pedro Costa',
                dataAlteracao: '09/03/2026, 09:30:00',
                alteradoPor: 'Administrador'
            },
            {
                id: 4,
                nome: 'Cimento Portland CP II',
                tipoId: 1,
                tipoNome: 'Material de Construção',
                descricao: 'Saco de cimento Portland CP II - 50kg',
                quantidade: 100,
                unidade: 'PC',
                localId: 3,
                localNome: 'Galpão Sul',
                status: 'Ativo',
                dataCriacao: '25/01/2026, 11:15:00',
                criadoPor: 'Sistema',
                dataAlteracao: '25/01/2026, 11:15:00',
                alteradoPor: 'Sistema'
            },
            {
                id: 5,
                nome: 'Resistor 1KΩ',
                tipoId: 5,
                tipoNome: 'Componente Eletrônico',
                descricao: 'Resistor de carbono 1KΩ 1/4W 5%',
                quantidade: 0,
                unidade: 'UN',
                localId: 2,
                localNome: 'Armazém Norte',
                status: 'Inativo',
                dataCriacao: '28/01/2026, 13:20:00',
                criadoPor: 'Técnico',
                dataAlteracao: '10/03/2026, 16:45:00',
                alteradoPor: 'Administrador'
            }
        ];

        this.itens = itensExemplo;
        localStorage.setItem('itens', JSON.stringify(this.itens));
        this.renderItens();
    }
}

// Inicializar o sistema quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    window.cadastroItens = new CadastroItensManager();
});