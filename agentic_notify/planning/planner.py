import json
import uuid
import logging
from typing import Dict, Any, Optional

from agentic_notify.schemas.workflow import WorkflowDefinition, WorkflowStep
from agentic_notify.tools.registry import ToolRegistry
from agentic_notify.planning.prompts import SYSTEM_PLANNER_PROMPT

logger = logging.getLogger(__name__)

class AgenticPlanner:
    """
    Converts natural language user intents into structured WorkflowDefinition schemas.
    """
    def __init__(self, tool_registry: ToolRegistry, llm_client: Optional[Any] = None):
        self.tool_registry = tool_registry
        self.llm_client = llm_client

    async def plan_workflow(self, intent: str, trigger_type: str = "notification") -> WorkflowDefinition:
        """
        Executes a prompt to an LLM to generate the JSON graph, then strictly validates it 
        through the Pydantic definition.
        """
        tools = json.dumps(self.tool_registry.get_all_tool_schemas(), indent=2)
        system_prompt = SYSTEM_PLANNER_PROMPT.format(tools=tools)
        
        logger.info(f"Generating plan for intent: '{intent}' utilizing registered tools.")
        
        # Real-world behavior: Wait for LLM
        # response_text = await self.llm_client.chat(messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": intent}])
        
        # Mocked deterministic response for Phase 4 proof-of-concept
        mock_generated_plan = {
            "workflow_id": f"wf_llm_{uuid.uuid4().hex[:8]}",
            "workflow_name": "Generated LLM Plan",
            "description": f"Automated workflow for: {intent}",
            "enabled": True,
            "trigger": {
                "type": trigger_type
            },
            "steps": [
                {
                    "id": "step_create_reminder",
                    "kind": "adapter",
                    "name": "create_reminder",
                    "input_from": {
                        "task_text": "event.body",
                        "task_title": "event.title"
                    }
                }
            ]
        }
        
        try:
            # The most crucial step of the backend design: 
            # Force the untrusted LLM payload through the strict Pydantic `WorkflowDefinition` validator.
            workflow = WorkflowDefinition(**mock_generated_plan)
            logger.info(f"Successfully validated LLM plan into WorkflowDefinition: {workflow.workflow_id}")
            return workflow
        except Exception as e:
            logger.error(f"LLM produced invalid workflow schema! Planning failed: {e}")
            raise ValueError(f"Planner failed schema validation: {e}")
