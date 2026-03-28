# API Reference

While Agentic-Notify exposes many sub-modules, these are the core classes you will interact with while building your orchestration pipelines.

---

## `NotificationOrchestrator`
The central coordinator class (`agentic_notify.orchestrator`). It manages the registration of Adapters, Handlers, and Workflows, and exposes the primary event processing loop.

*   `register_adapter(adapter: BaseAdapter)`: Mounts an external tool for execution.
*   `register_handler(handler: BaseHandler)`: Mounts an internal logic handler (like Human-in-the-loop).
*   `register_workflow(workflow: WorkflowDefinition)`: Stores a static execution graph.
*   `async process_event(raw_payload: Dict[str, Any]) -> Dict[str, Any]`: The main ingestion pipe. Accepts an unstructured dictionary, norms it, and executes the lifecycle.

---

## `AgenticPlanner`
The LLM integration bridge (`agentic_notify.planning.planner`). It generates multi-step workflows dynamically.

*   `async plan_workflow(intent: str) -> WorkflowDefinition`: Takes a natural language string, prompts the LLM alongside the loaded `ToolRegistry`, and strictly attempts to validate the returned JSON string into a Pydantic `WorkflowDefinition` model.

---

## `NotificationEvent`
The canonical data model for all inbound signals (`agentic_notify.schemas.notification`).

```python
class NotificationEvent(BaseModel):
    event_id: str
    source_platform: str
    source_app: str
    title: Optional[str] = None
    body: Optional[str] = None
    received_at: datetime
    metadata: Dict[str, Any] = {}
```

---

## `WorkflowDefinition`
The Pydantic schema mapping the Execution Graph (`agentic_notify.schemas.workflow`).

```python
class WorkflowDefinition(BaseModel):
    workflow_id: str
    workflow_name: str
    steps: List[WorkflowStep]
```

*   `WorkflowStep`: The core state-block defining how standard data inputs map to an Adapter's expected arguments. Features `id`, `kind`, `name`, and `input_from` mappings.
