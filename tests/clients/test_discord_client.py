from unittest.mock import patch

import httpx
import pytest

from parma_mining.discord.client import DiscordClient
from parma_mining.discord.model import ServerModel
from parma_mining.mining_common.exceptions import CrawlingError


@pytest.fixture
def discord_client():
    return DiscordClient("dummy_api_key", "dummy_api_version")


@patch("parma_mining.discord.client.DiscordClient.get")
def test_get_server_details_success(mock_get, discord_client: DiscordClient):
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

    mock_get.return_value = httpx.Response(
        request=httpx.Request("GET", "test"), json=test_data, status_code=200
    )

    result = discord_client.get_server_details("test_server_id")

    assert isinstance(result, ServerModel)
    assert result.name == "Solana Tech"


@patch("parma_mining.discord.client.DiscordClient.get")
def test_get_companies_by_list_exception(mock_get, discord_client: DiscordClient):
    exception_instance = CrawlingError("Error fetching organization details!")
    mock_get.side_effect = exception_instance
    with pytest.raises(CrawlingError):
        discord_client.get_server_details("test_server_id")
