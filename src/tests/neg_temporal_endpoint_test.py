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
async def test_unknown_activity(t_client: Client):
    async with Worker(
        t_client,
        task_queue=MOCK_QUEUE_NAME,
        workflows=test_workflows,
        activities=test_activities,
    ):
        payload: ActivityExecutionInput = ActivityExecutionInput(
            activity_name="dataclass_unknown_activity",
            activity_task_queue=MOCK_QUEUE_NAME,
            args={"str_1": "q", "str_2": "w"},
            start_to_close_timeout=10,
            parent_workflow_id="pytest-parent-workflow",
            execution_timeout=10,
        )
        resp: ExecutionResult = await activity_execution(
            client=t_client, payload=payload
        )
        assert not resp.success, resp
        assert resp.error == "Activity task failed"


@pytest.mark.asyncio
async def test_wrong_args_activity(t_client: Client):
    async with Worker(
        t_client,
        task_queue=MOCK_QUEUE_NAME,
        workflows=test_workflows,
        activities=test_activities,
    ):
        payload: ActivityExecutionInput = ActivityExecutionInput(
            activity_name="dataclass_arg_activity",
            activity_task_queue=MOCK_QUEUE_NAME,
            args={"str_FOO": "q", "str_2": "w"},
            start_to_close_timeout=10,
            parent_workflow_id="pytest-parent-workflow",
            execution_timeout=4,
        )
        resp: ExecutionResult = await activity_execution(
            client=t_client, payload=payload
        )
        assert not resp.success, resp
        assert resp.error == "Activity task failed"


@pytest.mark.asyncio
async def test_wrong_timeouts_activity(t_client: Client):
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
            start_to_close_timeout=-6,
            parent_workflow_id="pytest-parent-workflow",
            execution_timeout=4,
        )
        resp: ExecutionResult = await activity_execution(
            client=t_client, payload=payload
        )
        assert not resp.success, resp
        assert resp.error == "Workflow timed out"


@pytest.mark.asyncio
async def test_unknown_workflow(t_client: Client):
    async with Worker(
        t_client,
        task_queue=MOCK_QUEUE_NAME,
        workflows=test_workflows,
        activities=test_activities,
    ):
        payload: WorkflowExecutionInput = WorkflowExecutionInput(
            workflow_name="UNKNOWNDataclassArgWorkflow",
            workflow_task_queue=MOCK_QUEUE_NAME,
            args={"str_1": "q", "str_2": "w"},
            workflow_id="pytest-single-workflow",
            execution_timeout=4
        )
        resp: ExecutionResult = await workflow_execution(
            client=t_client, payload=payload
        )
        assert not resp.success, resp
        assert resp.error == "Workflow timed out"
