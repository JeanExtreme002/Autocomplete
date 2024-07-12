from fastapi import APIRouter, status
from pydantic import BaseModel, Field, constr
from typing import List

from src.controllers import Controller


class Term(BaseModel):
    term: constr(min_length=4, max_length=500) = Field(
        ..., description="Term to be entered into the search engine"
    )


router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
def index():
    return {"status": "alive"}

@router.get("/{text}", response_model=List[str], status_code=status.HTTP_200_OK)
def get_terms(text: str):
    return Controller.get_terms(text)

@router.post("/feed", status_code=status.HTTP_201_CREATED)
def create_term(term: Term):
    Controller.create_term(term.term)
