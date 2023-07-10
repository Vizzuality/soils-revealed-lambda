from typing import Any, List

from fastapi import APIRouter, HTTPException


from soils.analysis.analysis import analysis
from soils import schemas


################################################################################
# Routes handler for the API
################################################################################
api_router = APIRouter()


#  response_model=List[schemas.AnalysisResponse]
@api_router.post("/analysis")
def get_data(params: schemas.AnalysisRequest) -> Any:
    try:
        result = analysis(params)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
