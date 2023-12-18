from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from parma_mining.discord.api.main import app

client = TestClient(app)


@pytest.fixture
def mock_pdl_client(mocker) -> MagicMock:
    mock = mocker.patch(
        "parma_mining.discord.api.main.DiscordClient.get_server_details"
    )
    mock.return_value = {
        "id": "363985050578190336",
        "name": "English",
        "description": "Join the best place to practice your English skills",
        "features": [
            "ANIMATED_ICON",
            "GUILD_COMMUNICATION_DISABLED_GUILDS",
            "NEW_THREAD_PERMISSIONS",
        ],
        "owner_id": "313389983904038915",
        "region": "europe",
        "max_presences": None,
        "max_members": 750000,
        "preferred_locale": "en-US",
        "premium_tier": 3,
        "premium_subscription_count": 256,
        "approximate_member_count": 736507,
        "approximate_presence_count": 62512,
    }
    return mock


def test_get_server_details(mock_pdl_client: MagicMock):
    payload = {"servers": {"test": ["testid"]}, "type": "server_id"}
    response = client.post("/server", json=payload)
    success_code = 200
    assert response.status_code == success_code
    assert response.json() == [
        {
            "id": "363985050578190336",
            "name": "English",
            "description": "Join the best place to practice your English skills",
            "features": [
                "ANIMATED_ICON",
                "GUILD_COMMUNICATION_DISABLED_GUILDS",
                "NEW_THREAD_PERMISSIONS",
            ],
            "owner_id": "313389983904038915",
            "region": "europe",
            "max_presences": None,
            "max_members": 750000,
            "preferred_locale": "en-US",
            "premium_tier": 3,
            "premium_subscription_count": 256,
            "approximate_member_count": 736507,
            "approximate_presence_count": 62512,
        }
    ]
