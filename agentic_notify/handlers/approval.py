from typing import Dict, Any, List
import logging
from agentic_notify.handlers.base import BaseHandler
from agentic_notify.schemas.notification import NotificationEvent

logger = logging.getLogger(__name__)

class ApprovalHandler(BaseHandler):
    """
    Human-in-the-Loop Handler. 
    When a workflow executes this step, it halts execution and returns 'awaiting_approval'.
    The orchestrator pauses the run state until a human explicitly resumes it.
    """
    @property
    def name(self) -> str:
        return "request_human_approval"

    async def handle(self, event: NotificationEvent, context: Dict[str, Any]) -> Dict[str, Any]:
        reason = context.get("reason", "Action requires explicit user approval.")
        action_payload = context.get("action_payload", {})
        
        logger.info(f"⏸️ WORKFLOW HALTED: Requesting Human Approval for: {reason}")
        
        # In a real system, you would trigger an outbound push notification or email here
        # telling the user to click an "Approve" button.
        
        return {
            "status": "awaiting_approval",
            "approval_ticket_id": f"ticket_{event.event_id}",
            "reason": reason,
            "pending_action": action_payload
        }
