
class EstoqueManager {
    constructor() {
        this.produtos = JSON.parse(localStorage.getItem('produtos')) || [];
        this.usuarios = JSON.parse(localStorage.getItem('usuarios')) || [];
        this.locais = JSON.parse(localStorage.getItem('locais')) || [];
        this.tipos = JSON.parse(localStorage.getItem('tipos')) || [];
        this.produtoEditando = null;
        this.usuarioEditando = null;
        this.usuarioExcluindo = null;
        this.localEditando = null;
        this.localExcluindo = null;
        this.tipoEditando = null;
        this.tipoExcluindo = null;
        this.usuarioLogado = 'Administrador'; // Simulação de usuário logado
        this.senhaUsuarioLogado = '123456'; // Senha para validação (em produção deveria vir do backend)
        this.init();
    }

    init() {
        this.setupModuleNavigation();
        this.setupBackButtons();
        this.setupDropdown();
        this.setupModal();
        this.setupModalUsuario();
        this.setupModalLocal();
        this.setupModalConfirmacao();
        this.setupModalConfirmacaoLocal();
        this.setupFilters();
        this.setupFiltrosUsuarios();
        this.setupForm();
        this.setupFormUsuario();
        this.setupFormLocal();
        this.setupModalTipo();
        this.setupFormTipo();
        this.setupModalConfirmacaoTipo();
        this.renderUsuarios();
        
        // Limpar dados antigos e adicionar novos dados de exemplo
        localStorage.removeItem('usuarios');
        this.usuarios = [];
        this.adicionarUsuariosExemplo();
        
        // Inicializar tema salvo
        this.initTheme();
        
        // Mostrar dashboard inicialmente
        this.showSection('dashboard');
    }

    setupModuleNavigation() {
        const moduleCards = document.querySelectorAll('.course-card');
        moduleCards.forEach(card => {
            card.addEventListener('click', () => {
                const module = card.getAttribute('data-module');
                if (module === 'usuarios') {
                    this.showSection('usuarios');
                    this.updateBreadcrumb('usuarios');
                    this.renderUsuarios();
                } else if (module === 'locais') {
                    this.showSection('locais');
                    this.updateBreadcrumb('locais');
                    this.renderLocais();
                } else if (module === 'tipos-item') {
                    // Navegar para a página de tipos de item
                    window.location.href = '../../tipos-item/index.html';
                } else if (module === 'itens') {
                    // Navegar para a página de cadastro de itens
                    window.location.href = '../../cadastro-itens/index.html';
                } else if (module === 'estoque') {
                    // Navegar para a página de controle de estoque
                    window.location.href = '../../Controle de estoque/index.html';
                } else if (module === 'movimentacoes') {
                    this.showToast('Módulo de Movimentações em desenvolvimento', 'info');
                } else {
                    this.showSection(module);
                    this.updateBreadcrumb(module);
                }
            });
        });
    }

    setupBackButtons() {
        const backButtons = document.querySelectorAll('.btn-back');
        backButtons.forEach(button => {
            button.addEventListener('click', () => {
                this.showSection('dashboard');
            });
        });
    }

    showSection(sectionId) {
        // Ocultar todas as seções
        const allSections = document.querySelectorAll('section');
        allSections.forEach(section => {
            section.classList.remove('active');
        });

        // Mostrar seção específica
        const targetSection = document.getElementById(sectionId);
        if (targetSection) {
            targetSection.classList.add('active');
        }

        // Carregamento específico da seção
        if (sectionId === 'usuarios') {
            this.renderUsuarios();
        }
    }


    setupSidebarToggle() {
        const sidebarToggle = document.getElementById('sidebar-toggle');
        const dashboardSidebar = document.getElementById('dashboard-sidebar');
        const mainContent = document.querySelector('.main-content');

        if (sidebarToggle && dashboardSidebar) {
            sidebarToggle.addEventListener('click', () => {
                dashboardSidebar.classList.toggle('collapsed');
                
                // Ajustar margin do main content
                if (dashboardSidebar.classList.contains('collapsed')) {
                    mainContent.style.marginLeft = '40px';
                    sidebarToggle.setAttribute('title', 'Mostrar painel');
                } else {
                    mainContent.style.marginLeft = '320px';
                    sidebarToggle.setAttribute('title', 'Ocultar painel');
                }
            });
        }

        // Configurar navegação do sidebar
        const menuItems = document.querySelectorAll('.menu-item');
        menuItems.forEach(item => {
            item.addEventListener('click', () => {
                // Remover classe active de todos os itens
                menuItems.forEach(i => i.classList.remove('active'));
                // Adicionar classe active ao item clicado
                item.classList.add('active');
                
                // Navegar para a seção correspondente
                const sectionId = item.getAttribute('data-section');
                if (sectionId) {
                    this.showSection(sectionId);
                    this.updateBreadcrumb(sectionId);
                }
            });
        });
    }

    updateBreadcrumb(sectionId) {
        const breadcrumb = document.getElementById('breadcrumb');
        const sectionNames = {
            'dashboard': 'Dashboard',
            'usuarios': 'Gestão de Usuários',
            'locais': 'Gestão de Locais',
            'tipos-item': 'Tipos de Item',
            'itens': 'Cadastro de Itens',
            'estoque': 'Controle de Estoque',
            'movimentacoes': 'Movimentações'
        };

        if (breadcrumb) {
            breadcrumb.innerHTML = `<span class="breadcrumb-item active">${sectionNames[sectionId] || 'Dashboard'}</span>`;
        }
    }

    updateMiniStats() {
        // Atualizar números do dashboard sidebar
        const totalUsuarios = this.usuarios.length;
        const usuariosAtivos = this.usuarios.filter(u => u.ativo === 'S').length;
        const totalItens = this.produtos ? this.produtos.length : 0;
        const atividadeHoje = 5; // Valor fixo por enquanto

        // Atualizar elementos do sidebar
        const miniUsuarios = document.getElementById('mini-usuarios');
        const miniAtivos = document.getElementById('mini-ativos');
        const miniItens = document.getElementById('mini-itens');
        const miniAtividade = document.getElementById('mini-atividade');

        if (miniUsuarios) miniUsuarios.textContent = totalUsuarios;
        if (miniAtivos) miniAtivos.textContent = usuariosAtivos;
        if (miniItens) miniItens.textContent = totalItens;
        if (miniAtividade) miniAtividade.textContent = atividadeHoje;

        // Atualizar também os cards principais
        const totalUsuariosCard = document.getElementById('total-usuarios');
        const usuariosAtivosCard = document.getElementById('usuarios-ativos');
        const totalItensCard = document.getElementById('total-itens');
        const atividadeHojeCard = document.getElementById('atividade-hoje');

        if (totalUsuariosCard) totalUsuariosCard.textContent = totalUsuarios;
        if (usuariosAtivosCard) usuariosAtivosCard.textContent = usuariosAtivos;
        if (totalItensCard) totalItensCard.textContent = totalItens;
        if (atividadeHojeCard) atividadeHojeCard.textContent = atividadeHoje;
    }

    setupDropdown() {
        const themeToggle = document.getElementById('theme-toggle');
        const logoutBtn = document.getElementById('logout-btn');
        const userDropdown = document.getElementById('user-dropdown');
        const userBtn = document.getElementById('user-btn');
        const userDropdownContent = document.getElementById('user-dropdown-content');
        const perfilBtn = document.getElementById('perfil-btn');
        const configBtn = document.getElementById('config-btn');
        const sairBtn = document.getElementById('sair-btn');

        if (themeToggle) {
            themeToggle.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggleTheme();
            });
        }

        if (logoutBtn) {
            logoutBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.logout();
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
                    window.location.href = '../index.html';
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

    setupModal() {
        const modal = document.getElementById('modal');
        const btnAdicionar = document.getElementById('btn-adicionar');
        const btnCancelar = document.getElementById('btn-cancelar');
        const closeBtn = document.querySelector('.close');

        if (btnAdicionar) {
            btnAdicionar.addEventListener('click', () => this.abrirModal());
        }
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
    }

    setupFilters() {
        const buscarInput = document.getElementById('buscar-produto');
        const filtroCategoria = document.getElementById('filtro-categoria');

        if (buscarInput) {
            buscarInput.addEventListener('input', () => this.aplicarFiltros());
        }
        if (filtroCategoria) {
            filtroCategoria.addEventListener('change', () => this.aplicarFiltros());
        }
    }

    setupForm() {
        const form = document.getElementById('produto-form');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.salvarProduto();
            });
        }
    }

    abrirModal(produto = null) {
        const modal = document.getElementById('modal');
        const modalTitle = document.getElementById('modal-title');
        const form = document.getElementById('produto-form');
        
        this.produtoEditando = produto;
        
        if (produto) {
            modalTitle.textContent = 'Editar Produto';
            this.preencherForm(produto);
        } else {
            modalTitle.textContent = 'Adicionar Produto';
            form.reset();
        }
        
        modal.classList.add('active');
    }

    fecharModal() {
        const modal = document.getElementById('modal');
        modal.classList.remove('active');
        this.produtoEditando = null;
    }

    preencherForm(produto) {
        document.getElementById('nome').value = produto.nome;
        document.getElementById('categoria').value = produto.categoria;
        document.getElementById('quantidade').value = produto.quantidade;
        document.getElementById('preco').value = produto.preco;
    }

    salvarProduto() {
        const nome = document.getElementById('nome').value;
        const categoria = document.getElementById('categoria').value;
        const quantidade = parseInt(document.getElementById('quantidade').value);
        const preco = parseFloat(document.getElementById('preco').value);

        const produto = {
            id: this.produtoEditando ? this.produtoEditando.id : Date.now(),
            nome,
            categoria,
            quantidade,
            preco,
            status: this.getStatus(quantidade)
        };

        if (this.produtoEditando) {
            const index = this.produtos.findIndex(p => p.id === this.produtoEditando.id);
            this.produtos[index] = produto;
        } else {
            this.produtos.push(produto);
        }

        this.salvarLocalStorage();
        this.renderProdutos();
        this.fecharModal();
    }

    excluirProduto(id) {
        if (confirm('Tem certeza que deseja excluir este produto?')) {
            this.produtos = this.produtos.filter(p => p.id !== id);
            this.salvarLocalStorage();
            this.renderProdutos();
        }
    }

    getStatus(quantidade) {
        if (quantidade === 0) return 'sem-estoque';
        if (quantidade <= 5) return 'estoque-baixo';
        return 'em-estoque';
    }

    getStatusText(status) {
        const statusMap = {
            'em-estoque': 'Em Estoque',
            'estoque-baixo': 'Estoque Baixo',
            'sem-estoque': 'Sem Estoque'
        };
        return statusMap[status] || status;
    }

    renderProdutos() {
        const tbody = document.getElementById('produtos-tbody');
        if (!tbody) return;

        tbody.innerHTML = '';

        this.produtos.forEach(produto => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${produto.id}</td>
                <td>${produto.nome}</td>
                <td>${this.getCategoriaText(produto.categoria)}</td>
                <td>${produto.quantidade}</td>
                <td>R$ ${produto.preco.toFixed(2).replace('.', ',')}</td>
                <td><span class="status ${produto.status}">${this.getStatusText(produto.status)}</span></td>
                <td class="actions">
                    <button class="btn-edit" onclick="estoque.abrirModal(${JSON.stringify(produto).replace(/"/g, '&quot;')})">Editar</button>
                    <button class="btn-delete" onclick="estoque.excluirProduto(${produto.id})">Excluir</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    getCategoriaText(categoria) {
        const categoriaMap = {
            'eletronicos': 'Eletrônicos',
            'roupas': 'Roupas',
            'casa': 'Casa e Jardim',
            'livros': 'Livros'
        };
        return categoriaMap[categoria] || categoria;
    }

    aplicarFiltros() {
        const buscaInput = document.getElementById('buscar-produto');
        const categoriaInput = document.getElementById('filtro-categoria');
        
        const busca = buscaInput ? buscaInput.value.toLowerCase() : '';
        const categoria = categoriaInput ? categoriaInput.value : '';

        let produtosFiltrados = this.produtos;

        if (busca) {
            produtosFiltrados = produtosFiltrados.filter(produto =>
                produto.nome.toLowerCase().includes(busca)
            );
        }

        if (categoria) {
            produtosFiltrados = produtosFiltrados.filter(produto =>
                produto.categoria === categoria
            );
        }

        this.renderProdutosFiltrados(produtosFiltrados);
    }

    renderProdutosFiltrados(produtos) {
        const tbody = document.getElementById('produtos-tbody');
        tbody.innerHTML = '';

        produtos.forEach(produto => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${produto.id}</td>
                <td>${produto.nome}</td>
                <td>${this.getCategoriaText(produto.categoria)}</td>
                <td>${produto.quantidade}</td>
                <td>R$ ${produto.preco.toFixed(2).replace('.', ',')}</td>
                <td><span class="status ${produto.status}">${this.getStatusText(produto.status)}</span></td>
                <td class="actions">
                    <button class="btn-edit" onclick="estoque.abrirModal(${JSON.stringify(produto).replace(/"/g, '&quot;')})">Editar</button>
                    <button class="btn-delete" onclick="estoque.excluirProduto(${produto.id})">Excluir</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    salvarLocalStorage() {
        localStorage.setItem('produtos', JSON.stringify(this.produtos));
    }

    adicionarProdutosExemplo() {
        const produtosExemplo = [
            {
                id: 1,
                nome: 'Smartphone Samsung Galaxy',
                categoria: 'eletronicos',
                quantidade: 15,
                preco: 899.99,
                status: 'em-estoque'
            },
            {
                id: 2,
                nome: 'Camiseta Polo',
                categoria: 'roupas',
                quantidade: 3,
                preco: 79.90,
                status: 'estoque-baixo'
            },
            {
                id: 3,
                nome: 'Aspirador de Pó',
                categoria: 'casa',
                quantidade: 0,
                preco: 299.99,
                status: 'sem-estoque'
            },
            {
                id: 4,
                nome: 'Livro: JavaScript Moderno',
                categoria: 'livros',
                quantidade: 25,
                preco: 59.90,
                status: 'em-estoque'
            }
        ];

        this.produtos = produtosExemplo;
        this.salvarLocalStorage();
        this.renderProdutos();
    }

    // FUNCIONALIDADES DE USUÁRIOS
    setupNavigation() {
        const navLinks = document.querySelectorAll('.nav-link');
        const sections = {
            'produtos': document.getElementById('produtos'),
            'usuarios': document.getElementById('usuarios')
        };

        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                if (link.getAttribute('href').startsWith('#')) {
                    e.preventDefault();
                    const targetId = link.getAttribute('href').substring(1);
                    
                    // Update active nav link
                    navLinks.forEach(nl => nl.classList.remove('active'));
                    link.classList.add('active');
                    
                    // Show/hide sections
                    Object.values(sections).forEach(section => {
                        if (section) {
                            section.classList.remove('active');
                            section.style.display = 'none';
                        }
                    });
                    
                    if (sections[targetId]) {
                        sections[targetId].classList.add('active');
                        sections[targetId].style.display = 'block';
                    }
                }
            });
        });
    }

    setupModalUsuario() {
        const modal = document.getElementById('modal-usuario');
        const btnAdicionar = document.getElementById('btn-adicionar-usuario');
        const btnVoltar = document.getElementById('btn-exportar-usuario');
        const btnCancelar = document.getElementById('btn-cancelar-usuario');
        const closeBtn = document.getElementById('close-usuario');

        if (btnAdicionar) {
            btnAdicionar.addEventListener('click', () => this.abrirModalUsuario());
        }
        if (btnVoltar) {
            btnVoltar.addEventListener('click', () => this.voltarParaDashboard());
        }
        if (btnCancelar) {
            btnCancelar.addEventListener('click', () => this.fecharModalUsuario());
        }
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.fecharModalUsuario());
        }
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) this.fecharModalUsuario();
            });
        }
    }

    setupFiltrosUsuarios() {
        // Filtros principais de usuários
        const nomeInput = document.getElementById('nome-input');
        const emailInput = document.getElementById('email-input');
        const btnBuscar = document.getElementById('btn-buscar');
        const btnLimpar = document.getElementById('btn-limpar');
        const btnFiltroAvancado = document.getElementById('btn-filtro-avancado');

        // Event listeners para filtros em tempo real
        if (nomeInput) {
            nomeInput.addEventListener('input', () => this.aplicarFiltrosUsuarios());
        }
        if (emailInput) {
            emailInput.addEventListener('input', () => this.aplicarFiltrosUsuarios());
        }
        
        // Event listeners para botões
        if (btnBuscar) {
            btnBuscar.addEventListener('click', () => {
                this.aplicarFiltrosUsuarios();
                this.showToast('Filtros aplicados!', 'info');
            });
        }
        if (btnLimpar) {
            btnLimpar.addEventListener('click', () => this.limparFiltrosUsuarios());
        }
        if (btnFiltroAvancado) {
            btnFiltroAvancado.addEventListener('click', () => this.toggleFiltroAvancadoUsuarios());
        }

        // Filtros para locais
        this.setupFiltrosLocais();
    }

    setupFiltrosLocais() {
        const nomeLocalInput = document.getElementById('nome-local-input');
        const descricaoLocalInput = document.getElementById('descricao-local-input');
        const btnBuscarLocais = document.getElementById('btn-buscar-locais');
        const btnLimparLocais = document.getElementById('btn-limpar-locais');
        const btnFiltroAvancadoLocais = document.getElementById('btn-filtro-avancado-locais');

        // Event listeners para filtros em tempo real
        if (nomeLocalInput) {
            nomeLocalInput.addEventListener('input', () => this.aplicarFiltrosLocais());
        }
        if (descricaoLocalInput) {
            descricaoLocalInput.addEventListener('input', () => this.aplicarFiltrosLocais());
        }
        
        // Event listeners para botões
        if (btnBuscarLocais) {
            btnBuscarLocais.addEventListener('click', () => {
                this.aplicarFiltrosLocais();
                this.showToast('Filtros aplicados!', 'info');
            });
        }
        if (btnLimparLocais) {
            btnLimparLocais.addEventListener('click', () => this.limparFiltrosLocais());
        }
        if (btnFiltroAvancadoLocais) {
            btnFiltroAvancadoLocais.addEventListener('click', () => this.toggleFiltroAvancadoLocais());
        }
    }

    setupFormUsuario() {
        const form = document.getElementById('usuario-form');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.salvarUsuario();
            });
        }
    }

    abrirModalUsuario(usuario = null) {
        const modal = document.getElementById('modal-usuario');
        const modalTitle = document.getElementById('modal-usuario-title');
        const form = document.getElementById('usuario-form');
        
        this.usuarioEditando = usuario;
        
        if (usuario) {
            modalTitle.textContent = 'Editar Usuário';
            this.preencherFormUsuario(usuario);
        } else {
            modalTitle.textContent = 'Adicionar Usuário';
            form.reset();
        }
        
        modal.classList.add('active');
    }

    fecharModalUsuario() {
        const modal = document.getElementById('modal-usuario');
        modal.classList.remove('active');
        this.usuarioEditando = null;
    }

    preencherFormUsuario(usuario) {
        document.getElementById('nome-usuario').value = usuario.nome;
        document.getElementById('email').value = usuario.email;
        document.getElementById('ativo').value = usuario.ativo;
        // Limpar campo senha na edição
        document.getElementById('senha').value = '';
    }

    salvarUsuario() {
        const nome = document.getElementById('nome-usuario').value;
        const email = document.getElementById('email').value;
        const senha = document.getElementById('senha').value;
        const ativo = document.getElementById('ativo').value;

        const agora = new Date().toLocaleString('pt-BR');

        // Calcular próximo ID sequencial
        let novoId;
        if (this.usuarioEditando) {
            novoId = this.usuarioEditando.id;
        } else {
            const maiorId = this.usuarios.length > 0 ? Math.max(...this.usuarios.map(u => u.id)) : 0;
            novoId = maiorId + 1;
        }

        const novoUsuario = {
            id: novoId,
            nome,
            email,
            senha: this.usuarioEditando && !senha ? this.usuarioEditando.senha : senha, // Manter senha existente se não foi alterada
            ativo,
            dataCriacao: this.usuarioEditando ? this.usuarioEditando.dataCriacao : agora,
            criadoPor: this.usuarioEditando ? this.usuarioEditando.criadoPor : this.usuarioLogado,
            dataAlteracao: agora,
            alteradoPor: this.usuarioLogado
        };

        if (this.usuarioEditando) {
            const index = this.usuarios.findIndex(u => u.id === this.usuarioEditando.id);
            this.usuarios[index] = novoUsuario;
            this.showToast('Usuário atualizado com sucesso!', 'success');
        } else {
            this.usuarios.push(novoUsuario);
            this.showToast('Usuário adicionado com sucesso!', 'success');
        }

        this.salvarUsuariosLocalStorage();
        this.renderUsuarios();
        this.updateMiniStats(); // Atualizar estatísticas
        this.fecharModalUsuario();
    }

    excluirUsuario(id) {
        this.usuarioExcluindo = id;
        const modal = document.getElementById('modal-confirmacao');
        modal.classList.add('active');
    }

    setupModalConfirmacao() {
        const modal = document.getElementById('modal-confirmacao');
        const btnCancelar = document.getElementById('btn-cancelar-exclusao');
        const btnConfirmar = document.getElementById('btn-confirmar-exclusao');

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

    fecharModalConfirmacao() {
        const modal = document.getElementById('modal-confirmacao');
        modal.classList.remove('active');
        this.usuarioExcluindo = null;
    }

    confirmarExclusao() {
        if (this.usuarioExcluindo) {
            this.usuarios = this.usuarios.filter(u => u.id !== this.usuarioExcluindo);
            this.salvarUsuariosLocalStorage();
            this.renderUsuarios();
        }
        this.fecharModalConfirmacao();
    }

    renderUsuarios() {
        const tbody = document.getElementById('usuarios-tbody');
        if (!tbody) return;

        tbody.innerHTML = '';

        this.usuarios.forEach(usuario => {
            const row = document.createElement('tr');
            const isAtivo = usuario.ativo === 'S';
            row.innerHTML = `
                <td class="checkbox-col">
                    <input type="checkbox" class="user-checkbox" data-id="${usuario.id}">
                </td>
                <td class="id-col">${usuario.id}</td>
                <td class="name-col">${usuario.nome}</td>
                <td class="email-col">${usuario.email}</td>
                <td class="status-col">
                    ${isAtivo ? 'Ativo' : 'Inativo'}
                </td>
                <td class="actions-col">
                    <div class="actions">
                        <button class="btn-edit" onclick="estoque.abrirModalUsuario(${JSON.stringify(usuario).replace(/"/g, '&quot;')})" title="Editar">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="m18.5 2.5 a2.12 2.12 0 0 1 3 3l-9.5 9.5-4 1 1-4 9.5-9.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                        <button class="btn-delete" onclick="estoque.excluirUsuario(${usuario.id})" title="Excluir">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6h14ZM10 11v6M14 11v6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                    </div>
                </td>
            `;
            tbody.appendChild(row);
        });
        
        // Atualizar contadores na tabela
        this.updateTableCounters();
    }

    aplicarFiltrosUsuarios() {
        const nome = document.getElementById('nome-input')?.value.toLowerCase() || '';
        const email = document.getElementById('email-input')?.value.toLowerCase() || '';

        let usuariosFiltrados = this.usuarios;

        if (nome) {
            usuariosFiltrados = usuariosFiltrados.filter(usuario =>
                usuario.nome.toLowerCase().includes(nome)
            );
        }

        if (email) {
            usuariosFiltrados = usuariosFiltrados.filter(usuario =>
                usuario.email.toLowerCase().includes(email)
            );
        }

        this.renderUsuariosFiltrados(usuariosFiltrados);
    }

    limparFiltrosUsuarios() {
        const nomeInput = document.getElementById('nome-input');
        const emailInput = document.getElementById('email-input');

        if (nomeInput) nomeInput.value = '';
        if (emailInput) emailInput.value = '';

        this.renderUsuarios();
        this.showToast('Filtros de usuários limpos!', 'info');
    }

    toggleFiltroAvancadoUsuarios() {
        // Funcionalidade de filtro avançado para usuários (a ser implementada)
        this.showToast('Filtro avançado de usuários em desenvolvimento', 'info');
    }

    toggleFiltroAvancadoLocais() {
        // Funcionalidade de filtro avançado para locais (a ser implementada)
        this.showToast('Filtro avançado de locais em desenvolvimento', 'info');
    }

    renderUsuariosFiltrados(usuarios) {
        const tbody = document.getElementById('usuarios-tbody');
        if (!tbody) return;

        tbody.innerHTML = '';

        usuarios.forEach(usuario => {
            const row = document.createElement('tr');
            const isAtivo = usuario.ativo === 'S';
            row.innerHTML = `
                <td>${usuario.id}</td>
                <td>${usuario.nome}</td>
                <td>${usuario.email}</td>
                <td><span class="status ${isAtivo ? 'em-estoque' : 'sem-estoque'}">
                    ${isAtivo ? 'Ativo' : 'Inativo'}</span></td>
                <td>${usuario.dataCriacao}</td>
                <td>${usuario.criadoPor}</td>
                <td>${usuario.dataAlteracao}</td>
                <td>${usuario.alteradoPor}</td>
                <td class="actions">
                    <button class="btn-edit" onclick="estoque.abrirModalUsuario(${JSON.stringify(usuario).replace(/"/g, '&quot;')})">Editar</button>
                    <button class="btn-delete" onclick="estoque.excluirUsuario(${usuario.id})">Excluir</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    salvarUsuariosLocalStorage() {
        localStorage.setItem('usuarios', JSON.stringify(this.usuarios));
    }

    adicionarUsuariosExemplo() {
        const usuarios = [
            {
                id: 1,
                nome: 'Arthur Moraes',
                email: 'arthur.moraes@chvn.com.br',
                senha: '123456',
                ativo: 'S',
                cpf: '272.037.428-81',
                dataNascimento: '19/04/1975',
                dataCriacao: '25/02/2026, 09:00:00',
                criadoPor: 'Sistema',
                dataAlteracao: '25/02/2026, 12:35:00',
                alteradoPor: 'Sistema'
            }
        ];

        this.usuarios = usuarios;
        this.salvarUsuariosLocalStorage();
        this.renderUsuarios();
    }

    updateTableCounters() {
        // Método removido - contadores não são mais exibidos na interface
        return;
    }

    verInfoUsuario(id) {
        const usuario = this.usuarios.find(u => u.id === id);
        if (usuario) {
            alert(`Informações do usuário:\n\nID: ${usuario.id}\nNome: ${usuario.nome}\nEmail: ${usuario.email}\nStatus: ${usuario.ativo === 'S' ? 'Ativo' : 'Inativo'}\nCPF: ${usuario.cpf || 'Não informado'}\nData de Nascimento: ${usuario.dataNascimento || 'Não informada'}`);
        }
    }

    exportarUsuarios() {
        if (this.usuarios.length === 0) {
            this.showToast('Nenhum usuário para exportar', 'warning');
            return;
        }

        // Preparar dados para exportação
        const dadosExportacao = this.usuarios.map(usuario => ({
            'ID': usuario.id,
            'Nome': usuario.nome,
            'Email': usuario.email,
            'Status': usuario.ativo === 'S' ? 'Ativo' : 'Inativo',
            'Data Criação': usuario.dataCriacao || '',
            'Criado Por': usuario.criadoPor || ''
        }));

        // Converter para CSV
        const headers = Object.keys(dadosExportacao[0]);
        const csvContent = [
            headers.join(','),
            ...dadosExportacao.map(row => 
                headers.map(header => `"${row[header]}"`).join(',')
            )
        ].join('\n');

        // Criar e baixar arquivo
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        
        if (link.download !== undefined) {
            const url = URL.createObjectURL(blob);
            link.setAttribute('href', url);
            link.setAttribute('download', `usuarios_${new Date().toLocaleDateString('pt-BR').replace(/\//g, '-')}.csv`);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            this.showToast(`${this.usuarios.length} usuários exportados com sucesso!`, 'success');
        }
    }

    voltarParaDashboard() {
        this.showSection('dashboard');
    }

    logout() {
        // Redirecionar para a tela de login
        window.location.href = '../../tela2entrar/index.html';
    }

    salvarLocalStorage() {
        localStorage.setItem('produtos', JSON.stringify(this.produtos));
        localStorage.setItem('usuarios', JSON.stringify(this.usuarios));
        localStorage.setItem('locais', JSON.stringify(this.locais));
    }

    // FUNCIONALIDADES DE LOCAIS
    renderLocais() {
        const tbody = document.getElementById('locais-tbody');
        if (!tbody) return;

        // Inicializar locais se não existir
        if (!this.locais) {
            this.locais = JSON.parse(localStorage.getItem('locais')) || [];
            this.adicionarLocaisExemplo();
        }

        tbody.innerHTML = '';

        this.locais.forEach(local => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="checkbox-col">
                    <input type="checkbox" class="local-checkbox" data-id="${local.id}">
                </td>
                <td class="id-col">${local.id}</td>
                <td class="name-col">${local.nome}</td>
                <td class="description-col">${local.descricao || 'N/A'}</td>
                <td class="status-col">
                    <span class="status ${local.status.toLowerCase()}">${local.status}</span>
                </td>
                <td class="date-creation-col">${local.dataCriacao || 'N/A'}</td>
                <td class="created-by-col">${local.criadoPor || 'N/A'}</td>
                <td class="date-modification-col">${local.dataAlteracao || 'N/A'}</td>
                <td class="modified-by-col">${local.alteradoPor || 'N/A'}</td>
                <td class="actions-col">
                    <div class="actions">
                        <button class="btn-edit" onclick="estoque.abrirModalLocal(${JSON.stringify(local).replace(/"/g, '&quot;')})" title="Editar">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="m18.5 2.5 a2.12 2.12 0 0 1 3 3l-9.5 9.5-4 1 1-4 9.5-9.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                        <button class="btn-delete" onclick="estoque.excluirLocal(${local.id})" title="Excluir">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6h14ZM10 11v6M14 11v6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                    </div>
                </td>
            `;
            tbody.appendChild(row);
        });

        // Configurar botões específicos de locais
        this.setupBotoesLocais();
    }

    setupBotoesLocais() {
        const btnVoltar = document.getElementById('btn-voltar-dashboard-locais');
        const btnAdicionar = document.getElementById('btn-adicionar-local');
        const btnBuscar = document.getElementById('btn-buscar-locais');
        const btnLimpar = document.getElementById('btn-limpar-locais');
        
        if (btnVoltar) {
            btnVoltar.addEventListener('click', () => this.showSection('dashboard'));
        }
        
        if (btnAdicionar) {
            btnAdicionar.addEventListener('click', () => this.abrirModalLocal());
        }

        if (btnBuscar) {
            btnBuscar.addEventListener('click', () => this.aplicarFiltrosLocais());
        }

        if (btnLimpar) {
            btnLimpar.addEventListener('click', () => this.limparFiltrosLocais());
        }

        // Configurar filtros em tempo real
        const nomeInput = document.getElementById('nome-local-input');
        const descricaoInput = document.getElementById('descricao-local-input');

        if (nomeInput) {
            nomeInput.addEventListener('input', () => this.aplicarFiltrosLocais());
        }

        if (descricaoInput) {
            descricaoInput.addEventListener('input', () => this.aplicarFiltrosLocais());
        }
    }

    // FUNCIONALIDADES DO MODAL DE LOCAIS
    setupModalLocal() {
        const modal = document.getElementById('modal-local');
        const btnCancelar = document.getElementById('btn-cancelar-local');
        const closeBtn = document.getElementById('close-local');

        if (btnCancelar) {
            btnCancelar.addEventListener('click', () => this.fecharModalLocal());
        }
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.fecharModalLocal());
        }
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) this.fecharModalLocal();
            });
        }
    }

    setupFormLocal() {
        const form = document.getElementById('local-form');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.salvarLocal();
            });
        }
    }

    abrirModalLocal(local = null) {
        const modal = document.getElementById('modal-local');
        const modalTitle = document.getElementById('modal-local-title');
        const form = document.getElementById('local-form');
        
        this.localEditando = local;
        
        if (local) {
            modalTitle.textContent = 'Editar Local';
            this.preencherFormLocal(local);
        } else {
            modalTitle.textContent = 'Adicionar Local';
            form.reset();
            // Limpar apenas o campo de senha na criação
            document.getElementById('senha-confirmacao').value = '';
        }
        
        modal.classList.add('active');
    }

    fecharModalLocal() {
        const modal = document.getElementById('modal-local');
        modal.classList.remove('active');
        this.localEditando = null;
    }

    preencherFormLocal(local) {
        document.getElementById('nome-local').value = local.nome || '';
        document.getElementById('status-local').value = local.status || 'Ativo';
        // Limpar campo senha na edição (sempre exigir senha para confirmar alterações)
        document.getElementById('senha-confirmacao').value = '';
    }

    validarSenha(senha) {
        return senha === this.senhaUsuarioLogado;
    }

    salvarLocal() {
        const nome = document.getElementById('nome-local').value;
        const status = document.getElementById('status-local').value;
        const senhaConfirmacao = document.getElementById('senha-confirmacao').value;

        // Validar senha
        if (!this.validarSenha(senhaConfirmacao)) {
            this.showToast('Senha incorreta! Digite sua senha para confirmar as alterações.', 'error');
            return;
        }

        // Validar campos obrigatórios
        if (!nome.trim()) {
            this.showToast('O nome do local é obrigatório!', 'warning');
            return;
        }

        const agora = new Date().toLocaleString('pt-BR');

        // Calcular próximo ID sequencial
        let novoId;
        if (this.localEditando) {
            novoId = this.localEditando.id;
        } else {
            const maiorId = this.locais && this.locais.length > 0 ? Math.max(...this.locais.map(l => l.id)) : 0;
            novoId = maiorId + 1;
        }

        const novoLocal = {
            id: novoId,
            nome,
            descricao: this.localEditando ? this.localEditando.descricao : '',
            endereco: this.localEditando ? this.localEditando.endereco : '',
            capacidade: this.localEditando ? this.localEditando.capacidade : 0,
            responsavel: this.localEditando ? this.localEditando.responsavel : '',
            status,
            dataCriacao: this.localEditando ? this.localEditando.dataCriacao : agora,
            criadoPor: this.localEditando ? this.localEditando.criadoPor : this.usuarioLogado,
            dataAlteracao: agora,
            alteradoPor: this.usuarioLogado
        };

        // Inicializar array se não existir
        if (!this.locais) {
            this.locais = [];
        }

        if (this.localEditando) {
            const index = this.locais.findIndex(l => l.id === this.localEditando.id);
            this.locais[index] = novoLocal;
            this.showToast('Local atualizado com sucesso!', 'success');
        } else {
            this.locais.push(novoLocal);
            this.showToast('Local adicionado com sucesso!', 'success');
        }

        localStorage.setItem('locais', JSON.stringify(this.locais));
        this.renderLocais();
        this.fecharModalLocal();
    }

    excluirLocal(id) {
        this.localExcluindo = id;
        const modal = document.getElementById('modal-confirmacao-local');
        modal.classList.add('active');
    }

    setupModalConfirmacaoLocal() {
        const modal = document.getElementById('modal-confirmacao-local');
        const btnCancelar = document.getElementById('btn-cancelar-exclusao-local');
        const btnConfirmar = document.getElementById('btn-confirmar-exclusao-local');

        if (btnCancelar) {
            btnCancelar.addEventListener('click', () => this.fecharModalConfirmacaoLocal());
        }
        if (btnConfirmar) {
            btnConfirmar.addEventListener('click', () => this.confirmarExclusaoLocal());
        }
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) this.fecharModalConfirmacaoLocal();
            });
        }
    }

    fecharModalConfirmacaoLocal() {
        const modal = document.getElementById('modal-confirmacao-local');
        modal.classList.remove('active');
        this.localExcluindo = null;
    }

    confirmarExclusaoLocal() {
        if (this.localExcluindo) {
            this.locais = this.locais.filter(l => l.id !== this.localExcluindo);
            localStorage.setItem('locais', JSON.stringify(this.locais));
            this.renderLocais();
            this.showToast('Local excluído com sucesso!', 'success');
        }
        this.fecharModalConfirmacaoLocal();
    }

    aplicarFiltrosLocais() {
        const nome = document.getElementById('nome-local-input')?.value.toLowerCase() || '';
        const descricao = document.getElementById('descricao-local-input')?.value.toLowerCase() || '';

        let locaisFiltrados = this.locais;

        if (nome) {
            locaisFiltrados = locaisFiltrados.filter(local =>
                local.nome.toLowerCase().includes(nome)
            );
        }

        if (descricao) {
            locaisFiltrados = locaisFiltrados.filter(local =>
                local.descricao && local.descricao.toLowerCase().includes(descricao)
            );
        }

        this.renderLocaisFiltrados(locaisFiltrados);
    }

    renderLocaisFiltrados(locais) {
        const tbody = document.getElementById('locais-tbody');
        if (!tbody) return;

        tbody.innerHTML = '';

        locais.forEach(local => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="checkbox-col">
                    <input type="checkbox" class="local-checkbox" data-id="${local.id}">
                </td>
                <td class="id-col">${local.id}</td>
                <td class="name-col">${local.nome}</td>
                <td class="description-col">${local.descricao || 'N/A'}</td>
                <td class="status-col">
                    <span class="status ${local.status.toLowerCase()}">${local.status}</span>
                </td>
                <td class="date-creation-col">${local.dataCriacao || 'N/A'}</td>
                <td class="created-by-col">${local.criadoPor || 'N/A'}</td>
                <td class="date-modification-col">${local.dataAlteracao || 'N/A'}</td>
                <td class="modified-by-col">${local.alteradoPor || 'N/A'}</td>
                <td class="actions-col">
                    <div class="actions">
                        <button class="btn-edit" onclick="estoque.abrirModalLocal(${JSON.stringify(local).replace(/"/g, '&quot;')})" title="Editar">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="m18.5 2.5 a2.12 2.12 0 0 1 3 3l-9.5 9.5-4 1 1-4 9.5-9.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                        <button class="btn-delete" onclick="estoque.excluirLocal(${local.id})" title="Excluir">
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

    limparFiltrosLocais() {
        const nomeInput = document.getElementById('nome-local-input');
        const descricaoInput = document.getElementById('descricao-local-input');

        if (nomeInput) nomeInput.value = '';
        if (descricaoInput) descricaoInput.value = '';

        this.renderLocais();
        this.showToast('Filtros limpos!', 'info');
    }

    adicionarLocaisExemplo() {
        const locaisExemplo = [
            {
                id: 1,
                nome: 'Depósito Central',
                descricao: 'Depósito principal para armazenamento de produtos',
                endereco: 'Rua das Indústrias, 123',
                capacidade: 1000,
                responsavel: 'João Silva',
                status: 'Ativo',
                dataCriacao: '20/01/2026, 08:00:00',
                criadoPor: 'Sistema',
                dataAlteracao: '20/01/2026, 08:00:00',
                alteradoPor: 'Sistema'
            },
            {
                id: 2,
                nome: 'Armazém Norte',
                descricao: 'Armazém secundário zona norte',
                endereco: 'Av. Norte, 456',
                capacidade: 500,
                responsavel: 'Maria Santos',
                status: 'Ativo',
                dataCriacao: '22/01/2026, 10:30:00',
                criadoPor: 'Administrador',
                dataAlteracao: '25/02/2026, 14:20:00',
                alteradoPor: 'Maria'
            },
            {
                id: 3,
                nome: 'Galpão Sul',
                descricao: 'Galpão em manutenção',
                endereco: 'Rua Sul, 789',
                capacidade: 300,
                responsavel: 'Pedro Costa',
                status: 'Ativo',
                dataCriacao: '15/02/2026, 16:45:00',
                criadoPor: 'Pedro Costa',
                dataAlteracao: '09/03/2026, 09:30:00',
                alteradoPor: 'Administrador'
            }
        ];

        this.locais = locaisExemplo;
        localStorage.setItem('locais', JSON.stringify(this.locais));
    }

    // FUNCIONALIDADES DE TIPOS
    setupModalTipo() {
        const modal = document.getElementById('modal-tipo');
        const btnCancelar = document.getElementById('btn-cancelar-tipo');
        const closeBtn = document.getElementById('close-tipo');

        if (btnCancelar) {
            btnCancelar.addEventListener('click', () => this.fecharModalTipo());
        }
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.fecharModalTipo());
        }
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) this.fecharModalTipo();
            });
        }
    }

    setupFormTipo() {
        const form = document.getElementById('tipo-form');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.salvarTipo();
            });
        }
    }

    setupModalConfirmacaoTipo() {
        const modal = document.getElementById('modal-confirmacao-tipo');
        const btnCancelar = document.getElementById('btn-cancelar-exclusao-tipo');
        const btnConfirmar = document.getElementById('btn-confirmar-exclusao-tipo');

        if (btnCancelar) {
            btnCancelar.addEventListener('click', () => this.fecharModalConfirmacaoTipo());
        }
        if (btnConfirmar) {
            btnConfirmar.addEventListener('click', () => this.confirmarExclusaoTipo());
        }
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) this.fecharModalConfirmacaoTipo();
            });
        }
    }

    renderTipos() {
        const tbody = document.getElementById('tipos-tbody');
        if (!tbody) return;

        // Inicializar tipos se não existir
        if (!this.tipos || this.tipos.length === 0) {
            this.tipos = JSON.parse(localStorage.getItem('tipos')) || [];
            if (this.tipos.length === 0) {
                this.adicionarTiposExemplo();
            }
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
                <td class="category-col">${tipo.categoria}</td>
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
                        <button class="btn-edit" onclick="estoque.abrirModalTipo(${JSON.stringify(tipo).replace(/"/g, '&quot;')})" title="Editar">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="m18.5 2.5 a2.12 2.12 0 0 1 3 3l-9.5 9.5-4 1 1-4 9.5-9.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                        <button class="btn-delete" onclick="estoque.excluirTipo(${tipo.id})" title="Excluir">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6h14ZM10 11v6M14 11v6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                    </div>
                </td>
            `;
            tbody.appendChild(row);
        });

        // Configurar botões específicos de tipos
        this.setupBotoesTipos();
    }

    setupBotoesTipos() {
        const btnVoltar = document.getElementById('btn-voltar-dashboard-tipos');
        const btnAdicionar = document.getElementById('btn-adicionar-tipo');
        const btnBuscar = document.getElementById('btn-buscar-tipos');
        const btnLimpar = document.getElementById('btn-limpar-tipos');
        const btnFiltroAvancado = document.getElementById('btn-filtro-avancado-tipos');
        
        if (btnVoltar) {
            btnVoltar.removeEventListener('click', this.voltarParaDashboard);
            btnVoltar.addEventListener('click', () => this.showSection('dashboard'));
        }
        
        if (btnAdicionar) {
            btnAdicionar.removeEventListener('click', this.abrirModalTipo);
            btnAdicionar.addEventListener('click', () => this.abrirModalTipo());
        }

        if (btnBuscar) {
            btnBuscar.removeEventListener('click', this.aplicarFiltrosTipos);
            btnBuscar.addEventListener('click', () => {
                this.aplicarFiltrosTipos();
                this.showToast('Filtros aplicados!', 'info');
            });
        }

        if (btnLimpar) {
            btnLimpar.removeEventListener('click', this.limparFiltrosTipos);
            btnLimpar.addEventListener('click', () => this.limparFiltrosTipos());
        }

        if (btnFiltroAvancado) {
            btnFiltroAvancado.removeEventListener('click', this.toggleFiltroAvancadoTipos);
            btnFiltroAvancado.addEventListener('click', () => this.toggleFiltroAvancadoTipos());
        }

        // Configurar filtros em tempo real
        const nomeInput = document.getElementById('nome-tipo-input');
        const categoriaSelect = document.getElementById('categoria-tipo-select');

        if (nomeInput) {
            nomeInput.removeEventListener('input', this.aplicarFiltrosTipos);
            nomeInput.addEventListener('input', () => this.aplicarFiltrosTipos());
        }

        if (categoriaSelect) {
            categoriaSelect.removeEventListener('change', this.aplicarFiltrosTipos);
            categoriaSelect.addEventListener('change', () => this.aplicarFiltrosTipos());
        }
    }

    abrirModalTipo(tipo = null) {
        const modal = document.getElementById('modal-tipo');
        const modalTitle = document.getElementById('modal-tipo-title');
        const form = document.getElementById('tipo-form');
        
        this.tipoEditando = tipo;
        
        if (tipo) {
            modalTitle.textContent = 'Editar Tipo de Item';
            this.preencherFormTipo(tipo);
        } else {
            modalTitle.textContent = 'Adicionar Tipo de Item';
            form.reset();
        }
        
        modal.classList.add('active');
    }

    fecharModalTipo() {
        const modal = document.getElementById('modal-tipo');
        modal.classList.remove('active');
        this.tipoEditando = null;
    }

    preencherFormTipo(tipo) {
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

        // Validar campos obrigatórios
        if (!nome.trim()) {
            this.showToast('O nome do tipo é obrigatório!', 'warning');
            return;
        }

        if (!categoria) {
            this.showToast('A categoria é obrigatória!', 'warning');
            return;
        }

        const agora = new Date().toLocaleString('pt-BR');

        // Calcular próximo ID sequencial
        let novoId;
        if (this.tipoEditando) {
            novoId = this.tipoEditando.id;
        } else {
            const maiorId = this.tipos && this.tipos.length > 0 ? Math.max(...this.tipos.map(t => t.id)) : 0;
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

        // Inicializar array se não existir
        if (!this.tipos) {
            this.tipos = [];
        }

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
        this.fecharModalTipo();
    }

    excluirTipo(id) {
        this.tipoExcluindo = id;
        const modal = document.getElementById('modal-confirmacao-tipo');
        modal.classList.add('active');
    }

    fecharModalConfirmacaoTipo() {
        const modal = document.getElementById('modal-confirmacao-tipo');
        modal.classList.remove('active');
        this.tipoExcluindo = null;
    }

    confirmarExclusaoTipo() {
        if (this.tipoExcluindo) {
            this.tipos = this.tipos.filter(t => t.id !== this.tipoExcluindo);
            localStorage.setItem('tipos', JSON.stringify(this.tipos));
            this.renderTipos();
            this.showToast('Tipo de item excluído com sucesso!', 'success');
        }
        this.fecharModalConfirmacaoTipo();
    }

    aplicarFiltrosTipos() {
        const nome = document.getElementById('nome-tipo-input')?.value.toLowerCase() || '';
        const categoria = document.getElementById('categoria-tipo-select')?.value || '';

        let tiposFiltrados = this.tipos || [];

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
                <td class="category-col">${tipo.categoria}</td>
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
                        <button class="btn-edit" onclick="estoque.abrirModalTipo(${JSON.stringify(tipo).replace(/"/g, '&quot;')})" title="Editar">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="m18.5 2.5 a2.12 2.12 0 0 1 3 3l-9.5 9.5-4 1 1-4 9.5-9.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                        <button class="btn-delete" onclick="estoque.excluirTipo(${tipo.id})" title="Excluir">
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

    limparFiltrosTipos() {
        const nomeInput = document.getElementById('nome-tipo-input');
        const categoriaSelect = document.getElementById('categoria-tipo-select');

        if (nomeInput) nomeInput.value = '';
        if (categoriaSelect) categoriaSelect.value = '';

        this.renderTipos();
        this.showToast('Filtros limpos!', 'info');
    }

    toggleFiltroAvancadoTipos() {
        this.showToast('Filtro avançado de tipos em desenvolvimento', 'info');
    }

    adicionarTiposExemplo() {
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
                criadoPor: 'Administrador',
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
                criadoPor: 'Pedro Costa',
                dataAlteracao: '05/03/2026, 09:30:00',
                alteradoPor: 'Administrador'
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
                criadoPor: 'Técnico',
                dataAlteracao: '10/03/2026, 16:45:00',
                alteradoPor: 'Administrador'
            }
        ];

        this.tipos = tiposExemplo;
        localStorage.setItem('tipos', JSON.stringify(this.tipos));
    }
}

// Inicializar o sistema quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    window.estoque = new EstoqueManager();
});
