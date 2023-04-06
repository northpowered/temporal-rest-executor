import pytest
from .worker import (
    Worker,
    Client,
    test_activities,
    test_workflows,
    MOCK_QUEUE_NAME
)
from executor.temporal import (
    internal_workflow_execution,
    ActivityExecutionInput,
    ExecutionResult,
)


@pytest.mark.asyncio
async def test_a_dataclass(t_client: Client):
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
        resp: ExecutionResult = await internal_workflow_execution(
            client=t_client, payload=payload
        )
        assert resp.success, resp
        assert resp.data == "qw"


@pytest.mark.asyncio
async def test_a_single_arg(t_client: Client):
    async with Worker(
        t_client,
        task_queue=MOCK_QUEUE_NAME,
        workflows=test_workflows,
        activities=test_activities,
    ):
        payload: ActivityExecutionInput = ActivityExecutionInput(
            activity_name="single_arg_activity",
            activity_task_queue=MOCK_QUEUE_NAME,
            args="spam",
            start_to_close_timeout=10,
            parent_workflow_id="pytest-parent-workflow",
            execution_timeout=4,
        )
        resp: ExecutionResult = await internal_workflow_execution(
            client=t_client, payload=payload
        )
        assert resp.success, resp
        assert resp.data == "spamspam"


@pytest.mark.asyncio
async def test_a_no_arg(t_client: Client):
    async with Worker(
        t_client,
        task_queue=MOCK_QUEUE_NAME,
        workflows=test_workflows,
        activities=test_activities,
    ):
        payload: ActivityExecutionInput = ActivityExecutionInput(
            activity_name="no_arg_activity",
            activity_task_queue=MOCK_QUEUE_NAME,
            args=None,
            start_to_close_timeout=10,
            parent_workflow_id="pytest-parent-workflow",
            execution_timeout=4,
        )
        resp: ExecutionResult = await internal_workflow_execution(
            client=t_client, payload=payload
        )
        assert resp.success, resp
        assert resp.data == "foo"


@pytest.mark.asyncio
async def test_a_seq_arg(t_client: Client):
    async with Worker(
        t_client,
        task_queue=MOCK_QUEUE_NAME,
        workflows=test_workflows,
        activities=test_activities,
    ):
        payload: ActivityExecutionInput = ActivityExecutionInput(
            activity_name="seq_arg_activity",
            activity_task_queue=MOCK_QUEUE_NAME,
            args=["spam", "eggs"],
            start_to_close_timeout=10,
            parent_workflow_id="pytest-parent-workflow",
            execution_timeout=4,
        )
        resp: ExecutionResult = await internal_workflow_execution(
            client=t_client, payload=payload
        )
        assert resp.success, resp
        assert resp.data == "spameggs"
