from typing import Any, List, Optional, Dict

from pydantic import BaseModel, Field


class ServerModel(BaseModel):
    id: str
    name: str
    description: Optional[str]
    features: Optional[List[str]]
    owner_id: Optional[str]
    region: Optional[str]
    max_presences: Optional[int]
    max_members: Optional[int]
    preferred_locale: Optional[str]
    premium_tier: Optional[int]
    premium_subscription_count: Optional[int]
    approximate_member_count: Optional[int]
    approximate_presence_count: Optional[int]


class MessageAuthor(BaseModel):
    id: str
    username: Optional[str]


class ChannelMessage(BaseModel):
    id: str
    channel_id: Optional[str]
    content: Optional[str]
    author: Optional[MessageAuthor]


class ServersRequest(BaseModel):
    servers: Dict[str, List[str]]
    type: str


class ChannelsRequest(BaseModel):
    channels: Dict[str, List[str]]
    limit: Optional[int] = Field(None, ge=0, le=100)
    type: str
