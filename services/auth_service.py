from config.security import verificar_senha, criar_token
from models.usuario import Usuario


class AuthService:

    def __init__(self, db):
        self.db = db

    def autenticar(self, email: str, senha: str):

        # busca usuário por email
        usuario = (
            self.db.query(Usuario)
            .filter(Usuario.email == email)
            .first()
        )

        # usuário não encontrado
        if not usuario:
            return None

        # valida senha
        if not verificar_senha(senha, usuario.senha):
            return None

        # gera token JWT
        token = criar_token({
            "sub": usuario.email,
            "id": usuario.id,
            "admin": usuario.admin
        })

        # retorno padronizado
        return {
            "access_token": token,
            "token_type": "bearer",
            "usuario": {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
                "admin": usuario.admin,
                "ativo": usuario.ativo
            }
        }