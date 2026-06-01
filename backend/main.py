import requests
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date

from database import engine, Base, SessionLocal
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NBP Currency API")

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
    nbp_url = "http://api.nbp.pl/api/exchangerates/tables/A?format=json"
    response = requests.get(nbp_url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Błąd podczas pobierania danych z NBP")
    
    data = response.json()[0]
    rates = data.get("rates", [])
    date_str = data.get("effectiveDate")
    
    record_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    added_count = 0
    for rate in rates:
        exists = db.query(models.CurrencyRate).filter(
            models.CurrencyRate.currency_code == rate["code"],
            models.CurrencyRate.date == record_date
        ).first()
        
        if not exists:
            new_rate = models.CurrencyRate(
                currency_code=rate["code"],
                currency_name=rate["currency"],
                date=record_date,
                average_rate=rate["mid"]
            )
            db.add(new_rate)
            added_count += 1
            
    db.commit()
    
    return {"status": "success", "added": added_count, "date": date_str}

@app.get("/currencies")
def get_all_currencies(db: Session = Depends(get_db)):
    rates = db.query(models.CurrencyRate).all()
    return rates

@app.get("/currencies/{query_date}")
def get_currencies_by_date(query_date: date, db: Session = Depends(get_db)):
    rates = db.query(models.CurrencyRate).filter(models.CurrencyRate.date == query_date).all()
    return rates