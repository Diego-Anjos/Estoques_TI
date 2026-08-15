"""Model ORM — ESTOQUES_TI_LOCAIS"""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Local(Base):
    __tablename__ = "estoques_ti_locais"

    id_local: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    setor: Mapped[Optional[str]] = mapped_column(String(80))
    descricao: Mapped[Optional[str]] = mapped_column(String(300))
    status: Mapped[Optional[str]] = mapped_column(String(20), default="Ativo", server_default="Ativo")
    data_criacao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    criado_por: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("estoques_ti_usuarios.id_usuario")
    )
    data_alteracao: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    alterado_por: Mapped[Optional[int]] = mapped_column(Integer)

    def to_dict(self) -> dict:
        return {
            "id_local": self.id_local,
            "nome": self.nome,
            "setor": self.setor,
            "descricao": self.descricao,
            "status": self.status,
            "data_criacao": self.data_criacao,
            "criado_por": self.criado_por,
            "data_alteracao": self.data_alteracao,
            "alterado_por": self.alterado_por,
        }
