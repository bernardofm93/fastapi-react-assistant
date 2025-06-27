from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage

from app.core.db_sqlite import search_sql
from app.core.db_vectordb import search_sac, search_proper_nouns_catalog
from app.core.tracking import save_interaction

model = init_chat_model(
    model="llama3.1",
    model_provider="ollama",
    temperature=0
)

checkpointer = InMemorySaver()

REACT_PROMPT = """
Você é um assistente especializado em responder perguntas sobre a C&A. 

Você possui acesso às respostas para as perguntas mais frequentes e ao catálogo com descrição detalhada e preço dos produtos.
Caso julgue necessário, você pode utilizar mais de uma ferramenta para responder à pergunta do usuário.

Considere o contexto da conversa antes de acionar alguma das ferramentas.

Pense antes de responder, avaliando se a informação encontrada nas ferramentas é pertinente à pergunta do usuário.
"""

agent_executor = create_react_agent(model=model, 
                                    tools=[search_sac, search_sql, search_proper_nouns_catalog], 
                                    prompt=REACT_PROMPT, 
                                    checkpointer=checkpointer)

def answer_question(question: str, thread_id: str = ""):
    """Responde a uma pergunta do usuário utilizando Agente ReAct."""
    config = {"configurable": {"thread_id": thread_id}}
    last_event = None
    input_tokens = 0
    output_tokens = 0

    save_interaction(thread_id, "user", question)

    for event in agent_executor.stream(
        {"messages": [{"role": "user", "content": question}]},
        stream_mode="values", config=config,
    ):
        event["messages"][-1].pretty_print()
        last_event = event            

    for message in last_event["messages"]:
        if isinstance(message, AIMessage):
            input_tokens += message.usage_metadata['input_tokens']
            output_tokens += message.usage_metadata['output_tokens']
    
    resposta = last_event["messages"][-1].content

    save_interaction(thread_id, "assistant", resposta, last_event["messages"], 
                     input_tokens, output_tokens, input_tokens + output_tokens)

    return {
        "query": question,
        "answer": resposta,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens
    }