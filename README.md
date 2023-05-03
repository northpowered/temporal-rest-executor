# Temporal-REST-executor

[![codecov](https://codecov.io/github/northpowered/temporal-rest-executor/branch/main/graph/badge.svg?token=0Ei4nXXFfL)](https://codecov.io/github/northpowered/temporal-rest-executor)
[![CI](https://github.com/northpowered/temporal-rest-executor/actions/workflows/ci.yml/badge.svg)](https://github.com/northpowered/temporal-rest-executor/actions/workflows/ci.yml)
[![Docker Image CD](https://github.com/northpowered/temporal-rest-executor/actions/workflows/docker-image.yml/badge.svg)](https://github.com/northpowered/temporal-rest-executor/actions/workflows/docker-image.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=northpowered_temporal-rest-executor&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=northpowered_temporal-rest-executor)

This is a simple tool to execute [Temporal](https://temporal.io/) workflows/activities through the REST endpoints

Service provides some REST endpoints which can execute any workflow or activity, registered is the namespace (You can set it)

Based on [FastAPI](https://github.com/tiangolo/fastapi) and may be useful for development and QA

Args for endpoints:

**Activity execution**

```
activity_name - [string] - REQUIRED
activity_task_queue - [string] - REQUIRED
args - [ANY] - may be null
start_to_close_timeout - [int] - Default is 10
schedule_to_start_timeout - [int] - may be null
heartbeat_timeout - [int] - may be null
schedule_to_close_timeout - [int] - may be null
retry_policy - [Object] - may be null
parent_workflow_id - [string] - If null, UUID4 will be used
parent_workflow_execution_timeout - [int] - Default is 10
parent_workflow_run_timeout - [int] - may be null
parent_workflow_task_timeout - [int] - may be null

# RetryPolicy object

initial_interval - [int] - Default is 1
backoff_coefficient - [float] - Default is 2
maximum_interval - [int] - may be null
maximum_attempts - [int] - Default is 0
```


**Workflow execution**
```
workflow_name - [string] - REQUIRED
workflow_task_queue - [string] - REQUIRED
args - [ANY] - may be null
execution_timeout - [int] - Default is 10
workflow_id- [string] - If null, UUID4 will be used
```
### Run

Simply run docker image
```bash
docker run -p 8000:8000 ghcr.io/northpowered/temporal-rest-executor:latest
```

You can add Temporal endpoint as an env var
```bash
docker run -e TEMPORAL_ENDPOINT=temporal:7233 -p 8000:8000 ghcr.io/northpowered/temporal-rest-executor:latest
```

And specify docker network (this is the example for default Temporal compose manifest)
```bash
docker run -e TEMPORAL_ENDPOINT=temporal:7233 -p 8000:8000 --network temporal-network ghcr.io/northpowered/temporal-rest-executor:latest
```

## Config

Some env vars:

**TEMPORAL_ENDPOINT = localhost:7233**

**TEMPORAL_NAMESPACE = default**

**TEMPORAL_INTERNAL_FLOW_NAME = InternalExecutionWorkflow**

**TEMPORAL_INTERNAL_TASK_QUEUE = internal-execution-queue**

**UVICORN_BIND_ADDR = 0.0.0.0**

**UVICORN_BIND_PORT = 8000**

**TELEMETRY_ENABLED = True**

**TELEMETRY_AGENT_HOST = localhost**

**TELEMETRY_AGENT_PORT = 6831**

**PROMETHEUS_ENDPOINT_ENABLED = True**

**PROMETHEUS_ENDPOINT_PORT = 9000**

## Use

Default FastAPI Swagger is available

or You can use curl:

> Activity execution
```bash
curl -X 'POST' \
  'http://localhost:8000/v1/execution/activity' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "activity_name": "my_activity",
  "activity_task_queue": "my_queue",
  "args": ["ANY", "PARAMS"],
  "start_to_close_timeout": 10,
  "execution_timeout": 10,
  "parent_workflow_id": "MyQAWorkflow"
}'
```

> Workflow execution
```bash
curl -X 'POST' \
  'http://localhost:8000/v1/execution/workflow' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "workflow_name": "MyWorkflow",
  "workflow_task_queue": "my_queue",
  "args": "some args",
  "workflow_id": "my_id",
  "execution_timeout": 3
}'
```

