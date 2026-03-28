from typing import Dict, Any
import logging
from agentic_notify.adapters.base import BaseAdapter

logger = logging.getLogger(__name__)

class MockReminderAdapter(BaseAdapter):
    """
    A mock adapter to simulate creating a reminder on a user's device.
    """
    @property
    def name(self) -> str:
        return "create_reminder"

    async def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"*** Action Executed: MockReminderAdapter received {payload} ***")
        return {"status": "success", "reminder_id": "rem_test_001", "echo_payload": payload}
