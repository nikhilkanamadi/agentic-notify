import pytest
from agentic_notify.orchestrator import NotificationOrchestrator
from agentic_notify.storage.memory import InMemoryStore
from agentic_notify.adapters.base import BaseAdapter
from agentic_notify.schemas.workflow import WorkflowDefinition, WorkflowTrigger, WorkflowStep

class DummyAdapter(BaseAdapter):
    @property
    def name(self) -> str:
        return "dummy_action"
        
    async def execute(self, payload: dict) -> dict:
        return {"status": "success"}


@pytest.mark.asyncio
async def test_orchestrator_initialization():
    store = InMemoryStore()
    orchestrator = NotificationOrchestrator(storage=store)
    
    assert orchestrator.storage is store
    assert len(orchestrator.adapters) == 0

@pytest.mark.asyncio
async def test_adapter_registration():
    store = InMemoryStore()
    orchestrator = NotificationOrchestrator(storage=store)
    
    adapter = DummyAdapter()
    orchestrator.register_adapter(adapter)
    
    assert "dummy_action" in orchestrator.adapters
    assert orchestrator.adapters["dummy_action"] is adapter

@pytest.mark.asyncio
async def test_workflow_execution():
    store = InMemoryStore()
    orchestrator = NotificationOrchestrator(storage=store)
    orchestrator.register_adapter(DummyAdapter())
    
    workflow = WorkflowDefinition(
        workflow_id="wf_dummy",
        workflow_name="Dummy Workflow",
        trigger=WorkflowTrigger(type="notification"),
        steps=[
            WorkflowStep(
                id="step_1",
                kind="adapter",
                name="dummy_action",
                input_from={}
            )
        ]
    )
    
    orchestrator.register_workflow(workflow)
    orchestrator.router.add_rule(lambda e: e.title == "test", "wf_dummy")
    
    mock_payload = {
        "event_id": "evt_test",
        "source_platform": "ios",
        "source_app": "testing",
        "title": "test",
        "received_at": "2026-03-28T12:00:00Z"
    }
    
    result = await orchestrator.process_event(mock_payload)
    
    assert result["run_status"] == "success"
    assert result["workflow_id"] == "wf_dummy"
