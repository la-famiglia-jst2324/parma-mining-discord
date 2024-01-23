from fastapi.testclient import TestClient

from parma_mining.discord.api.main import app
from parma_mining.mining_common.const import HTTP_200, HTTP_405

client = TestClient(app)


def test_root_success():
    response = client.get("/")
    assert response.status_code == HTTP_200
    assert response.json() == {"welcome": "at parma-mining-discord"}


def test_root_method_not_allowed():
    response = client.post("/")
    assert response.status_code == HTTP_405
