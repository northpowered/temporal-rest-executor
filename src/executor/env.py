from os import getenv

SERVICE_NAME: str = getenv("SERVICE_NAME", "Temporal REST executor")

UVICORN_RELOAD: bool = getenv("UVICORN_RELOAD", False)

UVICORN_BIND_ADDR: str = getenv("UVICORN_BIND_ADDR", "0.0.0.0")

UVICORN_BIND_PORT: int = getenv("UVICORN_BIND_PORT", 8000)

TEMPORAL_ENDPOINT: str = getenv("TEMPORAL_ENDPOINT", "localhost:7233")

TEMPORAL_NAMESPACE: str = getenv("TEMPORAL_NAMESPACE", "default")

TEMPORAL_INTERNAL_FLOW_NAME: str = getenv(
    "TEMPORAL_INTERNAL_FLOW_NAME", "InternalExecutionWorkflow"
)

TEMPORAL_INTERNAL_TASK_QUEUE: str = getenv(
    "TEMPORAL_INTERNAL_TASK_QUEUE", "internal-execution-queue"
)

TELEMETRY_ENABLED: bool = getenv(
    "TELEMETRY_ENABLED", True
)

TELEMETRY_AGENT_HOST: str = getenv(
    "TELEMETRY_AGENT_HOST", "localhost"
)

TELEMETRY_AGENT_PORT: str = getenv(
    "TELEMETRY_AGENT_PORT", "6831"
)

PROMETHEUS_ENDPOINT_ENABLED: bool = getenv(
    "PROMETHEUS_ENDPOINT_ENABLED", True
)

PROMETHEUS_ENDPOINT_PORT: str = getenv(
    "PROMETHEUS_ENDPOINT_PORT", "9000"
)
