from pydantic import BaseModel
from typing import Any
from dataclasses import dataclass


# We use dataclasses instead of Pydantic for workflow args
# to avoid issues with workflow-unsafe Pydantic features


@dataclass
class ActivityExecutionInput:
    activity_name: str
    activity_task_queue: str
    args: Any | None = None
    start_to_close_timeout: int = 10
    execution_timeout: int = 10
    parent_workflow_id: str | None = None


@dataclass
class WorkflowExecutionInput:
    workflow_name: str
    workflow_task_queue: str
    args: Any | None = None
    workflow_id: str | None = None
    execution_timeout: int = 10


@dataclass
class InternalOutput:
    success: bool = True
    data: Any | None = None


class ExecutionResult(BaseModel):
    success: bool = True
    execution_init: ActivityExecutionInput | WorkflowExecutionInput
    execution_id: str = ""
    error: str | None = None
    data: Any | None = None
