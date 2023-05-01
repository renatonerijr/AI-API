import openai
import re
from decouple import config

from fastapi import FastAPI
from fastapi.param_functions import Depends
from pydantic import BaseModel, validator

from src.config.db import get_session
from src.prompts.safety_prompt import SAFETY_PROMPT

from sqlmodel import select
from better_profanity import profanity

profanity.load_censor_words()

app = FastAPI()

openai.api_key = config("OPENAI_API_KEY")

class UserInput(BaseModel):
    input: str

    @validator('input')
    def cleanup_input(cls, v):
        res = re.sub('[,*)="/|\@#%(&$_:^]', '', v)
        return profanity.censor(res)


# @app.post("/input-cleanup")
# async def input_cleanup(
#     user_input: UserInput,
#     session=Depends(get_session)
# ):
#     safety_prompt = SAFETY_PROMPT.replace('<<INPUT>>', user_input.input)
#     response = openai.Completion.create(model="text-davinci-003", prompt=safety_prompt, temperature=0, max_tokens=300)
#     return response

async def complete_prompt(
    user_input: UserInput,
    session=Depends(get_session)
):
    response = openai.Completion.create(model="text-davinci-003", prompt=user_input.input, temperature=0, max_tokens=300)
    return response