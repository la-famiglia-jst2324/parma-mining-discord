"""Main entrypoint for the API routes in of parma-analytics."""
import logging
import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, status

from parma_mining.discord.api.dependencies.auth import authenticate
from parma_mining.discord.client import DiscordClient
from parma_mining.discord.model import (
    ChannelMessage,
    ChannelsRequest,
    ServerModel,
    ServersRequest,
)

env = os.getenv("DEPLOYMENT_ENV", "local")

if env == "prod":
    logging.basicConfig(level=logging.INFO)
elif env in ["staging", "local"]:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.warning(f"Unknown environment '{env}'. Defaulting to INFO level.")
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

load_dotenv()

authorization_key = str(os.getenv("DISCORD_AUTH_KEY"))
base_url = str(os.getenv("DISCORD_BASE_URL"))

app = FastAPI()


# root endpoint
@app.get("/", status_code=200)
def root():
    """Root endpoint for the API."""
    logger.debug("Root endpoint called")
    return {"welcome": "at parma-mining-discord"}


@app.post("/server", status_code=status.HTTP_200_OK)
def get_server_details(
    servers: ServersRequest, token: str = Depends(authenticate)
) -> list[ServerModel]:
    """Endpoint to get detailed information about a dict of servers."""
    discord_client = DiscordClient(authorization_key, base_url)
    all_server_details = []

    for company_name, server_ids in servers.servers.items():
        for server_id in server_ids:
            server_details = discord_client.get_server_details(server_id)
            all_server_details.append(server_details)
    return all_server_details


@app.post("/channel", status_code=status.HTTP_200_OK)
def get_channel_details(
    channels: ChannelsRequest, token: str = Depends(authenticate)
) -> list[list[ChannelMessage]]:
    """Endpoint to get detailed information about a dict of channels."""
    discord_client = DiscordClient(authorization_key, base_url)
    all_channel_details = []

    for company_name, channel_ids in channels.channels.items():
        for channel_id in channel_ids:
            channel_details = discord_client.get_channel_messages(
                channel_id, channels.limit or 100
            )
            all_channel_details.append(channel_details)
    return all_channel_details
