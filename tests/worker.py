import asyncio
from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker
from dataclasses import dataclass
from datetime import timedelta


@dataclass
class ConcExecutionPayload:
    str_1: str
    str_2: str


@activity.defn()
async def dataclass_arg_activity(input: ConcExecutionPayload) -> str:
    return input.str_1 + input.str_2


@activity.defn()
async def single_arg_activity(input: str) -> str:
    return input + input


@activity.defn()
async def no_arg_activity() -> str:
    return "foo"


@activity.defn()
async def seq_arg_activity(str_1: str, str_2: str) -> str:
    return str_1 + str_2


@workflow.defn(sandboxed=False)
class DataclassArgWorkflow:
    @workflow.run
    async def run(self, input: ConcExecutionPayload) -> dict:
        return await workflow.execute_activity(
            dataclass_arg_activity,
            input,
            start_to_close_timeout=timedelta(seconds=10),
        )


@workflow.defn(sandboxed=False)
class SingleArgWorkflow:
    @workflow.run
    async def run(self, input: str) -> dict:
        return await workflow.execute_activity(
            single_arg_activity,
            input,
            start_to_close_timeout=timedelta(seconds=10),
        )


@workflow.defn(sandboxed=False)
class NoArgWorkflow:
    @workflow.run
    async def run(self) -> dict:
        return await workflow.execute_activity(
            no_arg_activity,
            start_to_close_timeout=timedelta(seconds=10),
        )


@workflow.defn(sandboxed=False)
class SeqArgWorkflow:
    @workflow.run
    async def run(self, str_1: str, str_2: str) -> dict:
        return await workflow.execute_activity(
            seq_arg_activity,
            args=[str_1, str_2],
            start_to_close_timeout=timedelta(seconds=10),
        )



test_workflows: list = [
            DataclassArgWorkflow,
            SingleArgWorkflow,
            NoArgWorkflow,
            SeqArgWorkflow,
        ]
test_activities: list = [
            dataclass_arg_activity,
            single_arg_activity,
            no_arg_activity,
            seq_arg_activity,
        ]


async def create_worker() -> Worker:
    client = await Client.connect(
        "localhost:7233",
    )

    worker = Worker(
        client,
        task_queue="service-b-task-queue",
        workflows=test_workflows,
        activities=test_activities,
    )
    return worker


async def run_worker():
    worker = await create_worker()
    await worker.run()


def run_worker_sync():
    asyncio.run(run_worker())
