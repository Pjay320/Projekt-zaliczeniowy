from sqlalchemy import Column, Integer, String, Date, Float
from database import Base

class CurrencyRate(Base):
    __tablename__ = "currency_rates"

    id = Column(Integer, primary_key=True, index=True)
    currency_code = Column(String, index=True)  
    currency_name = Column(String)              
    date = Column(Date, index=True)             
    average_rate = Column(Float)               