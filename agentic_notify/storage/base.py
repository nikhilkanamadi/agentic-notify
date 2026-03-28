from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class BaseStorage(ABC):
    """
    Storage layer abstraction for runs, step cache, audit trails, and configurations.
    """
    
    @abstractmethod
    async def save_workflow_run(self, run_id: str, run_data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    async def get_workflow_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        pass
        
    @abstractmethod
    async def log_audit_event(self, event_type: str, data: Dict[str, Any]) -> None:
        pass
