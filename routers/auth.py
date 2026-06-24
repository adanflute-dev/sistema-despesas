from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from config.database import get_db

from models.usuario import Usuario

from schemas.usuario_schema import (
    LoginSchema,
    TokenResponse
)

from config.security import (
    verificar_senha,
    criar_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    dados: LoginSchema,
    db: Session = Depends(get_db)
):

    usuario = db.query(
        Usuario
    ).filter(
        Usuario.email == dados.email
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado"
        )

    if not verificar_senha(
        dados.senha,
        usuario.senha
    ):
        raise HTTPException(
            status_code=401,
            detail="Senha inválida"
        )

    token = criar_token(
        {
            "sub": usuario.email,
            "id": usuario.id,
            "admin": usuario.admin
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }