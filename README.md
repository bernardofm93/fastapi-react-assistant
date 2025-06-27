# 🧠 FastAPI ReAct Assistant
![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI Version](https://img.shields.io/badge/FastAPI-0.115.13-green)
![LangChain](https://img.shields.io/badge/LangChain-0.3.26-purple)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-orange)

Assistente Conversacional que utiliza um **Agente ReAct** para responder perguntas sobre produtos e SAC, combinando **consulta em SQL** e/ou **busca semântica**.  
O projeto inclui:

✅ **FastAPI** como backend HTTP  
✅ **LangGraph + LangChain** para criação do agente ReAct  
✅ **Ollama** como servidor local de modelos LLM e embeddings  
✅ **ChromaDB** como banco vetorial do SAC e dos nomes dos produtos  
✅ **SQLite** para persistir histórico de conversas e catálogo de produtos

---

🧩 Visão Geral

O projeto implementa um ReAct Agent que combina raciocínio e ações sobre diferentes fontes de dados para responder perguntas relacionadas ao catálogo e ao serviço de atendimento ao cliente da C&A.

⸻

🖼️ Arquitetura do Agente

A arquitetura de um agente ReAct pode ser representada por um grafo, contendo um nodo de assistente e outro de ferramentas, conforme imagem abaixo. 

![alt text](image.png)

O agente ReAct segue a lógica:
	1.	Recebe a pergunta do usuário
	2.	Analisa o contexto e o histórico
	3.	Decide qual ou quais ferramentas utilizar
	4.	Executa buscas SQL ou semânticas conforme necessário
	5.	Combina e organiza a resposta final


⸻

🛠️ Ferramentas Utilizadas

O agente conta com duas ferramentas principais:

- Busca SQL de Produtos	Realiza consultas estruturadas na base de dados SQLite para retornar informações detalhadas sobre produtos, como preço, título e descrição. Ideal para perguntas objetivas que envolvem filtros e atributos conhecidos.
- Busca Semântica de FAQ	Utiliza embeddings gerados via Ollama e ChromaDB para recuperar respostas por similaridade semântica. Indicada para perguntas abertas ou quando o usuário utiliza linguagem natural sem correspondência direta no catálogo.

⸻


## 🖥️ :computer: Requisitos

- :snake: [**Python 3.10+**](https://www.python.org/downloads/)
- :whale: [**Docker**](https://www.docker.com/products/docker-desktop/)
- [**Ollama**](https://ollama.com/download) (Para rodar modelos de LLM e embeddings)


⸻

🏃 :pushpin: Rodando localmente

Antes de tudo, certifique-se de que o Ollama está rodando e de que os modelos foram baixados.


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

Exemplo de Request body:

        {
        "question": "Quais calças custam menos de 200 reais?",
        "thread_id": "thread-123"
        }


⸻

🔹 GET /historico/{thread_id}

Recupera todo o histórico da conversa a partir do ID da thread.


⸻

🔹 Swagger Docs

Interface interativa:

http://localhost:8000/docs


⸻

🐳 :whale: Docker

Rodando via Docker Compose.

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

📓 🧪 Testando em Jupyter Notebook

Caso seja mais acessível, é possível realizar o teste no arquivo **teste_agente.ipynb**. 