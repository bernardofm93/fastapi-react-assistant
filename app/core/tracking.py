from app.db.database import conn

def save_interaction(
    thread_id: str,
    role: str,
    content: str,
    tokens_prompt: int = 0,
    tokens_completion: int = 0,
    tokens_total: int = 0
):
    """
    Salva uma entrada no histórico da conversa no SQLite.
    """
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO conversa (
            thread_id,
            role,
            content,
            tokens_prompt,
            tokens_completion,
            tokens_total
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (thread_id, role, content, tokens_prompt, tokens_completion, tokens_total))

    conn.commit()