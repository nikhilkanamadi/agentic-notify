from abc import ABC, abstractmethod
from typing import Any, Dict

from agentic_notify.schemas.notification import NotificationEvent

class BaseHandler(ABC):
    """
    A Handler is responsible for processing a step logic in memory.
    It does not necessarily perform a permanent external action (like an Adapter),
    but typically manipulates, routes, or transforms data (e.g., classification, summarization).
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """The canonical name of the handler used in workflow definitions."""
        pass

    @abstractmethod
    async def handle(self, event: NotificationEvent, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the notification event and context.
        Returns the mutated context or result of the handling.
        """
        pass
