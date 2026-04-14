from datetime import datetime
from pydantic import BaseModel, Field


class JellyfinExternalIdsPayload(BaseModel):
    IMDB: str | None = Field(
        default=None,
        description="IMDb identifier for the media item, used as the internal media id.",
    )


class JellyfinMediaPayload(BaseModel):
    ExternalIds: JellyfinExternalIdsPayload = Field(
        default_factory=JellyfinExternalIdsPayload,
        description="External provider identifiers supplied by Jellyfin for the media.",
    )
    Title: str | None = Field(
        default=None,
        description="Primary media title provided by Jellyfin.",
    )
    EpisodeTitle: str | None = Field(
        default=None,
        description="Episode title fallback when a primary media title is not present.",
    )
    Year: int | str | None = Field(
        default=None,
        description="Release year provided by Jellyfin; can be numeric or string-formatted.",
    )


class JellyfinSessionPayload(BaseModel):
    PlayedToCompletion: bool | str | None = Field(
        default=None,
        description="Indicates whether playback reached completion in the reported session.",
    )
    UserId: str | int | None = Field(
        default=None,
        description="Jellyfin user identifier for the session that triggered the webhook.",
    )
    User: str | None = Field(
        default=None,
        description="Display username for the Jellyfin user in the playback session.",
    )


class JellyfinWebhookPayload(BaseModel):
    Session: JellyfinSessionPayload = Field(
        default_factory=JellyfinSessionPayload,
        description="Session details associated with the playback event.",
    )
    Media: JellyfinMediaPayload = Field(
        default_factory=JellyfinMediaPayload,
        description="Media details associated with the playback event.",
    )
    Timestamp: datetime | str | None = Field(
        default=None,
        description="Event timestamp from Jellyfin in ISO datetime format or equivalent string.",
    )

