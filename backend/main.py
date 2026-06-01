import requests
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import engine, Base, SessionLocal
import models

# Tworzy tabele w bazie przy starcie
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NBP Currency API")

# Funkcja pomocnicza: otwiera sesję bazy danych na czas trwania zapytania
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Backend API dziala! Tabela utworzona."}

@app.post("/currencies/fetch")
def fetch_currencies(db: Session = Depends(get_db)):
    # 1. Pobranie danych z API NBP (Tabela A - średnie kursy walut obcych)
    nbp_url = "http://api.nbp.pl/api/exchangerates/tables/A?format=json"
    response = requests.get(nbp_url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Błąd podczas pobierania danych z NBP")
    
    data = response.json()[0]
    rates = data.get("rates", [])
    date_str = data.get("effectiveDate")
    
    # Zamiana daty z tekstu na obiekt daty w Pythonie
    record_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    # 2. Zapis do bazy danych
    added_count = 0
    for rate in rates:
        # Sprawdzamy, czy ten kurs dla tej daty już istnieje
        exists = db.query(models.CurrencyRate).filter(
            models.CurrencyRate.currency_code == rate["code"],
            models.CurrencyRate.date == record_date
        ).first()
        
        # Jeśli nie istnieje, dodajemy nowy wiersz do bazy
        if not exists:
            new_rate = models.CurrencyRate(
                currency_code=rate["code"],
                currency_name=rate["currency"],
                date=record_date,
                average_rate=rate["mid"]
            )
            db.add(new_rate)
            added_count += 1
            
    db.commit() # Zatwierdzenie zmian w bazie
    
    return {"status": "success", "added": added_count, "date": date_str}