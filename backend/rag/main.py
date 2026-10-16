from llm_client import llm_client, ollama_client, openai_client

import os


def get_llm_client(mode: str) -> llm_client.LLMClient:
    if mode == "ollama":
        api_url = os.environ.get("REMOTE_OLLAMA_HOST")
        return ollama_client.OllamaClient(api_url=api_url)
    elif mode == "openai":
        return openai_client.OpenAIClient()
    else:
        raise ValueError(f"Unsupported embedding mode: {mode}")


def main():
    mode = os.environ.get("MODE")
    client = get_llm_client(mode)

    text = "Example input text for embedding"
    embeddings = client.embed(text)
    print(f"Embeddings from {mode}:", embeddings)


if __name__ == "__main__":
    main()
