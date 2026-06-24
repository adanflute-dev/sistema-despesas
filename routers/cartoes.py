from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from config.database import get_db

from models.cartao import Cartao

from schemas.cartao_schema import (
    CartaoCreate,
    CartaoUpdate,
    CartaoResponse
)

router = APIRouter(
    prefix="/cartoes",
    tags=["Cartões"]
)

@router.get(
    "/",
    response_model=list[CartaoResponse]
)
def listar(
    db: Session = Depends(get_db)
):
    return db.query(
        Cartao
    ).all()


@router.post(
    "/",
    response_model=CartaoResponse
)
def criar(
    dados: CartaoCreate,
    db: Session = Depends(get_db)
):
    novo = Cartao(
        **dados.model_dump()
    )

    db.add(novo)

    db.commit()

    db.refresh(novo)

    return novo


@router.put(
    "/{id}",
    response_model=CartaoResponse
)
def atualizar(
    id: int,
    dados: CartaoUpdate,
    db: Session = Depends(get_db)
):
    cartao = db.query(
        Cartao
    ).filter(
        Cartao.id == id
    ).first()

    if not cartao:
        raise HTTPException(
            status_code=404,
            detail="Cartão não encontrado"
        )

    update_data = dados.model_dump(
        exclude_unset=True
    )

    for campo, valor in update_data.items():
        setattr(
            cartao,
            campo,
            valor
        )

    db.commit()

    db.refresh(cartao)

    return cartao


@router.delete("/{id}")
def excluir(
    id: int,
    db: Session = Depends(get_db)
):
    cartao = db.query(
        Cartao
    ).filter(
        Cartao.id == id
    ).first()

    if not cartao:
        raise HTTPException(
            status_code=404,
            detail="Cartão não encontrado"
        )

    db.delete(cartao)

    db.commit()

    return {
        "mensagem": "Excluído com sucesso"
    }