# Extending Adapters

The true power of Agentic-Notify is its complete decoupling from external endpoints. The Orchestrator doesn't natively know how to speak to Google Calendar or Stripe—it relies entirely on **Adapters**.

Adapters are your physical tools. When you extend `BaseAdapter`, you automatically register that component with the internal `ToolRegistry`, making it instantly discoverable by the Agentic LLM Planner.

---

## 🛠️ Building a Custom Adapter

To build an interface with a new external system, simply subclass `BaseAdapter` and override the `execute` method.

### Example: Creating a Stripe Payment Adapter

```python
import logging
from typing import Dict, Any
from agentic_notify.adapters.base import BaseAdapter

logger = logging.getLogger(__name__)

class StripeRefundAdapter(BaseAdapter):
    """
    Adapter that interfaces with the Stripe API to issue refunds based on notification context.
    """
    
    @property
    def name(self) -> str:
        # This is the exact keyword the LLM and the Workflow schema will call
        return "issue_stripe_refund"

    async def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        charge_id = payload.get("charge_id")
        amount = payload.get("amount")
        
        if not charge_id:
            raise ValueError("StripeRefundAdapter requires a 'charge_id'.")
            
        logger.info(f"Issuing refund for {charge_id} handling {amount} cents.")
        
        # Insert real `stripe.Refund.create(charge=charge_id)` logic here
        
        return {
            "status": "success",
            "refund_id": "re_12345",
            "processed_amount": amount
        }
```

## 🔌 Registering Your Adapter

Once defined, you must mount it to the active `NotificationOrchestrator` before starting your integrations (like FastAPI).

```python
from agentic_notify.orchestrator import NotificationOrchestrator
from my_custom_code import StripeRefundAdapter

orchestrator = NotificationOrchestrator(...)

# Register it dynamically
orchestrator.register_adapter(StripeRefundAdapter())
```

Once registered, if your `AgenticPlanner` encounters an intent like *"A customer complained about charge ch_999, issue a refund"*, the LLM will automatically generate a step mapped to `issue_stripe_refund` and map the charge ID into the payload!
