from fastapi import FastAPI, File, UploadFile
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Test": "Test"}


@app.post("/research")
async def research(request: str):
    logger.info(f"Research request: {request}")
    return {"message": f"Research request: {request}"}


@app.post("/sources")
async def add_files(files: list[UploadFile] = File(...)):
    for file in files:
        logger.info(f"Processing file: {file.filename}")
        file_content = await file.read()

    return {"message": f"Added {len(files)} files"}
