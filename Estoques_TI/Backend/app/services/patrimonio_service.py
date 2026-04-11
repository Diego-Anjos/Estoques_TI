"""
Service para lógica de negócio relacionada a Patrimônio
"""
from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.patrimonio_repo import PatrimonioRepository
from app.repositories.item_repo import ItemRepository
from app.schemas.patrimonio import PatrimonioCreate, PatrimonioUpdate, PatrimonioResponse


class PatrimonioService:
    """Service para gerenciar patrimônio"""
    
    @staticmethod
    def criar_patrimonio(dados: PatrimonioCreate, usuario_id: Optional[int] = None) -> PatrimonioResponse:
        """Cria um novo patrimônio"""
        # Verifica se item existe
        item = ItemRepository.buscar_por_id(dados.item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item não encontrado"
            )
        
        # Verifica se item é do tipo PATRIMONIO
        if item['tipo'] != 'PATRIMONIO':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item não é do tipo PATRIMONIO"
            )
        
        # Verifica se número de série já existe
        patrimonio_existente = PatrimonioRepository.buscar_por_numero_serie(dados.numero_serie)
        if patrimonio_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Número de série já cadastrado"
            )
        
        # Cria patrimônio
        dados_dict = dados.model_dump()
        novo_id = PatrimonioRepository.criar(dados_dict, usuario_id)
        
        # Busca e retorna patrimônio criado
        patrimonio = PatrimonioRepository.buscar_por_id(novo_id)
        if not patrimonio:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar patrimônio"
            )
        
        return PatrimonioResponse(**patrimonio)
    
    @staticmethod
    def buscar_patrimonio(patrimonio_id: int) -> PatrimonioResponse:
        """Busca patrimônio por ID"""
        patrimonio = PatrimonioRepository.buscar_por_id(patrimonio_id)
        if not patrimonio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patrimônio não encontrado"
            )
        return PatrimonioResponse(**patrimonio)
    
    @staticmethod
    def listar_patrimonios(status: Optional[str] = None) -> List[PatrimonioResponse]:
        """Lista todos os patrimônios, opcionalmente filtrados por status"""
        patrimonios = PatrimonioRepository.listar_todos(status)
        return [PatrimonioResponse(**p) for p in patrimonios]
    
    @staticmethod
    def atualizar_patrimonio(patrimonio_id: int, dados: PatrimonioUpdate, alterado_por: Optional[int] = None) -> PatrimonioResponse:
        """Atualiza um patrimônio"""
        # Verifica se patrimônio existe
        patrimonio = PatrimonioRepository.buscar_por_id(patrimonio_id)
        if not patrimonio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patrimônio não encontrado"
            )
        
        # Verifica se número de série já está em uso por outro patrimônio
        if dados.numero_serie:
            patrimonio_serie = PatrimonioRepository.buscar_por_numero_serie(dados.numero_serie)
            if patrimonio_serie and patrimonio_serie['id'] != patrimonio_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Número de série já cadastrado para outro patrimônio"
                )
        
        # Atualiza patrimônio
        dados_dict = dados.model_dump(exclude_unset=True)
        if not dados_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nenhum dado para atualizar"
            )
        
        sucesso = PatrimonioRepository.atualizar(patrimonio_id, dados_dict, alterado_por)
        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao atualizar patrimônio"
            )
        
        # Busca e retorna patrimônio atualizado
        patrimonio_atualizado = PatrimonioRepository.buscar_por_id(patrimonio_id)
        return PatrimonioResponse(**patrimonio_atualizado)
    
    @staticmethod
    def deletar_patrimonio(patrimonio_id: int) -> dict:
        """Deleta um patrimônio"""
        # Verifica se patrimônio existe
        patrimonio = PatrimonioRepository.buscar_por_id(patrimonio_id)
        if not patrimonio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patrimônio não encontrado"
            )
        
        # Deleta patrimônio
        sucesso = PatrimonioRepository.deletar(patrimonio_id)
        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao deletar patrimônio"
            )
        
        return {"mensagem": "Patrimônio deletado com sucesso"}
