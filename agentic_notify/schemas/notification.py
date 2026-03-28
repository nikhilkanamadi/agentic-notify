from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class NotificationEvent(BaseModel):
    """
    The canonical schema for an incoming platform event (e.g., from Android/iOS/Web).
    All integrations must parse their raw events into this format.
    """
    event_id: str
    kind: str = "notification"
    source_platform: str
    source_app: str
    title: Optional[str] = None
    body: Optional[str] = None
    received_at: datetime = Field(default_factory=datetime.utcnow)
    priority_hint: str = "unknown"
    metadata: Dict[str, Any] = Field(default_factory=dict)
