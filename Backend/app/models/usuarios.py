"""Model ORM — ESTOQUES_TI_USUARIOS"""
from datetime import datetime
from typing import Optional

from sqlalchemy import CHAR, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Usuario(Base):
    __tablename__ = "estoques_ti_usuarios"

    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    cargo: Mapped[Optional[str]] = mapped_column(String(100))
    ativo: Mapped[str] = mapped_column(CHAR(1), nullable=False, default="S", server_default="S")
    data_criacao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    criado_por: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("estoques_ti_usuarios.id_usuario")
    )
    data_alteracao: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    alterado_por: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("estoques_ti_usuarios.id_usuario")
    )

    def to_dict(self) -> dict:
        return {
            "id_usuario": self.id_usuario,
            "nome": self.nome,
            "email": self.email,
            "cargo": self.cargo,
            "ativo": self.ativo,
            "data_criacao": self.data_criacao,
            "criado_por": self.criado_por,
            "data_alteracao": self.data_alteracao,
            "alterado_por": self.alterado_por,
        }
