from models.despesa import Despesa
from models.despesa_rateio import DespesaRateio


class DespesaRepository:

    def __init__(self, db):
        self.db = db

    def listar(self):
        return self.db.query(Despesa).all()

    def buscar_por_id(self, id: int):
        return self.db.query(Despesa).filter(Despesa.id == id).first()

    def criar(self, dados):

        despesa = Despesa(
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

        self.db.add(despesa)
        self.db.commit()
        self.db.refresh(despesa)

        # rateio
        for r in dados.rateio:
            self.db.add(
                DespesaRateio(
                    despesa_id=despesa.id,
                    funcionario_id=r.funcionario_id,
                    valor=r.valor
                )
            )

        self.db.commit()

        return despesa

    def deletar(self, despesa):
        self.db.delete(despesa)
        self.db.commit()