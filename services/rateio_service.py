from repositories.rateio_repository import RateioRepository


class RateioService:

    def __init__(self, db):
        self.db = db
        self.repo = RateioRepository(db)

    def criar_rateios(self, despesa_id: int, lista_rateio):

        """
        Cria múltiplos rateios para uma despesa
        """
        return self.repo.criar_multiplos(
            despesa_id,
            lista_rateio
        )

    def listar_por_despesa(self, despesa_id: int):

        """
        Lista todos os rateios de uma despesa
        """
        return self.repo.listar_por_despesa(despesa_id)

    def atualizar_rateio(self, despesa_id: int, novo_rateio):

        """
        Substitui todos os rateios de uma despesa
        (remove antigos e recria)
        """

        # remove antigos
        self.repo.deletar_por_despesa(despesa_id)

        # cria novos
        return self.repo.criar_multiplos(
            despesa_id,
            novo_rateio
        )

    def deletar_rateio(self, rateio_id: int):

        """
        Remove um rateio específico
        """
        return self.repo.deletar_por_id(rateio_id)

    def recalcular_rateio_proporcional(self, despesa_id: int, valores):

        """
        (Opcional avançado)
        Recalcula rateio proporcionalmente
        baseado em pesos enviados
        """

        total_peso = sum(v.peso for v in valores)

        self.repo.deletar_por_despesa(despesa_id)

        rateios = []

        for v in valores:

            valor_calculado = (v.peso / total_peso) * v.valor_total

            rateios.append(
                self.repo.criar(
                    despesa_id=despesa_id,
                    funcionario_id=v.funcionario_id,
                    valor=valor_calculado
                )
            )

        return rateios