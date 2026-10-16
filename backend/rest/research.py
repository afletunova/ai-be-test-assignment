from fastapi import APIRouter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = APIRouter()


@app.post("/research")
async def research(request: str):
    logger.info(f"Research request: {request}")
    return {"message": f"Research request: {request}"}
