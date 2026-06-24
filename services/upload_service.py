import os
from datetime import datetime

from models.comprovante import Comprovante


class UploadService:

    UPLOAD_DIR = "uploads"

    def __init__(self, db):
        self.db = db

        # garante que a pasta existe
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)

    def salvar_comprovante(self, despesa_id: int, file):

        """
        Salva arquivo fisicamente e registra no banco
        """

        # =========================
        # GERA NOME ÚNICO DO ARQUIVO
        # =========================
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{file.filename}"

        file_path = os.path.join(self.UPLOAD_DIR, filename)

        # =========================
        # SALVA ARQUIVO NO DISCO
        # =========================
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        # =========================
        # SALVA NO BANCO
        # =========================
        comprovante = Comprovante(
            despesa_id=despesa_id,
            arquivo=file_path
        )

        self.db.add(comprovante)
        self.db.commit()
        self.db.refresh(comprovante)

        return {
            "id": comprovante.id,
            "despesa_id": despesa_id,
            "arquivo": file_path,
            "mensagem": "Upload realizado com sucesso"
        }

    def listar_comprovantes(self, despesa_id: int):

        """
        Lista comprovantes de uma despesa
        """

        return (
            self.db.query(Comprovante)
            .filter(Comprovante.despesa_id == despesa_id)
            .all()
        )

    def deletar_comprovante(self, comprovante):

        """
        Remove arquivo do disco e do banco
        """

        # remove arquivo físico
        if os.path.exists(comprovante.arquivo):
            os.remove(comprovante.arquivo)

        # remove do banco
        self.db.delete(comprovante)
        self.db.commit()

        return True