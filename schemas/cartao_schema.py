from pydantic import BaseModel
from typing import Optional


class CartaoBase(BaseModel):
    descricao: str
    final_cartao: str
    bandeira: str
    tipo: str
    ativo: bool = True


class CartaoCreate(CartaoBase):
    pass


class CartaoUpdate(BaseModel):
    descricao: Optional[str] = None
    final_cartao: Optional[str] = None
    bandeira: Optional[str] = None
    tipo: Optional[str] = None
    ativo: Optional[bool] = None


class CartaoResponse(CartaoBase):
    id: int

    class Config:
        from_attributes = True