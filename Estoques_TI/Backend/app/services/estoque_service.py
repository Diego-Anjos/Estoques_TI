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
    def entrada_estoque(item_id: int, quantidade: int, usuario_id: Optional[int] = None) -> dict:
        """Registra entrada de itens no estoque"""
        if quantidade <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantidade deve ser maior que zero"
            )
        
        # Verifica se estoque existe
        estoque = EstoqueRepository.buscar_por_item(item_id)
        if not estoque:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estoque não encontrado para este item"
            )
        
        # Registra entrada
        sucesso = EstoqueRepository.entrada(item_id, quantidade, usuario_id)
        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao registrar entrada"
            )
        
        # Busca e retorna estoque atualizado
        estoque_atualizado = EstoqueRepository.buscar_por_item(item_id)
        return {
            **estoque_atualizado,
            "mensagem": f"Entrada de {quantidade} unidades registrada com sucesso"
        }
    
    @staticmethod
    def saida_estoque(item_id: int, quantidade: int, usuario_id: Optional[int] = None) -> dict:
        """Registra saída de itens do estoque"""
        if quantidade <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantidade deve ser maior que zero"
            )
        
        # Verifica se estoque existe
        estoque = EstoqueRepository.buscar_por_item(item_id)
        if not estoque:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estoque não encontrado para este item"
            )
        
        # Verifica se há quantidade suficiente
        if estoque['quantidade'] < quantidade:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Quantidade insuficiente em estoque. Disponível: {estoque['quantidade']}"
            )
        
        # Registra saída
        sucesso = EstoqueRepository.saida(item_id, quantidade, usuario_id)
        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao registrar saída. Verifique se há quantidade suficiente."
            )
        
        # Busca e retorna estoque atualizado
        estoque_atualizado = EstoqueRepository.buscar_por_item(item_id)
        return {
            **estoque_atualizado,
            "mensagem": f"Saída de {quantidade} unidades registrada com sucesso"
        }
    
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
