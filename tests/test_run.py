import asyncio
import json
import logging
import sys

# Add current directory to path so testing works without pip installing
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agentic_notify.examples.app import orchestrator

# Ensure logging is routed to stdout
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.getLogger().setLevel(logging.INFO)

async def test_workflow():
    payload = {
        "event_id": "evt_test_01",
        "source_platform": "android",
        "source_app": "gmail",
        "title": "Interview in 30 mins",
        "body": "Don't forget your interview at 10:30 AM! Please prepare.",
        "received_at": "2026-03-28T10:00:00Z",
        "priority_hint": "unknown",
        "metadata": {}
    }

    print("========================================")
    print("SENDING MOCK ANDROID NOTIFICATION EVENT:")
    print(json.dumps(payload, indent=2))
    print("========================================\n")
    
    result = await orchestrator.process_event(payload)
    
    print("\n========================================")
    print("WORKFLOW EXECUTION RESULT:")
    print(json.dumps(result, indent=2))
    print("========================================")

if __name__ == "__main__":
    asyncio.run(test_workflow())
