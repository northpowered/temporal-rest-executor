from pydantic import BaseModel, validator, BaseSettings
from executor.schemas import WorkflowExecutionInput, ActivityExecutionInput
import yaml
import os
from loguru import logger
from typing import List

class PreDefinedEndpoint(BaseModel):
    type: str | None = None
    url: str | None = None
    config: WorkflowExecutionInput | ActivityExecutionInput | None = None

    class Config:
        allow_population_by_field_name = True


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
        print(raw_data)
        print(self.__fields__)
        for section_name in self.__fields__:
            print(section_name)
            section_data: dict = raw_data.get(section_name, dict())
            print(section_data)
            section: BaseModel = self.__getattribute__(section_name)
            loaded_section: BaseModel = section.parse_obj(
                section_data,
                section_name
            )
            print(loaded_section)
            if not loaded_section:
                os._exit(1)
            self.__setattr__(
                section_name,
                loaded_section
            )
        self.Config.use_presets = True

    def load(self, filename: str):
        try:
            raw_data: dict = dict()
            with open(filename, 'r') as f:
                raw_data = yaml.load(f, yaml.loader.SafeLoader)
            self.read_from_dict(raw_data)
        except FileNotFoundError:
            logger.warning("Manifest not found, presets disabled")


manifest: PresetManifest = PresetManifest()
