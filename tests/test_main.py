from fastapi.testclient import TestClient

from app.main import app
from app.constants.api_properties import GLOBAL_PREFIX


client = TestClient(app)


def test_read_main():
    """test main"""
    response = client.get(GLOBAL_PREFIX + "/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from Revius API"}
