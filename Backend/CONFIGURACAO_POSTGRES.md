# Configuração PostgreSQL (Supabase) — Estoques TI

1. Copie `Backend/.env.example` para `Backend/.env`
2. Defina `DATABASE_URL` com a URI do Supabase:
   `postgresql://postgres:SENHA@db.PROJETO.supabase.co:5432/postgres?sslmode=require`
3. Instale dependências e crie as tabelas:
   ```bash
   pip install -r requirements.txt
   python init_db.py
   ```
4. Teste a conexão:
   ```bash
   python test_connection.py
   ```
5. Suba a API:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

O projeto usa **apenas PostgreSQL**. Documentação Oracle foi removida.
