import logging
from fastapi import FastAPI

from agentic_notify.orchestrator import NotificationOrchestrator
from agentic_notify.storage.memory import InMemoryStore
from agentic_notify.integrations.fastapi_integration import FastAPIIntegration
from agentic_notify.adapters.mock_reminder import MockReminderAdapter
from agentic_notify.schemas.workflow import WorkflowDefinition, WorkflowTrigger, WorkflowStep

logging.basicConfig(level=logging.INFO)

# 1. Setup Core dependencies
storage = InMemoryStore()

# 2. Setup Orchestrator
orchestrator = NotificationOrchestrator(storage=storage)

# 3. Register our mock adapter
orchestrator.register_adapter(MockReminderAdapter())

# 4. Define and Register Workflow
workflow = WorkflowDefinition(
    workflow_id="wf_important_reminders",
    workflow_name="Important Notification Reminders",
    trigger=WorkflowTrigger(type="notification"),
    steps=[
        WorkflowStep(
            id="step_create_reminder",
            kind="adapter",
            name="create_reminder",
            # We map the inputs using standard dot notation to pull from the normalized event
            input_from={
                "task_text": "event.body", 
                "task_title": "event.title"
            }
        )
    ]
)
orchestrator.register_workflow(workflow)

# 5. Add deterministic routing rule (Route all events to our test workflow)
orchestrator.router.add_rule(lambda e: True, "wf_important_reminders")

# 6. Initialize FastAPI Integration
app = FastAPI()
integration = FastAPIIntegration(orchestrator, app)

# To run this example locally:
# python -m uvicorn agentic_notify.examples.app:app --reload
