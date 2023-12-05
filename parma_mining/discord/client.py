from fastapi import HTTPException
import httpx
from httpx import Response
from typing import List
from urllib.parse import urljoin

from parma_mining.discord.model import ChannelMessage, ServerModel


class DiscordClient:
    def __init__(self, authorization_key: str, base_url: str):
        self.authorization_key = authorization_key
        self.base_url = base_url

    def get(self, path: str, params: dict[str, str]) -> Response:
        full_path = (
            self.base_url + path
        )  # TODO : Make this concat with urljoin if possible
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
    ) -> List[ChannelMessage]:
        path = "/channels/" + channel_id + "/messages"
        params = {"limit": str(number_of_messages)}
        try:
            response = self.get(path, params)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
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
        path = "/guilds/" + server_id
        params = {"with_counts": "True"}
        try:
            response = self.get(path, params)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                error_detail = "Server not found."
            else:
                error_detail = str(exc)
            raise HTTPException(
                status_code=exc.response.status_code, detail=error_detail
            )

        parsed_server = ServerModel.model_validate(response.json())
        return parsed_server
