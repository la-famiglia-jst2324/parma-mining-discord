"""Pydantic models for discord data."""
from pydantic import BaseModel, Field


class ServerModel(BaseModel):
    """Server model for discord data.

    Used for /server endpoint.
    """

    id: str
    name: str
    description: str | None
    features: list[str] | None
    owner_id: str | None
    region: str | None
    max_presences: int | None
    max_members: int | None
    preferred_locale: str | None
    premium_tier: int | None
    premium_subscription_count: int | None
    approximate_member_count: int | None
    approximate_presence_count: int | None


class MessageAuthor(BaseModel):
    """Message author model for discord data."""

    id: str
    username: str | None


class ChannelMessage(BaseModel):
    """Channel message model for discord data.

    Used for /channel endpoint.
    """

    id: str
    channel_id: str | None
    content: str | None
    author: MessageAuthor | None


class ServersRequest(BaseModel):
    """/server Endpoint request model."""

    servers: dict[str, list[str]]
    type: str


class ChannelsRequest(BaseModel):
    """/channel Endpoint request model."""

    channels: dict[str, list[str]]
    limit: int | None = Field(None, ge=0, le=100)
    type: str
