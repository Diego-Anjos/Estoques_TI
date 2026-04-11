# 🔒 Segurança do Repositório Git - Sistema de Estoques de Computadores

## ✅ Arquivos Protegidos pelo .gitignore

Este documento lista todos os arquivos sensíveis que estão sendo **ignorados pelo Git** e **NÃO serão enviados** ao repositório remoto.

---

## 📁 Estrutura de Proteção

### 1. **Arquivo .gitignore Principal** (Raiz do Projeto)
Localização: `/.gitignore`

Protege:
- ✅ **Credenciais e Senhas**
  - `**/.env` - Arquivos de ambiente com senhas do banco de dados
  - `**/.env.local` - Variações de ambiente
  - `**/.env.production` - Ambiente de produção
  - `**/secrets.*` - Arquivos de segredos

- ✅ **Ambientes Virtuais Python**
  - `.venv/`, `venv/`, `env/` - Ambientes virtuais
  - `__pycache__/` - Cache Python
  - `*.pyc`, `*.pyo` - Bytecode compilado

- ✅ **Banco de Dados**
  - `*.sql.backup`, `*.sql.bak` - Backups de banco
  - `*.dump`, `*.dmp` - Dumps de banco
  - `*.db`, `*.sqlite` - Bancos locais

- ✅ **IDEs e Editores**
  - `.vscode/` - Configurações do VS Code
  - `.idea/` - Configurações do PyCharm

- ✅ **Logs e Temporários**
  - `*.log` - Arquivos de log
  - `*.tmp`, `*.temp` - Arquivos temporários

- ✅ **Certificados e Chaves**
  - `*.pem`, `*.key`, `*.cert` - Certificados SSL/TLS

---

### 2. **Backend/.gitignore**
Localização: `/Estoques_TI/Backend/.gitignore`

Proteção específica do backend Python:
- ✅ `.env` - **CRÍTICO**: Contém senha do Oracle
- ✅ `.venv/` - Ambiente virtual Python
- ✅ `__pycache__/` - Cache Python

---

### 3. **DB/.gitignore**
Localização: `/Estoques_TI/DB/.gitignore`

Proteção de arquivos de banco de dados:
- ✅ `*.sql.backup`, `*.sql.bak` - Backups
- ✅ `*.dump`, `*.dmp` - Dumps
- ✅ Diretórios: `backup/`, `dumps/`, `exports/`

---

## ⚠️ ATENÇÃO: Arquivo .env Detectado

### 🚨 Status Atual
- **Arquivo encontrado**: `Estoques_TI/Backend/.env`
- **Contém**: Credenciais reais do Oracle Database
  - Usuário: `vbicoop`
  - Senha: `Chvn2023!` ⚠️
  - DSN: Informações de conexão

### ✅ Proteção Ativa
- O arquivo `.env` **ESTÁ sendo ignorado** pelo Git
- **NÃO será enviado** ao repositório remoto
- Verificado com: `git check-ignore -v Estoques_TI/Backend/.env`

---

## 📋 Checklist de Segurança

Antes de fazer `git push`:

- [x] `.gitignore` criado na raiz do projeto
- [x] `.gitignore` específico para Backend
- [x] `.gitignore` específico para DB
- [x] Arquivo `.env` está sendo ignorado
- [x] Ambiente virtual `.venv` está sendo ignorado
- [x] Repositório Git inicializado
- [ ] **IMPORTANTE**: Verificar se `.env` nunca foi commitado antes

---

## 🔍 Como Verificar se Arquivos Sensíveis Estão Protegidos

Execute os seguintes comandos para verificar:

```bash
# Verificar se .env está sendo ignorado
git check-ignore -v Estoques_TI/Backend/.env

# Verificar status dos arquivos
git status

# Listar apenas arquivos que serão commitados
git status --short
```

**Resultado esperado**: O arquivo `.env` **NÃO deve aparecer** na lista de arquivos a serem commitados.

---

## ⚡ Comandos Úteis

### Verificar arquivos ignorados
```bash
git status --ignored
```

### Verificar se um arquivo específico está sendo ignorado
```bash
git check-ignore -v <caminho-do-arquivo>
```

### Ver o que será commitado
```bash
git status --short
```

---

## 🛡️ Boas Práticas de Segurança

1. ✅ **NUNCA** commite o arquivo `.env` com credenciais reais
2. ✅ Use `.env.example` como modelo (sem credenciais reais)
3. ✅ Mantenha senhas fortes e únicas
4. ✅ Rotacione senhas periodicamente
5. ✅ Use variáveis de ambiente em produção
6. ✅ Revise o `git status` antes de cada commit
7. ✅ Configure `.gitignore` ANTES do primeiro commit

---

## 📝 Arquivo .env.example

O arquivo `Estoques_TI/Backend/.env.example` serve como **modelo** e:
- ✅ **PODE** ser commitado (não contém credenciais reais)
- ✅ Mostra a estrutura necessária
- ✅ Contém instruções de uso
- ✅ Usa valores de exemplo (não reais)

---

## 🚀 Próximos Passos

Agora você pode fazer o commit inicial com segurança:

```bash
# Verificar o que será commitado
git status

# Adicionar arquivos (exceto os ignorados)
git add .

# Fazer o commit inicial
git commit -m "Initial commit: Sistema de Estoques de Computadores"

# Adicionar repositório remoto (se ainda não adicionou)
git remote add origin <URL-DO-SEU-REPOSITORIO>

# Enviar para o repositório remoto
git push -u origin master
```

---

## ✅ Resumo

- 🔒 **3 arquivos .gitignore** criados e configurados
- 🛡️ **Credenciais protegidas** - arquivo .env está sendo ignorado
- 📦 **Ambiente virtual protegido** - .venv não será enviado
- 🗄️ **Backups de banco protegidos** - dumps e backups ignorados
- ✅ **Pronto para subir ao repositório** com segurança

---

**Data de criação**: 10/04/2026  
**Última atualização**: 10/04/2026
