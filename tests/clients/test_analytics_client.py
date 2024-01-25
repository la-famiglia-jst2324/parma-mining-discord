from unittest.mock import patch

import httpx
import pytest

from parma_mining.discord.analytics_client import AnalyticsClient
from parma_mining.discord.model import ResponseModel, ServerModel
from parma_mining.mining_common.const import HTTP_200, HTTP_500

TOKEN = "mocked_token"


@pytest.fixture
def analytics_client():
    return AnalyticsClient()


@pytest.fixture
def mock_server_model():
    return ServerModel.model_validate(
        {
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
    )


@pytest.fixture
def mock_response_model(mock_server_model):
    return ResponseModel(
        source_name="TestSource",
        company_id="TestCompany",
        raw_data=mock_server_model,
    )


@patch("httpx.post")
def test_send_post_request_success(mock_post, analytics_client):
    mock_post.return_value = httpx.Response(HTTP_200, json={"key": "value"})
    response = analytics_client.send_post_request(
        TOKEN, "http://example.com", {"data": "test"}
    )
    assert response == {"key": "value"}


@patch("httpx.post")
def test_send_post_request_failure(mock_post, analytics_client):
    mock_post.return_value = httpx.Response(HTTP_500, text="Internal Server Error")
    with pytest.raises(Exception) as exc_info:
        analytics_client.send_post_request(
            TOKEN, "http://example.com", {"data": "test"}
        )
    assert "API request failed" in str(exc_info.value)


@patch("httpx.post")
def test_register_measurements(mock_post, analytics_client):
    mock_post.return_value = httpx.Response(HTTP_200, json={"id": "123"})
    mapping = {"Mappings": [{"DataType": "int", "MeasurementName": "test_metric"}]}
    result, updated_mapping = analytics_client.register_measurements(TOKEN, mapping)
    assert "source_measurement_id" in updated_mapping["Mappings"][0]
    assert result[0]["source_measurement_id"] == "123"


@patch("httpx.post")
def test_feed_raw_data(mock_post, analytics_client, mock_response_model):
    mock_post.return_value = httpx.Response(HTTP_200, json={"result": "success"})
    result = analytics_client.feed_raw_data(TOKEN, mock_response_model)
    assert result == {"result": "success"}
