from fastapi import FastAPI
from .env import (
    TEMPORAL_INTERNAL_TASK_QUEUE,
    TEMPORAL_ENDPOINT,
    TEMPORAL_INTERNAL_FLOW_NAME,
    TEMPORAL_NAMESPACE
)
from contextlib import asynccontextmanager
from .router import execution_router
from rich.console import Console


__title__: str = "Temporal REST executor"
__version__: str = "0.1.0"


console = Console()


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover
    console.print(f"""
    {__title__}:{__version__} loaded for this Temporal instance:
    Temporal endpoint = [blue bold]{TEMPORAL_ENDPOINT}[/ blue bold]
    Temporal namespace = [blue bold]{TEMPORAL_NAMESPACE}[/ blue bold]

    Internal Executor workflow name is = [blue bold]{TEMPORAL_INTERNAL_FLOW_NAME}[/ blue bold]
    And will be registred in = [blue bold]{TEMPORAL_INTERNAL_TASK_QUEUE}[/ blue bold] queue

    https://github.com/northpowered/temporal-rest-executor

    Created with [red]:heart:[/ red] and by [blue bold]northpowered[/ blue bold]
    """)  # noqa: E501 W293
    yield


app = FastAPI(
    title=__title__,
    description="",
    version=__version__,
    redoc_url=None,
    docs_url="/doc",
    lifespan=lifespan
)


app.include_router(execution_router)
