from pydantic import BaseModel
from typing import Optional


class FrotaBase(BaseModel):
    placa: str
    descricao: str
    marca: str
    modelo: str
    ativo: bool = True


class FrotaCreate(FrotaBase):
    pass


class FrotaUpdate(BaseModel):
    placa: Optional[str] = None
    descricao: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    ativo: Optional[bool] = None


class FrotaResponse(FrotaBase):
    id: int

    class Config:
        from_attributes = True