import asyncio
import json
import logging
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agentic_notify.orchestrator import NotificationOrchestrator
from agentic_notify.storage.memory import InMemoryStore
from agentic_notify.adapters.mock_reminder import MockReminderAdapter
from agentic_notify.adapters.notes import NotesAdapter
from agentic_notify.adapters.webhook import WebhookAdapter

from agentic_notify.schemas.workflow import WorkflowDefinition, WorkflowTrigger, WorkflowStep

# Make logging quiet for a cleaner presentation, except for our adapters/orchestrator
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.getLogger().setLevel(logging.INFO)

async def run_e2e_sample():
    print("\n" + "="*60)
    print("🚀 STARTING E2E SAMPLE OF AGENTIC-NOTIFY LIBRARY")
    print("="*60 + "\n")

    # 1. Initialize the Core system
    print("[1] Initializing Orchestrator & InMemory Storage...")
    storage = InMemoryStore()
    orchestrator = NotificationOrchestrator(storage=storage)

    # 2. Register real-world actions (Adapters)
    print("[2] Registering Device Adapters (Notes, Reminders, Webhooks)...")
    orchestrator.register_adapter(NotesAdapter())
    orchestrator.register_adapter(MockReminderAdapter())
    orchestrator.register_adapter(WebhookAdapter())

    # 3. Create a complex Multi-Step Workflow
    print("[3] Building a multi-step Workflow Graph...")
    workflow = WorkflowDefinition(
        workflow_id="wf_e2e_demo",
        workflow_name="E2E Notification Handler",
        description="Saves a note, sets a reminder, and fires a webhook.",
        trigger=WorkflowTrigger(type="notification"),
        steps=[
            WorkflowStep(
                id="step_save_note",
                kind="adapter",
                name="save_note",
                input_from={
                    "title": "event.title",
                    "content": "event.body"
                }
            ),
            WorkflowStep(
                id="step_create_reminder",
                kind="adapter",
                name="create_reminder",
                input_from={
                    "task_title": "event.title",
                    "task_text": "event.body"  
                }
            ),
            WorkflowStep(
                id="step_fire_webhook",
                kind="adapter",
                name="trigger_webhook",
                input_from={
                    "url": "https://httpbin.org/post", 
                    "data": {
                        "message": "Notification successfully processed by Agentic-Notify!",
                        "event_title": "event.title"
                    }
                }
            )
        ]
    )
    orchestrator.register_workflow(workflow)

    # 4. Tell the Router Engine to funnel matching events to this workflow
    print("[4] Configuring Routing Engine...")
    orchestrator.router.add_rule(lambda event: "demo" in str(event.metadata).lower() or True, "wf_e2e_demo")

    # 5. Create a mock Notification from a device
    print("\n[5] Simulating Incoming Device Notification payload:")
    mock_payload = {
        "event_id": "evt_demo_001",
        "source_platform": "ios",
        "source_app": "finance_app",
        "title": "Unusual Charge Detected",
        "body": "A charge of $500.00 was detected on your credit card. Please review.",
        "received_at": "2026-03-28T12:00:00Z",
        "metadata": {"type": "demo_alert", "severity": "high"}
    }
    print(json.dumps(mock_payload, indent=2))
    print("\n" + "-"*60 + "\n")

    # 6. Execute!
    print("⏩ PROCESSING EVENT THROUGH ORCHESTRATOR...\n")
    result = await orchestrator.process_event(mock_payload)

    # 7. Print Results
    print("\n" + "="*60)
    print("✅ EXECUTION COMPLETE! FINAL RESULT:")
    print("="*60)
    print(json.dumps(result, indent=2))

    # Pull the detailed trace strictly from the Storage Layer
    run_trace = await storage.get_workflow_run(result["run_id"])
    print("\n🔍 DETAILED EXECUTION TRACE (from Memory Storage):")
    print(json.dumps(run_trace, indent=2))
    
    print("\n🎉 Sample Application Finished successfully!")

if __name__ == "__main__":
    asyncio.run(run_e2e_sample())
