from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Adres URL do bazy: postgresql://użytkownik:hasło@nazwa_kontenera:port_wewnetrzny/nazwa_bazy
SQLALCHEMY_DATABASE_URL = "postgresql://nbp_user:nbp_password@db:5432/nbp_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()