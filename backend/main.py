import requests
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import engine, Base, SessionLocal
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NBP Currency API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/currencies/fetch/range")
def fetch_currencies_range(start_date: str, end_date: str, db: Session = Depends(get_db)):
    nbp_url = f"http://api.nbp.pl/api/exchangerates/tables/A/{start_date}/{end_date}/?format=json"
    response = requests.get(nbp_url, timeout=10)
    
    if response.status_code != 200:
        return {"status": "error", "message": "Brak danych dla tego zakresu"}
    
    data_list = response.json()
    new_rates = []
    
    for table in data_list:
        rates = table.get("rates", [])
        record_date = table.get("effectiveDate")
        
        for rate in rates:
            exists = db.query(models.CurrencyRate).filter_by(currency_code=rate["code"], date=record_date).first()
            if not exists:
                new_rates.append(models.CurrencyRate(
                    currency_code=rate["code"],
                    currency_name=rate["currency"],
                    date=record_date,
                    average_rate=rate["mid"]
                ))
    
    if new_rates:
        db.bulk_save_objects(new_rates)
        db.commit()
        return {"status": "success", "added": len(new_rates)}
    else:
        return {"status": "no_new_data", "added": 0}

@app.get("/currencies/stats")
def get_stats(start_date: str, end_date: str, db: Session = Depends(get_db)):
    try:
        if not start_date or not end_date:
            raise HTTPException(status_code=400, detail="Musisz podać zakres dat")
            
        stats = db.query(
            models.CurrencyRate.currency_code,
            models.CurrencyRate.currency_name,
            func.avg(models.CurrencyRate.average_rate).label("avg_rate")
        ).filter(
            models.CurrencyRate.date.between(start_date, end_date)
        ).group_by(models.CurrencyRate.currency_code, models.CurrencyRate.currency_name).all()
        
        return [{"code": r[0], "name": r[1], "avg": round(float(r[2]), 4)} for r in stats]
    except Exception as e:
        print(f"Błąd bazy danych: {e}") 
        raise HTTPException(status_code=400, detail="Błędny zakres dat lub brak danych")


@app.get("/currencies")
def get_all_currencies(start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    query = db.query(models.CurrencyRate)
    
    if start_date and end_date:
        query = query.filter(models.CurrencyRate.date.between(start_date, end_date))
        
    return query.order_by(models.CurrencyRate.date.desc()).all()