from typing import Optional

from pydantic import BaseModel


class AnalysisRequest(BaseModel):
    dataset: str
    variable: str
    years: list
    depth: str
    geometry: dict
    
    
class AnalysisResponse(BaseModel):
    dataset: str
    variable: str
    years: list
    depth: str
    geometry: dict
    value: float

# def myCoerc(n):
#     try:
#         return lambda v: None if v in ("null") else n(v)
#     except Exception:
#         return None


# null2int = myCoerc(int)
# null2float = myCoerc(float)

# to_bool = lambda v: v.lower() in ("true", "1")
# to_lower = lambda v: v.lower()
# # to_list = lambda v: json.loads(v.lower())
# to_list = lambda v: json.loads(v)



