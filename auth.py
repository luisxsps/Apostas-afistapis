from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, utils

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    if db.query(models.User).filter_by(username=username).first():
        raise HTTPException(400, "Usuário já existe")
    hashed = utils.hash_password(password)
    new_user = models.User(username=username, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    return {"msg": "Usuário criado"}

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(username=username).first()
    if not user or not utils.verify_password(password, user.hashed_password):
        raise HTTPException(401, "Credenciais inválidas")
    token = utils.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
