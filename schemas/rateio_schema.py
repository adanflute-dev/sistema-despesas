from pydantic import BaseModel


class RateioCreate(BaseModel):
    funcionario_id: int
    valor: float


class RateioResponse(RateioCreate):
    id: int
    despesa_id: int

    class Config:
        from_attributes = True