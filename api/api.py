from parsers.flibusta import get_books
from parsers.stepik import get_courses
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/{content_type}/search")
def read_item(content_type: str, query: Optional[str] = None):
    if query != None:
        if content_type == 'courses':
            return get_courses(query)
        elif content_type == 'books':
            return get_books(query)