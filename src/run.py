import uvicorn
from .env import UVICORN_RELOAD, UVICORN_BIND_ADDR, UVICORN_BIND_PORT


uvicorn.run(
    "main:app",
    reload=UVICORN_RELOAD,
    host=UVICORN_BIND_ADDR,
    port=UVICORN_BIND_PORT,
)
