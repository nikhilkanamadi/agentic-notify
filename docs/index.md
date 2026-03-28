# 🚀 Welcome to Agentic-Notify

**Agentic-Notify** is an open-source Python SDK for building agentic, notification-driven workflows. It acts as an autonomous orchestration layer that intercepts mobile or web notifications, plans multi-step actions using Large Language Models (LLMs), and executes them deterministically using strict Pydantic schemas.

---

## ⚡ The Problem It Solves

Traditional notification systems (like Firebase Cloud Messaging or APNs) are simple delivery pipes. They push a string to your phone, and you must manually open the app to take action.

**Agentic-Notify** transforms notifications into autonomous workflows. Instead of just displaying "Your flight is delayed," the engine intercepts the notification, uses a Dynamic Policy Engine to check your preferences, queries an LLM Planner, and executes a multi-step workflow (e.g., *canceling your Uber, emailing your boss, and setting a native reminder*).

---

## 📦 Installation

To install the library and the optional backend engine (FastAPI):

```bash
pip install agentic-notify[fastapi]
```

---

## 🛠️ Quick Start Guide

The easiest way to understand the architecture is to see it run end-to-end. The library is completely modular. You initialize the Orchestrator, register your Adapters (tools), and define the Workflow JSON graph.

### 1. Initialize the Engine
```python
import asyncio
from agentic_notify.orchestrator import NotificationOrchestrator
from agentic_notify.storage.memory import InMemoryStore
from agentic_notify.policies.engine import PolicyEngine

storage = InMemoryStore()
policy_engine = PolicyEngine()
orchestrator = NotificationOrchestrator(storage=storage, policy_engine=policy_engine)
```

### 2. Register Your Adapters (Tools)
Adapters are standard python classes that execute real-world logic.

```python
from agentic_notify.adapters.notes import NotesAdapter
from agentic_notify.adapters.mock_reminder import MockReminderAdapter

orchestrator.register_adapter(NotesAdapter())
orchestrator.register_adapter(MockReminderAdapter())
```

### 3. Define the Agentic Workflow
Using strict Pydantic models, define the graph that the LLM or Routing Engine will follow.

```python
from agentic_notify.schemas.workflow import WorkflowDefinition, WorkflowTrigger, WorkflowStep

workflow = WorkflowDefinition(
    workflow_id="wf_e2e_demo",
    workflow_name="E2E Notification Handler",
    trigger=WorkflowTrigger(type="notification"),
    steps=[
        WorkflowStep(
            id="step_save_note",
            kind="adapter",
            name="save_note",
            input_from={"title": "event.title", "content": "event.body"}
        ),
        WorkflowStep(
            id="step_create_reminder",
            kind="adapter",
            name="create_reminder",
            input_from={"task_title": "event.title", "task_text": "event.body"}
        )
    ]
)

orchestrator.register_workflow(workflow)

# Route incoming events with a specific keyword to this workflow
orchestrator.router.add_rule(lambda event: "charge" in str(event.title).lower(), "wf_e2e_demo")
```

### 4. Inject a Mock Notification Event
The orchestrator converts raw device payloads into unified `NotificationEvent` schemas.

```python
mock_payload = {
    "event_id": "evt_demo_001",
    "source_platform": "ios",
    "title": "Unusual Charge Detected",
    "body": "A charge of $500.00 was detected. Please review."
}

async def run():
    result = await orchestrator.process_event(mock_payload)
    print(result)

asyncio.run(run())
```

---

## 🧠 Advanced Features Included

*   **Pydantic Data Contracts:** Zero LLM hallucinations. The engine forces Agentic output into strict JSON schema validation locks.
*   **Human-in-the-Loop Hooks:** The `ApprovalHandler` safely halts execution on high-risk actions (like payments) and suspends state until human authorization is granted.
*   **Durable Postgres Storage:** Fully tracks all state execution securely by `tenant_id` for resumable, safe workflows.
*   **Dynamic Policy Engine:** A middleware barrier that checks dynamic user-profiles and boundaries *before* any action is ever triggered.
