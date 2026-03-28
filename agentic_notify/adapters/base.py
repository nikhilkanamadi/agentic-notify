from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAdapter(ABC):
    """
    An Adapter is responsible for performing a downstream action (e.g., calling an API, 
    saving to DB, triggering device native modules).
    This is entirely decoupled from the inbound integrations.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """The canonical name of the adapter used in workflow definitions."""
        pass

    @abstractmethod
    async def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the business action with the provided payload.
        Returns the output dict of the execution.
        """
        pass
