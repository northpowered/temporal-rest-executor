from fastapi import FastAPI
from .env import (
    TEMPORAL_INTERNAL_TASK_QUEUE,
    TEMPORAL_ENDPOINT,
    TEMPORAL_INTERNAL_FLOW_NAME,
    TEMPORAL_NAMESPACE,
    SERVICE_NAME,
    TELEMETRY_ENABLED,
    TELEMETRY_AGENT_HOST,
    TELEMETRY_AGENT_PORT,
    PROMETHEUS_ENDPOINT_ENABLED,
    PROMETHEUS_ENDPOINT_PORT
)
from contextlib import asynccontextmanager
from .router import (
    workflow_router,
    activity_router
)
from rich.console import Console


__title__: str = SERVICE_NAME
__version__: str = "0.3.0"


console = Console()


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover
    tracing_str: str = "[red bold]disabled[/ red bold]"

    if TELEMETRY_ENABLED:
        tracing_str = f"[blue bold]enabled[/ blue bold] on [blue bold]{TELEMETRY_AGENT_HOST}:{TELEMETRY_AGENT_PORT}[/ blue bold]"

    prometheus_str: str = "[red bold]disabled[/ red bold]"

    if PROMETHEUS_ENDPOINT_ENABLED:
        prometheus_str = f"[blue bold]enabled[/ blue bold] on [blue bold]127.0.0.1:{PROMETHEUS_ENDPOINT_PORT}[/ blue bold]"

    console.print(f"""
    {__title__}:{__version__} loaded for this Temporal instance:
    Temporal endpoint = [blue bold]{TEMPORAL_ENDPOINT}[/ blue bold]
    Temporal namespace = [blue bold]{TEMPORAL_NAMESPACE}[/ blue bold]

    Internal Executor workflow name is = [blue bold]{TEMPORAL_INTERNAL_FLOW_NAME}[/ blue bold]
    And will be registred in = [blue bold]{TEMPORAL_INTERNAL_TASK_QUEUE}[/ blue bold] queue

    OTEL tracing {tracing_str}
    Prometheus endpoint {prometheus_str}

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


app.include_router(workflow_router)
app.include_router(activity_router)
