"""Model ORM — ESTOQUES_TI_CONFIGURACOES"""
from sqlalchemy import CHAR, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ConfiguracaoSistema(Base):
    __tablename__ = "estoques_ti_configuracoes"

    id_config: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome_empresa: Mapped[str] = mapped_column(
        String(150), nullable=False, default="Controle de Estoque",
        server_default="Controle de Estoque",
    )
    modo_escuro: Mapped[str] = mapped_column(CHAR(1), nullable=False, default="N", server_default="N")
    alerta_estoque_minimo: Mapped[int] = mapped_column(
        Integer, nullable=False, default=5, server_default="5"
    )

    def to_dict(self) -> dict:
        return {
            "id_config": self.id_config,
            "nome_empresa": self.nome_empresa,
            "modo_escuro": self.modo_escuro == "S",
            "alerta_estoque_minimo": self.alerta_estoque_minimo,
        }
