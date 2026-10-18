from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from collections.abc import AsyncIterable
from pydantic import BaseModel

from ..rag import get_llm_client, research_and_answer

import os
import logging
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = APIRouter()


class ResearchRequest(BaseModel):
    request: str


@app.post("/research", status_code=200)
async def research(request: ResearchRequest):
    logger.info(f"Research request: {request.request}")

    try:
        mode = os.environ.get("MODE") or "ollama"
        client = get_llm_client(mode)
    except Exception as e:
        logger.error(f"Failed to initialize LLM client: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500, detail=f"LLM client initialization failed: {str(e)}"
        )

    async def event_generator() -> AsyncIterable[str]:
        try:
            for i, response in enumerate(
                research_and_answer(client, request.request), 1
            ):
                yield f"Research Response {i}\n\n"
                yield f"{response['answer']}\n\n"
            yield "\n"
        except Exception as e:
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=500, detail=f"Failed to process your request: {str(e)}"
            )

    return StreamingResponse(event_generator(), media_type="text/plain")
