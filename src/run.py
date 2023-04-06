import uvicorn
from executor.env import UVICORN_RELOAD, UVICORN_BIND_ADDR, UVICORN_BIND_PORT


uvicorn.run(
    "executor:app",
    reload=UVICORN_RELOAD,
    host=UVICORN_BIND_ADDR,
    port=UVICORN_BIND_PORT,
)
