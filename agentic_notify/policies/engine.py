from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class PolicyEngine:
    """
    Dynamically evaluates risk and permissions by checking user-configured boundaries
    before an action or workflow is allowed to fire.
    """
    def __init__(self):
        # In production, this would query a DB or a Vector Redis cache per user.
        self.user_restrictions: Dict[str, List[str]] = {
            "default_user": ["never_auto_delete", "never_silence_bank"],
            "vip_mode": ["disable_all_summarization"]
        }

    def evaluate(self, action: str, payload: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """
        Check if an action is allowed based on user restrictions and global rules.
        """
        user_id = context.get("event", {}).get("metadata", {}).get("user_id", "default_user")
        restrictions = self.user_restrictions.get(user_id, [])

        logger.info(f"Evaluating Policy: action '{action}' for user '{user_id}'")

        if action == "summarize" and "disable_all_summarization" in restrictions:
            logger.warning(f"POLICY BLOCK: User {user_id} has disabled AI summarization.")
            return False
            
        if action == "delete_email" and "never_auto_delete" in restrictions:
            logger.warning(f"POLICY BLOCK: User {user_id} has forbidden auto-deletion.")
            return False

        return True
