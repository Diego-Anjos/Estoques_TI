"""
Service para lógica de negócio relacionada a Estoque
"""
from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.estoque_repo import EstoqueRepository
from app.repositories.item_repo import ItemRepository


class EstoqueService:
    """Service para gerenciar estoque"""
    
    @staticmethod
    def criar_estoque(item_id: int, quantidade: int = 0, quantidade_minima: int = 0, 
                     localizacao: Optional[str] = None, usuario_id: Optional[int] = None) -> dict:
        """Cria um novo registro de estoque"""
        # Verifica se item existe
        item = ItemRepository.buscar_por_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item não encontrado"
            )
        
        # Verifica se item é do tipo ESTOQUE
        if item['tipo'] != 'ESTOQUE':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item não é do tipo ESTOQUE"
            )
        
        # Verifica se já existe estoque para este item
        estoque_existente = EstoqueRepository.buscar_por_item(item_id)
        if estoque_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe registro de estoque para este item"
            )
        
        # Cria estoque
        dados = {
            'item_id': item_id,
            'quantidade': quantidade,
            'quantidade_minima': quantidade_minima,
            'localizacao': localizacao
        }
        novo_id = EstoqueRepository.criar(dados, usuario_id)
        
        # Busca e retorna estoque criado
        estoque = EstoqueRepository.buscar_por_id(novo_id)
        if not estoque:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar estoque"
            )
        
        return estoque
    
    @staticmethod
    def buscar_estoque(estoque_id: int) -> dict:
        """Busca estoque por ID"""
        estoque = EstoqueRepository.buscar_por_id(estoque_id)
        if not estoque:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estoque não encontrado"
            )
        return estoque
    
    @staticmethod
    def listar_estoque() -> List[dict]:
        """Lista todo o estoque"""
        return EstoqueRepository.listar_todos()
    
    @staticmethod
    def deletar_estoque(estoque_id: int) -> dict:
        """Deleta um registro de estoque"""
        # Verifica se estoque existe
        estoque = EstoqueRepository.buscar_por_id(estoque_id)
        if not estoque:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estoque não encontrado"
            )
        
        # Deleta estoque
        sucesso = EstoqueRepository.deletar(estoque_id)
        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao deletar estoque"
            )
        
        return {"mensagem": "Estoque deletado com sucesso"}
