"""Model ORM — ESTOQUES_TI_SOFTWARE_LICENCAS"""
from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class SoftwareLicencaPool(Base):
    __tablename__ = "estoques_ti_software_licencas"

    id_pool: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_software: Mapped[int] = mapped_column(
        Integer, ForeignKey("estoques_ti_softwares.id_software"), nullable=False
    )
    total_licencas: Mapped[int] = mapped_column(Integer, nullable=False)
    contrato_ref: Mapped[Optional[str]] = mapped_column(String(100))
    data_expiracao: Mapped[Optional[date]] = mapped_column(Date)
    data_criacao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    criado_por: Mapped[Optional[int]] = mapped_column(Integer)
    data_alteracao: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    alterado_por: Mapped[Optional[int]] = mapped_column(Integer)

    def to_dict(self) -> dict:
        return {
            "id_pool": self.id_pool,
            "id_software": self.id_software,
            "total_licencas": self.total_licencas,
            "contrato_ref": self.contrato_ref,
            "data_expiracao": self.data_expiracao,
            "data_criacao": self.data_criacao,
            "criado_por": self.criado_por,
            "data_alteracao": self.data_alteracao,
            "alterado_por": self.alterado_por,
        }
