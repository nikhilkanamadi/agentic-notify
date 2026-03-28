from typing import Dict, Any, Optional, Callable, Tuple, List
from agentic_notify.schemas.notification import NotificationEvent

class RoutingEngine:
    """
    Determines which workflow to trigger based on the incoming NotificationEvent.
    """
    def __init__(self):
        # List of (rule_function, workflow_id)
        self.rules: List[Tuple[Callable[[NotificationEvent], bool], str]] = []

    def add_rule(self, rule_fn: Callable[[NotificationEvent], bool], workflow_id: str):
        """Add a simple deterministic rule."""
        self.rules.append((rule_fn, workflow_id))

    def route(self, event: NotificationEvent) -> Optional[str]:
        """Returns the matched workflow_id, or None if no match."""
        for rule_fn, workflow_id in self.rules:
            if rule_fn(event):
                return workflow_id
        return None
