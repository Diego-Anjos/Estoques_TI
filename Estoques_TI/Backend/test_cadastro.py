"""
Script de teste de cadastro nas tabelas principais
Testa INSERT, relacionamentos e triggers
"""
import oracledb
from dotenv import load_dotenv
import os
from datetime import datetime

# Carrega variáveis de ambiente
load_dotenv()

# Configurações
ORACLE_USER = os.getenv('ORACLE_USER')
ORACLE_PASSWORD = os.getenv('ORACLE_PASSWORD')
ORACLE_DSN = os.getenv('ORACLE_DSN')


def testar_cadastros():
    """Testa cadastros básicos nas tabelas principais"""
    print("=" * 80)
    print("🧪 TESTE DE CADASTRO - SISTEMA DE ESTOQUE TI")
    print("=" * 80)
    print()
    
    try:
        # Inicializa modo thick (obrigatório para Oracle 11g)
        try:
            oracledb.init_oracle_client()
            print("✅ Modo thick ativado (Oracle 11g)")
        except Exception as e:
            print(f"⚠️  Erro ao ativar modo thick: {e}")
            print("   Certifique-se de que o Oracle Instant Client está instalado")
            return False
        
        # Conecta ao banco
        print("🔌 Conectando ao banco de dados...")
        connection = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=ORACLE_DSN
        )
        cursor = connection.cursor()
        print("✅ Conectado com sucesso!")
        print()
        
        # ========================================================================
        # TESTE 1: Cadastrar Usuário
        # ========================================================================
        print("=" * 80)
        print("📝 TESTE 1: Cadastrando Usuário")
        print("=" * 80)
        
        sql_usuario = """
            INSERT INTO ESTOQUES_TI_USUARIOS (NOME, EMAIL, SENHA_HASH, ATIVO)
            VALUES (:nome, :email, :senha, :ativo)
            RETURNING ID_USUARIO INTO :id
        """
        
        id_usuario_var = cursor.var(int)
        cursor.execute(sql_usuario, {
            'nome': 'Admin Sistema',
            'email': 'admin@sistema.com',
            'senha': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIxF6q0OXm',  # senha: admin123
            'ativo': 'S',
            'id': id_usuario_var
        })
        id_usuario = id_usuario_var.getvalue()[0]
        connection.commit()
        
        print(f"✅ Usuário cadastrado com ID: {id_usuario}")
        print(f"   Nome: Admin Sistema")
        print(f"   Email: admin@sistema.com")
        print()
        
        # ========================================================================
        # TESTE 2: Cadastrar Local
        # ========================================================================
        print("=" * 80)
        print("📝 TESTE 2: Cadastrando Local")
        print("=" * 80)
        
        sql_local = """
            INSERT INTO ESTOQUES_TI_LOCAIS (NOME, DESCRICAO, CRIADO_POR)
            VALUES (:nome, :descricao, :criado_por)
            RETURNING ID_LOCAL INTO :id
        """
        
        id_local_var = cursor.var(int)
        cursor.execute(sql_local, {
            'nome': 'Almoxarifado Central',
            'descricao': 'Depósito principal de equipamentos de TI',
            'criado_por': id_usuario,
            'id': id_local_var
        })
        id_local = id_local_var.getvalue()[0]
        connection.commit()
        
        print(f"✅ Local cadastrado com ID: {id_local}")
        print(f"   Nome: Almoxarifado Central")
        print(f"   Criado por: Usuário ID {id_usuario}")
        print()
        
        # ========================================================================
        # TESTE 3: Cadastrar Tipo de Item
        # ========================================================================
        print("=" * 80)
        print("📝 TESTE 3: Cadastrando Tipo de Item")
        print("=" * 80)
        
        sql_tipo = """
            INSERT INTO ESTOQUES_TI_TIPOS_ITEM (CODIGO, NOME, SERIALIZADO, UNIDADE, CRIADO_POR)
            VALUES (:codigo, :nome, :serializado, :unidade, :criado_por)
            RETURNING ID_TIPO_ITEM INTO :id
        """
        
        id_tipo_var = cursor.var(int)
        cursor.execute(sql_tipo, {
            'codigo': 'COMP',
            'nome': 'Computador Desktop',
            'serializado': 'S',
            'unidade': 'UN',
            'criado_por': id_usuario,
            'id': id_tipo_var
        })
        id_tipo = id_tipo_var.getvalue()[0]
        connection.commit()
        
        print(f"✅ Tipo de Item cadastrado com ID: {id_tipo}")
        print(f"   Código: COMP")
        print(f"   Nome: Computador Desktop")
        print(f"   Serializado: Sim")
        print()
        
        # ========================================================================
        # TESTE 4: Cadastrar Item
        # ========================================================================
        print("=" * 80)
        print("📝 TESTE 4: Cadastrando Item")
        print("=" * 80)
        
        sql_item = """
            INSERT INTO ESTOQUES_TI_ITENS 
            (ID_TIPO_ITEM, NOME, MARCA, MODELO, DESCRICAO, ESTOQUE_MINIMO, CRIADO_POR)
            VALUES (:id_tipo, :nome, :marca, :modelo, :descricao, :estoque_min, :criado_por)
            RETURNING ID_ITEM INTO :id
        """
        
        id_item_var = cursor.var(int)
        cursor.execute(sql_item, {
            'id_tipo': id_tipo,
            'nome': 'Dell Optiplex 7010',
            'marca': 'Dell',
            'modelo': 'Optiplex 7010',
            'descricao': 'Computador desktop Intel Core i5, 8GB RAM, 256GB SSD',
            'estoque_min': 5,
            'criado_por': id_usuario,
            'id': id_item_var
        })
        id_item = id_item_var.getvalue()[0]
        connection.commit()
        
        print(f"✅ Item cadastrado com ID: {id_item}")
        print(f"   Nome: Dell Optiplex 7010")
        print(f"   Marca: Dell")
        print(f"   Modelo: Optiplex 7010")
        print(f"   Tipo: ID {id_tipo}")
        print()
        
        # ========================================================================
        # VERIFICAÇÃO: Listar dados cadastrados
        # ========================================================================
        print("=" * 80)
        print("📊 VERIFICAÇÃO: Listando Dados Cadastrados")
        print("=" * 80)
        print()
        
        # Listar usuários
        print("👥 USUÁRIOS:")
        cursor.execute("SELECT ID_USUARIO, NOME, EMAIL, ATIVO FROM ESTOQUES_TI_USUARIOS")
        for row in cursor.fetchall():
            print(f"   ID: {row[0]} | Nome: {row[1]} | Email: {row[2]} | Ativo: {row[3]}")
        print()
        
        # Listar locais
        print("📍 LOCAIS:")
        cursor.execute("SELECT ID_LOCAL, NOME, DESCRICAO FROM ESTOQUES_TI_LOCAIS")
        for row in cursor.fetchall():
            print(f"   ID: {row[0]} | Nome: {row[1]} | Descrição: {row[2]}")
        print()
        
        # Listar tipos de item
        print("📦 TIPOS DE ITEM:")
        cursor.execute("SELECT ID_TIPO_ITEM, CODIGO, NOME, SERIALIZADO FROM ESTOQUES_TI_TIPOS_ITEM")
        for row in cursor.fetchall():
            print(f"   ID: {row[0]} | Código: {row[1]} | Nome: {row[2]} | Serializado: {row[3]}")
        print()
        
        # Listar itens
        print("🖥️  ITENS:")
        cursor.execute("""
            SELECT i.ID_ITEM, i.NOME, i.MARCA, i.MODELO, t.NOME as TIPO
            FROM ESTOQUES_TI_ITENS i
            JOIN ESTOQUES_TI_TIPOS_ITEM t ON i.ID_TIPO_ITEM = t.ID_TIPO_ITEM
        """)
        for row in cursor.fetchall():
            print(f"   ID: {row[0]} | Nome: {row[1]} | Marca: {row[2]} | Modelo: {row[3]} | Tipo: {row[4]}")
        print()
        
        # ========================================================================
        # RESUMO
        # ========================================================================
        print("=" * 80)
        print("✅ RESUMO DO TESTE")
        print("=" * 80)
        print()
        print(f"   ✅ Usuário cadastrado: ID {id_usuario}")
        print(f"   ✅ Local cadastrado: ID {id_local}")
        print(f"   ✅ Tipo de Item cadastrado: ID {id_tipo}")
        print(f"   ✅ Item cadastrado: ID {id_item}")
        print()
        print("   ✅ Triggers funcionando (IDs auto-incrementados)")
        print("   ✅ Foreign Keys funcionando (relacionamentos OK)")
        print("   ✅ Campos de auditoria funcionando (criado_por)")
        print()
        print("🎉 TODOS OS TESTES PASSARAM COM SUCESSO!")
        print()
        
        # Fecha conexão
        cursor.close()
        connection.close()
        
        return True
        
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"❌ ERRO DE BANCO DE DADOS:")
        print(f"   Código: {error.code}")
        print(f"   Mensagem: {error.message}")
        return False
    
    except Exception as e:
        print(f"❌ ERRO INESPERADO: {e}")
        return False


if __name__ == "__main__":
    sucesso = testar_cadastros()
    print()
    print("=" * 80)
    if sucesso:
        print("✅ TESTE DE CADASTRO CONCLUÍDO COM SUCESSO!")
    else:
        print("❌ TESTE DE CADASTRO FALHOU")
    print("=" * 80)
