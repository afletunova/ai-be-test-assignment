from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def embed(self, text: str):
        pass

    def response(self, question: str, text_chunks: list, model: str = None, **kwargs):
        pass
