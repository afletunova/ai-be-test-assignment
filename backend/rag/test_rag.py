import os
from unittest import result
import ollama
from openai import OpenAI
from pathlib import Path

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

test_files_dir = Path(__file__).parent.parent / "tests" / "assets"


def test_openai_embedding():
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.embeddings.create(
        input="Test OpenAI Embedding Connection", model="text-embedding-3-small"
    )

    logger.info(
        f"Test OpenAI Embedding Connection Results: {response.data[0].embedding}"
    )


def test_ollama_connection():
    response = ollama.embed(
        input="Test Ollama Embedding Connection", model="qwen3-embedding"
    )

    logger.info(f"Test Ollama Embedding Connection Results: {response["embeddings"]}")


def test_openai_class_embed():
    from .llm_client import openai_client

    client = openai_client.OpenAIClient()

    response = client.embed("Test OpenAI Embed")

    logger.info(f"Test OpenAI Embed Results{response}")


def test_ollama_class_embed():
    from .llm_client import ollama_client

    client = ollama_client.OllamaClient(api_url=os.environ.get("REMOTE_OLLAMA_HOST"))

    response = client.embed("Test Ollama Embed")

    logger.info(f"Test Ollama Embed Results{response}")


def test_embed_and_store():
    from .main import embed_and_store
    from .llm_client import ollama_client

    client = ollama_client.OllamaClient(api_url=os.environ.get("REMOTE_OLLAMA_HOST"))

    embed_and_store(client, "Test embed_and_store")


def test_chunk_and_process():
    from .main import chunk_and_process
    from .llm_client import ollama_client

    client = ollama_client.OllamaClient(api_url=os.environ.get("REMOTE_OLLAMA_HOST"))

    chunk_and_process(client, "Test chunk_and_process")


def test_search():
    from .main import search
    from .llm_client import ollama_client

    client = ollama_client.OllamaClient(api_url=os.environ.get("REMOTE_OLLAMA_HOST"))

    results = search(client, 2)

    logger.info(f"Test Search Results: {results}")


def test_openai_response():
    from .llm_client import openai_client

    client = openai_client.OpenAIClient()

    question = "What is the capital of France?"
    text_chunks = [
        {"id": 48201193, "content": "France is a country in Western Europe."},
        {"id": 92028485, "content": "Paris is the capital and largest city of France."},
    ]

    response = client.response(question, text_chunks)

    logger.info(f"Test OpenAI Response Result: {response}")


def test_ollama_response():
    from .llm_client import ollama_client

    client = ollama_client.OllamaClient(api_url=os.environ.get("REMOTE_OLLAMA_HOST"))

    question = "What is the capital of France?"
    text_chunks = [
        {"id": 48201193, "content": "France is a country in Western Europe."},
        {"id": 92028485, "content": "Paris is the capital and largest city of France."},
    ]

    response = client.response(question, text_chunks)

    logger.info(f"Test Ollama Response Result: {response}")


def test_full_rag_with_ollama():
    from .main import chunk_and_process, research
    from .llm_client import ollama_client
    import os

    client = ollama_client.OllamaClient(api_url=os.environ.get("REMOTE_OLLAMA_HOST"))

    file = test_files_dir / "file1.md"

    with open(file, "r") as f:
        document_text = f.read()
        logger.info(f"Loaded document with {len(document_text)} characters")

    docs_id, chunks_content = chunk_and_process(client, document_text)
    logger.info(f"Created {len(docs_id)} chunks with IDs: {docs_id}")

    question = "What is the role of the hippocampus and neocortex in memory formation?"
    logger.info(f"Research question: {question}")

    response = research(client, question)
    responses = list(research(client, question))
    logger.info(f"Research answers: {responses}")
