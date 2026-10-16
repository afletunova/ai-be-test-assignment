from fastapi import FastAPI, File, UploadFile
import logging
from .rest.research import app as research_app
from .rest.sources import app as sources_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(research_app, prefix="/api")
app.include_router(sources_app, prefix="/api")


@app.get("/")
def read_root():
    return {"Test": "Test"}
