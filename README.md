# 📦 Estoques TI

![Status](https://img.shields.io/badge/Status-Concluído-success?style=for-the-badge)
![Versão](https://img.shields.io/badge/Versão-1.0-blue?style=for-the-badge)

Um sistema completo, seguro e robusto para gestão de inventário focado em **Equipamentos de TI**. Desenvolvido para facilitar o controle de ativos, rastrear movimentações (Entradas, Saídas e Devoluções por setor) e gerenciar ocorrências, garantindo a integridade dos dados e a segurança das operações[cite: 1].

---

## 💡 A Ideia do Projeto

O **Estoques TI** nasceu da necessidade de modernizar e organizar o fluxo de equipamentos de tecnologia dentro de uma empresa[cite: 1]. Em vez de usar planilhas genéricas que podem gerar furos no estoque, o sistema garante[cite: 1]:
- **Lock Transacional:** Previne saldo negativo caso duas pessoas tentem retirar o mesmo equipamento ao mesmo tempo[cite: 1].
- **Rastreabilidade:** Saiba exatamente para qual setor (ex: RH, Financeiro) um equipamento foi enviado ou de onde foi devolvido[cite: 1].
- **Segurança:** Autenticação via token JWT e proteção contra exclusão indevida de dados (Soft Delete e proteção de chaves estrangeiras)[cite: 1].

---

## 🚀 Tecnologias Utilizadas

### Backend
- **Python 3**[cite: 1]
- **FastAPI** (Framework web super rápido)[cite: 1]
- **SQLAlchemy** (ORM para comunicação com o banco)[cite: 1]
- **Uvicorn** (Servidor ASGI)[cite: 1]
- **JWT** (Autenticação e segurança)[cite: 1]

### Frontend
- **HTML5 / CSS3 / JavaScript Vanilla** (Sem frameworks pesados)[cite: 1]
- **Vite** (Bundler para servidor de desenvolvimento ultrarrápido)[cite: 1]
- **Design Responsivo & Tema Escuro/Claro**[cite: 1]

### Banco de Dados & Infra
- **Oracle Database**[cite: 1]
- **Docker & Docker Compose**[cite: 1]

---

## ⚙️ Como Instalar e Rodar no seu PC

### Pré-requisitos
Certifique-se de ter instalado em sua máquina[cite: 1]:
- [Git](https://git-scm.com/)[cite: 1]
- [Docker Desktop](https://www.docker.com/products/docker-desktop)[cite: 1]
- [Python 3.10+](https://www.python.org/)[cite: 1]
- [Node.js & npm](https://nodejs.org/)[cite: 1]

### Passo a Passo

**1. Clone o repositório**
```bash
git clone [https://github.com/Diego-Anjos/Estoques_TI.git](https://github.com/Diego-Anjos/Estoques_TI.git)
cd "Estoques TI"
```

**2. Suba o Banco de Dados Oracle (Docker)**
Abra o seu terminal (Git Bash ou PowerShell) e rode[cite: 1]:
```bash
cd Backend
docker-compose up -d
```
*Aguarde alguns instantes até o banco Oracle inicializar por completo.*[cite: 1]

**3. Rode a API (Backend)**
> ⚠️ **Atenção (Usuários de Windows):** É muito importante configurar o encoding para UTF-8 no terminal para evitar travamentos durante a inicialização (devido a emojis e caracteres especiais)[cite: 1].

Abra um terminal **PowerShell**, certifique-se de estar dentro da pasta `Backend` e rode[cite: 1]:
```powershell
cd Backend
$env:PYTHONIOENCODING="utf-8"
$env:PYTHONUTF8="1"
.\`.venv\Scripts\uvicorn` app.main:app --reload --host 127.0.0.1 --port 8000
```
*A API estará disponível em `http://127.0.0.1:8000` (Documentação Swagger em `/docs`)[cite: 1].*

*(Se usar Git Bash, substitua `$env:VAR="valor"` por `export VAR="valor"` e use barras normais `./.venv/...`)[cite: 1].*

**4. Rode o Frontend**
Abra um **novo terminal**, vá para a pasta Frontend e inicie o servidor com Vite[cite: 1]:
```bash
cd Frontend
npm install
npm run dev
```
*Acesse a interface em `http://localhost:5173`.*[cite: 1]

---

## 👥 Desenvolvedores

Projeto criado e desenvolvido com dedicação por[cite: 1]:

* **Diego Anjos**[cite: 1]
* **Maria Tavares**[cite: 1]

---
*Transformando o caos do estoque de TI em um processo simples e seguro.* 🚀💻[cite: 1]
