from misc.router import APIRouter, APIVersion
from .endpoints import activity_execution, workflow_execution


activity_router = APIRouter(
    prefix="/activity",
    tags=["Activities"],
    responses={
        404: {"description": "URL not found"},
        400: {"description": "Bad request"},
    },
    version=APIVersion(1),
)


workflow_router = APIRouter(
    prefix="/workflow",
    tags=["Workflows"],
    responses={
        404: {"description": "URL not found"},
        400: {"description": "Bad request"},
    },
    version=APIVersion(1),
)


activity_router.add_api_route(
    "/execute",
    activity_execution,
    summary="Execute any activity in the namespace",
    methods=["post"],
)


workflow_router.add_api_route(
    "/execute",
    workflow_execution,
    summary="Execute any workflow in the namespace",
    methods=["post"],
)
