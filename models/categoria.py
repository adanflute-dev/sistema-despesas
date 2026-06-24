from sqlalchemy import Column, Integer, String, Boolean
from config.database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(
        String(255),
        nullable=False
    )

    descricao = Column(
        String(500),
        nullable=True
    )

    tipo = Column(
        String(100),  # ex: DESPESA, RECEITA, COMBUSTIVEL, MANUTENCAO
        nullable=False
    )

    ativo = Column(
        Boolean,
        default=True
    )