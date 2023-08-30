from test.utils import read_json
import os
import pytest
from fastapi.testclient import TestClient

import logging

logger = logging.getLogger()


@pytest.mark.parametrize(
    "payload_path, response_path",
    [
        ("./test/fixtures/request.json", "./test/fixtures/response.json"),
        ("./test/fixtures/request_recent.json", "./test/fixtures/response_recent.json"),
        ("./test/fixtures/request_future.json", "./test/fixtures/response_future.json"),
    ],
)
def test_success_analysis_endpoint(
    client: TestClient, payload_path: str, response_path: str
) -> None:
    """
    Test the analysis endpoint with a valid payload.

    Args:
        client: The test client.
        payload_path: The path to the payload.
        response_path: The path to the expected response.

        Returns:
            None
    """
    assert os.path.exists(payload_path)
    assert os.path.exists(response_path)

    response = client.post("/api/v1/analysis", json=read_json(payload_path))

    assert response.status_code == 200

    expected_response = read_json(response_path)

    assert response.json() == expected_response
