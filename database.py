import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables dari file .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Debugging untuk memastikan URL database terbaca (dari versi teman)
print("DATABASE_URL =", DATABASE_URL)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True, # Memastikan koneksi tetap hidup
    pool_recycle=3600,
    echo=True 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependency FastAPI yang menyediakan sesi database untuk setiap request.
    Koneksi akan ditutup otomatis setelah request selesai.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()