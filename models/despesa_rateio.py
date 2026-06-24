from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import ForeignKey

from config.database import Base

class DespesaRateio(Base):

    __tablename__ = "despesas_rateio"

    id = Column(
        Integer,
        primary_key=True
    )

    despesa_id = Column(
        Integer,
        ForeignKey("despesas.id")
    )

    funcionario_id = Column(
        Integer,
        ForeignKey("funcionarios.id")
    )

    valor = Column(
        Float
    )