from fastapi import APIRouter
from app.db.database import conn

router = APIRouter()

@router.get("/{thread_id}")
def get_thread_history(thread_id: str):
    """Recupera o histórico de conversa para uma thread específica."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT role, content, timestamp FROM conversa
        WHERE thread_id = ?
        ORDER BY timestamp
    """, (thread_id,))
    
    rows = cursor.fetchall()
    return [
        {"role": row[0], "content": row[1], "timestamp": row[2]}
        for row in rows
    ]