from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import User

router = APIRouter(prefix="/pix")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/deposito")
def simular_pix(username: str, valor: float, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user:
        return {"erro": "Usuário não encontrado"}
    user.saldo += valor
    db.commit()
    return {"msg": f"R${valor:.2f} creditado via PIX simulado"}
