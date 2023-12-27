import requests
import pytest


@pytest.fixture
def res_api():
    FLASK_API_URL = "http://localhost:5000/search"
    params = {"query": "crevette", "table": "food"}
    response = requests.get(FLASK_API_URL, params=params)
    yield response


def test_api(res_api):
    response = res_api
    assert response.status_code == 200
