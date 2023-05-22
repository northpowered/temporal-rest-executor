from pydantic import BaseModel
from typing import Any
from dataclasses import dataclass
from temporalio.common import RetryPolicy
from .common import schedule_timeout_from_request


# We use dataclasses instead of Pydantic for workflow args
# to avoid issues with workflow-unsafe Pydantic features


@dataclass
class RetryPolicyInput:
    initial_interval: int = 1
    backoff_coefficient: float = 2
    maximum_interval: int | None = None
    maximum_attempts: int = 0

    def get_policy(self) -> RetryPolicy:
        return RetryPolicy(
            initial_interval=schedule_timeout_from_request(
                self.initial_interval
            ),
            backoff_coefficient=self.backoff_coefficient,
            maximum_interval=schedule_timeout_from_request(
                self.maximum_interval
            ),
            maximum_attempts=self.maximum_attempts,
        )


@dataclass
class ActivityExecutionInput:
    activity_name: str
    activity_task_queue: str
    args: Any | None = None
    start_to_close_timeout: int = 10
    parent_workflow_id: str | None = None
    schedule_to_start_timeout: int | None = None
    heartbeat_timeout: int | None = None
    schedule_to_close_timeout: int | None = None
    retry_policy: RetryPolicyInput | None = None
    parent_workflow_execution_timeout: int = 10
    parent_workflow_run_timeout: int | None = None
    parent_workflow_task_timeout: int | None = None

    def get_policy(self) -> RetryPolicy | None:
        if self.retry_policy:
            return self.retry_policy.get_policy()
        else:
            return None


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

    class Config:
        smart_union = True