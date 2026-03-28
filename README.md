# agentic-notify

A Python library for building **agentic, notification-driven workflows** with pluggable adapters, policy-aware handlers, and scalable integration interfaces for cross-native applications.

## Overview

`agentic-notify` gives you a **backend-first orchestration SDK** with clear extension points:

- **Ingestion & Normalization:** Accept notifications from Android/React Native bridges and convert them to a canonical schema.
- **Agentic Routing:** Send notifications to workflows based on LLM decisions or rules.
- **Workflow Orchestration:** Execute steps safely, handle retries, and check execution policies.
- **Adapters:** Connect your workflow engine to device boundaries (Reminders, Summaries, Local DBs).

## Architecture Approach

- **Schemas define contracts** (via Pydantic)
- **Normalizers unify platforms**
- **Routers decide**
- **Workflows orchestrate**
- **Handlers transform**
- **Adapters act**
- **Integrations connect**
- **Policies constrain**

## Installation

```bash
# Core package
pip install agentic-notify

# Install with FastAPI and Redis support
pip install agentic-notify[fastapi,redis]
```
