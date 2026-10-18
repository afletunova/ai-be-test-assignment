import requests
import subprocess
import json

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

        response_url = f"{self.api_url}/embed"
        response = requests.post(response_url, json=payload)
        response.raise_for_status()

        data = response.json()
        embedding = data.get("embedding")
        if isinstance(embedding, str):
            embedding = json.loads(embedding)
        if isinstance(embedding, list):
            return embedding
        elif "error" in data:
            raise RuntimeError(f"Error from embedding API: {data['error']}")
        else:
            raise RuntimeError("Unexpected response format from embedding API")

    def response(
        self,
        question,
        text_chunks,
        model="qwen2.5:3b",
        text_chunks_example=None,
        question_example=None,
    ):
        # TODO: Actually stream the response

        if not question:
            raise ValueError("Input question cannot be empty")

        question_example = "What are the main causes of climate change?"
        text_chunks_example = """
        [
            {
                "id": 12345,
                "content": "Climate change is primarily caused by the increase in greenhouse gases such as carbon dioxide and methane."
            },
            {
                "id": 124595,
                "content": "Deforestation and burning fossil fuels contribute significantly to greenhouse gas emissions."
            }
        ]
        """
        output_format_example = """
        {
            "question": "What are the main causes of climate change?",
            "answer": "Climate change is mainly caused by increased greenhouse gas emissions, especially carbon dioxide and methane, with major contributors including fossil fuel burning and deforestation.",
            "sources": [12345, 124595]
        }
        """

        full_prompt = f"""
            You are an expert research assistant.
            You will be give a research question and a text chunks that might provide an answer to the question.
            Use the provided chunks from documents to generate an answer to the research question only if the answer is supported by the chunks.
            Return your response in a structured JSON format so it can be parsed downstream.

            The question format:
            ```json
            {question_example}
            ```

            The chunks format: 
            ```json
            {text_chunks_example}
            ```

            The response format:
            ```json
            {output_format_example}
            ```

            Your goal is to carefully read this question, and then read provided materials to answer the question in a clear, concise, and accurate way based solely on the information contained in the provided text chunks.

            Instructions:
            1. Understand the research question.
            2. Read the provided text chunk or chunks thoroughly.
            3. Extract and synthesise the relevant information from the text to answer the question.
            4. If the text is irrelevant or doesn't contain enough information to answer the question, respond with: "The provided text does not contain sufficient information to answer the question."
            5. Leave references to sources of the text chunks where it is possible and adequate.
            6. Convert your answer in a given response structure, for sources return only their ids.

            The research question:
            {question}
            
            Text chunks:
            {json.dumps(text_chunks, indent=4)}
        """

        response_schema = {
            "type": "object",
            "properties": {
                "question": {"type": "string"},
                "answer": {"type": "string"},
                "sources": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["question", "answer", "sources"],
        }

        logger.info(f"Full Promt: {full_prompt}")

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": full_prompt}],
            "format": response_schema,
        }

        response_url = f"{self.api_url}/v1/systemone"
        response = requests.post(response_url, json=payload)
        response.raise_for_status()

        data = response.json()
        if "message" in data and "content" in data["message"]:
            return data["message"]["content"]
        else:
            raise RuntimeError(f"Unexpected response format: {data}")
