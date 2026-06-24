from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean

from config.database import Base

class Usuario(Base):

    __tablename__ = "usuarios"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(
        String(255)
    )

    email = Column(
        String(255),
        unique=True
    )

    senha = Column(
        String(255)
    )

    admin = Column(
        Boolean,
        default=False
    )

    ativo = Column(
        Boolean,
        default=True
    )