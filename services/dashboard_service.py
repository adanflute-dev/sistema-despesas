from sqlalchemy import func

from models.despesa import Despesa
from models.funcionario import Funcionario
from models.frota import Frota


class DashboardService:

    def __init__(self, db):
        self.db = db

    def resumo(self):

        # =========================
        # TOTAL GERAL DE DESPESAS
        # =========================
        total_despesas = self.db.query(
            func.sum(Despesa.valor_total)
        ).scalar()

        # =========================
        # TOTAL DE REGISTROS
        # =========================
        total_registros = self.db.query(
            func.count(Despesa.id)
        ).scalar()

        # =========================
        # DESPESAS POR STATUS
        # =========================
        por_status = self.db.query(
            Despesa.status,
            func.count(Despesa.id)
        ).group_by(Despesa.status).all()

        # =========================
        # DESPESAS POR FUNCIONÁRIO
        # =========================
        por_funcionario = (
            self.db.query(
                Funcionario.nome,
                func.sum(Despesa.valor_total)
            )
            .join(Despesa, Despesa.funcionario_id == Funcionario.id)
            .group_by(Funcionario.nome)
            .all()
        )

        # =========================
        # DESPESAS POR FROTA
        # =========================
        por_frota = (
            self.db.query(
                Frota.placa,
                func.sum(Despesa.valor_total)
            )
            .join(Despesa, Despesa.frota_id == Frota.id)
            .group_by(Frota.placa)
            .all()
        )

        # =========================
        # RETORNO FINAL DO DASHBOARD
        # =========================
        return {
            "total_despesas": float(total_despesas or 0),
            "total_registros": total_registros or 0,
            "por_status": [
                {"status": s, "total": c}
                for s, c in por_status
            ],
            "por_funcionario": [
                {"funcionario": n, "total": float(t or 0)}
                for n, t in por_funcionario
            ],
            "por_frota": [
                {"frota": p, "total": float(t or 0)}
                for p, t in por_frota
            ]
        }