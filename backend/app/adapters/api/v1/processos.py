from fastapi import APIRouter, HTTPException

from ...core.schemas import WordsCounterRequest, WordsCounterResponse
from ...core.logger import logger

router = APIRouter(tags=["words-counter"])


@router.post(
    "/processos",
    response_description="",
)
async def post_processos(request: WordsCounterRequest) -> WordsCounterResponse:
    """
    """
    # words_string = request.words_string.strip()

    # if not words_string:
    #     logger.error('POST /')
    #     raise HTTPException(
    #         status_code=422,
    #         detail="Input string is empty or contains only whitespace."
    #     )

    # words_count = len(words_string.split())

    # logger.info('POST /')

    return {"": ""}