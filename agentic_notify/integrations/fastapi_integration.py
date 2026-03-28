from fastapi import FastAPI, Request
from typing import Any, Dict
from agentic_notify.integrations.base import BaseIntegration
import logging

logger = logging.getLogger(__name__)

class FastAPIIntegration(BaseIntegration):
    """
    Exposes a REST API endpoint for ingesting notification events.
    Requires FastAPI to be installed and passed in.
    """
    def __init__(self, orchestrator, app: FastAPI):
        self.orchestrator = orchestrator
        self.app = app
        self._register_routes()

    def _register_routes(self):
        @self.app.post("/events/ingest")
        async def ingest_event(request: Request):
            payload = await request.json()
            logger.info("FastAPI received event payload")
            result = await self.orchestrator.process_event(payload)
            return result

    async def start(self) -> None:
        logger.info("FastAPIIntegration started (managed by external uvicorn/asgi)")

    def stop(self) -> None:
        pass
