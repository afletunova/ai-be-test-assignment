import requests
import subprocess

from .llm_client import LLMClient


class OllamaClient(LLMClient):
    def __init__(self, api_url, model_name="qwen3-embedding"):
        if api_url is None:
            raise ValueError("api_url must be provided and cannot be None")
        self.api_url = api_url.rstrip("/")
        self.model_name = model_name

    def embed(self, text: str):
        if not text:
            raise ValueError("Input text cannot be empty")

        payload = {"text": text}

        response = requests.post(self.api_url, json=payload)
        response.raise_for_status()

        data = response.json()
        if "embedding" in data:
            return data["embedding"]
        elif "error" in data:
            raise RuntimeError(f"Error from embedding API: {data['error']}")
        else:
            raise RuntimeError("Unexpected response format from embedding API")
