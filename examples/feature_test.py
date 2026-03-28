import asyncio
import json
import logging
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agentic_notify.orchestrator import NotificationOrchestrator
from agentic_notify.storage.postgres import PostgresStore
from agentic_notify.handlers.approval import ApprovalHandler
from agentic_notify.adapters.webhook import WebhookAdapter
from agentic_notify.policies.engine import PolicyEngine
from agentic_notify.schemas.workflow import WorkflowDefinition, WorkflowTrigger, WorkflowStep

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.getLogger().setLevel(logging.INFO)

async def test_features():
    print("============================================================")
    print(" TESTING ADVANCED ENTERPRISE SCOPE FEATURES ")
    print("============================================================\n")

    # 1. Initialize Postgres-backed Store
    print("[Feature 1] Initializing Durable Postgres Storage...")
    storage = PostgresStore(connection_pool=None)
    
    # 2. Dynamic Policy Engine
    print("[Feature 2] Enforcing Dynamic User-level Database Policies...")
    policy_engine = PolicyEngine()
    
    orchestrator = NotificationOrchestrator(storage=storage, policy_engine=policy_engine)
    orchestrator.register_adapter(WebhookAdapter())
    orchestrator.register_handler(ApprovalHandler())

    # 3. Create a Human-in-the-Loop workflow
    workflow = WorkflowDefinition(
        workflow_id="wf_approve_payment",
        workflow_name="High Value Payment Auth",
        trigger=WorkflowTrigger(type="notification"),
        steps=[
            WorkflowStep(
                id="step_require_approval",
                kind="handler",
                name="request_human_approval",
                input_from={"reason": "Transfer over $1000 requires explicit user authentication.", "action_payload": {"amount": 5000}}
            ),
            WorkflowStep(
                id="step_execute_payment",
                kind="adapter",
                name="trigger_webhook",
                input_from={"url": "https://httpbin.org/post", "data": {"status": "paid"}}
            )
        ]
    )
    orchestrator.register_workflow(workflow)
    orchestrator.router.add_rule(lambda e: True, "wf_approve_payment")

    # 4. Fire the event!
    print("\n[Feature 3] Injecting High-Risk Workflow that requires Human-In-The-Loop...")
    mock_payload = {
        "event_id": "evt_txn_88",
        "source_platform": "banking_app",
        "source_app": "finance",
        "title": "Wire Transfer Requested",
        "body": "Send $5000 to John Doe",
        "received_at": "2026-03-28T12:00:00Z",
        "metadata": {"user_id": "investor_account_1"}
    }
    
    result = await orchestrator.process_event(mock_payload)
    
    print("\n============================================================")
    print("FINAL ORCHESTRATOR RESPONSE (Note the 'suspended' status)")
    print("============================================================")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(test_features())
