from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean

from config.database import Base

class Cartao(Base):

    __tablename__ = "cartoes"

    id = Column(
        Integer,
        primary_key=True
    )

    descricao = Column(
        String(255)
    )

    final_cartao = Column(
        String(10)
    )

    bandeira = Column(
        String(50)
    )

    tipo = Column(
        String(30)
    )

    ativo = Column(
        Boolean,
        default=True
    )