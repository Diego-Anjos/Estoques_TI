"""Base declarativa SQLAlchemy compartilhada pelos models."""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base para todos os models ORM."""
    pass
