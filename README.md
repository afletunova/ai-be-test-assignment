# AI Engineer Technical Test. Backend API --- Research Agent.

This repository exists to showcase the research agent I created with a purpose of being tested for an AI Engineer position. 

## Overview

This backend module is suppose to:

- Receive rest requests from the provided frontend
- Stream responses back to the provided frontend
- Embed uploaded source files & query at the correct times
- Build an LLM research agent that acts on the user’s research request
- The agent should be able to utilise external sources

At this moment, it does everything from the list above except for answer generation and utilising external sources. Also, it's compatibility with provided Frontend is not fully tested yet.

## Architecture

To cover API side I chose FastAPI as an efficient framework to work with Python. Also, automatic documentation covers a part of the assignment. 

RAG pipeline itself at this moment consist of chunking, embedding, vector storage and vector search. Chunking is done using LangChain RecursiveCharacterTextSplitter, since it splits the text chunks into small enough chunks recursively for this prototype of a RAG. It gors well with the solution too.

I also implemented LLM client abstraction, allowing to choose between Ollama or OpenAI models. Currently I've been testing this solution primarily on Ollama, in order to save on OpenAI tokens.

For the database I chose PostgreSQL with pgvector extension since I am familiar with both and it's a good combination to use for this prototype. 

## Prerequisites

- Docker & Docker Compose
- Pythin 3.13+
- PostrgeSQL with pgvector (presented here via official Docker image)
- Ollama server (I spinned up my own on Flask) or OpenAI API key



## Environmental Variables

Most of them are optional, however to test this pipeline, it is better to either fill Ollama's remote host var, or to use OpenAI API key.

## Installation & Setup

I recommend using Docker.

1. Clone repository

```bash
git clone https://github.com/afletunova/ai-be-test-assignment.git
```

1. Set up '.env' file

```bash
cd ai-be-test-assignment.git
cp .env.example .env
```

And fill missing variables with your own credentials

1. (Optional) Run docker compose

```bash
docker compose up
```

This step should create two containers: 

- one with the backend itself 
- and the second with pg database

or you can proceed without Docker

### Local Development

1. Install dependencies

```bash
pip install -r requirements.txt
```

1. Run the backend locally with your own PostgreSQL DB

```bash
fastapi run main.py --port 8080
```



## API Endpoints

1. `POST /api/research`
  - Summary: Research endpoint, expecting the research request as an input, and streaming the answer back. 
  - Request Body:
    - Content-Type: `application/json`
    - Schema:
    ```json
    {
        "request": "string"
    }
    ```
    - Responses: 
      - `200 OK` --- Successful response
      - `422 Unprocessable Entity` --- Validation error, returns details about the validation issues.
2. `POST /api/sources`
  - Summary: Upload files into the backend and process them
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
    - `200 OK` --- Successful upload response. Output reference: UploadResult. Contains an array of uploaded files with properties:
      - `name` (string)
      - `size` (integer)
      - `type` (string)
    - `422 Unprocessable Entity` --- Validation error, returns details about the validation issues.



## Project Structure

## Key Features

## Testing

## Error Handling

## Development Notes

## AI disclosure



