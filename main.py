import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

from query_service import QueryService

load_dotenv()

allowed_origins = [
    "http://localhost:3000",
]

query_service = QueryService()


def init_logging():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_logging()

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/query/")
async def query(address: str, dietary_restrictions: str):
    return EventSourceResponse(query_service.query(address=address, dietary_restrictions=dietary_restrictions))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
