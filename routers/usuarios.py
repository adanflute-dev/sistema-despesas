from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from config.security import gerar_hash

from models.usuario import Usuario

from schemas.usuario_schema import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse
)

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


@router.get("/", response_model=list[UsuarioResponse])
def listar(db: Session = Depends(get_db)):
    return db.query(Usuario).all()


@router.get("/{id}", response_model=UsuarioResponse)
def buscar(id: int, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.id == id).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return usuario


@router.post("/", response_model=UsuarioResponse)
def criar(dados: UsuarioCreate, db: Session = Depends(get_db)):

    # hash da senha
    senha_hash = gerar_hash(dados.senha)

    novo = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha=senha_hash,
        admin=dados.admin,
        ativo=dados.ativo
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo


@router.put("/{id}", response_model=UsuarioResponse)
def atualizar(id: int, dados: UsuarioUpdate, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.id == id).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    update_data = dados.model_dump(exclude_unset=True)

    # se vier senha, faz hash
    if "senha" in update_data:
        update_data["senha"] = gerar_hash(update_data["senha"])

    for campo, valor in update_data.items():
        setattr(usuario, campo, valor)

    db.commit()
    db.refresh(usuario)

    return usuario


@router.delete("/{id}")
def excluir(id: int, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.id == id).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    db.delete(usuario)
    db.commit()

    return {"mensagem": "Usuário excluído com sucesso"}