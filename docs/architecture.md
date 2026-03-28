# The Architecture

Agentic-Notify is built on a highly decoupled architecture designed to keep the "Brain" separate from the "Hands." The system operates sequentially through four distinct lifecycle phases.

---

## 🏗️ 1. Ingestion & Normalization
The system is entirely agnostic to where a notification originates.
*   Whether it's an iOS push notification, a webhook from GitHub, or a background Android worker, events hit the **Integration Layer** (e.g. `FastAPIIntegration`).
*   The raw payload is immediately cast into the strict `NotificationEvent` Pydantic schema, normalizing keys like `body` and `source_platform` so the orchestrator only deals with a unified data structure.

## 🧠 2. Routing & Planning (The Brain)
Once normalized, the event must be mapped to a workflow.
*   **Deterministic Routing:** The `RoutingEngine` can trigger pre-saved workflows based on simple lambda rules (`if "urgent" in body -> wf_123`).
*   **Agentic Planning:** If there's no set rule, the `AgenticPlanner` takes over. It feeds the notification and the `ToolRegistry` to an LLM (e.g., GPT-4o). The LLM autonomously drafts a multi-step `WorkflowDefinition` execution graph and passes it through strict Pydantic JSON validation to prevent hallucinations.

## 🛡️ 3. Safety & Policy
Before the Orchestrator starts the engine, the event hits the `PolicyEngine`.
*   This middleware evaluates dynamic user preferences and boundaries pulled from databases. For example, it ensures a VIP account's notification isn't accidentally deleted, halting execution instantly if a rule is violated.

## ⚙️ 4. The Executor (The Hands)
Instead of hardcoded script executions, the `WorkflowExecutor` runs an asynchronous state-machine.
*   It iterates step-by-step through the `WorkflowDefinition` graph. 
*   It dynamically injects arguments (e.g., mapping `"event.body"` into `"task_text"`).
*   If it encounters an `ApprovalHandler`, the engine gracefully suspends state, saves the entire memory to the `PostgresStore`, and halts until human authorization resumes it.
*   Once authorized, it delegates execution to physical **Adapters** (like APIs or Databases) to invoke actual change in the real world.
