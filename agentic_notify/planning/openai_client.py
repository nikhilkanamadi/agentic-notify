import json
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class OpenAIPlannerClient:
    """
    A concrete client wrapper for OpenAI's API to be used by the AgenticPlanner.
    Requires `openai` package to be installed.
    """
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        try:
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(api_key=api_key)
            self.model = model
            logger.info(f"Initialized OpenAIPlannerClient with model: {self.model}")
        except ImportError:
            raise ImportError("Please install openai package: `pip install openai`")

    async def chat(self, system_prompt: str, user_intent: str) -> Dict[str, Any]:
        """
        Sends the prompt to OpenAI and expects a JSON response constrained to the 
        WorkflowDefinition schema.
        """
        logger.info("Calling OpenAI API for workflow generation...")
        
        try:
            # Using response_format={ "type": "json_object" } perfectly aligns with 
            # our Pydantic validation boundary.
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_intent}
                ],
                response_format={"type": "json_object"},
                temperature=0.2, # Low temperature for deterministic planning
            )
            
            content = response.choices[0].message.content
            if not content:
                raise ValueError("OpenAI returned an empty response.")
                
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise
