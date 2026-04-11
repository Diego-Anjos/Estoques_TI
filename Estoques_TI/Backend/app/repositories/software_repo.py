"""
Repository para operações de banco de dados relacionadas a Software/Licenças
"""
from typing import List, Optional, Dict, Any
from app.core.database import get_cursor


# Nome da tabela no banco Oracle
TABLE_NAME = "ESTOQUES_TI_SOFTWARES"


class SoftwareRepository:
    """Repository para gerenciar software/licenças no banco de dados"""
    
    @staticmethod
    def criar(dados: Dict[str, Any], usuario_id: Optional[int] = None) -> int:
        """Cria um novo software"""
        sql = f"""
            INSERT INTO {TABLE_NAME} (NOME, FABRICANTE, VERSAO, TIPO_LICENCA, TOTAL_LICENCAS,
                                 LICENCAS_EM_USO, DATA_AQUISICAO, DATA_EXPIRACAO, 
                                 CHAVE_LICENCA, OBSERVACOES, CRIADO_POR)
            VALUES (:nome, :fabricante, :versao, :tipo_licenca, :total_licencas,
                    :licencas_em_uso, :data_aquisicao, :data_expiracao,
                    :chave_licenca, :observacoes, :criado_por)
            RETURNING ID INTO :id
        """
        
        with get_cursor() as cursor:
            id_var = cursor.var(int)
            cursor.execute(sql, {
                'nome': dados['nome'],
                'fabricante': dados.get('fabricante'),
                'versao': dados.get('versao'),
                'tipo_licenca': dados['tipo_licenca'],
                'total_licencas': dados['total_licencas'],
                'licencas_em_uso': dados.get('licencas_em_uso', 0),
                'data_aquisicao': dados.get('data_aquisicao'),
                'data_expiracao': dados.get('data_expiracao'),
                'chave_licenca': dados.get('chave_licenca'),
                'observacoes': dados.get('observacoes'),
                'criado_por': usuario_id,
                'id': id_var
            })
            return id_var.getvalue()[0]
    
    @staticmethod
    def buscar_por_id(software_id: int) -> Optional[Dict[str, Any]]:
        """Busca software por ID"""
        sql = f"""
            SELECT ID, NOME, FABRICANTE, VERSAO, TIPO_LICENCA, TOTAL_LICENCAS,
                   LICENCAS_EM_USO, DATA_AQUISICAO, DATA_EXPIRACAO, CHAVE_LICENCA,
                   OBSERVACOES, CRIADO_EM, CRIADO_POR, ALTERADO_EM, ALTERADO_POR
            FROM {TABLE_NAME}
            WHERE ID = :id
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql, {'id': software_id})
            row = cursor.fetchone()
            
            if row:
                return {
                    'id': row[0],
                    'nome': row[1],
                    'fabricante': row[2],
                    'versao': row[3],
                    'tipo_licenca': row[4],
                    'total_licencas': row[5],
                    'licencas_em_uso': row[6],
                    'licencas_disponiveis': row[5] - row[6],
                    'data_aquisicao': row[7],
                    'data_expiracao': row[8],
                    'chave_licenca': row[9],
                    'observacoes': row[10],
                    'criado_em': row[11],
                    'criado_por': row[12],
                    'alterado_em': row[13],
                    'alterado_por': row[14]
                }
            return None
    
    @staticmethod
    def listar_todos() -> List[Dict[str, Any]]:
        """Lista todos os softwares"""
        sql = f"""
            SELECT ID, NOME, FABRICANTE, VERSAO, TIPO_LICENCA, TOTAL_LICENCAS,
                   LICENCAS_EM_USO, DATA_AQUISICAO, DATA_EXPIRACAO, CHAVE_LICENCA,
                   OBSERVACOES, CRIADO_EM, CRIADO_POR, ALTERADO_EM, ALTERADO_POR
            FROM {TABLE_NAME}
            ORDER BY NOME
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            return [
                {
                    'id': row[0],
                    'nome': row[1],
                    'fabricante': row[2],
                    'versao': row[3],
                    'tipo_licenca': row[4],
                    'total_licencas': row[5],
                    'licencas_em_uso': row[6],
                    'licencas_disponiveis': row[5] - row[6],
                    'data_aquisicao': row[7],
                    'data_expiracao': row[8],
                    'chave_licenca': row[9],
                    'observacoes': row[10],
                    'criado_em': row[11],
                    'criado_por': row[12],
                    'alterado_em': row[13],
                    'alterado_por': row[14]
                }
                for row in rows
            ]
    
    @staticmethod
    def atualizar(software_id: int, dados: Dict[str, Any], alterado_por: Optional[int] = None) -> bool:
        """Atualiza um software"""
        campos = []
        params = {'id': software_id, 'alterado_por': alterado_por}
        
        if 'nome' in dados:
            campos.append("NOME = :nome")
            params['nome'] = dados['nome']
        
        if 'fabricante' in dados:
            campos.append("FABRICANTE = :fabricante")
            params['fabricante'] = dados['fabricante']
        
        if 'versao' in dados:
            campos.append("VERSAO = :versao")
            params['versao'] = dados['versao']
        
        if 'tipo_licenca' in dados:
            campos.append("TIPO_LICENCA = :tipo_licenca")
            params['tipo_licenca'] = dados['tipo_licenca']
        
        if 'total_licencas' in dados:
            campos.append("TOTAL_LICENCAS = :total_licencas")
            params['total_licencas'] = dados['total_licencas']
        
        if 'licencas_em_uso' in dados:
            campos.append("LICENCAS_EM_USO = :licencas_em_uso")
            params['licencas_em_uso'] = dados['licencas_em_uso']
        
        if 'data_aquisicao' in dados:
            campos.append("DATA_AQUISICAO = :data_aquisicao")
            params['data_aquisicao'] = dados['data_aquisicao']
        
        if 'data_expiracao' in dados:
            campos.append("DATA_EXPIRACAO = :data_expiracao")
            params['data_expiracao'] = dados['data_expiracao']
        
        if 'chave_licenca' in dados:
            campos.append("CHAVE_LICENCA = :chave_licenca")
            params['chave_licenca'] = dados['chave_licenca']
        
        if 'observacoes' in dados:
            campos.append("OBSERVACOES = :observacoes")
            params['observacoes'] = dados['observacoes']
        
        if not campos:
            return False
        
        campos.append("ALTERADO_EM = CURRENT_TIMESTAMP")
        campos.append("ALTERADO_POR = :alterado_por")
        
        sql = f"UPDATE {TABLE_NAME} SET {', '.join(campos)} WHERE ID = :id"
        
        with get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.rowcount > 0
    
    @staticmethod
    def alocar_licenca(software_id: int, quantidade: int, alterado_por: Optional[int] = None) -> bool:
        """Aloca licenças (aumenta licencas_em_uso)"""
        sql = f"""
            UPDATE {TABLE_NAME} 
            SET LICENCAS_EM_USO = LICENCAS_EM_USO + :quantidade,
                ALTERADO_EM = CURRENT_TIMESTAMP,
                ALTERADO_POR = :alterado_por
            WHERE ID = :id
            AND (LICENCAS_EM_USO + :quantidade) <= TOTAL_LICENCAS
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql, {
                'id': software_id,
                'quantidade': quantidade,
                'alterado_por': alterado_por
            })
            return cursor.rowcount > 0
    
    @staticmethod
    def liberar_licenca(software_id: int, quantidade: int, alterado_por: Optional[int] = None) -> bool:
        """Libera licenças (diminui licencas_em_uso)"""
        sql = f"""
            UPDATE {TABLE_NAME} 
            SET LICENCAS_EM_USO = LICENCAS_EM_USO - :quantidade,
                ALTERADO_EM = CURRENT_TIMESTAMP,
                ALTERADO_POR = :alterado_por
            WHERE ID = :id
            AND LICENCAS_EM_USO >= :quantidade
        """
        
        with get_cursor() as cursor:
            cursor.execute(sql, {
                'id': software_id,
                'quantidade': quantidade,
                'alterado_por': alterado_por
            })
            return cursor.rowcount > 0
    
    @staticmethod
    def deletar(software_id: int) -> bool:
        """Deleta um software"""
        sql = f"DELETE FROM {TABLE_NAME} WHERE ID = :id"
        
        with get_cursor() as cursor:
            cursor.execute(sql, {'id': software_id})
            return cursor.rowcount > 0
