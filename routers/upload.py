import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from models.comprovante import Comprovante

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/comprovante/{despesa_id}")
def upload_comprovante(
    despesa_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not file:
        raise HTTPException(status_code=400, detail="Arquivo inválido")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    comprovante = Comprovante(
        despesa_id=despesa_id,
        arquivo=file_path
    )

    db.add(comprovante)
    db.commit()

    return {
        "mensagem": "Upload realizado com sucesso",
        "arquivo": file_path
    }