from typing import Dict, List, Any, Literal, Union

from pydantic import BaseModel


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
    land_cover: Dict[str, Any]
    land_cover_groups: Dict[str, Any]


class RecentResponse(FutureResponse):
    _type: Literal["recent"]
    land_cover_group_2018: Dict[str, Any]

class AnalysisResponse(BaseModel):
    dataset: str
    variable: str
    years: List[str]
    depth: str
    geometry: Dict[str, Any]
    root: Union[FutureResponse, RecentResponse]

    @classmethod
    def from_common_response(cls, common_response: CommonResponse, dataset: str
                             ) -> "AnalysisResponse":
        if dataset == "recent":
            root = RecentResponse(
                _type="recent",
                land_cover_group_2018={},
                land_cover={},
                land_cover_groups={},
                **common_response.dict()
            )
        elif dataset in SCENARIOS:
            root = FutureResponse(
                _type="future",
                land_cover={},
                land_cover_groups={},
                **common_response.dict()
            )
        else:
            root = common_response

        return cls(
            dataset=dataset,
            variable="",
            years=[],
            depth="",
            geometry={},
            root=root
        )