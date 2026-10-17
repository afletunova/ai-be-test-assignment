import os
from unittest import result
import ollama
from openai import OpenAI

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_openai_embedding():
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.embeddings.create(
        input="Test OpenAI Embedding", model="text-embedding-3-small"
    )

    print(response.data[0].embedding)


def test_ollama_connection():
    response = ollama.embed(input="Test Ollama Embedding", model="qwen3-embedding")

    print(response["embeddings"])


def test_openai_class_embed():
    from .llm_client import openai_client

    client = openai_client.OpenAIClient()

    response = client.embed("Test OpenAI Embed")

    print(response)


def test_ollama_class_embed():
    from .llm_client import ollama_client

    client = ollama_client.OllamaClient(api_url=os.environ.get("REMOTE_OLLAMA_HOST"))

    response = client.embed("Test Ollama Embed")

    print(response)


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
