import pytest
from .worker import (
    Worker,
    Client,
    test_activities,
    test_workflows,
    MOCK_QUEUE_NAME
)
from executor.temporal import (
    ExecutionResult,
    WorkflowExecutionInput,
    external_workflow_execution,
)


@pytest.mark.asyncio
async def test_w_dataclass(t_client: Client):
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
        resp: ExecutionResult = await external_workflow_execution(
            client=t_client, payload=payload
        )
        assert resp.success, resp
        assert resp.data == "qw"


@pytest.mark.asyncio
async def test_w_single_arg(t_client: Client):
    async with Worker(
        t_client,
        task_queue=MOCK_QUEUE_NAME,
        workflows=test_workflows,
        activities=test_activities,
    ):
        payload: WorkflowExecutionInput = WorkflowExecutionInput(
            workflow_name="SingleArgWorkflow",
            workflow_task_queue=MOCK_QUEUE_NAME,
            args="spam",
            workflow_id="pytest-single-workflow",
        )
        resp: ExecutionResult = await external_workflow_execution(
            client=t_client, payload=payload
        )
        assert resp.success, resp
        assert resp.data == "spamspam"


@pytest.mark.asyncio
async def test_w_no_arg(t_client: Client):
    async with Worker(
        t_client,
        task_queue=MOCK_QUEUE_NAME,
        workflows=test_workflows,
        activities=test_activities,
    ):
        payload: WorkflowExecutionInput = WorkflowExecutionInput(
            workflow_name="NoArgWorkflow",
            workflow_task_queue=MOCK_QUEUE_NAME,
            args=None,
            workflow_id="pytest-single-workflow",
        )
        resp: ExecutionResult = await external_workflow_execution(
            client=t_client, payload=payload
        )
        assert resp.success, resp
        assert resp.data == "foo"


@pytest.mark.asyncio
async def test_w_seq_arg(t_client: Client):
    async with Worker(
        t_client,
        task_queue=MOCK_QUEUE_NAME,
        workflows=test_workflows,
        activities=test_activities,
    ):
        payload: WorkflowExecutionInput = WorkflowExecutionInput(
            workflow_name="SeqArgWorkflow",
            workflow_task_queue=MOCK_QUEUE_NAME,
            args=["spam", "eggs"],
            workflow_id="pytest-single-workflow",
        )
        resp: ExecutionResult = await external_workflow_execution(
            client=t_client, payload=payload
        )
        assert resp.success, resp
        assert resp.data == "spameggs"
