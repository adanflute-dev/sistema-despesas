from models.cartao import Cartao


class CartaoRepository:

    def __init__(self, db):
        self.db = db

    def listar(self):
        return self.db.query(Cartao).all()

    def buscar_por_id(self, id: int):
        return self.db.query(Cartao).filter(Cartao.id == id).first()

    def criar(self, dados):

        obj = Cartao(**dados.model_dump())

        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return obj

    def atualizar(self, obj, dados):

        for campo, valor in dados.model_dump(exclude_unset=True).items():
            setattr(obj, campo, valor)

        self.db.commit()
        self.db.refresh(obj)

        return obj

    def deletar(self, obj):
        self.db.delete(obj)
        self.db.commit()