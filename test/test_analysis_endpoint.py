from test.utils import read_json
import os
import pytest
from fastapi.testclient import TestClient
from pydantic.tools import parse_obj_as

from soils.schemas import AnalysisRequest, AnalysisResponse


@pytest.mark.parametrize(
    "payload_path",
    [
        "./test/fixtures/request.json",
        "./test/fixtures/request_recent.json",
        "./test/fixtures/request_future.json"
    ]
)
@pytest.mark.parametrize(
    "response_path", 
    [
        "./test/fixtures/response.json", 
        "./test/fixtures/response_recent.json",
        "./test/fixtures/response_future.json"
    ]
)
def test_success_analysis_endpoint(
    client: TestClient, payload_path: str, response_path: str
) -> None:
    assert os.path.exists(payload_path)
    assert os.path.exists(response_path)

    payload = parse_obj_as(AnalysisRequest, read_json(payload_path))

    response = client.post("/api/v1/analysis", json=payload.dict())

    assert response.status_code == 200

    expected_response = parse_obj_as(AnalysisResponse, read_json(response_path))

    response_body = parse_obj_as(AnalysisResponse, response.json())

    assert response_body == expected_response
