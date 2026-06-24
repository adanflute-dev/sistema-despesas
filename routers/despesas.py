from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db

from models.despesa import Despesa
from models.despesa_rateio import DespesaRateio

from schemas.despesa_schema import (
    DespesaCreate,
    DespesaUpdate,
    DespesaResponse,
    DespesaDetalhadaResponse
)

router = APIRouter(
    prefix="/despesas",
    tags=["Despesas"]
)


@router.get("/", response_model=list[DespesaResponse])
def listar(db: Session = Depends(get_db)):
    return db.query(Despesa).all()


@router.get("/{id}", response_model=DespesaDetalhadaResponse)
def buscar(id: int, db: Session = Depends(get_db)):

    despesa = db.query(Despesa).filter(Despesa.id == id).first()

    if not despesa:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")

    rateio = db.query(DespesaRateio).filter(
        DespesaRateio.despesa_id == id
    ).all()

    resultado = DespesaDetalhadaResponse(
        **despesa.__dict__,
        rateio=rateio
    )

    return resultado


@router.post("/", response_model=DespesaResponse)
def criar(dados: DespesaCreate, db: Session = Depends(get_db)):

    nova = Despesa(
        funcionario_id=dados.funcionario_id,
        frota_id=dados.frota_id,
        cartao_id=dados.cartao_id,
        categoria=dados.categoria,
        fornecedor=dados.fornecedor,
        forma_pagamento=dados.forma_pagamento,
        descricao=dados.descricao,
        valor_total=dados.valor_total,
        data_despesa=dados.data_despesa
    )

    db.add(nova)
    db.commit()
    db.refresh(nova)

    # rateio
    for r in dados.rateio:
        db.add(
            DespesaRateio(
                despesa_id=nova.id,
                funcionario_id=r.funcionario_id,
                valor=r.valor
            )
        )

    db.commit()

    return nova


@router.put("/{id}", response_model=DespesaResponse)
def atualizar(id: int, dados: DespesaUpdate, db: Session = Depends(get_db)):

    despesa = db.query(Despesa).filter(Despesa.id == id).first()

    if not despesa:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")

    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(despesa, campo, valor)

    db.commit()
    db.refresh(despesa)

    return despesa


@router.delete("/{id}")
def excluir(id: int, db: Session = Depends(get_db)):

    despesa = db.query(Despesa).filter(Despesa.id == id).first()

    if not despesa:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")

    db.delete(despesa)
    db.commit()

    return {"mensagem": "Despesa excluída com sucesso"}