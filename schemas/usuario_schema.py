from pydantic import BaseModel, EmailStr
from typing import Optional


class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    admin: bool = False
    ativo: bool = True


class UsuarioCreate(UsuarioBase):
    senha: str


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    admin: Optional[bool] = None
    ativo: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    email: EmailStr
    senha: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"