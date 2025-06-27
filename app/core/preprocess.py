import re
from uuid import uuid4
from typing import List, Dict

def split_faq_by_question_and_sentences(text: str) -> List[Dict]:
    """
    Divide um texto de FAQ em blocos com a estrutura:
    Pergunta: <pergunta>
    Resposta: <parte da resposta>.
    
    A pergunta começa com "# <texto>?" e a resposta é separada por ".\n"
    """
    pattern = r"# (.*\?)"
    matches = list(re.finditer(pattern, text))
    chunks = []

    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        question = match.group(1).strip()
        answer_block = text[start:end].strip()

        subchunks = re.split(r"\.\s*\n", answer_block)
        subchunks = [chunk.strip() for chunk in subchunks if chunk.strip()]

        for j, sub in enumerate(subchunks):
            chunk_text = f"Pergunta: {question}\nResposta: {sub}."
            chunks.append({
                "text": chunk_text,
                "metadata": {
                    "question": question,
                    "chunk_id": f"{i}-{j}"
                }
            })

    return chunks

def load_and_process_faq(md_filepath: str) -> List[str]:
    """
    Lê os dados do SAC e retorna os chunks prontos para vetorização.
    """
    with open(md_filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    chunks = split_faq_by_question_and_sentences(content)
    return [c['text'] for c in chunks]

def uuids_for_chunks(chunks: List[str]) -> List[str]:
    """Gera UUIDs únicos para cada chunk de texto."""
    return [str(uuid4()) for _ in chunks]