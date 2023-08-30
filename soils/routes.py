from typing import Any
import json

from fastapi import APIRouter, HTTPException

from soils.analysis.analysis import analysis
from soils.schemas import AnalysisRequest, AnalysisResponse
from soils.encoders import NpEncoder

import logging
import traceback


################################################################################
# Routes handler for the API
################################################################################
api_router = APIRouter()


@api_router.post("/analysis", response_model=AnalysisResponse)
def get_data(params: AnalysisRequest) -> Any:
    try:
        result = analysis(params)
        # return JSONResponse(
        #     content=, status_code=200
        # )
        return json.loads(json.dumps(result, cls=NpEncoder))

    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error(e.__context__)
        logging.error(e.__dict__)
        raise HTTPException(status_code=500, detail=str(e))
