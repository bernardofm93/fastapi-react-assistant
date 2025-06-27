from fastapi import FastAPI

from app.api.endpoints import chat, history

app = FastAPI(
    title="Assistente Inteligente",
    description="API para responder perguntas sobre produtos e atendimento ao cliente usando LLM",
    version="1.0.0"
)

app.include_router(chat.router, prefix="/chat")
app.include_router(history.router, prefix="/historico")