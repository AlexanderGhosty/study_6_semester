import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI(title="Python Microservice 2")

# Подключение к БД через переменные окружения
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "labdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class ProcessedItem(Base):
    """Отдельная таблица для обработанных данных."""
    __tablename__ = "processed_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    original_name = Column(String(100), nullable=False)
    processed_name = Column(String(100), nullable=False)
    description = Column(Text, default="")
    source_id = Column(Integer, nullable=False)
    processed_at = Column(String(50), nullable=False)
    received_at = Column(DateTime, default=datetime.utcnow)


# Создание таблицы при запуске
Base.metadata.create_all(bind=engine)


class ProcessedItemRequest(BaseModel):
    original_name: str
    processed_name: str
    description: str = ""
    source_id: int
    processed_at: str


@app.post("/api/processed")
def receive_processed_data(data: ProcessedItemRequest):
    """Принимает обработанные данные из Микросервиса 1 и сохраняет в БД."""
    session = SessionLocal()
    try:
        item = ProcessedItem(
            original_name=data.original_name,
            processed_name=data.processed_name,
            description=data.description,
            source_id=data.source_id,
            processed_at=data.processed_at,
        )
        session.add(item)
        session.commit()
        session.refresh(item)
        return {"status": "ok", "id": item.id}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


@app.get("/api/processed")
def get_all_processed(skip: int = 0, limit: int = 100):
    """Возвращает все обработанные записи."""
    session = SessionLocal()
    try:
        items = session.query(ProcessedItem).offset(skip).limit(limit).all()
        return [
            {
                "id": i.id,
                "original_name": i.original_name,
                "processed_name": i.processed_name,
                "description": i.description,
                "source_id": i.source_id,
                "processed_at": i.processed_at,
            }
            for i in items
        ]
    finally:
        session.close()


@app.get("/health")
def health():
    return {"status": "healthy"}