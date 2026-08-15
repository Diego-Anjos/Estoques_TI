"""Model ORM — ESTOQUES_TI_PATRIMONIOS"""
from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Patrimonio(Base):
    __tablename__ = "estoques_ti_patrimonios"

    id_patrimonio: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_item: Mapped[int] = mapped_column(
        Integer, ForeignKey("estoques_ti_itens.id_item"), nullable=False
    )
    numero_serie: Mapped[Optional[str]] = mapped_column(String(120), unique=True)
    numero_patrimonio: Mapped[Optional[str]] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="EM_ESTOQUE", server_default="EM_ESTOQUE"
    )
    id_local: Mapped[int] = mapped_column(
        Integer, ForeignKey("estoques_ti_locais.id_local"), nullable=False
    )
    id_usuario_alocado: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("estoques_ti_usuarios.id_usuario")
    )
    data_compra: Mapped[Optional[date]] = mapped_column(Date)
    data_fim_garantia: Mapped[Optional[date]] = mapped_column(Date)
    observacoes: Mapped[Optional[str]] = mapped_column(String(400))
    data_criacao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    criado_por: Mapped[Optional[int]] = mapped_column(Integer)
    data_alteracao: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    alterado_por: Mapped[Optional[int]] = mapped_column(Integer)

    def to_dict(self) -> dict:
        return {
            "id_patrimonio": self.id_patrimonio,
            "id_item": self.id_item,
            "numero_serie": self.numero_serie,
            "numero_patrimonio": self.numero_patrimonio,
            "status": self.status,
            "id_local": self.id_local,
            "id_usuario_alocado": self.id_usuario_alocado,
            "data_compra": self.data_compra,
            "data_fim_garantia": self.data_fim_garantia,
            "observacoes": self.observacoes,
            "data_criacao": self.data_criacao,
            "criado_por": self.criado_por,
            "data_alteracao": self.data_alteracao,
            "alterado_por": self.alterado_por,
        }
