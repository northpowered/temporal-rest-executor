import pytest
from .worker import (
    Worker,
    Client,
    test_activities,
    test_workflows,
    MOCK_QUEUE_NAME
)
from executor.temporal import (
    WorkflowExecutionInput,
    ActivityExecutionInput,
    ExecutionResult,
)
from executor.endpoints import activity_execution, workflow_execution


@pytest.mark.asyncio
async def test_a_endpoint(t_client: Client):
    async with Worker(
        t_client,
        task_queue=MOCK_QUEUE_NAME,
        workflows=test_workflows,
        activities=test_activities,
    ):
        payload: ActivityExecutionInput = ActivityExecutionInput(
            activity_name="dataclass_arg_activity",
            activity_task_queue=MOCK_QUEUE_NAME,
            args={"str_1": "q", "str_2": "w"},
            start_to_close_timeout=10,
            parent_workflow_id="pytest-parent-workflow",
            execution_timeout=4,
        )
        resp: ExecutionResult = await activity_execution(
            client=t_client, payload=payload
        )
        assert resp.success, resp
        assert resp.data == "qw"


@pytest.mark.asyncio
async def test_a_endpoint_rand_id(t_client: Client):
    async with Worker(
        t_client,
        task_queue=MOCK_QUEUE_NAME,
        workflows=test_workflows,
        activities=test_activities,
    ):
        payload: ActivityExecutionInput = ActivityExecutionInput(
            activity_name="dataclass_arg_activity",
            activity_task_queue=MOCK_QUEUE_NAME,
            args={"str_1": "q", "str_2": "w"},
            start_to_close_timeout=10,
            parent_workflow_id=None,
            execution_timeout=4,
        )
        resp: ExecutionResult = await activity_execution(
            client=t_client, payload=payload
        )
        assert resp.success, resp
        assert resp.data == "qw"


@pytest.mark.asyncio
async def test_w_endpoint(t_client: Client):
    async with Worker(
        t_client,
        task_queue=MOCK_QUEUE_NAME,
        workflows=test_workflows,
        activities=test_activities,
    ):
        payload: WorkflowExecutionInput = WorkflowExecutionInput(
            workflow_name="DataclassArgWorkflow",
            workflow_task_queue=MOCK_QUEUE_NAME,
            args={"str_1": "q", "str_2": "w"},
            workflow_id="pytest-single-workflow",
        )
        resp: ExecutionResult = await workflow_execution(
            client=t_client, payload=payload
        )
        assert resp.success, resp
        assert resp.data == "qw"


@pytest.mark.asyncio
async def test_w_endpoint_rand_id(t_client: Client):
    async with Worker(
        t_client,
        task_queue=MOCK_QUEUE_NAME,
        workflows=test_workflows,
        activities=test_activities,
    ):
        payload: WorkflowExecutionInput = WorkflowExecutionInput(
            workflow_name="DataclassArgWorkflow",
            workflow_task_queue=MOCK_QUEUE_NAME,
            args={"str_1": "q", "str_2": "w"},
            workflow_id=None,
        )
        resp: ExecutionResult = await workflow_execution(
            client=t_client, payload=payload
        )
        assert resp.success, resp
        assert resp.data == "qw"
