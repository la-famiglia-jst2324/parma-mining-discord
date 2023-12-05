"""Main entrypoint for the API routes in of parma-analytics."""

from fastapi import FastAPI, status
import os
from dotenv import load_dotenv
from parma_mining.discord.client import DiscordClient
from typing import List
from parma_mining.discord.model import (
    ChannelMessage,
    ChannelsRequest,
    ServerModel,
    ServersRequest,
)


load_dotenv()

authorization_key = str(os.getenv("DISCORD_AUTH_KEY"))
base_url = str(os.getenv("DISCORD_BASE_URL"))

app = FastAPI()


# root endpoint
@app.get("/", status_code=200)
def root():
    """Root endpoint for the API."""
    return {"welcome": "at parma-mining-discord"}


@app.get("/server", status_code=status.HTTP_200_OK)
def get_server_details(servers: ServersRequest) -> List[ServerModel]:
    _discordClient = DiscordClient(authorization_key, base_url)
    all_server_details = []

    for company_name, server_ids in servers.servers.items():
        for server_id in server_ids:
            server_details = _discordClient.get_server_details(server_id)
            all_server_details.append(server_details)
    return all_server_details


@app.get("/channel", status_code=status.HTTP_200_OK)
def get_channel_details(channels: ChannelsRequest) -> List[List[ChannelMessage]]:
    _discordClient = DiscordClient(authorization_key, base_url)
    all_channel_details = []

    for company_name, channel_ids in channels.channels.items():
        for channel_id in channel_ids:
            channel_details = _discordClient.get_channel_messages(
                channel_id, channels.limit or 100
            )
            all_channel_details.append(channel_details)
    return all_channel_details
