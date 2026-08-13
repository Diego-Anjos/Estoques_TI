"""
Script para cadastrar NOVOS dados em todas as 12 tabelas
Mantém os dados existentes intactos
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


def cadastrar_novos_dados():
    """Cadastra um conjunto completamente novo de dados"""
    print("=" * 80)
    print("🆕 CADASTRO DE NOVOS DADOS - SISTEMA DE ESTOQUE TI")
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
        
        # Timestamp único para evitar duplicatas
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # ========================================================================
        # CONTAGEM INICIAL
        # ========================================================================
        print("=" * 80)
        print("📊 CONTAGEM INICIAL DE REGISTROS")
        print("=" * 80)
        print()
        
        tabelas = {
            'USUARIOS': 'ESTOQUES_TI_USUARIOS',
            'LOCAIS': 'ESTOQUES_TI_LOCAIS',
            'TIPOS_ITEM': 'ESTOQUES_TI_TIPOS_ITEM',
            'ITENS': 'ESTOQUES_TI_ITENS',
            'ESTOQUE_SALDO': 'ESTOQUES_TI_ESTOQUE_SALDO',
            'MOVIMENTACOES': 'ESTOQUES_TI_MOVIMENTACOES',
            'PATRIMONIOS': 'ESTOQUES_TI_PATRIMONIOS',
            'PATRIMONIO_ATR': 'ESTOQUES_TI_PATRIMONIO_ATR',
            'SOFTWARES': 'ESTOQUES_TI_SOFTWARES',
            'SOFTWARE_LICENCAS': 'ESTOQUES_TI_SOFTWARE_LICENCAS',
            'ATRIBUICOES': 'ESTOQUES_TI_ATRIBUICOES',
            'OCORRENCIAS': 'ESTOQUES_TI_OCORRENCIAS'
        }
        
        contagem_inicial = {}
        for nome, tabela in tabelas.items():
            cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
            count = cursor.fetchone()[0]
            contagem_inicial[nome] = count
            print(f"   {nome:<20} {count} registro(s)")
        
        print()
        
        # ========================================================================
        # PARTE 1: Cadastrar Novo Usuário
        # ========================================================================
        print("=" * 80)
        print("📝 PARTE 1: Cadastrando Novo Usuário")
        print("=" * 80)
        
        sql_usuario = """
            INSERT INTO ESTOQUES_TI_USUARIOS (NOME, EMAIL, SENHA_HASH, ATIVO)
            VALUES (:nome, :email, :senha, :ativo)
            RETURNING ID_USUARIO INTO :id
        """
        
        id_usuario_var = cursor.var(int)
        cursor.execute(sql_usuario, {
            'nome': 'Maria Santos',
            'email': f'maria.santos{timestamp}@empresa.com',
            'senha': '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIxF6q0OXm',
            'ativo': 'S',
            'id': id_usuario_var
        })
        id_usuario = id_usuario_var.getvalue()[0]
        connection.commit()
        
        print(f"✅ Novo Usuário cadastrado com ID: {id_usuario}")
        print(f"   Nome: Maria Santos")
        print(f"   Email: maria.santos{timestamp}@empresa.com")
        print()
        
        # ========================================================================
        # PARTE 2: Cadastrar Novo Local
        # ========================================================================
        print("=" * 80)
        print("📝 PARTE 2: Cadastrando Novo Local")
        print("=" * 80)
        
        sql_local = """
            INSERT INTO ESTOQUES_TI_LOCAIS (NOME, DESCRICAO, CRIADO_POR)
            VALUES (:nome, :descricao, :criado_por)
            RETURNING ID_LOCAL INTO :id
        """
        
        id_local_var = cursor.var(int)
        cursor.execute(sql_local, {
            'nome': f'Departamento Financeiro - {timestamp}',
            'descricao': 'Setor responsável pela gestão financeira da empresa',
            'criado_por': id_usuario,
            'id': id_local_var
        })
        id_local = id_local_var.getvalue()[0]
        connection.commit()
        
        print(f"✅ Novo Local cadastrado com ID: {id_local}")
        print(f"   Nome: Departamento Financeiro")
        print(f"   Criado por: Usuário ID {id_usuario}")
        print()
        
        # ========================================================================
        # PARTE 3: Cadastrar Novo Tipo de Item
        # ========================================================================
        print("=" * 80)
        print("📝 PARTE 3: Cadastrando Novo Tipo de Item")
        print("=" * 80)
        
        sql_tipo = """
            INSERT INTO ESTOQUES_TI_TIPOS_ITEM (CODIGO, NOME, SERIALIZADO, UNIDADE, CRIADO_POR)
            VALUES (:codigo, :nome, :serializado, :unidade, :criado_por)
            RETURNING ID_TIPO_ITEM INTO :id
        """
        
        id_tipo_var = cursor.var(int)
        cursor.execute(sql_tipo, {
            'codigo': f'MON-{timestamp}',
            'nome': 'Monitor LED',
            'serializado': 'S',
            'unidade': 'UN',
            'criado_por': id_usuario,
            'id': id_tipo_var
        })
        id_tipo = id_tipo_var.getvalue()[0]
        connection.commit()
        
        print(f"✅ Novo Tipo de Item cadastrado com ID: {id_tipo}")
        print(f"   Código: MON-{timestamp}")
        print(f"   Nome: Monitor LED")
        print(f"   Serializado: Sim")
        print()
        
        # ========================================================================
        # PARTE 4: Cadastrar Novo Item
        # ========================================================================
        print("=" * 80)
        print("📝 PARTE 4: Cadastrando Novo Item")
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
            'nome': 'Samsung 27 polegadas 4K',
            'marca': 'Samsung',
            'modelo': 'LU28E590DS',
            'descricao': 'Monitor LED 27" 4K UHD, 60Hz, HDMI/DisplayPort',
            'estoque_min': 10,
            'criado_por': id_usuario,
            'id': id_item_var
        })
        id_item = id_item_var.getvalue()[0]
        connection.commit()
        
        print(f"✅ Novo Item cadastrado com ID: {id_item}")
        print(f"   Nome: Samsung 27 polegadas 4K")
        print(f"   Marca: Samsung")
        print(f"   Modelo: LU28E590DS")
        print(f"   Tipo: ID {id_tipo}")
        print()
        
        # ========================================================================
        # PARTE 5: Cadastrar Estoque Saldo
        # ========================================================================
        print("=" * 80)
        print("📝 PARTE 5: Cadastrando Estoque Saldo")
        print("=" * 80)
        
        cursor.execute("""
            INSERT INTO ESTOQUES_TI_ESTOQUE_SALDO (ID_ITEM, ID_LOCAL, QUANTIDADE, ALTERADO_POR)
            VALUES (:id_item, :id_local, :qtd, :usuario)
        """, {'id_item': id_item, 'id_local': id_local, 'qtd': 20, 'usuario': id_usuario})
        connection.commit()
        
        print(f"✅ Estoque Saldo cadastrado")
        print(f"   Item: {id_item} | Local: {id_local} | Quantidade: 20")
        print()
        
        # ========================================================================
        # PARTE 6: Cadastrar Movimentação
        # ========================================================================
        print("=" * 80)
        print("📝 PARTE 6: Cadastrando Movimentação")
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
            'qtd': 20,
            'tipo': 'ENTRADA',
            'motivo': 'Compra de monitores para o departamento financeiro',
            'usuario': id_usuario,
            'id': id_mov_var
        })
        id_movimentacao = id_mov_var.getvalue()[0]
        connection.commit()
        
        print(f"✅ Movimentação cadastrada com ID: {id_movimentacao}")
        print(f"   Tipo: ENTRADA | Quantidade: 20 | Item: {id_item}")
        print()
        
        # ========================================================================
        # PARTE 7: Cadastrar Patrimônio
        # ========================================================================
        print("=" * 80)
        print("📝 PARTE 7: Cadastrando Patrimônio")
        print("=" * 80)
        
        numero_serie = f"SNMON{timestamp}"
        numero_patrimonio = f"PAT-MON-{timestamp}"
        
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
            'data_compra': date(2026, 2, 20),
            'data_garantia': date(2029, 2, 20),
            'obs': 'Monitor novo, em perfeito estado',
            'usuario': id_usuario,
            'id': id_pat_var
        })
        id_patrimonio = id_pat_var.getvalue()[0]
        connection.commit()
        
        print(f"✅ Patrimônio cadastrado com ID: {id_patrimonio}")
        print(f"   Série: {numero_serie}")
        print(f"   Patrimônio: {numero_patrimonio}")
        print(f"   Status: EM_ESTOQUE")
        print()
        
        # ========================================================================
        # PARTE 8: Cadastrar Atributos do Patrimônio
        # ========================================================================
        print("=" * 80)
        print("📝 PARTE 8: Cadastrando Atributos do Patrimônio")
        print("=" * 80)
        
        atributos = [
            ('Resolução', '3840x2160 (4K UHD)'),
            ('Tamanho', '27 polegadas'),
            ('Tipo de Painel', 'TN'),
            ('Conexões', 'HDMI 1.4, DisplayPort 1.2')
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
        # PARTE 9: Cadastrar Software
        # ========================================================================
        print("=" * 80)
        print("📝 PARTE 9: Cadastrando Software")
        print("=" * 80)
        
        nome_software = f"Zoom Business - {timestamp}"
        
        sql_sw = """
            INSERT INTO ESTOQUES_TI_SOFTWARES 
            (NOME, FABRICANTE, DESCRICAO, CRIADO_POR)
            VALUES (:nome, :fabricante, :descricao, :usuario)
            RETURNING ID_SOFTWARE INTO :id
        """
        
        id_sw_var = cursor.var(int)
        cursor.execute(sql_sw, {
            'nome': nome_software,
            'fabricante': 'Zoom Video Communications',
            'descricao': 'Plataforma de videoconferência empresarial',
            'usuario': id_usuario,
            'id': id_sw_var
        })
        id_software = id_sw_var.getvalue()[0]
        connection.commit()
        
        print(f"✅ Software cadastrado com ID: {id_software}")
        print(f"   Nome: {nome_software}")
        print(f"   Fabricante: Zoom Video Communications")
        print()
        
        # ========================================================================
        # PARTE 10: Cadastrar Pool de Licenças
        # ========================================================================
        print("=" * 80)
        print("📝 PARTE 10: Cadastrando Pool de Licenças")
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
            'total': 100,
            'contrato': f'CONT-ZOOM-{timestamp}',
            'expiracao': date(2027, 12, 31),
            'usuario': id_usuario,
            'id': id_pool_var
        })
        id_pool = id_pool_var.getvalue()[0]
        connection.commit()
        
        print(f"✅ Pool de Licenças cadastrado com ID: {id_pool}")
        print(f"   Total de Licenças: 100")
        print(f"   Contrato: CONT-ZOOM-{timestamp}")
        print(f"   Expira em: 31/12/2027")
        print()
        
        # ========================================================================
        # PARTE 11: Cadastrar Atribuição de Licença
        # ========================================================================
        print("=" * 80)
        print("📝 PARTE 11: Cadastrando Atribuição de Licença")
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
            'obs': 'Licença Zoom para reuniões do departamento financeiro',
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
        # PARTE 12: Cadastrar Ocorrência
        # ========================================================================
        print("=" * 80)
        print("📝 PARTE 12: Cadastrando Ocorrência")
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
            'titulo': 'Monitor apresentando pixel queimado',
            'descricao': 'O monitor Samsung apresenta um pixel morto no canto superior direito. Solicito verificação da garantia.',
            'severidade': 'BAIXA',
            'status': 'ABERTA',
            'abriu': id_usuario,
            'solicitante': id_usuario,
            'patrimonio': id_patrimonio,
            'id': id_ocor_var
        })
        id_ocorrencia = id_ocor_var.getvalue()[0]
        connection.commit()
        
        print(f"✅ Ocorrência cadastrada com ID: {id_ocorrencia}")
        print(f"   Título: Monitor apresentando pixel queimado")
        print(f"   Severidade: BAIXA | Status: ABERTA")
        print(f"   Patrimônio: {id_patrimonio}")
        print()
        
        # ========================================================================
        # CONTAGEM FINAL
        # ========================================================================
        print("=" * 80)
        print("📊 CONTAGEM FINAL DE REGISTROS")
        print("=" * 80)
        print()
        
        print(f"{'TABELA':<20} {'ANTES':<10} {'DEPOIS':<10} {'NOVOS':<10}")
        print("-" * 50)
        
        for nome, tabela in tabelas.items():
            cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
            count_final = cursor.fetchone()[0]
            count_inicial = contagem_inicial[nome]
            novos = count_final - count_inicial
            print(f"{nome:<20} {count_inicial:<10} {count_final:<10} +{novos}")
        
        print()
        
        # ========================================================================
        # RESUMO FINAL
        # ========================================================================
        print("=" * 80)
        print("✅ RESUMO DOS NOVOS CADASTROS")
        print("=" * 80)
        print()
        print(f"   ✅ Usuário: ID {id_usuario} (Maria Santos)")
        print(f"   ✅ Local: ID {id_local} (Departamento Financeiro)")
        print(f"   ✅ Tipo de Item: ID {id_tipo} (Monitor LED)")
        print(f"   ✅ Item: ID {id_item} (Samsung 27' 4K)")
        print(f"   ✅ Estoque Saldo: 20 unidades")
        print(f"   ✅ Movimentação: ID {id_movimentacao} (ENTRADA)")
        print(f"   ✅ Patrimônio: ID {id_patrimonio}")
        print(f"   ✅ Atributos: 4 atributos cadastrados")
        print(f"   ✅ Software: ID {id_software} (Zoom Business)")
        print(f"   ✅ Pool Licenças: ID {id_pool} (100 licenças)")
        print(f"   ✅ Atribuição: ID {id_atribuicao}")
        print(f"   ✅ Ocorrência: ID {id_ocorrencia}")
        print()
        print("   ✅ Todas as 12 tabelas atualizadas")
        print("   ✅ Dados antigos preservados")
        print("   ✅ Novos relacionamentos criados")
        print()
        print("🎉 NOVOS DADOS CADASTRADOS COM SUCESSO!")
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
    sucesso = cadastrar_novos_dados()
    print()
    print("=" * 80)
    if sucesso:
        print("✅ CADASTRO DE NOVOS DADOS CONCLUÍDO COM SUCESSO!")
    else:
        print("❌ CADASTRO DE NOVOS DADOS FALHOU")
    print("=" * 80)
