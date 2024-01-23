import logging
from unittest.mock import MagicMock

import httpx
import pytest
from fastapi.testclient import TestClient

from parma_mining.discord.api.dependencies.auth import authenticate
from parma_mining.discord.api.main import app
from parma_mining.mining_common.const import HTTP_200
from tests.dependencies.mock_auth import mock_authenticate


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
def mock_discord_client(mocker) -> MagicMock:
    test_data = {
        "id": "428295358100013066",
        "name": "Solana Tech",
        "description": "null",
        "features": ["ANIMATED_ICON"],
        "owner_id": "996518139909116074",
        "region": "us-west",
        "max_presences": 0,
        "max_members": 500000,
        "preferred_locale": "en-US",
        "premium_tier": 3,
        "premium_subscription_count": 18,
        "approximate_member_count": 131799,
        "approximate_presence_count": 9129,
    }
    mock_get = mocker.patch("parma_mining.discord.api.main.DiscordClient.get")
    mock_get.return_value = httpx.Response(
        request=httpx.Request("GET", "test"), json=test_data, status_code=200
    )

    return mock_get


@pytest.fixture
def mock_analytics_client(mocker) -> MagicMock:
    """Mocking the AnalyticClient's method to avoid actual API calls during testing."""
    mock = mocker.patch("parma_mining.discord.api.main.AnalyticsClient.feed_raw_data")
    mock = mocker.patch(
        "parma_mining.discord.api.main.AnalyticsClient.crawling_finished"
    )
    mock.return_value = {}
    # No return value needed, but you can add side effects or exceptions if necessary
    return mock


def test_companies_success(
    client: TestClient, mock_discord_client: MagicMock, mock_analytics_client: MagicMock
):
    payload = {
        "task_id": 123,
        "companies": {
            "Example_id1": {"name": ["langfuse"]},
            "Example_id2": {"name": ["personio"]},
        },
    }
    headers = {"Authorization": "Bearer test"}
    response = client.post("/companies", json=payload, headers=headers)

    mock_analytics_client.assert_called()
    mock_discord_client.assert_called()
    assert response.status_code == HTTP_200
