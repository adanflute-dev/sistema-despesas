from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from config.database import get_db

from models.despesa import Despesa
from models.funcionario import Funcionario
from models.frota import Frota

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def resumo(db: Session = Depends(get_db)):

    total_despesas = db.query(
        func.sum(Despesa.valor_total)
    ).scalar()

    total_registros = db.query(
        func.count(Despesa.id)
    ).scalar()

    por_status = db.query(
        Despesa.status,
        func.count(Despesa.id)
    ).group_by(Despesa.status).all()

    por_funcionario = db.query(
        Funcionario.nome,
        func.sum(Despesa.valor_total)
    ).join(Despesa, Despesa.funcionario_id == Funcionario.id)\
     .group_by(Funcionario.nome).all()

    por_frota = db.query(
        Frota.placa,
        func.sum(Despesa.valor_total)
    ).join(Despesa, Despesa.frota_id == Frota.id)\
     .group_by(Frota.placa).all()

    return {
        "total_despesas": total_despesas or 0,
        "total_registros": total_registros or 0,
        "por_status": por_status,
        "por_funcionario": por_funcionario,
        "por_frota": por_frota
    }