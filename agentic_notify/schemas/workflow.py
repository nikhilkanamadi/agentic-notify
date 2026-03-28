from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict

class WorkflowStep(BaseModel):
    """
    A single step in the workflow graph.
    Can either trigger an internal handler or call an external tool adapter.
    """
    id: str
    kind: str  # typically "tool" or "handler"
    name: str  # e.g., "summarize_text", "create_reminder"
    depends_on: List[str] = []
    input_from: Dict[str, Any] = {}
    timeout_ms: int = 15000
    retry_limit: int = 2

class WorkflowTrigger(BaseModel):
    """
    Conditions describing how a workflow should be triggered.
    """
    type: str  # e.g., "schedule", "notification", "event"
    schedule: Optional[str] = None
    event_pattern: Optional[Dict[str, Any]] = None

class WorkflowDefinition(BaseModel):
    """
    A deterministic, structured execution graph for an agentic workflow.
    """
    model_config = ConfigDict(extra="allow")
    
    workflow_id: str
    workflow_name: str
    description: Optional[str] = None
    enabled: bool = True
    trigger: WorkflowTrigger
    steps: List[WorkflowStep]
