from typing import List, Literal, Union

from pydantic import BaseModel, RootModel, Field, PrivateAttr


class AnalysisRequest(BaseModel):
    dataset: str
    variable: str
    years: List[str]
    depth: str
    geometry: dict


class CommonResponse(BaseModel):
    data: str
    counts: List[int]
    bins: List[float]
    mean_diff: float
    mean_years: List[int]
    mean_values: List[float]
    area_ha: float


class FutureResponse(CommonResponse):
    _type: Literal["future"]
    land_cover: dict
    land_cover_groups: dict


class RecentResponse(CommonResponse):
    _type: Literal["recent"]
    land_cover_group_2018: dict
    land_cover: dict
    land_cover_groups: dict


class AnalysisResponse(RootModel):
    root: Union[FutureResponse, RecentResponse] = Field(..., discriminator="_type")
