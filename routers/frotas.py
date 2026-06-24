from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from config.database import get_db

from models.frota import Frota

from schemas.frota_schema import (
    FrotaCreate,
    FrotaUpdate,
    FrotaResponse
)

router = APIRouter(
    prefix="/frotas",
    tags=["Frotas"]
)

@router.get(
    "/",
    response_model=list[FrotaResponse]
)
def listar(
    db: Session = Depends(get_db)
):
    return db.query(
        Frota
    ).all()


@router.post(
    "/",
    response_model=FrotaResponse
)
def criar(
    dados: FrotaCreate,
    db: Session = Depends(get_db)
):
    nova = Frota(
        **dados.model_dump()
    )

    db.add(nova)

    db.commit()

    db.refresh(nova)

    return nova


@router.put(
    "/{id}",
    response_model=FrotaResponse
)
def atualizar(
    id: int,
    dados: FrotaUpdate,
    db: Session = Depends(get_db)
):
    frota = db.query(
        Frota
    ).filter(
        Frota.id == id
    ).first()

    if not frota:
        raise HTTPException(
            status_code=404,
            detail="Frota não encontrada"
        )

    update_data = dados.model_dump(
        exclude_unset=True
    )

    for campo, valor in update_data.items():
        setattr(
            frota,
            campo,
            valor
        )

    db.commit()

    db.refresh(frota)

    return frota


@router.delete("/{id}")
def excluir(
    id: int,
    db: Session = Depends(get_db)
):
    frota = db.query(
        Frota
    ).filter(
        Frota.id == id
    ).first()

    if not frota:
        raise HTTPException(
            status_code=404,
            detail="Frota não encontrada"
        )

    db.delete(frota)

    db.commit()

    return {
        "mensagem": "Excluída com sucesso"
    }