import os
import json

from pydantic import BaseModel
from openai import OpenAI
from .llm_client import LLMClient


class ResearchAnswerExtraction(BaseModel):
    question: str
    answer: str
    sources: list[str]


class OpenAIClient(LLMClient):
    def __init__(self, model_name="text-embedding-3-large"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model_name = model_name

    def embed(self, text: str):
        client = OpenAI()

        response = client.embeddings.create(input=text, model="text-embedding-3-small")

        return response.data[0].embedding

    def response(
        self,
        question,
        text_chunks,
        model="gpt-5.4-mini",
        instructions=None,
        prompt=None,
        text_chunks_example=None,
        question_example=None,
    ):
        # TODO: Actually stream the response
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

        if not instructions:
            instructions = f"""
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
            """
        if not prompt:
            prompt = f"""
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

        client = OpenAI()

        response = client.responses.parse(
            model=model,
            input=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": prompt},
            ],
            text_format=ResearchAnswerExtraction,
        )

        for output in response.output:
            if output.type != "message":
                continue

            for item in output.content:
                if item.type == "refusal":
                    return item.refusal

                if not item.parsed:
                    raise Exception("Could not parse response")

        return item.text
