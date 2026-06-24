from pydantic import BaseModel
from typing import Optional
from typing import List
from datetime import date

from schemas.rateio_schema import RateioCreate


class DespesaBase(BaseModel):

    funcionario_id: int

    frota_id: int

    categoria: str

    fornecedor: str

    forma_pagamento: str

    descricao: str

    valor_total: float

    data_despesa: date

    cartao_id: Optional[int] = None


class DespesaCreate(DespesaBase):

    rateio: List[RateioCreate] = []


class DespesaUpdate(BaseModel):

    funcionario_id: Optional[int] = None

    frota_id: Optional[int] = None

    categoria: Optional[str] = None

    fornecedor: Optional[str] = None

    forma_pagamento: Optional[str] = None

    descricao: Optional[str] = None

    valor_total: Optional[float] = None

    data_despesa: Optional[date] = None

    cartao_id: Optional[int] = None

    status: Optional[str] = None


class DespesaResponse(BaseModel):

    id: int

    funcionario_id: int

    frota_id: int

    cartao_id: Optional[int]

    categoria: str

    fornecedor: str

    forma_pagamento: str

    descricao: str

    valor_total: float

    data_despesa: date

    status: str

    class Config:
        from_attributes = True


class DespesaDetalhadaResponse(BaseModel):

    id: int

    funcionario_id: int

    frota_id: int

    cartao_id: Optional[int]

    categoria: str

    fornecedor: str

    forma_pagamento: str

    descricao: str

    valor_total: float

    data_despesa: date

    status: str

    rateio: List[RateioCreate] = []

    class Config:
        from_attributes = True