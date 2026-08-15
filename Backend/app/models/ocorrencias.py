"""Model ORM — ESTOQUES_TI_OCORRENCIAS"""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Ocorrencia(Base):
    __tablename__ = "estoques_ti_ocorrencias"

    id_ocorrencia: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    descricao: Mapped[Optional[str]] = mapped_column(String(2000))
    severidade: Mapped[str] = mapped_column(
        String(20), nullable=False, default="MEDIA", server_default="MEDIA"
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="ABERTA", server_default="ABERTA"
    )
    id_usuario_abriu: Mapped[int] = mapped_column(
        Integer, ForeignKey("estoques_ti_usuarios.id_usuario"), nullable=False
    )
    id_usuario_solicitante: Mapped[int] = mapped_column(
        Integer, ForeignKey("estoques_ti_usuarios.id_usuario"), nullable=False
    )
    id_usuario_relacionado: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("estoques_ti_usuarios.id_usuario")
    )
    id_patrimonio_relacionado: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("estoques_ti_patrimonios.id_patrimonio")
    )
    data_abertura: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    data_fechamento: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    data_alteracao: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    alterado_por: Mapped[Optional[int]] = mapped_column(Integer)

    def to_dict(self) -> dict:
        return {
            "id_ocorrencia": self.id_ocorrencia,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "severidade": self.severidade,
            "status": self.status,
            "id_usuario_abriu": self.id_usuario_abriu,
            "id_usuario_solicitante": self.id_usuario_solicitante,
            "id_usuario_relacionado": self.id_usuario_relacionado,
            "id_patrimonio_relacionado": self.id_patrimonio_relacionado,
            "data_abertura": self.data_abertura,
            "data_fechamento": self.data_fechamento,
            "data_alteracao": self.data_alteracao,
            "alterado_por": self.alterado_por,
        }
