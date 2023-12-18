from pydantic import BaseModel, Field


class ServerModel(BaseModel):
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
    id: str
    username: str | None


class ChannelMessage(BaseModel):
    id: str
    channel_id: str | None
    content: str | None
    author: MessageAuthor | None


class ServersRequest(BaseModel):
    servers: dict[str, list[str]]
    type: str


class ChannelsRequest(BaseModel):
    channels: dict[str, list[str]]
    limit: int | None = Field(None, ge=0, le=100)
    type: str
