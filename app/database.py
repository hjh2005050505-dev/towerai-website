from __future__ import annotations

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "towerai.sqlite3"

def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                company TEXT,
                contact TEXT,
                interest TEXT,
                message TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

def save_lead(name: str, company: str, contact: str, interest: str, message: str) -> int:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("INSERT INTO leads (name, company, contact, interest, message) VALUES (?, ?, ?, ?, ?)", (name, company, contact, interest, message))
        return int(cursor.lastrowid)
