from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean

from config.database import Base

class Funcionario(Base):

    __tablename__ = "funcionarios"

    id = Column(
        Integer,
        primary_key=True
    )

    nome = Column(
        String(255)
    )

    cpf = Column(
        String(20)
    )

    cargo = Column(
        String(100)
    )

    telefone = Column(
        String(50)
    )

    ativo = Column(
        Boolean,
        default=True
    )