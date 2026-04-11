"""
Script para corrigir todos os repositories de uma vez
Atualiza os nomes das tabelas para corresponder ao schema Oracle
"""

import os
import re

# Mapeamento de arquivos e suas respectivas tabelas Oracle
REPOSITORY_TABLE_MAP = {
    'tipo_item_repo.py': 'ESTOQUES_TI_TIPOS_ITEM',
    'item_repo.py': 'ESTOQUES_TI_ITENS',
    'estoque_repo.py': 'ESTOQUES_TI_ESTOQUE_SALDO',
    'patrimonio_repo.py': 'ESTOQUES_TI_PATRIMONIOS',
    'software_repo.py': 'ESTOQUES_TI_SOFTWARES',
    'ocorrencia_repo.py': 'ESTOQUES_TI_OCORRENCIAS'
}

# Mapeamento de nomes de tabelas antigas para novas
TABLE_REPLACEMENTS = {
    'USUARIOS': 'ESTOQUES_TI_USUARIOS',
    'LOCAIS': 'ESTOQUES_TI_LOCAIS',
    'TIPOS_ITEM': 'ESTOQUES_TI_TIPOS_ITEM',
    'ITENS': 'ESTOQUES_TI_ITENS',
    'ESTOQUE': 'ESTOQUES_TI_ESTOQUE_SALDO',
    'ESTOQUE_SALDO': 'ESTOQUES_TI_ESTOQUE_SALDO',
    'MOVIMENTACOES': 'ESTOQUES_TI_MOVIMENTACOES',
    'PATRIMONIO': 'ESTOQUES_TI_PATRIMONIOS',
    'PATRIMONIO_ATRIBUTOS': 'ESTOQUES_TI_PATRIMONIO_ATR',
    'SOFTWARE': 'ESTOQUES_TI_SOFTWARES',
    'SOFTWARE_LICENCAS': 'ESTOQUES_TI_SOFTWARE_LICENCAS',
    'SOFTWARE_ATRIBUICOES': 'ESTOQUES_TI_ATRIBUICOES',
    'ATRIBUICOES': 'ESTOQUES_TI_ATRIBUICOES',
    'OCORRENCIAS': 'ESTOQUES_TI_OCORRENCIAS'
}


def fix_repository_file(filepath: str, table_name: str):
    """Corrige um arquivo de repository"""
    print(f"\n📝 Processando: {os.path.basename(filepath)}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Adiciona constante TABLE_NAME se não existir
    if 'TABLE_NAME = ' not in content:
        # Encontra a posição após os imports
        import_end = content.find('\n\nclass ')
        if import_end != -1:
            before = content[:import_end]
            after = content[import_end:]
            content = f"{before}\n\n# Nome da tabela no banco Oracle\nTABLE_NAME = \"{table_name}\"\n{after}"
            print(f"   ✅ Adicionada constante TABLE_NAME = \"{table_name}\"")
    
    # Substitui referências diretas às tabelas por {TABLE_NAME}
    for old_table, new_table in TABLE_REPLACEMENTS.items():
        # Padrões para encontrar referências às tabelas
        patterns = [
            (f'FROM {old_table}\\b', f'FROM {{TABLE_NAME}}'),
            (f'INTO {old_table}\\b', f'INTO {{TABLE_NAME}}'),
            (f'UPDATE {old_table}\\b', f'UPDATE {{TABLE_NAME}}'),
            (f'DELETE FROM {old_table}\\b', f'DELETE FROM {{TABLE_NAME}}'),
            (f'INSERT INTO {old_table}\\b', f'INSERT INTO {{TABLE_NAME}}'),
            (f'JOIN {old_table}\\b', f'JOIN {{TABLE_NAME}}'),
        ]
        
        for pattern, replacement in patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                print(f"   ✅ Substituído: {pattern} → {replacement}")
    
    # Converte strings SQL sem f-string para f-strings quando necessário
    # Procura por sql = """ ou sql = ''' que contenham {TABLE_NAME}
    def add_f_to_sql(match):
        indent = match.group(1)
        quote = match.group(2)
        sql_content = match.group(3)
        
        if '{TABLE_NAME}' in sql_content:
            return f'{indent}sql = f{quote}{sql_content}{quote}'
        return match.group(0)
    
    content = re.sub(
        r'(\s+)sql = ("""|\'\'\'|"|\')(.*?)\2',
        add_f_to_sql,
        content,
        flags=re.DOTALL
    )
    
    # Salva o arquivo se houve mudanças
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   💾 Arquivo atualizado!")
        return True
    else:
        print(f"   ℹ️  Nenhuma mudança necessária")
        return False


def main():
    """Função principal"""
    print("=" * 80)
    print("🔧 CORREÇÃO AUTOMÁTICA DE REPOSITORIES")
    print("=" * 80)
    
    repo_dir = os.path.join(os.path.dirname(__file__), 'app', 'repositories')
    
    if not os.path.exists(repo_dir):
        print(f"❌ Diretório não encontrado: {repo_dir}")
        return
    
    print(f"\n📂 Diretório: {repo_dir}")
    
    files_updated = 0
    files_processed = 0
    
    # Processa cada arquivo
    for filename, table_name in REPOSITORY_TABLE_MAP.items():
        filepath = os.path.join(repo_dir, filename)
        
        if os.path.exists(filepath):
            files_processed += 1
            if fix_repository_file(filepath, table_name):
                files_updated += 1
        else:
            print(f"\n⚠️  Arquivo não encontrado: {filename}")
    
    # Resumo
    print("\n" + "=" * 80)
    print("📊 RESUMO")
    print("=" * 80)
    print(f"   Arquivos processados: {files_processed}")
    print(f"   Arquivos atualizados: {files_updated}")
    print()
    
    if files_updated > 0:
        print("✅ Correções aplicadas com sucesso!")
    else:
        print("ℹ️  Nenhuma correção necessária")
    
    print("\n💡 Próximos passos:")
    print("   1. Execute: python test_connection.py")
    print("   2. Configure o arquivo .env com suas credenciais Oracle")
    print("   3. Teste a API: python -m app.main")


if __name__ == "__main__":
    main()
