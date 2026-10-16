from fastapi import APIRouter, UploadFile, File
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = APIRouter()


@app.post("/sources")
async def add_files(files: list[UploadFile] = File(...)):
    for file in files:
        logger.info(f"Processing file: {file.filename}")
        file_content = await file.read()

    return {"message": f"Added {len(files)} files"}
