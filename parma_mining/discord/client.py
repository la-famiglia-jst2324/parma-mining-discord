"""Discord API client."""
import logging

import httpx
from fastapi import status
from httpx import Response

from parma_mining.discord.model import (
    ChannelMessage,
    DiscoveryResponse,
    ServerListModel,
    ServerModel,
)
from parma_mining.mining_common.exceptions import ClientError, CrawlingError

logger = logging.getLogger(__name__)


class DiscordClient:
    """Discord API client."""

    def __init__(self, authorization_key: str, base_url: str):
        """Initialize Discord API client."""
        self.authorization_key = authorization_key
        self.base_url = base_url

    def get(self, path: str, params: dict[str, str]) -> Response:
        """Make a GET request to the Discord API."""
        full_path = self.base_url + path
        return httpx.get(
            url=full_path,
            headers={
                "Content-Type": "application/json",
                "Authorization": self.authorization_key,
            },
            params=params,
            timeout=30,
        )

    def get_all_servers(self) -> list[ServerListModel]:
        """Get all servers that user has joined."""
        path = "/users/@me/guilds"
        params = {"with_counts": "True"}
        try:
            response = self.get(path, params)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error(f"Error response {exc.response.status_code} ")

            if exc.response.status_code == status.HTTP_404_NOT_FOUND:
                error_detail = "Servers not found."
            else:
                error_detail = str(exc)
            raise CrawlingError(error_detail)

        result = []
        for server in response.json():
            parsed_server = ServerListModel.model_validate(server)
            result.append(parsed_server)
        return result

    def search_organizations(self, query: str) -> DiscoveryResponse:
        """Search organization on Discord."""
        try:
            servers = self.get_all_servers()
            channel_ids = []
            for server in servers:
                if query in str(server.name):
                    channel_ids.append(server.id)
            return DiscoveryResponse.model_validate({"server_ids": channel_ids})
        except Exception as e:
            msg = f"Error searching organizations for {query}: {e}"
            logger.error(msg)
            raise ClientError()

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
            raise CrawlingError(error_detail)
        parsed_server = ServerModel.model_validate(response.json())
        return parsed_server

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
            raise CrawlingError(error_detail)

        messages = []
        for message in response.json():
            parsed_message = ChannelMessage.model_validate(message)
            messages.append(parsed_message)
        return messages
