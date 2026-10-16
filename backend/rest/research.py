from fastapi import APIRouter
from collections.abc import AsyncIterable
from pydantic import BaseModel

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = APIRouter()


class ResearchRequest(BaseModel):
    request: str


class ResearchResponse(BaseModel):
    message: str


@app.post("/research", response_model=ResearchResponse, status_code=200)
async def research(request: ResearchRequest) -> AsyncIterable[str]:
    logger.info(f"Research request: {request.request}")
    response = ResearchResponse(message=f"Research request: {request.request}")

    for line in response.message.splitlines():
        yield line
