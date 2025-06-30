from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth, pagamento

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(pagamento.router)

@app.get("/")
def root():
    return {"msg": "API de apostas está online!"}
