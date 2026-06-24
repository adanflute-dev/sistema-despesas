from pydantic import BaseModel
from typing import Optional


class FuncionarioBase(BaseModel):
    nome: str
    cpf: str
    cargo: str
    telefone: str
    ativo: bool = True


class FuncionarioCreate(FuncionarioBase):
    pass


class FuncionarioUpdate(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    cargo: Optional[str] = None
    telefone: Optional[str] = None
    ativo: Optional[bool] = None


class FuncionarioResponse(FuncionarioBase):
    id: int

    class Config:
        from_attributes = True