from typing import Dict, Any
import logging
from agentic_notify.adapters.base import BaseAdapter

logger = logging.getLogger(__name__)

class NotesAdapter(BaseAdapter):
    """
    Simulates saving content to a local notes app or document store.
    """
    @property
    def name(self) -> str:
        return "save_note"

    async def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        title = payload.get("title", "Untitled Note")
        content = payload.get("content", "")
        
        logger.info(f"Action Executed: Saved Note => Title: '{title}', Content Length: {len(content)}")
        
        return {
            "status": "success",
            "note_id": "note_1001",
            "saved_title": title
        }
