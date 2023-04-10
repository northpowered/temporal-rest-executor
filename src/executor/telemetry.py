
from temporalio.runtime import Runtime, TelemetryConfig, PrometheusConfig
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry import trace
from .env import (
    TELEMETRY_AGENT_HOST,
    TELEMETRY_AGENT_PORT,
    SERVICE_NAME as SN,
    PROMETHEUS_ENDPOINT_PORT,
    TELEMETRY_ENABLED,
    PROMETHEUS_ENDPOINT_ENABLED
)


def init_runtime_with_telemetry() -> Runtime:

    # Setup global tracer for workflow traces
    if TELEMETRY_ENABLED:
        provider = TracerProvider(resource=Resource.create({SERVICE_NAME: SN}))
        provider.add_span_processor(
            BatchSpanProcessor(
                JaegerExporter(
                    agent_host_name=TELEMETRY_AGENT_HOST,
                    agent_port=int(TELEMETRY_AGENT_PORT),
                )
            )
        )
        trace.set_tracer_provider(provider)

    # Metrics setup
    metrics_config: PrometheusConfig | None = None
    if PROMETHEUS_ENDPOINT_ENABLED:
        metrics_config = PrometheusConfig(
            bind_address=f"127.0.0.1:{PROMETHEUS_ENDPOINT_PORT}"
        )

    return Runtime(telemetry=TelemetryConfig(
        metrics=metrics_config
        )
    )


runtime = init_runtime_with_telemetry()
