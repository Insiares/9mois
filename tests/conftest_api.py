import requests
import pytest

def test_api():
    FLASK_API_URL = "http://localhost:5000/search"
    params = {"query": "crevette", "table": "food"}
    response = requests.get(FLASK_API_URL, params=params)
    assert response.status_code == 200