"""
Service para lógica de negócio relacionada a Ocorrências
"""
from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.ocorrencia_repo import OcorrenciaRepository
from app.schemas.ocorrencia import OcorrenciaCreate, OcorrenciaUpdate, OcorrenciaResponse, FecharOcorrenciaRequest, AlterarStatusRequest


class OcorrenciaService:
    """Service para gerenciar ocorrências"""
    
    @staticmethod
    def criar_ocorrencia(dados: OcorrenciaCreate, usuario_id: Optional[int] = None) -> OcorrenciaResponse:
        """Cria uma nova ocorrência"""
        # Cria ocorrência
        dados_dict = dados.model_dump()
        novo_id = OcorrenciaRepository.criar(dados_dict, usuario_id)
        
        # Busca e retorna ocorrência criada
        ocorrencia = OcorrenciaRepository.buscar_por_id(novo_id)
        if not ocorrencia:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar ocorrência"
            )
        
        return OcorrenciaResponse(**ocorrencia)
    
    @staticmethod
    def buscar_ocorrencia(ocorrencia_id: int) -> OcorrenciaResponse:
        """Busca ocorrência por ID"""
        ocorrencia = OcorrenciaRepository.buscar_por_id(ocorrencia_id)
        if not ocorrencia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ocorrência não encontrada"
            )
        return OcorrenciaResponse(**ocorrencia)
    
    @staticmethod
    def listar_ocorrencias(status: Optional[str] = None, tipo: Optional[str] = None) -> List[OcorrenciaResponse]:
        """Lista todas as ocorrências, opcionalmente filtradas por status e/ou tipo"""
        ocorrencias = OcorrenciaRepository.listar_todos(status, tipo)
        return [OcorrenciaResponse(**o) for o in ocorrencias]
    
    @staticmethod
    def atualizar_ocorrencia(ocorrencia_id: int, dados: OcorrenciaUpdate, alterado_por: Optional[int] = None) -> OcorrenciaResponse:
        """Atualiza uma ocorrência"""
        # Verifica se ocorrência existe
        ocorrencia = OcorrenciaRepository.buscar_por_id(ocorrencia_id)
        if not ocorrencia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ocorrência não encontrada"
            )
        
        # Atualiza ocorrência
        dados_dict = dados.model_dump(exclude_unset=True)
        if not dados_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nenhum dado para atualizar"
            )
        
        sucesso = OcorrenciaRepository.atualizar(ocorrencia_id, dados_dict, alterado_por)
        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao atualizar ocorrência"
            )
        
        # Busca e retorna ocorrência atualizada
        ocorrencia_atualizada = OcorrenciaRepository.buscar_por_id(ocorrencia_id)
        return OcorrenciaResponse(**ocorrencia_atualizada)
    
    @staticmethod
    def fechar_ocorrencia(ocorrencia_id: int, dados: FecharOcorrenciaRequest, alterado_por: Optional[int] = None) -> OcorrenciaResponse:
        """Fecha uma ocorrência"""
        # Verifica se ocorrência existe
        ocorrencia = OcorrenciaRepository.buscar_por_id(ocorrencia_id)
        if not ocorrencia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ocorrência não encontrada"
            )
        
        # Verifica se ocorrência já está fechada
        if ocorrencia['status'] == 'FECHADO':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ocorrência já está fechada"
            )
        
        # Fecha ocorrência
        sucesso = OcorrenciaRepository.fechar(ocorrencia_id, dados.resolucao, alterado_por)
        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao fechar ocorrência"
            )
        
        # Busca e retorna ocorrência fechada
        ocorrencia_fechada = OcorrenciaRepository.buscar_por_id(ocorrencia_id)
        return OcorrenciaResponse(**ocorrencia_fechada)
    
    @staticmethod
    def deletar_ocorrencia(ocorrencia_id: int) -> dict:
        """Deleta uma ocorrência"""
        # Verifica se ocorrência existe
        ocorrencia = OcorrenciaRepository.buscar_por_id(ocorrencia_id)
        if not ocorrencia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ocorrência não encontrada"
            )
        
        # Deleta ocorrência
        sucesso = OcorrenciaRepository.deletar(ocorrencia_id)
        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao deletar ocorrência"
            )
        
        return {"mensagem": "Ocorrência deletada com sucesso"}
