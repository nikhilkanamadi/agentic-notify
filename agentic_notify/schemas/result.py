from pydantic import BaseModel
from typing import Any, Dict, Optional

class StepResult(BaseModel):
    """Result of a single workflow step execution."""
    status: str  # "success", "failed", "awaiting_approval"
    output: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    started_at: str
    ended_at: str
    latency_ms: int

class WorkflowRunResult(BaseModel):
    """Result of an entire workflow execution."""
    run_id: str
    workflow_id: str
    status: str
    step_results: Dict[str, StepResult]
