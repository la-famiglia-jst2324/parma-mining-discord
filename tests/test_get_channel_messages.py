import logging
from unittest.mock import MagicMock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from parma_mining.discord.api.dependencies.auth import authenticate
from parma_mining.discord.api.dependencies.mock_auth import mock_authenticate
from parma_mining.discord.api.main import app


@pytest.fixture
def client():
    assert app
    app.dependency_overrides.update(
        {
            authenticate: mock_authenticate,
        }
    )
    return TestClient(app)


logger = logging.getLogger(__name__)


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


def test_get_channel_messages(client: TestClient, mock_pdl_client: MagicMock):
    payload = {"channels": {"test": ["testid"]}, "type": "channel_id", "limit": 50}
    response = client.post("/channel", json=payload)
    assert response.status_code == status.HTTP_200_OK
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
