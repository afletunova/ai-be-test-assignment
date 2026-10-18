from .llm_client import llm_client, ollama_client, openai_client

from pgvector import Vector
from pgvector.psycopg import register_vector

from langchain_text_splitters import RecursiveCharacterTextSplitter

import psycopg
import json
import os


def get_llm_client(mode: str) -> llm_client.LLMClient:
    if mode == "ollama":
        api_url = os.environ.get("REMOTE_OLLAMA_HOST")
        return ollama_client.OllamaClient(api_url=api_url)
    elif mode == "openai":
        return openai_client.OpenAIClient()
    else:
        raise ValueError(f"Unsupported embedding mode: {mode}")


def init_db(conn):
    # TODO: run once at startup
    # TODO: dimension is hardcoded, but it should match the embedder
    conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
    register_vector(conn)
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS text_chunks (
            id bigserial PRIMARY KEY,
            content text,
            embedding vector({os.environ.get("VECTOR_SIZE")})
        )
        """)


def embed_and_store(llm_client, text):
    # TODO: reuse one connection
    # TODO: make the connection a parameter and do not create one inside
    # TODO: use batch embed
    # TODO: store source name and identify each chunk
    DATABASE_URL = (
        os.environ.get("DATABASE_URL")
        or f"postgresql://{os.environ.get('POSTGRES_USER', 'postgres')}:{os.environ.get('POSTGRES_PASSWORD', 'password')}@db:5432/{os.environ.get('POSTGRES_DB', 'research_semantic')}"
    )
    conn = psycopg.connect(DATABASE_URL, autocommit=True)
    register_vector(conn)
    cur = conn.cursor()
    try:
        embedding = llm_client.embed(text)
        query = "INSERT INTO text_chunks (content, embedding) VALUES (%s, %s::vector) RETURNING id"
        cur.execute(query, (text, embedding))
        id = cur.fetchone()[0]
    finally:
        conn.close()

    return id


def chunk_and_process(llm_client, text_data):
    # Split one document into overlapping chunks, then embed and insert each.
    # TODO: accept filename/metadata
    # TODO: keep the same connection
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", " ", ""]
    )

    docs = text_splitter.create_documents([text_data])
    docs_id = []
    chunks_content = []

    for doc in docs:
        chunk_id = embed_and_store(llm_client=llm_client, text=doc.page_content)
        docs_id.append(chunk_id)
        chunks_content.append(doc)

    return docs_id, chunks_content


def search(llm_client, question_id, k=5):
    DATABASE_URL = (
        os.environ.get("DATABASE_URL")
        or f"postgresql://{os.environ.get('POSTGRES_USER', 'postgres')}:{os.environ.get('POSTGRES_PASSWORD', 'password')}@db:5432/{os.environ.get('POSTGRES_DB', 'research_semantic')}"
    )
    conn = psycopg.connect(DATABASE_URL, autocommit=True)
    cur = conn.cursor()
    try:
        question_embed_query = "SELECT embedding FROM text_chunks WHERE id = %s;"
        cur.execute(question_embed_query, (question_id,))
        question_embed = cur.fetchone()[0]

        results_query = (
            "SELECT id, content FROM text_chunks ORDER BY embedding <-> %s LIMIT %s;"
        )
        cur.execute(results_query, (question_embed, k))
        results = cur.fetchall()
    finally:
        conn.close()

    top_k_similar_texts = [{"id": row[0], "content": row[1]} for row in results]

    return top_k_similar_texts


def research_and_answer(llm_client, text):
    # TODO: stream the response
    docs_id, questions = chunk_and_process(llm_client, text)

    for id, question in zip(docs_id, questions):
        question_text = question.page_content
        text_chunks = search(llm_client, id)
        response = llm_client.response(question, text_chunks)

        if isinstance(response, str):
            response = json.loads(response)

        yield response


def main():
    # TODO: add retrieve(query)
    mode = os.environ.get("MODE") or "ollama"
    client = get_llm_client(mode)

    text = "Example input text for embedding"
    chunk_and_process(client, text)


if __name__ == "__main__":
    main()
