from temporalio.client import Client, WorkflowFailureError
from temporalio import workflow
from temporalio.worker import Worker
from .schemas import (
    ActivityExecutionInput,
    ExecutionResult,
    WorkflowExecutionInput,
    InternalOutput,
)
from .env import (
    TEMPORAL_ENDPOINT,
    TEMPORAL_NAMESPACE,
    TEMPORAL_INTERNAL_FLOW_NAME,
    TEMPORAL_INTERNAL_TASK_QUEUE,
)
from datetime import timedelta
from uuid import uuid4
import opentelemetry.context
from temporalio.contrib.opentelemetry import TracingInterceptor
from .telemetry import runtime
from .common import schedule_timeout_from_request


async def temporal_client():  # pragma: no cover

    opentelemetry.context.get_current()

    return await Client.connect(
        TEMPORAL_ENDPOINT,
        namespace=TEMPORAL_NAMESPACE,
        interceptors=[TracingInterceptor()],
        runtime=runtime,
    )


@workflow.defn(name=TEMPORAL_INTERNAL_FLOW_NAME, sandboxed=False)
class InternalExecutionWorkflow:
    @workflow.run
    async def run(self, payload: ActivityExecutionInput) -> InternalOutput:
        response: InternalOutput = InternalOutput()
        try:
            if payload.args is None:
                result = await workflow.execute_activity(
                    activity=payload.activity_name,
                    task_queue=payload.activity_task_queue,
                    start_to_close_timeout=schedule_timeout_from_request(
                        payload.start_to_close_timeout
                    ),
                    schedule_to_start_timeout=schedule_timeout_from_request(
                        payload.schedule_to_start_timeout
                    ),
                    heartbeat_timeout=schedule_timeout_from_request(
                        payload.heartbeat_timeout
                    ),
                    schedule_to_close_timeout=schedule_timeout_from_request(
                        payload.schedule_to_close_timeout
                    ),
                    retry_policy=payload.get_policy(),
                )
            else:
                args = payload.args

                if not isinstance(args, list):
                    args = [args]

                result = await workflow.execute_activity(
                    activity=payload.activity_name,
                    task_queue=payload.activity_task_queue,
                    start_to_close_timeout=schedule_timeout_from_request(
                        payload.start_to_close_timeout
                    ),
                    schedule_to_start_timeout=schedule_timeout_from_request(
                        payload.schedule_to_start_timeout
                    ),
                    heartbeat_timeout=schedule_timeout_from_request(
                        payload.heartbeat_timeout
                    ),
                    schedule_to_close_timeout=schedule_timeout_from_request(
                        payload.schedule_to_close_timeout
                    ),
                    retry_policy=payload.get_policy(),
                    args=args,
                )
        except Exception as ex:
            response.success = False
            response.data = str(ex)
        else:
            response.data = result
        return response


async def internal_workflow_execution(
    client: Client, payload: ActivityExecutionInput
) -> ExecutionResult:
    async with Worker(
        client,
        task_queue=TEMPORAL_INTERNAL_TASK_QUEUE,
        workflows=[InternalExecutionWorkflow],
    ):
        print(type(payload))
        print(payload)
        response: ExecutionResult = ExecutionResult(execution_init=payload)
        print(response)
        if payload.parent_workflow_id is None:
            workflow_id: str = str(uuid4())
        else:
            workflow_id: str = payload.parent_workflow_id

        response.execution_id = workflow_id

        try:
            result: InternalOutput = await client.execute_workflow(
                InternalExecutionWorkflow.run,
                payload,
                id=workflow_id,
                task_queue=TEMPORAL_INTERNAL_TASK_QUEUE,
                execution_timeout=schedule_timeout_from_request(
                    payload.parent_workflow_execution_timeout
                ),
                run_timeout=schedule_timeout_from_request(
                    payload.parent_workflow_execution_timeout
                ),
                task_timeout=schedule_timeout_from_request(
                    payload.parent_workflow_execution_timeout
                ),
            )
            assert result.success, result.data
            response.data = result.data
        except WorkflowFailureError as ex:
            response.success = False
            response.error = str(ex.cause)
        except AssertionError as ex:
            response.success = False
            response.error = str(ex)

        return response


async def external_workflow_execution(
    client: Client, payload: WorkflowExecutionInput
) -> ExecutionResult:
    response: ExecutionResult = ExecutionResult(execution_init=payload)

    if payload.workflow_id is None:
        workflow_id: str = str(uuid4())
    else:
        workflow_id: str = payload.workflow_id

    response.execution_id = workflow_id

    try:
        if payload.args is None:
            result = await client.execute_workflow(
                workflow=payload.workflow_name,
                task_queue=payload.workflow_task_queue,
                id=workflow_id,
                execution_timeout=timedelta(seconds=payload.execution_timeout)
            )
        else:
            result = await client.execute_workflow(
                payload.workflow_name,
                payload.args,
                task_queue=payload.workflow_task_queue,
                id=workflow_id,
                execution_timeout=timedelta(seconds=payload.execution_timeout)
            )
        response.data = result
    except WorkflowFailureError as ex:
        response.success = False
        response.error = str(ex.cause)
    return response
