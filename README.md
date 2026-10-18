# AI Engineer Technical Test. Backend API — Research Agent.

This repository showcases the research agent I created for an AI Engineer position. 

## Overview

This backend module is supposed to:

- Receive REST requests from the provided frontend.
- Stream responses back to the provided frontend.
- Embed uploaded source files & query at the correct times.
- Build an LLM research agent that acts on the user’s research request.
- The agent should be able to utilise external sources.

At the moment, it does everything in the list above except using external sources. Also, its compatibility with the provided Frontend is not fully tested yet.

## Architecture

For the API side, I chose FastAPI as an efficient Python framework. Automatic documentation also covers part of the assignment.

What's working now: 

- REST endpoints functional
- Streaming research responses implemented
- File embedding working
- Research agent with LLM answer generation

External resources were not yet covered.

I also implemented an LLM client abstraction, letting me choose between Ollama and OpenAI models. Currently, I’ve been testing this solution primarily on Ollama to save on OpenAI tokens.

For the database, I chose PostgreSQL with the pgvector extension since I am familiar with both and it’s a good combination to use for this prototype.

## Prerequisites

- Docker & Docker Compose
- Python 3.14+
- PostgreSQL with pgvector (presented here via official Docker image)
- Ollama server (I spun up my own on Flask) or OpenAI API key



## Environmental Variables

Most of them are optional. However, to test this pipeline, it is better to either fill in Ollama’s remote host var, or to use an OpenAI API key.

## Installation & Setup

I recommend using Docker.

1. Clone repository

```bash
git clone https://github.com/afletunova/ai-be-test-assignment.git
```

1. Set up the '.env' file

```bash
cd ai-be-test-assignment.git
cp .env.example .env
```

And fill in the missing variables with your own credentials

1. (Optional) Run docker compose

```bash
docker compose up
```

This step should create two containers: 

- one with the backend itself 
- and the second with the PostgreSQL database

Or you can proceed without Docker

### Local Development

1. Install dependencies

```bash
pip install -r requirements.txt
```

1. Run the backend locally with your own PostgreSQL DB.

```bash
fastapi run main.py --port 8080
```



## API Endpoints

1. `POST /api/research`
  - Summary: Research endpoint, expecting the research request as input, and streaming the answer back.
  - Request Body:
    - Content-Type: `application/json`
    - Schema:
    ```json
    {
        "request": "string"
    }
    ```
    - Responses: 
      - `200 OK` — Successful response
      - `422 Unprocessable Entity` — Validation error, returns details about the validation issues.
2. `POST /api/sources`
  - Summary: Upload files to the backend and process them.
  - Request Body: 
    - Content-Type: `multipart/form-data`
    - Schema:
    ```json
    {
        "files": [
            "binary file content"
        ]
    }
    ```
    - Required field: `files` (array of files)
  - Responses: 
    - `200 OK` — Successful upload response. Output reference: UploadResult. Contains an array of uploaded files with properties:
      - `name` (string)
      - `size` (integer)
      - `type` (string)
    - `422 Unprocessable Entity` — Validation error, returns details about the validation issues.



## Project Structure

app/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── rag/
│   │   ├── main.py          # RAG pipeline (chunking, embedding, search, research)
│   │   ├── llm_client/      # LLM client abstraction
│   │   │   ├── llm_client.py       # Base interface
│   │   │   ├── openai_client.py    # OpenAI implementation
│   │   │   └── ollama_client.py    # Ollama implementation
│   │   └── test_rag.py      # RAG tests
│   └── rest/
│       ├── research.py      # /api/research endpoint
│       └── sources.py       # /api/sources endpoint
├── postgres/
│   ├── init-db.sh          # Database initialization script
│   └── schema.sql          # Database schema with pgvector
├── compose.yaml            # Docker Compose configuration
└── .env.example           # Environment variables template

## Key Features

- This RAG pipeline supports switching between locally running Ollama and OpenAI with MODE and VECTOR_SIZE env variables.
- Vector Search is supported by pgvector semantic search.
- Chunking is performed via RecursiveCharacterTextSplitter for optimal chunk sizes.
- Research requests can also be chunked.
- The deployment is containerised with PostgreSQL and the backend.
- Logging and exception handling are supported on a basic level.



## Testing

You can run tests using pytest (with env variables set up): 

```bash
pytest backend/rag/test_rag.py -v
pytest backend/rest/test_endpoints.py -v
```

Or test specific functionality

```bash
pytest backend/rag/test_rag.py::test_full_rag_with_ollama -v
```

You can also test the API using curl and the provided document examples:

```bash
curl -X POST "http://localhost:8080/api/sources" \
  -F "files=@backend/tests/assets/file1.md"
```

```bash
curl -N -X POST "http://localhost:8080/api/research" \
  -H "Content-Type: application/json" \
  -d '{"request": "What is the role of the hippocampus and neocortex in memory formation?"}'
```



## Development Notes

Right now, the database is only initialised on the first run, so you can only choose the model and vector_size at the beginning. You cannot add embeddings using another model. Vector size must match the embedding model (1536 for OpenAI, 4096 for some Ollama models).

LLM responses return structured JSON with question/answer/sources. 

Search uses L2 distance (`<->` in psql).

## What else I would have done given more time

The scope of this task exceeded the suggested hours, so I prioritised building a first end-to-end pipeline scaffold.

What I’d change:

- I would have spent more time testing frontend <-> backend integration in a containerised environment, but I hit some frontend errors that I decided not to dive deep into.
- I would have added external sources usage, of course.
- DB connections should be optimised. Right now, I stopped at a simple connection per chunk, but to make this solution production-ready, I would spend time on proper connection pooling.
- Embedding and chunk processing can also be parallelised. For instance, my first step would have been to add batch processing of incoming documents.
- I would have stored more data on each document and question. Metadata can provide proper source references for each answer the agent returns.
- Agentic usage could also have gone beyond simple embedding, vector search, and answer generation.
- The current solution doesn’t store which model was used for embedding answers. Answers themselves are worth saving.
- I would have added response evaluation based on the model used, prompt version, and other metadata, depending on what would have been done at this point.
- The Golden Set of research requests, with and without related documents, would have been an essential addition to this pipeline.
- Not everything in this solution was fully tested. I can think of many scenarios where something crashes or doesn’t work as expected, so test coverage should have improved, and the implementation should have changed.

## AI disclosure

Where AI wasn't used: 

- Architecture and design
- Writing the code
- Setting up the infrastructure
- Solving the task
- Making decisions

Where it was used (as a part of how I am thinking and being efficient):

- Planning and prioritising tasks (I have my own time and task management system that utilises an agent)
- For my own research of existing solutions, primarily to save time, I used AI as an advanced search engine, which helped me to summarise key points about certain embedding models available for me to test within this solution (I chose the best and most appropriate tools myself based on the information I’ve gathered, including the information I found using simple search engines)
- Generating api/research requests to test the app
- I used AI to review what I’ve managed to finish, update my tasks, and see what gaps I left at the very end of implementation. 
- Used Grammarly to polish the README since English isn't my first language, and I’ve relied on it for years.
- Used an agent to generate the project’s structure for the README.

