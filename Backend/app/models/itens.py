"""Model ORM — ESTOQUES_TI_ITENS"""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Item(Base):
    __tablename__ = "estoques_ti_itens"

    id_item: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_tipo_item: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("estoques_ti_tipos_item.id_tipo_item")
    )
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    tipo: Mapped[Optional[str]] = mapped_column(String(120))
    marca: Mapped[Optional[str]] = mapped_column(String(120))
    modelo: Mapped[Optional[str]] = mapped_column(String(120))
    descricao: Mapped[Optional[str]] = mapped_column(String(400))
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    unidade: Mapped[str] = mapped_column(String(30), nullable=False, default="UN", server_default="UN")
    id_local: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("estoques_ti_locais.id_local")
    )
    status: Mapped[Optional[str]] = mapped_column(String(20), default="Ativo", server_default="Ativo")
    estoque_minimo: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
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
            "id_item": self.id_item,
            "nome": self.nome,
            "tipo": self.tipo,
            "descricao": self.descricao,
            "quantidade": self.quantidade,
            "unidade": self.unidade,
            "id_local": self.id_local,
            "status": self.status,
            "id_tipo_item": self.id_tipo_item,
            "marca": self.marca,
            "modelo": self.modelo,
            "estoque_minimo": self.estoque_minimo,
            "data_criacao": self.data_criacao,
            "criado_por": self.criado_por,
            "data_alteracao": self.data_alteracao,
            "alterado_por": self.alterado_por,
            "nome_local": getattr(self, "nome_local", None),
        }
