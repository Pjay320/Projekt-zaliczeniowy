from fastapi import FastAPI
from database import engine, Base
import models

# To polecenie tworzy tabele w bazie danych (jeśli jeszcze nie istnieją)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NBP Currency API")

@app.get("/")
def read_root():
    return {"message": "Backend API dziala! Tabela utworzona."}