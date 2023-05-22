import openai
import re
from decouple import config

from fastapi import FastAPI
from fastapi.param_functions import Depends
from pydantic import BaseModel, validator

from src.config.db import get_session
from src.vector_db import client
from src.prompts.safety_prompt import SAFETY_PROMPT

from sqlmodel import select
from better_profanity import profanity
from qdrant_client.http.models import PointStruct
from qdrant_client.http import models

profanity.load_censor_words()

app = FastAPI()

openai.api_key = config("OPENAI_API_KEY")


class UserInput(BaseModel):
    input: str


@app.post("/complete_prompt")
async def complete_prompt(
    user_input: UserInput,
    session=Depends(get_session)
):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=user_input.input,
        temperature=0.8,
        max_tokens=300
    )

    return response


@app.post("/complete_chat")
async def complete_chat_prompt(
    user_input: UserInput,
    session=Depends(get_session)
):

    response = openai.Embedding.create(
        input=user_input.input,
        model="text-embedding-ada-002"
    )

    input_embedding = response['data'][0]['embedding']

    operation_info = client.search(
        collection_name="test_collection",
        search_params=models.SearchParams(
            hnsw_ef=128,
            exact=False
        ),
        query_vector=input_embedding,
        limit=150,
    )
    prompt = ""
    if operation_info:
        prompt += "Here are some context from previous messages:"
        for op in operation_info:
            prompt += f"{op.payload['role'].upper()}: {op.payload['message']}"

    prompt += f"USER: {user_input.input}"
    prompt = prompt.replace('\n', '')
    print(prompt)
    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=500
    )

    operation_info = client.upsert(
        collection_name="test_collection",
        wait=True,
        points=[
            PointStruct(id=1, vector=input_embedding, payload={"role": "user", "message": user_input.input}),
            PointStruct(id=2, vector=input_embedding, payload={"role": "assistant", "message": completion['choices'][0].text}),
        ]
    )

    return completion
