import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = PROJECT_DIR / "database"
DATABASE_FILE = DATABASE_DIR / "sales.db"

def get_connection():
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_FILE)

    return connection