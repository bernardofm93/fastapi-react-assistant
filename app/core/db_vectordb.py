import chromadb
import pandas as pd
from uuid import uuid4
from langchain_ollama import OllamaEmbeddings
from app.core.preprocess import carregar_e_processar_faq, gerar_uuids_para_chunks

client = chromadb.Client()
collection = client.create_collection(name="sac")

embeddings = OllamaEmbeddings(model="mxbai-embed-large")

DADOS_SAC = "data/dados-sac.md"
perguntas_chunks = carregar_e_processar_faq(DADOS_SAC)
uuids = gerar_uuids_para_chunks(perguntas_chunks)

for i, chunk_text in enumerate(perguntas_chunks):
    collection.add(
        ids=[uuids[i]],
        embeddings=embeddings.embed_query(chunk_text),
        documents=[chunk_text]
    )

def search_sac(question: str):
    """Busca informações sobre o serviço de atendimento ao cliente."""
    embedded = embeddings.embed_query(question)
    results = collection.query(
        query_embeddings=[embedded],
        n_results=3
    )
    return results

DADOS_CATALOGO = "data/dados-produtos.json"
catalogo = pd.read_json(DADOS_CATALOGO)
catalog_collection = client.create_collection(name="catalog")
for i, row in catalogo.iterrows():
    catalog_collection.add(
        ids=[str(uuid4())],
        embeddings=embeddings.embed_query(row['description']),
        documents=[row['description']],
        metadatas=[{"productId": row['productId'], "title": row['title']}]
    )

def search_proper_nouns_catalog(question):
    """Busca de produtos no catálogo por similaridade semântica ao produto procurado pelo cliente. 
    Os dados retornados correspondem à coluna 'description' da tabela 'produtos'. Caso necessário, a pergunta do cliente pode ser reescrita para melhorar a busca."""
    embedded = embeddings.embed_query(question)
    results = catalog_collection.query(
        query_embeddings=[embedded],
        n_results=5
    )
    print(results['documents'][0])
    print(results['metadatas'][0])
    return results