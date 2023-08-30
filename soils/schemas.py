from typing import Dict, List, Any, Literal, Union

from pydantic import BaseModel, Field, RootModel

SCENARIOS = [
    "crop_I",
    "crop_MG",
    "crop_MGI",
    "grass_part",
    "grass_full",
    "rewilding",
    "degradation_ForestToGrass",
    "degradation_ForestToCrop",
    "degradation_NoDeforestation",
]


class AnalysisRequest(BaseModel):
    dataset: str
    variable: str
    years: List[str]
    depth: str
    geometry: dict


class CommonData(BaseModel):
    data: str
    counts: List[int]
    bins: List[float]
    mean_diff: float
    mean_years: List[int]
    mean_values: List[float]
    area_ha: float


class BaseResponse(CommonData):
    _type: Literal["common"]


class FutureResponse(CommonData):
    _type: Literal["future"]
    land_cover: Dict[str, Any]
    land_cover_groups: Dict[str, Any]


class RecentResponse(CommonData):
    _type: Literal["recent"]
    land_cover_group_2018: Dict[str, Any]
    land_cover: Dict[str, Any]
    land_cover_groups: Dict[str, Any]


class AnalysisResponse(RootModel):
    _root: Union[FutureResponse, RecentResponse, BaseResponse] = Field(
        ..., discriminator="_type", exclude=True
    )
