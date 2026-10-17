from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

from ..rag import chunk_and_process, get_llm_client
from ..rag.llm_client import llm_client, ollama_client, openai_client

import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = APIRouter()


class UploadedFile(BaseModel):
    name: str
    size: int
    type: str


class UploadResult(BaseModel):
    uploaded: list[UploadedFile]


@app.post("/sources", response_model=UploadResult, status_code=200)
async def add_files(files: list[UploadFile] = File(...)) -> UploadResult:
    uploaded: list[UploadedFile] = []

    mode = os.environ.get("MODE") or "ollama"
    client = get_llm_client(mode)

    for file in files:
        logger.info(f"Processing file: {file.filename}")
        file_content = await file.read()
        uploaded.append(
            UploadedFile(
                name=file.filename or "",
                size=len(file_content),
                type=file.content_type or "application/octet-stream",
            )
        )
        # TODO: decide if there's a need to store the doc
        chunk_and_process(client, file)

    logger.info(f"Uploaded {len(uploaded)} files")
    return UploadResult(uploaded=uploaded)
