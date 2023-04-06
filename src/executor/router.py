from fastapi import APIRouter as _APIRouter
from typing import NamedTuple
from .endpoints import activity_execution, workflow_execution


class APIVersion(NamedTuple):
    major: int = 1
    minor: int | None = None

    def __str__(self) -> str:  # pragma: no cover
        if self.minor is not None:
            return f"{self.major}_{self.minor}"
        else:
            return f"{self.major}"


class APIRouter(_APIRouter):
    def __init__(self, version: APIVersion | None = None, **kwargs):  # pragma: no cover # noqa: E501
        super().__init__(**kwargs)
        if version:
            self.prefix = f"/v{version}{self.prefix}"


execution_router = APIRouter(
    prefix="/execution",
    tags=["Temporal execution"],
    responses={
        404: {"description": "URL not found"},
        400: {"description": "Bad request"},
    },
    version=APIVersion(1),
)


execution_router.add_api_route(
    "/activity",
    activity_execution,
    summary="Execute any activity in the namespace",
    methods=["post"],
)

execution_router.add_api_route(
    "/workflow",
    workflow_execution,
    summary="Execute any workflow in the namespace",
    methods=["post"],
)
