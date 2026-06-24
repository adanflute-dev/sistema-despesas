from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from config.database import Base

class Comprovante(Base):

    __tablename__ = "comprovantes"

    id = Column(
        Integer,
        primary_key=True
    )

    despesa_id = Column(
        Integer,
        ForeignKey("despesas.id")
    )

    arquivo = Column(
        String(500)
    )