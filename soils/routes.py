from typing import Any, List
import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse


from soils.analysis.analysis import analysis
from soils.schemas import AnalysisRequest, AnalysisResponse
from soils.encoders import NpEncoder
import logging


################################################################################
# Routes handler for the API
################################################################################
api_router = APIRouter()


# TODO: add as response model response_model=List[AnalysisResponse]
@api_router.post("/analysis", response_model=List[AnalysisResponse])
def get_data(params: AnalysisRequest) -> Any:
    try:
        result = analysis(params)
        return JSONResponse(
            content=json.loads(json.dumps(result, cls=NpEncoder)), status_code=200
        )

    except Exception as e:
        logging.error(e.__dict__)
        raise HTTPException(status_code=500, detail=str(e))
