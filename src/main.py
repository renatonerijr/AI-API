from fastapi import FastAPI
from fastapi.param_functions import Depends
from pydantic import BaseModel, validator
from src.config.db import get_session
from sqlmodel import select
from better_profanity import profanity

profanity.load_censor_words()

app = FastAPI()

class UserInput(BaseModel):
    input: str

    @validator('input')
    def cleanup_input(cls, v):
        return profanity.censor(v)

@app.post("/input-cleanup")
async def input_cleanup(
    user_input: UserInput,
    session=Depends(get_session)
):
    return user_input