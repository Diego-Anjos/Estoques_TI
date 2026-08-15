"""Model ORM — ESTOQUES_TI_ESTOQUE_SALDO"""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class EstoqueSaldo(Base):
    __tablename__ = "estoques_ti_estoque_saldo"

    id_item: Mapped[int] = mapped_column(
        Integer, ForeignKey("estoques_ti_itens.id_item"), primary_key=True
    )
    id_local: Mapped[int] = mapped_column(
        Integer, ForeignKey("estoques_ti_locais.id_local"), primary_key=True
    )
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    data_alteracao: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    alterado_por: Mapped[Optional[int]] = mapped_column(Integer)

    def to_dict(self) -> dict:
        return {
            "id_item": self.id_item,
            "id_local": self.id_local,
            "quantidade": self.quantidade,
            "data_alteracao": self.data_alteracao,
            "alterado_por": self.alterado_por,
        }
