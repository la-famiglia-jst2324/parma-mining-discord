"""Pydantic models for discord data."""
from datetime import datetime

from pydantic import BaseModel, Field


class ServerListModel(BaseModel):
    """Listed servers model."""

    id: str
    name: str | None
    owner: bool | None
    permissions: str | None
    features: list[str] | None
    approximate_member_count: int | None
    approximate_presence_count: int | None


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


class CompaniesRequest(BaseModel):
    """Companies request model for GitHub data."""

    task_id: int
    companies: dict[str, dict[str, list[str]]]


class ResponseModel(BaseModel):
    """Response model for GitHub data."""

    source_name: str
    company_id: str
    raw_data: ServerModel


class DiscoveryRequest(BaseModel):
    """Request model for the discovery endpoint."""

    company_id: str
    name: str


class DiscoveryResponse(BaseModel):
    """Define the output model for the discovery endpoint."""

    server_ids: list[str] = []


class FinalDiscoveryResponse(BaseModel):
    """Define the final discovery response model."""

    identifiers: dict[str, DiscoveryResponse]
    validity: datetime


class ErrorInfoModel(BaseModel):
    """Error info for the crawling_finished endpoint."""

    error_type: str
    error_description: str | None


class CrawlingFinishedInputModel(BaseModel):
    """Internal base model for the crawling_finished endpoints."""

    task_id: int
    errors: dict[str, ErrorInfoModel] | None = None
