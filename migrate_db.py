from sqlalchemy import create_engine, text
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Ganesh@2022")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "minipay")

encoded_password = quote_plus(DB_PASSWORD)
DATABASE_URL = f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

def run_migration():
    with engine.connect() as conn:
        try:
            # Check if column exists (PostgreSQL specific way, or just try-catch)
            # Simplest for now: Try adding it, ignore if fails
            conn.execute(text("ALTER TABLE transactions ADD COLUMN items VARCHAR"))
            conn.commit()
            print("Migration successful: Added 'items' column.")
        except Exception as e:
            print(f"Migration failed (maybe column exists?): {e}")

if __name__ == "__main__":
    run_migration()
