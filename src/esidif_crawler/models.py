from datetime import datetime

from pydantic import BaseModel, Field


class DiscoveredLink(BaseModel):
    url: str
    source_url: str
    anchor_text: str = ""
    depth: int = 0
    is_document: bool = False

class DocumentRecord(BaseModel):
    url: str
    canonical_url: str
    source_url: str
    title: str = ""
    anchor_text: str = ""
    module: str = ""
    mime_type: str = ""
    extension: str = ""
    filename: str = ""
    size_bytes: int | None = None
    sha256: str | None = None
    first_seen: datetime = Field(default_factory=datetime.utcnow)
    last_seen: datetime = Field(default_factory=datetime.utcnow)
    status: str = "discovered"
    local_path: str | None = None
