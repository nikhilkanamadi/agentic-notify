import uuid
import logging
from typing import Any, Dict, Optional

from agentic_notify.adapters.base import BaseAdapter
from agentic_notify.handlers.base import BaseHandler
from agentic_notify.schemas.notification import NotificationEvent
from agentic_notify.schemas.workflow import WorkflowDefinition
from agentic_notify.schemas.result import WorkflowRunResult
from agentic_notify.storage.base import BaseStorage
from agentic_notify.routing.engine import RoutingEngine
from agentic_notify.workflows.engine import WorkflowExecutor
from agentic_notify.policies.engine import PolicyEngine

logger = logging.getLogger(__name__)

class NotificationOrchestrator:
    """
    The main coordinator. Receives events, routes them to workflows, 
    evaluates policies, and delegates execution.
    """
    def __init__(
        self,
        storage: BaseStorage,
        router: Optional[RoutingEngine] = None,
        policy_engine: Optional[PolicyEngine] = None,
        executor: Optional[WorkflowExecutor] = None,
    ):
        self.storage = storage
        self.router = router or RoutingEngine()
        self.policy_engine = policy_engine or PolicyEngine()
        self.executor = executor or WorkflowExecutor(storage=self.storage)
        
        self.adapters: Dict[str, BaseAdapter] = {}
        self.handlers: Dict[str, BaseHandler] = {}
        self.workflows: Dict[str, WorkflowDefinition] = {}

    def register_adapter(self, adapter: BaseAdapter) -> None:
        self.adapters[adapter.name] = adapter
        logger.info(f"Registered adapter: {adapter.name}")

    def register_handler(self, handler: BaseHandler) -> None:
        self.handlers[handler.name] = handler
        logger.info(f"Registered handler: {handler.name}")

    def register_workflow(self, workflow: WorkflowDefinition) -> None:
        self.workflows[workflow.workflow_id] = workflow
        logger.info(f"Registered workflow: {workflow.workflow_id} ({workflow.workflow_name})")

    async def process_event(self, raw_event_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        1. Normalize raw event
        2. Route
        3. Execute workflow steps sequentially
        """
        # 1. Normalize
        try:
            event = NotificationEvent(**raw_event_payload)
        except Exception as e:
            logger.error(f"Event normalization failed: {e}")
            return {"status": "error", "message": "Invalid event schema.", "details": str(e)}
            
        logger.info(f"Normalized event: {event.event_id}")

        # 2. Route
        workflow_id = self.router.route(event)
        if not workflow_id or workflow_id not in self.workflows:
            msg = f"No workflow matched or found for event {event.event_id}"
            logger.info(msg)
            return {"status": "ignored", "message": msg}
            
        workflow = self.workflows[workflow_id]
        
        # 3. Policy Execution Check
        if not self.policy_engine.evaluate("start_workflow", {"workflow_id": workflow_id}, {"event": event.model_dump()}):
            logger.warning(f"Policy denied workflow {workflow_id}")
            return {"status": "denied", "message": "Policy check failed."}

        # 4. Execute
        run_id = f"run_{uuid.uuid4().hex}"
        logger.info(f"Delegating execution for {workflow_id} as run {run_id}")
        
        result: WorkflowRunResult = await self.executor.execute(
            run_id=run_id,
            workflow=workflow,
            event=event,
            adapters=self.adapters,
            handlers=self.handlers
        )
        
        return {
            "status": "processed", 
            "run_id": run_id, 
            "workflow_id": workflow_id,
            "run_status": result.status
        }
