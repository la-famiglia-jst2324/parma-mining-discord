from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from parma_mining.discord.api.main import app

client = TestClient(app)


@pytest.fixture
def mock_pdl_client(mocker) -> MagicMock:
    mock = mocker.patch(
        "parma_mining.discord.api.main.DiscordClient.get_channel_messages"
    )
    mock.return_value = [
        {
            "id": "1181602247747051561",
            "channel_id": "763957300507181077",
            "content": "",
            "author": {"id": "911615634343874590", "username": "friday1369"},
        },
        {
            "id": "1181602224745484308",
            "channel_id": "763957300507181077",
            "content": "Wednesday",
            "author": {"id": "1031359100744900728", "username": "scxrfxce99"},
        },
    ]
    return mock


def test_get_channel_messages(mock_pdl_client: MagicMock):
    payload = {"channels": {"test": ["testid"]}, "type": "channel_id", "limit": 50}
    response = client.post("/channel", json=payload)
    success_code = 200
    assert response.status_code == success_code
    assert response.json() == [
        [
            {
                "id": "1181602247747051561",
                "channel_id": "763957300507181077",
                "content": "",
                "author": {"id": "911615634343874590", "username": "friday1369"},
            },
            {
                "id": "1181602224745484308",
                "channel_id": "763957300507181077",
                "content": "Wednesday",
                "author": {"id": "1031359100744900728", "username": "scxrfxce99"},
            },
        ]
    ]
