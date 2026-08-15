"""Model ORM — ESTOQUES_TI_PATRIMONIO_ATR"""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class PatrimonioAtributo(Base):
    __tablename__ = "estoques_ti_patrimonio_atr"

    id_patrimonio: Mapped[int] = mapped_column(
        Integer, ForeignKey("estoques_ti_patrimonios.id_patrimonio"), primary_key=True
    )
    nome_atributo: Mapped[str] = mapped_column(String(60), primary_key=True)
    valor_atributo: Mapped[str] = mapped_column(String(200), nullable=False)
    data_criacao: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    criado_por: Mapped[Optional[int]] = mapped_column(Integer)

    def to_dict(self) -> dict:
        return {
            "id_patrimonio": self.id_patrimonio,
            "nome_atributo": self.nome_atributo,
            "valor_atributo": self.valor_atributo,
            "data_criacao": self.data_criacao,
            "criado_por": self.criado_por,
        }
