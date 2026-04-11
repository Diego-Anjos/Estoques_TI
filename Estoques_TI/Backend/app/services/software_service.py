"""
Service para lógica de negócio relacionada a Software/Licenças
"""
from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.software_repo import SoftwareRepository
from app.schemas.software import (
    SoftwareCreate, 
    SoftwareUpdate, 
    SoftwareResponse,
    SoftwareAtribuicaoCreate
)


class SoftwareService:
    """Service para gerenciar software/licenças"""
    
    @staticmethod
    def criar_software(dados: SoftwareCreate, usuario_id: Optional[int] = None) -> SoftwareResponse:
        """Cria um novo software"""
        # Valida que licenças em uso não excede total
        if dados.licencas_em_uso > dados.total_licencas:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Licenças em uso não pode exceder total de licenças"
            )
        
        # Cria software
        dados_dict = dados.model_dump()
        novo_id = SoftwareRepository.criar(dados_dict, usuario_id)
        
        # Busca e retorna software criado
        software = SoftwareRepository.buscar_por_id(novo_id)
        if not software:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar software"
            )
        
        return SoftwareResponse(**software)
    
    @staticmethod
    def buscar_software(software_id: int) -> SoftwareResponse:
        """Busca software por ID"""
        software = SoftwareRepository.buscar_por_id(software_id)
        if not software:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Software não encontrado"
            )
        return SoftwareResponse(**software)
    
    @staticmethod
    def listar_softwares() -> List[SoftwareResponse]:
        """Lista todos os softwares"""
        softwares = SoftwareRepository.listar_todos()
        return [SoftwareResponse(**s) for s in softwares]
    
    @staticmethod
    def atualizar_software(software_id: int, dados: SoftwareUpdate, alterado_por: Optional[int] = None) -> SoftwareResponse:
        """Atualiza um software"""
        # Verifica se software existe
        software = SoftwareRepository.buscar_por_id(software_id)
        if not software:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Software não encontrado"
            )
        
        # Valida que licenças em uso não excede total
        total_licencas = dados.total_licencas if dados.total_licencas is not None else software['total_licencas']
        licencas_em_uso = dados.licencas_em_uso if dados.licencas_em_uso is not None else software['licencas_em_uso']
        
        if licencas_em_uso > total_licencas:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Licenças em uso não pode exceder total de licenças"
            )
        
        # Atualiza software
        dados_dict = dados.model_dump(exclude_unset=True)
        if not dados_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nenhum dado para atualizar"
            )
        
        sucesso = SoftwareRepository.atualizar(software_id, dados_dict, alterado_por)
        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao atualizar software"
            )
        
        # Busca e retorna software atualizado
        software_atualizado = SoftwareRepository.buscar_por_id(software_id)
        return SoftwareResponse(**software_atualizado)
    
    
    @staticmethod
    def deletar_software(software_id: int) -> dict:
        """Deleta um software"""
        # Verifica se software existe
        software = SoftwareRepository.buscar_por_id(software_id)
        if not software:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Software não encontrado"
            )
        
        # Deleta software
        sucesso = SoftwareRepository.deletar(software_id)
        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao deletar software"
            )
        
        return {"mensagem": "Software deletado com sucesso"}
