import json
import pytest
from fastapi.testclient import TestClient
from pydantic.tools import parse_obj_as

from soils.schemas import AnalysisRequest, AnalysisResponse


@pytest.mark.parametrize("payload_path", ["./fixtures/request.json"])
@pytest.mark.parametrize("response_path", ["./fixtures/response.json"])
def test_success_analysis_endpoint(
    client: TestClient, payload_path: str, response_path: str
) -> None:
    payload = parse_obj_as(AnalysisRequest, json.loads(payload_path))

    expected_response = parse_obj_as(AnalysisResponse, json.loads(response_path))
    response = client.post("/api/v1/analysis", json=payload)

    assert response.status_code == 200

    response_body = parse_obj_as(AnalysisResponse, response.json())

    assert response_body == expected_response
