from datetime import datetime
from datetime import timedelta

from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = "SUA_CHAVE"

ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def gerar_hash(
    senha: str
):

    return pwd_context.hash(senha)

def verificar_senha(
    senha,
    hash_senha
):

    return pwd_context.verify(
        senha,
        hash_senha
    )

def criar_token(
    dados: dict
):

    payload = dados.copy()

    expire = (
        datetime.utcnow()
        + timedelta(hours=8)
    )

    payload.update(
        {"exp": expire}
    )

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )