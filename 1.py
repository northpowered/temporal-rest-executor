from fastapi import FastAPI, Depends
import uvicorn
from temporalio.client import Client
from temporalio.worker import Worker
from temporalio import activity
from typing import Any
import datetime
from encryption.codec import EncryptionCodec
import dataclasses
import temporalio.converter


app = FastAPI(
    docs_url="/doc"
)


async def create_t_client():
    return await Client.connect(
        "localhost:7233",
        data_converter=dataclasses.replace(
            temporalio.converter.default(), payload_codec=EncryptionCodec()
        ),
    )

async def foo_endpoint(
        workflow: str,
        args: Any,
        queue: str,
        id: str,
        client: Client = Depends(create_t_client)
    ):
    
    resp = await client.execute_workflow(
        workflow,
        args,
        task_queue=queue,
        id=id
    )
    return resp

app.add_api_route('/foo',endpoint=foo_endpoint,methods=['POST'])


if __name__ == "__main__":
    uvicorn.run(
        "c:app"
    )