from typing import Any, Dict
from abc import ABC, abstractmethod
from agentic_notify.schemas.notification import NotificationEvent

class BaseIntegration(ABC):
    """
    An Integration receives raw events from an external host system
    (e.g., FastAPI route, background worker, Webhook, RN Bridge).
    """

    @abstractmethod
    async def start(self) -> None:
        """Start the integration listener or service."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stop the integration."""
        pass
