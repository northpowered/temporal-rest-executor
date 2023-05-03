# Getting started

[![codecov](https://codecov.io/github/northpowered/temporal-rest-executor/branch/main/graph/badge.svg?token=0Ei4nXXFfL)](https://codecov.io/github/northpowered/temporal-rest-executor)
[![CI](https://github.com/northpowered/temporal-rest-executor/actions/workflows/ci.yml/badge.svg)](https://github.com/northpowered/temporal-rest-executor/actions/workflows/ci.yml)
[![Docker Image CD](https://github.com/northpowered/temporal-rest-executor/actions/workflows/docker-image.yml/badge.svg)](https://github.com/northpowered/temporal-rest-executor/actions/workflows/docker-image.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=northpowered_temporal-rest-executor&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=northpowered_temporal-rest-executor)


## What is it?

This is a simple tool to operate with [Temporal](https://temporal.io/) workflows/activities through the REST endpoints.

Service provides some REST endpoints which can execute (now) any workflow or activity, registered is the namespace.

Based on [FastAPI](https://github.com/tiangolo/fastapi) and may be useful for development and QA.

## Quick start

### Docker

Run the docker image
```bash
docker run -p 8000:8000 ghcr.io/northpowered/temporal-rest-executor:latest
```

You can add Temporal endpoint as an env var. All env vars`ll be listed below.

```bash
docker run -e TEMPORAL_ENDPOINT=temporal:7233 -p 8000:8000 ghcr.io/northpowered/temporal-rest-executor:latest
```

And specify docker network (this is the example for [default Temporal docker-compose manifest](https://github.com/temporalio/docker-compose/blob/main/docker-compose.yml))
```bash
docker run -e TEMPORAL_ENDPOINT=temporal:7233 -p 8000:8000 --network temporal-network ghcr.io/northpowered/temporal-rest-executor:latest
```

### Manual start

Use it for development or debugging

```bash
git clone git@github.com:northpowered/temporal-rest-executor.git

poetry install

python3 src/run.py
```

## Configuration

### TEMPORAL_ENDPOINT

Temporal endpoint string

`TEMPORAL_ENDPOINT=localhost:7233`

### TEMPORAL_NAMESPACE

Temporal namespace string

Will be deprecated soon, moved to the REST args

`TEMPORAL_NAMESPACE=default`

### TEMPORAL_INTERNAL_FLOW_NAME

Name of the workflow for execution remote activities

`TEMPORAL_INTERNAL_FLOW_NAME=InternalExecutionWorkflow`

### TEMPORAL_INTERNAL_TASK_QUEUE

Task queue for internal workflow

`TEMPORAL_INTERNAL_TASK_QUEUE=internal-execution-queue`

### UVICORN_BIND_ADDR

Address for uvicorn HTTP server

`UVICORN_BIND_ADDR=0.0.0.0`

### UVICORN_BIND_PORT

Port for uvicorn HTTP server

`UVICORN_BIND_PORT=8000`

### TELEMETRY_ENABLED

Flag to enable OTEL collection

`TELEMETRY_ENABLED=True`

### TELEMETRY_AGENT_HOST

OTEL collector address

`TELEMETRY_AGENT_HOST=localhost`

### TELEMETRY_AGENT_PORT

OTEL collector port

`TELEMETRY_AGENT_PORT=6831`

### PROMETHEUS_ENDPOINT_ENABLED

Flag to enable Prometheus endpoint

`PROMETHEUS_ENDPOINT_ENABLED=True`

### PROMETHEUS_ENDPOINT_PORT

Prometheus endpoint port to bind on

`PROMETHEUS_ENDPOINT_PORT=9000`