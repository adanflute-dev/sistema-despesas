from models.despesa import Despesa
from repositories.rateio_repository import RateioRepository


class DespesaService:

    def __init__(self, db):
        self.db = db
        self.rateio_repo = RateioRepository(db)

    def criar_despesa(self, dados):

        # =========================
        # CRIA DESPESA PRINCIPAL
        # =========================
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

        # =========================
        # CRIA RATEIO AUTOMATICAMENTE
        # =========================
        if hasattr(dados, "rateio") and dados.rateio:

            self.rateio_repo.criar_multiplos(
                despesa.id,
                dados.rateio
            )

        return despesa

    def atualizar_despesa(self, despesa, dados):

        # =========================
        # ATUALIZA CAMPOS DINÂMICOS
        # =========================
        update_data = dados.model_dump(exclude_unset=True)

        for campo, valor in update_data.items():
            setattr(despesa, campo, valor)

        self.db.commit()
        self.db.refresh(despesa)

        return despesa

    def deletar_despesa(self, despesa):

        # =========================
        # REMOVE RATEIOS PRIMEIRO
        # =========================
        self.rateio_repo.deletar_por_despesa(despesa.id)

        # =========================
        # REMOVE DESPESA
        # =========================
        self.db.delete(despesa)
        self.db.commit()

        return True

    def obter_despesa_com_rateio(self, despesa_id: int):

        despesa = (
            self.db.query(Despesa)
            .filter(Despesa.id == despesa_id)
            .first()
        )

        if not despesa:
            return None

        rateio = self.rateio_repo.listar_por_despesa(despesa_id)

        return {
            "id": despesa.id,
            "funcionario_id": despesa.funcionario_id,
            "frota_id": despesa.frota_id,
            "cartao_id": despesa.cartao_id,
            "categoria": despesa.categoria,
            "fornecedor": despesa.fornecedor,
            "forma_pagamento": despesa.forma_pagamento,
            "descricao": despesa.descricao,
            "valor_total": despesa.valor_total,
            "data_despesa": despesa.data_despesa,
            "status": despesa.status,
            "rateio": [
                {
                    "id": r.id,
                    "funcionario_id": r.funcionario_id,
                    "valor": r.valor
                }
                for r in rateio
            ]
        }