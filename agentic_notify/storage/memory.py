from typing import Any, Dict, List, Optional
from agentic_notify.storage.base import BaseStorage

class InMemoryStore(BaseStorage):
    """
    A simple dictionary-backed storage for rapid prototyping and testing.
    """
    def __init__(self):
        self.runs: Dict[str, Dict[str, Any]] = {}
        self.audits: List[Dict[str, Any]] = []

    async def save_workflow_run(self, run_id: str, run_data: Dict[str, Any]) -> None:
        self.runs[run_id] = run_data

    async def get_workflow_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        return self.runs.get(run_id)

    async def log_audit_event(self, event_type: str, data: Dict[str, Any]) -> None:
        self.audits.append({"event_type": event_type, "data": data})
