from parsers.flibusta import get_books
from parsers.stepik import get_courses
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    title: str
    source: str
    link: str
    cover: Optional[str] = None
    description: Optional[str] = None

@app.get("/api/{content_type}/search", response_model=List[Item])
def read_item(content_type: str, query: Optional[str] = None):
    if query != None:
        if content_type == 'courses':
            return get_courses(query)
        elif content_type == 'books':
            return get_books(query)