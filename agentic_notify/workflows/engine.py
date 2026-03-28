import logging
from typing import Dict, Any
from datetime import datetime
import time

from agentic_notify.schemas.notification import NotificationEvent
from agentic_notify.schemas.workflow import WorkflowDefinition
from agentic_notify.schemas.result import WorkflowRunResult, StepResult
from agentic_notify.adapters.base import BaseAdapter
from agentic_notify.handlers.base import BaseHandler
from agentic_notify.storage.base import BaseStorage

logger = logging.getLogger(__name__)

class WorkflowExecutor:
    """
    Iterates over workflow steps and invokes the appropriate handler or adapter,
    capable of suspending state for Human-in-the-Loop approvals.
    """
    def __init__(self, storage: BaseStorage):
        self.storage = storage

    async def execute(
        self,
        run_id: str,
        workflow: WorkflowDefinition,
        event: NotificationEvent,
        adapters: Dict[str, BaseAdapter],
        handlers: Dict[str, BaseHandler],
        resume_from_step: str = None
    ) -> WorkflowRunResult:
        
        logger.info(f"Starting/Resuming run {run_id} for workflow {workflow.workflow_id}")
        # In a real durable engine, we would fetch existing step_results from DB here if resuming.
        step_results: Dict[str, StepResult] = {}
        context = {"event": event.model_dump(), "steps": {}}

        run_status = "success"

        for step in workflow.steps:
            # Skip steps already executed if we are resuming from an approval
            if resume_from_step and step.id != resume_from_step:
                continue
            elif resume_from_step and step.id == resume_from_step:
                resume_from_step = None # We caught up

            start_time = time.time()
            started_at = datetime.utcnow().isoformat()
            
            try:
                # Resolve inputs mapping
                step_input = {}
                for in_key, in_val in step.input_from.items():
                    if isinstance(in_val, str) and "." in in_val:
                        parts = in_val.split(".", 1)
                        if parts[0] in context["steps"]:
                            step_input[in_key] = context["steps"][parts[0]].get(parts[1])
                        elif parts[0] == "event":
                            step_input[in_key] = context["event"].get(parts[1])
                        else:
                            step_input[in_key] = in_val
                    else:
                        step_input[in_key] = in_val
                
                # Execute step
                output = None
                if step.kind == "adapter":
                    if step.name not in adapters:
                        raise ValueError(f"Adapter '{step.name}' not registered.")
                    output = await adapters[step.name].execute(step_input)
                elif step.kind == "handler":
                    if step.name not in handlers:
                        raise ValueError(f"Handler '{step.name}' not registered.")
                    output = await handlers[step.name].handle(event, step_input) # Pass resolved input
                else:
                    raise ValueError(f"Unknown step kind '{step.kind}'")
                
                context["steps"][step.id] = output
                
                # Handle Human-in-the-loop interruption
                if output and output.get("status") == "awaiting_approval":
                    latency = int((time.time() - start_time) * 1000)
                    step_result = StepResult(
                        status="awaiting_approval",
                        output=output,
                        started_at=started_at,
                        ended_at=datetime.utcnow().isoformat(),
                        latency_ms=latency
                    )
                    step_results[step.id] = step_result
                    run_status = "suspended"
                    break # Halt execution graph immediately
                
                latency = int((time.time() - start_time) * 1000)
                step_result = StepResult(
                    status="success",
                    output=output,
                    started_at=started_at,
                    ended_at=datetime.utcnow().isoformat(),
                    latency_ms=latency
                )
                
            except Exception as e:
                logger.error(f"Step {step.id} failed: {e}")
                latency = int((time.time() - start_time) * 1000)
                step_result = StepResult(
                    status="failed",
                    error={"message": str(e)},
                    started_at=started_at,
                    ended_at=datetime.utcnow().isoformat(),
                    latency_ms=latency
                )
                step_results[step.id] = step_result
                run_status = "failed"
                break

            step_results[step.id] = step_result

        run_result = WorkflowRunResult(
            run_id=run_id,
            workflow_id=workflow.workflow_id,
            status=run_status,
            step_results=step_results
        )
        
        # Persist State explicitly so it can be resumed later if 'suspended'
        await self.storage.save_workflow_run(run_id, run_result.model_dump())
        return run_result
