"""Model ORM — ESTOQUES_TI_MOVIMENTACOES"""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class EstoqueMovimentacao(Base):
    __tablename__ = "estoques_ti_movimentacoes"

    id_movimentacao: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_item: Mapped[int] = mapped_column(
        Integer, ForeignKey("estoques_ti_itens.id_item"), nullable=False
    )
    id_local_origem: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("estoques_ti_locais.id_local")
    )
    id_local_destino: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("estoques_ti_locais.id_local")
    )
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo_movimentacao: Mapped[str] = mapped_column(String(20), nullable=False)
    motivo: Mapped[Optional[str]] = mapped_column(String(300))
    setor_destino: Mapped[Optional[str]] = mapped_column(String(80))
    setor_origem: Mapped[Optional[str]] = mapped_column(String(80))
    documento_ref: Mapped[Optional[str]] = mapped_column(String(80))
    data_criacao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    criado_por: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("estoques_ti_usuarios.id_usuario")
    )

    def to_dict(self) -> dict:
        return {
            "id_movimentacao": self.id_movimentacao,
            "id_item": self.id_item,
            "id_local_origem": self.id_local_origem,
            "id_local_destino": self.id_local_destino,
            "quantidade": self.quantidade,
            "tipo_movimentacao": self.tipo_movimentacao,
            "observacao": self.motivo,
            "setor_destino": self.setor_destino,
            "setor_origem": self.setor_origem,
            "data_movimentacao": self.data_criacao,
            "usuario_id": self.criado_por,
            "nome_item": getattr(self, "nome_item", None),
            "quantidade_atual": getattr(self, "quantidade_atual", None),
        }
