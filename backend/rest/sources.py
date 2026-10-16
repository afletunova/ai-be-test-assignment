from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

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

    logger.info(f"Uploaded {len(uploaded)} files")
    return UploadResult(uploaded=uploaded)
