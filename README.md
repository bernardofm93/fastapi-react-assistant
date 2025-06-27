# 🧠 FastAPI ReAct Assistant
![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI Version](https://img.shields.io/badge/FastAPI-0.111.1-green)
![LangChain](https://img.shields.io/badge/LangChain-0.1.20-purple)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-orange)

Assistente Conversacional que utiliza **ReAct Agent** para responder perguntas sobre produtos e SAC, combinando **consulta em SQL** e/ou **busca semântica**.  
O projeto inclui:

✅ **FastAPI** como backend HTTP  
✅ **LangGraph + LangChain** para criação do agente ReAct  
✅ **Ollama** como servidor local de modelos LLM e embeddings  
✅ **ChromaDB** como banco vetorial do SAC e dos nomes dos produtos  
✅ **SQLite** para persistir histórico de conversas e catálogo de produtos  

---

## 🖥️ :computer: Requisitos

- :snake: [**Python 3.10+**](https://www.python.org/downloads/)
- :whale: [**Docker**](https://www.docker.com/products/docker-desktop/)
- [**Ollama**](https://ollama.com/download) (Para rodar modelos de LLM e embeddings)


⸻

🏃 :pushpin: Rodando localmente

Antes de tudo, certifique-se de que Ollama está rodando e de que os modelos foram baixados.

📥 Clone o repositório

git clone https://github.com/seu-usuario/fastapi-react-assistant.git


⸻

🧰 Instale as dependências

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


⸻

🤖 Baixe modelos no Ollama

ollama pull llama3.1
ollama pull mxbai-embed-large


⸻

🗃️ Preprocessamento inicial

Gera o banco de produtos (produtos.db) e popula o ChromaDB com embeddings:

python -m app.db.preprocess


⸻

🚀 Suba a API

uvicorn app.main:app --reload

Por padrão, estará disponível em:

http://localhost:8000


⸻

📚 Endpoints

🔹 POST /chat/

Envia uma pergunta e recebe a resposta do assistente.

Exemplo de body:

{
  "question": "Quais calças custam menos de 200 reais?",
  "thread_id": "minha-conversa-123"
}


⸻

🔹 GET /historico/{thread_id}

Recupera todo o histórico da conversa.

Parâmetros de query opcionais:
	•	columns: Quais colunas retornar (role, content, timestamp, tokens_input, tokens_output)

Exemplo:

/historico/minha-conversa-123?columns=role&columns=content


⸻

🔹 Swagger Docs

Interface interativa:

http://localhost:8000/docs


⸻

🐳 :whale: Docker

Você também pode rodar tudo via Docker Compose.

⸻

🛠️ Build da imagem

docker build -t fastapi-react-assistant .


⸻

🚀 Run com Docker

Certifique-se que o Ollama está rodando no host e passe o .env:

docker run -d --env-file .env -p 8000:8000 --name assistant fastapi-react-assistant


⸻


🧠 Exemplos de uso com cURL

Enviar pergunta:

curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{"question":"Quantos produtos custam abaixo de 200 reais?","thread_id":"teste"}'

Consultar histórico:

curl "http://localhost:8000/historico/teste


⸻

⚠️ Observações
	•	O Ollama precisa estar rodando localmente ou acessível no OLLAMA_BASE_URL.
	•	Os modelos devem estar baixados previamente.