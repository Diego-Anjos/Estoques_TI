# Guia de Estrutura do Projeto

## Estrutura Implementada

A estrutura do front-end foi reorganizada seguindo as melhores práticas de desenvolvimento web moderno:

```
front-end/
├── pages/                              # Páginas do sistema organizadas por módulo
│   ├── auth/                           # Módulo de autenticação
│   │   ├── login/                      # Página de login (migrado de tela2entrar/)
│   │   │   ├── index.html
│   │   │   ├── style.css
│   │   │   └── tela inicial.png
│   │   └── dashboard/                  # Dashboard principal (migrado de tela1/)
│   │       ├── index.html
│   │       ├── style.css
│   │       ├── tela inicial.png
│   │       └── paginainicial/
│   └── inventory/                      # Módulo de controle de estoque
│       ├── items/                      # Cadastro de itens (migrado de cadastro-itens/)
│       │   ├── index.html
│       │   ├── style.css
│       │   ├── script.js
│       │   └── Controle de Estoque/
│       ├── item-types/                 # Tipos de item (migrado de tipos-item/)
│       │   ├── index.html
│       │   ├── style.css
│       │   └── script.js
│       ├── locations/                  # Gestão de locais (migrado de Gestão de locais/)
│       │   ├── index.html
│       │   └── style.css
│       └── stock-control/              # Controle de estoque (migrado de Controle de estoque/)
│           ├── index.html
│           ├── style.css
│           └── script.js
├── assets/                             # Recursos estáticos
│   ├── images/                         # Imagens do projeto
│   │   ├── tela inicial.png
│   ├── fonts/                          # Fontes customizadas
│   └── icons/                          # Ícones do sistema
├── shared/                             # Recursos compartilhados
│   ├── css/                            # CSS global
│   │   └── global.css                  # Estilos globais e variáveis CSS
│   ├── js/                             # JavaScript compartilhado
│   │   └── utils.js                    # Utilitários JavaScript
│   └── components/                     # Componentes reutilizáveis
└── docs/                               # Documentação
    ├── README.md                       # Guia principal
    └── STRUCTURE.md                    # Este arquivo
```

## Benefícios da Nova Estrutura

### 1. **Organização Modular**
- Páginas agrupadas por funcionalidade (auth, inventory)
- Facilita manutenção e desenvolvimento em equipe
- Melhor compreensão da arquitetura do sistema

### 2. **Recursos Centralizados**
- Assets organizados por tipo (images, fonts, icons)
- CSS e JavaScript compartilhados em local específico
- Evita duplicação de código e recursos

### 3. **Escalabilidade**
- Estrutura preparada para crescimento do projeto
- Fácil adição de novos módulos e funcionalidades
- Padrão consistente em todo o projeto

### 4. **Manutenibilidade**
- Código mais fácil de localizar e manter
- Separação clara entre funcionalidades
- Documentação organizada

## Como Usar a Nova Estrutura

### Para Desenvolvedores

1. **Adicionando uma Nova Página:**
   ```
   pages/[modulo]/[nome-da-pagina]/
   ├── index.html
   ├── style.css
   └── script.js (se necessário)
   ```

2. **Usando Recursos Compartilhados:**
   ```html
   <!-- No HTML -->
   <link rel="stylesheet" href="../../../shared/css/global.css">
   <script type="module" src="../../../shared/js/utils.js"></script>
   ```

3. **Adicionando Assets:**
   - Imagens: `assets/images/`
   - Fontes: `assets/fonts/`
   - Ícones: `assets/icons/`

### Referências de Caminhos

**De uma página para recursos compartilhados:**
- CSS Global: `../../../shared/css/global.css`
- Utils JS: `../../../shared/js/utils.js`
- Imagens: `../../../assets/images/nome-imagem.png`

**Entre páginas do mesmo módulo:**
- `../outra-pagina/index.html`

**Entre módulos diferentes:**
- `../../outro-modulo/pagina/index.html`

## Próximos Passos Recomendados

1. **Atualizar referências** nos arquivos HTML existentes
2. **Implementar componentes** reutilizáveis em `shared/components/`
3. **Criar arquivo de temas** em `shared/css/themes.css`
4. **Adicionar API utilities** em `shared/js/api.js`
5. **Documentar componentes** criados

## Convenções de Nomenclatura

- **Pastas:** kebab-case (palavras-separadas-por-hifen)
- **Arquivos:** kebab-case para CSS/HTML, camelCase para JS
- **Classes CSS:** BEM ou kebab-case
- **IDs JavaScript:** camelCase
- **Variáveis CSS:** --kebab-case

## Estrutura Original → Nova Estrutura

| Estrutura Antiga | Nova Localização |
|-----------------|------------------|
| `tela2entrar/` | `pages/auth/login/` |
| `tela1/` | `pages/auth/dashboard/` |
| `cadastro-itens/` | `pages/inventory/items/` |
| `tipos-item/` | `pages/inventory/item-types/` |
| `Gestão de locais/` | `pages/inventory/locations/` |
| `Controle de estoque/` | `pages/inventory/stock-control/` |

Esta estrutura mantém todos os arquivos originais funcionando, mas organizados de forma mais profissional e escalável.