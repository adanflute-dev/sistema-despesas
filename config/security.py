from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from passlib.context import CryptContext

# =========================
# CONFIGURAÇÕES JWT
# =========================

SECRET_KEY = "SUA_CHAVE_SUPER_SECRETA_AQUI"  # ideal: vir do .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 horas

# =========================
# HASH DE SENHA (BCRYPT)
# =========================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# =========================
# SENHAS
# =========================

def gerar_hash(senha: str) -> str:
    """
    Gera hash seguro da senha
    """
    return pwd_context.hash(senha)


def verificar_senha(senha: str, hash_senha: str) -> bool:
    """
    Verifica senha informada com hash salvo
    """
    return pwd_context.verify(senha, hash_senha)


# =========================
# JWT
# =========================

def criar_token(dados: dict, expires_delta: timedelta | None = None) -> str:
    """
    Cria token JWT com expiração
    """

    to_encode = dados.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def decodificar_token(token: str) -> dict:
    """
    Decodifica token JWT e valida assinatura
    """

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload

    except JWTError:
        return None