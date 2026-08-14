"""
Service para lógica de negócio relacionada a Ocorrências
"""
from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.ocorrencia_repo import OcorrenciaRepository
from app.schemas.ocorrencia import (
    OcorrenciaCreate,
    OcorrenciaUpdate,
    OcorrenciaResponse,
    FecharOcorrenciaRequest,
    AlterarStatusRequest,
    StatusOcorrenciaEnum,
)


def _to_response(ocorrencia: dict) -> OcorrenciaResponse:
    """Remove campos auxiliares (ex.: solicitante_nome) antes do schema."""
    data = {k: v for k, v in ocorrencia.items() if k != "solicitante_nome"}
    return OcorrenciaResponse(**data)


class OcorrenciaService:
    """Service para gerenciar ocorrências"""

    @staticmethod
    def criar_ocorrencia(
        dados: OcorrenciaCreate, usuario_id: Optional[int] = None
    ) -> OcorrenciaResponse:
        """Cria uma nova ocorrência"""
        dados_dict = dados.model_dump()
        # Enum → valor string para o Oracle
        if hasattr(dados_dict.get("severidade"), "value"):
            dados_dict["severidade"] = dados_dict["severidade"].value

        novo_id = OcorrenciaRepository.criar(dados_dict, usuario_id)
        ocorrencia = OcorrenciaRepository.buscar_por_id(novo_id)
        if not ocorrencia:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar ocorrência",
            )
        return _to_response(ocorrencia)

    @staticmethod
    def buscar_ocorrencia(ocorrencia_id: int) -> OcorrenciaResponse:
        """Busca ocorrência por ID"""
        ocorrencia = OcorrenciaRepository.buscar_por_id(ocorrencia_id)
        if not ocorrencia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ocorrência não encontrada",
            )
        return _to_response(ocorrencia)

    @staticmethod
    def listar_ocorrencias(
        status_filtro: Optional[str] = None, tipo: Optional[str] = None
    ) -> List[OcorrenciaResponse]:
        """Lista todas as ocorrências, opcionalmente filtradas por status e/ou tipo"""
        ocorrencias = OcorrenciaRepository.listar_todos(status_filtro, tipo)
        return [_to_response(o) for o in ocorrencias]

    @staticmethod
    def listar_ocorrencias_abertas() -> List[OcorrenciaResponse]:
        """Lista ocorrências abertas (ABERTA / EM_ANDAMENTO)."""
        ocorrencias = OcorrenciaRepository.listar_abertas()
        return [_to_response(o) for o in ocorrencias]

    @staticmethod
    def alterar_status(
        ocorrencia_id: int,
        dados: AlterarStatusRequest,
        alterado_por: Optional[int] = None,
    ) -> OcorrenciaResponse:
        """Altera apenas o status de uma ocorrência."""
        ocorrencia = OcorrenciaRepository.buscar_por_id(ocorrencia_id)
        if not ocorrencia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ocorrência não encontrada",
            )

        novo_status = (
            dados.status.value
            if isinstance(dados.status, StatusOcorrenciaEnum)
            else str(dados.status)
        )

        if ocorrencia["status"] == novo_status:
            return _to_response(ocorrencia)

        sucesso = OcorrenciaRepository.alterar_status(
            ocorrencia_id, novo_status, alterado_por
        )
        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao alterar status da ocorrência",
            )

        # Observações opcionais: anexa à descrição via fechar parcial / update
        if dados.observacoes:
            desc_atual = ocorrencia.get("descricao") or ""
            nota = f"[Status → {novo_status}] {dados.observacoes}"
            nova_desc = f"{desc_atual}\n{nota}".strip() if desc_atual else nota
            OcorrenciaRepository.atualizar(
                ocorrencia_id, {"descricao": nova_desc}, alterado_por
            )

        atualizada = OcorrenciaRepository.buscar_por_id(ocorrencia_id)
        return _to_response(atualizada)

    @staticmethod
    def atualizar_ocorrencia(
        ocorrencia_id: int,
        dados: OcorrenciaUpdate,
        alterado_por: Optional[int] = None,
    ) -> OcorrenciaResponse:
        """Atualiza uma ocorrência"""
        ocorrencia = OcorrenciaRepository.buscar_por_id(ocorrencia_id)
        if not ocorrencia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ocorrência não encontrada",
            )

        dados_dict = dados.model_dump(exclude_unset=True)
        if not dados_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nenhum dado para atualizar",
            )

        for chave in ("severidade", "status"):
            if chave in dados_dict and hasattr(dados_dict[chave], "value"):
                dados_dict[chave] = dados_dict[chave].value

        sucesso = OcorrenciaRepository.atualizar(ocorrencia_id, dados_dict, alterado_por)
        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao atualizar ocorrência",
            )

        return _to_response(OcorrenciaRepository.buscar_por_id(ocorrencia_id))

    @staticmethod
    def fechar_ocorrencia(
        ocorrencia_id: int,
        dados: FecharOcorrenciaRequest,
        alterado_por: Optional[int] = None,
    ) -> OcorrenciaResponse:
        """Fecha uma ocorrência"""
        ocorrencia = OcorrenciaRepository.buscar_por_id(ocorrencia_id)
        if not ocorrencia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ocorrência não encontrada",
            )

        if ocorrencia["status"] == StatusOcorrenciaEnum.FECHADA.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ocorrência já está fechada",
            )

        sucesso = OcorrenciaRepository.fechar(
            ocorrencia_id, dados.observacoes, alterado_por
        )
        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao fechar ocorrência",
            )

        return _to_response(OcorrenciaRepository.buscar_por_id(ocorrencia_id))

    @staticmethod
    def deletar_ocorrencia(ocorrencia_id: int) -> dict:
        """Deleta uma ocorrência"""
        ocorrencia = OcorrenciaRepository.buscar_por_id(ocorrencia_id)
        if not ocorrencia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ocorrência não encontrada",
            )

        sucesso = OcorrenciaRepository.deletar(ocorrencia_id)
        if not sucesso:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao deletar ocorrência",
            )

        return {"mensagem": "Ocorrência deletada com sucesso"}
