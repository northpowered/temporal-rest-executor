from .worker import Worker, test_activities, test_workflows, Client
import pytest
from fastapi.testclient import TestClient
from src.main import app


rest = TestClient(app)


# @pytest.mark.asyncio
# async def test_base(client2: Client):
#     async with Worker(
#         client2,
#         task_queue="service-b-task-queue",
#         workflows=test_workflows,
#         activities=test_activities,
#     ) as w:
#         print(client2.identity)
#         print(w.task_queue)
#         print(w.is_running)
#         p = {"str_1": "q", "str_2": "w"}
#         j = {
#             "activity_name": "dataclass_arg_activity",
#             "activity_task_queue": "service-b-task-queue",
#             "args": p,
#             "start_to_close_timeout": 10,
#             "execution_timeout": 4,
#             "parent_workflow_id": "string",
#         }
#         r = rest.post("/v1/execution/activity", json=j)
#         assert r.status_code == 200
#         resp = r.json()
#         assert resp["success"], resp

from src.temporal import (
    internal_workflow_execution,
    ActivityExecutionInput,
    ExecutionResult,
)


@pytest.mark.asyncio
async def test_base(client2: Client):
    async with Worker(
        client2,
        task_queue="service-b-task-queue",
        workflows=test_workflows,
        activities=test_activities,
    ):
        payload: ActivityExecutionInput = ActivityExecutionInput(
            activity_name="dataclass_arg_activity",
            activity_task_queue="service-b-task-queue",
            args={"str_1": "q", "str_2": "w"},
            start_to_close_timeout=10,
            parent_workflow_id="foobar",
            execution_timeout=4,
        )
        resp: ExecutionResult = await internal_workflow_execution(
            client=client2, payload=payload
        )
        assert resp.success, resp
