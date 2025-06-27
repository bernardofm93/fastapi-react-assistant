from fastapi import APIRouter
from app.models.request import ChatRequest
from app.core.agent import answer_question

router = APIRouter()

@router.post("/")
def chat(req: ChatRequest):
    """
    Recebe uma pergunta e um ID de thread, e retorna a resposta do assistente.
    """
    return answer_question(req.question, req.thread_id)