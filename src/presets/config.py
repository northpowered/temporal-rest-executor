from misc.router import APIRouter, APIVersion
from functools import partial
from fastapi import Depends
from executor.temporal import (
    temporal_client,
    Client,
    internal_workflow_execution,
    external_workflow_execution,
)
from pydantic import BaseModel, validator, BaseSettings, parse_obj_as
from executor.schemas import WorkflowExecutionInput, ActivityExecutionInput
import yaml
import os
from loguru import logger
from typing import List, Coroutine, Any

class PreDefinedEndpoint(BaseModel):
    type: str | None = None
    url: str | None = None
    config: WorkflowExecutionInput | ActivityExecutionInput | None = None

    class Config:
        allow_population_by_field_name = True
        smart_union = True


    @validator('type')
    def check_type(cls, v):
        assert v in ['workflow', 'activity'], f"Unknown endpoint type {v}"
        return v

    @validator('url')
    def check_url(cls, v):
        assert len(v) >= 2, "Url len MUST be >= 2"
        assert v[0] == '/', "Url MUST starts with /"
        return v


class PresetManifest(BaseSettings):

    endpoints: List[PreDefinedEndpoint] = list()
    
    class Config:
        use_presets: bool = False
        allow_population_by_field_name = True

    def read_from_dict(self, raw_data: dict):

        self.endpoints = parse_obj_as(List[PreDefinedEndpoint], raw_data.get('endpoints', list()))
        self.Config.use_presets = True

    def load(self, filename: str):
        try:
            raw_data: dict = dict()
            with open(filename, 'r') as f:
                raw_data = yaml.load(f, yaml.loader.SafeLoader)
            self.read_from_dict(raw_data)
        except FileNotFoundError:
            logger.warning("Manifest not found, presets disabled")

    def validate_presets(self) -> bool:
        urls: list = list()
        for endpoint in self.endpoints:
            urls.append(endpoint.url)
        seen = set()
        dupes = [x for x in urls if x in seen or seen.add(x)]
        if len(dupes):
            logger.error(f"URL duplications found: {dupes}")
            return False
        return True

    def generate_router(self) -> APIRouter:
        router = APIRouter(
            prefix="/presets",
            tags=["Presets"],
            responses={
                404: {"description": "URL not found"},
                400: {"description": "Bad request"},
            },
            version=APIVersion(1),
        )
        for endpoint in self.endpoints:
            client: Client = Depends(temporal_client)
            match endpoint.type:
                case "activity": 
                    prototype = internal_workflow_execution
                case "workflow": 
                    prototype = external_workflow_execution
            
            

            router.add_api_route(
                path=endpoint.url,
                endpoint=partial(
                    prototype,
                    client=client,
                    payload=endpoint.config
                ),
                dependencies=[client],
                methods=['post'],
                response_model=Any,
                summary="Add it!",
                description="Add it!",
                
            )
        return router

manifest: PresetManifest = PresetManifest()
