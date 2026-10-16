import os
import ollama
from openai import OpenAI


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
