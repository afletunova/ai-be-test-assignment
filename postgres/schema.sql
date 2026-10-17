CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE text_chunks (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    content text NOT NULL,
    embedding vector(${VECTOR_SIZE})
);