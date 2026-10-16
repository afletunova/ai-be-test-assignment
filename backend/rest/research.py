from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from collections.abc import AsyncIterable
from pydantic import BaseModel

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = APIRouter()


class ResearchRequest(BaseModel):
    request: str


@app.post("/research", status_code=200)
async def research(request: ResearchRequest):
    async def event_generator() -> AsyncIterable[str]:
        logger.info(f"Research request: {request.request}")
        response = f"Research request: {request.request}"

        for line in response.splitlines():
            yield line + "\n"

    return StreamingResponse(event_generator(), media_type="text/plain")
