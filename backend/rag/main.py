# Draft ingest path. Not wired to POST /api/sources yet.
# Not tested: DB, chunk-to-vector, retrieval
# Not implemented yet: search, answer gen

from .llm_client import llm_client, ollama_client, openai_client

from pgvector import Vector
from pgvector.psycopg import register_vector
from langchain_text_splitters import RecursiveCharacterTextSplitter

import psycopg
import os


def get_llm_client(mode: str) -> llm_client.LLMClient:
    if mode == "ollama":
        api_url = os.environ.get("REMOTE_OLLAMA_HOST")
        return ollama_client.OllamaClient(api_url=api_url)
    elif mode == "openai":
        return openai_client.OpenAIClient()
    else:
        raise ValueError(f"Unsupported embedding mode: {mode}")


"""!!! The part from here to the next comment is not tested !!!"""


def init_db(conn):
    # TODO: run once at startup
    # TODO: dimension is hardcoded, but it should match the embedder
    conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
    register_vector(conn)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS text_chunks (
            id bigserial PRIMARY KEY,
            content text,
            embedding vector(1536)
        )
        """)


def embed_and_store(llm_client, text):
    # TODO: reuse one connection
    # TODO: use batch embed
    # TODO: store source name and identify each chunk
    conn = psycopg.connect(os.environ["DATABASE_URL"], autocommit=True)
    try:
        init_db(conn)
        embedding = llm_client.embed(text)
        conn.execute(
            "INSERT INTO text_chunks (content, embedding) VALUES (%s, %s)",
            (text, Vector(embedding)),
        )
    finally:
        conn.close()


def chunk_and_process(llm_client, text_data):
    # Split one document into overlapping chunks, then embed and insert each.
    # TODO: accept filename/metadata
    # TODO: keep the same connection
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", " ", ""]
    )

    docs = text_splitter.create_documents([text_data])

    for doc in docs:
        embed_and_store(llm_client=llm_client, text=doc.page_content)


def main():
    # TODO: add retrieve(query)
    mode = os.environ.get("MODE") or "ollama"
    client = get_llm_client(mode)

    text = "Example input text for embedding"
    chunk_and_process(client, text)


"""!!! The not tested part is ending here!!!"""

if __name__ == "__main__":
    main()
