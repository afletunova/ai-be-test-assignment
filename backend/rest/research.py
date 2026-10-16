from fastapi import APIRouter
import logging

from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = APIRouter()

class ResearchRequest(BaseModel):
    request: str

class ResearchResponse(BaseModel):
    message: str


@app.post("/research", response_model=ResearchResponse, status_code=200)
async def research(request: ResearchRequest):
    logger.info(f"Research request: {request.request}")
    return ResearchResponse(message=f"Research request: {request.request}")
