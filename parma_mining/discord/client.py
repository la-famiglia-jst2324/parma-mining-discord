"""Discord API client."""
import logging
from urllib.parse import urljoin

import httpx
from fastapi import HTTPException, status
from httpx import Response

from parma_mining.discord.model import ChannelMessage, ServerModel

logger = logging.getLogger(__name__)


class DiscordClient:
    """Discord API client."""

    def __init__(self, authorization_key: str, base_url: str):
        """Initialize Discord API client."""
        self.authorization_key = authorization_key
        self.base_url = base_url

    def get(self, path: str, params: dict[str, str]) -> Response:
        """Make a GET request to the Discord API."""
        full_path = urljoin(self.base_url, path)
        return httpx.get(
            url=full_path,
            headers={
                "Content-Type": "application/json",
                "Authorization": self.authorization_key,
            },
            params=params,
        )

    def get_channel_messages(
        self, channel_id: str, number_of_messages: int
    ) -> list[ChannelMessage]:
        """Get the last n messages from a channel."""
        path = "/channels/" + channel_id + "/messages"
        params = {"limit": str(number_of_messages)}
        try:
            response = self.get(path, params)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"Error response {exc.response.status_code} "
                f"for channel {channel_id}: {str(exc)}"
            )

            if exc.response.status_code == status.HTTP_404_NOT_FOUND:
                error_detail = "Channel not found."
            else:
                error_detail = str(exc)
            raise HTTPException(
                status_code=exc.response.status_code, detail=error_detail
            )
        messages = []
        for message in response.json():
            parsed_message = ChannelMessage.model_validate(message)
            messages.append(parsed_message)
        return messages

    def get_server_details(self, server_id: str) -> ServerModel:
        """Get detailed information about a server."""
        path = "/guilds/" + server_id
        params = {"with_counts": "True"}
        try:
            response = self.get(path, params)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"Error response {exc.response.status_code} "
                f"for server {server_id}: {str(exc)}"
            )

            if exc.response.status_code == status.HTTP_404_NOT_FOUND:
                error_detail = "Server not found."
            else:
                error_detail = str(exc)
            raise HTTPException(
                status_code=exc.response.status_code, detail=error_detail
            )

        parsed_server = ServerModel.model_validate(response.json())
        return parsed_server
