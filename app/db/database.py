import sqlite3
from pathlib import Path

DB_PATH = Path("app/db/conversas.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    """Inicializa o banco de dados SQLite e cria a tabela de conversas se não existir."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            thread_id TEXT,
            role TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            tokens_prompt INTEGER,
            tokens_completion INTEGER,
            tokens_total INTEGER
        )
    """)
    conn.commit()

init_db()