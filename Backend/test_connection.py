"""
Script de teste de conexão com Oracle Database
Verifica se todas as tabelas do sistema existem
"""
import oracledb
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente
load_dotenv()

# Configurações
ORACLE_USER = os.getenv('ORACLE_USER')
ORACLE_PASSWORD = os.getenv('ORACLE_PASSWORD')
ORACLE_DSN = os.getenv('ORACLE_DSN')

# Lista de tabelas esperadas no banco de dados
TABELAS_ESPERADAS = [
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

# Sequences esperadas
SEQUENCES_ESPERADAS = [
    'ESTOQUES_TI_SEQ_USR',
    'ESTOQUES_TI_SEQ_LOC',
    'ESTOQUES_TI_SEQ_TPI',
    'ESTOQUES_TI_SEQ_IT',
    'ESTOQUES_TI_SEQ_EMV',
    'ESTOQUES_TI_SEQ_PAT',
    'ESTOQUES_TI_SEQ_SW',
    'ESTOQUES_TI_SEQ_SLP',
    'ESTOQUES_TI_SEQ_SAT',
    'ESTOQUES_TI_SEQ_OCO'
]


def testar_conexao():
    """Testa a conexão com o banco Oracle"""
    print("=" * 80)
    print("🔍 TESTE DE CONEXÃO COM ORACLE DATABASE")
    print("=" * 80)
    print()
    
    # Verifica se as variáveis de ambiente estão configuradas
    print("📋 Verificando configurações...")
    print(f"   ORACLE_USER: {ORACLE_USER}")
    print(f"   ORACLE_PASSWORD: {'*' * len(ORACLE_PASSWORD) if ORACLE_PASSWORD else 'NÃO CONFIGURADO'}")
    print(f"   ORACLE_DSN: {ORACLE_DSN}")
    print()
    
    if not all([ORACLE_USER, ORACLE_PASSWORD, ORACLE_DSN]):
        print("❌ ERRO: Variáveis de ambiente não configuradas corretamente!")
        print("   Configure o arquivo .env com as credenciais corretas.")
        return False
    
    try:
        # Inicializa o cliente Oracle em modo thick para suportar versões antigas
        try:
            oracledb.init_oracle_client()
            print("✅ Modo thick ativado (suporte para Oracle 11g)")
        except Exception as e:
            print(f"⚠️  Modo thick não disponível: {e}")
            print("   Tentando em modo thin...")
        
        # Tenta conectar
        print("🔌 Tentando conectar ao banco de dados...")
        connection = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=ORACLE_DSN
        )
        print("✅ Conexão estabelecida com sucesso!")
        print()
        
        # Verifica versão do Oracle
        cursor = connection.cursor()
        cursor.execute("SELECT BANNER FROM V$VERSION WHERE ROWNUM = 1")
        versao = cursor.fetchone()[0]
        print(f"📊 Versão do Oracle: {versao}")
        print()
        
        # Verifica usuário atual
        cursor.execute("SELECT USER FROM DUAL")
        usuario_atual = cursor.fetchone()[0]
        print(f"👤 Usuário conectado: {usuario_atual}")
        print()
        
        # Verifica tabelas
        print("=" * 80)
        print("📦 VERIFICANDO TABELAS")
        print("=" * 80)
        print()
        
        tabelas_encontradas = []
        tabelas_faltando = []
        
        for tabela in TABELAS_ESPERADAS:
            cursor.execute("""
                SELECT COUNT(*) 
                FROM USER_TABLES 
                WHERE TABLE_NAME = :nome
            """, {'nome': tabela})
            
            existe = cursor.fetchone()[0] > 0
            
            if existe:
                # Conta registros
                cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
                count = cursor.fetchone()[0]
                print(f"   ✅ {tabela:<35} ({count} registros)")
                tabelas_encontradas.append(tabela)
            else:
                print(f"   ❌ {tabela:<35} (NÃO ENCONTRADA)")
                tabelas_faltando.append(tabela)
        
        print()
        
        # Verifica sequences
        print("=" * 80)
        print("🔢 VERIFICANDO SEQUENCES")
        print("=" * 80)
        print()
        
        sequences_encontradas = []
        sequences_faltando = []
        
        for sequence in SEQUENCES_ESPERADAS:
            cursor.execute("""
                SELECT COUNT(*) 
                FROM USER_SEQUENCES 
                WHERE SEQUENCE_NAME = :nome
            """, {'nome': sequence})
            
            existe = cursor.fetchone()[0] > 0
            
            if existe:
                # Pega valor atual
                cursor.execute(f"SELECT {sequence}.CURRVAL FROM DUAL")
                try:
                    valor = cursor.fetchone()[0]
                    print(f"   ✅ {sequence:<35} (valor atual: {valor})")
                except:
                    print(f"   ✅ {sequence:<35} (não inicializada)")
                sequences_encontradas.append(sequence)
            else:
                print(f"   ❌ {sequence:<35} (NÃO ENCONTRADA)")
                sequences_faltando.append(sequence)
        
        print()
        
        # Resumo
        print("=" * 80)
        print("📊 RESUMO")
        print("=" * 80)
        print()
        print(f"   Tabelas encontradas: {len(tabelas_encontradas)}/{len(TABELAS_ESPERADAS)}")
        print(f"   Sequences encontradas: {len(sequences_encontradas)}/{len(SEQUENCES_ESPERADAS)}")
        print()
        
        if tabelas_faltando:
            print("⚠️  ATENÇÃO: As seguintes tabelas não foram encontradas:")
            for tabela in tabelas_faltando:
                print(f"      - {tabela}")
            print()
        
        if sequences_faltando:
            print("⚠️  ATENÇÃO: As seguintes sequences não foram encontradas:")
            for sequence in sequences_faltando:
                print(f"      - {sequence}")
            print()
        
        if not tabelas_faltando and not sequences_faltando:
            print("✅ TODAS AS TABELAS E SEQUENCES ESTÃO PRESENTES!")
            print()
            print("🎉 Banco de dados configurado corretamente!")
        else:
            print("❌ Banco de dados incompleto. Execute o script SQL de criação das tabelas.")
        
        print()
        
        # Fecha conexão
        cursor.close()
        connection.close()
        print("🔌 Conexão fechada.")
        
        return len(tabelas_faltando) == 0 and len(sequences_faltando) == 0
        
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"❌ ERRO DE BANCO DE DADOS:")
        print(f"   Código: {error.code}")
        print(f"   Mensagem: {error.message}")
        print()
        print("💡 Dicas:")
        print("   - Verifique se o DSN está correto (formato: host:porta/service_name)")
        print("   - Verifique se o usuário e senha estão corretos")
        print("   - Verifique se o banco de dados está acessível")
        return False
    
    except Exception as e:
        print(f"❌ ERRO INESPERADO: {e}")
        return False


if __name__ == "__main__":
    sucesso = testar_conexao()
    print()
    print("=" * 80)
    if sucesso:
        print("✅ TESTE CONCLUÍDO COM SUCESSO!")
    else:
        print("❌ TESTE FALHOU - Corrija os problemas acima")
    print("=" * 80)
