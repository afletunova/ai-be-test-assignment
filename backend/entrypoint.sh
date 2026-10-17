#!/bin/bash

MODE=${MODE:-"ollama"}

if [ "$MODE" = "ollama" ]; then
    echo "Running with Ollama..."
elif [ "$MODE" = "openapi" ]; then
    echo "Running with OpenAPI..."
else
    echo "Unknown MODE: $MODE"
    exit 1
fi

exec "$@"