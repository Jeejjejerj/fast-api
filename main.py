from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# 1. Ma'lumotlar bazasi sozlamalari
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:parol_yozing@localhost:5432/postgres")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
from sqlalchemy.orm import declarative_base
Base = declarative_base()

# 2. DB Model (Jadval)
class Item(Base):
  
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)

# Jadvalni yaratish
Base.metadata.create_all(bind=engine)

# 3. FastAPI ilovasi
app = FastAPI(title="24/7 Doimiy Ishlaydigan API")

# DB Sessiyasini boshqarish
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 4. API Yo'nalishlari (Endpoints)
@app.get("/")
def read_root():
    return {"status": "online", "message": "API muvaffaqiyatli ishlayapti!"}

@app.post("/items/")
def create_item(name: str, description: str = None, db: Session = Depends(get_db)):
    db_item = Item(name=name, description=description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/")
def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()