import logging
from typing import Any
from pydantic.tools import parse_obj_as

from soils.schemas import AnalysisRequest, AnalysisResponse
from soils.analysis.statistics import SoilStatistics, LandCoverStatistics

logger = logging.getLogger()
logger.setLevel(logging.INFO)

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


def analysis(event: AnalysisRequest) -> Any:
    """
    Perform analysis based on the provided event.

    Args:
        event: The event containing the analysis request.

    Returns:
        A dictionary containing the computed statistics.
    """
    logger.info(f"## EVENT\r {event}")

    dataset = event.dataset
    group_type = (
        "recent" if dataset == "recent" else "future" if dataset in SCENARIOS else None
    )

    logger.info(f"## GROUP_TYPE\r {group_type}")

    stats_dict = {}

    # Get general statistics
    soil_statistics = SoilStatistics(event.dict())
    stats_dict.update(soil_statistics.get_statistics())

    # Get land cover statistics
    if group_type:
        lc_statistics = LandCoverStatistics(event.dict(), group_type)
        stats_dict.update(lc_statistics.get_statistics())

    # TODO: this is a temporary fix to avoid the serialization of the
    #      numpy arrays. We should find a better way to do this
    return stats_dict
    # return parse_obj_as(AnalysisResponse, stats_dict)
