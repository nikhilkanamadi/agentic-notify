import asyncio
import json
import logging
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agentic_notify.examples.app import orchestrator
from agentic_notify.tools.registry import ToolRegistry, ToolSchema
from agentic_notify.planning.planner import AgenticPlanner

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.getLogger().setLevel(logging.INFO)

async def test_agentic_planning():
    print("========================================")
    print("PHASE 4: AGENTIC PLANNING & EXECUTION TEST")
    print("========================================\n")

    # 1. Setup the Tool Registry for the LLM
    registry = ToolRegistry()
    registry.register_tool(ToolSchema(
        name="create_reminder",
        description="Creates a native reminder based on inputs.",
        input_schema={"type": "object", "properties": {"task_text": {"type": "string"}, "task_title": {"type": "string"}}},
        idempotent=True
    ))

    # 2. Invoke the LLM Planner
    planner = AgenticPlanner(tool_registry=registry)
    intent = "Whenever I get a Gmail notification about an interview, create a reminder so I don't forget it!"
    
    print(f"USER INTENT: '{intent}'\n")
    
    workflow_def = await planner.plan_workflow(intent=intent)
    
    print("\n[LLM Generated Workflow]")
    print(json.dumps(workflow_def.model_dump(), indent=2))
    
    # 3. Register the newly generated workflow to the Orchestrator
    orchestrator.register_workflow(workflow_def)
    
    # Update our Routing Rule to route to this new LLM-generated workflow
    orchestrator.router.rules.clear() # clear the MVP stub
    orchestrator.router.add_rule(lambda e: "interview" in (e.body or "").lower(), workflow_def.workflow_id)

    # 4. Supply a matching raw event to see it run end-to-end
    mock_payload = {
        "event_id": "evt_llm_test_99",
        "source_platform": "android",
        "source_app": "gmail",
        "title": "Interview Link Enclosed",
        "body": "Hey there, you have an interview tomorrow at noon. Be ready!",
        "received_at": "2026-03-29T12:00:00Z"
    }
    
    print("\n[Firing Event into Orchestrator]")
    result = await orchestrator.process_event(mock_payload)
    
    print("\n[Final Execution Result]")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(test_agentic_planning())
