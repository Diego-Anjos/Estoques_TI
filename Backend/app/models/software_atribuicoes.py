"""Model ORM — ESTOQUES_TI_ATRIBUICOES"""
from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class SoftwareAtribuicao(Base):
    __tablename__ = "estoques_ti_atribuicoes"

    id_atribuicao: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_pool: Mapped[int] = mapped_column(
        Integer, ForeignKey("estoques_ti_software_licencas.id_pool"), nullable=False
    )
    id_usuario: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("estoques_ti_usuarios.id_usuario")
    )
    id_patrimonio: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("estoques_ti_patrimonios.id_patrimonio")
    )
    data_atribuicao: Mapped[date] = mapped_column(Date, nullable=False)
    data_remocao: Mapped[Optional[date]] = mapped_column(Date)
    observacoes: Mapped[Optional[str]] = mapped_column(String(300))
    data_criacao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    criado_por: Mapped[int] = mapped_column(
        Integer, ForeignKey("estoques_ti_usuarios.id_usuario"), nullable=False
    )

    def to_dict(self) -> dict:
        return {
            "id_atribuicao": self.id_atribuicao,
            "id_pool": self.id_pool,
            "id_usuario": self.id_usuario,
            "id_patrimonio": self.id_patrimonio,
            "data_atribuicao": self.data_atribuicao,
            "data_remocao": self.data_remocao,
            "observacoes": self.observacoes,
            "data_criacao": self.data_criacao,
            "criado_por": self.criado_por,
        }
