from fastapi import Depends
from .temporal import (
    temporal_client,
    Client,
    internal_workflow_execution,
    external_workflow_execution,
)
from .schemas import WorkflowExecutionInput, ActivityExecutionInput


async def workflow_execution(
    payload: WorkflowExecutionInput,
    client: Client = Depends(temporal_client)
):
    return await external_workflow_execution(client=client, payload=payload)


async def activity_execution(
    payload: ActivityExecutionInput,
    client: Client = Depends(temporal_client)
):
    return await internal_workflow_execution(client=client, payload=payload)
