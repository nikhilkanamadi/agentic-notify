from typing import Dict, Any, List
from pydantic import BaseModel

class ToolSchema(BaseModel):
    """
    Metadata representation of an Adapter or Handler.
    This is what the LLM planner sees to know what actions it can take.
    """
    name: str
    description: str
    input_schema: Dict[str, Any]
    idempotent: bool
    sensitivity: str = "low"

class ToolRegistry:
    """Holds metadata for all registered actions globally."""
    def __init__(self):
        self._tools: Dict[str, ToolSchema] = {}

    def register_tool(self, schema: ToolSchema):
        self._tools[schema.name] = schema

    def get_all_tool_schemas(self) -> List[Dict[str, Any]]:
        return [t.model_dump() for t in self._tools.values()]
