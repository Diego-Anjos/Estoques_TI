"""Model ORM — ESTOQUES_TI_TIPOS_ITEM"""
from datetime import datetime
from typing import Optional

from sqlalchemy import CHAR, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class TipoItem(Base):
    __tablename__ = "estoques_ti_tipos_item"

    id_tipo_item: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    categoria: Mapped[Optional[str]] = mapped_column(String(80))
    descricao: Mapped[Optional[str]] = mapped_column(String(400))
    status: Mapped[Optional[str]] = mapped_column(String(20), default="Ativo", server_default="Ativo")
    serializado: Mapped[str] = mapped_column(CHAR(1), nullable=False, default="N", server_default="N")
    unidade: Mapped[str] = mapped_column(String(30), nullable=False, default="UN", server_default="UN")
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
            "id_tipo_item": self.id_tipo_item,
            "codigo": self.codigo,
            "nome": self.nome,
            "categoria": self.categoria,
            "descricao": self.descricao,
            "status": self.status,
            "serializado": self.serializado,
            "unidade": self.unidade,
            "data_criacao": self.data_criacao,
            "criado_por": self.criado_por,
            "data_alteracao": self.data_alteracao,
            "alterado_por": self.alterado_por,
        }
