from fastapi import APIRouter, UploadFile, File

from collections.abc import AsyncIterable

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = APIRouter()


@app.post("/sources", status_code=200)
async def add_files(files: list[UploadFile] = File(...)) -> AsyncIterable[str]:

    for file in files:
        logger.info(f"Processing file: {file.filename}")
        file_content = await file.read()

    logging.info(f"Uploaded {len(files)} files")

    message = f"Added {len(files)} files"

    for line in message.splitlines():
        yield line
