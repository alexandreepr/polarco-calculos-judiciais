from pydantic import BaseModel

class WordsCounterRequest(BaseModel):
    words_string: str

class WordsCounterResponse(BaseModel):
    words_count: int
