from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from config.database import get_db

from models.funcionario import Funcionario

from schemas.funcionario_schema import (
    FuncionarioCreate,
    FuncionarioUpdate,
    FuncionarioResponse
)

router = APIRouter(
    prefix="/funcionarios",
    tags=["Funcionários"]
)

@router.get(
    "/",
    response_model=list[FuncionarioResponse]
)
def listar(
    db: Session = Depends(get_db)
):
    return db.query(
        Funcionario
    ).all()


@router.get(
    "/{id}",
    response_model=FuncionarioResponse
)
def buscar(
    id: int,
    db: Session = Depends(get_db)
):
    funcionario = db.query(
        Funcionario
    ).filter(
        Funcionario.id == id
    ).first()

    if not funcionario:
        raise HTTPException(
            status_code=404,
            detail="Funcionário não encontrado"
        )

    return funcionario


@router.post(
    "/",
    response_model=FuncionarioResponse
)
def criar(
    dados: FuncionarioCreate,
    db: Session = Depends(get_db)
):
    novo = Funcionario(
        **dados.model_dump()
    )

    db.add(novo)

    db.commit()

    db.refresh(novo)

    return novo


@router.put(
    "/{id}",
    response_model=FuncionarioResponse
)
def atualizar(
    id: int,
    dados: FuncionarioUpdate,
    db: Session = Depends(get_db)
):
    funcionario = db.query(
        Funcionario
    ).filter(
        Funcionario.id == id
    ).first()

    if not funcionario:
        raise HTTPException(
            status_code=404,
            detail="Funcionário não encontrado"
        )

    update_data = dados.model_dump(
        exclude_unset=True
    )

    for campo, valor in update_data.items():
        setattr(
            funcionario,
            campo,
            valor
        )

    db.commit()

    db.refresh(funcionario)

    return funcionario


@router.delete("/{id}")
def excluir(
    id: int,
    db: Session = Depends(get_db)
):
    funcionario = db.query(
        Funcionario
    ).filter(
        Funcionario.id == id
    ).first()

    if not funcionario:
        raise HTTPException(
            status_code=404,
            detail="Funcionário não encontrado"
        )

    db.delete(funcionario)

    db.commit()

    return {
        "mensagem": "Excluído com sucesso"
    }