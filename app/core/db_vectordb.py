from uuid import uuid4
import chromadb
import pandas as pd

from langchain_ollama import OllamaEmbeddings

from app.core.preprocess import load_and_process_faq, uuids_for_chunks

client = chromadb.Client()
collection = client.create_collection(name="sac")

embeddings = OllamaEmbeddings(model="granite-embedding:278m")

DADOS_SAC = "data/dados-sac.md"
perguntas_chunks = load_and_process_faq(DADOS_SAC)
uuids = uuids_for_chunks(perguntas_chunks)

for i, chunk_text in enumerate(perguntas_chunks):
    collection.add(
        ids=[uuids[i]],
        embeddings=embeddings.embed_query(chunk_text),
        documents=[chunk_text]
    )

def search_sac(question: str):
    """Busca informações sobre o serviço de atendimento ao cliente e perguntas mais frequentes."""
    embedded = embeddings.embed_query(question)
    results = collection.query(
        query_embeddings=[embedded],
        n_results=5
    )
    return results


DADOS_CATALOGO = "data/dados-produtos.json"
catalog = pd.read_json(DADOS_CATALOGO)
catalog_collection = client.create_collection(name="catalog")

for i, row in catalog.iterrows():
    catalog_collection.add(
        ids=[str(uuid4())],
        embeddings=embeddings.embed_query(row['description']),
        documents=[row['description']],
        metadatas=[{"productId": row['productId'], "title": row['title'], "price": row['price']}]
    )

def search_proper_nouns_catalog(question):
    """Busca produtos no catálogo com base na similaridade semântica em relação ao que o cliente está procurando.
    Os dados retornados correspondem à coluna description da tabela produtos. 
    Se julgar necessário, você pode reescrever ou reformular a pergunta do cliente para aprimorar a qualidade da busca."""
    embedded = embeddings.embed_query(question)
    results = catalog_collection.query(
        query_embeddings=[embedded],
        n_results=5
    )
    print(results['documents'][0])
    print(results['metadatas'][0])
    return results