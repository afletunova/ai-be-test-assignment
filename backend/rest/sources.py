from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

from ..rag import chunk_and_process, get_llm_client

import os
import logging
import traceback

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

    try:
        mode = os.environ.get("MODE") or "ollama"
        client = get_llm_client(mode)
    except Exception as e:
        logger.error(f"Failed to initialize LLM client: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500, detail=f"LLM client initialization failed: {str(e)}"
        )

    try:
        for file in files:
            logger.info(f"Processing file: {file.filename}")
            file_content = await file.read()
            file_text = file_content.decode("utf-8")

            uploaded.append(
                UploadedFile(
                    name=file.filename or "",
                    size=len(file_content),
                    type=file.content_type or "application/octet-stream",
                )
            )
            # TODO: decide if there's a need to store the doc
            logger.info(f"Calling chunk_and_process for {file.filename}")
            chunk_and_process(client, file_text)
            logger.info(f"Successfully processed {file.filename}")
    except Exception as e:
        logger.error(f"Failed to process file {file.filename}: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500, detail=f"Failed to process {file.filename}: {str(e)}"
        )

    logger.info(f"Uploaded {len(uploaded)} files")
    return UploadResult(uploaded=uploaded)
