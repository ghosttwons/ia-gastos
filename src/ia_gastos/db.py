from pathlib import Path
import sqlite3

DB_PATH = Path.home() / ".ia_gastos" / "gastos.db"

SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS expenses (
  id INTEGER PRIMARY KEY,
  date TEXT NOT NULL,
  description TEXT NOT NULL,
  amount REAL NOT NULL,
  method TEXT,
  category TEXT
);
CREATE TABLE IF NOT EXISTS bills (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  amount REAL NOT NULL,
  due_day INTEGER NOT NULL,
  category TEXT,
  notify_days_before INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS budgets (
  id INTEGER PRIMARY KEY,
  month TEXT NOT NULL,        -- yyyy-mm
  category TEXT NOT NULL,
  amount REAL NOT NULL
);
"""

def ensure_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as con:
        con.executescript(SCHEMA)

def connect():
    ensure_db()
    return sqlite3.connect(DB_PATH)
