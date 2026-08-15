"""Model ORM — ESTOQUES_TI_SOFTWARES"""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Software(Base):
    __tablename__ = "estoques_ti_softwares"

    id_software: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    fabricante: Mapped[Optional[str]] = mapped_column(String(120))
    descricao: Mapped[Optional[str]] = mapped_column(String(300))
    data_criacao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    criado_por: Mapped[Optional[int]] = mapped_column(Integer)
    data_alteracao: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    alterado_por: Mapped[Optional[int]] = mapped_column(Integer)

    def to_dict(self) -> dict:
        return {
            "id_software": self.id_software,
            "nome": self.nome,
            "fabricante": self.fabricante,
            "descricao": self.descricao,
            "data_criacao": self.data_criacao,
            "criado_por": self.criado_por,
            "data_alteracao": self.data_alteracao,
            "alterado_por": self.alterado_por,
        }
