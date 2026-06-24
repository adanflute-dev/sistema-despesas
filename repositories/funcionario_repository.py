from models.funcionario import Funcionario


class FuncionarioRepository:

    def __init__(self, db):
        self.db = db

    def listar(self):
        return self.db.query(Funcionario).all()

    def buscar_por_id(self, id: int):
        return self.db.query(Funcionario).filter(Funcionario.id == id).first()

    def criar(self, dados):

        obj = Funcionario(**dados.model_dump())

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