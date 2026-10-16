import os

from openai import OpenAI
from .llm_client import LLMClient


class OpenAIClient(LLMClient):
    def __init__(self, model_name="text-embedding-3-large"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model_name = model_name

    def embed(self, text: str):
        client = OpenAI()

        response = client.embeddings.create(input=text, model="text-embedding-3-small")

        return response.data[0].embedding
