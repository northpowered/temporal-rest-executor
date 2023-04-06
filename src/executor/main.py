from fastapi import FastAPI
from .router import execution_router

app = FastAPI(
    title="Temporal REST executor",
    description="",
    version="0.1.0",
    redoc_url=None,
    docs_url="/doc",
)

app.include_router(execution_router)
