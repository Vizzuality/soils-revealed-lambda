import json
import pytest
import requests

def read_payload_from_file(filename):
    with open(filename) as file:
        payload = json.load(file)
    return payload

@pytest.fixture(params=['data_recent.json', 'data_future.json'])
def payload(request):
    return read_payload_from_file(request.param)

def test_analysis_endpoint(payload):
    url = 'http://localhost:5020/api/v1/analysis'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    assert response.status_code == 200
    response_data = response.json()

    # Common assertions for both payloads
    assert 'data' in response_data
    assert 'counts' in response_data['data']
    assert 'bins' in response_data['data']
    assert "mean_diff" in response_data['data']
    assert "mean_years" in response_data['data']
    assert "mean_values" in response_data['data']
    assert "area_ha" in response_data['data']
    assert "land_cover" in response_data['data']
    assert "land_cover_groups" in response_data['data']

    # Perform assertions based on the payload
    if 'dataset' in payload and payload['dataset'] == 'recent':
        assert "land_cover_group_2018" in response_data['data']
