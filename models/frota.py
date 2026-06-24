from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean

from config.database import Base

class Frota(Base):

    __tablename__ = "frotas"

    id = Column(
        Integer,
        primary_key=True
    )

    placa = Column(
        String(20)
    )

    descricao = Column(
        String(255)
    )

    marca = Column(
        String(100)
    )

    modelo = Column(
        String(100)
    )

    ativo = Column(
        Boolean,
        default=True
    )