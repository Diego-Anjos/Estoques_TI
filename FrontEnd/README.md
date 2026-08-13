<<<<<<< HEAD
# Sistema de Controle de Estoque - Front-end

## Estrutura de Pastas Padronizada

### Organização Atual
```
front-end/
├── pages/                          # Páginas principais do sistema
│   ├── auth/                       # Páginas de autenticação
│   │   ├── login/                  # Página de login
│   │   │   ├── index.html
│   │   │   ├── style.css
│   │   │   └── script.js
│   │   └── dashboard/              # Dashboard inicial
│   │       ├── index.html
│   │       ├── style.css
│   │       └── script.js
│   ├── inventory/                  # Módulos do sistema de estoque
│   │   ├── items/                  # Cadastro de itens
│   │   │   ├── index.html
│   │   │   ├── style.css
│   │   │   └── script.js
│   │   ├── item-types/             # Tipos de item
│   │   │   ├── index.html
│   │   │   ├── style.css
│   │   │   └── script.js
│   │   ├── locations/              # Gestão de locais
│   │   │   ├── index.html
│   │   │   ├── style.css
│   │   │   └── script.js
│   │   └── stock-control/          # Controle de estoque
│   │       ├── index.html
│   │       ├── style.css
│   │       └── script.js
├── assets/                         # Recursos estáticos
│   ├── images/                     # Imagens
│   ├── fonts/                      # Fontes
│   └── icons/                      # Ícones
├── shared/                         # Componentes compartilhados
│   ├── css/                        # CSS global
│   │   ├── global.css              # Estilos globais
│   │   ├── components.css          # Componentes reutilizáveis
│   │   └── themes.css              # Temas (claro/escuro)
│   ├── js/                         # JavaScript global
│   │   ├── utils.js                # Utilitários
│   │   ├── api.js                  # Comunicação com API
│   │   └── components.js           # Componentes JS
│   └── components/                 # Componentes HTML reutilizáveis
│       ├── header/
│       ├── modals/
│       └── forms/
└── docs/                           # Documentação
    ├── README.md                   # Este arquivo
    ├── STRUCTURE.md                # Guia de estrutura
    └── CONVENTIONS.md              # Convenções de código
```

## Convenções de Nomenclatura

### Pastas
- Use kebab-case (palavras separadas por hífen)
- Nomes em inglês para consistência
- Organize por funcionalidade

### Arquivos
- index.html: Página principal do módulo
- style.css: Estilos específicos do módulo
- script.js: JavaScript específico do módulo

### Classes CSS
- Use BEM (Block Element Modifier) quando possível
- Prefixos específicos por módulo

### IDs e Variáveis JavaScript
- Use camelCase
- Nomes descritivos e específicos

## Padrões de Desenvolvimento

### Estrutura HTML
- DOCTYPE html5
- Meta viewport para responsividade
- Título descritivo específico por página
- Link para CSS local
- Script no final do body

### CSS
- Mobile-first approach
- CSS Variables para cores e espaçamentos
- Comentários organizacionais
- Separação por seções lógicas

### JavaScript
- ES6+ features
- Funções puras quando possível
- Event delegation
- Tratamento de erros consistente

## Migração da Estrutura Atual

### Mapeamento das pastas existentes:
- `tela1/` → `pages/auth/dashboard/`
- `tela2entrar/` → `pages/auth/login/`
- `cadastro-itens/` → `pages/inventory/items/`
- `tipos-item/` → `pages/inventory/item-types/`
- `Gestão de locais/` → `pages/inventory/locations/`
- `Controle de estoque/` → `pages/inventory/stock-control/`

### Próximos Passos:
1. Criar nova estrutura de pastas
2. Migrar arquivos existentes
3. Atualizar referências de caminhos
4. Implementar arquivos compartilhados
5. Documentar componentes reutilizáveis
=======
# Sistema-de-Estoque
Sistema de Estoque é uma aplicação web desenvolvida para facilitar a organização e o gerenciamento empresarial, permitindo o cadastro de produtos, empresas e usuários. O projeto segue em desenvolvimento, com novas funcionalidades sendo implementadas.
>>>>>>> 37c72df4ad5ce6c13c9fb5b90681731336b406dd
