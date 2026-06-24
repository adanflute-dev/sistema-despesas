from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from datetime import datetime

from config.database import Base

class Despesa(Base):

    __tablename__ = "despesas"

    id = Column(
        Integer,
        primary_key=True
    )

    funcionario_id = Column(
        Integer,
        ForeignKey("funcionarios.id")
    )

    frota_id = Column(
        Integer,
        ForeignKey("frotas.id")
    )

    cartao_id = Column(
        Integer,
        ForeignKey("cartoes.id"),
        nullable=True
    )

    categoria = Column(
        String(100)
    )

    fornecedor = Column(
        String(255)
    )

    forma_pagamento = Column(
        String(50)
    )

    descricao = Column(
        String(500)
    )

    valor_total = Column(
        Float
    )

    data_despesa = Column(
        Date
    )

    status = Column(
        String(30),
        default="PENDENTE"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )