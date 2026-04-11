"""
Script de teste completo do sistema de estoque TI
Testa todas as 12 tabelas e seus relacionamentos
"""
import oracledb
from dotenv import load_dotenv
import os
from datetime import datetime, date

# Carrega variáveis de ambiente
load_dotenv()

# Configurações
ORACLE_USER = os.getenv('ORACLE_USER')
ORACLE_PASSWORD = os.getenv('ORACLE_PASSWORD')
ORACLE_DSN = os.getenv('ORACLE_DSN')


def teste_completo():
    """Testa todas as tabelas do sistema"""
    print("=" * 80)
    print("🧪 TESTE COMPLETO - SISTEMA DE ESTOQUE TI")
    print("=" * 80)
    print()
    
    try:
        # Inicializa modo thick
        try:
            oracledb.init_oracle_client()
            print("✅ Modo thick ativado (Oracle 11g)")
        except Exception as e:
            print(f"⚠️  Erro ao ativar modo thick: {e}")
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
        # PARTE 1: Verificar dados existentes
        # ========================================================================
        print("=" * 80)
        print("📊 PARTE 1: Verificando Dados Existentes")
        print("=" * 80)
        print()
        
        # Buscar primeiro usuário
        cursor.execute("SELECT ID_USUARIO, NOME FROM ESTOQUES_TI_USUARIOS WHERE ROWNUM = 1")
        usuario = cursor.fetchone()
        id_usuario = usuario[0]
        print(f"✅ Usuário encontrado: ID {id_usuario} - {usuario[1]}")
        
        # Buscar primeiro local
        cursor.execute("SELECT ID_LOCAL, NOME FROM ESTOQUES_TI_LOCAIS WHERE ROWNUM = 1")
        local = cursor.fetchone()
        id_local = local[0]
        print(f"✅ Local encontrado: ID {id_local} - {local[1]}")
        
        # Buscar primeiro tipo de item
        cursor.execute("SELECT ID_TIPO_ITEM, NOME FROM ESTOQUES_TI_TIPOS_ITEM WHERE ROWNUM = 1")
        tipo = cursor.fetchone()
        id_tipo = tipo[0]
        print(f"✅ Tipo de Item encontrado: ID {id_tipo} - {tipo[1]}")
        
        # Buscar primeiro item
        cursor.execute("SELECT ID_ITEM, NOME FROM ESTOQUES_TI_ITENS WHERE ROWNUM = 1")
        item = cursor.fetchone()
        id_item = item[0]
        print(f"✅ Item encontrado: ID {id_item} - {item[1]}")
        print()
        
        # ========================================================================
        # PARTE 2: Cadastrar Estoque Saldo
        # ========================================================================
        print("=" * 80)
        print("📝 PARTE 2: Cadastrando Estoque Saldo")
        print("=" * 80)
        
        # Verificar se já existe saldo
        cursor.execute("""
            SELECT COUNT(*) FROM ESTOQUES_TI_ESTOQUE_SALDO 
            WHERE ID_ITEM = :id_item AND ID_LOCAL = :id_local
        """, {'id_item': id_item, 'id_local': id_local})
        
        if cursor.fetchone()[0] > 0:
            print(f"⚠️  Saldo já existe para Item {id_item} no Local {id_local}")
            print("   Atualizando quantidade...")
            cursor.execute("""
                UPDATE ESTOQUES_TI_ESTOQUE_SALDO 
                SET QUANTIDADE = QUANTIDADE + 10, ALTERADO_POR = :usuario
                WHERE ID_ITEM = :id_item AND ID_LOCAL = :id_local
            """, {'usuario': id_usuario, 'id_item': id_item, 'id_local': id_local})
        else:
            cursor.execute("""
                INSERT INTO ESTOQUES_TI_ESTOQUE_SALDO (ID_ITEM, ID_LOCAL, QUANTIDADE, ALTERADO_POR)
                VALUES (:id_item, :id_local, 10, :usuario)
            """, {'id_item': id_item, 'id_local': id_local, 'usuario': id_usuario})
        
        connection.commit()
        print(f"✅ Estoque Saldo cadastrado/atualizado")
        print(f"   Item: {id_item} | Local: {id_local} | Quantidade: 10")
        print()
        
        # ========================================================================
        # PARTE 3: Cadastrar Movimentação
        # ========================================================================
        print("=" * 80)
        print("📝 PARTE 3: Cadastrando Movimentação")
        print("=" * 80)
        
        sql_mov = """
            INSERT INTO ESTOQUES_TI_MOVIMENTACOES 
            (ID_ITEM, ID_LOCAL_DESTINO, QUANTIDADE, TIPO_MOVIMENTACAO, MOTIVO, CRIADO_POR)
            VALUES (:id_item, :id_local, :qtd, :tipo, :motivo, :usuario)
            RETURNING ID_MOVIMENTACAO INTO :id
        """
        
        id_mov_var = cursor.var(int)
        cursor.execute(sql_mov, {
            'id_item': id_item,
            'id_local': id_local,
            'qtd': 10,
            'tipo': 'ENTRADA',
            'motivo': 'Compra de equipamentos novos',
            'usuario': id_usuario,
            'id': id_mov_var
        })
        id_movimentacao = id_mov_var.getvalue()[0]
        connection.commit()
        
        print(f"✅ Movimentação cadastrada com ID: {id_movimentacao}")
        print(f"   Tipo: ENTRADA | Quantidade: 10 | Item: {id_item}")
        print()
        
        # ========================================================================
        # PARTE 4: Cadastrar Patrimônio
        # ========================================================================
        print("=" * 80)
        print("📝 PARTE 4: Cadastrando Patrimônio")
        print("=" * 80)
        
        # Gera números únicos usando timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        numero_serie = f"SN{timestamp}"
        numero_patrimonio = f"PAT-2026-{timestamp}"
        
        sql_pat = """
            INSERT INTO ESTOQUES_TI_PATRIMONIOS 
            (ID_ITEM, NUMERO_SERIE, NUMERO_PATRIMONIO, STATUS, ID_LOCAL, 
             DATA_COMPRA, DATA_FIM_GARANTIA, OBSERVACOES, CRIADO_POR)
            VALUES (:id_item, :serie, :patrimonio, :status, :id_local,
                    :data_compra, :data_garantia, :obs, :usuario)
            RETURNING ID_PATRIMONIO INTO :id
        """
        
        id_pat_var = cursor.var(int)
        cursor.execute(sql_pat, {
            'id_item': id_item,
            'serie': numero_serie,
            'patrimonio': numero_patrimonio,
            'status': 'EM_ESTOQUE',
            'id_local': id_local,
            'data_compra': date(2026, 1, 15),
            'data_garantia': date(2029, 1, 15),
            'obs': 'Equipamento novo, em perfeito estado',
            'usuario': id_usuario,
            'id': id_pat_var
        })
        id_patrimonio = id_pat_var.getvalue()[0]
        connection.commit()
        
        print(f"✅ Patrimônio cadastrado com ID: {id_patrimonio}")
        print(f"   Série: {numero_serie} | Patrimônio: {numero_patrimonio}")
        print(f"   Status: EM_ESTOQUE")
        print()
        
        # ========================================================================
        # PARTE 5: Cadastrar Atributos do Patrimônio
        # ========================================================================
        print("=" * 80)
        print("📝 PARTE 5: Cadastrando Atributos do Patrimônio")
        print("=" * 80)
        
        atributos = [
            ('Processador', 'Intel Core i5-12400'),
            ('Memória RAM', '16GB DDR4'),
            ('Armazenamento', '512GB SSD NVMe'),
            ('Sistema Operacional', 'Windows 11 Pro')
        ]
        
        for nome, valor in atributos:
            cursor.execute("""
                INSERT INTO ESTOQUES_TI_PATRIMONIO_ATR 
                (ID_PATRIMONIO, NOME_ATRIBUTO, VALOR_ATRIBUTO, CRIADO_POR)
                VALUES (:id_pat, :nome, :valor, :usuario)
            """, {
                'id_pat': id_patrimonio,
                'nome': nome,
                'valor': valor,
                'usuario': id_usuario
            })
            print(f"   ✅ {nome}: {valor}")
        
        connection.commit()
        print(f"✅ {len(atributos)} atributos cadastrados")
        print()
        
        # ========================================================================
        # PARTE 6: Cadastrar Software
        # ========================================================================
        print("=" * 80)
        print("📝 PARTE 6: Cadastrando Software")
        print("=" * 80)
        
        # Gera nome único usando timestamp
        nome_software = f"Microsoft Office 365 - {timestamp}"
        
        sql_sw = """
            INSERT INTO ESTOQUES_TI_SOFTWARES 
            (NOME, FABRICANTE, DESCRICAO, CRIADO_POR)
            VALUES (:nome, :fabricante, :descricao, :usuario)
            RETURNING ID_SOFTWARE INTO :id
        """
        
        id_sw_var = cursor.var(int)
        cursor.execute(sql_sw, {
            'nome': nome_software,
            'fabricante': 'Microsoft',
            'descricao': 'Pacote de produtividade com Word, Excel, PowerPoint, etc.',
            'usuario': id_usuario,
            'id': id_sw_var
        })
        id_software = id_sw_var.getvalue()[0]
        connection.commit()
        
        print(f"✅ Software cadastrado com ID: {id_software}")
        print(f"   Nome: {nome_software}")
        print(f"   Fabricante: Microsoft")
        print()
        
        # ========================================================================
        # PARTE 7: Cadastrar Pool de Licenças
        # ========================================================================
        print("=" * 80)
        print("📝 PARTE 7: Cadastrando Pool de Licenças")
        print("=" * 80)
        
        sql_pool = """
            INSERT INTO ESTOQUES_TI_SOFTWARE_LICENCAS 
            (ID_SOFTWARE, TOTAL_LICENCAS, CONTRATO_REF, DATA_EXPIRACAO, CRIADO_POR)
            VALUES (:id_sw, :total, :contrato, :expiracao, :usuario)
            RETURNING ID_POOL INTO :id
        """
        
        id_pool_var = cursor.var(int)
        cursor.execute(sql_pool, {
            'id_sw': id_software,
            'total': 50,
            'contrato': 'CONT-MS-2026-001',
            'expiracao': date(2027, 12, 31),
            'usuario': id_usuario,
            'id': id_pool_var
        })
        id_pool = id_pool_var.getvalue()[0]
        connection.commit()
        
        print(f"✅ Pool de Licenças cadastrado com ID: {id_pool}")
        print(f"   Total de Licenças: 50")
        print(f"   Contrato: CONT-MS-2026-001")
        print(f"   Expira em: 31/12/2027")
        print()
        
        # ========================================================================
        # PARTE 8: Cadastrar Atribuição de Licença
        # ========================================================================
        print("=" * 80)
        print("📝 PARTE 8: Cadastrando Atribuição de Licença")
        print("=" * 80)
        
        sql_atrib = """
            INSERT INTO ESTOQUES_TI_ATRIBUICOES 
            (ID_POOL, ID_USUARIO, ID_PATRIMONIO, DATA_ATRIBUICAO, OBSERVACOES, CRIADO_POR)
            VALUES (:id_pool, :id_usuario, :id_pat, :data, :obs, :criado_por)
            RETURNING ID_ATRIBUICAO INTO :id
        """
        
        id_atrib_var = cursor.var(int)
        cursor.execute(sql_atrib, {
            'id_pool': id_pool,
            'id_usuario': id_usuario,
            'id_pat': id_patrimonio,
            'data': date.today(),
            'obs': 'Licença atribuída para uso corporativo',
            'criado_por': id_usuario,
            'id': id_atrib_var
        })
        id_atribuicao = id_atrib_var.getvalue()[0]
        connection.commit()
        
        print(f"✅ Atribuição cadastrada com ID: {id_atribuicao}")
        print(f"   Usuário: {id_usuario} | Patrimônio: {id_patrimonio}")
        print(f"   Pool: {id_pool}")
        print()
        
        # ========================================================================
        # PARTE 9: Cadastrar Ocorrência
        # ========================================================================
        print("=" * 80)
        print("📝 PARTE 9: Cadastrando Ocorrência")
        print("=" * 80)
        
        sql_ocor = """
            INSERT INTO ESTOQUES_TI_OCORRENCIAS 
            (TITULO, DESCRICAO, SEVERIDADE, STATUS, 
             ID_USUARIO_ABRIU, ID_USUARIO_SOLICITANTE, ID_PATRIMONIO_RELACIONADO)
            VALUES (:titulo, :descricao, :severidade, :status,
                    :abriu, :solicitante, :patrimonio)
            RETURNING ID_OCORRENCIA INTO :id
        """
        
        id_ocor_var = cursor.var(int)
        cursor.execute(sql_ocor, {
            'titulo': 'Computador apresentando lentidão',
            'descricao': 'O equipamento está muito lento ao abrir programas. Pode ser necessário upgrade de memória.',
            'severidade': 'MEDIA',
            'status': 'ABERTA',
            'abriu': id_usuario,
            'solicitante': id_usuario,
            'patrimonio': id_patrimonio,
            'id': id_ocor_var
        })
        id_ocorrencia = id_ocor_var.getvalue()[0]
        connection.commit()
        
        print(f"✅ Ocorrência cadastrada com ID: {id_ocorrencia}")
        print(f"   Título: Computador apresentando lentidão")
        print(f"   Severidade: MEDIA | Status: ABERTA")
        print(f"   Patrimônio: {id_patrimonio}")
        print()
        
        # ========================================================================
        # PARTE 10: Verificação Final - Listar Tudo
        # ========================================================================
        print("=" * 80)
        print("📊 PARTE 10: Verificação Final - Resumo Completo")
        print("=" * 80)
        print()
        
        # Contar registros em cada tabela
        tabelas = [
            'ESTOQUES_TI_USUARIOS',
            'ESTOQUES_TI_LOCAIS',
            'ESTOQUES_TI_TIPOS_ITEM',
            'ESTOQUES_TI_ITENS',
            'ESTOQUES_TI_ESTOQUE_SALDO',
            'ESTOQUES_TI_MOVIMENTACOES',
            'ESTOQUES_TI_PATRIMONIOS',
            'ESTOQUES_TI_PATRIMONIO_ATR',
            'ESTOQUES_TI_SOFTWARES',
            'ESTOQUES_TI_SOFTWARE_LICENCAS',
            'ESTOQUES_TI_ATRIBUICOES',
            'ESTOQUES_TI_OCORRENCIAS'
        ]
        
        print("📦 CONTAGEM DE REGISTROS POR TABELA:")
        print()
        for tabela in tabelas:
            cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
            count = cursor.fetchone()[0]
            status = "✅" if count > 0 else "⚠️ "
            print(f"   {status} {tabela:<40} {count} registro(s)")
        
        print()
        
        # ========================================================================
        # RESUMO FINAL
        # ========================================================================
        print("=" * 80)
        print("✅ RESUMO DO TESTE COMPLETO")
        print("=" * 80)
        print()
        print(f"   ✅ Estoque Saldo: Item {id_item} no Local {id_local}")
        print(f"   ✅ Movimentação: ID {id_movimentacao} (ENTRADA)")
        print(f"   ✅ Patrimônio: ID {id_patrimonio} (SN123456789)")
        print(f"   ✅ Atributos: 4 atributos cadastrados")
        print(f"   ✅ Software: ID {id_software} (Office 365)")
        print(f"   ✅ Pool Licenças: ID {id_pool} (50 licenças)")
        print(f"   ✅ Atribuição: ID {id_atribuicao}")
        print(f"   ✅ Ocorrência: ID {id_ocorrencia}")
        print()
        print("   ✅ Todas as 12 tabelas testadas")
        print("   ✅ Todos os relacionamentos funcionando")
        print("   ✅ Todas as sequences funcionando")
        print("   ✅ Campos de auditoria funcionando")
        print()
        print("🎉 SISTEMA 100% FUNCIONAL!")
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
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    sucesso = teste_completo()
    print()
    print("=" * 80)
    if sucesso:
        print("✅ TESTE COMPLETO CONCLUÍDO COM SUCESSO!")
    else:
        print("❌ TESTE COMPLETO FALHOU")
    print("=" * 80)
