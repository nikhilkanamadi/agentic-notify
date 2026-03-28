from typing import Dict, Any
import logging
import json
import urllib.request
import urllib.error
from agentic_notify.adapters.base import BaseAdapter

logger = logging.getLogger(__name__)

class WebhookAdapter(BaseAdapter):
    """
    Adapter that fires an HTTP POST to an external webhook URL.
    """
    @property
    def name(self) -> str:
        return "trigger_webhook"

    async def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = payload.get("url")
        data = payload.get("data", {})
        
        if not url:
            raise ValueError("WebhookAdapter requires a 'url' in the payload.")
            
        logger.info(f"Action Executed: Firing Webhook to {url}")
        
        req = urllib.request.Request(
            url, 
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        try:
            # Note: Minimal blocking sync call for demonstration.
            # In production asyncio, use aiohttp or httpx.
            with urllib.request.urlopen(req, timeout=10) as response:
                return {
                    "status": "success",
                    "http_code": response.getcode()
                }
        except urllib.error.URLError as e:
            logger.error(f"Webhook failed: {e}")
            raise RuntimeError(f"Webhook call failed: {e}")
