from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from app.workflow import workflow


app = FastAPI()

class BookRequest(BaseModel):
    theme: str


class Page(BaseModel):
    page: int
    text: str
    image_prompt: str


class BookResponse(BaseModel):
    story: str
    pages: List[Page]


@app.post("/generate", response_model=BookResponse)
def generate(req: BookRequest):

    result = workflow.invoke({"theme": req.theme})

    return {
        "story": result["story"],
        "pages": result["pages"]
    }