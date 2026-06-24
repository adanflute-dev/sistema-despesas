from models.despesa_rateio import DespesaRateio


class RateioRepository:

    def __init__(self, db):
        self.db = db

    def listar_por_despesa(self, despesa_id: int):
        """
        Retorna todos os rateios de uma despesa específica
        """
        return (
            self.db.query(DespesaRateio)
            .filter(DespesaRateio.despesa_id == despesa_id)
            .all()
        )

    def buscar_por_id(self, id: int):
        """
        Busca um rateio específico pelo ID
        """
        return (
            self.db.query(DespesaRateio)
            .filter(DespesaRateio.id == id)
            .first()
        )

    def criar(self, despesa_id: int, funcionario_id: int, valor: float):
        """
        Cria um novo rateio
        """

        rateio = DespesaRateio(
            despesa_id=despesa_id,
            funcionario_id=funcionario_id,
            valor=valor
        )

        self.db.add(rateio)
        self.db.commit()
        self.db.refresh(rateio)

        return rateio

    def criar_multiplos(self, despesa_id: int, lista_rateio: list):
        """
        Cria vários rateios de uma vez (batch insert lógico)
        """

        rateios = []

        for r in lista_rateio:
            obj = DespesaRateio(
                despesa_id=despesa_id,
                funcionario_id=r.funcionario_id,
                valor=r.valor
            )
            self.db.add(obj)
            rateios.append(obj)

        self.db.commit()

        # refresh opcional (caso precise IDs)
        for r in rateios:
            self.db.refresh(r)

        return rateios

    def deletar_por_despesa(self, despesa_id: int):
        """
        Remove todos os rateios de uma despesa (útil em update)
        """

        self.db.query(DespesaRateio).filter(
            DespesaRateio.despesa_id == despesa_id
        ).delete()

        self.db.commit()

        return True

    def deletar_por_id(self, id: int):
        """
        Remove um rateio específico
        """

        rateio = self.buscar_por_id(id)

        if not rateio:
            return False

        self.db.delete(rateio)
        self.db.commit()

        return True