import os
import time
from sqlalchemy import create_engine

# Pastikan kita mengimpor Base dan semua model Anda
# agar SQLAlchemy tahu tabel apa saja yang harus dibuat.
from src.models.db_models import Base
from src.models.db_models import Request, Result, User

# Ambil URL database dari environment variable yang sama
DATABASE_URL = os.getenv("DATABASE_URL")

def create_db_tables():
    """
    Script untuk membuat tabel di database.
    Akan mencoba koneksi beberapa kali jika database belum siap.
    """
    print("Migration script started...")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable not set")

    retries = 5
    while retries > 0:
        try:
            print("Attempting to connect to the database...")
            engine = create_engine(DATABASE_URL)
            Base.metadata.create_all(bind=engine)
            print("Tables created successfully!")
            # Inisialisasi user default
            # (Anda bisa menambahkan logika ini jika perlu)
            print("Database tables are ready.")
            break
        except Exception as e:
            retries -= 1
            print(f"Could not connect to database: {e}")
            print(f"Retrying in 5 seconds... ({retries} retries left)")
            time.sleep(5)
    
    if retries == 0:
        print("Could not create tables after several retries. Exiting.")
        exit(1)


if __name__ == "__main__":
    create_db_tables()